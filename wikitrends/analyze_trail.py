"""Editor trail: where the most active critical-term editors of the scoped articles also edit, and whether their editing
pattern differs from that of the most active editors of matched comparison articles (aggregates only).

  python analyze_trail.py [--data data/trail/raw.json.gz] [--out patterns/trail]
  python analyze_trail.py --scan patterns/trail          -> publication privacy gate only (analyze_coord.privacy_scan)
  -> patterns/trail/results.json, articles.md (discovery list), cards.md (plain-language pattern cards)

Input: trail.py's raw file, made in ONE workflow job under one in-job salt: the 2021-2026 revision histories of the scoped
topic articles (guard.py scope: curated core + Israel / Palestine Top and High importance) and of the 1:1 matched
comparison articles, with the lead (section 0) critical-term count (analyze.CRITICAL) and connection-term count (CONN, below)
of every revision; the two populations (top TRAIL_N accounts by number of lead edits that change the critical-term count,
topic and comparison); each population account's 2021-2026 contributions (namespace 0 in full, talk namespaces as counts),
PageAssessments of the edited titles, and the lead counts before / after their edits on outside articles that three or
more accounts of the same population edited. Accounts are HMAC-hashed with the in-job salt; names never reach the file.

Lexicons. Critical = analyze.CRITICAL (settler-colonial, apartheid, genocide, ethnic cleansing, occupation, Nakba /
expulsion, war crimes). Connection ("Jewish-history or Israeli-perspective" terms) = analyze.CONNECTION (indigenous /
homeland / self-determination / Land of Israel; antisemitism / persecution / pogrom) + analyze "terrorism" + JH (Jewish
history: Kingdom of Israel / Judah, First / Second Temple, Hasmonean, Israelites, Judea, Holocaust, Jewish people /
homeland / presence / community / history ...) + IPX (suicide bombing, rocket attacks / fire, hostages). Fixed before
any data was seen.

Edit direction. d_crit = lead critical count after minus before the edit; d_conn likewise. A "critical-term edit" has
d_crit != 0; its direction is the sign of d_crit (insert / remove). A "critical-ward" edit inserts critical terms or removes
connection terms; a "counter" edit does the opposite.

Pattern metrics (per account, compared between the two populations; account-level bootstrap B=2000 for intervals, group
label permutation P=2000 for p values; Cliff's delta as effect size):
  topic concentration  share of 2021-2026 mainspace edits in Israel / Palestine articles (PageAssessments of IP_PROJECTS),
                       and, symmetric for both groups, in the account's HOME topic (the 3 most frequent non-generic
                       WikiProjects of the scoped articles where it made its critical-term edits)
  direction            for accounts with >= 10 critical-term edits: share of those edits in the account's majority direction
  persistence          number of distinct articles where the account's net d_crit has the sign of its majority direction
  re-insertion         share of the account's reverted critical-term edits (scoped articles; reverts by another account,
                       analyze_guard.find_reverts) followed within 30 days by an edit of the same account to the same
                       article that moves the critical count in the same direction again
  single-purpose       home-topic share >= 0.5 (sensitivity 0.33 and 0.75; IP share >= 0.5 shown for both groups)
  timing               spike weeks (weekly mainspace edits >= 10 and > median + 4 MAD of the account's own weeks);
                       lift = share of spike weeks within 0-14 days after a calendar event / share of all weeks there
                       (topic group: Israel / Palestine events; comparison group: the calendar's comparison events)
Privacy: outputs carry no usernames, hashes, revids or per-account rows; distributions are binned and every bin / cell
with 1-2 accounts or 1-2 articles is written "<3"; the discovery list needs >= 3 distinct accounts per article. privacy_scan
must pass before anything is published.
"""
import argparse, gzip, json, math, os, re, sys, time
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze as A             # noqa: E402
import analyze_guard as AG      # noqa: E402

OUT = os.path.join(HERE, "patterns", "trail")
RAW = os.path.join(HERE, "data", "trail", "raw.json.gz")
CAL = os.path.join(HERE, "patterns", "events", "calendar.json")
FROM = "2021-01-01T00:00:00Z"
MIN_ED = 3                      # distinct accounts per discovery article / per published cell
MIN_DIR = 10                    # critical-term edits needed for the direction-consistency metric
REINS_DAYS = 30
SPA = 0.5
EVENT_DAYS = 14
IP_PROJECTS = {"Israel", "Palestine", "Israel Palestine Collaboration", "Jewish history", "Judaism", "Zionism",
               "Jewish culture", "Arab-Israeli conflict", "Arab–Israeli conflict"}
GENERIC = {"Biography", "Military history", "Politics", "Human rights", "Countries", "Cities", "Geography", "Law",
           "International relations", "History", "Religion", "Death", "Disaster management", "Crime and Criminal Biography",
           "Women", "Women's History", "Education", "Journalism", "Media", "Current events", "Discrimination",
           "Social movements", "Ethnic groups", "Organizations", "Socialism", "Conservatism", "Elections and Referendums",
           "United Nations", "Christianity", "Islam", "Middle East", "Terrorism", "Politics of the United States",
           "United States", "Europe", "Asia", "Africa", "Economics", "Business", "Military history/Task forces",
           "Death/Task forces", "Human rights/Task forces", "Sociology", "Philosophy", "Anthropology", "Environment",
           "Women in Red", "Biography/Task forces", "Law Enforcement", "Freedom of speech", "Disability", "Globalization"}

# rev tuple (scoped histories): [revid, ts, u, flags, sha, size, undo_idx, restore_idx, crit, conn]
F_BASE = 32                     # the last revision before 2021 (baseline state, not an edit in the window)
# contribution flags
C_SECT, C_VE, C_MINOR, C_NEW, C_RV = 1, 2, 4, 8, 16

JH = [re.compile(p, re.I) for p in (
    r"\bJewish (?:history|people|peoples|homeland|kingdoms?|state|presence|communit(?:y|ies)|population|heritage|roots|"
    r"connection|life|refugees|civilization|nation)\b",
    r"\bkingdoms? of (?:israel|judah)\b", r"\b(?:first|second) temple\b", r"\bhasmonean\w*", r"\bisraelites?\b",
    r"\bjudaea\b", r"\bjudea\b", r"\bholocaust\b", r"\bjewish exodus\b")]
IPX = [re.compile(p, re.I) for p in (r"\bsuicide bomb\w*", r"\brocket (?:attacks?|fire|barrages?)\b", r"\bhostages?\b")]
CONN_FRAMES = list(A.CONNECTION) + ["terrorism"]


def crit_count(p):
    return sum(A.count(k, p) for k in A.CRITICAL)


def conn_count(p):
    return sum(A.count(k, p) for k in CONN_FRAMES) + sum(len(r.findall(p)) for r in JH + IPX)


def lead_counts_text(wt):
    """section-0 wikitext -> (critical count, connection count)."""
    p = A.prose(A.split_lead(wt))
    return crit_count(p), conn_count(p)


def key_terms(sentence):
    """Surface forms of critical and connection terms in a sentence -> sorted list (lower case)."""
    out = set()
    for k in list(A.CRITICAL) + CONN_FRAMES:
        if A.count(k, sentence) > 0:
            for r in A.RXI[k]:
                out.update(m.group(0).lower() for m in r.finditer(sentence))
    for r in JH + IPX:
        out.update(m.group(0).lower() for m in r.finditer(sentence))
    return sorted(out)


