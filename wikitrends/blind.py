"""Blind stance coding of lead-section changes (SPEC.md, "Blind stance coding").

  python blind.py prepare OUTDIR [--max N]   -> OUTDIR/batch_XX.json (what coders see) + OUTDIR/key.json (never shown)
  python blind.py score OUTDIR               -> adds `blind` summary into data/results.json

Coders see two versions of an encyclopedia lead (A and B, random order) with
the subject and main entity names masked, and return one label per item.
The key (which version is newer, which article/group) never enters coder context.
"""
import glob, json, os, random, re, sys
from collections import Counter

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

# Names masked in every item (both groups), longest first. Same scheme for all items:
# each distinct name gets [ENTITY-n] consistently within the item.
NAMES = """
Israeli-occupied|Israel Defense Forces|Israelis|Israeli|Israel|Zionists|Zionist|Zionism|Anti-Zionism|anti-Zionist|anti-Zionism
Jewish|Jews|Jew|Judaism|Judaic|Hebrew|Yishuv|Eretz Israel|Land of Israel|Aliyah|Knesset|IDF|Mossad|Haganah|Irgun|Likud|Netanyahu|Ben-Gurion|Herzl
Palestinians|Palestinian|Palestine|Hamas|Hezbollah|PLO|Fatah|Gaza Strip|Gaza|West Bank|East Jerusalem|Jerusalem|Tel Aviv|Golan Heights|Golan|Nakba|Intifada
Arabs|Arab|Ottoman|British Mandate|Mandatory
Kurds|Kurdish|Kurdistan|Turks|Turkish|Turkey|Armenians|Armenian|Armenia|Azerbaijani|Azerbaijan|Karabakh|Artsakh
Hindus|Hindu|Hindutva|Muslims|Muslim|Islamic|Islam|Indians|Indian|India|Pakistanis|Pakistani|Pakistan|Kashmiri|Kashmir
Irish|Ireland|Ulster|Unionist|Republican|Basques|Basque|Catalans|Catalan|Catalonia|Spanish|Spain
Ukrainians|Ukrainian|Ukraine|Russians|Russian|Russia|Crimea|Donbas|Poles|Polish|Poland|Greeks|Greek|Greece|Cypriots|Cypriot|Cyprus
Tibetans|Tibetan|Tibet|Uyghurs|Uyghur|Xinjiang|Chinese|China|Taiwanese|Taiwan|Rohingya|Myanmar|Darfur|Sudanese|Sudan|Tigray|Ethiopian|Ethiopia
Sahrawi|Western Sahara|Moroccan|Morocco|Algerians|Algerian|Algeria|French|France|Aboriginal|Australian|Australia|Māori|Native Americans|Canadian|Canada
Christians|Christian|Christianity|Catholics|Catholic|Orthodox|Sikhs|Sikh|Buddhists|Buddhist|Druze|Copts|Coptic|Romani|Roma
""".replace("\n", "|").strip("|").split("|")
NAMES = sorted({n for n in NAMES if n}, key=len, reverse=True)

RUBRIC_VERSION = "v1"


def mask(text, extra):
    names = sorted(set(NAMES) | {e for e in extra if len(e) > 3}, key=len, reverse=True)
    mapping = {}
    def sub(m):
        key = m.group(0).lower()
        if key not in mapping:
            mapping[key] = f"[ENTITY-{len(mapping) + 1}]"
        return mapping[key]
    rx = re.compile(r"\b(?:" + "|".join(re.escape(n) for n in names) + r")\b", re.I)
    return rx.sub(sub, text), mapping


def title_terms(title):
    t = re.sub(r"\(.*?\)", "", title)
    return [w for w in re.split(r"[\s–\-:,]+", t) if w and w[0].isupper() and w.lower() not in
            {"the", "of", "and", "in", "on", "list", "history", "war", "state", "people", "genocide"}]


def clip(t, n=2500):
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + " …"


