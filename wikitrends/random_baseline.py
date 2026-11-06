"""Random-Wikipedia baseline: are the topic's lead changes just site-wide drift?

  python random_baseline.py sample                    -> data/random/frame.json        (list=random draws, deduped,
                                                                                         disambiguation pages excluded)
  python random_baseline.py shard --shard I --of N    -> data/random/rand_I.json.gz    (checkpointed via mass._run;
                                                                                         exits non-zero if >5% of rows error)
  python random_baseline.py merge                     -> data/random_baseline.json, data/random_leads.json.gz
                                                         (exits non-zero if <95% of the frame arrived; files written first)
  python random_baseline.py analyze                   -> patterns/sampling/random_baseline.md
  MASS_LIMIT=40 ...                                   -> test mode (first 40 rows of the shard)
  WT_RANDOM_N (default 3500)                          -> eligible titles to draw

Sampling. list=random (rnnamespace=0, rnfilterredir=nonredirects, rnlimit=500) is repeated until WT_RANDOM_N distinct
eligible titles are drawn. The API is not seedable, so the drawn list *is* the frame: every row records its page id, draw
round, position and UTC draw time. Disambiguation pages (pageprops `disambiguation`, batched by 50 page ids) and anything
`info` still flags as a redirect are dropped. The fixed seed (SEED) is used where randomness is ours: the bootstrap CIs.
Existence in 2021 is decided per row in the shard (the 2021-01-01 lead fetch, plus one creation-date request when that
lead is missing), so `existed_2021` / `created_later` flags are kept instead of dropping rows.

Per row (shard): the mass_narr features (critical counts, event-filter residuals, lead prose) at mass.DATES
(2021-01-01, 2023-07-01, now; "now" fixed by the frame so shards agree), group "random", project None
(mass_narr.groups_for returns no narrative groups for it), plus pageviews (one call via mass2.pageviews, last 12 complete
months kept). Lead fetches are strict: a failed request is an error, never "no lead".

Measures (same for random, mass_narr topic/comparison and mass2 topic/comparison): on articles with all three leads of
>= 20 words, per window (pre-war 2021-01 -> 2023-07, post-war 2023-07 -> now): share gaining critical lead terms (count
up), mean change in critical hits per 10k lead words, and the event-filter split of that change (narrative residual vs
event sentences, sentence level, hits per 10k words of all lead text, so unfiltered = residual + event).
"""
import argparse, glob, gzip, json, os, sys, time
from collections import Counter

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wt_net                   # noqa: E402
import analyze as A             # noqa: E402
import mass as M                # noqa: E402
import mass_narr as MN          # noqa: E402

API = "https://en.wikipedia.org/w/api.php"
DATA = A.DATA
RDIR = os.path.join(DATA, "random")
OUT_MD = os.path.join(HERE, "patterns", "sampling", "random_baseline.md")
KIND = "rand"
SEED = 20261106
TARGET = int(os.environ.get("WT_RANDOM_N", "3500"))
MAX_ROUNDS = 40
MIN_WORDS = 20
NB = int(os.environ.get("WT_BOOT", "2000"))
CRIT = list(A.CRITICAL)
WINDOWS = (("pre", 0, 1), ("post", 1, 2))
D2021 = M.DATES[0]


def _now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _api(params):
    j = wt_net.get_json(API, {**params, "format": "json", "formatversion": 2})
    if not isinstance(j, dict) or "error" in j or "query" not in j:
        raise RuntimeError(f"API request failed: {params.get('list') or params.get('prop')} -> {str(j)[:200]}")
    return j


# ================================================================== 1. sample
def draw_round():
    j = _api({"action": "query", "list": "random", "rnnamespace": 0, "rnfilterredir": "nonredirects", "rnlimit": 500})
    return j["query"].get("random") or [], _now()


def page_flags(ids):
    """{pageid: {"disambiguation": bool, "redirect": bool, "missing": bool}} for up to 50 ids per request."""
    out = {}
    for k in range(0, len(ids), 50):
        part = ids[k:k + 50]
        j = _api({"action": "query", "prop": "pageprops|info", "ppprop": "disambiguation", "pageids": "|".join(map(str, part))})
        for p in j["query"].get("pages") or []:
            out[p.get("pageid")] = {"disambiguation": "disambiguation" in (p.get("pageprops") or {}),
                                    "redirect": bool(p.get("redirect")), "missing": bool(p.get("missing")) or p.get("ns", 0) != 0}
    return out


