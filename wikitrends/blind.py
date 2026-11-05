"""Blind stance coding, v2 (SPEC amendment 3).

  python blind.py prepare OUTDIR [--max N] [--pilot 20]
      -> OUTDIR/shard_XX.json   what coders see (mixed topic/comparison, anchors in random positions)
         OUTDIR/calib.json      synthetic known-answer pairs (also mixed into shards)
         OUTDIR/reid.json       30 masked topic items: can a model re-identify the subject? (blinding check)
         OUTDIR/key.json        hidden key (never shown to coders)
  python blind.py score OUTDIR  -> OUTDIR/blind_summary.json, and `blind` merged into data/results.json

Design (from the method revisit):
  - every real item is coded in BOTH orders (A/B swapped), by different coders/shards; disagreement -> unclear
  - 4 fixed anchors per shard (2 known-direction, 1 identical pair, 1 date-only change) to detect drift
  - synthetic known-answer calibration items made by controlled single edits on comparison leads
  - number/date-only diffs are settled in code (no LLM)
  - quotes are verified verbatim against the item text
"""
import glob, json, os, random, re, sys
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
RUBRIC_VERSION = "v2"

NAMES = """
Israeli-occupied|Israel Defense Forces|Israelis|Israeli|Israel|Zionists|Zionist|Zionism|Anti-Zionism|anti-Zionist|anti-Zionism
Jewish|Jewry|Jews|Jew|Zion|Judaism|Judaic|Hebrew|Yishuv|Eretz Israel|Land of Israel|Aliyah|Knesset|IDF|Mossad|Haganah|Irgun|Likud|Netanyahu|Ben-Gurion|Herzl
Palestinians|Palestinian|Palestine|Hamas|Hezbollah|PLO|Fatah|Gaza Strip|Gaza|West Bank|East Jerusalem|Jerusalem|Tel Aviv|Golan Heights|Golan|Nakba|Intifada
Arabs|Arab|Ottoman|British Mandate|Mandatory|Holocaust|Shoah|Torah|Talmud|rabbinic|rabbis|rabbi|synagogue|Sephardic|Ashkenazi|Mizrahi|kibbutz|Levant|Sinai|Lebanon|Syria|Jordan|Egypt|Iran
Kurds|Kurdish|Kurdistan|Turks|Turkish|Turkey|Armenians|Armenian|Armenia|Azerbaijani|Azerbaijan|Karabakh|Artsakh
Hindus|Hindu|Hindutva|Muslims|Muslim|Islamic|Islam|Indians|Indian|India|Pakistanis|Pakistani|Pakistan|Kashmiri|Kashmir
Irish|Ireland|Ulster|Unionist|Republican|Basques|Basque|Catalans|Catalan|Catalonia|Spanish|Spain
Ukrainians|Ukrainian|Ukraine|Russians|Russian|Russia|Crimea|Donbas|Poles|Polish|Poland|Greeks|Greek|Greece|Cypriots|Cypriot|Cyprus
Tibetans|Tibetan|Tibet|Uyghurs|Uyghur|Xinjiang|Chinese|China|Taiwanese|Taiwan|Rohingya|Myanmar|Darfur|Sudanese|Sudan|Tigray|Ethiopian|Ethiopia
Sahrawi|Western Sahara|Moroccan|Morocco|Algerians|Algerian|Algeria|French|France|Aboriginal|Australian|Australia|Māori|Native Americans|Canadian|Canada
Christians|Christian|Christianity|Catholics|Catholic|Orthodox|Sikhs|Sikh|Buddhists|Buddhist|Druze|Copts|Coptic|Romani|Roma|British|Britain|United Kingdom|United States|American
""".replace("\n", "|").strip("|").split("|")
NAMES = sorted({n for n in NAMES if n}, key=len, reverse=True)
LABELS = {"B_less_favourable", "B_more_favourable", "no_stance_change", "unclear"}