def first_sentence(wt):
    if not wt:
        return None
    ss = A.sentences(A.prose(A.split_lead(wt)))
    return ss[0] if ss else None


def iso(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))


ep = AG.ep
sup = AG.sup
r3 = AG.r3


def sanitize(s, n=240):
    """Public article text for the discovery list: no long digit runs / hex runs (privacy gate patterns), capped."""
    if not s:
        return s
    s = re.sub(r"\d{7,}", "[n]", s)
    s = re.sub(r"(?<![\w.])(?=[0-9]*[a-f])[0-9a-f]{10,}(?![\w.])", "[x]", s, flags=re.I)
    s = re.sub(r"oldid=|diff=|index\.php|curid=|action=compare", "", s, flags=re.I)
    s = s.replace("/wiki/Special:", "/wiki/Special ")
    return s if len(s) <= n else s[:n - 1] + "…"


# ------------------------------------------------------------------ edits in the scoped histories
def chain_deltas(revs):
    """revs (chronological, crit/conn filled or None) -> list of (index, d_crit, d_conn) for revisions in the window with a
    measured predecessor. Hidden / unmeasured revisions break the chain only locally (compared with the last measured one)."""
    out, prev = [], None
    for k, r in enumerate(revs):
        c, n = r[8], r[9]
        if c is None:
            continue
        if prev is not None and not (r[3] & F_BASE):
            out.append((k, c - prev[0], n - prev[1]))
        prev = (c, n)
    return out


def scoped_edits(arts):
    """-> {group: {acct: [(title, ts, d_crit, d_conn, idx)]}} for registered, non-bot accounts (all their lead edits)."""
    E = {"topic": defaultdict(list), "comparison": defaultdict(list)}
    for a in arts:
        revs = a["revs"]
        for k, dc, dn in chain_deltas(revs):
            r = revs[k]
            if r[2] is None or r[3] & (AG.F_ANON | AG.F_BOT | AG.F_HIDDEN):
                continue
            E[a["group"]][r[2]].append((a["title"], r[1], dc, dn, k))
    return E


def rank_population(E_group, n, exclude=(), seed=7):
    """Top n accounts by number of critical-term edits (d_crit != 0); ties broken by a seeded random key (no hash order)."""
    rnd = np.random.default_rng(seed)
    cnt = {u: sum(1 for e in v if e[2] != 0) for u, v in E_group.items() if u not in exclude}
    cnt = {u: c for u, c in cnt.items() if c > 0}
    keys = sorted(cnt)
    tie = dict(zip(keys, rnd.random(len(keys))))
    return sorted(cnt, key=lambda u: (-cnt[u], tie[u]))[:n], cnt


# ------------------------------------------------------------------ discovery
def discovery_candidates(contribs, pop, exclude_titles, titles, min_ed=MIN_ED):
    """-> {title: {acct: [contrib rows]}} for outside titles edited by >= min_ed accounts of the population."""
    by = defaultdict(lambda: defaultdict(list))
    for u in pop:
        c = contribs.get(u)
        if not c:
            continue
        for row in c["ns0"]:
            t = titles[row[2]]
            if t in exclude_titles:
                continue
            by[t][u].append(row)
    return {t: v for t, v in by.items() if len(v) >= min_ed}


def edit_delta(row, disc):
    """contribution row [revid, parentid, tid, ts, sizediff, fl] -> (d_crit, d_conn) or None (unmeasured)."""
    if row[5] & C_SECT and not row[5] & C_VE:
        return (0, 0)                           # a section edit leaves the lead unchanged
    a = disc.get(str(row[0]))
    if a is None:
        return None
    b = (0, 0) if not row[1] else disc.get(str(row[1]))
    if b is None:
        return None
    return (a[0] - b[0], a[1] - b[1])


def rank_discovery(cands, disc, min_ed=MIN_ED):
    """-> list of article dicts ranked by distinct qualifying accounts, then net critical insertions."""
    rows = []
    for t, by in cands.items():
        qual, net_c, net_n, meas, tot, ed_meas = set(), 0, 0, 0, 0, set()
        ins_eds, rem_conn_eds = set(), set()
        for u, rs in by.items():
            for row in rs:
                tot += 1
                d = edit_delta(row, disc)
                if d is None:
                    continue
                meas += 1; ed_meas.add(u)
                net_c += d[0]; net_n += d[1]
                if d[0] > 0:
                    ins_eds.add(u)
                if d[1] < 0:
                    rem_conn_eds.add(u)
                if d[0] > 0 or d[1] < 0:
                    qual.add(u)
        rows.append({"title": t, "editors_edited": len(by), "editors_measured": len(ed_meas),
                     "editors_qualifying": len(qual), "editors_inserting_critical": len(ins_eds),
                     "editors_removing_connection": len(rem_conn_eds), "net_critical": net_c, "net_connection": net_n,
                     "edits": tot, "edits_measured": meas})
    rows.sort(key=lambda r: (-r["editors_qualifying"], -r["net_critical"], r["net_connection"], r["title"]))
    return [r for r in rows if r["editors_qualifying"] >= min_ed], rows


# ------------------------------------------------------------------ statistics
def cliff(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if not len(x) or not len(y):
        return None
    gt = (x[:, None] > y[None, :]).sum(); lt = (x[:, None] < y[None, :]).sum()
    return float((gt - lt) / (len(x) * len(y)))


def compare(xt, xc, rng, B=2000, P=2000, stat="mean"):
    """Two independent samples of account-level values -> estimates, difference, bootstrap CI, permutation p, Cliff's delta."""
    xt = np.asarray([v for v in xt if v is not None and math.isfinite(v)], float)
    xc = np.asarray([v for v in xc if v is not None and math.isfinite(v)], float)
    f = np.mean if stat == "mean" else np.median
    res = {"n_topic": sup(len(xt)), "n_comparison": sup(len(xc)), "stat": stat}
    if len(xt) < MIN_ED or len(xc) < MIN_ED:
        res["note"] = "too few accounts (<3) in a group"
        return res
    obs = float(f(xt) - f(xc))
    bt = [f(rng.choice(xt, len(xt))) for _ in range(B)]
    bc = [f(rng.choice(xc, len(xc))) for _ in range(B)]
    bd = np.asarray(bt) - np.asarray(bc)
    allv = np.concatenate([xt, xc]); nt = len(xt)
    null = []
    for _ in range(P):
        rng.shuffle(allv)
        null.append(f(allv[:nt]) - f(allv[nt:]))
    null = np.asarray(null)
    p = (np.sum(np.abs(null) >= abs(obs) - 1e-12) + 1) / (P + 1)
    cd = cliff(xt, xc)
    bcd = []
    for _ in range(min(B, 500)):
        bcd.append(cliff(rng.choice(xt, len(xt)), rng.choice(xc, len(xc))))
    res.update({"topic": r3(f(xt)), "topic_ci95": AG.ci(bt), "comparison": r3(f(xc)), "comparison_ci95": AG.ci(bc),
                "difference": r3(obs), "difference_ci95": AG.ci(bd), "p_permutation": r3(p, 4),
                "cliffs_delta": r3(cd), "cliffs_delta_ci95": AG.ci(bcd)})
    return res


def compare_share(kt, nt, kc, nc, rng, B=2000):
    """Proportions of accounts -> shares, Wilson intervals, bootstrap CI of the difference, Fisher-like permutation p."""
    def wil(k, n):
        if not n:
            return [None, None]
        z, ph = 1.96, k / n
        d = 1 + z * z / n; c = ph + z * z / (2 * n); s = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n))
        return [r3(max(0.0, (c - s) / d)), r3(min(1.0, (c + s) / d))]
    res = {"topic_k": sup(kt), "topic_n": sup(nt), "comparison_k": sup(kc), "comparison_n": sup(nc)}
    if nt < MIN_ED or nc < MIN_ED:
        res["note"] = "too few accounts"
        return res
    xt = np.r_[np.ones(kt), np.zeros(nt - kt)]; xc = np.r_[np.ones(kc), np.zeros(nc - kc)]
    bd = [rng.choice(xt, nt).mean() - rng.choice(xc, nc).mean() for _ in range(B)]
    allv = np.r_[xt, xc]; obs = kt / nt - kc / nc; null = []
    for _ in range(B):
        rng.shuffle(allv); null.append(allv[:nt].mean() - allv[nt:].mean())
    p = (np.sum(np.abs(np.asarray(null)) >= abs(obs) - 1e-12) + 1) / (B + 1)
    res.update({"topic": r3(kt / nt), "topic_ci95": wil(kt, nt), "comparison": r3(kc / nc), "comparison_ci95": wil(kc, nc),
                "difference": r3(obs), "difference_ci95": AG.ci(bd), "p_permutation": r3(p, 4)})
    return res


