"""Sampling audit of the mass2 tier (see AUDIT.md).

  python audit.py DF.pkl          (DF.pkl from build_df.py)
writes chart_data/*.json and prints every number quoted in AUDIT.md.

Design reconstructed from mass.py frame():
  * frame = talk pages in Category:{Top,High,Mid}-importance <suffix>, suffix discovered by keyword prefix;
  * an article belongs to the FIRST project (in list order) that lists it; importance = highest level across the
    group's projects; articles listed by both a topic and a comparison project are dropped ("both");
  * per project: shuffle, sort Top > High > Mid, keep the first cap (topic 1,400, comparison 260).
So within project x importance the draw is a simple random sample of size n from a pool of N; pi = n / N.
Pools are exact for levels that were taken whole (n_frame = N); for the level where the cap bites N is estimated from
category_counts scaled by the project's own pool/category ratio on its whole levels; later levels have pi = 0.
"""
import json, os, sys, math, hashlib
from collections import Counter, defaultdict
import numpy as np, pandas as pd
import statsmodels.api as sm

HERE = os.path.dirname(os.path.abspath(__file__))
WT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "chart_data")
os.makedirs(OUT, exist_ok=True)
B = int(os.environ.get("AUDIT_B", "1000"))
RNG = np.random.default_rng(20261106)
LEVELS = ["Top", "High", "Mid"]
TOPIC = ["Israel", "Judaism", "Jewish history", "Palestine", "Zionism", "Jewish culture", "Arab–Israeli conflict"]
CONTROL = ["India", "Pakistan", "Turkey", "Kurdistan", "Armenia", "Azerbaijan", "Ukraine", "Russia", "Ireland",
           "Taiwan", "Tibet", "Cyprus", "Greece", "Poland", "Iran", "Sri Lanka", "Bangladesh", "Serbia",
           "Bosnia and Herzegovina", "Hinduism", "Islam", "Catholicism", "Sikhism", "Buddhism", "Armenian history"]
CAP = {"topic": 1400, "comparison": 260}
CONFLICT = ["Kurdistan", "Armenia", "Azerbaijan", "Ukraine", "Russia", "Taiwan", "Tibet", "Sri Lanka",
            "Bosnia and Herzegovina", "Serbia"]
RELIGION = ["Hinduism", "Islam", "Catholicism", "Sikhism", "Buddhism"]
COUNTRY = ["India", "Pakistan", "Turkey", "Ireland", "Greece", "Poland", "Iran", "Bangladesh"]
OUT_OF_SCOPE_SUFFIX = ("Indiana articles", "Indianapolis articles")      # prefix 'India' matched the US state


def dump(name, obj):
    with open(os.path.join(OUT, name), "w") as f:
        json.dump(obj, f, indent=1, default=lambda x: None if (isinstance(x, float) and not math.isfinite(x)) else
                  (float(x) if isinstance(x, (np.floating,)) else int(x) if isinstance(x, np.integer) else str(x)))


def r(x, k=4):
    return None if x is None or (isinstance(x, float) and not math.isfinite(x)) else round(float(x), k)


# ============================================================ 1. population vs sample
fr = json.load(open(os.path.join(WT, "data", "mass", "frame.json")))
cc = fr["category_counts"]
proj_of_suffix = {}
for g, P in (("topic", TOPIC), ("comparison", CONTROL)):
    for p in P:
        for cat in cc:
            suf = cat.split("-importance ", 1)[1]
            if suf.startswith(p) and len(suf) <= len(p) + 20:
                if suf not in proj_of_suffix or len(p) > len(proj_of_suffix[suf][1]):
                    proj_of_suffix[suf] = (g, p)
Ncat = defaultdict(int); Ncat_oos = defaultdict(int); suffixes = defaultdict(set)
for cat, n in cc.items():
    lev, suf = cat[len("Category:"):].split("-importance ", 1)
    g, p = proj_of_suffix[suf]
    suffixes[p].add(suf)
    if suf in OUT_OF_SCOPE_SUFFIX:
        Ncat_oos[(g, p, lev)] += n
    else:
        Ncat[(g, p, lev)] += n
nfr = Counter((x["group"], x["project"], x["importance"]) for x in fr["rows"])
df = pd.read_pickle(sys.argv[1])
df = df[df.grp != "atrocity"].copy()
nm2 = Counter(zip(df.grp, df.project, df.importance))

