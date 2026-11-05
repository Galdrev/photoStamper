"""Coherence, outcome-blind cleaning, and standard models (SPEC_NARRATIVE amendment C1-C3).

  python cohere.py [deep|mass]  -> data/cohere_<tier>.json
Standard tools only: pandas, numpy, statsmodels (OLS, cluster-robust SEs), Spearman correlations, PCA.
"""
import json, os, sys

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

import analyze as A

D = A.DATA
NARR = ["N1_indigeneity_share_J", "N2_ancient_naming_share_P", "N4_displacement_share_P", "N5_forced_share",
        "N6_violence_share_israeli", "N7_occupied_share"]


def load_types():
    p = os.path.join(D, "wikidata_types.json")
    return json.load(open(p)) if os.path.exists(p) else {}


def coherence(df, cols):
    """Pairwise Spearman correlations + PCA on the (pairwise) correlation matrix."""
    cols = [c for c in cols if c in df and df[c].notna().sum() >= 10]
    if len(cols) < 3:
        return None
    corr = df[cols].corr(method="spearman", min_periods=10)
    nobs = {f"{a}|{b}": int(df[[a, b]].dropna().shape[0]) for i, a in enumerate(cols) for b in cols[i + 1:]}
    m = corr.fillna(0).values
    w, v = np.linalg.eigh(m)
    order = np.argsort(w)[::-1]
    w, v = w[order], v[:, order]
    load = v[:, 0] * (1 if v[:, 0].sum() >= 0 else -1)
    return {"columns": cols, "spearman": corr.round(3).where(corr.notna(), None).values.tolist(), "pairs_n": nobs,
            "pc1_share": float(w[0] / w.sum()), "pc1_loadings": dict(zip(cols, map(float, load))),
            "eigenvalues": list(map(float, w))}


def ols(df, y, cluster):
    d = df.dropna(subset=[y, "group_topic"]).copy()
    if d["group_topic"].nunique() < 2 or len(d) < 30:
        return None
    covs = [c for c in ("log_words", "log_edits", "log_views", "created") if c in d and d[c].nunique() > 1]
    f = f"{y} ~ group_topic" + "".join(f" + {c}" for c in covs)
    try:
        m = smf.ols(f, data=d).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d[cluster])[0]})
    except Exception as e:
        return {"error": str(e)}
    ci = m.conf_int().loc["group_topic"]
    return {"coef": float(m.params["group_topic"]), "lo": float(ci[0]), "hi": float(ci[1]), "p": float(m.pvalues["group_topic"]),
            "n": int(m.nobs), "clusters": int(d[cluster].nunique()), "formula": f}


def boot(x, n=2000, seed=4):
    x = np.asarray([v for v in x if v is not None and not np.isnan(v)], float)
    if len(x) < 5:
        return None
    b = np.random.default_rng(seed).choice(x, (n, len(x))).mean(1)
    return {"mean": float(x.mean()), "lo": float(np.percentile(b, 2.5)), "hi": float(np.percentile(b, 97.5)), "n": int(len(x))}


