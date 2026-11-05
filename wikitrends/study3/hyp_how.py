"""HOW/WHO hypotheses: process behind critical-vocabulary change. Frozen on the discovery half.

Usage:  python3 hyp_how.py [deep.json] [mass.json]
Each h* function takes a list of articles in the corresponding schema (deep: D['articles']; mass: M['articles'])
and returns a dict with the point estimate and a bootstrap CI / permutation p. Seeds are fixed.

Shared definitions
  CRITICAL = 7 frames (settler_colonial, apartheid, genocide, ethnic_cleansing, occupation, nakba_expulsion, war_crimes)
  "critical count" = raw sum of the 7 frame counts (full text unless stated).
  "gain" in a period = critical count at period end > count at period start (strict).
  mass periods: pre = 2021-01 -> 2023-07 (f[0]->f[1]); post = 2023-07 -> latest (f[1]->f[2]).
  deep periods: pre-war snapshot = last crit_series_date <= 2023-07; end = last snapshot.
  deep groups: treatment vs control (control_contaminated dropped). mass groups: g == 't' vs 'c'.
  Mass articles need non-null f at all 3 dates.
"""
import json, sys
import numpy as np

CR = ["settler_colonial", "apartheid", "genocide", "ethnic_cleansing", "occupation", "nakba_expulsion", "war_crimes"]
PLACEBO = ["terrorism", "militant", "placebo_geography", "indigenous_homeland", "persecution_antisemitism"]
Q = [f"{y}-Q{q}" for y in range(2021, 2027) for q in range(1, 5)]   # index 11 = 2023-Q4
B = 2000


# ---------------------------------------------------------------- helpers
def _mass_rows(arts):
    out = []
    for a in arts:
        f = a["f"]
        if any(x is None for x in f):
            continue
        out.append(dict(T=int(a["g"] == "t"), e=a["e"], rv=a["rv"],
                        w=[x[0] for x in f], k=[sum(x[1:8]) for x in f]))
    return out


def _arr(rows, key):
    return np.array([r[key] for r in rows], float)


def _boot_groups(rows, fn, b=B, seed=0):
    """Stratified bootstrap (resample within T=1 and T=0)."""
    rng = np.random.default_rng(seed)
    T = np.array([r["T"] for r in rows]); it, ic = np.where(T == 1)[0], np.where(T == 0)[0]
    est = fn(rows); bs = []
    for _ in range(b):
        idx = np.concatenate([rng.choice(it, len(it)), rng.choice(ic, len(ic))])
        bs.append(fn([rows[i] for i in idx]))
    bs = np.array(bs, float)
    lo, hi = np.nanpercentile(bs, [2.5, 97.5], axis=0)
    return est, lo, hi


def _qi(s):
    y, m = int(s[:4]), int(s[5:7]); return (y - 2021) * 4 + (m - 1) // 3


def _deep_rows(arts, frames=CR):
    rows = []
    for a in arts:
        if a["group"] not in ("treatment", "control"):
            continue
        d = a["crit_series_dates"]
        ix = [j for j, x in enumerate(d) if x <= "2023-07"]
        if not ix or d[0] != "2021-01":
            continue
        i = ix[-1]
        c = np.array([sum(a["frame_series"][k][j] for k in CR) for j in range(len(d))], float)
        p = np.array([sum(a["frame_series"][k][j] for k in PLACEBO) for j in range(len(d))], float)
        w = np.array(a["words_series"], float)
        qe = np.array([a["quarter_edits"].get(q, 0) for q in Q], float)
        rows.append(dict(T=int(a["group"] == "treatment"), d=d, c=c, p=p, w=w, i=i, qe=qe,
                         gain=int(c[-1] > c[i]), pgain=int(p[-1] > p[i]),
                         lpre=np.log1p(qe[:11].mean()), lpost=np.log1p(qe[11:23].mean()),
                         anyc=int(c[i] > 0), lw=np.log(max(w[i], 1))))
    return rows