strata = []
for g, P in (("topic", TOPIC), ("comparison", CONTROL)):
    for p in P:
        if not suffixes.get(p):
            strata.append({"group": g, "project": p, "importance": None, "note": "no importance categories found by discover(): project contributes nothing"})
            continue
        tot = sum(nfr[(g, p, l)] for l in LEVELS)
        capped = tot >= CAP[g]
        last = max((i for i, l in enumerate(LEVELS) if nfr[(g, p, l)] > 0), default=-1)
        full = [l for i, l in enumerate(LEVELS) if (not capped) or i < last]
        ratios = [nfr[(g, p, l)] / Ncat[(g, p, l)] for l in full if Ncat[(g, p, l)] > 0]
        rp = min(1.0, float(np.median(ratios))) if ratios else None
        for i, l in enumerate(LEVELS):
            nc = Ncat[(g, p, l)]
            if l in full:
                status, N = "whole level taken", nfr[(g, p, l)]
            elif i == last:
                status = "cap bites here"
                N = max(nfr[(g, p, l)], round((rp if rp is not None else 1.0) * nc))
            else:
                status, N = "not sampled (cap reached)", round((rp if rp is not None else 1.0) * nc)
            strata.append({"group": g, "project": p, "importance": l, "N_category": nc, "N_category_out_of_scope": Ncat_oos[(g, p, l)],
                           "pool_ratio_used": r(rp, 3), "N_pool_est": int(N), "n_frame": nfr[(g, p, l)], "n_mass2": nm2[(g, p, l)],
                           "status": status, "pi_frame": r(nfr[(g, p, l)] / N, 4) if N else None,
                           "pi_mass2": r(nm2[(g, p, l)] / N, 4) if N else None})
ST = pd.DataFrame(strata)
st_ok = ST.dropna(subset=["importance"])
print("== strata (group, project, importance): N_category, N_pool_est, n_frame, n_mass2, pi")
for _, x in st_ok.iterrows():
    print(f"  {x.group:10} {x.project:24} {x.importance:4} Ncat={x.N_category:6} Npool~{x.N_pool_est:6} nfr={x.n_frame:5} nm2={x.n_mass2:5} "
          f"pi={x.pi_mass2} [{x.status}]")
for _, x in ST[ST.importance.isna()].iterrows():
    print("  ", x.group, x.project, x.note)
grp_tab = {}
for g in ("topic", "comparison"):
    s = st_ok[st_ok.group == g]
    lev = {}
    for l in LEVELS:
        t = s[s.importance == l]
        lev[l] = {"N_category": int(t.N_category.sum()), "N_pool_est": int(t.N_pool_est.sum()), "n_mass2": int(t.n_mass2.sum()),
                  "pi": r(t.n_mass2.sum() / t.N_pool_est.sum()) if t.N_pool_est.sum() else None,
                  "pool_with_pi0": int(t[t.n_mass2 == 0].N_pool_est.sum())}
    grp_tab[g] = {"levels": lev, "N_category": int(s.N_category.sum()), "N_pool_est": int(s.N_pool_est.sum()),
                  "n_mass2": int(s.n_mass2.sum()), "pi": r(s.n_mass2.sum() / s.N_pool_est.sum()),
                  "share_of_pool_with_pi0": r(s[s.n_mass2 == 0].N_pool_est.sum() / s.N_pool_est.sum())}
print("== group totals", json.dumps(grp_tab, indent=1))

# design weights
wkey = {(x.group, x.project, x.importance): (x.N_pool_est / x.n_mass2 if x.n_mass2 else np.nan) for _, x in st_ok.iterrows()}
# strata with fewer than 30 sampled articles are collapsed into one cell per group x importance (pooled N / pooled n):
# otherwise one Bosnia-and-Herzegovina Mid article would stand for 514 pages (weight 514).
small = st_ok[(st_ok.n_mass2 > 0) & (st_ok.n_mass2 < 30)]
wcol = dict(wkey)
for (g, l), t in small.groupby(["group", "importance"]):
    for _, x in t.iterrows():
        wcol[(x.group, x.project, x.importance)] = t.N_pool_est.sum() / t.n_mass2.sum()
print("collapsed small strata:", [(x.group, x.project, x.importance, int(x.n_mass2)) for _, x in small.iterrows()],
      {k: round(v, 1) for k, v in wcol.items() if k in set(zip(small.group, small.project, small.importance))})
df["w_raw"] = [wkey.get((g, p, i), np.nan) for g, p, i in zip(df.grp, df.project, df.importance)]
df["w"] = [wcol.get((g, p, i), np.nan) for g, p, i in zip(df.grp, df.project, df.importance)]
assert df.w.notna().all(), df[df.w.isna()][["title", "grp", "project", "importance"]]
df["stratum"] = df.grp + "|" + df.project + "|" + df.importance
for g in ("topic", "comparison"):
    w = df[df.grp == g].w
    print(f"weights {g}: min {w.min():.2f} median {w.median():.2f} max {w.max():.2f}; Kish deff {len(w) * (w ** 2).sum() / w.sum() ** 2:.2f}; "
          f"n_eff {w.sum() ** 2 / (w ** 2).sum():.0f} of {len(w)}")

# ============================================================ outcome columns
rate = lambda c, w: c * 1e4 / w
okL = np.ones(len(df), bool)
for s in ("21", "23", "nw"):
    okL &= (df[f"lw_{s}"] >= 20).values & (df[f"src_{s}"] == "text").values & df[f"res_{s}"].notna().values