def hist(vals, edges):
    """Binned distribution with small-cell suppression -> list of {bin, n}."""
    vals = [v for v in vals if v is not None and math.isfinite(v)]
    out = []
    for k in range(len(edges) - 1):
        lo, hi = edges[k], edges[k + 1]
        last = k == len(edges) - 2
        n = sum(1 for v in vals if lo <= v < hi or (last and v == hi))
        out.append({"bin": f"{lo:g}-{hi:g}", "n": sup(n)})
    return out


def quart(vals):
    vals = [v for v in vals if v is not None and math.isfinite(v)]
    if len(vals) < 2 * MIN_ED:
        return None
    return [r3(np.percentile(vals, q)) for q in (25, 50, 75)]


# ------------------------------------------------------------------ per-account metrics
def week_of(t):
    return int((t - WEEK0) // (7 * 86400))


WEEK0 = ep("2021-01-04T00:00:00Z")      # Monday


def account_metrics(D):
    """-> {group: {acct: metrics dict}} (kept in memory only; never written)."""
    titles = D["titles"]
    assess = D.get("assess") or {}
    scope_pa = D.get("scope_assess") or {}
    arts = D["articles"]
    E = scoped_edits(arts)
    disc = D.get("disc") or {}
    art_by_title = {a["title"]: a for a in arts}
    t_end = ep(D["summary"].get("window_end") or iso(time.time()))
    n_weeks = week_of(t_end) + 1
    M = {}
    for g in ("topic", "comparison"):
        M[g] = {}
        for u in D["population"][g]:
            m = {}
            ev = E[g].get(u, [])
            crit_scoped = [e for e in ev if e[2] != 0]
            # home topic: most frequent non-generic projects of the scoped articles of its critical-term edits
            pc = Counter()
            for e in crit_scoped:
                for p in scope_pa.get(e[0]) or []:
                    if p not in GENERIC:
                        pc[p] += 1
            home = {p for p, _ in pc.most_common(3)}
            c = (D["contribs"].get(u) or {})
            ns0 = c.get("ns0") or []
            m["n_ns0"] = len(ns0); m["n_talk"] = c.get("talk", 0); m["truncated"] = bool(c.get("truncated"))
            ass = [assess.get(titles[r[2]]) for r in ns0]
            done = [x for x in ass if x is not None]
            m["assessed_share"] = len(done) / len(ns0) if ns0 else None
            m["ip_share"] = (sum(1 for x in done if set(x) & IP_PROJECTS) / len(done)) if done else None
            m["home_share"] = (sum(1 for x in done if set(x) & home) / len(done)) if (done and home) else None
            m["talk_ratio"] = (m["n_talk"] / len(ns0)) if ns0 else None
            # all measured critical-term edits: scoped + outside (discovery measurements)
            scoped_titles = set(D["scope"]["topic"]) | set(D["scope"]["comparison"])
            per_art = defaultdict(int)
            dirs = []
            for e in crit_scoped:
                dirs.append(1 if e[2] > 0 else -1); per_art[e[0]] += e[2]
            for r in ns0:
                t = titles[r[2]]
                if t in scoped_titles:
                    continue
                d = edit_delta(r, disc)
                if d and d[0] != 0:
                    dirs.append(1 if d[0] > 0 else -1); per_art[t] += d[0]
            m["n_crit"] = len(dirs)
            m["n_crit_scoped"] = len(crit_scoped)
            if dirs:
                ins = sum(1 for x in dirs if x > 0)
                maj = 1 if ins * 2 >= len(dirs) else -1
                m["majority"] = "insert" if maj > 0 else "remove"
                m["consistency"] = max(ins, len(dirs) - ins) / len(dirs)
                m["persist"] = sum(1 for v in per_art.values() if v != 0 and (v > 0) == (maj > 0))
                m["arts_crit"] = sum(1 for v in per_art.values() if v != 0)
            else:
                m["majority"] = None; m["consistency"] = None; m["persist"] = 0; m["arts_crit"] = 0
            # re-insertion after reverts (scoped articles)
            m["reverted"], m["reinserted"] = reinsertion(u, ev, art_by_title)
            # timing
            wk = np.zeros(max(1, n_weeks), int)
            for r in ns0:
                w = week_of(r[3])
                if 0 <= w < len(wk):
                    wk[w] += 1
            m["weeks"] = wk
            M[g][u] = m
    return M, E


def reinsertion(u, ev, art_by_title, days=REINS_DAYS):
    """-> (reverted critical-term episodes, of which re-inserted within `days`) for account u in the scoped articles."""
    by_art = defaultdict(list)
    for e in ev:
        by_art[e[0]].append(e)
    n_rv, n_re = 0, 0
    for t, es in by_art.items():
        a = art_by_title[t]; revs = a["revs"]
        if not any(e[2] != 0 for e in es):
            continue
        rvs = a.get("_reverts")
        if rvs is None:
            rvs = a["_reverts"] = AG.find_reverts(revs)
            pos = {r[0]: k for k, r in enumerate(revs)}
            for rv in rvs:
                b = pos.get(rv["before"], -1) if rv["before"] else -1
                rv["_lo"], rv["_hi"] = b + 1, pos.get(rv["after"], -1)
        dmap = {e[4]: e[2] for e in es}
        for rv in rvs:
            if rv["u"] == u or u not in rv["rev_authors"]:
                continue
            net = sum(dmap.get(k, 0) for k in range(rv["_lo"], rv["_hi"] + 1))
            if net == 0:
                continue
            n_rv += 1
            sgn = net > 0
            if any(e[1] > rv["t"] and e[1] <= rv["t"] + days * 86400 and e[2] != 0 and (e[2] > 0) == sgn for e in es):
                n_re += 1
    return n_rv, n_re


def spikes(wk):
    wk = np.asarray(wk, float)
    if wk.sum() == 0:
        return np.zeros(len(wk), bool)
    med = np.median(wk); mad = np.median(np.abs(wk - med)) or 1.0
    return (wk >= 10) & (wk > med + 4 * mad)


def event_weeks(cal, kind, n_weeks):
    mask = np.zeros(n_weeks, bool)
    for e in cal:
        is_cmp = e.get("type") == "comparison"
        if (kind == "comparison") != is_cmp:
            continue
        t0 = ep(e["date"] + "T00:00:00Z")
        for d in range(0, EVENT_DAYS + 1):
            w = week_of(t0 + d * 86400)
            if 0 <= w < n_weeks:
                mask[w] = True
    return mask


def timing(M, cal, rng, B=2000):
    out = {}
    lifts = {}
    for g in ("topic", "comparison"):
        accts = list(M[g].values())
        if not accts:
            out[g] = {"note": "no accounts"}; continue
        n_weeks = len(accts[0]["weeks"])
        mask = event_weeks(cal, g, n_weeks)
        exp = float(mask.mean()) if n_weeks else None
        per = []
        for m in accts:
            s = spikes(m["weeks"])
            per.append((int(s.sum()), int((s & mask).sum()), float(m["weeks"][mask].sum()), float(m["weeks"].sum())))
        def lift(rows):
            ns = sum(r[0] for r in rows); ni = sum(r[1] for r in rows)
            return (ni / ns) / exp if ns and exp else None
        def act_lift(rows):
            tot = sum(r[3] for r in rows); inn = sum(r[2] for r in rows)
            return (inn / tot) / exp if tot and exp else None
        L = lift(per)
        bl = [lift([per[i] for i in rng.integers(0, len(per), len(per))]) for _ in range(B)]
        ba = [act_lift([per[i] for i in rng.integers(0, len(per), len(per))]) for _ in range(B)]
        lifts[g] = (per, bl)
        out[g] = {"accounts_with_spikes": sup(sum(1 for r in per if r[0])), "spike_weeks": sum(r[0] for r in per),
                  "spike_weeks_in_event_windows": sum(r[1] for r in per), "expected_share_of_weeks": r3(exp),
                  "spike_lift": r3(L), "spike_lift_ci95": AG.ci(bl),
                  "activity_lift": r3(act_lift(per)), "activity_lift_ci95": AG.ci(ba),
                  "events": int(sum(1 for e in cal if (e.get("type") == "comparison") == (g == "comparison")))}
    if "topic" in lifts and "comparison" in lifts:
        bt, bc = np.asarray([x if x is not None else np.nan for x in lifts["topic"][1]]), \
                 np.asarray([x if x is not None else np.nan for x in lifts["comparison"][1]])
        d = bt - bc
        lt, lc = out["topic"].get("spike_lift"), out["comparison"].get("spike_lift")
        out["difference"] = {"spike_lift_difference": r3(lt - lc) if lt is not None and lc is not None else None,
                             "ci95": AG.ci(d[np.isfinite(d)])}
    return out


# ------------------------------------------------------------------ analysis
def analyze(D, seed=11, B=2000, P=2000, log=print):
    rng = np.random.default_rng(seed)
    cal = json.load(open(CAL))["events"] if os.path.exists(CAL) else []
    M, E = account_metrics(D)
    R = {"meta": meta(D, M)}
    T, C = M["topic"], M["comparison"]
    # population description
    R["population"] = {g: {"accounts": sup(len(M[g])),
                           "critical_term_edits_in_scope_quartiles": quart([m["n_crit_scoped"] for m in M[g].values()]),
                           "mainspace_edits_2021_2026_quartiles": quart([m["n_ns0"] for m in M[g].values()]),
                           "contribution_lists_truncated": sup(sum(1 for m in M[g].values() if m["truncated"])),
                           "assessed_share_of_edits_median": r3(np.median([m["assessed_share"] for m in M[g].values()
                                                                          if m["assessed_share"] is not None]))
                           if any(m["assessed_share"] is not None for m in M[g].values()) else None}
                       for g in ("topic", "comparison")}
    # (b) patterns
    E1 = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0]
    P_ = {}
    P_["topic_concentration_ip"] = {
        "what": "share of each account's 2021-2026 mainspace edits in Israel / Palestine articles (PageAssessments)",
        **compare([m["ip_share"] for m in T.values()], [m["ip_share"] for m in C.values()], rng, B, P),
        "quartiles": {"topic": quart([m["ip_share"] for m in T.values()]), "comparison": quart([m["ip_share"] for m in C.values()])},
        "distribution": {"topic": hist([m["ip_share"] for m in T.values()], E1),
                         "comparison": hist([m["ip_share"] for m in C.values()], E1)}}
    P_["topic_concentration_home"] = {
        "what": "share of each account's mainspace edits in its own home topic (3 most frequent non-generic WikiProjects of "
                "the scoped articles where it made critical-term edits); the like-for-like comparison",
        **compare([m["home_share"] for m in T.values()], [m["home_share"] for m in C.values()], rng, B, P),
        "quartiles": {"topic": quart([m["home_share"] for m in T.values()]), "comparison": quart([m["home_share"] for m in C.values()])},
        "distribution": {"topic": hist([m["home_share"] for m in T.values()], E1),
                         "comparison": hist([m["home_share"] for m in C.values()], E1)}}
    ct = [m["consistency"] for m in T.values() if m["n_crit"] >= MIN_DIR]
    cc = [m["consistency"] for m in C.values() if m["n_crit"] >= MIN_DIR]
    maj = {g: Counter(m["majority"] for m in M[g].values() if m["n_crit"] >= MIN_DIR) for g in M}
    P_["direction_consistency"] = {
        "what": f"accounts with >= {MIN_DIR} critical-term edits: share of those edits in the account's majority direction "
                "(0.5 = balanced, 1 = always one way)",
        **compare(ct, cc, rng, B, P),
        "majority_direction": {g: {k: sup(v) for k, v in maj[g].items()} for g in maj},
        "share_at_least_0.8": compare_share(sum(1 for x in ct if x >= .8), len(ct), sum(1 for x in cc if x >= .8), len(cc), rng, B),
        "distribution": {"topic": hist(ct, [.5, .6, .7, .8, .9, 1.0]), "comparison": hist(cc, [.5, .6, .7, .8, .9, 1.0])},
        "coin_flip_expectation": r3(coin_flip_consistency(ct + cc, rng))}
    pe = [0, 1, 2, 3, 5, 10, 20, 50, 1e9]
    P_["cross_article_persistence"] = {
        "what": "number of distinct articles where the account's net critical-term change has the sign of its majority "
                "direction (scoped articles + outside articles edited by >= 3 accounts of its group)",
        **compare([m["persist"] for m in T.values()], [m["persist"] for m in C.values()], rng, B, P, stat="median"),
        "mean": compare([m["persist"] for m in T.values()], [m["persist"] for m in C.values()], rng, B, P),
        "share_of_articles_same_direction": compare(
            [m["persist"] / m["arts_crit"] for m in T.values() if m["arts_crit"] >= 3],
            [m["persist"] / m["arts_crit"] for m in C.values() if m["arts_crit"] >= 3], rng, B, P),
        "distribution": {"topic": hist([m["persist"] for m in T.values()], pe),
                         "comparison": hist([m["persist"] for m in C.values()], pe)}}
    for d in P_["cross_article_persistence"]["distribution"].values():
        for b in d:
            b["bin"] = b["bin"].replace("-1e+09", "+")
    rv_t = sum(m["reverted"] for m in T.values()); re_t = sum(m["reinserted"] for m in T.values())
    rv_c = sum(m["reverted"] for m in C.values()); re_c = sum(m["reinserted"] for m in C.values())
    P_["reinsertion_after_revert"] = {
        "what": f"share of reverted critical-term edits (scoped articles, reverted by another account) followed within "
                f"{REINS_DAYS} days by the same account moving the same article's critical count the same way again",
        "topic_reverted": rv_t, "topic_reinserted": re_t, "comparison_reverted": rv_c, "comparison_reinserted": re_c,
        "accounts_with_reverts": {"topic": sup(sum(1 for m in T.values() if m["reverted"])),
                                  "comparison": sup(sum(1 for m in C.values() if m["reverted"]))},
        "pooled": pooled_rate(T, C, rng, B),
        "per_account": compare([m["reinserted"] / m["reverted"] for m in T.values() if m["reverted"] >= 3],
                               [m["reinserted"] / m["reverted"] for m in C.values() if m["reverted"] >= 3], rng, B, P)}
    hs_t = [m["home_share"] for m in T.values() if m["home_share"] is not None]
    hs_c = [m["home_share"] for m in C.values() if m["home_share"] is not None]
    ip_t = [m["ip_share"] for m in T.values() if m["ip_share"] is not None]
    ip_c = [m["ip_share"] for m in C.values() if m["ip_share"] is not None]
    P_["single_purpose"] = {
        "what": f"account is single-purpose if >= {SPA:.0%} of its 2021-2026 mainspace edits are in its home topic",
        "threshold_0.5": compare_share(sum(1 for x in hs_t if x >= SPA), len(hs_t), sum(1 for x in hs_c if x >= SPA), len(hs_c), rng, B),
        "sensitivity_0.33": compare_share(sum(1 for x in hs_t if x >= 1 / 3), len(hs_t), sum(1 for x in hs_c if x >= 1 / 3), len(hs_c), rng, B),
        "sensitivity_0.75": compare_share(sum(1 for x in hs_t if x >= .75), len(hs_t), sum(1 for x in hs_c if x >= .75), len(hs_c), rng, B),
        "ip_share_0.5": compare_share(sum(1 for x in ip_t if x >= SPA), len(ip_t), sum(1 for x in ip_c if x >= SPA), len(ip_c), rng, B)}
    P_["timing_vs_events"] = {"what": "spike weeks of mainspace activity in the 0-14 days after calendar events (lift 1 = "
                                      "no more than the share of weeks those windows cover)", **timing(M, cal, rng, B)}
    P_["talk_ratio"] = {"what": "talk-namespace edits per mainspace edit, 2021-2026",
                        **compare([m["talk_ratio"] for m in T.values()], [m["talk_ratio"] for m in C.values()], rng, B, P, stat="median")}
    R["patterns"] = P_
    # (a) discovery
    R["discovery"] = discovery_results(D)
    R["verdicts"] = verdicts(R)
    R["suppressed"] = suppressed_note(R)
    return R


