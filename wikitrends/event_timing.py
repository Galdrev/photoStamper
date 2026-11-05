"""Event timing: do real-world events line up with edit surges and with vocabulary change?

Event study on weekly series against a calendar committed before looking at the data
(patterns/events/calendar.json). For each event and outcome:

    excess = (mean of weeks +0..+2 + c) / (mean of weeks -6..-1 + c)        (c = small smoothing for sparse counts)

compared with 2,000 random placebo dates from the same period (permutation p = share of placebo dates with an
excess at least as large). Type-level tests compare the mean log-excess of a type's events with the mean of the
same number of random dates. A local placebo (dates within +-26 weeks of each event) guards against the 2023-24
level shift. Overlap sensitivity drops an event when a stronger (higher a-priori tier) event, or an equal-tier
earlier one, lies within 21 days.

Outcomes (weekly unless noted)
  topic_edits        all revisions of deep-panel topic articles that existed before 2021 (results.json w_edits)
  comparison_edits   same for clean comparison articles (control group, contaminated excluded)
  shocked_edits      the shocked comparison articles (Ukraine, Russia, Armenia ...) - the placebo conflicts' own pages
  term_ins           critical-term insertions into topic leads (ratchet.json for its 40 key articles, pilot.json
                     lead term events for the other pilot articles; --mass2: data/mass2_events.json.gz instead)
  term_ins_durable   the subset of insertions that were still standing 7 days later
  term_ins_cmp       the same insertion count for comparison-article leads
  ins_per_edit       term insertions per 100 edits of the same lead-panel articles (edits from results.json)
  rfc_starts         RfC openings on topic talk pages (only with --mass2: the pilot keeps counts, not dates)
  pageviews          monthly, pilot.json (or mass2) topic articles: excess = mean(m, m+1) / mean(m-6..m-1)

Also: cross-correlation of weekly topic edits with weekly term insertions at lags -8..+8 (raw and first-differenced
log series), and a "which events left a mark" ranking with the lead changes in each window quoted from bisect.json
and ratchet.json first-sentence variants.

  python event_timing.py            -> data/event_timing.json, patterns/events/chart_data/*.json
  python event_timing.py --mass2    -> uses data/mass2_events.json.gz (+ mass2.json for groups/pageviews) if present
"""
import argparse, gzip, json, math, os, re, sys
from collections import Counter, defaultdict
from datetime import datetime, timezone, date, timedelta

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT_DIR = os.path.join(HERE, "patterns", "events")
CHART = os.path.join(OUT_DIR, "chart_data")
CRITICAL = ["settler_colonial", "apartheid", "genocide", "ethnic_cleansing", "occupation", "nakba_expulsion", "war_crimes"]
WEEK0 = date(2021, 1, 1)
PRE, POST = (-6, -1), (0, 2)
N_PLACEBO = 2000
SEED = 20261105
CAP = 10                      # per article-week cap for the robust edit series
TYPES = ["military_escalation", "ceasefire_deal", "legal_institutional", "humanitarian_media", "social_global", "comparison"]


def wk(d):
    if isinstance(d, (int, float)):
        d = datetime.fromtimestamp(d, tz=timezone.utc).date()
    elif isinstance(d, str):
        d = date.fromisoformat(d[:10])
    return (d - WEEK0).days // 7


def wk_date(i):
    return (WEEK0 + timedelta(days=7 * i)).isoformat()


def load_any(p):
    for q in (p, p + ".gz"):
        if os.path.exists(q):
            with (gzip.open(q, "rt", encoding="utf-8") if q.endswith(".gz") else open(q, encoding="utf-8")) as f:
                return json.load(f)
    return None


# ------------------------------------------------------------------ series
def parse_weekly(s, n):
    v = np.zeros(n)
    for i, x in enumerate((s or "").split(",")[:n]):
        if x:
            v[i] = float(x)
    return v


def deep_series(res):
    n = res["n_weeks"]
    out = {k: np.zeros(n) for k in ("topic_edits", "comparison_edits", "shocked_edits", "topic_reverted",
                                    "topic_active", "comparison_active", "topic_edits_capped")}
    per_title = {}
    cnt = Counter()
    for a in res["articles"]:
        w = parse_weekly(a.get("w_edits"), n)
        per_title[a["title"]] = w
        if a.get("created_in_window"):
            continue                                   # new pages would add a step at creation
        if a["group"] == "treatment":
            out["topic_edits"] += w; cnt["topic"] += 1
            out["topic_active"] += (w > 0)                 # robust: how many articles were edited that week
            out["topic_edits_capped"] += np.minimum(w, CAP)  # robust: one article's edit war counts at most CAP
            out["topic_reverted"] += parse_weekly(a.get("w_reverted"), n)
        elif a["group"] == "control":
            if a.get("shocked"):
                out["shocked_edits"] += w; cnt["shocked"] += 1
            else:
                out["comparison_edits"] += w; cnt["comparison"] += 1
                out["comparison_active"] += (w > 0)
    return out, per_title, dict(cnt), n