df["okL"] = okL
for lab, f in (("unf", "crit"), ("res", "res"), ("ev", "ev")):
    df[f"post_{lab}"] = rate(df[f"{f}_nw"], df.lw_nw) - rate(df[f"{f}_23"], df.lw_23)
    df[f"pre_{lab}"] = rate(df[f"{f}_23"], df.lw_23) - rate(df[f"{f}_21"], df.lw_21)
okG = df.crit_23.notna() & df.crit_nw.notna()
df["okG"] = okG & df.v12.notna()
df["gain"] = np.where(okG, (df.crit_nw > df.crit_23).astype(float), np.nan)
okF = (df.fw_21 > 0) & (df.fw_23 > 0) & (df.fw_nw > 0)
df["okF"] = okF
df["fup_post"] = np.where(okF, (df.fcrit_nw > df.fcrit_23).astype(float), np.nan)
df["fup_pre"] = np.where(okF, (df.fcrit_23 > df.fcrit_21).astype(float), np.nan)
df["v12"] = df.v12.astype(float)
df["is_t"] = (df.grp == "topic").values
df["ip"] = df.project.isin(["Israel", "Palestine"]).values
df["ju"] = (df.project == "Judaism").values
df = df.reset_index(drop=True)


# ============================================================ estimator
def wm(x, w, m):
    m = m & np.isfinite(x)
    sw = w[m].sum()
    return float((x[m] * w[m]).sum() / sw) if sw > 0 else np.nan


def stats(D, w, ctrl=None):
    """All headline statistics on frame D with weights w. ctrl: boolean mask restricting the comparison rows."""
    t = D["is_t"]; c = ~t if ctrl is None else (~t & ctrl)
    o = {}
    L = D["okL"]
    for lab in ("unf", "res", "ev"):
        o[f"a_{lab}_t"] = wm(D[f"post_{lab}"], w, t & L); o[f"a_{lab}_c"] = wm(D[f"post_{lab}"], w, c & L)
        o[f"a_{lab}"] = o[f"a_{lab}_t"] - o[f"a_{lab}_c"]
    o["a_pre_res"] = wm(D["pre_res"], w, t & L) - wm(D["pre_res"], w, c & L)
    o["c_share"] = o["a_res"] / o["a_unf"] if o["a_unf"] else np.nan
    G = D["okG"]
    o["b_t"] = wm(D["gain"], w, t & G); o["b_c"] = wm(D["gain"], w, c & G); o["b"] = o["b_t"] - o["b_c"]
    F = D["okF"]
    fd = D["fup_post"] - D["fup_pre"]
    o["b_full_did"] = wm(fd, w, t & F) - wm(fd, w, c & F)
    v = D["v12"]
    for nm, m in (("t", t), ("c", c)):
        mm = m & G & np.isfinite(v)
        o[f"d_{nm}"] = float((w[mm] * v[mm] * D["gain"][mm]).sum() / (w[mm] * v[mm]).sum()) if (w[mm] * v[mm]).sum() > 0 else np.nan
    o["d"] = o["d_t"] - o["d_c"]
    o["d_did"] = (o["d_t"] - o["b_t"]) - (o["d_c"] - o["b_c"])
    o["e_ip"] = wm(D["gain"], w, t & G & D["ip"]); o["e_ju"] = wm(D["gain"], w, t & G & D["ju"]); o["e"] = o["e_ip"] - o["e_ju"]
    o["e_full"] = wm(fd, w, t & F & D["ip"]) - wm(fd, w, t & F & D["ju"])
    o["e_ju_vs_c"] = o["e_ju"] - o["b_c"]
    return o


def arrays(d):
    return {k: d[k].values.astype(float) if d[k].dtype != bool else d[k].values for k in
            ["is_t", "okL", "okG", "okF", "post_unf", "post_res", "post_ev", "pre_res", "gain", "fup_post", "fup_pre", "v12", "ip", "ju"]}


def strat_idx(groups):
    return [np.array(ix) for ix in groups]


def bootstrap(d, wcol=None, mode="stratum", ctrl=None, Bn=B):
    D = arrays(d); w = d[wcol].values if wcol else np.ones(len(d))
    cm = None if ctrl is None else ctrl.values
    est = stats(D, w, cm)
    if mode == "stratum":
        units = [np.where(d.stratum.values == s)[0] for s in d.stratum.unique()]
    else:   # project clusters within group
        units = None
        cl = {g: [np.where((d.grp.values == g) & (d.project.values == p))[0] for p in d[d.grp == g].project.unique()]
              for g in ("topic", "comparison")}
    sims = defaultdict(list)
    for _ in range(Bn):
        if mode == "stratum":
            idx = np.concatenate([u[RNG.integers(0, len(u), len(u))] for u in units])
        else:
            idx = np.concatenate([cl[g][k] for g in cl for k in RNG.integers(0, len(cl[g]), len(cl[g]))])
        Di = {k: v[idx] for k, v in D.items()}
        s = stats(Di, w[idx], None if cm is None else cm[idx])
        for k, v in s.items():
            if np.isfinite(v):
                sims[k].append(v)
    out = {}
    for k, v in est.items():
        lo, hi = (np.percentile(sims[k], [2.5, 97.5]) if len(sims[k]) > 0.5 * Bn else (np.nan, np.nan))
        out[k] = {"est": r(v), "lo": r(lo), "hi": r(hi)}
    return out