def mask(text, extra):
    names = sorted(set(NAMES) | {e for e in extra if len(e) > 3}, key=len, reverse=True)
    mapping = {}
    def sub(m):
        k = m.group(0).lower()
        mapping.setdefault(k, f"[ENTITY-{len(mapping) + 1}]")
        return mapping[k]
    return re.compile(r"\b(?:" + "|".join(re.escape(n) for n in names) + r")\b", re.I).sub(sub, text)


def title_terms(title):
    t = re.sub(r"\(.*?\)", "", title)
    return [w for w in re.split(r"[\s–\-:,]+", t) if w and w[0].isupper() and w.lower() not in
            {"the", "of", "and", "in", "on", "list", "history", "war", "state", "people", "genocide"}]


def clip(t, n=2200):
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + " …"


def numeric_only(a, b):
    norm = lambda s: re.sub(r"\s+", " ", re.sub(r"\d[\d,. ]*", "#", s)).strip()
    return norm(a) == norm(b)


# ---- synthetic known-answer edits (applied to a neutral comparison lead) ------------------------------
EDITS = [
    ("neg_label", "B_less_favourable", lambda s: re.sub(r"\.\s*$", ", widely condemned as extremist.", s, count=1)),
    ("pos_label", "B_more_favourable", lambda s: re.sub(r"\.\s*$", ", widely praised as a model of tolerance.", s, count=1)),
    ("hedge_removed", "B_less_favourable", None),   # A: "accused of" sentence  -> B: stated as fact
    ("hedge_added", "B_more_favourable", None),     # reverse
    ("date_change", "no_stance_change", None),
]


def make_calibration(leads, rnd, n=30):
    out = []
    pool = [x for x in leads if x["group"] == "control" and len(x["lead1"]) > 300]
    for i in range(n):
        x = rnd.choice(pool)
        base = mask(clip(x["lead1"], 900), title_terms(x["title"]))
        sents = re.split(r"(?<=[.!?])\s+", base)
        first, rest = sents[0], " ".join(sents[1:])
        kind, want, fn = EDITS[i % len(EDITS)]
        if kind in ("neg_label", "pos_label"):
            a, b = base, fn(first) + " " + rest
        elif kind == "hedge_removed":
            a = base + " It has been accused of committing serious abuses against civilians."
            b = base + " It committed serious abuses against civilians."
        elif kind == "hedge_added":
            a = base + " It committed serious abuses against civilians."
            b = base + " It has been accused of committing serious abuses against civilians."
        else:
            a = base + " It had about 2.1 million members in 2019."
            b = base + " It had about 2.4 million members in 2024."
        out.append({"A": a, "B": b, "want": want, "edit": kind})
    return out


ANCHORS = [
    {"A": "[ENTITY-1] is a trade union founded in 1921 that represents dock workers.",
     "B": "[ENTITY-1] is a trade union founded in 1921 that represents dock workers, and has been widely condemned for violent intimidation of members.",
     "want": "B_less_favourable"},
    {"A": "[ENTITY-1] is a charity that has been accused of misusing donations.",
     "B": "[ENTITY-1] is a charity, recognised by several governments for its relief work.",
     "want": "B_more_favourable"},
    {"A": "[ENTITY-1] is a mountain range in the north of [ENTITY-2], rising to 3,100 metres.",
     "B": "[ENTITY-1] is a mountain range in the north of [ENTITY-2], rising to 3,100 metres.",
     "want": "no_stance_change"},
    {"A": "[ENTITY-1] is a city with a population of 412,000 (2015 census).",
     "B": "[ENTITY-1] is a city with a population of 436,000 (2023 census).",
     "want": "no_stance_change"},
]