def durable_flags(evs):
    """evs: list of (t_epoch, term, kind) for one article, sorted. Insertion durable if the term is not removed
    within 7 days (censored insertions at the end count as durable if >= 7 days before the data end)."""
    out = []
    by_term = defaultdict(list)
    for e in evs:
        by_term[e[1]].append(e)
    for term, es in by_term.items():
        for i, e in enumerate(es):
            if e[2] != "insert":
                continue
            nxt = next((x for x in es[i + 1:] if x[2] == "remove"), None)
            out.append((e[0], term, nxt is None or nxt[0] - e[0] >= 7 * 86400))
    return out


def ts_epoch(ts):
    return datetime.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc).timestamp()


def lead_events_current(ratchet, pilot):
    """{title: {"group": topic|comparison, "events": [(t, term, kind, revid)], "src": ...}} from ratchet (preferred: every
    revision of 40 key articles) plus pilot lead term events for the other pilot articles."""
    from corpus import KEY_ARTICLES, KEY_ARTICLES_CONTROL
    arts = {}
    for t, fr in ratchet["events"].items():
        g = "topic" if t in KEY_ARTICLES else "comparison" if t in KEY_ARTICLES_CONTROL else None
        if not g:
            continue
        ev = [(e["t"], term, e["kind"], e.get("revid")) for term, es in fr.items() if term in CRITICAL for e in es]
        arts[t] = {"group": g, "events": sorted(ev), "src": "ratchet"}
    for t in ratchet["events"]:
        pass
    for t in set(KEY_ARTICLES) | set(KEY_ARTICLES_CONTROL):        # key articles with no events still count as panel members
        if t not in arts:
            arts[t] = {"group": "topic" if t in KEY_ARTICLES else "comparison", "events": [], "src": "ratchet"}
    for a in pilot["articles"]:
        t = a.get("canonical") or a["title"]
        if t in arts or a["title"] in arts or not a.get("term_events"):
            continue
        ev = [(ts_epoch(e["ts"]), e["term"], e["kind"], e.get("revid")) for e in a["term_events"].get("events") or []
              if e["term"] in CRITICAL]
        arts[a["title"]] = {"group": a["group"], "events": sorted(ev), "src": "pilot"}
    return arts


def lead_events_mass2(m2, m2ev):
    groups = {}
    for a in (m2 or {}).get("articles", []):
        groups[a.get("title")] = a.get("group")
    arts, rfc = {}, defaultdict(list)
    for t, det in (m2ev or {}).get("articles", {}).items():
        g = groups.get(t)
        if g not in ("topic", "comparison"):
            continue
        ev = []
        for e in det.get("lead_events") or []:
            if e.get("term") in CRITICAL and e.get("ts"):
                ev.append((ts_epoch(e["ts"]), e["term"], e["kind"], e.get("revid")))
        arts[t] = {"group": g, "events": sorted(ev), "src": "mass2"}
        for d in det.get("discussions") or []:
            if d.get("kind") == "rfc" and d.get("ts"):
                rfc[g].append(ts_epoch(d["ts"]))
    return arts, rfc


def term_series(arts, n):
    s = {k: np.zeros(n) for k in ("term_ins", "term_ins_durable", "term_rem", "term_ins_cmp", "term_ins_durable_cmp")}
    log = []
    for t, a in arts.items():
        cmp_ = a["group"] != "topic"
        for e in a["events"]:
            i = wk(e[0])
            if 0 <= i < n:
                if e[2] == "insert":
                    s["term_ins_cmp" if cmp_ else "term_ins"][i] += 1
                elif not cmp_:
                    s["term_rem"][i] += 1
        for (t0, term, dur) in durable_flags(a["events"]):
            i = wk(t0)
            if 0 <= i < n and dur:
                s["term_ins_durable_cmp" if cmp_ else "term_ins_durable"][i] += 1
            if not cmp_:
                log.append({"title": t, "t": t0, "term": term, "durable": dur})
    return s, log


def monthly_pageviews_current(pilot):
    tot = defaultdict(lambda: defaultdict(float))
    for a in pilot["articles"]:
        pv = (a.get("pageviews") or {}).get("all-access") or {}
        for m, v in pv.items():
            if v is not None:
                tot[a["group"]][m] += v
    return tot