def fmt(x, scale=1, k=2, unit=""):
    if x["est"] is None:
        return "n/a"
    lo = np.nan if x["lo"] is None else x["lo"]; hi = np.nan if x["hi"] is None else x["hi"]
    return f"{x['est'] * scale:+.{k}f}{unit} [{lo * scale:+.{k}f}, {hi * scale:+.{k}f}]"


KEYS = [("a_unf", 1, 2, ""), ("a_res", 1, 2, ""), ("c_share", 100, 0, "%"), ("b_t", 100, 1, "%"), ("b_c", 100, 1, "%"), ("b", 100, 1, " pp"),
        ("b_full_did", 100, 1, " pp"), ("d_t", 100, 1, "%"), ("d_c", 100, 1, "%"), ("d", 100, 1, " pp"), ("d_did", 100, 1, " pp"),
        ("e_ip", 100, 1, "%"), ("e_ju", 100, 1, "%"), ("e", 100, 1, " pp"), ("e_full", 100, 1, " pp"), ("e_ju_vs_c", 100, 1, " pp"), ("a_pre_res", 1, 2, "")]


def show(title, res):
    print("== " + title)
    for k, s, kk, u in KEYS:
        if k in res:
            print(f"   {k:11} {fmt(res[k], s, kk, u)}")


# ---------- reproduce the cards, then weight
print("n okL", df.groupby("grp").okL.sum().to_dict(), "okG", df.groupby("grp").okG.sum().to_dict(), "okF", df.groupby("grp").okF.sum().to_dict())
main = {}
for sub in ("all", "relevant"):
    d = df if sub == "all" else df[df.rel].reset_index(drop=True)
    main[sub] = {"unweighted": bootstrap(d, None), "design_weighted": bootstrap(d, "w"),
                 "unweighted_projectCI": bootstrap(d, None, mode="cluster", Bn=400), "design_weighted_projectCI": bootstrap(d, "w", mode="cluster", Bn=400)}
    main[sub]["raw_design_weights_uncollapsed"] = bootstrap(d, "w_raw", Bn=300)
    main[sub]["topic_weighted_only"] = bootstrap(d.assign(w_t=np.where(d.is_t, d.w, 1.0)), "w_t")
    for k, v in main[sub].items():
        show(f"{sub} / {k}", v)

# importance-specific DiDs and importance-standardised estimate (comparison reweighted to topic population's level mix)
imp = {}
for l in LEVELS:
    d = df[df.importance == l].reset_index(drop=True)
    imp[l] = {"n_t": int((d.grp == "topic").sum()), "n_c": int((d.grp == "comparison").sum()),
              "unweighted": bootstrap(d, None, Bn=500), "design_weighted": bootstrap(d, "w", Bn=500)}
    show(f"importance={l} unweighted (n_t={imp[l]['n_t']}, n_c={imp[l]['n_c']})", imp[l]["unweighted"])
    show(f"importance={l} weighted", imp[l]["design_weighted"])
# standardisation: topic keeps design weights; each comparison importance level is rescaled to the topic population share of that level
tp = df[df.is_t].groupby("importance").w.sum(); tp = tp / tp.sum()
cp = df[~df.is_t].groupby("importance").w.sum(); cp = cp / cp.sum()
df["w_std"] = df.w
for l in LEVELS:
    m = (~df.is_t) & (df.importance == l)
    df.loc[m, "w_std"] = df.loc[m, "w"] * tp[l] / cp[l]
print("population level mix topic", tp.round(3).to_dict(), "comparison (covered)", cp.round(3).to_dict())
std = {s: bootstrap(df if s == "all" else df[df.rel].reset_index(drop=True), "w_std") for s in ("all", "relevant")}
show("importance-standardised (comparison levels reweighted to topic mix)", std["all"])
show("importance-standardised, relevant", std["relevant"])
# Top+High only (the levels both groups actually sample), design-weighted
th = df[df.importance.isin(["Top", "High"])].reset_index(drop=True)
thres = {"unweighted": bootstrap(th, None), "design_weighted": bootstrap(th, "w")}
show("Top+High only, unweighted", thres["unweighted"]); show("Top+High only, weighted", thres["design_weighted"])