def coin_flip_consistency(vals_unused, rng, n=20, reps=4000):
    """Expected majority share for an account with n critical-term edits whose directions are fair coin flips."""
    x = rng.binomial(n, .5, reps)
    return float(np.mean(np.maximum(x, n - x) / n))


def pooled_rate(T, C, rng, B=2000):
    tt = [(m["reverted"], m["reinserted"]) for m in T.values() if m["reverted"]]
    cc = [(m["reverted"], m["reinserted"]) for m in C.values() if m["reverted"]]
    def rate(rows):
        n = sum(r[0] for r in rows)
        return sum(r[1] for r in rows) / n if n else None
    res = {"topic": r3(rate(tt)), "comparison": r3(rate(cc))}
    if len(tt) < MIN_ED or len(cc) < MIN_ED:
        res["note"] = "too few accounts with reverted critical-term edits (<3)"
        return res
    bt = [rate([tt[i] for i in rng.integers(0, len(tt), len(tt))]) for _ in range(B)]
    bc = [rate([cc[i] for i in rng.integers(0, len(cc), len(cc))]) for _ in range(B)]
    bd = [a - b for a, b in zip(bt, bc) if a is not None and b is not None]
    res.update({"topic_ci95": AG.ci([x for x in bt if x is not None]), "comparison_ci95": AG.ci([x for x in bc if x is not None]),
                "difference": r3(res["topic"] - res["comparison"]), "difference_ci95": AG.ci(bd)})
    return res