def sample(target=TARGET, path=None):
    path = path or os.path.join(RDIR, "frame.json")
    rows, seen, excl = [], set(), Counter()
    excluded = {"disambiguation": [], "redirect": [], "missing": []}
    rounds = 0
    while len(rows) < target and rounds < MAX_ROUNDS:
        rounds += 1
        got, at = draw_round()
        fresh = []
        for pos, r in enumerate(got):
            if r.get("ns", 0) != 0:
                excl["namespace"] += 1; continue
            if r["id"] in seen:
                excl["duplicate"] += 1; continue
            seen.add(r["id"]); fresh.append((pos, r))
        fl = page_flags([r["id"] for _, r in fresh])
        for pos, r in fresh:
            f = fl.get(r["id"], {"missing": True})
            why = "missing" if f.get("missing") else "disambiguation" if f.get("disambiguation") else "redirect" if f.get("redirect") else None
            if why:
                excl[why] += 1; excluded[why].append(r["title"]); continue
            rows.append({"title": r["title"], "pageid": r["id"], "group": "random", "project": None, "importance": None,
                         "draw_round": rounds, "draw_pos": pos, "drawn_at": at})
        wt_net.heartbeat("sample", len(rows), target, rounds=rounds)
    if len(rows) < target:
        sys.exit(f"sample: only {len(rows)} eligible titles after {rounds} rounds (target {target})")
    drawn = len(rows) + sum(excl[k] for k in ("disambiguation", "redirect", "missing"))
    rows = rows[:target]                                   # draw order is the API's randomness; truncation is deterministic
    fr = {"generated": _now(), "now": time.strftime("%Y-%m-%dT00:00:00Z"), "dates": [M.DATES[0], M.DATES[1]],
          "seed": SEED, "seed_note": "list=random is not seedable: this drawn list is the frame; the seed fixes the bootstrap",
          "params": {"list": "random", "rnnamespace": 0, "rnfilterredir": "nonredirects", "rnlimit": 500, "target": target},
          "rounds": rounds, "distinct_drawn": drawn, "excluded_counts": dict(excl), "excluded": excluded, "rows": rows}
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"; json.dump(fr, open(tmp, "w")); os.replace(tmp, path)
    print(f"sample: {len(rows)} rows in {rounds} rounds; excluded {dict(excl)}", flush=True)
    return fr


# ================================================================== 2. shard
def created_at(title):
    """(first-revision timestamp or None, page missing now?)."""
    j = _api({"action": "query", "prop": "revisions", "titles": title, "rvlimit": 1, "rvdir": "newer", "rvprop": "timestamp"})
    p = (j["query"].get("pages") or [{}])[0]
    if p.get("missing"):
        return None, True
    revs = p.get("revisions") or []
    return (revs[0].get("timestamp") if revs else None), False


def last12(monthly, now):
    """The 12 complete months before `now` (YYYYMM labels)."""
    y, m = int(now[:4]), int(now[5:7])
    out = []
    for _ in range(12):
        y, m = (y, m - 1) if m > 1 else (y - 1, 12)
        out.append(f"{y}{m:02d}")
    return sorted(out)


def views(title, now):
    import mass2 as M2                       # reuse the mass2 helper (one call: 2021-01 .. last complete month)
    pv = M2.pageviews([title])
    mon = pv.get("monthly")
    if not mon:
        return {"monthly": None, "views_12m": None}
    keep = last12(mon, now)
    return {"monthly": {k: mon[k] for k in keep if k in mon}, "views_12m": sum(mon.get(k, 0) for k in keep)}


def collect(row, now=None):
    now = now or M.DATES[-1]
    out = MN.features(row, fetch=lambda t, d: MN.lead_at(t, d, strict=True))
    out["created"], out["deleted"] = None, False
    if out["snaps"][0] is not None:
        out["existed_2021"] = True
    else:                                    # no 2021 lead: created later, a redirect then, or gone now
        out["created"], out["deleted"] = created_at(row["title"])
        out["existed_2021"] = bool(out["created"] and out["created"] <= D2021)
    out["created_later"] = not out["existed_2021"] and not out["deleted"]
    out["pageviews"] = views(row["title"], now)
    return out


def load_frame(path=None):
    return json.load(open(path or os.path.join(RDIR, "frame.json")))