# ============================================================ 2. selection effects (sample vs population, topic vs comparison)
sel = {}
for g in ("topic", "comparison"):
    d = df[df.grp == g]
    sel[g] = {"importance_mix_sample": d.importance.value_counts(normalize=True).round(3).to_dict(),
              "importance_mix_population": (d.groupby("importance").w.sum() / d.w.sum()).round(3).to_dict(),
              "created_after_2021_share": r((d.created_in_window.notna()).mean(), 3),
              "created_after_2021_share_weighted": r((d.created_in_window.notna() * d.w).sum() / d.w.sum(), 3),
              "stub_or_start_share": r(d.qclass.isin(["stub", "start"]).mean(), 3),
              "stub_or_start_share_weighted": r((d.qclass.isin(["stub", "start"]) * d.w).sum() / d.w.sum(), 3),
              "ga_fa_share": r(d.qclass.isin(["ga", "fa"]).mean(), 3),
              "median_bytes_now": r(d.bytes_nw.median(), 0), "median_lead_words_2023": r(d.lw_23.median(), 0),
              "median_edits_prewar": r(d.edits_w1.median(), 0), "median_views_per_month_prewar": r(d.vpm_w1.median(), 0),
              "relevant_share": r(d.rel.mean(), 3), "ct_notice_share": r(d.ct_notice.mean(), 3),
              "multi_title_rows(redirect dupes merged)": int((d.n_frame_titles > 1).sum()),
              "n": int(len(d))}
# cross-tagging contamination
tp_names = {"Israel", "Palestine", "Judaism", "Jewish history"}
cp_names = set(CONTROL)
comp_with_topic_tag = df[(df.grp == "comparison") & df.assess_projects.apply(lambda s: bool(tp_names & set(s.split("|"))))]
top_with_comp_tag = df[(df.grp == "topic") & df.assess_projects.apply(lambda s: bool(cp_names & set(s.split("|"))))]
sel["cross_tagged"] = {"comparison_articles_with_a_topic_project_tag_now": int(len(comp_with_topic_tag)),
                       "examples": comp_with_topic_tag.sort_values("v12", ascending=False).title.head(12).tolist(),
                       "topic_articles_with_a_comparison_project_tag_now": int(len(top_with_comp_tag)),
                       "examples_topic": top_with_comp_tag.sort_values("v12", ascending=False).title.head(12).tolist(),
                       "excluded_both_in_frame": fr["excluded_both"]}
sel["indiana_rows_in_India_sample"] = [t for t in df[df.project == "India"].title if "Indiana" in t or "Indianapolis" in t]
print("== selection", json.dumps(sel, indent=1, ensure_ascii=False))
# does the cross-tagged comparison set behave like topic?
ct = df.title.isin(comp_with_topic_tag.title)
show("comparison excluding cross-tagged articles (unweighted)", bootstrap(df, None, ctrl=~ct, Bn=500))

# ============================================================ 4. balance and matching
df["log_lw21"] = np.log1p(df.lw_21.fillna(0)); df["miss21"] = df.lw_21.isna().astype(float)
df["log_pageid"] = np.log(df.pageid.astype(float))
df["created_post2021"] = df.created_in_window.notna().astype(float)
df["log_ed1"] = np.log1p(df.edits_w1.astype(float)); df["log_vpm1"] = np.log1p(df.vpm_w1.astype(float).fillna(0))
df["imp_ord"] = df.importance.map({"Top": 3, "High": 2, "Mid": 1}).astype(float)
df["base_crit_any"] = (df.crit_23.fillna(0) > 0).astype(float)
COV = [("lead words 2021 (log)", "log_lw21"), ("no 2021 lead", "miss21"), ("page id (log; age proxy, higher = newer)", "log_pageid"),
       ("created after 2021-01-01", "created_post2021"), ("edits 2021-01..2023-07 (log)", "log_ed1"),
       ("views/month 2021-01..2023-07 (log)", "log_vpm1"), ("importance (Top=3, High=2, Mid=1)", "imp_ord"),
       ("lead had a critical term in Jul 2023", "base_crit_any")]


def smd(d, w=None, cols=COV):
    w = np.ones(len(d)) if w is None else np.asarray(w)
    t = d.is_t.values; out = {}
    for lab, c in cols:
        x = d[c].values.astype(float)
        mt = np.average(x[t], weights=w[t]); mc = np.average(x[~t], weights=w[~t])
        vt = np.average((x[t] - mt) ** 2, weights=w[t]); vc = np.average((x[~t] - mc) ** 2, weights=w[~t])
        sd0 = math.sqrt((x[t].var() + x[~t].var()) / 2)            # pooled SD of the raw sample, fixed across adjustments
        out[lab] = {"mean_topic": r(mt, 3), "mean_comp": r(mc, 3), "smd": r((mt - mc) / sd0 if sd0 else np.nan, 3)}
    return out