def monthly_pageviews_mass2(m2):
    tot = defaultdict(lambda: defaultdict(float))
    for a in (m2 or {}).get("articles", []):
        pv = ((a.get("pageviews") or {}).get("monthly")) or {}
        if isinstance(pv, dict) and "views" in pv:
            y, mo = int(pv["start"][:4]), int(pv["start"][4:])
            for v in pv["views"]:
                if v is not None:
                    tot[a.get("group")][f"{y}{mo:02d}"] += v
                y, mo = (y, mo + 1) if mo < 12 else (y + 1, 1)
    return tot


# ------------------------------------------------------------------ event study
def excess_at(x, i, c, pre_w=PRE, post_w=POST):
    if i + pre_w[0] < 0:
        return None
    pre = x[i + pre_w[0]: i + pre_w[1] + 1]
    post = x[i + post_w[0]: i + post_w[1] + 1]
    if len(pre) < pre_w[1] - pre_w[0] + 1 or len(post) < post_w[1] - post_w[0] + 1:
        return None
    return (post.mean() + c) / (pre.mean() + c)


def smooth_c(x, lo, hi):
    """Smoothing constant: 10% of the series mean over the study period, at least 0.25 per week."""
    m = float(np.mean(x[lo:hi])) if hi > lo else 0.0
    return max(0.25, 0.1 * m)


def month_key(d):
    return f"{d.year}{d.month:02d}"


def add_months(y, m, k):
    t = y * 12 + (m - 1) + k
    return t // 12, t % 12 + 1


def pv_excess(series, d):
    y, m = d.year, d.month
    post = [series.get("%d%02d" % add_months(y, m, k)) for k in (0, 1)]
    pre = [series.get("%d%02d" % add_months(y, m, k)) for k in range(-6, 0)]
    if any(v is None or v == 0 for v in post + pre):
        return None
    return float(np.mean(post) / np.mean(pre))


