"""Sampling audit, step 1: one row per mass2 article with outcomes, covariates and design fields.
python build_df.py OUT.pkl   (reuses analyze_mass2.build so outcomes match the cards exactly)"""
import os, sys, json
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
WT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, WT)
import analyze_mass2 as AM
import analyze as A

CRIT = list(A.CRITICAL)
M, EV, ED, LD, SU, TY = AM.load(A.DATA)
arts = AM.build(M, {}, LD, TY, workers=4)
DATES = AM.DATES
rows = []
for a in arts:
    r = a.r
    d = {"title": a.t, "grp": a.grp, "project": a.proj, "importance": r.get("importance"), "rel": bool(a.rel),
         "n_frame_titles": len(r.get("frame_titles") or []), "created_in_window": r.get("created_in_window"),
         "pageid": (r.get("now") or {}).get("pageid"), "v12": a.v12}
    for k, s in zip(DATES, ("21", "23", "nw")):
        L = a.L.get(k)
        d[f"lw_{s}"] = L["w"] if L else np.nan
        d[f"crit_{s}"] = L["crit"] if L else np.nan
        d[f"res_{s}"] = L["res"] if L and L.get("res") is not None else np.nan
        d[f"ev_{s}"] = L["ev"] if L and L.get("ev") is not None else np.nan
        d[f"src_{s}"] = L.get("src") if L else None
        art = a.snap[k]["article"]
        d[f"fw_{s}"] = art.get("full_words") if art else np.nan
        d[f"fcrit_{s}"] = sum((art.get("lex_full") or {}).get(t, 0) for t in CRIT) if art else np.nan
        d[f"bytes_{s}"] = art.get("bytes") if art else np.nan
        d[f"exists_{s}"] = bool((a.snap[k].get("rev") or {}).get("revid"))
    for w in ("w1", "w2"):
        ww = a.win.get(w) or {}
        d[f"edits_{w}"] = ww.get("edits", 0) or 0
        d[f"vpm_{w}"] = ((ww.get("views") or {}).get("per_month"))
    tn = r.get("talk_now") or {}
    d["ct_notice"] = bool(tn.get("ct_notice"))
    d["qclass"] = (tn.get("class") or "").lower()
    ass = ((r.get("now") or {}).get("assessments") or {})
    d["assess_projects"] = "|".join(sorted(ass))
    d["n_projects"] = len([p for p in ass if p != "Project-independent assessment"])
    rows.append(d)
df = pd.DataFrame(rows)
df.to_pickle(sys.argv[1])
print(df.shape, df.grp.value_counts().to_dict())