def cem_weights(d, ncut=4):
    """Coarsened exact matching (ATT weights). Bins: quantiles of each continuous covariate on the pooled sample."""
    key = d.importance.astype(str)
    for c in ("log_lw21", "log_pageid", "log_ed1", "log_vpm1"):
        q = pd.qcut(d[c].rank(method="first"), ncut, labels=False).astype(str)
        key = key + "|" + q
    key = key + "|" + d.miss21.astype(int).astype(str) + "|" + d.created_post2021.astype(int).astype(str)
    t = d.is_t.values
    tab = pd.crosstab(key, t)
    if True not in tab.columns or False not in tab.columns:
        return np.zeros(len(d))
    ok = tab[(tab[True] > 0) & (tab[False] > 0)]
    nt_m, nc_m = ok[True].sum(), ok[False].sum()
    wt = np.zeros(len(d))
    kk = key.values
    good = set(ok.index)
    for i in range(len(d)):
        if kk[i] in good:
            wt[i] = 1.0 if t[i] else (ok.loc[kk[i], True] / ok.loc[kk[i], False]) * (nc_m / nt_m)
    return wt


PSX = ["log_lw21", "miss21", "log_pageid", "created_post2021", "log_ed1", "log_vpm1"]


def ps_weights(d):
    """1:1 nearest-neighbour propensity matching with replacement, caliper 0.2 SD of the logit; returns match weights."""
    X = pd.get_dummies(d.importance, drop_first=True, dtype=float)
    X = pd.concat([d[PSX].astype(float), X], axis=1)
    X = sm.add_constant(X)
    m = sm.Logit(d.is_t.astype(float).values, X.values).fit(disp=0, maxiter=200)
    lp = X.values @ m.params
    t = d.is_t.values
    cal = 0.2 * lp.std()
    ci = np.where(~t)[0]; order = np.argsort(lp[ci]); cs = lp[ci][order]
    wt = np.zeros(len(d))
    for i in np.where(t)[0]:
        j = np.searchsorted(cs, lp[i])
        cand = [k for k in (j - 1, j) if 0 <= k < len(cs)]
        k = min(cand, key=lambda k: abs(cs[k] - lp[i]))
        if abs(cs[k] - lp[i]) <= cal:
            wt[i] += 1; wt[ci[order[k]]] += 1
    return wt


def match_boot(d, method, Bn=300):
    """Re-runs the matching in every bootstrap replicate (articles resampled within group)."""
    fn = cem_weights if method == "cem" else ps_weights
    def one(dd):
        w = fn(dd)
        D = arrays(dd)
        s = stats(D, w)
        return {k: s[k] for k in ("a_unf", "a_res", "b_t", "b_c", "b", "b_full_did")}, w
    est, w0 = one(d)
    sims = defaultdict(list)
    gi = {g: np.where(d.grp.values == g)[0] for g in ("topic", "comparison")}
    for _ in range(Bn):
        idx = np.concatenate([gi[g][RNG.integers(0, len(gi[g]), len(gi[g]))] for g in gi])
        s, _ = one(d.iloc[idx].reset_index(drop=True))
        for k, v in s.items():
            if np.isfinite(v):
                sims[k].append(v)
    out = {k: {"est": r(v), "lo": r(np.percentile(sims[k], 2.5)), "hi": r(np.percentile(sims[k], 97.5))} for k, v in est.items()}
    t = d.is_t.values
    out["_matched"] = {"topic_kept": int((w0[t] > 0).sum()), "topic_total": int(t.sum()), "comparison_used": int((w0[~t] > 0).sum()),
                       "comparison_total": int((~t).sum())}
    return out, w0


bal, matched = {}, {}
for sub in ("all", "relevant"):
    d = (df if sub == "all" else df[df.rel]).reset_index(drop=True)
    res_c, wc = match_boot(d, "cem", Bn=int(os.environ.get("AUDIT_MB", "300")))
    res_p, wp = match_boot(d, "ps", Bn=int(os.environ.get("AUDIT_MB", "300")))
    bal[sub] = {"unweighted": smd(d), "design_weighted": smd(d, d.w.values), "cem": smd(d.iloc[np.where(wc > 0)[0]], wc[wc > 0]),
                "ps_matched": smd(d.iloc[np.where(wp > 0)[0]], wp[wp > 0])}
    matched[sub] = {"cem": res_c, "ps_nn": res_p}
    print(f"== balance ({sub})")
    for lab, _ in COV:
        print(f"   {lab:42} " + "  ".join(f"{k}={bal[sub][k][lab]['smd']:+.2f}" for k in bal[sub]))
    for k, v in matched[sub].items():
        print(f"   matched {k}: {v['_matched']}")
        for kk in ("a_unf", "a_res", "b_t", "b_c", "b", "b_full_did"):
            s = 100 if kk.startswith("b") else 1
            print(f"      {kk:10} {fmt(v[kk], s, 2 if s == 1 else 1)}")

# ============================================================ 5. which comparison projects
proj = []
for (g, p), d in df.groupby(["grp", "project"]):
    L = d[d.okL]
    proj.append({"group": g, "project": p, "n": int(len(d)), "ct_notice": r(d.ct_notice.mean(), 3), "relevant": r(d.rel.mean(), 3),
                 "base_rate_2023": r((L.crit_23 * 1e4 / L.lw_23).mean(), 2), "pre_war_change": r(L.pre_unf.mean(), 2),
                 "post_war_change": r(L.post_unf.mean(), 2), "gain_share": r(d.gain.mean(), 4),
                 "log_edits_prewar": r(d.log_ed1.mean(), 2), "share_top": r((d.importance == "Top").mean(), 3)})