def _logit(X, y, iters=50):
    """Plain Newton logit with tiny ridge (for bootstrap stability). Returns coefficients."""
    X = np.column_stack([np.ones(len(y)), X]); beta = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-np.clip(X @ beta, -30, 30)))
        g = X.T @ (y - p) - 1e-4 * beta
        Hm = (X * (p * (1 - p))[:, None]).T @ X + 1e-4 * np.eye(len(beta))
        step = np.linalg.solve(Hm, g); beta += step
        if np.abs(step).max() < 1e-8:
            break
    return beta


# ---------------------------------------------------------------- H1 (mass)
def h1_surge_concentration(mass_arts, top_q=0.8):
    """Excess post-war gain is concentrated in the highest-edit articles.
    hi = edits e >= pooled 80th percentile. For each stratum: DiD = [P(gain post)-P(gain pre)]_t - [same]_c.
    Statistic = DiD(hi) - DiD(rest). Prediction: > 0."""
    rows = _mass_rows(mass_arts)
    cut = np.quantile(_arr(rows, "e"), top_q)
    def did(rr, hi):
        out = []
        for T in (1, 0):
            x = [r for r in rr if r["T"] == T and (r["e"] >= cut) == hi]
            if not x: return np.nan
            out.append(np.mean([r["k"][2] > r["k"][1] for r in x]) - np.mean([r["k"][1] > r["k"][0] for r in x]))
        return out[0] - out[1]
    fn = lambda rr: [did(rr, True), did(rr, False), did(rr, True) - did(rr, False)]
    est, lo, hi = _boot_groups(rows, fn, seed=1)
    return {"edit_cut": cut, "DiD_hi": (est[0], lo[0], hi[0]), "DiD_rest": (est[1], lo[1], hi[1]),
            "triple_diff": (est[2], lo[2], hi[2])}


# ---------------------------------------------------------------- H2 (deep)
def h2_surge_not_baseline(deep_arts):
    """Within topic, critical gain is predicted by the post-war SURGE in editing, not by baseline churn.
    logit(gain ~ lpost + lpre + anyc + log words_pre), topic articles only.
    lpre = log1p(mean quarterly edits 2021Q1-2023Q3), lpost = log1p(mean 2023Q4-2026Q3).
    Statistic = coef(lpre) for critical gain minus coef(lpre) for placebo-frame gain (same model).
    Prediction: coef_lpre(critical) < 0 and difference < 0. Also report T x burst interaction (pooled)."""
    rows = [r for r in _deep_rows(deep_arts) if r["T"] == 1]
    def fn(rr):
        X = np.array([[r["lpost"], r["lpre"], r["anyc"], r["lw"]] for r in rr])
        bc = _logit(X, np.array([r["gain"] for r in rr], float))
        bp = _logit(X, np.array([r["pgain"] for r in rr], float))
        return [bc[2], bp[2], bc[2] - bp[2]]
    rng = np.random.default_rng(2); est = fn(rows)
    bs = np.array([fn([rows[i] for i in rng.integers(0, len(rows), len(rows))]) for _ in range(B)])
    lo, hi = np.percentile(bs, [2.5, 97.5], axis=0)
    allr = _deep_rows(deep_arts)
    burst = lambda rr: [np.median([r["lpost"] - r["lpre"] for r in rr if r["T"] == 1]) -
                        np.median([r["lpost"] - r["lpre"] for r in rr if r["T"] == 0])]
    be, bl, bh = _boot_groups(allr, burst, seed=3)
    return {"n_topic": len(rows), "coef_lpre_critical": (est[0], lo[0], hi[0]),
            "coef_lpre_placebo": (est[1], lo[1], hi[1]), "difference": (est[2], lo[2], hi[2]),
            "burst_median_T_minus_C": (be[0], bl[0], bh[0])}


