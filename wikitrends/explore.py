"""Exploratory analyses (NOT pre-registered; labelled as such in the report).

  E1 hedging      share of loaded-term mentions that carry attribution ("accused of", "critics describe")
  E2 citations    which source domains articles cite, over time; ADL natural experiment (June 2024)
  E3 terror       "terrorist" vs "militant" labelling of armed groups, topic vs comparison groups
  E4 definitions  how often the first sentence changes; first-sentence frame terms

  python explore.py  -> merges `explore` into data/results.json
"""
import glob, gzip, json, os, re
from collections import Counter, defaultdict

import numpy as np

import analyze as A
from corpus import ARMED_GROUPS_TOPIC, ARMED_GROUPS_CONTROL

LOADED = ["genocide", "apartheid", "ethnic_cleansing", "war_crimes", "settler_colonial"]
HEDGE = re.compile(r"\b(?:alleg\w*|accus\w*|critics?|described as|characteri[sz]\w*|according to|claim\w*|argu\w*|"
                   r"considered by|some (?:scholars|historians|experts|observers)|have called|has been called|label\w*|"
                   r"denounc\w*|condemn\w*|disput\w*|controvers\w*|so-called|charges? of)\b", re.I)
URL = re.compile(r"https?://(?:www\d?\.|m\.|amp\.)?([a-z0-9\-\.]+\.[a-z]{2,})", re.I)
SOURCE_CLASSES = {
    "Israeli press": ["timesofisrael.com", "haaretz.com", "haaretz.co.il", "jpost.com", "ynetnews.com", "israelhayom.com",
                      "i24news.tv", "jns.org", "israelnationalnews.com", "maariv.co.il", "calcalistech.com"],
    "Arab & Palestinian press, pro-Palestinian outlets": ["aljazeera.com", "aljazeera.net", "middleeasteye.net", "electronicintifada.net",
                                          "mondoweiss.net", "wafa.ps", "palestinechronicle.com", "972mag.com", "aa.com.tr",
                                          "english.wafa.ps", "newarab.com", "alaraby.co.uk", "alarabiya.net", "dropsitenews.com"],
    "Rights orgs & UN": ["amnesty.org", "hrw.org", "btselem.org", "un.org", "ohchr.org", "unrwa.org", "icj-cij.org", "icc-cpi.int",
                         "ochaopt.org", "reliefweb.int", "who.int", "unicef.org", "msf.org", "savethechildren.org"],
    "Pro-Israel advocacy": ["adl.org", "ngo-monitor.org", "camera.org", "memri.org", "jcpa.org", "honestreporting.com",
                            "stopantisemitism.org", "simonwiesenthal.org", "ajc.org", "jewishvirtuallibrary.org"],
    "Western wire & papers": ["nytimes.com", "bbc.co.uk", "bbc.com", "theguardian.com", "washingtonpost.com", "reuters.com",
                              "apnews.com", "cnn.com", "nbcnews.com", "economist.com", "ft.com", "wsj.com", "npr.org",
                              "lemonde.fr", "dw.com", "france24.com", "independent.co.uk", "telegraph.co.uk", "theatlantic.com"],
    "Scholarly (books, journals)": ["books.google", "doi.org", "jstor.org", "cambridge.org", "oup.com", "tandfonline.com",
                                    "springer.com", "wiley.com", "academic.oup.com", "muse.jhu.edu", "brill.com",
                                    "sagepub.com", "routledge.com", "archive.org"],
}
DOM2CLASS = {d: c for c, ds in SOURCE_CLASSES.items() for d in ds}


def classify(dom):
    dom = dom.lower()
    for d, c in DOM2CLASS.items():
        if dom == d or dom.endswith("." + d) or dom.startswith(d):
            return c
    return None


