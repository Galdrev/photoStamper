"""Study 2: competing narratives (SPEC_NARRATIVE.md). Runs on the raw article cache (CI).

  python narrative.py -> data/narrative.json

Sentence-level attribution: a frame term is attributed to the group whose term is nearest to it within the same
sentence. Measures N1-N8 are computed per article per quarterly snapshot, for the topic (Jewish/Israeli J vs
Palestinian/Arab P) and for comparison disputes (group A vs group B) where the measure generalises.
"""
import glob, gzip, json, os, random, re
from collections import Counter, defaultdict

import numpy as np

import analyze as A
from corpus import NARRATIVE_DISPUTES, SHARED_SITES

R = lambda p: re.compile(p, re.I)
TOPIC_GROUPS = {"J": R(r"\b(?:jews?|jewish|jewry|israelites?|hebrews?|judeans?|israelis?|zionists?)\b"),
                "P": R(r"\b(?:palestinians?|palestinian arabs?|arabs?)\b")}
INDIG = R(r"\b(?:indigenous|natives?|native (?:inhabitants|people|population)|original inhabitants|aboriginal|autochthonous|"
          r"descendants? of (?:the )?(?:ancient|canaanites?|israelites?|original)|indigeneity)\b")
PERIOD = R(r"\b(?:bronze age|iron age|first temple|second temple|hasmonean|maccabe\w*|herod\w*|babylonian exile|"
           r"\d{1,4}\s?bce|bce\b|before the common era|kingdom of (?:israel|judah)|roman judaea|achaemenid|persian period)\b")
LAND_J = R(r"\b(?:land of israel|eretz israel|kingdoms? of (?:israel|judah)|judaea|judea|canaan|israel|judah|samaria|yehud)\b")
LAND_P = R(r"\bpalestin(?:e|ian)\b")
TEMPLE_MOUNT = R(r"\btemple mount\b")
HARAM = R(r"\b(?:haram al-sharif|al-haram al-sharif|al-aqsa (?:compound|mosque compound)|noble sanctuary)\b")
DISP_P = R(r"\b(?:nakba|palestinian (?:refugees?|exodus|expulsions?|displacement|flight)|1948 palestinian expulsion)\b")
DISP_J = R(r"\b(?:jewish exodus|jewish refugees|expulsions? of (?:the )?jews from (?:arab|muslim)\w*|jews (?:from|of) arab (?:countries|lands|states)|"
           r"farhud|mizrahi refugees|exodus of jews from)\b")
Y1948 = R(r"\b1948\b|\bwar of independence\b|\bnakba\b")
FORCED = R(r"\b(?:expelled|expulsions?|forced (?:out|to (?:leave|flee))|driven out|ethnically cleansed|ethnic cleansing|depopulated|deported)\b")
FLIGHT = R(r"\b(?:fled|flight|left|evacuated|abandoned|emigrated)\b")
VIOL = R(r"\b(?:terroris[mt]s?|terror attacks?|massacres?)\b")
ACT_P = R(r"\b(?:palestinians?|hamas|plo|fatah|islamic jihad|pflp|fedayeen|arab (?:gunmen|militants|rioters|forces)|hezbollah)\b")
ACT_I = R(r"\b(?:israel(?:i|is)?|idf|israel defense forces|irgun|lehi|haganah|settlers?|jewish (?:militants|underground|terrorists)|kach|kahane)\b")
TERRIT = R(r"\b(?:west bank|east jerusalem|gaza|golan|judea and samaria|the territories)\b")
OCC = R(r"\boccup(?:ied|ation|ying)\b")
DISPUTED = R(r"\bdisputed\b")
SOP = R(r"\bstate of palestine\b")
SOP_COUNTRY = R(r"state of palestine[^.]{0,40}\bis a (?:country|state|sovereign)")
SOP_CLAIM = R(r"state of palestine[^.]{0,80}\b(?:claimed|proclaimed|de jure|partially recognized|aspir\w+|declared)\b")
LANDCONF = R(r"\b(?:land|territor\w*|borders?|war|conflict|occupation|settlements?|refugees?|homeland|sovereignty|annex\w*|partition|ceasefire|intifada|nakba)\b")
JEWISH_HIST = R(r"\b(?:jewish|jews|israelites?|hebrews?|judaism|temple|kingdom of (?:israel|judah)|judean)\b")