def run(args):
    res = json.load(open(os.path.join(DATA, "results.json")))
    cal = json.load(open(os.path.join(OUT_DIR, "calendar.json")))["events"]
    deep, per_title, ncount, n = deep_series(res)
    ratchet = json.load(open(os.path.join(DATA, "ratchet.json")))
    pilot = json.load(open(os.path.join(DATA, "pilot", "pilot.json")))
    bisect = json.load(open(os.path.join(DATA, "bisect.json")))
    source, rfc = "ratchet+pilot", None
    if args.mass2:
        mdir = args.mass2_dir or DATA
        m2ev = load_any(os.path.join(mdir, "mass2_events.json.gz"))
        if m2ev:
            m2 = load_any(os.path.join(mdir, "mass2.json"))
            arts, rfc = lead_events_mass2(m2, m2ev)
            pv = monthly_pageviews_mass2(m2)
            source = "mass2"
        else:
            print("--mass2: data/mass2_events.json.gz not found; using ratchet+pilot", file=sys.stderr)
    if source != "mass2":
        arts = lead_events_current(ratchet, pilot)
        pv = monthly_pageviews_current(pilot)
    terms, ins_log = term_series(arts, n)
    S = {**deep, **terms}
    # edits of the lead-panel topic articles (denominator for insertions per edit)
    lp_edits = np.zeros(n); lp_n = 0
    for t, a in arts.items():
        if a["group"] == "topic" and t in per_title:
            lp_edits += per_title[t]; lp_n += 1
    S["lead_panel_edits"] = lp_edits
    if rfc:
        S["rfc_starts"] = np.zeros(n)
        for t0 in rfc.get("topic", []):
            i = wk(t0)
            if 0 <= i < n:
                S["rfc_starts"][i] += 1
    last_full = n - 1                                   # last (partial) week excluded
    lo, hi = -PRE[0], last_full - POST[1]               # valid event weeks
    outcomes = ["topic_edits", "topic_edits_capped", "topic_active", "comparison_active", "comparison_edits", "shocked_edits", "lead_panel_edits", "term_ins", "term_ins_durable",
                "term_ins_cmp"] + (["rfc_starts"] if "rfc_starts" in S else [])
    C = {k: smooth_c(S[k], lo, hi) for k in outcomes}

    # insertions per 100 edits: ratio of excesses (edits and insertions on the same lead panel)
    def ipe(i):
        a = excess_at(S["term_ins"], i, C["term_ins"]); b = excess_at(S["lead_panel_edits"], i, C["lead_panel_edits"])
        return None if a is None or b is None else a / b

    rng = np.random.default_rng(SEED)
    plc_weeks = rng.integers(lo, hi + 1, N_PLACEBO)
    allx = {k: np.array([excess_at(S[k], i, C[k]) for i in range(n)], dtype=object) for k in outcomes}
    allx["ins_per_edit"] = np.array([ipe(i) for i in range(n)], dtype=object)
    outs = outcomes + ["ins_per_edit"]
    plc = {k: np.array([float(allx[k][i]) for i in plc_weeks]) for k in outs}

    # pageviews (monthly)
    pv_out = {}
    for g in ("topic", "comparison"):
        pv_out[g] = {k: v for k, v in pv.get(g, {}).items()}
    months = sorted(pv_out["topic"])
    pv_first = date(int(months[6][:4]), int(months[6][4:]), 1) if len(months) > 8 else None
    pv_last = date(int(months[-2][:4]), int(months[-2][4:]), 1) if months else None
    plc_days = [WEEK0 + timedelta(days=int(7 * w + rng.integers(0, 7))) for w in plc_weeks]
    plc_pv = np.array([x for x in (pv_excess(pv_out["topic"], d) for d in plc_days) if x is not None])

    ev = []
    for e in cal:
        d = date.fromisoformat(e["date"]); i = wk(d)
        if not (lo <= i <= hi):
            continue
        row = {**e, "week": i, "week_start": wk_date(i)}
        for k in outs:
            x = allx[k][i]
            row[k] = None if x is None else round(float(x), 3)
            row["p_" + k] = None if x is None else round(float(np.mean(plc[k] >= float(x))), 4)
            # local placebo: weeks within +-26 of the event
            loc = [float(allx[k][j]) for j in range(max(lo, i - 26), min(hi, i + 26) + 1) if abs(j - i) > 3 and allx[k][j] is not None]
            row["plocal_" + k] = None if x is None or not loc else round(float(np.mean(np.array(loc) >= float(x))), 4)
            row["detr_" + k] = None if x is None or not loc else round(float(x) / float(np.median(loc)), 3)
        px = pv_excess(pv_out["topic"], d) if pv_first and pv_first <= d <= pv_last else None
        row["pageviews"] = None if px is None else round(px, 3)
        row["p_pageviews"] = None if px is None else round(float(np.mean(plc_pv >= px)), 4)
        pxc = pv_excess(pv_out["comparison"], d) if pv_first and pv_first <= d <= pv_last else None
        row["pageviews_cmp"] = None if pxc is None else round(pxc, 3)
        row["raw"] = {k: {"pre": round(float(S[k][i - 6:i].mean()), 2), "post": round(float(S[k][i:i + 3].mean()), 2)}
                      for k in ("topic_edits", "comparison_edits", "term_ins", "term_ins_durable")}
        ev.append(row)

    # overlap sets
    def drop_overlap(rows, strict=False):
        keep = []
        for r in rows:
            d = date.fromisoformat(r["date"])
            bad = False
            for o in rows:
                if o is r:
                    continue
                dd = abs((date.fromisoformat(o["date"]) - d).days)
                if dd > 21:
                    continue
                if strict or o["tier"] > r["tier"] or (o["tier"] == r["tier"] and o["date"] < r["date"]):
                    bad = True; break
            if not bad:
                keep.append(r)
        return keep

    sets = {"all": ev, "no_stronger_within_3w": drop_overlap(ev), "isolated_3w": drop_overlap(ev, strict=True)}
    pv_plc_log = np.log(plc_pv)

    def type_table(rows):
        tab = {}
        for ty in TYPES:
            rs = [r for r in rows if r["type"] == ty]
            cell = {"n": len(rs)}
            for k in outs + ["pageviews"]:
                xs = [r[k] for r in rs if r.get(k) is not None]
                if not xs:
                    cell[k] = None; continue
                lx = np.log(np.array(xs, dtype=float))
                pl = pv_plc_log if k == "pageviews" else np.log(plc[k])
                draws = np.array([rng.choice(pl, len(xs), replace=False).mean() for _ in range(N_PLACEBO)])
                cell[k] = {"geo_mean_excess": round(float(np.exp(lx.mean())), 3),
                           "share_above_placebo_median": round(float(np.mean(lx > np.median(pl))), 2),
                           "p": round(float(np.mean(draws >= lx.mean())), 4), "n": len(xs)}
            tab[ty] = cell
        return tab

    tables = {k: type_table(v) for k, v in sets.items()}

    def local_table(rows):
        """Excess relative to the median excess of weeks within +-26 of the event (removes the 2023-24 rise and decay);
        p from a sign-flip test on the log ratios (one-sided, > 1)."""
        tab = {}
        for ty in TYPES:
            rs = [r for r in rows if r["type"] == ty]
            cell = {"n": len(rs)}
            for k in outs:
                xs = np.log(np.array([r["detr_" + k] for r in rs if r.get("detr_" + k)], dtype=float))
                if len(xs) < 2:
                    cell[k] = None; continue
                flips = np.array([(xs * rng.choice([-1, 1], len(xs))).mean() for _ in range(N_PLACEBO)])
                cell[k] = {"geo_mean_vs_local": round(float(np.exp(xs.mean())), 3), "p": round(float(np.mean(flips >= xs.mean())), 4),
                           "share_above_local": round(float(np.mean(xs > 0)), 2), "n": len(xs)}
            tab[ty] = cell
        return tab
    local_tables = {k: local_table(v) for k, v in sets.items()}
    # direct contrast: legal vs military on log(insertions per edit) and log(edits)
    def contrast(rows, k):
        a = [math.log(r[k]) for r in rows if r["type"] == "legal_institutional" and r.get(k)]
        b = [math.log(r[k]) for r in rows if r["type"] == "military_escalation" and r.get(k)]
        if len(a) < 2 or len(b) < 2:
            return None
        obs = np.mean(a) - np.mean(b); pool = np.array(a + b)
        perm = []
        for _ in range(N_PLACEBO):
            rng.shuffle(pool); perm.append(pool[:len(a)].mean() - pool[len(a):].mean())
        return {"legal_minus_military_log": round(float(obs), 3), "ratio": round(float(math.exp(obs)), 3),
                "p_two_sided": round(float(np.mean(np.abs(perm) >= abs(obs))), 4), "n_legal": len(a), "n_military": len(b)}
    contrasts = {s: {k: contrast(v, k) for k in ("topic_edits", "topic_edits_capped", "topic_active", "term_ins", "term_ins_durable", "ins_per_edit")}
                 for s, v in sets.items()}

    # slow-response sensitivity: weeks +0..+12 vs -13..-1 (does vocabulary follow legal events with a delay?)
    LPRE, LPOST = (-13, -1), (0, 12)
    llo, lhi = -LPRE[0], last_full - LPOST[1]
    lplc_weeks = rng.integers(llo, lhi + 1, N_PLACEBO)
    long_keys = ["topic_edits", "topic_active", "comparison_edits", "shocked_edits", "term_ins", "term_ins_durable", "term_ins_cmp"]
    lx_all = {k: [excess_at(S[k], i, C[k], LPRE, LPOST) for i in range(n)] for k in long_keys}
    lplc = {k: np.log(np.array([lx_all[k][i] for i in lplc_weeks], dtype=float)) for k in long_keys}
    long_tab = {}
    for ty in TYPES:
        rs = [r for r in ev if r["type"] == ty and llo <= r["week"] <= lhi]
        cell = {"n": len(rs)}
        for k in long_keys:
            xs = np.log(np.array([lx_all[k][r["week"]] for r in rs], dtype=float))
            if not len(xs):
                cell[k] = None; continue
            draws = np.array([rng.choice(lplc[k], len(xs), replace=False).mean() for _ in range(N_PLACEBO)])
            cell[k] = {"geo_mean_excess": round(float(np.exp(xs.mean())), 3), "p": round(float(np.mean(draws >= xs.mean())), 4), "n": len(xs)}
        long_tab[ty] = cell
    for r in ev:
        r["long_term_ins_durable"] = None if not (llo <= r["week"] <= lhi) else round(float(lx_all["term_ins_durable"][r["week"]]), 3)
        r["long_topic_edits"] = None if not (llo <= r["week"] <= lhi) else round(float(lx_all["topic_edits"][r["week"]]), 3)

    # monthly cross-correlation (slow lags): monthly topic edits vs monthly durable insertions, 0..9 months
    mon = defaultdict(lambda: np.zeros(4))
    for i in range(last_full):
        m = wk_date(i)[:7]
        mon[m] += [S["topic_edits"][i], S["term_ins"][i], S["term_ins_durable"][i], S["comparison_edits"][i]]
    mk = sorted(mon); M = np.array([mon[m] for m in mk])
    def mx(a, b, L):
        return round(float(np.corrcoef(a[:len(a) - L] if L else a, b[L:])[0, 1]), 3)
    monthly_lag = {"note": "corr(monthly topic edits_m, monthly insertions_{m+L}), L in months; raw levels (trending), so read the shape only",
                   "months": len(mk), "ins": {L: mx(M[:, 0], M[:, 1], L) for L in range(0, 10)},
                   "durable": {L: mx(M[:, 0], M[:, 2], L) for L in range(0, 10)}}

    # lag analysis
    def xcorr(a, b, lags=range(-8, 9)):
        out = {}
        for L in lags:            # corr(a_t, b_{t+L}); positive L = b follows a
            if L >= 0:
                x, y = a[:len(a) - L], b[L:]
            else:
                x, y = a[-L:], b[:len(b) + L]
            out[L] = round(float(np.corrcoef(x, y)[0, 1]), 3)
        return out
    rng_w = slice(0, last_full)
    e_t, i_t = S["topic_edits"][rng_w], S["term_ins"][rng_w]
    lag = {"note": "corr(topic_edits_t, term_ins_{t+L}); positive L = insertions follow edits by L weeks",
           "n_weeks": int(last_full), "band95": round(2 / math.sqrt(last_full), 3),
           "raw": xcorr(e_t, i_t),
           "diff_log": xcorr(np.diff(np.log1p(e_t)), np.diff(np.log1p(i_t))),
           "raw_post_oct2023": xcorr(e_t[wk("2023-10-02"):], i_t[wk("2023-10-02"):]),
           "comparison_raw": xcorr(S["comparison_edits"][rng_w], S["term_ins_cmp"][rng_w]),
           "durable_raw": xcorr(e_t, S["term_ins_durable"][rng_w])}
    # peak weeks of each series (to place the 2024-H1 wave)
    def top_weeks(x, k=8):
        idx = np.argsort(-x[:last_full])[:k]
        return [{"week_start": wk_date(int(i)), "value": float(x[i])} for i in sorted(idx)]
    peaks = {k: top_weeks(S[k]) for k in ("topic_edits", "term_ins", "term_ins_durable", "comparison_edits")}

    # half-year totals and share of insertions in event windows
    in_win = np.zeros(n, bool)
    for r in ev:
        if r["type"] != "comparison":
            in_win[r["week"]: r["week"] + 3] = True
    win_share = {"weeks_share": round(float(in_win[lo:last_full].mean()), 3),
                 "term_ins_share": round(float(S["term_ins"][lo:last_full][in_win[lo:last_full]].sum() / max(1, S["term_ins"][lo:last_full].sum())), 3),
                 "durable_share": round(float(S["term_ins_durable"][lo:last_full][in_win[lo:last_full]].sum() / max(1, S["term_ins_durable"][lo:last_full].sum())), 3),
                 "topic_edits_share": round(float(S["topic_edits"][lo:last_full][in_win[lo:last_full]].sum() / S["topic_edits"][lo:last_full].sum()), 3)}

    # which events left a mark
    def examples(r):
        w0, w1 = r["week"], r["week"] + 3
        t0 = datetime.combine(date.fromisoformat(wk_date(w0)), datetime.min.time(), tzinfo=timezone.utc).timestamp()
        t1 = t0 + 21 * 86400
        ins = [x for x in ins_log if t0 <= x["t"] < t1]
        by_art = Counter((x["title"], x["term"]) for x in ins)
        dur = Counter((x["title"], x["term"]) for x in ins if x["durable"])
        quotes = []
        for title, edits in bisect.items():
            for b in edits:
                bt = ts_epoch(b["timestamp"])
                if t0 <= bt < t1 and title in arts and arts[title]["group"] == "topic":
                    if crit_hit(b.get("after")) != crit_hit(b.get("before")) or crit_hit(b.get("after")):
                        quotes.append({"title": title, "ts": b["timestamp"][:10], "reverted": b.get("reverted"),
                                       "before": (b.get("before") or "")[:300], "after": (b.get("after") or "")[:300],
                                       "comment": (b.get("comment") or "")[:160]})
        fsv = []
        for title, a in ratchet["articles"].items():
            if title not in arts or arts[title]["group"] != "topic":
                continue
            for v in a.get("fs_variants", []):
                ft = ts_epoch(v["first_seen"])
                if t0 <= ft < t1 and crit_hit(v["s"]) and v.get("live_days", 0) >= 7:
                    fsv.append({"title": title, "first_seen": v["first_seen"][:10], "live_days": round(v["live_days"], 1), "s": v["s"][:300]})
        return {"insertions": [{"title": t, "term": k, "n": c, "durable": dur.get((t, k), 0)} for (t, k), c in by_art.most_common(10)],
                "first_sentence_edits": quotes[:6], "first_sentence_variants_live_7d": sorted(fsv, key=lambda x: -x["live_days"])[:4]}

    topic_ev = [r for r in ev if r.get("term_ins_durable") is not None]
    rank, used = [], set()
    for r in sorted(topic_ev, key=lambda r: (-(r["term_ins_durable"]), -r["tier"])):
        if r["week"] in used:
            continue                       # same week => identical window: report once, list the co-events
        used.add(r["week"])
        r = dict(r, co_events=[o["event"] for o in ev if o["week"] == r["week"] and o is not r])
        rank.append(r)
        if len(rank) == 12:
            break
    marks = [{"date": r["date"], "event": r["event"], "co_events_same_week": r["co_events"], "type": r["type"], "tier": r["tier"],
              "excess_term_ins_durable": r["term_ins_durable"], "p": r["p_term_ins_durable"], "plocal": r["plocal_term_ins_durable"],
              "excess_term_ins": r["term_ins"], "excess_topic_edits": r["topic_edits"], "raw": r["raw"], **examples(r)} for r in rank]

    out = {"source": source, "n_events_in_window": len(ev), "n_events_calendar": len(cal), "panel": ncount,
           "lead_panel": {"topic": sum(a["group"] == "topic" for a in arts.values()),
                          "comparison": sum(a["group"] != "topic" for a in arts.values()), "topic_in_deep": lp_n,
                          "topic_insertions": int(S["term_ins"].sum()), "topic_durable": int(S["term_ins_durable"].sum()),
                          "comparison_insertions": int(S["term_ins_cmp"].sum())},
           "rfc_available": "rfc_starts" in S,
           "smoothing": {k: round(v, 3) for k, v in C.items()},
           "placebo": {k: {"median": round(float(np.median(plc[k])), 3), "p90": round(float(np.percentile(plc[k], 90)), 3)} for k in outs}
                      | {"pageviews": {"median": round(float(np.median(plc_pv)), 3), "p90": round(float(np.percentile(plc_pv, 90)), 3)}},
           "events": ev, "type_tables": tables, "type_tables_local": local_tables, "legal_vs_military": contrasts, "lag": lag, "peaks": peaks,
           "event_window_share": win_share, "left_a_mark": marks, "long_window_type_table": long_tab,
           "monthly_lag": monthly_lag,
           "half_years": half_years(S, last_full)}
    json.dump(out, open(os.path.join(DATA, "event_timing.json" if source != "mass2" else "event_timing_mass2.json"), "w"), indent=1)

    # chart data: weekly timeline with event markers
    os.makedirs(CHART, exist_ok=True)
    pre = "mass2_" if source == "mass2" else ""          # mass v2 runs never overwrite the published chart files
    tl = {"source": f"deep panel weekly edits (results.json, articles existing before 2021: topic n={ncount.get('topic')}, "
                    f"clean comparison n={ncount.get('comparison')}); critical-term insertions into leads ({source}: "
                    f"{out['lead_panel']['topic']} topic and {out['lead_panel']['comparison']} comparison leads)",
          "week_start": [wk_date(i) for i in range(last_full)],
          "topic_edits": S["topic_edits"][:last_full].astype(int).tolist(),
          "comparison_edits": S["comparison_edits"][:last_full].astype(int).tolist(),
          "topic_articles_edited": S["topic_active"][:last_full].astype(int).tolist(),
          "comparison_articles_edited": S["comparison_active"][:last_full].astype(int).tolist(),
          "topic_edits_capped10": S["topic_edits_capped"][:last_full].astype(int).tolist(),
          "shocked_comparison_edits": S["shocked_edits"][:last_full].astype(int).tolist(),
          "topic_term_insertions": S["term_ins"][:last_full].astype(int).tolist(),
          "topic_term_insertions_durable7d": S["term_ins_durable"][:last_full].astype(int).tolist(),
          "comparison_term_insertions": S["term_ins_cmp"][:last_full].astype(int).tolist(),
          "events": [{"date": e["date"], "week_start": wk_date(wk(e["date"])), "label": e["event"], "type": e["type"], "tier": e["tier"]} for e in cal]}
    json.dump(tl, open(os.path.join(CHART, pre + "01_weekly_timeline_events.json"), "w"))
    tt = {"local_note": "tables_local: excess divided by the median excess of weeks within +-26 of the event; sign-flip p",
          "tables_local": local_tables,
          "note": "geometric-mean excess (weeks +0..+2 over -6..-1) by event type; p = share of 2,000 random same-size sets of placebo dates with an equal or larger mean log-excess",
          "outcomes": outs + ["pageviews"], "tables": tables}
    json.dump(tt, open(os.path.join(CHART, pre + "02_type_by_outcome.json"), "w"), indent=1)
    json.dump({"note": lag["note"], "band95": lag["band95"], "lags": list(range(-8, 9)),
               "raw": [lag["raw"][L] for L in range(-8, 9)], "diff_log": [lag["diff_log"][L] for L in range(-8, 9)],
               "comparison_raw": [lag["comparison_raw"][L] for L in range(-8, 9)]},
              open(os.path.join(CHART, pre + "03_lag_xcorr.json"), "w"), indent=1)
    json.dump({"note": "events ranked by excess durable critical-term insertions into topic leads (weeks +0..+2 vs -6..-1)",
               "rows": [{k: m[k] for k in ("date", "event", "type", "excess_term_ins_durable", "p", "plocal", "excess_topic_edits")}
                        | {"durable_post_per_week": m["raw"]["term_ins_durable"]["post"], "durable_pre_per_week": m["raw"]["term_ins_durable"]["pre"]}
                        for m in marks]}, open(os.path.join(CHART, pre + "04_left_a_mark.json"), "w"), indent=1)
    json.dump({"note": "per-event excess for scatter: x = excess topic edits, y = excess durable term insertions, colour = type",
               "rows": [{k: r.get(k) for k in ("date", "event", "type", "tier", "topic_edits", "term_ins", "term_ins_durable",
                                                "ins_per_edit", "topic_edits_capped", "topic_active", "comparison_edits", "shocked_edits", "pageviews", "p_topic_edits", "p_topic_active", "p_term_ins_durable")}
                        for r in ev]}, open(os.path.join(CHART, pre + "05_event_scatter.json"), "w"), indent=1)
    report(out)
    return out


