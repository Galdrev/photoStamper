"""Revert guarding, tag-team reverting, talk-page voting blocs and their overlap with the coord network (aggregates only).

  python analyze_guard.py [--data data/guard/raw.json.gz] [--coord data/coord.json.gz] [--out patterns/guard]
  python analyze_guard.py --scan patterns/guard            -> publication privacy gate only (analyze_coord.privacy_scan)
  -> patterns/guard/results.json, cards.md, arbcom.md

Input: guard.py's raw file (full revision histories of the scoped topic and matched comparison articles, account names
already HMAC-hashed with the in-job salt; talk-page !votes with hashed signatures; lead critical-term counts for the
before / after state of sampled reverts; the redacted ArbCom extract) and coord.py's merged data from the SAME job (same
salt), from which the coord network edges are recomputed here (analyze_coord.Engine, topic/any, same seed as the coord run).

Reverts. Identity reverts: revision i whose sha1 equals that of a revision 2..15 back (and differs from i-1); the
revisions in between are reverted. Summary reverts: "Undid revision N" (the undone revision is reverted), "Restored
revision N", and remaining revert-like summaries / revert tags (the latest revision by another account is reverted).
Self-reverts (every reverted revision by the reverter) are dropped. Time to revert = revert time - time of the first
reverted revision. Direction of the reverted edit(s): lead critical-term count (analyze.CRITICAL, analyze.count on the
prose of section 0) after the last reverted revision vs before the first one: lower = the reverted edit REMOVED critical
terms; higher = ADDED them. Measured for a random sample of reverts since 2021-01-01 (as many as the time budget allowed).

Nulls. Q1 topic vs comparison: article-label permutation (1,000 draws); intervals: article (cluster) bootstrap (B=1,000).
Concentration (top-5 / top-10 share, Gini) is size dependent, so both groups are rarefied to the same number of reverts.
Direction within a group: direction labels permuted among measured reverts within article. Q2: reverter labels shuffled
among reverts in the same article and calendar month (500 draws). Q3: stances permuted among the voters of each
discussion (1,000 draws; 100 calibration worlds give the significant pairs / blocs expected by chance). Q4: random sets of
the same size from the same reverter population, matched on revert-count decile (1,000 draws).

Privacy: outputs carry no usernames, hashes, revids or URLs; every account count of 1 or 2 is written as "<3";
privacy_scan must pass before anything is written to the publication directory is pushed.
"""
import argparse, gzip, json, math, os, re, sys, time, zlib
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "patterns", "guard")
RAW = os.path.join(HERE, "data", "guard", "raw.json.gz")
COORD = os.path.join(HERE, "data", "coord.json.gz")
RADIUS = 15
LEAD_FROM = "2021-01-01T00:00:00Z"
FAST_H = 24.0
SEQ_W = (24, 72)
MIN_SHARED, P_EDGE, MIN_BLOC = 3, 0.01, 3
# rev tuple: [revid, ts, u, flags, sha, size, undo_idx, restore_idx]
F_ANON, F_BOT, F_RVSUM, F_RVTAG, F_HIDDEN = 1, 2, 4, 8, 16


def iso(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))