def nearest(text, pos, groups):
    """Group whose term is nearest to character position pos within the sentence."""
    best, bd = None, 10 ** 9
    for g, rx in groups.items():
        for m in rx.finditer(text):
            d = abs(m.start() - pos)
            if d < bd:
                best, bd = g, d
    return best


def snapshot_measures(full_wt, groups, is_topic):
    fp = A.prose(full_wt); lp = A.prose(A.split_lead(full_wt))
    words = max(1, len(re.findall(r"\w+", fp)))
    sents = A.sentences(fp)
    c = Counter(); samples = defaultdict(list)
    for s in sents:
        for m in INDIG.finditer(s):
            g = nearest(s, m.start(), groups)
            if g: c[f"N1_{g}"] += 1; samples["N1"].append((g, s[:300]))
        if is_topic:
            if PERIOD.search(s):
                c["N2_J"] += len(LAND_J.findall(s)); c["N2_P"] += len(LAND_P.findall(s))
                if LAND_P.search(s): samples["N2"].append(("P", s[:300]))
            if Y1948.search(s) and TOPIC_GROUPS["P"].search(s):
                f, l = len(FORCED.findall(s)), len(FLIGHT.findall(s))
                c["N5_forced"] += f; c["N5_flight"] += l
                if f or l: samples["N5"].append(("forced" if f >= l else "flight", s[:300]))
            for m in VIOL.finditer(s):
                g = nearest(s, m.start(), {"P": ACT_P, "I": ACT_I})
                if g: c[f"N6_{g}"] += 1; samples["N6"].append((g, s[:300]))
            if TERRIT.search(s):
                c["N7_occ"] += len(OCC.findall(s)); c["N7_disp"] += len(DISPUTED.findall(s))
        else:
            for m in VIOL.finditer(s):
                g = nearest(s, m.start(), groups)
                if g: c[f"N6_{g}"] += 1
    if is_topic:
        c["N4_P"] = len(DISP_P.findall(fp)); c["N4_J"] = len(DISP_J.findall(fp))
        tm, hr = TEMPLE_MOUNT.search(fp), HARAM.search(fp)
        if tm and hr:
            c["N3_both"] = 1; c["N3_tm_first"] = int(tm.start() < hr.start())
        if SOP.search(fp):
            c["N7_sop_country"] = len(SOP_COUNTRY.findall(fp)); c["N7_sop_claim"] = len(SOP_CLAIM.findall(fp))
        c["N8_jewish_in_lead"] = int(bool(JEWISH_HIST.search(lp)))
    c["_words"] = words
    for g, rx in groups.items():
        c[f"G_{g}"] = len(rx.findall(fp))
    c["LANDCONF"] = len(LANDCONF.findall(fp))
    return c, samples


def share(c, a, b):
    t = c.get(a, 0) + c.get(b, 0)
    return c.get(a, 0) / t if t else None


MEASURES = {  # name -> function(counter) -> value (share or rate)
    "N1_indigeneity_share_J": lambda c: share(c, "N1_J", "N1_P"),
    "N2_ancient_naming_share_P": lambda c: share(c, "N2_P", "N2_J"),
    "N3_temple_mount_first": lambda c: c.get("N3_tm_first") if c.get("N3_both") else None,
    "N4_displacement_share_P": lambda c: share(c, "N4_P", "N4_J"),
    "N4_rate_P": lambda c: c.get("N4_P", 0) * 1e4 / c["_words"],
    "N4_rate_J": lambda c: c.get("N4_J", 0) * 1e4 / c["_words"],
    "N5_forced_share": lambda c: share(c, "N5_forced", "N5_flight"),
    "N6_violence_share_israeli": lambda c: share(c, "N6_I", "N6_P"),
    "N7_occupied_share": lambda c: share(c, "N7_occ", "N7_disp"),
    "N7_sop_country_share": lambda c: share(c, "N7_sop_country", "N7_sop_claim"),
    "N8_jewish_history_in_lead": lambda c: c.get("N8_jewish_in_lead"),
}
CONTROL_MEASURES = {"N1_indigeneity_share_A": lambda c: share(c, "N1_A", "N1_B"),
                    "N6_violence_share_A": lambda c: share(c, "N6_A", "N6_B")}