PJ = pd.DataFrame(proj)
ip_ref = df[df.ip]; Lr = ip_ref[ip_ref.okL]
ref = {"ct_notice": ip_ref.ct_notice.mean(), "relevant": ip_ref.rel.mean(), "base_rate_2023": (Lr.crit_23 * 1e4 / Lr.lw_23).mean(),
       "pre_war_change": Lr.pre_unf.mean(), "log_edits_prewar": ip_ref.log_ed1.mean()}
feat = list(ref)
C = PJ[PJ.group == "comparison"].copy()
sd_ = C[feat].std()
C["distance_to_IsraelPalestine"] = np.sqrt((((C[feat] - pd.Series(ref)) / sd_) ** 2).sum(axis=1))
C["a_priori"] = C.project.map(lambda p: "conflict" if p in CONFLICT else "religion" if p in RELIGION else "country")
C = C.sort_values("distance_to_IsraelPalestine")
print("== comparison projects ranked by similarity to Israel+Palestine (pre-treatment features)")
print(C[["project", "a_priori", "n", "ct_notice", "relevant", "base_rate_2023", "pre_war_change", "log_edits_prewar", "distance_to_IsraelPalestine", "post_war_change", "gain_share"]].to_string(index=False))
print("topic projects:\n", PJ[PJ.group == "topic"].to_string(index=False))
nearest = C.project.head(8).tolist()
subsets = {"all comparison": None, "conflict projects (a priori)": CONFLICT, "religion projects": RELIGION, "country projects": COUNTRY,
           "8 most similar (data-driven)": nearest, "live wars 2022+ (Ukraine, Russia, Armenia, Azerbaijan)": ["Ukraine", "Russia", "Armenia", "Azerbaijan"]}
comp_sets = {}
for nm, P in subsets.items():
    for sub in ("all", "relevant"):
        d = (df if sub == "all" else df[df.rel]).reset_index(drop=True)
        ctrl = None if P is None else d.project.isin(P)
        comp_sets[f"{nm} | {sub}"] = {"unweighted": bootstrap(d, None, ctrl=ctrl, Bn=500), "design_weighted": bootstrap(d, "w", ctrl=ctrl, Bn=500),
                                      "n_comparison": int((~d.is_t & (True if ctrl is None else ctrl)).sum())}
        show(f"comparison = {nm} ({sub}), unweighted", comp_sets[f"{nm} | {sub}"]["unweighted"])
        show(f"comparison = {nm} ({sub}), weighted", comp_sets[f"{nm} | {sub}"]["design_weighted"])
# conflict-only + CEM
dcf = df[df.is_t | df.project.isin(CONFLICT)].reset_index(drop=True)
cf_cem, _ = match_boot(dcf, "cem", Bn=200)
print("conflict-only CEM:", {k: v for k, v in cf_cem.items()})

# ============================================================ mass v1 A1 / A5 (the +3.6 pp headline) weighted
la = json.load(open(os.path.join(WT, "data", "mass_results.json")))["mass"]
FR = la["lab_frames"]; CR = [FR.index(k) + 1 for k in ["settler_colonial", "apartheid", "genocide", "ethnic_cleansing", "occupation", "nakba_expulsion", "war_crimes"]]
v1 = []
for a in la["lab_articles"]:
    f = a["f"]
    if f is None or any(x is None or x[0] <= 0 for x in f):
        continue
    cnt = [sum(x[i] for i in CR) for x in f]
    g = "topic" if a["g"] == "t" else "comparison"
    imp_ = {"T": "Top", "H": "High", "M": "Mid"}[a["i"]]
    half = "discovery" if int(hashlib.sha1(("study3|" + a["t"]).encode()).hexdigest(), 16) % 2 == 0 else "holdout"
    v1.append({"title": a["t"], "grp": g, "project": a["p"], "importance": imp_, "up_post": float(cnt[2] > cnt[1]), "up_pre": float(cnt[1] > cnt[0]), "half": half})
V1 = pd.DataFrame(v1)
n1 = Counter(zip(V1.grp, V1.project, V1.importance))
Npool = {(x.group, x.project, x.importance): x.N_pool_est for _, x in st_ok.iterrows()}
V1["w"] = [Npool[k] / n1[k] for k in zip(V1.grp, V1.project, V1.importance)]
V1["stratum"] = V1.grp + "|" + V1.project + "|" + V1.importance
V1["d"] = V1.up_post - V1.up_pre


def a1(d, w):
    t = d.grp.values == "topic"
    x = d.d.values
    ip = np.isin(d.project.values, ["Israel", "Palestine"]); ju = d.project.values == "Judaism"
    return {"A1": np.average(x[t], weights=w[t]) - np.average(x[~t], weights=w[~t]),
            "A5": np.average(x[t & ip], weights=w[t & ip]) - np.average(x[t & ju], weights=w[t & ju]),
            "A5b": np.average(x[t & ju], weights=w[t & ju]) - np.average(x[~t], weights=w[~t])}


