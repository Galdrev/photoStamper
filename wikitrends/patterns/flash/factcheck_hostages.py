"""Independent recount of every hostage fact for the card 3 moment, from the raw stored data only.
Does not import build_page.py / build_flash.py; uses its own word lists and sentence splitting.
Run: python3 -I patterns/flash/factcheck_hostages.py .   (from wikitrends/; writes patterns/flash/factcheck_hostages.json)
"""
import gzip, json, os, re, sys

W = sys.argv[1]
D = os.path.join(W, "data")
CL = json.load(open(os.path.join(D, "crosslang.json")))["articles"]
LG = json.load(open(os.path.join(W, "patterns", "langs", "langs.json")))
LA = LG["articles"]
RA = json.load(open(os.path.join(D, "ratchet.json")))["articles"]
M2 = json.load(gzip.open(os.path.join(D, "mass2_leads.json.gz")))["leads"]
LJ = json.load(open(os.path.join(D, "leads.json")))
NW = json.load(open(os.path.join(W, "patterns", "crosswiki", "chart_data", "narrative.json")))["hostages"]

# our own word list (broader than crosswiki.py's: Italian "rapimento", Arabic verb "أسروا"/noun "أسرى", Hebrew "חטיפת")
HOST = {
    "en": r"hostage|captive|abduct|kidnap",
    "de": r"geisel|entführ|verschlepp",
    "fr": r"otage|enlev|kidnapp|captif|captive",
    "es": r"rehén|rehenes|secuestr|cautiv",
    "it": r"ostagg|rapiment|rapit[oiae]|sequestr",
    "pt": r"refém|reféns|sequestr|raptad|rapto",
    "nl": r"gijzel|ontvoer|gevangengenomen",
    "pl": r"zakładni|porwan|uprowadz",
    "ru": r"заложни|похищ|пленн",
    "he": r"חטופ|חטיפ|בני ערובה|בני־ערובה|שבוי",
    "ar": r"رهائن|رهين|أسرى|اسرى|أسروا|اسروا|أسر |مختطف|محتجز|خطف",
}
RX = {l: re.compile(p, re.I) for l, p in HOST.items()}
ORDER = LG["meta"]["lang_order"]
NATIVE = {"he": "עברית", "ar": "العربية", "en": "English", "de": "Deutsch", "fr": "Français", "es": "Español", "it": "Italiano",
          "pt": "Português", "nl": "Nederlands", "pl": "Polski", "ru": "Русский"}


STARTS = ["מתקפת הפתע על ישראל", "טבח שבעה באוקטובר", "Der Terrorangriff", "Der Angriff", "Der Überfall"]


def strip_caption(t):
    """image-caption residue at the head of a held lead (de "mini|...", he "ממוזער|...") is not prose: cut to the first prose start"""
    if re.match(r"\s*(mini|miniatur|thumb|ממוזער)\|", t):
        k = min([t.find(s) for s in STARTS if t.find(s) >= 0] or [0])
        return t[k:]
    return t


def split(t):
    """sentences; a full stop may be followed by a closing quote (Arabic '.»'); no split after a day number ("7. Oktober"),
    a single capital ("J. Smith") or common abbreviations"""
    t = strip_caption(t)
    parts, cur = [], ""
    for tok in re.split(r"(?:(?<=[.!?؟][»\"”’])|(?<=[.!?؟]))\s+", t):
        cur = (cur + " " + tok) if cur else tok
        if re.search(r"(\b\d{1,2}\.|\b[A-ZА-Я]\.|\bca\.|\bz\. ?B\.|\bbzw\.|\bu\. a\.|\bSt\.|\bDr\.|\bv\.)$", cur):
            continue
        parts.append(cur)
        cur = ""
    if cur:
        parts.append(cur)
    return [p.strip() for p in parts if p.strip()]


out = {"first_sentence": {}, "opening_held": {}, "full_lead_counts": {}, "israel_hamas": {}}

# 1. English: every stored version of the October 7 first sentence
V = RA["October 7 attacks"]["fs_variants"]
en_hits = [v["id"] for v in V if RX["en"].search(v.get("s") or "")]
tl = RA["October 7 attacks"]["fs_timeline"]
out["en_versions"] = {"n_versions": len(V), "with_hostage_word": en_hits, "timeline_from": tl[0][0], "timeline_to": tl[-1][0]}
# the 2 Nov 2026 crawl copy (M2 latest) and its sentence 9
o7 = M2["October 7 attacks"][-1]
ss = split(o7)
hs = [i + 1 for i, s in enumerate(ss) if RX["en"].search(s)]
out["en_oct7_latest_crawl"] = {"n_sentences": len(ss), "hostage_sentences": hs, "first_sentence_has": bool(RX["en"].search(ss[0])),
                               "sentence9": ss[8] if len(ss) > 8 else None}