def boot(vals, n=2000, seed=3):
    v = np.array([x for x in vals if x is not None], float)
    if len(v) < 5:
        return None
    rng = np.random.default_rng(seed)
    b = rng.choice(v, (n, len(v))).mean(1)
    return {"mean": float(v.mean()), "lo": float(np.percentile(b, 2.5)), "hi": float(np.percentile(b, 97.5)), "n": int(len(v))}


def main():
    manifest = json.load(open(os.path.join(A.DATA, "manifest.json")))
    dispute_of = {t: d for d, spec in NARRATIVE_DISPUTES.items() for t in spec["articles"]}
    per = {}; samples = defaultdict(list)
    for fn in sorted(glob.glob(os.path.join(A.ART, "*.json.gz"))):
        rec = json.load(gzip.open(fn, "rt", encoding="utf-8"))
        t = rec["title"]
        if t not in manifest:
            continue
        if manifest[t][0] == "treatment":
            kind, groups = "topic", TOPIC_GROUPS
        elif t in dispute_of:
            spec = NARRATIVE_DISPUTES[dispute_of[t]]
            kind, groups = dispute_of[t], {"A": R(spec["A"]), "B": R(spec["B"])}
        else:
            kind, groups = "other_control", {}          # baseline relevance features only (amendment C2b)
        rows, last = [], None
        for s in rec["snapshots"]:
            if s.get("text") is not None:
                if re.match(r"\s*#redirect", s["text"], re.I):
                    last = None; continue
                last = s["text"]
            if last is None:
                continue
            c, smp = snapshot_measures(last, groups, kind == "topic")
            rows.append({"date": s["date"][:7], "c": dict(c)})
            if s is rec["snapshots"][-1] or s["date"].startswith("2026-10"):
                for k, v in smp.items():
                    samples[(kind, k)].extend([(t, g, x) for g, x in v])
        if rows:
            per[t] = {"kind": kind, "subgroup": manifest[t][1], "rows": rows, "shared_site": t in SHARED_SITES}
    dates = sorted({r["date"] for v in per.values() for r in v["rows"]})
    first, last = dates[0], dates[-1]
    at = lambda rows, d: next((r for r in reversed(rows) if r["date"] <= d), None)

    out = {"dates": dates, "first": first, "last": last, "measures": {}, "disputes": {}, "pooled": {}, "shared_sites": {}}
    topic = [v for v in per.values() if v["kind"] == "topic"]
    # pooled shares per date (sum of counts across articles), the main trend lines
    def pooled(arts, a, b, d):
        ca = cb = 0
        for v in arts:
            r = at(v["rows"], d)
            if r:
                ca += r["c"].get(a, 0); cb += r["c"].get(b, 0)
        return (ca / (ca + cb) if ca + cb else None), ca + cb
    pairs = {"N1_indigeneity_share_J": ("N1_J", "N1_P"), "N2_ancient_naming_share_P": ("N2_P", "N2_J"),
             "N4_displacement_share_P": ("N4_P", "N4_J"), "N5_forced_share": ("N5_forced", "N5_flight"),
             "N6_violence_share_israeli": ("N6_I", "N6_P"), "N7_occupied_share": ("N7_occ", "N7_disp"),
             "N7_sop_country_share": ("N7_sop_country", "N7_sop_claim"), "N3_temple_mount_first": ("N3_tm_first", None)}
    for m, (a, b) in pairs.items():
        if b is None:
            series = []
            for d in dates:
                rr = [at(v["rows"], d) for v in topic]; rr = [r for r in rr if r and r["c"].get("N3_both")]
                series.append({"date": d, "value": float(np.mean([r["c"]["N3_tm_first"] for r in rr])) if rr else None, "n": len(rr)})
        else:
            series = [{"date": d, "value": pooled(topic, a, b, d)[0], "n": pooled(topic, a, b, d)[1]} for d in dates]
        # article-level change first -> last (articles with the measure defined at both ends)
        ch = []
        for v in topic:
            r0, r1 = at(v["rows"], first), at(v["rows"], last)
            if r0 and r1:
                x0, x1 = MEASURES[m](r0["c"]), MEASURES[m](r1["c"])
                if x0 is not None and x1 is not None:
                    ch.append(x1 - x0)
        out["pooled"][m] = series
        out["measures"][m] = {"article_change": boot(ch), "pooled_first": series[0]["value"], "pooled_last": series[-1]["value"],
                              "mentions_first": series[0]["n"], "mentions_last": series[-1]["n"]}
    for m in ("N4_rate_P", "N4_rate_J"):
        ch = []
        for v in topic:
            r0, r1 = at(v["rows"], first), at(v["rows"], last)
            if r0 and r1:
                ch.append(MEASURES[m](r1["c"]) - MEASURES[m](r0["c"]))
        out["measures"][m] = {"article_change": boot(ch)}
    # N8 shared sites: share of site articles whose lead mentions Jewish history, per date
    sites = [v for t, v in per.items() if v["shared_site"]]
    out["shared_sites"] = {"articles": [t for t, v in per.items() if v["shared_site"]],
                           "series": [{"date": d, "share": (lambda rr: float(np.mean(rr)) if rr else None)(
                               [at(v["rows"], d)["c"].get("N8_jewish_in_lead", 0) for v in sites if at(v["rows"], d)])} for d in dates]}
    # comparison disputes: analogous indigeneity and violence shares, pooled first vs last
    for d_name in NARRATIVE_DISPUTES:
        arts = [v for v in per.values() if v["kind"] == d_name]
        res = {"articles": len(arts)}
        for m, (a, b) in (("N1_indigeneity_share_A", ("N1_A", "N1_B")), ("N6_violence_share_A", ("N6_A", "N6_B"))):
            f, nf = pooled(arts, a, b, first); l, nl = pooled(arts, a, b, last)
            res[m] = {"first": f, "last": l, "change": (l - f) if f is not None and l is not None else None, "mentions": [nf, nl]}
        res["labels"] = {"A": NARRATIVE_DISPUTES[d_name]["A_label"], "B": NARRATIVE_DISPUTES[d_name]["B_label"]}
        out["disputes"][d_name] = res
    # per-article first/last values + outcome-blind baseline relevance (amendment C1/C2b)
    arts_out = {}
    for t, v in per.items():
        r0, r1 = at(v["rows"], first), at(v["rows"], last)
        if not (r0 and r1):
            continue
        ms = MEASURES if v["kind"] == "topic" else CONTROL_MEASURES
        b = r0["c"]; gk = [k for k in b if k.startswith("G_")]
        arts_out[t] = {"kind": v["kind"], "subgroup": v["subgroup"],
                       "first": {m: f(r0["c"]) for m, f in ms.items()}, "last": {m: f(r1["c"]) for m, f in ms.items()},
                       "words_first": b["_words"], "baseline_both_groups": all(b.get(k, 0) > 0 for k in gk),
                       "baseline_landconf_per_1000": b.get("LANDCONF", 0) * 1000 / b["_words"]}
    out["articles"] = arts_out
    # samples for validation (KWIC precision + attribution check)
    rnd = random.Random(7)
    out["validation_samples"] = {f"{k[0]}:{k[1]}": rnd.sample(v, min(30, len(v))) for k, v in samples.items()}
    out["n_topic_articles"] = len(topic)
    json.dump(out, open(os.path.join(A.DATA, "narrative.json"), "w"))
    for m, r in out["measures"].items():
        print(m, r)
    for d, r in out["disputes"].items():
        print(d, r)


if __name__ == "__main__":
    main()