def set_now(now):
    M.DATES[-1] = now                        # same list object as mass_narr.DATES
    try:
        import mass2 as M2
        M2.set_now(now)
    except Exception as e:                   # pragma: no cover
        print("warning: mass2.set_now failed:", e, file=sys.stderr)


def run_shard(i, n):
    fr = load_frame()
    set_now(fr["now"])
    rows = M.shard(fr["rows"], i, n)
    lim = int(os.environ.get("MASS_LIMIT", "0"))
    M._run(KIND, collect, rows[:lim] if lim else rows, i, out_dir=RDIR)


# ================================================================== 3. merge + shared measures
def lm(s):
    """(words, critical hits, residual critical hits) from a mass_narr-style snap (full or mass2-sparse counts)."""
    if not isinstance(s, dict) or not s.get("words"):
        return None
    c = s.get("counts") or {}
    ev = (s.get("ev") or {}).get("sentence") or {}
    rc = ev.get("res_counts") or {}
    return s["words"], sum(c.get(k, 0) or 0 for k in CRIT), sum(rc.get(k, 0) or 0 for k in CRIT)


def panel_rows(snaps_lists):
    """Articles with all three leads of >= MIN_WORDS words -> list of 3 (w, c, r) tuples."""
    out = []
    for sn in snaps_lists:
        if not isinstance(sn, list) or len(sn) < 3:
            continue
        x = [lm(s) for s in sn[:3]]
        if all(v is not None and v[0] >= MIN_WORDS for v in x):
            out.append(x)
    return out


def window_arrays(P, a, b):
    """Per-article arrays for window a -> b."""
    if not P:
        return None
    X = np.array(P, dtype=float)                     # n x 3 x (w, c, r)
    w0, c0, r0 = X[:, a, 0], X[:, a, 1], X[:, a, 2]
    w1, c1, r1 = X[:, b, 0], X[:, b, 1], X[:, b, 2]
    return {"gain": (c1 > c0).astype(float), "lose": (c1 < c0).astype(float), "any0": (c0 > 0).astype(float),
            "chg": (c1 / w1 - c0 / w0) * 1e4, "res": (r1 / w1 - r0 / w0) * 1e4,
            "ev": ((c1 - r1) / w1 - (c0 - r0) / w0) * 1e4, "res_gain": (r1 > r0).astype(float),
            "words_changed": (w1 != w0).astype(float), "c0": c0, "c1": c1, "w0": w0, "w1": w1}


def boot_means(x, rng, B=None):
    B = B or NB
    if len(x) == 0:
        return None
    idx = rng.integers(0, len(x), size=(B, len(x)))
    return x[idx].mean(axis=1)


def _ci(bm):
    return None if bm is None else [round(float(np.percentile(bm, 2.5)), 4), round(float(np.percentile(bm, 97.5)), 4)]


def r4(x):
    return None if x is None or not np.isfinite(x) else round(float(x), 4)


def summarize(P, seed=SEED):
    """Summary of one group's panel: per window share gaining, mean change per 10k, residual split (with bootstrap CIs)."""
    rng = np.random.default_rng(seed)
    out = {"n": len(P)}
    for wn, a, b in WINDOWS:
        d = window_arrays(P, a, b)
        if d is None:
            out[wn] = None; continue
        chg, res = d["chg"].mean(), d["res"].mean()
        out[wn] = {"share_gaining": r4(d["gain"].mean()), "share_gaining_ci": _ci(boot_means(d["gain"], rng)),
                   "share_losing": r4(d["lose"].mean()), "share_with_term_at_start": r4(d["any0"].mean()),
                   "mean_change_per10k": r4(chg), "mean_change_per10k_ci": _ci(boot_means(d["chg"], rng)),
                   "pooled_change_per10k": r4((d["c1"].sum() / d["w1"].sum() - d["c0"].sum() / d["w0"].sum()) * 1e4),
                   "residual_change_per10k": r4(res), "residual_change_per10k_ci": _ci(boot_means(d["res"], rng)),
                   "event_change_per10k": r4(d["ev"].mean()),
                   "residual_share": r4(res / chg) if abs(chg) > 1e-9 else None,
                   "share_gaining_residual": r4(d["res_gain"].mean()),
                   "share_lead_words_changed": r4(d["words_changed"].mean())}
    return out