def refs_of(wt):
    """Count citations: cite templates and <ref> bodies; classify by URL domain or doi/isbn."""
    out = Counter()
    bodies = re.findall(r"<ref[^>/]*>(.*?)</ref\s*>", wt, flags=re.S | re.I)
    for b in bodies:
        doms = URL.findall(b)
        cls = None
        for d in doms:
            cls = classify(d)
            if cls:
                break
        if not cls and re.search(r"\{\{\s*cite (?:book|journal|thesis)|\bdoi\s*=|\bisbn\s*=|\{\{\s*(?:sfn|harvnb)", b, re.I):
            cls = "Scholarly (books, journals)"
        out[cls or "Other"] += 1
        for d in doms:
            if d.lower().endswith("adl.org"):
                out["_adl"] += 1; break
    # short-footnote styles cite books via {{sfn}} outside <ref>
    out["Scholarly (books, journals)"] += len(re.findall(r"\{\{\s*(?:sfn|sfnp|harvnb)\s*\|", wt, re.I))
    out["_total"] = sum(v for k, v in out.items() if not k.startswith("_"))
    return out


def hedged_share(p):
    hits = hedged = 0
    for k in LOADED:
        for r in A.RXI[k]:
            for m in r.finditer(p):
                hits += 1
                win = p[max(0, m.start() - 120):m.end() + 60]
                hedged += bool(HEDGE.search(win))
    return hits, hedged


def mean(xs):
    xs = [x for x in xs if x is not None]
    return float(np.mean(xs)) if xs else None