def deep():
    res = json.load(open(os.path.join(D, "results.json"))); nar = json.load(open(os.path.join(D, "narrative.json")))
    types = load_types()
    rows = []
    for a in res["articles"]:
        t = a["title"]; n = nar["articles"].get(t, {})
        r = {"title": t, "group": a["group"], "subgroup": a["subgroup"],
             "log_words": np.log(max(1, a["words0"])), "log_edits": np.log1p(a["edits"]), "log_views": np.log1p(a["views"]),
             "created": int(bool(a["created_in_window"])),
             "crit_full": (a["crit1"] - a["crit0"]) if a["crit0"] is not None and a["crit1"] is not None else None,
             "crit_lead": (a["lcrit1"] - a["lcrit0"]) if a.get("lcrit0") is not None and a.get("lcrit1") is not None else None,
             "wd_keep": types.get(t, {}).get("keep", True), "wd_types": types.get(t, {}).get("drop_types", []),
             "base_both": n.get("baseline_both_groups"), "base_landconf": n.get("baseline_landconf_per_1000")}
        for m in NARR:
            f0, f1 = n.get("first", {}).get(m), n.get("last", {}).get(m)
            r[m] = (f1 - f0) if f0 is not None and f1 is not None else None
        rows.append(r)
    df = pd.DataFrame(rows)
    df["group_topic"] = (df["group"] == "treatment").astype(int)
    df["relevant"] = df["wd_keep"] & (df["base_both"].fillna(False) | (df["base_landconf"].fillna(0) >= 2))
    df = df[df["group"].isin(["treatment", "control"])]
    out = {"tier": "deep", "n": int(len(df)),
           "filter_counts": {"all": int(len(df)), "wikidata_keep": int(df["wd_keep"].sum()), "relevant": int(df["relevant"].sum()),
                             "dropped_types": pd.Series([x for l in df["wd_types"] for x in l]).value_counts().head(15).to_dict()}}
    for label, sub in (("unfiltered", df), ("filtered", df[df["relevant"]])):
        topic = sub[sub["group_topic"] == 1]
        out[label] = {
            "coherence_topic": coherence(topic, NARR + ["crit_full", "crit_lead"]),
            "narrative_change_topic": {m: boot(topic[m]) for m in NARR},
            "ols": {y: ols(sub, y, "subgroup") for y in ("crit_full", "crit_lead")},
            "n_topic": int(len(topic)), "n_comparison": int((sub["group_topic"] == 0).sum())}
    json.dump(out, open(os.path.join(D, "cohere_deep.json"), "w"), default=str)
    print(json.dumps({k: out[k] for k in ("n", "filter_counts")}, default=str))
    for lab in ("unfiltered", "filtered"):
        o = out[lab]; c = o["coherence_topic"]
        print(lab, "n", o["n_topic"], o["n_comparison"], "| PC1 share", c and round(c["pc1_share"], 2), "| OLS", {k: v and {kk: round(vv, 3) for kk, vv in v.items() if isinstance(vv, float)} for k, v in o["ols"].items()})


def mass():
    mn = json.load(open(os.path.join(D, "mass_narr.json"))); types = load_types()
    rows = []
    for t, a in mn["articles"].items():
        r = {"title": t, "group": a["group"], "project": a["project"], "importance": a["importance"],
             "log_words": np.log(max(1, a.get("lead_words_first") or 1)), "log_edits": np.log1p(a.get("edits") or 0),
             "log_views": 0.0, "wd_keep": types.get(t, {}).get("keep", True),
             "base_both": a.get("baseline_both_groups"), "base_landconf": a.get("baseline_landconf_per_1000")}
        for m in NARR:
            f0, f1 = a.get("first", {}).get(m), a.get("last", {}).get(m)
            r[m] = (f1 - f0) if f0 is not None and f1 is not None else None
        r["crit_lead"] = a.get("crit_lead_change")
        rows.append(r)
    df = pd.DataFrame(rows)
    df["group_topic"] = (df["group"] == "topic").astype(int)
    df["relevant"] = df["wd_keep"] & (df["base_both"].fillna(False) | (df["base_landconf"].fillna(0) >= 2))
    out = {"tier": "mass", "n": int(len(df)), "filter_counts": {"all": int(len(df)), "wikidata_keep": int(df["wd_keep"].sum()), "relevant": int(df["relevant"].sum())}}
    for label, sub in (("unfiltered", df), ("filtered", df[df["relevant"]])):
        topic = sub[sub["group_topic"] == 1]
        out[label] = {"coherence_topic": coherence(topic, NARR + ["crit_lead"]),
                      "coherence_by_project": {p: coherence(g, NARR + ["crit_lead"]) for p, g in topic.groupby("project")},
                      "narrative_change_topic": {m: boot(topic[m]) for m in NARR},
                      "narrative_change_by_project": {p: {m: boot(g[m]) for m in NARR} for p, g in topic.groupby("project")},
                      "ols_crit_lead": ols(sub.assign(log_views=0.0), "crit_lead", "project"),
                      "n_topic": int(len(topic)), "n_comparison": int((sub["group_topic"] == 0).sum())}
    json.dump(out, open(os.path.join(D, "cohere_mass.json"), "w"), default=str)
    for lab in ("unfiltered", "filtered"):
        o = out[lab]; c = o["coherence_topic"]
        print("mass", lab, o["n_topic"], o["n_comparison"], "PC1", c and round(c["pc1_share"], 2), "OLS", o["ols_crit_lead"])


if __name__ == "__main__":
    (mass if (len(sys.argv) > 1 and sys.argv[1] == "mass") else deep)()