def half_years(S, last_full):
    h = defaultdict(lambda: Counter())
    for i in range(last_full):
        d = wk_date(i); k = d[:4] + ("-H1" if int(d[5:7]) <= 6 else "-H2")
        for f in ("topic_edits", "term_ins", "term_ins_durable", "term_rem", "term_ins_cmp", "comparison_edits"):
            h[k][f] += float(S[f][i])
    out = {}
    for k in sorted(h):
        c = h[k]
        out[k] = {f: int(v) for f, v in c.items()} | {"durable_share": round(c["term_ins_durable"] / c["term_ins"], 3) if c["term_ins"] else None,
                                                       "ins_per_1000_edits": round(1000 * c["term_ins"] / c["topic_edits"], 2)}
    return out


CRIT_RX = None


def crit_hit(s):
    global CRIT_RX
    if CRIT_RX is None:
        sys.path.insert(0, HERE)
        import analyze as A
        CRIT_RX = A
    if not s:
        return False
    return any(CRIT_RX.count(k, s) > 0 for k in CRITICAL)


def report(o):
    print(f"source={o['source']} events in window={o['n_events_in_window']}/{o['n_events_calendar']} panel={o['panel']} lead={o['lead_panel']}")
    print("placebo medians:", {k: v['median'] for k, v in o['placebo'].items()})
    for s, tab in o["type_tables"].items():
        print(f"\n== type x outcome ({s}) geo-mean excess [p]")
        ks = ["topic_edits", "topic_edits_capped", "topic_active", "comparison_active", "shocked_edits", "term_ins", "term_ins_durable", "ins_per_edit", "pageviews"]
        print("type".ljust(22) + "n  " + "".join(k[:14].ljust(17) for k in ks))
        for ty, c in tab.items():
            print(ty.ljust(22) + str(c["n"]).ljust(3) + "".join(
                (f"{c[k]['geo_mean_excess']:.2f} [{c[k]['p']:.3f}]" if c.get(k) else "-").ljust(17) for k in ks))
    for s_, tab in o["type_tables_local"].items():
        print(f"\n== LOCAL (vs +-26w median) ({s_}) geo-mean [p]")
        ks = ["topic_edits", "topic_edits_capped", "topic_active", "comparison_active", "shocked_edits", "term_ins", "term_ins_durable", "ins_per_edit"]
        for ty, c in tab.items():
            print(ty.ljust(22) + str(c["n"]).ljust(3) + "".join(
                (f"{c[k]['geo_mean_vs_local']:.2f} [{c[k]['p']:.3f}]" if c.get(k) else "-").ljust(17) for k in ks))
    print("\nlegal vs military:", json.dumps(o["legal_vs_military"], indent=0))
    print("\nlag raw:", o["lag"]["raw"]); print("lag diff_log:", o["lag"]["diff_log"]); print("band", o["lag"]["band95"])
    print("window share:", o["event_window_share"])
    print("\n== long window (+0..+12 vs -13..-1)")
    for ty, c in o["long_window_type_table"].items():
        print(ty.ljust(22) + str(c["n"]).ljust(3) + "".join((f"{k[:10]} {c[k]['geo_mean_excess']:.2f} [{c[k]['p']:.3f}]  " if c.get(k) else "-") for k in c if k != "n"))
    print("monthly lag:", o["monthly_lag"])
    for k, v in o["half_years"].items():
        print(k, v)
    print("\nleft a mark:")
    for m in o["left_a_mark"]:
        print(f"  {m['date']} {m['type'][:10]:10s} x{m['excess_term_ins_durable']:.2f} p={m['p']} pl={m['plocal']} edits x{m['excess_topic_edits']} {m['event'][:60]}  {m['raw']['term_ins_durable']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mass2", action="store_true", help="use data/mass2_events.json.gz lead events (and RfC dates) if present")
    ap.add_argument("--mass2-dir", default=None, help="directory holding mass2*.json(.gz) (default: data/)")
    run(ap.parse_args())