def prepare(outdir, max_items=260, batch=40, seed=11):
    rnd = random.Random(seed)
    leads = [x for x in json.load(open(os.path.join(DATA, "leads.json"))) if x["primary"]]
    topic = [x for x in leads if x["group"] == "treatment"]
    ctrl = [x for x in leads if x["group"] == "control"]
    # keep all comparison items; sample topic down to fill the budget
    n_topic = max(0, min(len(topic), max_items - len(ctrl)))
    items = rnd.sample(topic, n_topic) + ctrl
    # unmasked repeat (placebo for identity sensitivity): 15 topic + 15 comparison items shown again WITHOUT masking
    swaps = [dict(x, placebo_swap=True) for x in rnd.sample(items[:n_topic], min(15, n_topic)) + rnd.sample(ctrl, min(15, len(ctrl)))]
    pool = [dict(x, placebo_swap=False) for x in items] + swaps
    rnd.shuffle(pool)
    key, coder_items = {}, []
    for i, x in enumerate(pool):
        iid = f"I{i:04d}"
        newer_is_b = rnd.random() < 0.5
        extra = title_terms(x["title"])
        a_txt, b_txt = (x["lead0"], x["lead1"]) if newer_is_b else (x["lead1"], x["lead0"])
        if x["placebo_swap"]:
            ma, mb = clip(a_txt), clip(b_txt)
        else:
            ma, _ = mask(clip(a_txt), extra); mb, _ = mask(clip(b_txt), extra)
        coder_items.append({"id": iid, "A": ma, "B": mb})
        key[iid] = {"title": x["title"], "group": x["group"], "newer_is_b": newer_is_b,
                    "placebo_swap": x["placebo_swap"], "rev0": x["rev0"], "rev1": x["rev1"], "d0": x["d0"], "d1": x["d1"]}
    os.makedirs(outdir, exist_ok=True)
    for b in range(0, len(coder_items), batch):
        json.dump(coder_items[b:b + batch], open(os.path.join(outdir, f"batch_{b // batch:02d}.json"), "w"), ensure_ascii=False, indent=0)
    json.dump(key, open(os.path.join(outdir, "key.json"), "w"))
    print(f"{len(coder_items)} items ({n_topic} topic, {len(ctrl)} comparison, {len(swaps)} unmasked repeat) "
          f"in {(len(coder_items) + batch - 1) // batch} batches")


# Labels coders may return. Direction is about version B relative to version A.
LABELS = {"B_less_favourable", "B_more_favourable", "no_stance_change", "unclear"}
KINDS = {"framing", "factual_update", "both", "none"}