def main():
    manifest_p = os.path.join(A.DATA, "manifest.json")
    manifest = json.load(open(manifest_p)) if os.path.exists(manifest_p) else {}
    from corpus import CONTROL_CONTAMINATED
    per = {}
    for fn in sorted(glob.glob(os.path.join(A.ART, "*.json.gz"))):
        rec = json.load(gzip.open(fn, "rt", encoding="utf-8"))
        if rec["title"] in manifest:
            rec["group"], rec["subgroup"] = manifest[rec["title"]]
        grp = "control_contaminated" if rec["group"] == "control" and rec["title"] in CONTROL_CONTAMINATED else rec["group"]
        rows, last = [], None
        for s in rec["snapshots"]:
            if s.get("text") is not None:
                if re.match(r"\s*#redirect", s["text"], re.I):
                    last = None; continue
                last = s["text"]
            if last is None:
                continue
            fp = A.prose(last); lp = A.prose(A.split_lead(last))
            w = len(re.findall(r"\w+", fp))
            if w < A.MIN_WORDS_FULL:
                continue
            h, hd = hedged_share(fp); lh, lhd = hedged_share(lp)
            sents = A.sentences(lp); fs = sents[0] if sents else ""
            rows.append({"date": s["date"][:7], "words": w, "hits": h, "hedged": hd, "lead_hits": lh, "lead_hedged": lhd,
                         "refs": refs_of(last), "terror": A.count("terrorism", fp), "militant": A.count("militant", fp),
                         "lead_terror": A.count("terrorism", lp), "lead_militant": A.count("militant", lp),
                         "fs": fs, "fs_crit": sum(A.count(k, fs) for k in A.CRITICAL)})
        if rows:
            per[rec["title"]] = {"group": grp, "subgroup": rec["subgroup"], "rows": rows,
                                 "balanced": rows[0]["date"] == "2021-01"}
    dates = sorted({r["date"] for v in per.values() for r in v["rows"]})
    at = lambda rows, d: next((r for r in reversed(rows) if r["date"] <= d), None)
    groups = {"topic": [v for v in per.values() if v["group"] == "treatment" and v["balanced"]],
              "comparison": [v for v in per.values() if v["group"] == "control" and v["balanced"]]}

    # E1 hedging: pooled share of loaded-term mentions with attribution nearby, per date
    e1 = {}
    for g, V in groups.items():
        for part, hk, dk in (("full", "hits", "hedged"), ("lead", "lead_hits", "lead_hedged")):
            series = []
            for d in dates:
                rr = [at(v["rows"], d) for v in V]; rr = [r for r in rr if r]
                hits = sum(r[hk] for r in rr); hed = sum(r[dk] for r in rr)
                series.append({"date": d, "mentions": hits, "hedged_share": hed / hits if hits else None,
                               "unhedged_per_article": (hits - hed) / len(rr) if rr else None})
            e1[f"{g}:{part}"] = series
    key_titles = ["Zionism", "Israel", "Gaza war", "Israeli apartheid", "Israeli–Palestinian conflict", "Nakba",
                  "History of Israel", "Israeli settlement", "Gaza genocide", "October 7 attacks"]
    e1_articles = {t: [{"date": r["date"], "mentions": r["hits"], "hedged": r["hedged"]} for r in per[t]["rows"]]
                   for t in key_titles if t in per}

    # E2 citations: class shares per date (pooled), topic subgroups for the ADL natural experiment
    def cite_series(V):
        out = []
        for d in dates:
            rr = [at(v["rows"], d) for v in V]; rr = [r for r in rr if r]
            tot = sum(r["refs"]["_total"] for r in rr) or 1
            row = {"date": d, "refs": tot, "adl_per_article": sum(r["refs"].get("_adl", 0) for r in rr) / max(1, len(rr))}
            for c in list(SOURCE_CLASSES) + ["Other"]:
                row[c] = sum(r["refs"].get(c, 0) for r in rr) / tot
            out.append(row)
        return out
    e2 = {g: cite_series(V) for g, V in groups.items()}
    conflict = [v for v in groups["topic"] if v["subgroup"] in ("conflict", "israel", "zionism")]
    antisem = [v for v in groups["topic"] if v["subgroup"] in ("antisemitism", "judaism")]
    e2["topic_conflict"] = cite_series(conflict); e2["topic_antisemitism_judaism"] = cite_series(antisem)

    # E3 terror vs militant for armed groups
    def terr(titles, part):
        out = []
        for t in titles:
            if t not in per:
                continue
            rows = per[t]["rows"]
            tk, mk = ("terror", "militant") if part == "full" else ("lead_terror", "lead_militant")
            out.append({"title": t, "series": [{"date": r["date"], "terror": r[tk], "militant": r[mk],
                                                "terror_share": r[tk] / (r[tk] + r[mk]) if r[tk] + r[mk] else None}
                                               for r in rows]})
        return out
    e3 = {"topic": {p: terr(ARMED_GROUPS_TOPIC, p) for p in ("full", "lead")},
          "comparison": {p: terr(ARMED_GROUPS_CONTROL, p) for p in ("full", "lead")}}
    for g in ("topic", "comparison"):
        for p in ("full", "lead"):
            e3[f"{g}:{p}:mean"] = [{"date": d, "terror_share": mean([next((x["terror_share"] for x in reversed(a["series"]) if x["date"] <= d), None)
                                                                     for a in e3[g][p]])} for d in dates]

    # E4 first-sentence churn: share of articles whose first sentence changed each quarter; critical terms in it
    e4 = {}
    for g, V in groups.items():
        rows = []
        for i, d in enumerate(dates[1:], 1):
            ch, crit, n = 0, 0, 0
            for v in V:
                a, b = at(v["rows"], dates[i - 1]), at(v["rows"], d)
                if a and b:
                    n += 1; ch += a["fs"] != b["fs"]; crit += b["fs_crit"] > 0
            rows.append({"date": d, "changed_share": ch / n if n else None, "fs_with_critical_term": crit / n if n else None})
        e4[g] = rows

    explore = {"note": "Exploratory, not pre-registered.", "dates": dates, "source_classes": list(SOURCE_CLASSES),
               "hedging": e1, "hedging_articles": e1_articles, "citations": e2, "terror": e3, "first_sentence": e4,
               "n": {g: len(V) for g, V in groups.items()}, "hedge_regex": HEDGE.pattern}
    rp = os.path.join(A.OUTDIR, "results.json")
    res = json.load(open(rp)) if os.path.exists(rp) else {}
    res["explore"] = explore
    json.dump(res, open(rp, "w"))
    for g in groups:
        s = e1[f"{g}:full"]; print(f"E1 {g}: hedged share {s[0]['hedged_share']} -> {s[-1]['hedged_share']}")
        c = e2[g]; print(f"E2 {g}: " + ", ".join(f"{k[:14]} {c[0][k]:.2f}->{c[-1][k]:.2f}" for k in SOURCE_CLASSES))
        print(f"E4 {g}: first-sentence-with-critical-term {e4[g][0]['fs_with_critical_term']} -> {e4[g][-1]['fs_with_critical_term']}")


if __name__ == "__main__":
    main()
