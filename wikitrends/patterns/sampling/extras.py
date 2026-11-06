"""Sampling audit, extra checks (see AUDIT.md section 4 and 3):
  * CEM with the topic side at its design weights (population ATT instead of sample ATT);
  * weighted (a) without the single comparison Mid article that dominates it;
  * comparison Mid imputed from comparison High (model-based bound).
python extras.py DF.pkl  -> chart_data/06_extras.json
"""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "audit.py")).read().split("# ---------- reproduce the cards")[0]
exec(compile(src, "audit_prep", "exec"))          # data prep, weights, stats(), bootstrap()

df["log_lw21"] = np.log1p(df.lw_21.fillna(0)); df["miss21"] = df.lw_21.isna().astype(float)
df["log_pageid"] = np.log(df.pageid.astype(float)); df["created_post2021"] = df.created_in_window.notna().astype(float)
df["log_ed1"] = np.log1p(df.edits_w1.astype(float)); df["log_vpm1"] = np.log1p(df.vpm_w1.astype(float).fillna(0))


def cem_w(d, tw, ncut=4):
    key = d.importance.astype(str)
    for c in ("log_lw21", "log_pageid", "log_ed1", "log_vpm1"):
        key = key + "|" + pd.qcut(d[c].rank(method="first"), ncut, labels=False).astype(str)
    key = (key + "|" + d.miss21.astype(int).astype(str) + "|" + d.created_post2021.astype(int).astype(str)).values
    t = d.is_t.values
    T = pd.Series(tw[t]).groupby(key[t]).sum(); Cn = pd.Series(1.0, index=range((~t).sum())).groupby(key[~t]).sum()
    good = T.index.intersection(Cn.index)
    w = np.zeros(len(d))
    for i in range(len(d)):
        if key[i] in good:
            w[i] = tw[i] if t[i] else T[key[i]] / Cn[key[i]]
    return w


out = {}
for sub in ("all", "relevant"):
    d = (df if sub == "all" else df[df.rel]).reset_index(drop=True)
    tw = np.where(d.is_t, d.w, 0.0)
    w = cem_w(d, tw)
    D = arrays(d)
    est = stats(D, w)
    sims = {k: [] for k in ("a_unf", "a_res", "b", "b_t", "b_c")}
    gi = {g: np.where(d.grp.values == g)[0] for g in ("topic", "comparison")}
    for _ in range(200):
        idx = np.concatenate([gi[g][RNG.integers(0, len(gi[g]), len(gi[g]))] for g in gi])
        dd = d.iloc[idx].reset_index(drop=True)
        ww = cem_w(dd, np.where(dd.is_t, dd.w, 0.0))
        s = stats(arrays(dd), ww)
        for k in sims:
            if np.isfinite(s[k]):
                sims[k].append(s[k])
    out[f"cem_topic_design_weighted|{sub}"] = {k: {"est": r(est[k]), "lo": r(np.percentile(v, 2.5)), "hi": r(np.percentile(v, 97.5))} for k, v in sims.items()}
    print(sub, "CEM, topic at design weights:", {k: (round(est[k], 4), round(np.percentile(v, 2.5), 4), round(np.percentile(v, 97.5), 4)) for k, v in sims.items()})

# weighted (a) without the one comparison Mid outlier
drop = df.title != "Martuni, Nagorno-Karabakh"
res = bootstrap(df[drop].reset_index(drop=True), "w", Bn=500)
out["design_weighted_without_Martuni"] = {k: res[k] for k in ("a_unf", "a_res", "b", "c_share")}
print("weighted without Martuni:", out["design_weighted_without_Martuni"])

# comparison Mid imputed by comparison High (comparison High articles carry the comparison Mid population weight)
cH = (~df.is_t) & (df.importance == "High"); cM = (~df.is_t) & (df.importance == "Mid")
WH = df.loc[cH, "w"].sum(); WM_pop = grp_tab["comparison"]["levels"]["Mid"]["N_pool_est"]
WT_pop = grp_tab["comparison"]["levels"]["Top"]["N_pool_est"]; WH_pop = grp_tab["comparison"]["levels"]["High"]["N_pool_est"]
d2 = df[~cM].copy()
m = (~d2.is_t) & (d2.importance == "High")
d2.loc[m, "w_imp"] = d2.loc[m, "w"] * (WH_pop + WM_pop) / WH
m = (~d2.is_t) & (d2.importance == "Top")
d2.loc[m, "w_imp"] = d2.loc[m, "w"] * WT_pop / d2.loc[m, "w"].sum()
d2.loc[d2.is_t, "w_imp"] = d2.loc[d2.is_t, "w"]
res2 = bootstrap(d2.reset_index(drop=True), "w_imp", Bn=500)
out["comparison_mid_imputed_by_high"] = {k: res2[k] for k in ("a_unf", "a_res", "c_share", "b_t", "b_c", "b", "b_full_did", "d_t", "d_c", "d", "e")}
print("comparison Mid imputed from comparison High:", {k: v for k, v in out["comparison_mid_imputed_by_high"].items()})
dump("06_extras.json", out)