# English opening sections of Israel and Hamas, every copy we hold (mass2 crawl snapshots + leads.json lead0/lead1)
for a in ("Israel", "Hamas"):
    cps = [x for x in M2[a] if x] + [v[k] for v in LJ if v["title"] == a for k in ("lead0", "lead1") if v.get(k)]
    out.setdefault("en_israel_hamas", {})[a] = {"copies": len(cps), "with_hostage_word": sum(1 for c in cps if RX["en"].search(c))}

# 2. Every edition: the October 7 first sentence and opening section, in every quarterly copy we hold (crosslang, 1,200 chars)
for l in ORDER:
    A = CL["October 7 attacks"].get(l)
    S = (LA["October 7 attacks"].get(l) or {}).get("slots", {}).get("s1")
    if not A or not A.get("series"):
        out["first_sentence"][l] = {"held": False}
        continue
    rows = []
    for x in A["series"]:
        ss = split(x["lead"])
        h = [i + 1 for i, s in enumerate(ss) if RX[l].search(s)]
        rows.append({"date": x["date"], "rev": x["revid"], "fs_has": bool(ss and RX[l].search(ss[0])), "held_hits": h, "held_sentences": len(ss)})
    # the curated first sentence (langs.json) of the first and latest copy, checked against the held text and searched
    cur = {}
    for w in ("first", "latest"):
        o = S[w]["orig"]
        lead = next(x["lead"] for x in A["series"] if x["revid"] == S[w]["revid"])
        assert o.strip(" .")[:60] in lead or l in ("fr", "it"), f"{l} {w}: curated first sentence not in the held copy"
        cur[w] = {"date": S[w]["date"], "rev": S[w]["revid"], "has": bool(RX[l].search(o)), "orig": o, "tr": S[w]["tr"], "truncated": S[w]["truncated"]}
    out["first_sentence"][l] = {"held": True, "copies": len(rows), "copies_fs_has": [r["date"] for r in rows if r["fs_has"]], "curated": cur}
    out["opening_held"][l] = rows[-1]
    out["full_lead_counts"][l] = NW.get(l, {}).get("October 7 attacks")

# 3. Israel and Hamas opening sections in every edition: held text (all quarters) and the full-lead counts (4 dates)
for l in ORDER:
    for a in ("Israel", "Hamas"):
        A = CL[a].get(l)
        held = [(x["date"], bool(RX[l].search(x["lead"] or ""))) for x in (A or {}).get("series", [])]
        out["israel_hamas"].setdefault(l, {})[a + "_held"] = {"copies": len(held), "with_hostage_word": [d for d, h in held if h]}
        out["israel_hamas"][l][a + "_full"] = NW.get(l, {}).get(a)

json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "factcheck_hostages.json"), "w"), ensure_ascii=False, indent=1)

# ---- report
print("EN first sentence: %d versions (%s .. %s); versions with a hostage word: %s" % (len(V), tl[0][0], tl[-1][0], en_hits or "none"))
e = out["en_oct7_latest_crawl"]
print("EN Oct 7 opening section, 2 Nov 2026 crawl: %d sentences; hostage sentences %s; sentence 9: %s" % (e["n_sentences"], e["hostage_sentences"], e["sentence9"]))
for a, v in out["en_israel_hamas"].items():
    print(f"EN {a} opening section: {v['copies']} copies, {v['with_hostage_word']} with a hostage word")
print()
n_held = n_has = 0
for l in ORDER:
    f = out["first_sentence"][l]
    if not f["held"]:
        print(f"{l}: no October 7 article held"); continue
    n_held += 1
    c = f["curated"]
    n_has += c["latest"]["has"]
    print(f"{l} {NATIVE[l]}: first sentence latest {c['latest']['date']} rev {c['latest']['rev']} hostages={c['latest']['has']} | first copy {c['first']['date']} hostages={c['first']['has']} | quarterly copies with hostages in sentence 1 (mechanical split): {f['copies_fs_has'] or 'none'} of {f['copies']}")
    oh = out["opening_held"][l]
    print(f"     held 1,200 chars, latest: hostage sentences {oh['held_hits']} of {oh['held_sentences']} held | full lead (crosswiki, 2026-11-08): {(out['full_lead_counts'][l] or {}).get('2026-11-08')}")
print(f"\nFIRST SENTENCE, latest copies: {n_held - n_has} of {n_held} editions without the hostages; {n_has} with")
print()
for l in ORDER:
    v = out["israel_hamas"][l]
    print(l, "Israel held:", v["Israel_held"], "full:", v["Israel_full"])
    print(l, "Hamas  held:", v["Hamas_held"], "full:", v["Hamas_full"])