v1res = {}
for half in ("holdout", "all"):
    d = (V1 if half == "all" else V1[V1.half == half]).reset_index(drop=True)
    units = [np.where(d.stratum.values == s)[0] for s in d.stratum.unique()]
    for lab, w in (("unweighted", np.ones(len(d))), ("design_weighted", d.w.values)):
        est = a1(d, w); sims = defaultdict(list)
        for _ in range(B):
            idx = np.concatenate([u[RNG.integers(0, len(u), len(u))] for u in units])
            for k, v in a1(d.iloc[idx], w[idx]).items():
                sims[k].append(v)
        v1res[f"{half}:{lab}"] = {k: {"est": r(v), "lo": r(np.percentile(sims[k], 2.5)), "hi": r(np.percentile(sims[k], 97.5))} for k, v in est.items()}
        print(f"mass v1 {half} {lab}: " + "; ".join(f"{k} {fmt(v, 100, 1, ' pp')}" for k, v in v1res[f'{half}:{lab}'].items()) + f" (n={len(d)})")

# ============================================================ chart data
dump("01_population_vs_sample.json", {"note": "per WikiProject x importance: category talk-page count (frame.json category_counts), estimated pool after "
      "first-project assignment and 'both' exclusion, frame and mass2 sample sizes, inclusion probability pi = n_mass2 / N_pool_est",
      "rows": strata, "group_totals": grp_tab})
dump("02_balance_smd.json", {"note": "standardised mean differences topic minus comparison (pooled raw-sample SD in the denominator); "
     "|SMD| < 0.1 is the usual balance bar. Columns: unweighted sample, design-weighted, after CEM, after 1:1 propensity matching",
     "chart": {"type": "dot plot (Love plot)", "x": "SMD", "y": "covariate", "series": "adjustment"}, "balance": bal})
rows = []
lab = {"a_unf": "(a) post-war lead critical DiD, hits/10k words", "b": "(b) share of leads gaining critical terms, topic minus comparison",
       "b_t": "(b) topic share gaining", "b_c": "(b) comparison share gaining", "b_full_did": "(b') full-text gain share, post-pre DiD (A1 analogue)",
       "c_share": "(c) narrative-residual share of (a)", "a_res": "(c) narrative-residual DiD", "d_t": "(d) topic view share on gaining leads",
       "d_c": "(d) comparison view share on gaining leads", "d_did": "(d) views-share minus article-share DiD",
       "e": "(e) Israel+Palestine minus Judaism, lead gain share", "e_full": "(e') Israel+Palestine minus Judaism, full-text post-pre (A5 analogue)",
       "e_ju_vs_c": "(e'') Judaism minus comparison, lead gain share"}
for sub in ("all", "relevant"):
    for k, nm in lab.items():
        row = {"subset": sub, "statistic": k, "label": nm}
        for v in ("unweighted", "design_weighted", "unweighted_projectCI", "design_weighted_projectCI", "raw_design_weights_uncollapsed", "topic_weighted_only"):
            row[v] = main[sub][v][k]
        row["importance_standardised"] = std[sub][k]
        if sub == "all":
            row["top_high_only_weighted"] = thres["design_weighted"][k]
        if k in matched[sub]["cem"]:
            row["cem"] = matched[sub]["cem"][k]; row["ps_nn"] = matched[sub]["ps_nn"][k]
        rows.append(row)
dump("03_weighted_vs_unweighted.json", {"note": "headline mass2 statistics, unweighted vs design-weighted (inverse inclusion probability within "
     "project x importance), with stratified-bootstrap 95% CIs (and project-cluster CIs), importance-standardised and matched versions",
     "chart": {"type": "paired dot-and-whisker per statistic", "series": "unweighted vs design-weighted"}, "rows": rows,
     "by_importance": {l: {"n_t": imp[l]["n_t"], "n_c": imp[l]["n_c"], "unweighted": {k: imp[l]["unweighted"][k] for k in lab},
                           "design_weighted": {k: imp[l]["design_weighted"][k] for k in lab}} for l in LEVELS},
     "mass_v1_A1_A5": v1res})
dump("04_comparison_projects.json", {"note": "comparison projects ranked by distance to Israel+Palestine on pre-war features; estimates against "
     "comparison subsets", "projects": C.to_dict("records"), "topic_projects": PJ[PJ.group == "topic"].to_dict("records"),
     "reference_IsraelPalestine": ref, "estimates": {k: {kk: (vv if kk == "n_comparison" else {s: vv[s] for s in ("a_unf", "b", "b_t", "b_c", "b_full_did", "d_t", "d_c")})
                                                       for kk, vv in v.items()} for k, v in comp_sets.items()},
     "conflict_only_cem": cf_cem})
dump("05_selection_effects.json", sel)
print("done")