def meta(D, M):
    s = D["summary"]
    return {"generated": iso(time.time()), "window": [FROM, s.get("window_end")],
            "scope_articles": {g: len(D["scope"][g]) for g in ("topic", "comparison")},
            "histories": s.get("history"), "leads": s.get("leads"), "contribs": s.get("contribs"),
            "assess": s.get("assess"), "discovery_measurement": s.get("discovery"), "extras": s.get("extras"),
            "population_size": {g: len(M[g]) for g in M}, "population_target": s.get("population_target"),
            "population_overlap_removed_from_comparison": sup(s.get("population_overlap", 0)),
            "requests": s.get("requests"), "elapsed_min": s.get("elapsed_min"),
            "bootstrap": 2000, "permutations": 2000}


def note_for(row, ex):
    """One-line, rule-based note on why an article may matter to the report."""
    pr = set(ex.get("projects") or [])
    desc = (ex.get("description") or "").lower()
    bits = []
    if pr & {"Jewish history", "Judaism", "Jewish culture"}:
        bits.append("Jewish history / Judaism article")
    if re.search(r"\b(village|town|city|municipality|neighbourhood|neighborhood|settlement|kibbutz|moshav|refugee camp)\b", desc):
        bits.append("a specific place")
    if "Biography" in pr or re.search(r"\b(born|politician|activist|writer|journalist|historian|singer|actor|actress|rabbi|"
                                      r"professor|scholar|footballer)\b", desc):
        bits.append("a person (BLP rules may apply)")
    if "Countries" in pr or re.search(r"\bcountry in\b|\bsovereign state\b", desc):
        bits.append("a country article")
    now = set(ex.get("first_now_terms") or []); then = set(ex.get("first_2021_terms") or [])
    if any("apartheid" in t for t in now | then) or re.search(r"apartheid", row["title"], re.I):
        bits.append("apartheid framing")
    if not (pr & IP_PROJECTS) and pr:
        bits.append("outside the Israel / Palestine WikiProjects")
    if ex.get("in_wider_corpus"):
        bits.append("already in our wider corpus (below Top/High)")
    gained, lost = sorted(now - then), sorted(then - now)
    if gained or lost:
        bits.append("first sentence " + "; ".join(x for x in (("gained " + ", ".join(gained)) if gained else "",
                                                              ("lost " + ", ".join(lost)) if lost else "") if x) + " since 2021")
    elif ex.get("created_after_2021"):
        bits.append("article created after 2021")
    else:
        bits.append("first sentence key terms unchanged since 2021; the changes are elsewhere in the opening section")
    return "; ".join(bits)