def merge():
    fr = load_frame()
    rows = [r for f in sorted(glob.glob(os.path.join(RDIR, f"{KIND}_*.json.gz"))) for r in json.load(gzip.open(f, "rt"))]
    byt = {}
    for r in rows:
        byt.setdefault(r["title"], r)
    arts, leads = {}, {}
    for t, r in byt.items():
        sn = r.get("snaps") or []
        arts[t] = {"pageid": r.get("pageid"), "drawn_at": r.get("drawn_at"), "existed_2021": r.get("existed_2021"),
                   "created_later": r.get("created_later"), "created": r.get("created"), "deleted": r.get("deleted"),
                   "views_12m": (r.get("pageviews") or {}).get("views_12m"),
                   "snaps": [None if x is None else {k: x.get(k) for k in ("date", "words", "crit", "counts", "ev")} for x in sn]}
        leads[t] = [None if x is None else x.get("lead_prose") for x in sn]
    P = panel_rows([a["snaps"] for a in arts.values() if a["existed_2021"]])
    fl = Counter()
    for a in arts.values():
        fl["existed_2021"] += bool(a["existed_2021"]); fl["created_later"] += bool(a["created_later"])
        fl["deleted"] += bool(a["deleted"]); fl["lead_2021_missing"] += a["snaps"][0] is None if a["snaps"] else 1
    n_frame = len(fr["rows"])
    summ = {"frame_rows": n_frame, "collected": len(arts), "flags": dict(fl), "panel_min_words": MIN_WORDS,
            "dates": [d[:10] for d in M.DATES[:2]] + [fr["now"][:10]],
            "median_lead_words_2023": r4(float(np.median([p[1][0] for p in P]))) if P else None, **summarize(P)}
    res = {"generated": _now(), "now": fr["now"], "frame": {k: fr.get(k) for k in ("generated", "seed", "rounds", "distinct_drawn",
                                                                                     "excluded_counts", "params")},
           "summary": summ, "articles": arts}
    json.dump(res, open(os.path.join(DATA, "random_baseline.json"), "w"))
    json.dump({"dates": summ["dates"], "leads": leads}, gzip.open(os.path.join(DATA, "random_leads.json.gz"), "wt"))
    post = summ.get("post") or {}
    print(f"random merged: {len(arts)}/{n_frame} rows, panel {summ['n']}; post-war share gaining {post.get('share_gaining')}, "
          f"mean change/10k {post.get('mean_change_per10k')}, residual share {post.get('residual_share')}", flush=True)
    if len(arts) < 0.95 * n_frame:
        sys.exit(f"random merge: only {len(arts)}/{n_frame} frame rows arrived (<95%)")
    return res


# ================================================================== 4. analyze
def _load(path):
    for p in (path, path + ".gz"):
        if os.path.exists(p):
            return json.load(gzip.open(p, "rt") if p.endswith(".gz") else open(p))
    return None


def mass2_snaps(r):
    at = r.get("at") or {}
    sn = []
    for k in ("2021-01-01", "2023-07-01", "now"):
        x = (at.get(k) or {}).get("narr")
        if isinstance(x, dict) and "same_as" in x:
            x = (at.get(x["same_as"]) or {}).get("narr")
            x = None if isinstance(x, dict) and "same_as" in x else x
        sn.append(x if isinstance(x, dict) else None)
    return sn


def group_panels(data_dir=None):
    data_dir = data_dir or DATA
    out = {}
    mn = _load(os.path.join(data_dir, "mass_narr.json"))
    if mn:
        for g in ("topic", "comparison"):
            out[("mass_narr", g)] = panel_rows([a.get("snaps") for a in mn["articles"].values() if a.get("group") == g])
    m2 = _load(os.path.join(data_dir, "mass2.json"))
    if m2:
        for g in ("topic", "comparison"):
            out[("mass2", g)] = panel_rows([mass2_snaps(r) for r in m2["articles"] if r.get("group") == g
                                            and (r.get("stratum") or r.get("group")) != "atrocity"])
    rb = _load(os.path.join(data_dir, "random_baseline.json"))
    if not rb:
        sys.exit(f"analyze: no random_baseline.json in {data_dir} (run merge first)")
    out[("random", "random")] = panel_rows([a["snaps"] for a in rb["articles"].values() if a.get("existed_2021")])
    return out, rb


