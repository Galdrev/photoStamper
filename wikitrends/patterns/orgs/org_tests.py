"""Tests of the organisational footprints in footprints.json (written before this script was run).

python patterns/orgs/org_tests.py  ->  patterns/orgs/org_tests.json (+ printout)

All tests are aggregate. Account hashes are used only within one article (concentration test), never across
articles, and never linked to any person or organisation.
"""
import gzip, json, math, os
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(WT, "data")
CRIT = ["settler_colonial", "apartheid", "genocide", "ethnic_cleansing", "occupation", "nakba_expulsion", "war_crimes"]
WEEK0 = date(2021, 1, 1)
NOW = date(2026, 11, 5)
NW = (NOW - WEEK0).days // 7
RNG = np.random.default_rng(20261106)
NPL = 2000


def wk(d):
    if isinstance(d, str):
        d = date.fromisoformat(d[:10])
    return (d - WEEK0).days // 7


# ------------------------------------------------------------------ data
m2 = json.load(open(os.path.join(DATA, "mass2.json")))
group = {a["title"]: a["group"] for a in m2["articles"]}
ev = json.load(gzip.open(os.path.join(DATA, "mass2_events.json.gz"), "rt"))["articles"]
EV = []                                              # (title, group, week, ts, term, kind, reverted, u, acct)
for t, det in ev.items():
    g = group.get(t)
    if g not in ("topic", "comparison"):
        continue
    for e in det.get("lead_events") or []:
        if e.get("term") in CRIT and e.get("ts"):
            EV.append((t, g, wk(e["ts"]), e["ts"], e["term"], e["kind"], bool(e.get("reverted")), e.get("u"), e.get("acct") or {}))


def series(g, kind=None, term=None, nonrev=False):
    s = np.zeros(NW)
    for (t, gg, w, ts, term_, k, rev, u, acct) in EV:
        if gg != g or not (0 <= w < NW):
            continue
        if kind and k != kind:
            continue
        if term and term_ != term:
            continue
        if nonrev and rev:
            continue
        s[w] += 1
    return s


res = json.load(open(os.path.join(DATA, "results.json")))
def parse_weekly(s, n):
    v = np.zeros(n)
    for i, x in enumerate((s or "").split(",")[:n]):
        if x:
            v[i] = float(x)
    return v
DEEP_T, DEEP_C = np.zeros(res["n_weeks"]), np.zeros(res["n_weeks"])
for a in res["articles"]:
    if a.get("created_in_window"):
        continue
    w = parse_weekly(a.get("w_edits"), res["n_weeks"])
    if a["group"] == "treatment":
        DEEP_T += w
    elif a["group"] == "control" and not a.get("shocked"):
        DEEP_C += w


# ------------------------------------------------------------------ DiD with placebo
def did(T, C, i, L):
    tp, tq = T[i - L:i].sum(), T[i:i + L].sum()
    cp, cq = C[i - L:i].sum(), C[i:i + L].sum()
    return math.log((tq + 1) / (tp + 1)) - math.log((cq + 1) / (cp + 1)), (tp, tq, cp, cq)


def placebo_weeks(L, lo=wk("2021-07-01"), hi=wk("2026-09-01")):
    return RNG.integers(max(lo, L), min(hi, NW - L), NPL)


def did_test(T, C, d, L, direction):
    i = wk(d)
    obs, cnt = did(T, C, i, L)
    pl = np.array([did(T, C, j, L)[0] for j in placebo_weeks(L)])
    loc = np.array([did(T, C, j, L)[0] for j in range(max(L, i - 26), min(NW - L, i + 27)) if abs(j - i) >= L])
    sgn = 1 if direction == "+" else -1
    p = float(np.mean(sgn * pl >= sgn * obs))
    pl_loc = float(np.mean(sgn * loc >= sgn * obs)) if len(loc) else None
    return {"date": d, "weeks": L, "direction": direction, "stat": round(obs, 3),
            "ratio": round(math.exp(obs), 2), "topic_pre_post": [int(cnt[0]), int(cnt[1])],
            "cmp_pre_post": [int(cnt[2]), int(cnt[3])], "p_global": round(p, 3), "p_local": None if pl_loc is None else round(pl_loc, 3),
            "placebo_sd": round(float(pl.std()), 3)}


