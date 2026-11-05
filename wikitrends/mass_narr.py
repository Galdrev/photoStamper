"""Mass-tier narrative (SPEC_NARRATIVE amendment C4): opening paragraph of every mass-frame article at 2021-01 and now.

  python mass_narr.py shard --shard I --of N  -> data/mass/narr_I.json.gz   (checkpointed)
  python mass_narr.py merge                    -> data/mass_narr.json
"""
import argparse, glob, gzip, json, os, re, sys, time

import analyze as A
import narrative as N
import wt_net
from mass import OUT, DATES, _run, shard

PROJECT_GROUPS = {"Armenia": "Karabakh", "Azerbaijan": "Karabakh", "Serbia": "Kosovo", "Ireland": "Northern Ireland",
                  "India": "Kashmir", "Pakistan": "Kashmir"}


def lead_at(title, date):
    j = wt_net.get_json("https://en.wikipedia.org/w/api.php", {"action": "query", "prop": "revisions", "titles": title, "rvlimit": 1,
                        "rvdir": "older", "rvstart": date, "rvprop": "ids|content", "rvslots": "main", "rvsection": 0,
                        "redirects": 1, "format": "json", "formatversion": 2})
    p = (j or {}).get("query", {}).get("pages", [{}])[0]
    if not p.get("revisions"):
        return None
    wt = p["revisions"][0].get("slots", {}).get("main", {}).get("content", "")
    return None if re.match(r"\s*#\w+\s*\[\[", wt) else wt


def features(row):
    from corpus import NARRATIVE_DISPUTES
    if row["group"] == "topic":
        groups, ms = N.TOPIC_GROUPS, N.MEASURES
    elif row["project"] in PROJECT_GROUPS:
        sp = NARRATIVE_DISPUTES[PROJECT_GROUPS[row["project"]]]
        groups, ms = {"A": N.R(sp["A"]), "B": N.R(sp["B"])}, N.CONTROL_MEASURES
    else:
        groups, ms = N.TOPIC_GROUPS, {}
    out = {**row, "snaps": []}
    for d in (DATES[0], DATES[-1]):
        wt = lead_at(row["title"], d)
        if not wt:
            out["snaps"].append(None); continue
        c, _ = N.snapshot_measures(wt, groups, row["group"] == "topic")
        lp = A.prose(wt); m = A.measure(lp, 20)
        out["snaps"].append({"c": dict(c), "vals": {k: f(c) for k, f in ms.items()},
                             "crit": None if m is None else m["rate"]["critical_rate"], "words": c["_words"]})
    return out


def merge():
    rows = [r for f in sorted(glob.glob(os.path.join(OUT, "narr_*.json.gz"))) for r in json.load(gzip.open(f, "rt"))]
    mp = os.path.join(A.DATA, "mass_results.json")
    edits = {a["t"]: a.get("e") for a in (json.load(open(mp))["mass"].get("lab_articles") or [])} if os.path.exists(mp) else {}
    arts = {}
    for r in rows:
        s0, s1 = (r["snaps"] + [None, None])[:2]
        if not s0 or not s1:
            continue
        b = s0["c"]; gk = [k for k in b if k.startswith("G_")]
        arts[r["title"]] = {"group": r["group"], "project": r["project"], "importance": r["importance"],
                            "first": s0["vals"], "last": s1["vals"], "lead_words_first": s0["words"], "edits": edits.get(r["title"]),
                            "crit_lead_change": (s1["crit"] - s0["crit"]) if s0["crit"] is not None and s1["crit"] is not None else None,
                            "baseline_both_groups": all(b.get(k, 0) > 0 for k in gk) if gk else False,
                            "baseline_landconf_per_1000": b.get("LANDCONF", 0) * 1000 / max(1, b["_words"])}
    json.dump({"articles": arts, "n": len(arts), "dates": [d[:10] for d in (DATES[0], DATES[-1])]},
              open(os.path.join(A.DATA, "mass_narr.json"), "w"))
    print("mass_narr merged:", len(arts), "articles with both leads")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cmd"); ap.add_argument("--shard", type=int, default=0); ap.add_argument("--of", type=int, default=1)
    a = ap.parse_args()
    if a.cmd == "merge":
        merge()
    else:
        rows = shard(json.load(open(os.path.join(OUT, "frame.json")))["rows"], a.shard, a.of)
        lim = int(os.environ.get("MASS_LIMIT", "0"))
        _run("narr", features, rows[:lim] if lim else rows, a.shard)