def prepare(outdir, max_items=260, shard_real=12, pilot=0, seed=11):
    rnd = random.Random(seed)
    leads = [x for x in json.load(open(os.path.join(DATA, "leads.json"))) if x["primary"]]
    topic = [x for x in leads if x["group"] == "treatment"]; ctrl = [x for x in leads if x["group"] == "control"]
    n_topic = max(0, min(len(topic), max_items - len(ctrl)))
    items = rnd.sample(topic, n_topic) + ctrl
    if pilot:
        items = rnd.sample(topic, pilot // 2) + rnd.sample(ctrl, pilot - pilot // 2)
    key, auto, real = {}, {}, []
    for i, x in enumerate(items):
        base = f"R{i:04d}"
        if numeric_only(x["lead0"], x["lead1"]):
            auto[base] = {"title": x["title"], "group": x["group"], "label": "no_stance_change", "kind": "factual_update"}
            continue
        extra = title_terms(x["title"])
        old, new = mask(clip(x["lead0"]), extra), mask(clip(x["lead1"]), extra)
        for o in (0, 1):                      # o=0: A=old,B=new ; o=1: A=new,B=old
            iid = f"{base}{'ab'[o]}"
            real.append({"id": iid, "A": old if o == 0 else new, "B": new if o == 0 else old})
            key[iid] = {"base": base, "orient": o, "type": "real", "title": x["title"], "group": x["group"],
                        "rev0": x["rev0"], "rev1": x["rev1"], "d0": x["d0"], "d1": x["d1"]}
    calib = make_calibration(leads, rnd, 0 if pilot else 30)
    for i, c in enumerate(calib):
        for o in (0, 1):
            iid = f"C{i:03d}{'ab'[o]}"
            flip = {"B_less_favourable": "B_more_favourable", "B_more_favourable": "B_less_favourable"}
            real.append({"id": iid, "A": c["A"] if o == 0 else c["B"], "B": c["B"] if o == 0 else c["A"]})
            key[iid] = {"base": f"C{i:03d}", "orient": o, "type": "calib", "edit": c["edit"],
                        "want": c["want"] if o == 0 else flip.get(c["want"], c["want"])}
    # shards: orientation a and b of the same base go to different shards
    a_items = [r for r in real if r["id"].endswith("a")]; b_items = [r for r in real if r["id"].endswith("b")]
    rnd.shuffle(a_items); rnd.shuffle(b_items)
    shards = [a_items[i:i + shard_real] for i in range(0, len(a_items), shard_real)] + \
             [b_items[i:i + shard_real] for i in range(0, len(b_items), shard_real)]
    os.makedirs(outdir, exist_ok=True)
    for f in glob.glob(os.path.join(outdir, "shard_*.json")):
        os.remove(f)
    for s_i, sh in enumerate(shards):
        sh = list(sh)
        for a_i, an in enumerate(ANCHORS):
            iid = f"N{s_i:02d}{a_i}"
            o = rnd.random() < 0.5
            flip = {"B_less_favourable": "B_more_favourable", "B_more_favourable": "B_less_favourable"}
            sh.insert(rnd.randrange(len(sh) + 1), {"id": iid, "A": an["B"] if o else an["A"], "B": an["A"] if o else an["B"]})
            key[iid] = {"type": "anchor", "shard": s_i, "want": flip.get(an["want"], an["want"]) if o else an["want"]}
        json.dump(sh, open(os.path.join(outdir, f"shard_{s_i:02d}.json"), "w"), ensure_ascii=False, indent=0)
    reid_src = rnd.sample(topic, min(30, len(topic)))
    reid = [{"id": f"Q{i:02d}", "text": mask(clip(x["lead1"], 1200), title_terms(x["title"]))} for i, x in enumerate(reid_src)]
    for i, x in enumerate(reid_src):
        key[f"Q{i:02d}"] = {"type": "reid", "title": x["title"]}
    json.dump(reid, open(os.path.join(outdir, "reid.json"), "w"), ensure_ascii=False, indent=0)
    json.dump({"key": key, "auto": auto, "rubric": RUBRIC_VERSION}, open(os.path.join(outdir, "key.json"), "w"))
    print(f"{len(items)} real items ({len(auto)} settled in code), {len(calib)} calibration, "
          f"{len(shards)} shards of ~{shard_real}+{len(ANCHORS)} anchors, {len(reid)} re-identification items")


def score(outdir):
    K = json.load(open(os.path.join(outdir, "key.json"))); key, auto = K["key"], K["auto"]
    shard_text = {}
    for f in glob.glob(os.path.join(outdir, "shard_*.json")):
        for it in json.load(open(f)):
            shard_text[it["id"]] = it
    codes, bad_quote, invalid = {}, 0, 0
    for f in sorted(glob.glob(os.path.join(outdir, "codes_*.json"))):
        try:
            rows = json.load(open(f))
        except json.JSONDecodeError:
            invalid += 1; continue
        for r in rows:
            iid = r.get("id")
            if iid not in key or r.get("label") not in LABELS:
                invalid += 1; continue
            q = (r.get("quote") or "").strip()
            m = re.match(r"^(A|B):\s*(.*)$", q, re.S)
            ok = bool(m) and m.group(2).strip(" .…\"'") and m.group(2).strip(" .…\"'") in shard_text.get(iid, {}).get(m.group(1), "")
            lab = r["label"]
            if lab in ("B_less_favourable", "B_more_favourable") and not ok:
                bad_quote += 1; lab = "unclear"          # unsupported directional label
            codes[iid] = {"label": lab, "kind": r.get("kind"), "conf": r.get("confidence"), "quote": q}
    flip = {"B_less_favourable": "B_more_favourable", "B_more_favourable": "B_less_favourable"}

    def to_newer(iid):
        c = codes.get(iid)
        if not c:
            return None
        lab = c["label"]
        return flip.get(lab, lab) if key[iid].get("orient") == 1 else lab

    # anchors
    anc = [(k, codes[k]["label"] == v["want"]) for k, v in key.items() if v["type"] == "anchor" and k in codes]
    by_shard = defaultdict(list)
    for k, ok in anc:
        by_shard[key[k]["shard"]].append(ok)
    # calibration (both orientations)
    cal = [(v, codes[k]["label"]) for k, v in key.items() if v["type"] == "calib" and k in codes]
    cal_acc = float(np.mean([lab == v["want"] for v, lab in cal])) if cal else None
    cal_by_edit = defaultdict(list)
    for v, lab in cal:
        cal_by_edit[v["edit"]].append(lab == v["want"])
    # real items: reconcile orientations
    bases = defaultdict(dict)
    for k, v in key.items():
        if v["type"] == "real":
            bases[v["base"]][v["orient"]] = to_newer(k)
    final, swap_ok = {}, []
    for b, d in bases.items():
        if 0 in d and 1 in d and d[0] and d[1]:
            swap_ok.append(d[0] == d[1])
            final[b] = d[0] if d[0] == d[1] else "unclear"
        elif d.get(0) or d.get(1):
            final[b] = "unclear"
    meta = {v["base"]: v for v in key.values() if v["type"] == "real"}
    for b, v in auto.items():
        final[b] = "no_stance_change"; meta[b] = v
    def share(g, lab):
        ids = [b for b in final if meta[b]["group"] == g]
        return (sum(final[b] == lab for b in ids) / len(ids) if ids else None), ids
    lt, ids_t = share("treatment", "B_less_favourable"); lc, ids_c = share("control", "B_less_favourable")
    mt, _ = share("treatment", "B_more_favourable"); mc, _ = share("control", "B_more_favourable")
    # net = less - more, per item in {-1,0,1}
    val = lambda b: 1 if final[b] == "B_less_favourable" else -1 if final[b] == "B_more_favourable" else 0
    yt, yc = np.array([val(b) for b in ids_t], float), np.array([val(b) for b in ids_c], float)
    diff = p = None
    if len(yt) and len(yc):
        diff = float(yt.mean() - yc.mean()); pool = np.concatenate([yt, yc]); rng = np.random.default_rng(3); perm = []
        for _ in range(5000):
            rng.shuffle(pool); perm.append(pool[:len(yt)].mean() - pool[len(yt):].mean())
        p = float((np.sum(np.abs(perm) >= abs(diff)) + 1) / 5001)
    # re-identification
    rp = os.path.join(outdir, "reid_codes.json"); reid = None
    if os.path.exists(rp):
        g = json.load(open(rp))
        norm = lambda s: re.sub(r"[^a-z0-9 ]", "", (s or "").lower()).strip()
        exact = []
        for x in g:
            a, q = norm(key.get(x["id"], {}).get("title")), norm(x.get("guess"))
            exact.append(bool(a) and (a == q or a in q or q in a))
        reid = {"n": len(exact), "share_exact_article_named": float(np.mean(exact)) if exact else None,
                "note": "Masking names does not blind a model that has read Wikipedia: treat coding as masked, not blind."}
    examples = []
    for b in ids_t + ids_c:
        if final[b] in ("B_less_favourable", "B_more_favourable") and b in meta and "rev0" in meta[b]:
            q = codes.get(b + "a", {}).get("quote") or ""
            examples.append({"title": meta[b]["title"], "group": meta[b]["group"],
                             "label": "newer_less_favourable" if final[b] == "B_less_favourable" else "newer_more_favourable",
                             "quote": q[:400], "rev0": meta[b]["rev0"], "rev1": meta[b]["rev1"], "d0": meta[b]["d0"], "d1": meta[b]["d1"]})
    kinds = {g: dict(Counter((codes.get(b + "a") or {}).get("kind") for b in final if meta[b]["group"] == g)) for g in ("treatment", "control")}
    blind = {"rubric": RUBRIC_VERSION, "n_items": len(final), "n_topic": len(ids_t), "n_control": len(ids_c),
             "settled_in_code": len(auto), "share_less_favourable_topic": lt, "share_less_favourable_control": lc,
             "share_more_favourable_topic": mt, "share_more_favourable_control": mc,
             "net_less_minus_more_diff": diff, "p_perm": p,
             "swap_consistency": float(np.mean(swap_ok)) if swap_ok else None,
             "anchor_accuracy": float(np.mean([ok for _, ok in anc])) if anc else None,
             "anchor_accuracy_min_shard": float(min(np.mean(v) for v in by_shard.values())) if by_shard else None,
             "calibration_accuracy": cal_acc, "calibration_by_edit": {k: float(np.mean(v)) for k, v in cal_by_edit.items()},
             "unsupported_quotes_downgraded": bad_quote, "invalid_rows": invalid, "reidentification": reid,
             "framing_vs_factual": kinds, "examples": examples,
             "gate_passed": bool(cal_acc is not None and cal_acc >= 0.8 and (not anc or np.mean([ok for _, ok in anc]) >= 0.9))}
    json.dump(blind, open(os.path.join(outdir, "blind_summary.json"), "w"), indent=1)
    json.dump({b: {"final": final[b], **{k: meta[b].get(k) for k in ("title", "group", "rev0", "rev1", "d0", "d1")}}
               for b in final}, open(os.path.join(outdir, "finals.json"), "w"))
    rp2 = os.path.join(DATA, "results.json")
    if os.path.exists(rp2):
        res = json.load(open(rp2)); res["blind"] = blind; json.dump(res, open(rp2, "w"))
    print(json.dumps({k: v for k, v in blind.items() if k != "examples"}, indent=1))


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        g = lambda f, d: int(sys.argv[sys.argv.index(f) + 1]) if f in sys.argv else d
        prepare(sys.argv[2], g("--max", 260), pilot=g("--pilot", 0))
    else:
        score(sys.argv[2])