def discovery_results(D):
    titles = D["titles"]
    excl = set(D["scope"]["topic"]) | set(D["scope"]["comparison"])
    disc = D.get("disc") or {}
    out = {}
    for g in ("topic", "comparison"):
        cands = discovery_candidates(D["contribs"], D["population"][g], excl, titles)
        ranked, allrows = rank_discovery(cands, disc)
        n_meas = sum(1 for r in allrows if r["editors_measured"] >= MIN_ED)
        out[g] = {"candidate_articles": len(cands), "candidates_measured_3plus": n_meas,
                  "articles_3plus_qualifying_editors": len(ranked),
                  "articles_3plus_inserting_critical": sum(1 for r in allrows if r["editors_inserting_critical"] >= MIN_ED),
                  "articles_3plus_removing_connection": sum(1 for r in allrows if r["editors_removing_connection"] >= MIN_ED)}
        if g == "topic":
            ex = D.get("extras") or {}
            lst = []
            for r in ranked:
                e = ex.get(r["title"]) or {}
                item = {"title": r["title"], "distinct_editors_qualifying": r["editors_qualifying"],
                        "distinct_editors_inserting_critical": sup(r["editors_inserting_critical"]),
                        "distinct_editors_removing_connection": sup(r["editors_removing_connection"]),
                        "distinct_editors_edited": r["editors_edited"], "net_critical_insertions": r["net_critical"],
                        "net_connection_change": r["net_connection"], "edits_measured": r["edits_measured"],
                        "first_sentence_2021_terms": e.get("first_2021_terms"), "first_sentence_now_terms": e.get("first_now_terms"),
                        "first_sentence_2021": sanitize(e.get("first_2021")), "first_sentence_now": sanitize(e.get("first_now")),
                        "lead_critical_2021_vs_now": e.get("lead_crit"), "lead_connection_2021_vs_now": e.get("lead_conn"),
                        "monthly_views_last_12m": fmt_views(e.get("views_month")) if e.get("views_month") is not None else None, "projects": e.get("projects"),
                        "note": note_for(r, e) if e else None}
                lst.append(item)
            out[g]["articles"] = lst
    return out


def fmt_views(v):
    if v is None:
        return "n/a"
    if isinstance(v, str):
        return v
    v = float(v)
    return f"{v / 1e6:.1f}M" if v >= 1e6 else f"{v / 1e3:.1f}k" if v >= 1e3 else f"{v:.0f}"


# ------------------------------------------------------------------ verdicts and rendering
def _excl0(d):
    ci = (d or {}).get("difference_ci95") or [None, None]
    return ci[0] is not None and ci[1] is not None and (ci[0] > 0 or ci[1] < 0)


def _v(d, more, less, same):
    if not d or d.get("note"):
        return "inconclusive: " + ((d or {}).get("note") or "not computed")
    if _excl0(d):
        return more if d["difference"] > 0 else less
    return same


def verdicts(R):
    P = R["patterns"]; v = {}
    v["topic_concentration"] = _v(P["topic_concentration_home"],
                                  "consistent with more concentrated topic interest than the comparison group (higher home-topic share). Concentrated interest is NOT by itself evidence of a vendetta",
                                  "the topic group is LESS concentrated on its home topic than the comparison group",
                                  "not distinguishable from the comparison group: both populations concentrate on their home topic to a similar degree")
    v["direction_consistency"] = _v(P["direction_consistency"],
                                    "consistent with more one-directional critical-term editing than the comparison group",
                                    "the topic group's critical-term edits are LESS one-directional than the comparison group's",
                                    "not distinguishable from the comparison group in how one-directional critical-term edits are")
    v["cross_article_persistence"] = _v(P["cross_article_persistence"]["mean"],
                                        "consistent with pushing the same direction across more articles than the comparison group",
                                        "the topic group pushes one direction across FEWER articles than the comparison group",
                                        "not distinguishable from the comparison group in the number of articles pushed the same way")
    pr = P["reinsertion_after_revert"]["pooled"]
    v["reinsertion"] = _v(pr, "consistent with more re-insertion after reverts than the comparison group",
                          "the topic group re-inserts LESS after reverts than the comparison group",
                          "not distinguishable from the comparison group in re-insertion after reverts")
    v["single_purpose"] = _v(P["single_purpose"]["threshold_0.5"],
                             "consistent with a larger share of single-purpose accounts than the comparison group (topic focus, not by itself misconduct)",
                             "the topic group has FEWER single-purpose accounts than the comparison group",
                             "not distinguishable from the comparison group in the share of single-purpose accounts")
    td = P["timing_vs_events"].get("difference") or {}
    tdd = {"difference": td.get("spike_lift_difference"), "difference_ci95": td.get("ci95")}
    v["timing"] = _v(tdd if tdd["difference"] is not None else {"note": "no spike weeks"},
                     "consistent with activity spikes tied more closely to news events than in the comparison group (news-driven editing, not by itself coordination)",
                     "the topic group's spikes are tied LESS closely to its events than the comparison group's",
                     "not distinguishable from the comparison group in how closely activity spikes follow news events")
    return v


def suppressed_note(R):
    """List the cells written as '<3' (by path), so the report can say what was withheld."""
    hits = []
    def walk(o, path):
        if isinstance(o, dict):
            for k, x in o.items():
                walk(x, path + [str(k)])
        elif isinstance(o, list):
            for i, x in enumerate(o):
                walk(x, path + [str(i)])
        elif o == "<3":
            hits.append("/".join(path))
    walk({k: v for k, v in R.items() if k != "suppressed"}, [])
    return {"cells_written_lt3": len(hits), "paths": hits[:200],
            "rule": "cells with 1-2 accounts are written <3; discovery articles need >= 3 distinct accounts; distributions are "
                    "binned; no per-account rows, labels, edit counts, revision ids or article lists are published"}


def f(x, k=2):
    if x is None:
        return "n/a"
    if isinstance(x, str):
        return x
    return f"{x:.{k}f}"


def fci(c, k=2):
    return f"[{f(c[0], k)}, {f(c[1], k)}]" if c and c[0] is not None else "[n/a]"


def line_cmp(d, k=2, pct=False):
    if not d or d.get("note"):
        return (d or {}).get("note", "n/a")
    g = (lambda x: f"{100 * x:.0f}%" if x is not None else "n/a") if pct else (lambda x: f(x, k))
    gc = (lambda c: f"[{g(c[0])}, {g(c[1])}]") if pct else (lambda c: fci(c, k))
    s = (f"topic {g(d['topic'])} {gc(d['topic_ci95'])} (n={d.get('n_topic', d.get('topic_n'))}) vs comparison "
         f"{g(d['comparison'])} {gc(d['comparison_ci95'])} (n={d.get('n_comparison', d.get('comparison_n'))}); difference "
         f"{('%+.0f pp' % (100 * d['difference'])) if pct else ('%+.*f' % (k, d['difference']))} "
         f"{('[%+.0f, %+.0f] pp' % (100 * d['difference_ci95'][0], 100 * d['difference_ci95'][1])) if pct and d['difference_ci95'][0] is not None else fci(d['difference_ci95'], k)}")
    if d.get("p_permutation") is not None:
        s += f", permutation p {d['p_permutation']}"
    if d.get("cliffs_delta") is not None:
        s += f", Cliff's delta {f(d['cliffs_delta'])} {fci(d['cliffs_delta_ci95'])}"
    return s