OUT = {"generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "n_events": len(EV), "tests": {}}
S = {}
for g in ("topic", "comparison"):
    for k in (None, "insert", "remove"):
        S[(g, k)] = series(g, k)
        S[(g, k, "nr")] = series(g, k, nonrev=True)
S[("topic", "insert", "genocide")] = series("topic", "insert", "genocide")
S[("comparison", "insert", "genocide")] = series("comparison", "insert", "genocide")

PLAN = [  # id, date, kind, direction
    ("F1a", "2024-01-15", "insert", "+"), ("F1a_s1", "2024-01-01", "insert", "+"), ("F1a_s2", "2024-02-01", "insert", "+"),
    ("F1b", "2024-10-24", "insert", "-"), ("F1c", "2024-12-09", "insert", "-"),
    ("F2", "2024-01-20", "remove", "-"),
    ("F3a_ins", "2025-01-23", "insert", "-"), ("F3a_rem", "2025-01-23", "remove", "-"), ("F3a_all", "2025-01-23", None, "-"),
    ("F4a", "2025-03-18", "insert", "-"), ("F4b", "2025-04-25", "insert", "-"),
    ("F5b", "2021-11-01", "insert", "+"),
]
for fid, d, k, dirn in PLAN:
    OUT["tests"][fid] = {"main_4w": did_test(S[("topic", k)], S[("comparison", k)], d, 4, dirn),
                         "sens_8w": did_test(S[("topic", k)], S[("comparison", k)], d, 8, dirn),
                         "sens_nonreverted_4w": did_test(S[("topic", k, "nr")], S[("comparison", k, "nr")], d, 4, dirn)}

# F5a: genocide insertions, and non-EC insertions on topic leads after Feb 2026
g_t, g_c = S[("topic", "insert", "genocide")], S[("comparison", "insert", "genocide")]
OUT["tests"]["F5a"] = {"main_4w": did_test(g_t, g_c, "2026-02-16", 4, "+"), "sens_8w": did_test(g_t, g_c, "2026-02-16", 8, "+")}
i0 = wk("2026-02-16")
def nonec(lo, hi):
    rows = [e for e in EV if e[1] == "topic" and e[5] == "insert" and lo <= e[2] < hi]
    return {"insertions": len(rows), "non_ec": sum(1 for e in rows if e[8] and e[8].get("ext") is False),
            "lt500": sum(1 for e in rows if e[8].get("lt500")), "genocide": sum(1 for e in rows if e[4] == "genocide")}
OUT["tests"]["F5a"]["non_ec_topic_insertions"] = {"12w_before": nonec(i0 - 12, i0), "12w_after": nonec(i0, i0 + 12)}

# F3a weekly edits on deep panel
OUT["tests"]["F3a_deep_edits"] = {"main_4w": did_test(DEEP_T, DEEP_C, "2025-01-23", 4, "-"),
                                  "sens_8w": did_test(DEEP_T, DEEP_C, "2025-01-23", 8, "-")}
OUT["tests"]["F1b_deep_edits"] = {"main_4w": did_test(DEEP_T, DEEP_C, "2024-10-24", 4, "-")}
OUT["tests"]["F1a_deep_edits"] = {"main_4w": did_test(DEEP_T, DEEP_C, "2024-01-15", 4, "+")}


# joint test: exposure / sanction dates (F1b, F1c, F3a, F4a, F4b), mean of the 4-week insertion statistics vs random 5-date sets
def joint(dates, k, dirn, L=4):
    T, C = S[("topic", k)], S[("comparison", k)]
    obs = np.mean([did(T, C, wk(d), L)[0] for d in dates])
    pw = placebo_weeks(L)
    sets = RNG.choice(pw, (NPL, len(dates)))
    pl = np.array([np.mean([did(T, C, j, L)[0] for j in s]) for s in sets])
    sgn = 1 if dirn == "+" else -1
    return {"dates": dates, "mean_stat": round(float(obs), 3), "ratio": round(math.exp(obs), 2), "p": round(float(np.mean(sgn * pl >= sgn * obs)), 3)}
OUT["tests"]["joint_exposure_sanctions"] = joint(["2024-10-24", "2024-12-09", "2025-01-23", "2025-03-18", "2025-04-25"], "insert", "-")


# F1d / F4c: period ratios
def period(lo, hi, k="insert"):
    a, b = wk(lo), wk(hi)
    t, c = S[("topic", k)][a:b].sum(), S[("comparison", k)][a:b].sum()
    n = b - a
    return {"from": lo, "to": hi, "weeks": n, "topic_per_week": round(t / n, 2), "cmp_per_week": round(c / n, 2), "ratio": round(t / max(c, 1), 2)}
OUT["tests"]["F1d"] = {"pre_war_2023H1": period("2023-01-01", "2023-10-07"), "war_before_channel": period("2023-10-07", "2024-02-01"),
                       "channel_active": period("2024-02-01", "2024-10-01"), "after_exposure": period("2024-10-01", "2025-06-01"),
                       "later": period("2025-06-01", "2026-11-05")}
OUT["tests"]["F4c"] = {"y2024": period("2024-01-01", "2025-01-01"), "y2025": period("2025-01-01", "2026-01-01")}
def heavy_share(lo, hi, g="topic"):
    a, b = wk(lo), wk(hi)
    per = defaultdict(Counter)
    rows = [e for e in EV if e[1] == g and e[5] == "insert" and a <= e[2] < b and e[7]]
    for e in [e for e in EV if e[1] == g and a <= e[2] < b and e[7]]:
        per[e[0]][e[7]] += 1
    heavy = sum(1 for e in rows if per[e[0]][e[7]] >= 3)
    return {"insertions_with_hash": len(rows), "share_by_accounts_with_3plus_flips_on_same_article": round(heavy / max(len(rows), 1), 3)}
OUT["tests"]["F4c"]["heavy_2024"] = heavy_share("2024-01-01", "2025-01-01")
OUT["tests"]["F4c"]["heavy_2025"] = heavy_share("2025-01-01", "2026-01-01")
OUT["tests"]["F4c"]["heavy_2023"] = heavy_share("2023-01-01", "2024-01-01")
for y in ("2023", "2024", "2025"):
    OUT["tests"]["F4c"][f"heavy_cmp_{y}"] = heavy_share(f"{y}-01-01", f"{int(y)+1}-01-01", "comparison")


# F3b: concentration before/after (12 months), topic vs comparison, real date vs placebo one year earlier
def conc(d, g, months=12, min_flips=5):
    i = date.fromisoformat(d)
    lo, hi = i - timedelta(days=365 * months // 12), i + timedelta(days=365 * months // 12)
    pre, post = defaultdict(Counter), defaultdict(Counter)
    for (t, gg, w, ts, term, k, rev, u, acct) in EV:
        if gg != g or not u:
            continue
        x = date.fromisoformat(ts[:10])
        if lo <= x < i:
            pre[t][u] += 1
        elif i <= x < hi:
            post[t][u] += 1
    arts = [t for t in pre if sum(pre[t].values()) >= min_flips and sum(post[t].values()) >= min_flips]
    top1 = lambda c: max(c.values()) / sum(c.values())
    carry = [sum(post[t][u] for u in post[t] if u in pre[t]) / sum(post[t].values()) for t in arts]
    return {"date": d, "group": g, "n_articles": len(arts),
            "top1_pre": round(float(np.mean([top1(pre[t]) for t in arts])), 3) if arts else None,
            "top1_post": round(float(np.mean([top1(post[t]) for t in arts])), 3) if arts else None,
            "carryover_share_of_post_flips_by_pre_accounts": round(float(np.mean(carry)), 3) if arts else None,
            "accounts_per_flip_pre": round(float(np.mean([len(pre[t]) / sum(pre[t].values()) for t in arts])), 3) if arts else None,
            "accounts_per_flip_post": round(float(np.mean([len(post[t]) / sum(post[t].values()) for t in arts])), 3) if arts else None}
OUT["tests"]["F3b"] = {f"{g}@{d}": conc(d, g) for d in ("2025-01-23", "2024-01-23", "2023-01-23") for g in ("topic", "comparison")}
OUT["tests"]["F3b_min3"] = {f"{g}@{d}": conc(d, g, min_flips=3) for d in ("2025-01-23", "2024-01-23") for g in ("topic", "comparison")}
# power: smallest post/pre ratio a one-sided 5% test could detect, from the placebo SD of the 4-week insertion DiD
_pl = np.array([did(S[("topic", "insert")], S[("comparison", "insert")], j, 4)[0] for j in placebo_weeks(4)])
OUT["power"] = {"placebo_sd_4w_insert": round(float(_pl.std()), 3), "placebo_q05": round(float(np.quantile(_pl, 0.05)), 3),
                "placebo_q95": round(float(np.quantile(_pl, 0.95)), 3),
                "detectable_drop_ratio": round(float(math.exp(np.quantile(_pl, 0.05))), 2), "detectable_rise_ratio": round(float(math.exp(np.quantile(_pl, 0.95))), 2)}


# F6: Zionism first sentence 'coloni-' removals, 6 weeks after 2024-09-14 vs random 6-week windows on the same article
ra = json.load(open(os.path.join(DATA, "ratchet.json")))["articles"]["Zionism"]
var = {v["id"]: v["s"] for v in ra["fs_variants"]}
tl = ra["fs_timeline"]
flips = []                                            # (date, +1 insert / -1 remove)
for (d0, v0, _), (d1, v1, _) in zip(tl, tl[1:]):
    if v0 in var and v1 in var:
        a, b = "coloni" in var[v0].lower(), "coloni" in var[v1].lower()
        if a != b:
            flips.append((date.fromisoformat(d1), 1 if b else -1))
def zcount(start, days=42, sign=-1):
    return sum(1 for (x, s) in flips if s == sign and start <= x < start + timedelta(days=days))
z0 = date(2024, 9, 14)
obs_r, obs_i = zcount(z0, sign=-1), zcount(z0, sign=1)
starts = [date(2021, 1, 1) + timedelta(days=int(k)) for k in RNG.integers(0, (date(2026, 9, 1) - date(2021, 1, 1)).days, NPL)]
pl = np.array([zcount(s, sign=-1) for s in starts])
starts24 = [date(2024, 1, 1) + timedelta(days=int(k)) for k in RNG.integers(0, 320, NPL)]
pl24 = np.array([zcount(s, sign=-1) for s in starts24])
OUT["tests"]["F6"] = {"window": "2024-09-14 + 42 days", "removals": obs_r, "insertions": obs_i,
                      "flips_total_with_text": len(flips), "removals_total": sum(1 for f in flips if f[1] < 0),
                      "p_vs_random_windows_2021_2026": round(float(np.mean(pl >= obs_r)), 3),
                      "p_vs_random_windows_2024_only": round(float(np.mean(pl24 >= obs_r)), 3),
                      "placebo_mean_2021_2026": round(float(pl.mean()), 2), "placebo_mean_2024": round(float(pl24.mean()), 2),
                      "by_month": dict(sorted(Counter(f"{x:%Y-%m}" for x, s in flips if s < 0).items()))}

json.dump(OUT, open(os.path.join(HERE, "org_tests.json"), "w"), indent=1, default=str)
print("power", OUT["power"])
for k, v in OUT["tests"].items():
    print(k, json.dumps(v, default=str))