def score(outdir):
    key = json.load(open(os.path.join(outdir, "key.json")))
    codings = {}  # iid -> list of (coder, newer_label, kind, quote)
    for fn in sorted(glob.glob(os.path.join(outdir, "codes_*.json"))):
        coder = os.path.basename(fn)[6:-5].rsplit("_b", 1)[0]
        for r in json.load(open(fn)):
            iid, lab = r.get("id"), r.get("label")
            if iid not in key or lab not in LABELS:
                continue
            k = key[iid]
            # translate "B vs A" into "newer vs older"
            if lab in ("B_less_favourable", "B_more_favourable"):
                b_less = lab == "B_less_favourable"
                newer_less = b_less if k["newer_is_b"] else not b_less
                lab = "newer_less_favourable" if newer_less else "newer_more_favourable"
            codings.setdefault(iid, []).append((coder, lab, r.get("kind"), r.get("quote", "")))
    coders = sorted({c for v in codings.values() for c, *_ in v})

    def majority(v):
        c = Counter(l for _, l, *_ in v).most_common()
        return c[0][0] if c and (len(c) == 1 or c[0][1] > c[1][1]) else "unclear"
    final = {iid: majority(v) for iid, v in codings.items()}

    def share(group, swap=False, lab="newer_less_favourable"):
        ids = [i for i in final if key[i]["group"] == group and key[i]["placebo_swap"] == swap]
        return (sum(final[i] == lab for i in ids) / len(ids) if ids else None), ids

    lt, ids_t = share("treatment"); lc, ids_c = share("control")
    mt, _ = share("treatment", lab="newer_more_favourable"); mc, _ = share("control", lab="newer_more_favourable")
    # permutation p-value on the difference in "less favourable" shares
    y = np.array([final[i] == "newer_less_favourable" for i in ids_t + ids_c], float)
    nt = len(ids_t); obs = y[:nt].mean() - y[nt:].mean() if nt and len(ids_c) else None
    p = None
    if obs is not None:
        rng = np.random.default_rng(3); perm = []
        for _ in range(5000):
            rng.shuffle(y); perm.append(y[:nt].mean() - y[nt:].mean())
        p = float((np.sum(np.abs(perm) >= abs(obs)) + 1) / 5001)
    # agreement: share of items where all coders agree; pairwise agreement per coder pair
    full_agree = np.mean([len({l for _, l, *_ in v}) == 1 for v in codings.values() if len(v) > 1]) if codings else None
    pair = {}
    for a in coders:
        for b in coders:
            if a < b:
                both = [(dict((c, l) for c, l, *_ in v)) for v in codings.values()]
                both = [d for d in both if a in d and b in d]
                if both:
                    pair[f"{a} vs {b}"] = float(np.mean([d[a] == d[b] for d in both]))
    # unmasked repeat: does seeing real names change the label? (per group)
    orig = {key[i]["title"]: final[i] for i in final if not key[i]["placebo_swap"]}
    flips_by = {}
    for g in ("treatment", "control"):
        sw = [i for i in final if key[i]["placebo_swap"] and key[i]["group"] == g and key[i]["title"] in orig]
        flips_by[g] = [final[i] != orig[key[i]["title"]] for i in sw]
    flips = flips_by["treatment"] + flips_by["control"]
    kinds = {}
    for g in ("treatment", "control"):
        ks = Counter()
        for i, v in codings.items():
            if key[i]["group"] == g and not key[i]["placebo_swap"]:
                ks[Counter(kd for _, _, kd, _ in v).most_common(1)[0][0]] += 1
        kinds[g] = dict(ks)
    examples = []
    for i in ids_t + ids_c:
        if final[i] in ("newer_less_favourable", "newer_more_favourable"):
            q = next((qq for _, l, _, qq in codings[i] if l == final[i] and qq), "")
            examples.append({"title": key[i]["title"], "group": key[i]["group"], "label": final[i], "quote": q[:400],
                             "rev0": key[i]["rev0"], "rev1": key[i]["rev1"], "d0": key[i]["d0"], "d1": key[i]["d1"]})
    blind = {"rubric": RUBRIC_VERSION, "coders": coders, "n_items": len(final), "n_topic": len(ids_t), "n_control": len(ids_c),
             "share_less_favourable_topic": lt, "share_less_favourable_control": lc,
             "share_more_favourable_topic": mt, "share_more_favourable_control": mc,
             "diff": obs, "p_perm": p, "all_coders_agree": None if full_agree is None else float(full_agree),
             "pairwise_agreement": pair,
             "unmasked_repeat_items": len(flips),
             "unmasked_flip_rate_topic": float(np.mean(flips_by["treatment"])) if flips_by["treatment"] else None,
             "unmasked_flip_rate_control": float(np.mean(flips_by["control"])) if flips_by["control"] else None,
             "framing_vs_factual": kinds, "examples": examples,
             "label_counts": {g: dict(Counter(final[i] for i in ids)) for g, ids in (("treatment", ids_t), ("control", ids_c))}}
    rp = os.path.join(DATA, "results.json")
    res = json.load(open(rp)); res["blind"] = blind
    json.dump(res, open(rp, "w"))
    json.dump(blind, open(os.path.join(outdir, "blind_summary.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in blind.items() if k != "examples"}, indent=1))


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        mx = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 260
        prepare(sys.argv[2], mx)
    else:
        score(sys.argv[2])