# ---------------------------------------------------------------- H3 (mass + deep)
def h3_direction_ratchet_mass(mass_arts):
    """Among articles whose critical count changed, the share that went UP rises post-war more in topic.
    Statistic = [P(up|changed) post - pre]_t - [same]_c. Prediction > 0."""
    rows = _mass_rows(mass_arts)
    def pu(x, a, b):
        ch = [r for r in x if r["k"][b] != r["k"][a]]
        return np.mean([r["k"][b] > r["k"][a] for r in ch]) if ch else np.nan
    def fn(rr):
        t = [r for r in rr if r["T"] == 1]; c = [r for r in rr if r["T"] == 0]
        return [(pu(t, 1, 2) - pu(t, 0, 1)) - (pu(c, 1, 2) - pu(c, 0, 1)), pu(t, 1, 2), pu(c, 1, 2)]
    est, lo, hi = _boot_groups(rows, fn, seed=4)
    return {"DiD_P_up_given_changed": (est[0], lo[0], hi[0]), "topic_post": est[1], "control_post": est[2]}


def h3b_ratchet_deep(deep_arts):
    """Deep quarterly series: ratchet = sum(quarterly increases)/(sum increases + sum |decreases|) of critical count,
    among articles with any movement in the period. Statistic = [post - pre]_treatment - [post - pre]_control."""
    rows = _deep_rows(deep_arts)
    def rat(r, post):
        seg = r["c"][r["i"]:] if post else r["c"][:r["i"] + 1]
        df = np.diff(seg); pos, neg = df[df > 0].sum(), -df[df < 0].sum()
        return pos / (pos + neg) if pos + neg > 0 else np.nan
    for r in rows:
        r["rpost"], r["rpre"] = rat(r, True), rat(r, False)
    def fn(rr):
        m = lambda T, k: np.nanmean([r[k] for r in rr if r["T"] == T])
        return [(m(1, "rpost") - m(1, "rpre")) - (m(0, "rpost") - m(0, "rpre")), m(1, "rpost"), m(0, "rpost")]
    est, lo, hi = _boot_groups(rows, fn, seed=5)
    return {"DiD_ratchet": (est[0], lo[0], hi[0]), "treat_post": est[1], "control_post": est[2]}


# ---------------------------------------------------------------- H4 (mass)
def h4_growth_vs_rewrite(mass_arts, grow=1.05):
    """Excess gains arrive with text growth rather than rewriting at constant length.
    Among gainers in a period, share whose words grew >= 5%. Statistic = [post - pre]_t - [post - pre]_c.
    Prediction (growth story) > 0; rewrite story < 0."""
    rows = _mass_rows(mass_arts)
    def sh(x, a, b):
        g = [r for r in x if r["k"][b] > r["k"][a]]
        return np.mean([r["w"][b] / r["w"][a] >= grow for r in g]) if g else np.nan
    def fn(rr):
        t = [r for r in rr if r["T"] == 1]; c = [r for r in rr if r["T"] == 0]
        return [(sh(t, 1, 2) - sh(t, 0, 1)) - (sh(c, 1, 2) - sh(c, 0, 1)), sh(t, 1, 2), sh(c, 1, 2)]
    est, lo, hi = _boot_groups(rows, fn, seed=6)
    return {"DiD_share_growing_among_gainers": (est[0], lo[0], hi[0]), "topic_post": est[1], "control_post": est[2]}