def render_dist(dd):
    return "; ".join(f"{b['bin']}: {b['n']}" for b in dd)


def render_cards(R):
    m = R["meta"]; P = R["patterns"]; V = R["verdicts"]; pop = R["population"]
    L = ["# Editor trail: pattern cards (aggregate only)", "",
         f"Generated {m['generated']}. Window {m['window'][0][:10]} to {(m['window'][1] or '')[:10]}. No usernames, account "
         "hashes, revision ids, per-account rows or per-account article lists appear here. Cells with 1-2 accounts are "
         "written <3. Each card compares the topic population with the comparison population and gives an effect size with "
         "a 95% bootstrap interval (accounts resampled) and a label-permutation p value.", "",
         "**Read this first.** Concentrated interest in a topic is NOT by itself evidence of a vendetta, of bad faith or of "
         "coordination. Many good-faith editors specialise. The comparison group (the most active critical-term editors of "
         "matched comparison articles: other conflicts, countries and ideologies) shows what ordinary heavy topic editing "
         "looks like. Where the topic group differs, the right wording is \"consistent with\" a pattern; where it does not, "
         "it is \"not distinguishable from\" the comparison group.", "",
         f"Populations: topic {pop['topic']['accounts']} accounts, comparison {pop['comparison']['accounts']} accounts "
         f"(target {m.get('population_target')}; accounts in both top lists were kept in the topic group only: "
         f"{m.get('population_overlap_removed_from_comparison')}). Critical-term edits in scope per account, quartiles: topic "
         f"{pop['topic']['critical_term_edits_in_scope_quartiles']}, comparison {pop['comparison']['critical_term_edits_in_scope_quartiles']}. "
         f"Mainspace edits 2021-2026 per account, quartiles: topic {pop['topic']['mainspace_edits_2021_2026_quartiles']}, "
         f"comparison {pop['comparison']['mainspace_edits_2021_2026_quartiles']}.", "",
         f"Coverage: histories {m.get('histories')}; leads {m.get('leads')}; contributions {m.get('contribs')}; "
         f"assessments {m.get('assess')}; outside-article lead measurements {m.get('discovery_measurement')}.", ""]
    c = P["topic_concentration_ip"]; h = P["topic_concentration_home"]
    L += ["## 1. Topic concentration", "",
          f"Israel / Palestine share of mainspace edits: {line_cmp(c, pct=True)}. Quartiles topic {c.get('quartiles', {}).get('topic')}, "
          f"comparison {c.get('quartiles', {}).get('comparison')}. (The comparison group's own topics are not Israel / "
          "Palestine, so this row only describes the topic group; the like-for-like row is the next one.)", "",
          f"Home-topic share (symmetric): {line_cmp(h, pct=True)}.", "",
          f"Distribution, Israel / Palestine share (accounts per bin): topic {render_dist(c['distribution']['topic'])}; "
          f"comparison {render_dist(c['distribution']['comparison'])}.", "",
          f"Distribution, home-topic share: topic {render_dist(h['distribution']['topic'])}; comparison "
          f"{render_dist(h['distribution']['comparison'])}.", "",
          f"**Verdict:** {V['topic_concentration']}.", ""]
    d = P["direction_consistency"]
    L += ["## 2. Direction consistency", "",
          f"{d['what']}. {line_cmp(d)}. A fair coin would give about {f(d['coin_flip_expectation'])} for an account with 20 "
          f"such edits. Majority direction (accounts): topic {d['majority_direction'].get('topic')}, comparison "
          f"{d['majority_direction'].get('comparison')}. Share of accounts at 0.8 or above: {line_cmp(d['share_at_least_0.8'], pct=True)}.", "",
          f"Distribution: topic {render_dist(d['distribution']['topic'])}; comparison {render_dist(d['distribution']['comparison'])}.", "",
          "Caveat: an account that mostly reverts vandalism or unsourced changes in one direction is also one-directional. "
          "This metric does not tell good-faith maintenance from advocacy.", "",
          f"**Verdict:** {V['direction_consistency']}.", ""]
    p = P["cross_article_persistence"]
    L += ["## 3. Cross-article persistence", "",
          f"{p['what']}. Median: {line_cmp(p)}. Mean: {line_cmp(p['mean'], 1)}. Share of an account's critical-term articles "
          f"that go its majority way (accounts with 3+ such articles): {line_cmp(p['share_of_articles_same_direction'], pct=True)}.", "",
          f"Distribution (articles): topic {render_dist(p['distribution']['topic'])}; comparison {render_dist(p['distribution']['comparison'])}.", "",
          f"**Verdict:** {V['cross_article_persistence']}.", ""]
    r = P["reinsertion_after_revert"]; pr = r["pooled"]
    L += ["## 4. Re-insertion after reverts", "",
          f"{r['what']}. Topic: {r['topic_reinserted']} of {r['topic_reverted']} reverted critical-term episodes; comparison: "
          f"{r['comparison_reinserted']} of {r['comparison_reverted']}. Pooled rate: topic {f(pr.get('topic'))} {fci(pr.get('topic_ci95'))}, "
          f"comparison {f(pr.get('comparison'))} {fci(pr.get('comparison_ci95'))}; difference {f(pr.get('difference'))} "
          f"{fci(pr.get('difference_ci95'))}{(' (' + pr['note'] + ')') if pr.get('note') else ''}. Per account (3+ reverted episodes): "
          f"{line_cmp(r['per_account'])}.", "",
          "Caveat: re-insertion can be a restored, better-sourced version after talk-page agreement; the metric does not see "
          "the talk page.", "",
          f"**Verdict:** {V['reinsertion']}.", ""]
    s = P["single_purpose"]
    L += ["## 5. Single-purpose accounts", "",
          f"{s['what']}. At 0.5: {line_cmp(s['threshold_0.5'], pct=True)}. Sensitivity at 0.33: {line_cmp(s['sensitivity_0.33'], pct=True)}. "
          f"At 0.75: {line_cmp(s['sensitivity_0.75'], pct=True)}. Israel / Palestine share at 0.5 (descriptive for the topic "
          f"group): {line_cmp(s['ip_share_0.5'], pct=True)}.", "",
          "Single-purpose is a description of focus. Wikipedia's own guidance treats such accounts with extra scrutiny for "
          "advocacy but does not treat focus as misconduct.", "",
          f"**Verdict:** {V['single_purpose']}.", ""]
    t = P["timing_vs_events"]
    tl = []
    for g in ("topic", "comparison"):
        x = t.get(g) or {}
        if x.get("note"):
            tl.append(f"{g}: {x['note']}"); continue
        tl.append(f"{g}: {x['spike_weeks']} spike weeks among {x['accounts_with_spikes']} accounts, "
                  f"{x['spike_weeks_in_event_windows']} in the windows after {x['events']} events (windows cover "
                  f"{f(x['expected_share_of_weeks'])} of weeks); spike lift {f(x['spike_lift'])} {fci(x['spike_lift_ci95'])}; "
                  f"all-activity lift {f(x['activity_lift'])} {fci(x['activity_lift_ci95'])}")
    td = t.get("difference") or {}
    L += ["## 6. Timing of activity spikes against the event calendar", "",
          f"{t['what']}. " + "; ".join(tl) + f". Difference in spike lift (topic - comparison): "
          f"{f(td.get('spike_lift_difference'))} {fci(td.get('ci95'))}.", "",
          "Caveat: the Israel / Palestine calendar has many more events than the comparison calendar, so its windows cover "
          "more weeks and its maximum possible lift is lower; lifts are comparable, raw counts are not. News-driven spikes are "
          "what ordinary editors also do.", "",
          f"**Verdict:** {V['timing']}.", ""]
    tr = P["talk_ratio"]
    L += ["## 7. Talk-page share (context)", "", f"{tr['what']}. Median: {line_cmp(tr)}.", ""]
    L += ["## Overall", "",
          "The pattern cards above are aggregate comparisons of two populations of heavy editors. A difference on a single "
          "metric is consistent with several explanations (expertise, maintenance, advocacy, a 1RR environment). None of the "
          "metrics, alone or together, identifies a vendetta or off-wiki coordination; ArbCom findings are the only "
          "account-level judgements this project relies on, and they are not linked to these data.", "",
          f"Suppressed for privacy: {R['suppressed']['cells_written_lt3']} cells written <3. {R['suppressed']['rule']}.", ""]
    return "\n".join(L)