def diff(P, Q, key, wn, seed=SEED):
    """Mean of `key` in P minus in Q for window wn, with an independent bootstrap CI."""
    a, b = dict((w, (x, y)) for w, x, y in WINDOWS)[wn]
    dp, dq = window_arrays(P, a, b), window_arrays(Q, a, b)
    if dp is None or dq is None:
        return None
    rng = np.random.default_rng(seed)
    bp, bq = boot_means(dp[key], rng), boot_means(dq[key], rng)
    return {"est": r4(dp[key].mean() - dq[key].mean()), "ci": _ci(bp - bq)}


def excess(P, Q, key, seed=SEED):
    """(post - pre) in P minus (post - pre) in Q: the post-war acceleration beyond the random baseline's."""
    dp = {w: window_arrays(P, a, b) for w, a, b in WINDOWS}
    dq = {w: window_arrays(Q, a, b) for w, a, b in WINDOWS}
    if any(v is None for v in list(dp.values()) + list(dq.values())):
        return None
    xp, xq = dp["post"][key] - dp["pre"][key], dq["post"][key] - dq["pre"][key]
    rng = np.random.default_rng(seed)
    return {"est": r4(xp.mean() - xq.mean()), "ci": _ci(boot_means(xp, rng) - boot_means(xq, rng))}


def _f(x, k=2, pct=False, sign=False):
    if x is None:
        return "n/a"
    v = x * 100 if pct else x
    s = f"{v:+.{k}f}" if sign else f"{v:.{k}f}"
    return s + ("%" if pct and not sign else " pp" if pct else "")


def _d(d, k=2, pct=False):
    if not d or d.get("est") is None or not d.get("ci"):
        return "n/a"
    lo, hi = d["ci"]
    m = 100 if pct else 1
    u = " pp" if pct else ""
    return f"{d['est'] * m:+.{k}f}{u} [{lo * m:+.{k}f}, {hi * m:+.{k}f}]"


def excludes0(d):
    return bool(d and d.get("ci") and (d["ci"][0] > 0 or d["ci"][1] < 0))


def conf(ds):
    k = sum(excludes0(d) for d in ds if d)
    n = sum(1 for d in ds if d)
    return "STRONG" if n and k == n else "SUGGESTIVE" if k else "NOT DISTINGUISHABLE"


def card(n, title, cf, what, chart, so_what, caveat):
    return (f"## {n}. {title}  [{cf}]\n\n**What we see:** {what}\n\n**Chart:** {chart}\n\n**So what:** {so_what}\n\n"
            f"**Caveat:** {caveat}\n")