# ---------------------------------------------------------------- H5 (deep)
def h5_timing_lag(deep_arts):
    """Do critical gains track the edit timeline (swept in with activity) or lag it (slow accretion)?
    Per article with any post-war gain, quarters 2023Q3..2026Q3: lag = gain-weighted mean quarter - edit-weighted
    mean quarter (positive increases only; a snapshot gap spreads its change evenly over the spanned quarters).
    Statistic = median lag treatment - median lag control, with permutation p (two-sided). Discovery: topic ~0, control > 0."""
    rows = []
    for r in _deep_rows(deep_arts):
        gq = np.zeros(24); d, c = r["d"], r["c"]
        for j in range(r["i"] + 1, len(d)):
            q0, q1 = _qi(d[j - 1]), _qi(d[j])
            if q1 > q0: gq[q0:q1] += (c[j] - c[j - 1]) / (q1 - q0)
        x = np.arange(10, 23); pos = np.clip(gq[10:23], 0, None); e = r["qe"][10:23]
        if pos.sum() > 0 and e.sum() > 0:
            rows.append((r["T"], (x * pos).sum() / pos.sum() - (x * e).sum() / e.sum()))
    T = np.array([t for t, _ in rows]); L = np.array([l for _, l in rows])
    stat = lambda T: np.median(L[T == 1]) - np.median(L[T == 0])
    obs = stat(T); rng = np.random.default_rng(7)
    perm = np.array([stat(rng.permutation(T)) for _ in range(B)])
    return {"n_t": int((T == 1).sum()), "n_c": int((T == 0).sum()), "median_lag_t": np.median(L[T == 1]),
            "median_lag_c": np.median(L[T == 0]), "diff": obs, "perm_p": float((np.abs(perm) >= abs(obs)).mean())}


# ---------------------------------------------------------------- rejected (kept for re-test)
def r1_revert_moderation_mass(mass_arts):
    """REJECTED: contested (high revert share) articles show steeper topic gain. Logit(gain post ~ T*log1p(e) + T*rvr
    + any_k1 + log w1). Statistic = coef T:rvr."""
    rows = _mass_rows(mass_arts)
    def fn(rr):
        T = np.array([r["T"] for r in rr], float); le = np.log1p(_arr(rr, "e")); rvr = _arr(rr, "rv") / np.maximum(_arr(rr, "e"), 1)
        X = np.column_stack([T, le, T * le, rvr, T * rvr, [r["k"][1] > 0 for r in rr], np.log([r["w"][1] for r in rr])])
        return [_logit(X, np.array([r["k"][2] > r["k"][1] for r in rr], float))[5]]
    est, lo, hi = _boot_groups(rows, fn, b=500, seed=8)
    return {"coef_T_x_revert_rate": (est[0], lo[0], hi[0])}


def r2_concentration_deep(deep_arts):
    """REJECTED: topic gains come from concentrated editing (top10 share), given volume.
    Topic only: logit(gain ~ log edits + top10 + anyc + log words_pre). Statistic = coef top10."""
    keep = {a["title"]: a for a in deep_arts}
    rows = []
    for a in deep_arts:
        if a["group"] != "treatment" or a.get("top10") is None: continue
        r = _deep_rows([a])
        if r: rows.append((r[0], np.log(max(a["edits"], 1)), a["top10"]))
    def fn(rr):
        X = np.array([[le, t10, r["anyc"], r["lw"]] for r, le, t10 in rr]); y = np.array([r["gain"] for r, _, _ in rr], float)
        return _logit(X, y)[2]
    rng = np.random.default_rng(9); est = fn(rows)
    bs = [fn([rows[i] for i in rng.integers(0, len(rows), len(rows))]) for _ in range(B)]
    return {"coef_top10": (est, *np.percentile(bs, [2.5, 97.5]))}


if __name__ == "__main__":
    dp = sys.argv[1] if len(sys.argv) > 1 else "/home/user/photoStamper/wikitrends/data/study3/discovery_deep.json"
    mp = sys.argv[2] if len(sys.argv) > 2 else "/home/user/photoStamper/wikitrends/data/study3/discovery_mass.json"
    deep = json.load(open(dp))["articles"]; mass = json.load(open(mp))["articles"]
    np.set_printoptions(precision=4, suppress=True)
    for fn, arg in [(h1_surge_concentration, mass), (h2_surge_not_baseline, deep), (h3_direction_ratchet_mass, mass),
                    (h3b_ratchet_deep, deep), (h4_growth_vs_rewrite, mass), (h5_timing_lag, deep),
                    (r1_revert_moderation_mass, mass), (r2_concentration_deep, deep)]:
        res = fn(arg)
        print(fn.__name__, {k: (tuple(round(float(x), 4) for x in v) if isinstance(v, tuple) else round(float(v), 4))
                            for k, v in res.items()})