def render_articles(R):
    D = R["discovery"]; t = D["topic"]; c = D["comparison"]
    L = ["# Editor trail: outside articles changed by the top topic editors (discovery list)", "",
         f"Generated {R['meta']['generated']}. Articles OUTSIDE the scoped topic and comparison sets where at least 3 distinct "
         "accounts of the topic population (the ~40 most active critical-term editors of the scoped opening sections, "
         "2021-2026) made an edit that inserted critical terms (analyze.CRITICAL) or removed Jewish-history / "
         "Israeli-perspective terms (CONN) in the opening section. Ranked by the number of such distinct accounts, then by the "
         "net critical-term insertions of all their measured edits. No account is named or labelled; counts only.", "",
         f"Topic population: {t['candidate_articles']} outside articles were edited by 3+ accounts; {t['candidates_measured_3plus']} "
         f"had 3+ accounts' edits measured; {t['articles_3plus_qualifying_editors']} qualify (3+ accounts with a qualifying edit; "
         f"{t['articles_3plus_inserting_critical']} with 3+ inserting critical terms, {t['articles_3plus_removing_connection']} "
         f"with 3+ removing connection terms).", "",
         f"Baseline, comparison population (same rule, its own outside articles): {c['candidate_articles']} edited by 3+ "
         f"accounts, {c['articles_3plus_qualifying_editors']} qualify ({c['articles_3plus_inserting_critical']} inserting "
         f"critical, {c['articles_3plus_removing_connection']} removing connection terms).", "",
         "Columns: editors = distinct accounts with a qualifying edit (ins = inserting critical terms, rem = removing connection "
         "terms); net crit = net critical-term change summed over all measured edits of the population's accounts (positive = "
         "inserted); net conn = same for connection terms; first sentence key terms 2021 -> now; lead counts 2021 -> now "
         "(critical / connection); monthly views = mean monthly user page views over the last 12 months.", "",
         "| # | Article | Editors (ins / rem) | Net crit | Net conn | First sentence key terms, 2021 -> now | Lead crit 2021->now | Monthly views | Why it might matter |",
         "|---|---|---|---|---|---|---|---|---|"]
    for k, a in enumerate(t.get("articles") or [], 1):
        t21 = ", ".join(a["first_sentence_2021_terms"]) if a["first_sentence_2021_terms"] else ("-" if a["first_sentence_2021_terms"] is not None else "n/a")
        tn = ", ".join(a["first_sentence_now_terms"]) if a["first_sentence_now_terms"] else ("-" if a["first_sentence_now_terms"] is not None else "n/a")
        lc = a.get("lead_critical_2021_vs_now")
        lcs = f"{lc[0] if lc[0] is not None else 'n/a'} -> {lc[1] if lc[1] is not None else 'n/a'}" if lc else "n/a"
        L.append(f"| {k} | {a['title']} | {a['distinct_editors_qualifying']} ({a['distinct_editors_inserting_critical']} / "
                 f"{a['distinct_editors_removing_connection']}) | {a['net_critical_insertions']:+d} | {a['net_connection_change']:+d} | "
                 f"{t21} -> {tn} | {lcs} | {fmt_views(a['monthly_views_last_12m'])} | {a['note'] or 'n/a'} |")
    L += ["", "## First sentences (2021 and now)", ""]
    for k, a in enumerate((t.get("articles") or [])[:40], 1):
        L += [f"**{k}. {a['title']}**", f"- 2021: {a['first_sentence_2021'] or 'n/a (no 2021 version)'}",
              f"- Now: {a['first_sentence_now'] or 'n/a'}", ""]
    L += ["Method notes: an edit's lead change is the critical / connection count of its section 0 minus that of its parent "
          "revision; section edits made in the source editor (summary starting with a section heading) leave the lead "
          "unchanged and are counted as zero. Net counts include every measured edit of the population's accounts on the "
          "article, in both directions. Articles in our scoped sets are excluded. The list finds candidates; whether a change "
          "is an improvement or a distortion needs a reading of the sources.", ""]
    return "\n".join(L)


def write_outputs(R, out_dir=OUT):
    os.makedirs(out_dir, exist_ok=True)
    json.dump(R, open(os.path.join(out_dir, "results.json"), "w"), indent=1, ensure_ascii=False,
              default=lambda o: o.item() if hasattr(o, "item") else str(o))
    open(os.path.join(out_dir, "cards.md"), "w").write(render_cards(R))
    open(os.path.join(out_dir, "articles.md"), "w").write(render_articles(R))


def scan(path):
    import analyze_coord as AC
    return AC.privacy_scan(path, [os.environ.get("WT_SALT", "")])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan")
    ap.add_argument("--data", default=RAW)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--boot", type=int, default=int(os.environ.get("TRAIL_BOOT", "2000")))
    a = ap.parse_args()
    if a.scan:
        bad = scan(a.scan)
        for b in bad[:50]:
            print("PRIVACY:", b)
        sys.exit(f"privacy gate: {len(bad)} problem(s) - nothing may be published" if bad else 0)
    D = json.load(gzip.open(a.data, "rt"))
    R = analyze(D, B=a.boot, P=a.boot)
    write_outputs(R, a.out)
    for k, v in R["verdicts"].items():
        print(f"[{k}] {v}")
    bad = scan(a.out)
    if bad:
        for b in bad[:50]:
            print("PRIVACY:", b)
        sys.exit(f"privacy gate: {len(bad)} problem(s) in {a.out}")


if __name__ == "__main__":
    main()