def analyze(data_dir=None, out_md=None):
    data_dir, out_md = data_dir or DATA, out_md or OUT_MD
    pan, rb = group_panels(data_dir)
    R = pan[("random", "random")]
    S = {k: summarize(v) for k, v in pan.items()}
    rs = S[("random", "random")]
    srcs = [s for s in ("mass_narr", "mass2") if (s, "topic") in pan]
    if not srcs:
        sys.exit("analyze: neither mass_narr.json nor mass2.json(.gz) found")
    g = lambda s, grp, wn, k: ((S.get((s, grp)) or {}).get(wn) or {}).get(k)
    D = {(s, grp, key, wn): diff(pan[(s, grp)], R, key, wn) for s in srcs for grp in ("topic", "comparison")
         for key in ("chg", "gain", "res") for wn in ("pre", "post")}
    X = {(s, grp, key): excess(pan[(s, grp)], R, key) for s in srcs for grp in ("topic", "comparison") for key in ("chg", "gain")}
    fl = rb["summary"].get("flags") or {}
    fm = rb.get("frame") or {}
    cards = []

    # 1. the frame
    med = lambda P: float(np.median([p[1][0] for p in P])) if P else None
    what = (f"{rb['summary']['frame_rows']:,} random main-namespace non-redirect articles drawn in {fm.get('rounds')} rounds of "
            f"list=random (exclusions: {fm.get('excluded_counts')}); {rb['summary']['collected']:,} collected, "
            f"{fl.get('existed_2021', 0):,} existed by 2021-01-01, {fl.get('created_later', 0):,} were created later "
            f"(flagged, kept out of the panel), {fl.get('deleted', 0)} deleted since the draw. Panel (all three leads >= {MIN_WORDS} "
            f"words): {rs['n']:,}. Median lead length in Jul 2023: random {med(R) or 0:.0f} words, "
            + ", ".join(f"{s} topic {med(pan[(s, 'topic')]) or 0:.0f} / comparison {med(pan[(s, 'comparison')]) or 0:.0f}" for s in srcs)
            + f". Share of leads with any critical term in Jul 2023: random {_f(g('random', 'random', 'post', 'share_with_term_at_start'), 1, True)}, "
            + ", ".join(f"{s} topic {_f(g(s, 'topic', 'post', 'share_with_term_at_start'), 1, True)}" for s in srcs) + ".")
    cards.append(card(1, "The random baseline frame", "DESCRIPTIVE", what,
                      "table: frame counts and lead length by group; data: data/random_baseline.json (summary)",
                      "The baseline is a probability sample of English Wikipedia articles, so its drift is the site-wide drift "
                      "a topic effect must exceed.",
                      "list=random is not seedable; the stored frame is the sample. Random pages are mostly far from "
                      "the topic, so critical terms are rare there: the baseline measures site-wide drift (style, bots, policy), "
                      "not drift on comparable contested topics; that is what the comparison group is for."))

    # 2. post-war lead change per 10k words
    ds = [D[(s, "topic", "chg", "post")] for s in srcs]
    what = (f"Mean change in lead critical hits per 10k words, post-war (Jul 2023 -> now): random "
            f"{_d({'est': g('random', 'random', 'post', 'mean_change_per10k'), 'ci': (rs.get('post') or {}).get('mean_change_per10k_ci')})} "
            f"(pre-war {_f(g('random', 'random', 'pre', 'mean_change_per10k'), 2, sign=True)}). "
            + " ".join(f"{s}: topic {_f(g(s, 'topic', 'post', 'mean_change_per10k'), 2, sign=True)}, comparison "
                       f"{_f(g(s, 'comparison', 'post', 'mean_change_per10k'), 2, sign=True)}; topic - random {_d(D[(s, 'topic', 'chg', 'post')])}, "
                       f"comparison - random {_d(D[(s, 'comparison', 'chg', 'post')])}; post-war acceleration (post - pre) beyond random: topic "
                       f"{_d(X[(s, 'topic', 'chg')])}, comparison {_d(X[(s, 'comparison', 'chg')])}." for s in srcs))
    cards.append(card(2, "Post-war lead change against the random baseline", conf(ds), what,
                      "bars: mean change per 10k lead words by group and window; x: window; y: change in hits per 10k; series: "
                      "topic, comparison, random; data: data/random_baseline.json, data/mass_narr.json, data/mass2.json.gz",
                      "If topic - random excludes zero, the topic's post-war lead change is not explained by site-wide drift.",
                      "Independent bootstrap of articles (seed fixed); the random 'now' is the baseline run's date, a few days or "
                      "weeks after the mass runs', so its post-war window is slightly longer. Per-10k rates of short leads are noisy."))

    # 3. share gaining
    ds = [D[(s, "topic", "gain", "post")] for s in srcs]
    what = (f"Share of leads whose critical-term count rose: random pre-war {_f(g('random', 'random', 'pre', 'share_gaining'), 2, True)}, "
            f"post-war {_f(g('random', 'random', 'post', 'share_gaining'), 2, True)} (losing post-war "
            f"{_f(g('random', 'random', 'post', 'share_losing'), 2, True)}). "
            + " ".join(f"{s}: topic pre {_f(g(s, 'topic', 'pre', 'share_gaining'), 1, True)} / post {_f(g(s, 'topic', 'post', 'share_gaining'), 1, True)}, "
                       f"comparison pre {_f(g(s, 'comparison', 'pre', 'share_gaining'), 1, True)} / post {_f(g(s, 'comparison', 'post', 'share_gaining'), 1, True)}; "
                       f"post-war topic - random {_d(D[(s, 'topic', 'gain', 'post')], 1, True)}, comparison - random "
                       f"{_d(D[(s, 'comparison', 'gain', 'post')], 1, True)}; acceleration beyond random: topic {_d(X[(s, 'topic', 'gain')], 1, True)}." for s in srcs)
            + f" Random leads whose word count changed at all, post-war: {_f(g('random', 'random', 'post', 'share_lead_words_changed'), 1, True)}.")
    cards.append(card(3, "Share of leads gaining critical terms, pre vs post-war", conf(ds), what,
                      "grouped bars: share gaining by window; series: topic, comparison, random; data: as card 2",
                      "Shows whether gains are spread across the site or concentrated on the topic.",
                      "A gain is any rise in the count, however small; random pages start with fewer terms, so they have less "
                      "room to lose and their gains come from a low base."))

    # 4. residual
    ds = [D[(s, "topic", "res", "post")] for s in srcs]
    what = (f"Event filter (sentence level) splits the post-war change into narrative residual and event sentences. Random: residual "
            f"{_f(g('random', 'random', 'post', 'residual_change_per10k'), 2, sign=True)}, event {_f(g('random', 'random', 'post', 'event_change_per10k'), 2, sign=True)}, "
            f"residual share {_f(g('random', 'random', 'post', 'residual_share'), 0, True)}. "
            + " ".join(f"{s}: topic residual {_f(g(s, 'topic', 'post', 'residual_change_per10k'), 2, sign=True)} (share "
                       f"{_f(g(s, 'topic', 'post', 'residual_share'), 0, True)}), comparison residual {_f(g(s, 'comparison', 'post', 'residual_change_per10k'), 2, sign=True)} "
                       f"(share {_f(g(s, 'comparison', 'post', 'residual_share'), 0, True)}); topic - random residual {_d(D[(s, 'topic', 'res', 'post')])}; "
                       f"pre-war topic - random residual {_d(D[(s, 'topic', 'res', 'pre')])}." for s in srcs))
    cards.append(card(4, "The narrative residual against the random baseline", conf(ds), what,
                      "stacked bars (residual + event part) per group, post-war; data: as card 2",
                      "A residual change on topic pages above the random residual is narrative change that neither recent-event "
                      "news nor site-wide drift accounts for.",
                      "Residual share is residual / unfiltered mean change; it is unstable when the unfiltered change is near zero "
                      "(likely for random pages). Hits are per 10k words of all lead text, so unfiltered = residual + event."))

    # 5. verdict
    t_post = [g(s, "topic", "post", "mean_change_per10k") for s in srcs]
    r_post = g("random", "random", "post", "mean_change_per10k")
    ratio = [r4(r_post / t) if t and r_post is not None and abs(t) > 1e-9 else None for t in t_post]
    k = conf([D[(s, "topic", "chg", "post")] for s in srcs] + [D[(s, "topic", "res", "post")] for s in srcs])
    what = (f"Random post-war drift as a share of the topic's post-war change: "
            + ", ".join(f"{s} {_f(r, 0, True)}" for s, r in zip(srcs, ratio))
            + f". Topic - random excludes zero for {sum(excludes0(D[(s, 'topic', 'chg', 'post')]) for s in srcs)}/{len(srcs)} sources "
              f"(unfiltered) and {sum(excludes0(D[(s, 'topic', 'res', 'post')]) for s in srcs)}/{len(srcs)} (residual).")
    cards.append(card(5, "Verdict: is the topic's lead change site-wide drift?", k, what,
                      "none (summary of cards 2-4)",
                      "STRONG here means the topic change exceeds random drift in every source on both the unfiltered and the "
                      "residual measure; NOT DISTINGUISHABLE means drift alone could account for it.",
                      "The comparison group remains the main control; the random baseline only rules site-wide drift in or out."))

    hdr = (f"# Random-Wikipedia baseline: is the topic's lead change site-wide drift?\n\nGenerated by `wikitrends/random_baseline.py "
           f"analyze` on {_now()[:10]}. Random frame drawn {(fm.get('generated') or '')[:10]}, now = {rb.get('now', '')[:10]}. "
           f"Measures as in mass_narr / analyze_mass2 card 12: articles with all three leads (2021-01-01, 2023-07-01, now) of >= "
           f"{MIN_WORDS} words; pre-war = 2021-01 -> 2023-07, post-war = 2023-07 -> now; CIs are 95% article bootstraps "
           f"(B={NB}, seed {SEED}). Panel sizes: " + ", ".join(f"{s}/{g_} {len(v):,}" for (s, g_), v in pan.items()) + ".\n\n")
    os.makedirs(os.path.dirname(out_md), exist_ok=True)
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(hdr + "\n".join(cards))
    print("analyze: wrote", out_md, flush=True)
    return {"summaries": {f"{a}/{b}": v for (a, b), v in S.items()}, "diffs": D, "excess": X}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["sample", "shard", "merge", "analyze"])
    ap.add_argument("--shard", type=int, default=0); ap.add_argument("--of", type=int, default=1)
    a = ap.parse_args()
    if a.cmd == "sample":
        sample()
    elif a.cmd == "shard":
        run_shard(a.shard, a.of)
    elif a.cmd == "merge":
        merge()
    else:
        analyze()