def ep(ts):
    return int(time.mktime(time.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S")) - time.timezone)


def sup(n):
    """Small-cell suppression for account counts: 1 or 2 accounts -> '<3'."""
    n = int(n)
    return "<3" if 0 < n < 3 else n


def r3(x, k=3):
    return None if x is None or (isinstance(x, float) and not math.isfinite(x)) else round(float(x), k)


def ci(a):
    a = np.asarray([x for x in a if x is not None and math.isfinite(x)], float)
    return [r3(np.percentile(a, 2.5)), r3(np.percentile(a, 97.5))] if len(a) else [None, None]


def pperm(obs, null, two=True):
    null = np.asarray([x for x in null if x is not None and math.isfinite(x)], float)
    if obs is None or not len(null):
        return None
    if two:
        c = np.mean(null)
        return r3((np.sum(np.abs(null - c) >= abs(obs - c) - 1e-12) + 1) / (len(null) + 1), 4)
    return r3((np.sum(null >= obs - 1e-12) + 1) / (len(null) + 1), 4)


# ------------------------------------------------------------------ reverts
def find_reverts(revs, radius=RADIUS):
    """revs: chronological list of rev tuples -> list of revert dicts (indices into revs; no names)."""
    out = []
    n = len(revs)
    for i in range(1, n):
        rid, ts, u, fl, sha, size, undo, rest = revs[i][:8]
        if fl & F_HIDDEN or (u is None):
            continue
        j = None
        if sha is not None and sha >= 0 and revs[i - 1][4] != sha:
            for k in range(i - 2, max(-1, i - radius - 1), -1):
                if revs[k][4] == sha:
                    j = k
                    break
        if j is not None:
            first, last, before, kind = j + 1, i - 1, j, "identity"
        elif undo is not None and 0 <= undo < i:
            first = last = undo; before, kind = undo - 1, "undo"
        elif rest is not None and 0 <= rest < i - 1:
            first, last, before, kind = rest + 1, i - 1, rest, "restore"
        elif fl & (F_RVSUM | F_RVTAG):
            k = i - 1
            while k >= 0 and revs[k][2] == u:
                k -= 1
            if k < 0:
                continue
            first = last = k; before, kind = k - 1, "summary"
        else:
            continue
        authors = {revs[k][2] for k in range(first, last + 1)}
        if authors <= {u}:
            continue                                   # self-revert
        tsha = revs[before][4] if before >= 0 else None
        out.append({"i": i, "t": ts, "t0": revs[first][1], "u": u, "anon": bool(fl & F_ANON), "bot": bool(fl & F_BOT),
                    "kind": kind, "target": tsha if (tsha is not None and tsha >= 0) else f"r{before}",
                    "before": revs[before][0] if before >= 0 else None, "after": revs[last][0],
                    "rev_anon": all(revs[k][3] & F_ANON for k in range(first, last + 1)),
                    "rev_authors": [a for a in authors if a is not None and a != u]})
    return out


def lead_direction(rv, leads):
    b, a = leads.get(str(rv["before"])) if rv["before"] else None, leads.get(str(rv["after"]))
    if b is None or a is None:
        return None
    return "remove" if a < b else "add" if a > b else "none"


def build(D):
    """-> per-article arrays and the flat revert table."""
    leads = D.get("leads") or {}
    rows = []
    arts = []
    for ai, a in enumerate(D["articles"]):
        revs = a.get("revs") or []
        arts.append({"title": a["title"], "group": a["group"], "tier": a.get("tier"), "n_revs": len(revs),
                     "truncated": a.get("truncated", False)})
        for rv in find_reverts(revs):
            rv["a"] = ai; rv["group"] = a["group"]
            rv["dt_h"] = max(0.0, (rv["t"] - rv["t0"]) / 3600.0)
            rv["human"] = not rv["anon"] and not rv["bot"]
            rv["ym"] = time.strftime("%Y-%m", time.gmtime(rv["t"]))
            rv["dir"] = lead_direction(rv, leads) if rv["t"] >= ep(LEAD_FROM) else None
            rv["in_window"] = rv["t"] >= ep(LEAD_FROM)
            rows.append(rv)
    return arts, rows


# ------------------------------------------------------------------ concentration
def gini(counts):
    x = np.sort(np.asarray(counts, float))
    x = x[x > 0]
    if len(x) < 2 or x.sum() == 0:
        return 0.0
    n = len(x)
    return float((2 * np.arange(1, n + 1) - n - 1).dot(x) / (n * x.sum()))


def conc_stats(ids, N, rng):
    """ids: int account codes; rarefied to N draws without replacement -> (top5 share, top10 share, gini)."""
    ids = np.asarray(ids)
    if N <= 0 or len(ids) == 0:
        return (None, None, None)
    if len(ids) > N:
        ids = rng.choice(ids, N, replace=False)
    c = np.bincount(ids)
    c = np.sort(c[c > 0])[::-1]
    tot = c.sum()
    return (float(c[:5].sum() / tot), float(c[:10].sum() / tot), gini(c))


def conc_point(ids, N, rng, reps=50):
    s = np.array([conc_stats(ids, N, rng) for _ in range(reps)], float)
    return s.mean(0) if len(s) else np.array([np.nan] * 3)


class Groups:
    """Reverts of one sample, split by article: dt (hours) and account code arrays; group label per article."""

    def __init__(self, rows, arts, code):
        self.na = len(arts)
        self.lab = np.array([a["group"] == "topic" for a in arts])
        by = defaultdict(list)
        for r in rows:
            by[r["a"]].append(r)
        self.dt = [np.array([r["dt_h"] for r in by[i]], float) for i in range(self.na)]
        self.acc = [np.array([code[r["u"]] for r in by[i]], np.int64) for i in range(self.na)]
        self.n = np.array([len(x) for x in self.dt])

    def cat(self, arr, sel):
        idx = np.where(sel)[0]
        return np.concatenate([arr[i] for i in idx]) if len(idx) else np.zeros(0)

    def stats(self, sel_t, sel_c, N, rng):
        dt_t, dt_c = self.cat(self.dt, sel_t), self.cat(self.dt, sel_c)
        ac_t, ac_c = self.cat(self.acc, sel_t).astype(np.int64), self.cat(self.acc, sel_c).astype(np.int64)
        mt = float(np.median(dt_t)) if len(dt_t) else np.nan
        mc = float(np.median(dt_c)) if len(dt_c) else np.nan
        ft = float(np.mean(dt_t <= FAST_H)) if len(dt_t) else np.nan
        fc = float(np.mean(dt_c <= FAST_H)) if len(dt_c) else np.nan
        n = min(N, len(ac_t), len(ac_c))
        ct, cc = conc_stats(ac_t, n, rng), conc_stats(ac_c, n, rng)
        return {"median_h": (mt, mc), "fast24": (ft, fc), "top5": (ct[0], cc[0]), "top10": (ct[1], cc[1]),
                "gini": (ct[2], cc[2])}


def compare_groups(rows, arts, rng, B=1000, P=1000, label="all"):
    """Topic vs comparison on one set of reverts: medians, fast share, rarefied concentration; bootstrap CI + permutation."""
    rows = [r for r in rows if r["human"]]
    code = {u: k for k, u in enumerate(sorted({r["u"] for r in rows}))}
    G = Groups(rows, arts, code)
    nt, nc = int(G.n[G.lab].sum()), int(G.n[~G.lab].sum())
    accts_t = len({r["u"] for r in rows if r["group"] == "topic"})
    accts_c = len({r["u"] for r in rows if r["group"] != "topic"})
    N = min(nt, nc)
    res = {"sample": label, "reverts_topic": nt, "reverts_comparison": nc, "articles_topic": int((G.lab & (G.n > 0)).sum()),
           "articles_comparison": int((~G.lab & (G.n > 0)).sum()), "reverting_accounts_topic": sup(accts_t),
           "reverting_accounts_comparison": sup(accts_c), "rarefied_to": N}
    if nt < 20 or nc < 20 or accts_t < 3 or accts_c < 3:
        res["note"] = "too few reverts or accounts in one group: not tested"
        return res
    # point estimates (concentration averaged over rarefactions)
    dt_t, dt_c = G.cat(G.dt, G.lab), G.cat(G.dt, ~G.lab)
    ac_t, ac_c = G.cat(G.acc, G.lab).astype(np.int64), G.cat(G.acc, ~G.lab).astype(np.int64)
    pt, pc = conc_point(ac_t, N, rng), conc_point(ac_c, N, rng)
    point = {"median_h": (float(np.median(dt_t)), float(np.median(dt_c))),
             "fast24": (float(np.mean(dt_t <= FAST_H)), float(np.mean(dt_c <= FAST_H))),
             "top5": (pt[0], pc[0]), "top10": (pt[1], pc[1]), "gini": (pt[2], pc[2])}
    boot = defaultdict(list)
    ti, cix = np.where(G.lab)[0], np.where(~G.lab)[0]
    for _ in range(B):
        bt = rng.choice(ti, len(ti)); bc = rng.choice(cix, len(cix))      # articles with replacement
        s = G_stats_multi(G, bt, bc, N, rng)
        for k, v in s.items():
            boot[k].append(v)
    perm = defaultdict(list)
    for _ in range(P):
        lab = rng.permutation(G.lab)
        s = G.stats(lab, ~lab, N, rng)
        for k, (a, b) in s.items():
            perm[k].append(None if a is None or b is None else a - b)
    for k, (a, b) in point.items():
        bb = boot[k]
        res[k] = {"topic": r3(a), "comparison": r3(b), "topic_ci95": ci([x[0] for x in bb]),
                  "comparison_ci95": ci([x[1] for x in bb]), "difference": r3(a - b),
                  "difference_ci95": ci([None if x[0] is None or x[1] is None else x[0] - x[1] for x in bb]),
                  "p_label_permutation": pperm(a - b, perm[k]),
                  "null_difference_mean": r3(np.nanmean([x for x in perm[k] if x is not None]))}
    return res


def G_stats_multi(G, bt, bc, N, rng):
    """Bootstrap replicate with articles drawn with replacement (bt / bc: article indices, repeats allowed)."""
    dt_t = np.concatenate([G.dt[i] for i in bt]) if len(bt) else np.zeros(0)
    dt_c = np.concatenate([G.dt[i] for i in bc]) if len(bc) else np.zeros(0)
    ac_t = np.concatenate([G.acc[i] for i in bt]).astype(np.int64) if len(bt) else np.zeros(0, np.int64)
    ac_c = np.concatenate([G.acc[i] for i in bc]).astype(np.int64) if len(bc) else np.zeros(0, np.int64)
    out = {}
    out["median_h"] = (float(np.median(dt_t)) if len(dt_t) else None, float(np.median(dt_c)) if len(dt_c) else None)
    out["fast24"] = (float(np.mean(dt_t <= FAST_H)) if len(dt_t) else None, float(np.mean(dt_c <= FAST_H)) if len(dt_c) else None)
    n = min(N, len(ac_t), len(ac_c))
    ct, cc = conc_stats(ac_t, n, rng), conc_stats(ac_c, n, rng)
    out["top5"], out["top10"], out["gini"] = (ct[0], cc[0]), (ct[1], cc[1]), (ct[2], cc[2])
    return out


def direction_test(rows, arts, group, rng, B=1000, P=1000):
    """Within one group: reverts of critical-term REMOVALS vs ADDITIONS (measured sample): time to revert, fast share,
    rarefied concentration. Null: direction labels permuted within article. CI: article bootstrap."""
    rr = [r for r in rows if r["human"] and r["group"] == group and r["dir"] in ("remove", "add")]
    code = {u: k for k, u in enumerate(sorted({r["u"] for r in rr}))}
    by = defaultdict(list)
    for r in rr:
        by[r["a"]].append(r)
    keys = sorted(by)
    dt = [np.array([r["dt_h"] for r in by[a]]) for a in keys]
    ac = [np.array([code[r["u"]] for r in by[a]], np.int64) for a in keys]
    rm = [np.array([r["dir"] == "remove" for r in by[a]]) for a in keys]
    nrem, nadd = sum(int(x.sum()) for x in rm), sum(int((~x).sum()) for x in rm)
    acc_rem = len({r["u"] for r in rr if r["dir"] == "remove"}); acc_add = len({r["u"] for r in rr if r["dir"] == "add"})
    res = {"group": group, "reverts_of_removals": nrem, "reverts_of_additions": nadd, "articles": len(keys),
           "accounts_reverting_removals": sup(acc_rem), "accounts_reverting_additions": sup(acc_add),
           "rarefied_to": min(nrem, nadd)}
    if nrem < 10 or nadd < 10 or acc_rem < 3 or acc_add < 3:
        res["note"] = "too few measured reverts or accounts in one direction: not tested"
        return res, None
    N = min(nrem, nadd)

    def stat(idx, masks, point=False):
        d = np.concatenate([dt[i] for i in idx]); a = np.concatenate([ac[i] for i in idx]); m = np.concatenate([masks[i] for i in idx])
        if m.sum() == 0 or (~m).sum() == 0:
            return None
        n = min(N, int(m.sum()), int((~m).sum()))
        cr = conc_point(a[m], n, rng, 30) if point else conc_stats(a[m], n, rng)
        ca = conc_point(a[~m], n, rng, 30) if point else conc_stats(a[~m], n, rng)
        return {"median_h": (float(np.median(d[m])), float(np.median(d[~m]))),
                "fast24": (float(np.mean(d[m] <= FAST_H)), float(np.mean(d[~m] <= FAST_H))),
                "top5": (cr[0], ca[0]), "top10": (cr[1], ca[1]), "gini": (cr[2], ca[2])}
    allidx = list(range(len(keys)))
    point = stat(allidx, rm, point=True)
    boot = defaultdict(list)
    for _ in range(B):
        s = stat(rng.choice(allidx, len(allidx)), rm)
        if s:
            for k, v in s.items():
                boot[k].append(v)
    perm = defaultdict(list)
    for _ in range(P):
        pm = [rng.permutation(x) for x in rm]
        s = stat(allidx, pm)
        if s:
            for k, (a, b) in s.items():
                perm[k].append(a - b)
    for k, (a, b) in point.items():
        res[k] = {"reverts_of_removals": r3(a), "reverts_of_additions": r3(b),
                  "removals_ci95": ci([x[0] for x in boot[k]]), "additions_ci95": ci([x[1] for x in boot[k]]),
                  "difference": r3(a - b), "difference_ci95": ci([x[0] - x[1] for x in boot[k]]),
                  "p_direction_permutation": pperm(a - b, perm[k])}
    return res, {k: [x[0] - x[1] for x in v] for k, v in boot.items()}


def q1(arts, rows, rng, B=1000, P=1000):
    leads_n = sum(1 for r in rows if r["in_window"])
    measured = [r for r in rows if r["dir"] is not None]
    out = {"definition": {"identity_radius": RADIUS, "fast_hours": FAST_H, "direction_window_from": LEAD_FROM[:10],
                          "concentration": "share of reverts by the 5 / 10 most active reverting accounts and Gini over "
                                           "reverting accounts, both groups rarefied to the same number of reverts",
                          "accounts": "registered, non-bot reverting accounts (IP / temporary accounts and bots are "
                                      "counted in the totals below but not in account statistics)"},
           "totals": {"reverts": len(rows), "reverts_by_bots": sum(r["bot"] for r in rows),
                      "reverts_by_ip_or_temp": sum(r["anon"] for r in rows),
                      "kinds": dict(Counter(r["kind"] for r in rows)),
                      "reverts_since_2021": leads_n, "direction_measured": len(measured),
                      "direction_measured_share_of_window": r3(len(measured) / leads_n) if leads_n else None,
                      "directions": {g: dict(Counter(r["dir"] for r in measured if r["group"] == g)) for g in ("topic", "comparison")}}}
    out["all_history"] = compare_groups(rows, arts, rng, B, P, "full history")
    out["since_2021"] = compare_groups([r for r in rows if r["in_window"]], arts, rng, B, P, "since 2021")
    out["by_direction_topic_vs_comparison"] = {}
    for d in ("remove", "add"):
        out["by_direction_topic_vs_comparison"][d] = compare_groups([r for r in measured if r["dir"] == d], arts, rng, B, P,
                                                                    f"reverts of critical-term {d}s")
    out["removal_vs_addition"] = {}
    boots = {}
    for g in ("topic", "comparison"):
        out["removal_vs_addition"][g], boots[g] = direction_test(rows, arts, g, rng, B, P)
    if boots.get("topic") and boots.get("comparison"):
        did = {}
        for k in boots["topic"]:
            a = out["removal_vs_addition"]["topic"][k]["difference"]; b = out["removal_vs_addition"]["comparison"][k]["difference"]
            m = min(len(boots["topic"][k]), len(boots["comparison"][k]))
            did[k] = {"difference_in_differences": r3(a - b),
                      "ci95": ci(np.array(boots["topic"][k][:m]) - np.array(boots["comparison"][k][:m]))}
        out["removal_vs_addition"]["topic_minus_comparison"] = did
    return out


# ------------------------------------------------------------------ Q2 tag teams
def chains(rows, W):
    """Label-free chains: per article and target version, reverts whose consecutive gaps are <= W hours (>=2 reverts)."""
    by = defaultdict(list)
    for k, r in enumerate(rows):
        by[(r["a"], r["target"])].append(k)
    out = []
    for key, ks in by.items():
        ks.sort(key=lambda k: rows[k]["t"])
        cur = [ks[0]]
        for k in ks[1:]:
            if rows[k]["t"] - rows[cur[-1]]["t"] <= W * 3600:
                cur.append(k)
            else:
                if len(cur) >= 2:
                    out.append(cur)
                cur = [k]
        if len(cur) >= 2:
            out.append(cur)
    return out


def seq_stats(ch, uarr, art):
    """-> sequences (chains with >=2 distinct accounts), pair -> set(articles)."""
    pairs = defaultdict(set)
    seqs = []
    for c in ch:
        us = sorted(set(int(uarr[k]) for k in c))
        if len(us) >= 2:
            seqs.append((c, us))
            a = art[c[0]]
            for x in range(len(us)):
                for y in range(x + 1, len(us)):
                    pairs[(us[x], us[y])].add(a)
    return seqs, pairs


def recur_summary(seqs, pairs, art):
    p3 = {p for p, s in pairs.items() if len(s) >= 3}
    p2 = {p for p, s in pairs.items() if len(s) >= 2}
    acc3 = {a for p in p3 for a in p}
    share = (sum(1 for c, us in seqs if any((us[x], us[y]) in p3 for x in range(len(us)) for y in range(x + 1, len(us))))
             / len(seqs)) if seqs else 0.0
    return {"pairs_2plus_articles": len(p2), "pairs_3plus_articles": len(p3), "accounts_in_3plus_pairs": len(acc3),
            "share_of_sequences_with_a_3plus_pair": share}


def components(pairs_set, min_size=3):
    import networkx as nx
    G = nx.Graph(); G.add_edges_from(pairs_set)
    return sorted([len(c) for c in nx.connected_components(G) if len(c) >= min_size], reverse=True)


def q2(arts, rows, rng, P=500, B=1000):
    res = {"definition": "a tag-team sequence = 2+ reverts toward the same version (same sha1 restored) of one article by "
                         "2+ different registered non-bot accounts, consecutive reverts no more than W hours apart",
           "null": "reverter labels shuffled among the reverts of the same article and calendar month (who reverts in that "
                   f"article-month is kept; who reverts toward which version is broken), {P} draws"}
    for W in SEQ_W:
        rr = [r for r in rows if r["human"]]
        code = {u: k for k, u in enumerate(sorted({r["u"] for r in rr}))}
        uarr = np.array([code[r["u"]] for r in rr], np.int64)
        art = np.array([r["a"] for r in rr], np.int64)
        lab_topic = np.array([arts[a]["group"] == "topic" for a in range(len(arts))])
        ch = chains(rr, W)
        seqs, pairs = seq_stats(ch, uarr, art)
        # per-article counts
        n_seq = np.zeros(len(arts)); n_rv = np.zeros(len(arts))
        for c, us in seqs:
            n_seq[art[c[0]]] += 1
        for a in art:
            n_rv[a] += 1
        ok = n_rv > 0
        def grp(sel):
            s, v = n_seq[sel & ok], n_rv[sel & ok]
            return (float(s.mean()) if len(s) else None, float(1000 * s.sum() / v.sum()) if v.sum() else None)
        (mt, rt), (mc, rc) = grp(lab_topic), grp(~lab_topic)
        bt, bc = np.where(lab_topic & ok)[0], np.where(~lab_topic & ok)[0]
        boot_m, boot_r = [], []
        for _ in range(B):
            x, y = rng.choice(bt, len(bt)), rng.choice(bc, len(bc))
            boot_m.append(n_seq[x].mean() - n_seq[y].mean())
            boot_r.append(1000 * n_seq[x].sum() / max(1, n_rv[x].sum()) - 1000 * n_seq[y].sum() / max(1, n_rv[y].sum()))
        perm_m, perm_r = [], []
        idx = np.where(ok)[0]
        for _ in range(1000):
            lab = lab_topic.copy(); lab[idx] = rng.permutation(lab_topic[idx])
            x, y = idx[lab[idx]], idx[~lab[idx]]
            perm_m.append(n_seq[x].mean() - n_seq[y].mean())
            perm_r.append(1000 * n_seq[x].sum() / max(1, n_rv[x].sum()) - 1000 * n_seq[y].sum() / max(1, n_rv[y].sum()))
        rec = {"sequences_topic": int(n_seq[lab_topic].sum()), "sequences_comparison": int(n_seq[~lab_topic].sum()),
               "per_article": {"topic": r3(mt), "comparison": r3(mc), "difference": r3(mt - mc) if mt is not None and mc is not None else None,
                               "difference_ci95": ci(boot_m), "p_label_permutation": pperm(mt - mc, perm_m) if mt is not None and mc is not None else None},
               "per_1000_reverts": {"topic": r3(rt), "comparison": r3(rc), "difference": r3(rt - rc) if rt is not None and rc is not None else None,
                                    "difference_ci95": ci(boot_r), "p_label_permutation": pperm(rt - rc, perm_r) if rt is not None and rc is not None else None}}
        # cross-article recurrence, per group, against the article-month shuffle
        groups_key = defaultdict(list)
        for k, r in enumerate(rr):
            groups_key[(r["a"], r["ym"])].append(k)
        gid = np.zeros(len(rr), np.int64)
        for k_, v in enumerate(groups_key.values()):
            gid[v] = k_
        order0 = np.argsort(gid, kind="stable")
        for g, sel in (("topic", True), ("comparison", False)):
            chg = [c for c in ch if lab_topic[art[c[0]]] == sel]
            sq, pr = seq_stats(chg, uarr, art)
            obs = recur_summary(sq, pr, art)
            nulls = defaultdict(list)
            null_counts = []                              # per draw: pair -> number of distinct articles
            for _ in range(P):
                u2 = np.empty_like(uarr)                  # labels permuted within article-month (vectorised)
                u2[order0] = uarr[np.lexsort((rng.random(len(uarr)), gid))]
                s2, p2 = seq_stats(chg, u2, art)
                for k, v in recur_summary(s2, p2, art).items():
                    nulls[k].append(v)
                nulls["sequences"].append(len(s2))
                null_counts.append({p: len(v) for p, v in p2.items() if len(v) >= 1})
            out = {"sequences": len(sq), "sequences_null_mean": r3(np.mean(nulls["sequences"]), 1),
                   "sequences_null_ci95": ci(nulls["sequences"])}
            for k, v in obs.items():
                vv = sup(v) if k == "accounts_in_3plus_pairs" else r3(v)
                out[k] = {"observed": vv, "null_mean": r3(np.mean(nulls[k])), "null_p95": r3(np.percentile(nulls[k], 95)),
                          "p_upper": pperm(v, nulls[k], two=False), "excess_over_null": r3(v - np.mean(nulls[k]))}
            # pair-level test: does THIS pair share sequences on more articles than it does once labels are shuffled?
            obs_c = {p: len(v) for p, v in pr.items()}
            sig = pair_significance(obs_c, null_counts)
            cal = pair_calibration(null_counts, K=min(100, P))
            sig_acc = {a for p in sig for a in p}
            comps = components(sig)
            out["significant_recurrent_pairs"] = {
                "rule": f"pair shares sequences on 3+ distinct articles and p<{P_EDGE} against that pair's own shuffle distribution",
                "observed": len(sig), "expected_by_chance_mean": r3(np.mean(cal), 2) if cal else None,
                "expected_p95": r3(np.percentile(cal, 95), 1) if cal else None, "accounts": sup(len(sig_acc)),
                "groups_3plus_accounts": {"count": len(comps), "sizes": comps}}
            rec[f"recurrence_{g}"] = out
            if g == "topic" and W == SEQ_W[0]:
                inv = {k: u for u, k in code.items()}
                res["_T"] = {inv[a] for a in sig_acc}
        res[f"W{W}h"] = rec
    return res


def pair_significance(obs_c, null_counts):
    n = len(null_counts)
    out = set()
    for p, c in obs_c.items():
        if c < 3:
            continue
        ge = sum(1 for d in null_counts if d.get(p, 0) >= c)
        if (ge + 1) / (n + 1) < P_EDGE:
            out.add(p)
    return out


def pair_calibration(null_counts, K=100):
    """Each of the first K shuffled worlds treated as observed, tested against the other draws -> significant pair counts."""
    n = len(null_counts)
    res = []
    for k in range(min(K, n)):
        c = 0
        for p, v in null_counts[k].items():
            if v < 3:
                continue
            ge = sum(1 for j, d in enumerate(null_counts) if j != k and d.get(p, 0) >= v)
            if (ge + 1) / n < P_EDGE:
                c += 1
        res.append(c)
    return res


# ------------------------------------------------------------------ Q3 voting blocs
def vote_matrix(discs, group):
    """-> voters (hashes), discussions (list of [(voter idx, stance code)]) restricted to voters with >=3 votes in the
    group and discussions with >=3 such voters."""
    dd = [d for d in discs if d["group"] == group]
    cnt = Counter(v[0] for d in dd for v in d["votes"])
    keep = {u for u, c in cnt.items() if c >= MIN_SHARED}
    voters = sorted(keep)
    vi = {u: k for k, u in enumerate(voters)}
    out = []
    for d in dd:
        vs = [(vi[u], s) for u, s in d["votes"] if u in vi]
        if len(vs) >= 3:
            codes = {s: k for k, s in enumerate(sorted({s for _, s in vs}))}
            out.append(([a for a, _ in vs], [codes[s] for _, s in vs], d["kind"]))
    return voters, out


def agreement_null(voters, D, rng, n=1000, K=100):
    """Pairs with >= MIN_SHARED shared discussions: observed agreements, null matrix (n x pairs) from within-discussion
    stance permutation."""
    inc = defaultdict(list)                         # pair -> list of (disc, pos_i, pos_j)
    for di, (vs, ss, _) in enumerate(D):
        for x in range(len(vs)):
            for y in range(x + 1, len(vs)):
                a, b = vs[x], vs[y]
                key = (a, b) if a < b else (b, a)
                inc[key].append((di, x, y))
    pairs = [p for p, l in inc.items() if len(l) >= MIN_SHARED]
    if not pairs:
        return pairs, np.zeros(0), np.zeros(0), np.zeros((0, 0))
    off = np.concatenate([[0], np.cumsum([len(D[d][0]) for d in range(len(D))])])
    flat_s = np.concatenate([np.array(ss) for _, ss, _ in D])
    pid, gi, gj = [], [], []
    for k, p in enumerate(pairs):
        for di, x, y in inc[p]:
            pid.append(k); gi.append(off[di] + x); gj.append(off[di] + y)
    pid, gi, gj = np.array(pid), np.array(gi), np.array(gj)
    shared = np.bincount(pid, minlength=len(pairs))
    obs = np.bincount(pid, weights=(flat_s[gi] == flat_s[gj]), minlength=len(pairs))
    segs = [np.arange(off[d], off[d + 1]) for d in range(len(D))]
    N = np.zeros((n, len(pairs)), np.int16)
    for s in range(n):
        perm = flat_s.copy()
        for sg in segs:
            perm[sg] = flat_s[rng.permutation(sg)]
        N[s] = np.bincount(pid, weights=(perm[gi] == perm[gj]), minlength=len(pairs))
    return pairs, shared, obs, N


def sig_edges(obs, N, exclude=None):
    """p = (1 + #null >= obs) / (n + 1); for a calibration world `exclude` = its own row."""
    n = N.shape[0] - (1 if exclude is not None else 0)
    ge = (N >= obs[None, :]).sum(0) - (1 if exclude is not None else 0)
    p = (ge + 1) / (n + 1)
    return (p < P_EDGE) & (obs >= MIN_SHARED), p


def communities(pairs, mask, weights=None):
    import networkx as nx
    G = nx.Graph()
    for k in np.where(mask)[0]:
        G.add_edge(pairs[k][0], pairs[k][1], weight=1.0 if weights is None else float(weights[k]))
    if not len(G):
        return []
    return [c for c in nx.community.louvain_communities(G, weight="weight", seed=11) if len(c) >= MIN_BLOC]


def q3_group(discs, group, rng, n=1000, K=100):
    voters, D = vote_matrix(discs, group)
    res = {"group": group, "discussions_with_3plus_regular_voters": len(D),
           "discussion_kinds": dict(Counter(k for _, _, k in D)), "regular_voters": sup(len(voters))}
    pairs, shared, obs, N = agreement_null(voters, D, rng, n, K)
    res["pairs_with_3plus_shared_discussions"] = len(pairs)
    if len(pairs) < 3:
        res["note"] = "too few voter pairs with 3+ shared discussions: not tested"
        return res, voters, pairs, None, []
    mask, p = sig_edges(obs, N)
    rate = obs / shared
    nrate = N / shared[None, :]
    # calibration: each of the first K null draws treated as observed
    cal_e, cal_b, cal_hi = [], [], []
    for k in range(min(K, n)):
        m, _ = sig_edges(N[k].astype(float), N, exclude=k)
        cal_e.append(int(m.sum())); cal_b.append(len(communities(pairs, m)))
    for k in range(n):
        cal_hi.append(float(np.mean(nrate[k] >= 0.8)))
    comms = communities(pairs, mask, -np.log10(p))
    pidx = {pp: k for k, pp in enumerate(pairs)}
    blocs = []
    for c in sorted(comms, key=len, reverse=True):
        mem = sorted(c)
        ks = [pidx[(a, b)] for i, a in enumerate(mem) for b in mem[i + 1:] if (a, b) in pidx]
        o = float(obs[ks].sum() / shared[ks].sum()) if ks else None
        nl = (N[:, ks].sum(1) / shared[ks].sum()) if ks else np.zeros(1)
        blocs.append({"size": len(c), "within_bloc_agreement": r3(o), "null_mean": r3(nl.mean()), "null_ci95": ci(nl),
                      "p_upper": pperm(o, nl, two=False) if o is not None else None})
    res.update({
        "significant_agreement_pairs": {"observed": int(mask.sum()), "expected_by_chance_mean": r3(np.mean(cal_e), 2),
                                         "expected_p95": r3(np.percentile(cal_e, 95), 1), "calibration_worlds": len(cal_e)},
        "share_of_pairs_agreeing_80pct_plus": {"observed": r3(np.mean(rate >= 0.8)), "null_mean": r3(np.mean(cal_hi)),
                                                "null_ci95": ci(cal_hi), "p_upper": pperm(float(np.mean(rate >= 0.8)), cal_hi, two=False)},
        "mean_pair_agreement": {"observed": r3(rate.mean()), "null_mean": r3(nrate.mean())},
        "blocs": {"count": len(blocs), "sizes": [b["size"] for b in blocs], "expected_by_chance_mean": r3(np.mean(cal_b), 2),
                  "expected_p95": r3(np.percentile(cal_b, 95), 1), "detail": blocs}})
    return res, voters, pairs, mask, comms


def q3(discs, rng, coord_edges, n=1000, K=100):
    out = {"definition": "!votes (support / oppose / include / exclude / keep / delete / option X...) in RfC, requested-move "
                         "and AfD discussions on the talk pages (and archives) of the scoped articles; one stance per "
                         "account per discussion; accounts with 3+ votes in the group, discussions with 3+ such voters",
           "null": f"stances permuted among the voters of each discussion, {n} draws; significant pair: p<{P_EDGE} and 3+ "
                   f"agreements; blocs: Louvain on significant pairs, 3+ accounts; {K} calibration worlds"}
    extra = {}
    for g in ("topic", "comparison"):
        r, voters, pairs, mask, comms = q3_group(discs, g, rng, n, K)
        out[g] = r
        extra[g] = (voters, pairs, mask, comms)
    # overlap with coord edges (topic)
    voters, pairs, mask, comms = extra["topic"]
    ov = {"coord_edges": len(coord_edges)}
    if coord_edges is not None and mask is not None:
        vi = {u: k for k, u in enumerate(voters)}
        pidx = {p: k for k, p in enumerate(pairs)}
        elig = []
        for a, b in coord_edges:
            if a in vi and b in vi:
                x, y = sorted((vi[a], vi[b]))
                if (x, y) in pidx:
                    elig.append(pidx[(x, y)])
        q = float(mask.mean()) if len(mask) else 0.0
        hit = int(sum(mask[k] for k in elig))
        coord_acc = {u for e in coord_edges for u in e}
        acc_vote = [u for u in coord_acc if u in vi]
        bloc_mem = {voters[i] for c in comms for i in c}
        acc_bloc = [u for u in acc_vote if u in bloc_mem]
        exp_b = len(acc_vote) * (len(bloc_mem) / len(voters)) if voters else 0
        nb = []
        for _ in range(1000):
            s = rng.choice(len(voters), size=min(len(acc_vote), len(voters)), replace=False) if voters else []
            nb.append(sum(1 for i in s if voters[i] in bloc_mem))
        ov.update({"coord_edges_that_are_voting_pairs_with_3plus_shared": sup(len(elig)),
                   "of_which_significant_agreement_pairs": sup(hit),
                   "expected_significant_by_chance": r3(len(elig) * q, 2),
                   "coord_accounts_among_regular_voters": sup(len(acc_vote)),
                   "coord_accounts_in_voting_blocs": sup(len(acc_bloc)),
                   "expected_in_blocs_by_chance": r3(exp_b, 2), "expected_p95": r3(np.percentile(nb, 95), 1) if nb else None,
                   "p_upper": pperm(len(acc_bloc), nb, two=False) if nb else None})
    out["overlap_with_coord_edges"] = ov
    return out, extra


# ------------------------------------------------------------------ Q4 overlap
def q4(rows, coord_edges, vote_extra, q2_sets, rng, n=1000):
    """Fast reverters of critical-term removals (topic) vs coord-edge accounts, voting-bloc members, recurrent tag-team
    accounts: overlap counts against random reverter sets matched on revert-count decile."""
    rr = [r for r in rows if r["human"] and r["group"] == "topic"]
    cnt = Counter(r["u"] for r in rr)
    out = {"definition": f"fast reverter = registered non-bot account with 2+ reverts, within {int(FAST_H)} h, of topic-"
                         "article edits that removed (or, as contrast, added) lead critical terms (measured sample since 2021)",
           "null": f"{n} random sets of the same size from all registered topic reverters, matched on revert-count decile"}
    if not rr:
        out["note"] = "no topic reverts"
        return out
    pop = sorted(cnt)
    dec = np.digitize([cnt[u] for u in pop], np.percentile([cnt[u] for u in pop], np.arange(10, 100, 10)))
    by_dec = defaultdict(list)
    for u, d in zip(pop, dec):
        by_dec[int(d)].append(u)
    udec = {u: int(d) for u, d in zip(pop, dec)}
    C = {u for e in (coord_edges or []) for u in e}
    voters, pairs, mask, comms = vote_extra.get("topic", (None, None, None, []))
    V = {voters[i] for c in (comms or []) for i in c} if voters else set()
    T = q2_sets or set()
    for d in ("remove", "add"):
        fc = Counter(r["u"] for r in rr if r["dir"] == d and r["dt_h"] <= FAST_H)
        F = sorted(u for u, c in fc.items() if c >= 2)
        rec = {"fast_reverters": sup(len(F))}
        if len(F) < 3:
            rec["note"] = "fewer than 3 fast reverters: overlaps suppressed"
            out[d] = rec
            continue
        for name, S in (("coord_edge_accounts", C), ("voting_bloc_members", V), ("recurrent_tag_team_accounts", T)):
            obs = len(set(F) & S)
            null = []
            for _ in range(n):
                draw = set()
                for u in F:
                    pool = by_dec[udec[u]]
                    draw.add(pool[int(rng.integers(len(pool)))])
                null.append(len(draw & S))
            rec[name] = {"set_size": sup(len(S)), "overlap": sup(obs), "expected_mean": r3(np.mean(null), 2),
                         "expected_p95": r3(np.percentile(null, 95), 1), "p_upper": pperm(obs, null, two=False)}
        out[d] = rec
    return out


# ------------------------------------------------------------------ coord edges (recomputed in-job, same salt)
def coord_edges(path, log=print, n_null=1000):
    """-> (list of hash pairs, meta). Same events, scope and seed as the coord run's topic/any network."""
    if not path or not os.path.exists(path):
        return None, {"available": False}
    import analyze_coord as AC
    D = json.load(gzip.open(path, "rt"))
    ev, _ = AC.build_events(D)
    sub = [e for e in ev if e["group"] == "topic"]
    E = AC.Engine(sub, "topic/any", n_null, 0, seed=7 + zlib.crc32(b"topic/any") % 1000).run(log)
    ed = [(E.accs[pid // E.NA], E.accs[pid % E.NA]) for _, pid, _ in E.edges("network")]
    summ = D.get("summary") or {}
    return ed, {"available": True, "edges": len(ed), "accounts": sup(len({u for e in ed for u in e})),
                "articles_collected": summ.get("n_articles"), "articles_expected": summ.get("n_articles_expected"),
                "complete": bool(summ.get("n_articles") and summ.get("n_articles_expected") and
                                 summ["n_articles"] >= 0.95 * summ["n_articles_expected"])}


# ------------------------------------------------------------------ ArbCom extraction (redaction happens here, in-job)
KEYWORDS = re.compile(r"off-?wiki|coordinat|canvass|discord|e-?mail|mailing list|\bproxy|proxying|meat-?pupp|whatsapp|"
                      r"telegram|tech for palestine|private (?:channel|group|forum)", re.I)
NAME_LINK = re.compile(r"\[\[\s*:?\s*(?:User|User talk|Special:Contributions|Special:Contribs)\s*:\s*([^\]|#/\n]+)", re.I)
NAME_TPL = re.compile(r"\{\{\s*(userlinks|user|u|admin|ping|noping|user5|userlinks-abuse|checkuser|np|user2|reply to|"
                      r"replyto|re|yo|user-multi|vandal|sockpuppeteer|unsigned|unsigned2)\s*\|([^{}]*)\}\}", re.I)
PROPER = {w.lower() for w in """Israel Israeli Israelis Palestine Palestinian Palestinians Gaza Hamas Hezbollah Arab Arabs
    Jewish Jews Zionism Zionist Zionists Discord WhatsApp Telegram Signal Twitter Reddit Facebook Wikipedia Wikipedians
    Wikimedia Foundation WMF English ArbCom Arbitration Committee Committee's Clerk Clerks PIA ARBPIA ARBECR CTOP CT AE ANI
    AN RfC RfCs RFC CheckUser CheckUsers Oversight Oversighters UTC January February March April May June July August
    September October November December Monday Tuesday Wednesday Thursday Friday Saturday Sunday Tech For Editor
    I II III IV V Arab-Israeli Israeli-Palestinian Palestine-Israel Middle East West Bank Jerusalem Lebanon Syria Iran
    Egypt Jordan United States Nations UN Nakba Holocaust Mandatory Ottoman British Britain US UK EU Wikiproject WikiProject
    Electronic Intifada Mondoweiss Forward Haaretz Times Guardian Jewish Journal Pirate Wires Standard""".split()}
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
DATE_RX = re.compile(r"\b(\d{1,2}) (" + MONTHS + r") (\d{4})\b")
SIDE_RX = [("pro-Israel", re.compile(r"pro-?Israel\w*|anti-?Palestin\w*", re.I)),
           ("pro-Palestinian", re.compile(r"pro-?Palestin\w*|anti-?Israel\w*", re.I))]
REMEDY_TYPES = [("site ban", r"site[- ]?ban"), ("topic ban", r"topic[- ]?ban"), ("interaction ban", r"interaction[- ]?ban"),
                ("desysop", r"desysop|administrative (?:tools|privileges|permissions) (?:are )?(?:removed|revoked)"),
                ("admonishment", r"admonish"), ("warning / reminder", r"\bwarned\b|\breminded\b|\bwarning\b"),
                ("editing restriction", r"restrict|word limit|\b1RR\b|balanced editing|limited to"),
                ("extended-confirmed restriction", r"extended[- ]confirmed|\bECR\b"),
                ("referral / review", r"referr|request for comment|\bRfC\b|review")]


def _norm_name(s):
    s = re.sub(r"[_\s]+", " ", s).strip().strip("'\"").strip()
    return (s[:1].upper() + s[1:]) if s else s


def collect_names(texts):
    names = []
    for t in texts:
        for m in NAME_LINK.finditer(t):
            names.append(_norm_name(m.group(1)))
        for m in NAME_TPL.finditer(t):
            for part in m.group(2).split("|"):
                if "=" in part or not part.strip():
                    continue
                names.append(_norm_name(part))
        # party lists: bullet lines in an "involved parties" / "parties" section
        for sec in re.finditer(r"^=+\s*(?:Involved )?parties\s*=+\s*$(.*?)(?=^=+[^=])", t, re.I | re.M | re.S):
            for line in sec.group(1).splitlines():
                m = re.match(r"^\*+\s*(?:\[\[[^\]]*\|)?([^\[\]{}|\n]{2,60}?)(?:\]\])?\s*(?:\(|$)", line)
                if m and not line.strip().startswith("*{{"):
                    names.append(_norm_name(m.group(1)))
    out, seen = [], set()
    for n in names:
        if n and len(n) >= 2 and n.lower() not in seen and not re.fullmatch(r"\d+", n):
            seen.add(n.lower()); out.append(n)
    return out


def redactor(names):
    order = {n: k + 1 for k, n in enumerate(names)}
    pats = []
    for n in sorted(names, key=len, reverse=True):
        alts = {re.escape(n), re.escape(n.replace(" ", "_")), re.escape(n[:1].lower() + n[1:])}
        pats.append((re.compile(r"(?<![\w])(?:" + "|".join(sorted(alts, key=len, reverse=True)) + r")(?![\w])", re.I),
                     f"Editor {order[n]}"))
    def red(s):
        for rx, rep in pats:
            s = rx.sub(rep, s)
        return s
    return red


def plain(wt):
    t = re.sub(r"<!--.*?-->", "", wt, flags=re.S)
    t = re.sub(r"<ref[^>]*?/>|<ref[^>]*>.*?</ref>", "", t, flags=re.S | re.I)
    t = re.sub(r"\{\{\s*(?:userlinks|user|u|admin|ping|noping|user5|np|re|yo)\s*\|([^|{}]*)[^{}]*\}\}", r"\1", t, flags=re.I)
    t = re.sub(r"\{\{[^{}]*\}\}", "", t)
    t = re.sub(r"\{\{[^{}]*\}\}", "", t)
    t = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"\[https?://\S+\s*([^\]]*)\]", r"\1", t)
    t = re.sub(r"https?://\S+", "", t)
    t = re.sub(r"'{2,}", "", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"\b\d{7,}\b", "", t)
    t = re.sub(r"(?<![\w.])(?=[0-9]*[a-f])[0-9a-f]{10,}(?![\w.])", "", t, flags=re.I)
    t = re.sub(r"(?i)oldid=|diff=|index\.php|special:|curid=|action=compare", "", t)
    return re.sub(r"\s+", " ", t).strip()


def _tok_ok(tok, ordinary):
    t = tok.strip(".,;:()[]\"'!?").replace("’", "'")
    t = re.sub(r"'s$", "", t)
    if not t or re.fullmatch(r"\d{1,6}", t) or re.fullmatch(r"Editor|\d+", t):
        return True
    parts = re.split(r"[-/]", t)
    return all((p.lower() in ordinary or p.lower() in PROPER or re.fullmatch(r"\d{1,6}", p) or p == "") for p in parts)


def scrub(s, ordinary):
    """Backstop after exact-name redaction: any token that is not an ordinary lowercase word of these pages or an allowed
    proper noun (and is capitalised, contains digits, or is camel-case) is replaced by [redacted]."""
    out = []
    for tok in s.split(" "):
        if re.fullmatch(r"Editor|\d+[.,;:)]*", tok) or _tok_ok(tok, ordinary):
            out.append(tok)
        elif tok[:1].isupper() or re.search(r"\d", tok) or re.search(r"[a-z][A-Z]", tok) or "_" in tok:
            out.append("[redacted]")
        else:
            out.append(tok)
    return " ".join(out)


def heading_ok(h, ordinary):
    h2 = re.sub(r"Editor \d+", "", h)
    return all(_tok_ok(t, ordinary) for t in h2.split())


def _sections(text):
    """-> list of (level, heading, body, parents)."""
    hs = list(re.finditer(r"^(={2,5})\s*(.*?)\s*\1\s*$", text, re.M))
    out, stack = [], []
    for k, m in enumerate(hs):
        lvl = len(m.group(1)); body = text[m.end(): hs[k + 1].start() if k + 1 < len(hs) else len(text)]
        stack = [s for s in stack if s[0] < lvl]
        out.append((lvl, m.group(2), body, [s[1] for s in stack]))
        stack.append((lvl, m.group(2)))
    return out


def _first_body(body):
    lines = []
    for ln in body.splitlines():
        s = ln.strip()
        if re.match(r"^(?::*\s*)?'*\s*(Support|Oppose|Abstain|Comments?|Passed|Enacted)\b", s, re.I) or s.startswith("#") \
                or s.startswith("{{ACMajority") or s.startswith(":Support"):
            break
        lines.append(ln)
    return "\n".join(lines)


def arbcom_extract(pages):
    """pages: {label: raw wikitext or None}. Redacts every name collected from User: links, user templates and party
    lists on ALL pages, then extracts findings of fact / remedies that mention off-wiki coordination, canvassing, Discord,
    email lists or proxying. Returns only redacted titles, dates, short quotes, remedy type and side."""
    texts = [t for t in pages.values() if t]
    names = collect_names(texts)
    red = redactor(names)
    red_pages = {k: red(v) if v else None for k, v in pages.items()}
    corpus = " ".join(plain(t) for t in red_pages.values() if t)
    wc = Counter(re.findall(r"(?<![A-Za-z0-9_])[a-z][a-z']*(?![A-Za-z0-9_])", corpus))   # words used in lower case
    ordinary = {w.strip("'") for w, c in wc.items() if c >= 2}
    items, dropped = [], 0
    page_meta = {}
    for label, t in red_pages.items():
        if not t:
            page_meta[label] = {"found": False}
            continue
        ds = [(int(d), m, int(y)) for d, m, y in DATE_RX.findall(t)]
        key = lambda x: (x[2], MONTHS.split("|").index(x[1]), x[0])
        page_meta[label] = {"found": True, "earliest_date": "%d %s %d" % min(ds, key=key) if ds else None,
                            "latest_date": "%d %s %d" % max(ds, key=key) if ds else None}
        for lvl, head, body, parents in _sections(t):
            ctx = " / ".join(parents + [head]).lower()
            if "finding" in ctx and "fact" in ctx and "principle" not in head.lower():
                kind = "finding of fact"
            elif "remed" in ctx and "enforcement" not in head.lower():
                kind = "remedy"
            else:
                continue
            if re.search(r"finding|remed|principle|proposed|final decision|enforcement", head, re.I) and lvl <= 3 and \
                    not KEYWORDS.search(head):
                continue                                           # container heading, not an item
            txt = plain(_first_body(body))
            if not txt or not (KEYWORDS.search(txt) or KEYWORDS.search(head)):
                continue
            title = plain(head)
            if not heading_ok(title, ordinary):
                title = "(heading withheld: may contain an unredacted name)"; dropped += 1
            ds2 = [(int(d), m, int(y)) for d, m, y in DATE_RX.findall(body)]
            date = "%d %s %d" % min(ds2, key=key) if ds2 else page_meta[label]["latest_date"]
            q = scrub(txt, ordinary)
            if len(q) > 320:
                q = q[:320].rsplit(" ", 1)[0] + " ..."
            sides = [s for s, rx in SIDE_RX if rx.search(txt)]
            rtype = None
            if kind == "remedy":
                rtype = next((n for n, rx in REMEDY_TYPES if re.search(rx, txt, re.I)), "other")
            items.append({"page": label, "kind": kind, "source": "proposed decision (may not have passed)"
                          if "proposed" in label.lower() else "case page (final decision)", "title": title, "date": date,
                          "quote": q, "remedy_type": rtype, "side": sides or "not stated in the text",
                          "keywords": sorted({m.group(0).lower() for m in KEYWORDS.finditer(txt)})})
    # final safety: no collected name may survive anywhere in the items
    blob = json.dumps(items, ensure_ascii=False).lower()
    leaks = sum(1 for n in names if len(n) >= 4 and re.search(r"(?<![\w])" + re.escape(n.lower()) + r"(?![\w])", blob))
    if leaks:
        items = [{**it, "quote": "(withheld: redaction check failed)", "title": "(heading withheld)"} for it in items]
    return {"pages": page_meta, "items": items, "editors_redacted": len(names), "headings_withheld": dropped,
            "redaction_leak_check": "passed" if not leaks else f"failed on {leaks} name(s): all quotes withheld"}


# ------------------------------------------------------------------ run + outputs
def analyze(D, coord_path=COORD, seed=11, B=1000, P=1000, n_vote=1000, K=100, log=print):
    rng = np.random.default_rng(seed)
    arts, rows = build(D)
    log(f"guard: {len(arts)} articles, {len(rows)} reverts")
    ce, cmeta = coord_edges(coord_path, log)
    R = {"meta": {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                  "articles": dict(Counter(a["group"] for a in arts)),
                  "articles_by_tier": {g: dict(Counter(a["tier"] for a in arts if a["group"] == g)) for g in ("topic", "comparison")},
                  "revisions_thousands": {g: r3(sum(a["n_revs"] for a in arts if a["group"] == g) / 1000, 1) for g in ("topic", "comparison")},
                  "histories_truncated": sum(1 for a in arts if a["truncated"]),
                  "collection": D.get("summary"), "coord_recomputed": cmeta,
                  "bootstrap": B, "permutations": P, "vote_null_draws": n_vote, "calibration_worlds": K}}
    log("guard: Q1"); R["q1_revert_guarding"] = q1(arts, rows, rng, B, P)
    log("guard: Q2"); R["q2_tag_team"] = q2(arts, rows, rng, P=min(P, 500), B=B)
    T = R["q2_tag_team"].pop("_T", set())     # accounts in significant recurrent pairs (Q4 only; never written)
    log("guard: Q3"); R["q3_voting_blocs"], extra = q3(D.get("discussions") or [], rng, ce or [], n_vote, K)
    log("guard: Q4"); R["q4_overlap"] = q4(rows, ce, extra, T, rng)
    R["arbcom"] = D.get("arbcom")
    R["verdicts"] = verdicts(R)
    return R


def _sig(d, key="p_label_permutation"):
    return d is not None and d.get(key) is not None and d[key] < 0.01


def verdicts(R):
    v = {}
    q1 = R["q1_revert_guarding"]
    rt = (q1.get("removal_vs_addition") or {}).get("topic") or {}
    did = (q1.get("removal_vs_addition") or {}).get("topic_minus_comparison") or {}
    faster = rt.get("median_h") and rt["median_h"]["difference"] is not None and rt["median_h"]["difference"] < 0 and \
        _sig(rt["median_h"], "p_direction_permutation")
    conc = rt.get("top10") and rt["top10"]["difference"] is not None and rt["top10"]["difference"] > 0 and \
        _sig(rt["top10"], "p_direction_permutation")
    did_ok = did.get("median_h") and did["median_h"]["ci95"][1] is not None and did["median_h"]["ci95"][1] < 0
    if "note" in rt:
        v["q1"] = "inconclusive: too few measured reverts of critical-term changes"
    elif faster and conc and did_ok:
        v["q1"] = "supports organised guarding: removals of critical terms are reverted faster and by fewer accounts, beyond the direction null and beyond the comparison articles"
    elif faster or conc:
        v["q1"] = "inconclusive: one guarding signature (speed or concentration) beyond chance, not both"
    else:
        v["q1"] = "no evidence: removals and additions of critical terms are reverted at similar speed and concentration"
    q2 = R["q2_tag_team"].get("W24h", {})
    rc = (q2.get("recurrence_topic") or {}).get("significant_recurrent_pairs") or {}
    rcc = (q2.get("recurrence_comparison") or {}).get("significant_recurrent_pairs") or {}
    ex_t = (rc.get("observed") or 0) - (rc.get("expected_by_chance_mean") or 0)
    ex_c = (rcc.get("observed") or 0) - (rcc.get("expected_by_chance_mean") or 0)
    if rc.get("observed", 0) > (rc.get("expected_p95") or 0) and rc.get("observed", 0) >= 3 and ex_t > ex_c:
        v["q2"] = "supports organised guarding: more pairs recur in tag-team sequences across articles than the article-month shuffle produces, and more than on comparison articles"
    elif rc.get("observed", 0) > (rc.get("expected_p95") or 0):
        v["q2"] = "inconclusive: recurrent pairs above the shuffle null, but few or not above the comparison articles"
    else:
        v["q2"] = "no evidence: recurrent tag-team pairs are what the label shuffle produces"
    q3 = R["q3_voting_blocs"].get("topic") or {}
    if "note" in q3 or not q3.get("blocs"):
        v["q3"] = "inconclusive: too few voting pairs"
    else:
        b = q3["blocs"]; s = q3["significant_agreement_pairs"]
        if b["count"] > (b["expected_p95"] or 0) and s["observed"] > (s["expected_p95"] or 0):
            v["q3"] = "supports organised guarding: more high-agreement pairs and voting blocs than the stance permutation produces"
        elif s["observed"] > (s["expected_p95"] or 0):
            v["q3"] = "inconclusive: more high-agreement pairs than chance, but no more blocs than chance"
        else:
            v["q3"] = "no evidence: co-vote agreement is what the stance permutation produces"
    q4 = R["q4_overlap"].get("remove") or {}
    hits = [k for k in ("coord_edge_accounts", "voting_bloc_members", "recurrent_tag_team_accounts")
            if isinstance(q4.get(k), dict) and q4[k].get("p_upper") is not None and q4[k]["p_upper"] < 0.01]
    if "note" in q4 or not q4:
        v["q4"] = "inconclusive: too few fast reverters of critical-term removals"
    elif hits:
        v["q4"] = "supports organised guarding: fast reverters of critical-term removals overlap " + ", ".join(hits) + " beyond matched random sets"
    else:
        v["q4"] = "no evidence: overlaps are within what matched random reverter sets give"
    ab = R.get("arbcom") or {}
    v["q5"] = (f"primary source: {len(ab.get('items') or [])} findings / remedies mention off-wiki coordination, canvassing, "
               "Discord, email or proxying (see arbcom.md)") if ab else "not collected"
    return v


def fmt(x):
    if isinstance(x, list):
        return "[" + ", ".join(fmt(y) for y in x) + "]"
    if isinstance(x, float):
        return f"{x:g}"
    return str(x)


def render_cards(R):
    L = [f"# Revert guarding, tag teams and voting blocs (aggregate only)", "",
         f"Generated {R['meta']['generated']}. No usernames, account hashes or revision ids appear here; account counts of "
         "1-2 are shown as <3. Each card gives the observed value, what the comparison articles or the null model give, "
         "and a one-line verdict.", "",
         f"Scope: {R['meta']['articles']} articles ({R['meta']['articles_by_tier']}); revisions (thousands) "
         f"{R['meta']['revisions_thousands']}; coord network recomputed in the same job: {R['meta']['coord_recomputed']}.", ""]
    q1 = R["q1_revert_guarding"]
    L += ["## 1. Revert guarding", "", f"Totals: {q1['totals']}", ""]
    for key in ("all_history", "since_2021"):
        c = q1[key]
        L.append(f"**Topic vs comparison, {c['sample']}** ({c['reverts_topic']} vs {c['reverts_comparison']} reverts by "
                 f"registered accounts; concentration rarefied to {c['rarefied_to']}).")
        for k in ("median_h", "fast24", "top5", "top10", "gini"):
            if k in c:
                d = c[k]
                L.append(f"- {k}: topic {fmt(d['topic'])} {fmt(d['topic_ci95'])} vs comparison {fmt(d['comparison'])} "
                         f"{fmt(d['comparison_ci95'])}; difference {fmt(d['difference'])} {fmt(d['difference_ci95'])}, "
                         f"label-permutation p {fmt(d['p_label_permutation'])}")
        if "note" in c:
            L.append(f"- {c['note']}")
        L.append("")
    for g in ("topic", "comparison"):
        c = q1["removal_vs_addition"].get(g) or {}
        L.append(f"**Reverts of critical-term removals vs additions, {g} articles** ({c.get('reverts_of_removals')} vs "
                 f"{c.get('reverts_of_additions')} measured reverts; accounts {c.get('accounts_reverting_removals')} vs "
                 f"{c.get('accounts_reverting_additions')}).")
        for k in ("median_h", "fast24", "top5", "top10", "gini"):
            if k in c:
                d = c[k]
                L.append(f"- {k}: removals {fmt(d['reverts_of_removals'])} {fmt(d['removals_ci95'])} vs additions "
                         f"{fmt(d['reverts_of_additions'])} {fmt(d['additions_ci95'])}; difference {fmt(d['difference'])} "
                         f"{fmt(d['difference_ci95'])}, direction-permutation p {fmt(d['p_direction_permutation'])}")
        if "note" in c:
            L.append(f"- {c['note']}")
        L.append("")
    did = q1["removal_vs_addition"].get("topic_minus_comparison")
    if did:
        L.append("**Difference in differences (topic minus comparison, removal minus addition):** " +
                 "; ".join(f"{k} {fmt(v['difference_in_differences'])} {fmt(v['ci95'])}" for k, v in did.items()))
        L.append("")
    L += [f"**Verdict:** {R['verdicts']['q1']}", ""]
    q2 = R["q2_tag_team"]
    L += ["## 2. Tag-team reverting", "", q2["definition"] + ". Null: " + q2["null"] + ".", ""]
    for W in SEQ_W:
        c = q2[f"W{W}h"]
        L.append(f"**Window {W} h.** Sequences: topic {c['sequences_topic']}, comparison {c['sequences_comparison']}. "
                 f"Per article: {c['per_article']}. Per 1,000 reverts: {c['per_1000_reverts']}.")
        for g in ("topic", "comparison"):
            r = c[f"recurrence_{g}"]
            L.append(f"- {g}: sequences {r['sequences']} (shuffle {r['sequences_null_mean']}); pairs on 3+ articles "
                     f"{r['pairs_3plus_articles']}; pairs on 2+ articles {r['pairs_2plus_articles']}; accounts in 3+-article "
                     f"pairs {r['accounts_in_3plus_pairs']}; pairs recurring beyond their own shuffle distribution "
                     f"{r['significant_recurrent_pairs']}")
        L.append("")
    L += [f"**Verdict:** {R['verdicts']['q2']}", ""]
    q3 = R["q3_voting_blocs"]
    L += ["## 3. Voting blocs on talk pages", "", q3["definition"] + ". Null: " + q3["null"] + ".", ""]
    for g in ("topic", "comparison"):
        c = q3[g]
        L.append(f"**{g}:** {json.dumps({k: v for k, v in c.items() if k != 'group'}, ensure_ascii=False)}")
        L.append("")
    L += [f"**Overlap with the recomputed coord edges:** {q3['overlap_with_coord_edges']}", "",
          f"**Verdict:** {R['verdicts']['q3']}", ""]
    L += ["## 4. Are the fast reverters the same accounts?", "", R["q4_overlap"].get("definition", ""), "",
          f"{json.dumps({k: v for k, v in R['q4_overlap'].items() if k not in ('definition',)}, ensure_ascii=False)}", "",
          f"**Verdict:** {R['verdicts']['q4']}", ""]
    L += ["## 5. ArbCom primary source", "", f"See arbcom.md. {R['verdicts']['q5']}", ""]
    return "\n".join(L)


def render_arbcom(ab):
    L = ["# ArbCom primary source: off-wiki coordination findings and remedies (redacted)", "",
         "Raw wikitext (action=raw) of the Palestine-Israel articles 4 and 5 case pages, the PIA5 proposed decision and "
         "evidence pages, fetched and processed inside the workflow job. Every username found in User: links, user "
         "templates or party lists on any of these pages was replaced by \"Editor N\" before extraction; any remaining "
         "capitalised token that is not an ordinary word on these pages or an allowed proper noun is shown as "
         "[redacted]; headings that may still contain a name are withheld. Items are those whose text mentions off-wiki "
         "coordination, canvassing, Discord, email, proxying or similar.", ""]
    if not ab:
        return "\n".join(L + ["Not collected."])
    L.append(f"Editors redacted: {ab['editors_redacted']}. Headings withheld: {ab['headings_withheld']}. Redaction leak "
             f"check: {ab['redaction_leak_check']}.")
    L.append("")
    L.append("| Page | Found | Earliest date | Latest date |")
    L.append("|---|---|---|---|")
    for k, v in ab["pages"].items():
        L.append(f"| {k} | {v.get('found')} | {v.get('earliest_date') or ''} | {v.get('latest_date') or ''} |")
    L.append("")
    for it in ab["items"]:
        L += [f"### {it['title']}", "",
              f"- Kind: {it['kind']}; source: {it['source']} ({it['page']}); date: {it['date']}",
              f"- Remedy type: {it['remedy_type'] or 'n/a (finding)'}; side: {it['side'] if isinstance(it['side'], str) else ', '.join(it['side'])}",
              f"- Mentions: {', '.join(it['keywords'])}", f"- Quote (redacted): \"{it['quote']}\"", ""]
    return "\n".join(L)


def write_outputs(R, out_dir=OUT):
    os.makedirs(out_dir, exist_ok=True)
    json.dump(R, open(os.path.join(out_dir, "results.json"), "w"), indent=1, ensure_ascii=False, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    open(os.path.join(out_dir, "cards.md"), "w").write(render_cards(R))
    open(os.path.join(out_dir, "arbcom.md"), "w").write(render_arbcom(R.get("arbcom")))


def scan(path):
    import analyze_coord as AC
    return AC.privacy_scan(path, [os.environ.get("WT_SALT", "")])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan")
    ap.add_argument("--data", default=RAW)
    ap.add_argument("--coord", default=COORD)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--boot", type=int, default=int(os.environ.get("GUARD_BOOT", "1000")))
    ap.add_argument("--perm", type=int, default=int(os.environ.get("GUARD_PERM", "1000")))
    a = ap.parse_args()
    if a.scan:
        bad = scan(a.scan)
        for b in bad[:50]:
            print("PRIVACY:", b)
        sys.exit(f"privacy gate: {len(bad)} problem(s) - nothing may be published" if bad else 0)
    D = json.load(gzip.open(a.data, "rt"))
    R = analyze(D, a.coord, B=a.boot, P=a.perm)
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
