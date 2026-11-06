"""Coordinated-editing analysis on the merged coord collector output (data/coord.json.gz).

  python analyze_coord.py [--data data/coord.json.gz] [--null 1000] [--calib 50]
  -> patterns/coord/cards.md, cards.json, chart_data/{network.json, blocs.json, sync.json, sweeps.json, profiles.json,
     windows.json, calibration.json}

Unit: one event = (revision, direction) of a critical-term insertion or removal by a registered, non-bot, visible account.
Two nulls, 1,000 draws each, per scope (topic / comparison) and direction (any / insert / remove):
  shared   account x article bipartite graph (binary), degree-preserving rewiring (curveball trades; every account keeps its
           number of articles, every article its number of accounts). Statistic: articles shared by a pair.
  time     every account's whole timeline shifted by one random offset of 1-7 days, either sign (keeps who edits which
           article, each account's rhythm, sprees and rough news week; breaks minute-level alignment between
           accounts). Statistic: distinct article pairs (a != b) on which the two accounts acted within W minutes,
           W = 10 / 30 (default) / 60. A second time null permutes timestamps among the events of the same article (each
           article keeps its activity curve) and is reported as p_article_shuffle. It has little power when a bloc makes up
           most of an article's events (the shuffle then swaps the bloc's own timestamps), so it is a robustness check, not
           the edge rule.
Edge: empirical p < 0.01 AND observed count >= 3, on the 30-minute window or on shared articles. Communities: Louvain on the
significant-edge graph (Louvain weight = -log10 p, as in the calibration worlds; the edge
'weight' field is log2 lift). Blocs (card a) use shared-article edges only.
Selection is calibrated: the whole pipeline (edges -> communities) is re-run on CALIB null worlds (each null draw treated
as if observed, p-values from the other draws), giving the edges / communities expected by chance and, per community, the
share of null worlds producing a community at least as large and as dense.
Card (e) tests every significant bloc / community (insert-direction and remove-direction blocs separately) against the
documented coordination windows (ORGS.md: email canvassing Oct 2023-Jan 2024, TfP Discord Jan-Sep 2024) and the sanction
dates (~9 Dec 2024, 25 Apr 2025), against matched random account sets.
Outputs never contain usernames or hashes: accounts are A1, A2... (network) and blocs "Bloc A (n accounts)".
"""
import argparse, gzip, json, math, os, re, sys, time, zlib
from collections import Counter, defaultdict
from datetime import datetime, timezone

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "patterns", "coord")
DATA = os.path.join(HERE, "data", "coord.json.gz")
WINDOWS = {"t10": 600, "t30": 1800, "t60": 3600}
DEFAULT_W = "t30"
P_EDGE, MIN_OBS, MIN_BLOC = 0.01, 3, 3
GAP = 10            # curveball draws are a thinned Markov chain: calibration worlds skip draws within 10 steps
SWEEP_MIN_ARTICLES, JACCARD = 5, 0.7
NAKBA = re.compile(r"\bnakba\b|1948 palestin\w* (?:exodus|expulsion)|depopulat\w*|expel+ed|expulsion", re.I)


# Documented coordination windows and sanction dates (patterns/orgs/ORGS.md; snippets, verify before publication).
DOC_WINDOWS = {
    "email_canvassing": ("2023-10-01", "2024-01-21", "ArbCom 'PIA canvassing' motions, 4-20 Jan 2024: email canvassing and proxying "
                         "for a banned editor (pro-Israel), dated from about Oct 2023"),
    "tfp_discord": ("2024-01-01", "2024-10-01", "Tech for Palestine Discord Wikipedia channel: created Jan 2024, public until about "
                    "Sep 2024; ArbCom sanctioned editing after off-wiki canvassing requests there (Dec 2024)"),
}
SANCTIONS = {"2024-12-09": "ArbCom private-case sanctions for off-wiki canvassing (date approximate, ~9 Dec 2024)",
             "2025-04-25": "ArbCom site bans on further off-wiki coordination evidence"}
DROP_WINDOW_D = 365


def iso(t):
    return datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d") if t is not None else None


def ep(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()


def norm_words(s):
    return re.findall(r"[a-z0-9]+", s.lower().replace("–", " ").replace("—", " "))


def shingles(s, k=5):
    w = norm_words(s)
    if len(w) < k:
        return {" ".join(w)} if w else set()
    return {" ".join(w[i:i + k]) for i in range(len(w) - k + 1)}


def nlp(p, n):
    """-log10 p capped at the resolution of n null draws (observed and calibration worlds then share one scale)."""
    return min(-math.log10(p), math.log10(n))


def bloc_name(i):
    s, i = "", i + 1
    while i:
        i, r = divmod(i - 1, 26); s = chr(65 + r) + s
    return s


# ------------------------------------------------------------------ events
def build_events(D):
    """-> list of event dicts (registered, visible, non-bot accounts only), plus counts of what was excluded."""
    arts = D["articles"]
    ev, excl = [], Counter()
    for r in D["revisions"]:
        if r.get("state") != "ok":
            excl["missing_or_deleted"] += 1; continue
        if r.get("user_hidden") or not r.get("u"):
            excl["user_hidden"] += 1; continue
        if r.get("anon"):
            excl["anon"] += 1; continue
        if r.get("bot"):
            excl["bot"] += 1; continue
        if not r.get("ts"):
            excl["no_ts"] += 1; continue
        g = (arts.get(r["title"]) or {}).get("group")
        for kind in sorted({e["kind"] for e in r["events"]}):
            ev.append({"u": r["u"], "title": r["title"], "group": g, "t": ep(r["ts"]), "kind": kind, "revid": r["revid"],
                       "terms": sorted({e["term"] for e in r["events"] if e["kind"] == kind}), "age_d": r.get("age_d"),
                       "village": bool((arts.get(r["title"]) or {}).get("village"))})
    return ev, excl


# ------------------------------------------------------------------ nulls
def curveball(rows, n, rng, thin=None, burn=None):
    """Degree-preserving bipartite rewiring (Strona et al. 2014). rows: list of sets. Yields flat int arrays (fixed row order)."""
    rows = [set(r) for r in rows]
    live = [i for i, r in enumerate(rows) if r]
    thin = thin or max(150, 3 * len(live))
    burn = burn if burn is not None else 5 * thin
    def trades(k):
        if len(live) < 2:
            return
        ii = rng.integers(0, len(live), size=(k, 2))
        for a, b in ii:
            if a == b:
                continue
            A, B = rows[live[a]], rows[live[b]]
            ao, bo = A - B, B - A
            if not ao or not bo:
                continue
            pool = list(ao | bo); rng.shuffle(pool)
            na = len(ao)
            A -= ao; B -= bo
            A.update(pool[:na]); B.update(pool[na:])
    trades(burn)
    for _ in range(n):
        trades(thin)
        yield np.fromiter((x for r in rows for x in sorted(r)), dtype=np.int32, count=sum(len(r) for r in rows))


def time_pairs(t, acc, art, kinds=None, wmax=3600, NA=None, NM=None):
    """Cross-article co-activity: for each window, sorted unique pair ids and counts of distinct article pairs."""
    n = len(t)
    out = {}
    if n < 2:
        return {w: (np.zeros(0, np.int64), np.zeros(0, np.int64)) for w in WINDOWS}
    o = np.argsort(t, kind="stable")
    ts, ac, ar = t[o], acc[o], art[o]
    je = np.searchsorted(ts, ts + wmax, side="right")
    cnt = je - np.arange(n) - 1
    tot = int(cnt.sum())
    if tot == 0:
        return {w: (np.zeros(0, np.int64), np.zeros(0, np.int64)) for w in WINDOWS}
    I = np.repeat(np.arange(n), cnt)
    starts = np.cumsum(cnt) - cnt
    J = np.arange(tot) - np.repeat(starts, cnt) + I + 1
    m = (ac[I] != ac[J]) & (ar[I] != ar[J])
    I, J = I[m], J[m]
    dt = ts[J] - ts[I]
    sw = ac[I] > ac[J]
    lo = np.where(sw, ac[J], ac[I]).astype(np.int64); hi = np.where(sw, ac[I], ac[J]).astype(np.int64)
    alo = np.where(sw, ar[J], ar[I]).astype(np.int64); ahi = np.where(sw, ar[I], ar[J]).astype(np.int64)
    pid = lo * NA + hi
    key = pid * (NM * NM) + alo * NM + ahi
    for w, sec in WINDOWS.items():
        k = np.unique(key[dt <= sec])
        p, c = np.unique(k // (NM * NM), return_counts=True)
        out[w] = (p, c)
    return out


def lookup(keys, vals, q):
    if len(keys) == 0 or len(q) == 0:
        return np.zeros(len(q), np.int64)
    idx = np.clip(np.searchsorted(keys, q), 0, len(keys) - 1)
    return np.where(keys[idx] == q, vals[idx], 0)


# ------------------------------------------------------------------ engine
class Engine:
    """One scope x direction: observed stats, 1,000-draw nulls, calibration worlds, significant edges."""

    def __init__(self, events, name, n_null=1000, n_calib=50, seed=7):
        self.name, self.n, self.K = name, n_null, n_calib
        self.rng = np.random.default_rng(seed)
        self.ev = events
        self.accs = sorted({e["u"] for e in events})
        self.arts = sorted({e["title"] for e in events})
        self.ai = {u: i for i, u in enumerate(self.accs)}
        self.mi = {a: i for i, a in enumerate(self.arts)}
        self.NA, self.NM = max(1, len(self.accs)), max(1, len(self.arts))
        self.t = np.array([e["t"] for e in events], float)
        self.acc = np.array([self.ai[e["u"]] for e in events], np.int64)
        self.art = np.array([self.mi[e["title"]] for e in events], np.int64)
        self.kind = np.array([e["kind"] == "insert" for e in events], bool)
        rows = [set() for _ in self.accs]
        for a, m in zip(self.acc, self.art):
            rows[a].add(int(m))
        self.rows = rows
        self.deg = np.array([len(r) for r in rows])
        self.off = np.concatenate([[0], np.cumsum(self.deg)]).astype(np.int64)
        self.Kacc = np.where(self.deg >= MIN_OBS)[0]
        self.kpos = -np.ones(self.NA, np.int64); self.kpos[self.Kacc] = np.arange(len(self.Kacc))
        self.posK = np.concatenate([np.arange(self.off[a], self.off[a + 1]) for a in self.Kacc]) if len(self.Kacc) else np.zeros(0, np.int64)
        self.rowK = np.repeat(np.arange(len(self.Kacc)), self.deg[self.Kacc]) if len(self.Kacc) else np.zeros(0, np.int64)
        self.flat_obs = np.fromiter((x for r in rows for x in sorted(r)), dtype=np.int32, count=int(self.deg.sum()))

    # ---- statistics of one world
    def shared_matrix(self, flat):
        A = np.zeros((len(self.Kacc), self.NM), np.float32)
        if len(self.Kacc):
            A[self.rowK, flat[self.posK]] = 1
        return A @ A.T

    def shared_pairs(self, C):
        iu = np.triu_indices(len(self.Kacc), 1)
        v = C[iu]
        m = v >= MIN_OBS
        a, b = self.Kacc[iu[0][m]], self.Kacc[iu[1][m]]
        lo, hi = np.minimum(a, b), np.maximum(a, b)
        return lo.astype(np.int64) * self.NA + hi, v[m].astype(np.int64)

    def tstats(self, t):
        return time_pairs(t, self.acc, self.art, NA=self.NA, NM=self.NM)

    def dayshift_t(self):
        """Primary time null: each account's whole timeline shifted by one random offset of 1-7 days (either sign, continuous).
        Keeps who edits which article and each account's own rhythm and sprees; breaks minute-level alignment between
        accounts (two accounts keep their alignment only if their offsets agree within the window: ~W / 12 days)."""
        k = self.rng.uniform(1, 7, size=self.NA) * self.rng.choice([-1, 1], size=self.NA)
        return self.t + 86400.0 * k[self.acc]

    def shuffle_t(self):
        base = np.argsort(self.art, kind="stable")
        order = np.lexsort((self.rng.random(len(self.t)), self.art))
        t2 = np.empty_like(self.t); t2[base] = self.t[order]
        return t2

    def shared_vals(self, C, pids):
        lo, hi = pids // self.NA, pids % self.NA
        a, b = self.kpos[lo], self.kpos[hi]
        ok = (a >= 0) & (b >= 0)
        v = np.zeros(len(pids), np.int64)
        if ok.any():
            v[ok] = C[a[ok], b[ok]].astype(np.int64)
        return v

    # ---- full run
    def run(self, log=print):
        t0 = time.time()
        n, K = self.n, self.K
        flats = list(curveball(self.rows, n, self.rng)) if len(self.accs) > 1 else [self.flat_obs] * n
        shuf = [self.dayshift_t() for _ in range(n)]       # primary time null (edges, calibration)
        jit = [self.shuffle_t() for _ in range(n)]         # secondary: timestamps permuted within article
        stats = ["shared"] + list(WINDOWS)
        # worlds: 0 = observed, 1..K = null draws 0..K-1 treated as observed (calibration)
        worlds = []
        for w in range(K + 1):
            if w == 0:
                C, ts = self.shared_matrix(self.flat_obs), self.tstats(self.t)
            else:
                C, ts = self.shared_matrix(flats[w - 1]), self.tstats(shuf[w - 1])
            d = {"shared": self.shared_pairs(C)}
            for k in WINDOWS:
                p, c = ts[k]; m = c >= MIN_OBS
                d[k] = (p[m], c[m])
            worlds.append({s: {"pid": d[s][0], "obs": d[s][1], "exc": np.zeros(len(d[s][0]), np.int64)} for s in stats})
        self.obs_C, self.obs_t = self.shared_matrix(self.flat_obs), self.tstats(self.t)
        # observed pairs: every pair with >= MIN_OBS on any stat; keep all their null values for mean / p95
        o_p = np.unique(np.concatenate([worlds[0][s]["pid"] for s in stats])) if any(len(worlds[0][s]["pid"]) for s in stats) \
            else np.zeros(0, np.int64)
        self.o_p = o_p
        self.o_obs = {"shared": self.shared_vals(self.obs_C, o_p)}
        for k in WINDOWS:
            self.o_obs[k] = lookup(*self.obs_t[k], o_p)
        tj = ["j" + k[1:] for k in WINDOWS]
        self.o_null = {s: np.zeros((n, len(o_p)), np.int32) for s in stats + tj}
        for s in range(n):
            C = self.shared_matrix(flats[s])
            ts, tjs = self.tstats(shuf[s]), self.tstats(jit[s])
            sv = {"shared": lambda q: self.shared_vals(C, q)}
            for k in WINDOWS:
                sv[k] = (lambda kk: (lambda q: lookup(*ts[kk], q)))(k)
            for w, W in enumerate(worlds):
                if w >= 1 and abs(w - 1 - s) <= GAP:       # a calibration world is not compared with its chain neighbours
                    continue
                for st in stats:
                    if len(W[st]["pid"]):
                        W[st]["exc"] += sv[st](W[st]["pid"]) >= W[st]["obs"]
            for st in stats:
                self.o_null[st][s] = sv[st](o_p)
            for k, jk in zip(WINDOWS, tj):
                self.o_null[jk][s] = lookup(*tjs[k], o_p)
        self.worlds, self.flats, self.shuf, self.jit = worlds, flats, shuf, jit
        # calibration: pipeline on each null world
        self.calib = []
        for w in range(1, K + 1):
            ne = n - sum(1 for s in range(n) if abs(w - 1 - s) <= GAP)
            net = self._world_edges(worlds[w], ne, rule="network")
            blc = self._world_edges(worlds[w], ne, rule="bloc")
            self.calib.append({"network": self._communities_of(net), "bloc": self._communities_of(blc),
                               "n_edges_network": len(net), "n_edges_bloc": len(blc),
                               "n_edges_sync": len(self._world_edges(worlds[w], ne, rule="sync"))})
        log(f"  [{self.name}] {len(self.accs)} accounts, {len(self.arts)} articles, {len(self.ev)} events, "
            f"{len(o_p)} candidate pairs, {time.time() - t0:.0f}s")
        return self

    def _world_edges(self, W, n_eff, rule):
        """-> {pid: weight} for one world under the edge rule."""
        st = {"network": ["shared", DEFAULT_W], "bloc": ["shared"], "sync": ["t10"]}[rule]
        out = {}
        for s in st:
            d = W[s]
            if not len(d["pid"]):
                continue
            p = (d["exc"] + 1) / (n_eff + 1)
            m = (p < P_EDGE) & (d["obs"] >= MIN_OBS)
            for pid, o, pp in zip(d["pid"][m], d["obs"][m], p[m]):
                out[int(pid)] = max(out.get(int(pid), 0), nlp(pp, self.n))
        return out

    def _communities_of(self, edges):
        import networkx as nx
        if not edges:
            return []
        G = nx.Graph()
        for pid, w in edges.items():
            G.add_edge(pid // self.NA, pid % self.NA, weight=w)
        out = []
        for c in nx.community.louvain_communities(G, weight="weight", seed=11):
            if len(c) >= MIN_BLOC:
                sub = G.subgraph(c)
                ws = [d["weight"] for _, _, d in sub.edges(data=True)]
                out.append({"size": len(c), "density": 2 * sub.number_of_edges() / (len(c) * (len(c) - 1)),
                            "strength": float(np.mean(ws)) if ws else 0.0, "members": sorted(c)})
        return out

    # ---- observed edges with full fields
    def pval(self, s, i):
        return (int((self.o_null[s][:, i] >= self.o_obs[s if s[0] != "j" else "t" + s[1:]][i]).sum()) + 1) / (self.n + 1)

    def edges(self, rule):
        st = {"network": ["shared", DEFAULT_W], "bloc": ["shared"], "sync": ["t10"]}[rule]
        res = []
        for i, pid in enumerate(self.o_p):
            sig = [s for s in st if self.o_obs[s][i] >= MIN_OBS and self.pval(s, i) < P_EDGE]
            if sig:
                res.append((i, int(pid), sig))
        return res

    def pair_stats(self, i):
        d = {}
        for s in ["shared"] + list(WINDOWS):
            nv = self.o_null[s][:, i]
            d[s] = {"observed": int(self.o_obs[s][i]), "null_mean": round(float(nv.mean()), 3),
                    "null_p95": float(np.percentile(nv, 95)), "p": round(self.pval(s, i), 4)}
            if s in WINDOWS:
                d[s]["p_article_shuffle"] = round(self.pval("j" + s[1:], i), 4)
        return d

    def pair_detail(self, a, b, window=WINDOWS[DEFAULT_W]):
        """Same-direction share, example article pairs and time span of a pair's co-activity (observed data)."""
        ia, ib = np.where(self.acc == a)[0], np.where(self.acc == b)[0]
        ex, same, tot, tt = Counter(), 0, 0, []
        for x in ia:
            dt = np.abs(self.t[ib] - self.t[x])
            for y in ib[(dt <= window) & (self.art[ib] != self.art[x])]:
                tot += 1; same += self.kind[x] == self.kind[y]
                ex[tuple(sorted((self.arts[self.art[x]], self.arts[self.art[y]])))] += 1
                tt += [self.t[x], self.t[y]]
        shared = self.rows[a] & self.rows[b]
        if not tot and shared:
            for m in shared:
                ka = self.kind[ia[self.art[ia] == m]].mean() >= 0.5
                kb = self.kind[ib[self.art[ib] == m]].mean() >= 0.5
                tot += 1; same += ka == kb
            tt = list(self.t[ia[np.isin(self.art[ia], list(shared))]]) + list(self.t[ib[np.isin(self.art[ib], list(shared))]])
        return {"same_direction_share": round(same / tot, 3) if tot else None,
                "example_article_pairs": [list(k) for k, _ in ex.most_common(3)],
                "shared_articles_examples": sorted(self.arts[m] for m in shared)[:5],
                "time_span": [iso(min(tt)), iso(max(tt))] if tt else None}

    # ---- fixed-set tests (pass C)
    def set_test(self, members):
        """Null comparison for one account set: articles touched by >=3 members (rewiring), member co-activity sum over
        article pairs within 30 / 60 min (day-shift null, article-shuffle null)."""
        S = sorted(members)
        def t3(rows_of):
            c = Counter(m for a in S for m in rows_of(a))
            return sum(1 for v in c.values() if v >= MIN_BLOC)
        o3 = t3(lambda a: self.rows[a])
        n3 = np.array([t3(lambda a, f=f: f[self.off[a]:self.off[a + 1]].tolist()) for f in self.flats])
        msk = np.isin(self.acc, S)
        def tsum(t, w):
            if msk.sum() < 2:
                return 0
            r = time_pairs(t[msk], self.acc[msk], self.art[msk], NA=self.NA, NM=self.NM)
            return int(r[w][1].sum())
        out = {"articles_3plus": {"observed": o3, "null_mean": round(float(n3.mean()), 3), "null_p95": float(np.percentile(n3, 95)),
                                  "p": round((int((n3 >= o3).sum()) + 1) / (self.n + 1), 4)}}
        for w in ("t30", "t60"):
            o = tsum(self.t, w)
            ns = np.array([tsum(x, w) for x in self.shuf]); nj = np.array([tsum(x, w) for x in self.jit])
            out[f"sync_{w}"] = {"observed": o, "null_mean": round(float(ns.mean()), 3), "null_p95": float(np.percentile(ns, 95)),
                                "p": round((int((ns >= o).sum()) + 1) / (self.n + 1), 4),
                                "article_shuffle_null_mean": round(float(nj.mean()), 3),
                                "p_article_shuffle": round((int((nj >= o).sum()) + 1) / (self.n + 1), 4)}
        return out

    def calib_share(self, rule, size, density, strength):
        """Share of null worlds whose pipeline produced a community at least this large and at least this dense, where
        density = (share of member pairs joined by a significant edge) x (mean capped -log10 p of those edges)."""
        sc = density * strength
        k = [any(c["size"] >= size and c["density"] * c["strength"] >= sc - 1e-9 for c in w[rule]) for w in self.calib]
        return round(sum(k) / len(k), 4) if k else None

    def calib_counts(self, rule):
        e = [w[f"n_edges_{rule}"] for w in self.calib]
        c = [len(w[rule]) for w in self.calib] if rule != "sync" else None
        return {"null_worlds": len(self.calib), "edges_mean": round(float(np.mean(e)), 2) if e else None,
                "edges_p95": round(float(np.percentile(e, 95)), 1) if e else None,
                **({"communities_mean": round(float(np.mean(c)), 2), "communities_p95": round(float(np.percentile(c, 95)), 1),
                    "communities_max": int(max(c))} if c else {})}


# ------------------------------------------------------------------ communities / blocs (observed)
def confidence(set_p, calib_share, sync_p=None):
    """The calibration share is the selection-aware test (the fixed-set p ignores that the set was picked from the data).
    Six scope x direction tests run, so the thresholds are strict:
    high: <=0.5% of null worlds (whole pipeline re-run) give a community this large and dense, the fixed-set null is beaten at
    p<=0.002 and the members are also synchronous (p<0.01). medium: <=1% of null worlds, fixed-set p<=0.01 (structure only:
    on six noise-only synthetic datasets x 6 tests, one 3-account group reached medium, i.e. roughly 1 per 36 tests)."""
    if calib_share is None:
        return "low"
    if set_p <= 0.002 and calib_share <= 0.005 and (sync_p is None or sync_p < 0.01):
        return "high"
    if set_p <= 0.01 and calib_share <= 0.01:
        return "medium"
    return "low"


def community_summary(E, members, edges_w, ev_by_acc, D, lp=None):
    import itertools
    S = sorted(members)
    evs = [e for a in S for e in ev_by_acc[a]]
    arts = Counter(e["title"] for e in evs)
    ins = sum(e["kind"] == "insert" for e in evs)
    ts = [e["t"] for e in evs]
    months = Counter(iso(t)[:7] for t in ts)
    sub = [edges_w[p] for p in (min(a, b) * E.NA + max(a, b) for a, b in itertools.combinations(S, 2)) if p in edges_w]
    dens = 2 * len(sub) / (len(S) * (len(S) - 1))
    lps = [lp[p] for p in (min(a, b) * E.NA + max(a, b) for a, b in itertools.combinations(S, 2)) if lp and p in lp]
    # inserted phrases: shingles of members' inserted sentences, counted over distinct articles
    revset = {(e["revid"]) for e in evs if e["kind"] == "insert"}
    sh = defaultdict(set)
    for r in D["revisions"]:
        if r["revid"] in revset:
            for x in r.get("added") or []:
                for z in shingles(x["s"]):
                    sh[z].add(r["title"])
    top = sorted(((len(v), z) for z, v in sh.items() if len(v) >= 2), reverse=True)[:5]
    return {"size": len(S), "density": round(dens, 3), "strength": round(float(np.mean(lps)), 3) if lps else 0.0,
            "n_articles": len(arts),
            "articles": [{"title": a, "events": c} for a, c in arts.most_common(10)],
            "direction": {"insert": ins, "remove": len(evs) - ins, "insert_share": round(ins / len(evs), 3) if evs else None},
            "active": {"first": iso(min(ts)), "last": iso(max(ts)), "busiest_month": months.most_common(1)[0][0] if months else None,
                       "events": len(evs)},
            "inserted_phrases": [{"shingle": f"“{z}”", "articles": n} for n, z in top]}


def age_bucket(d):
    if d is None:
        return "unknown"
    return "<30d" if d < 30 else "30d-1y" if d < 365 else "1-5y" if d < 1825 else ">5y"


def network(E, D, ev_by_acc, log=print):
    import networkx as nx
    edges = E.edges("network")
    ew, lp, recs = {}, {}, []
    for i, pid, sig in edges:
        ps = E.pair_stats(i)
        main = DEFAULT_W if DEFAULT_W in sig else "shared"
        m = ps[main]
        w = math.log2((m["observed"] + 1) / (m["null_mean"] + 1))
        ew[pid] = w
        lp[pid] = max(nlp(ps[s]["p"], E.n) for s in sig)
        recs.append((pid, sig, ps, main, w))
    G = nx.Graph()
    for pid, sig, ps, main, w in recs:
        G.add_edge(pid // E.NA, pid % E.NA, weight=lp[pid])      # same weighting as the calibration worlds
    comms = sorted(nx.community.louvain_communities(G, weight="weight", seed=11), key=lambda c: -len(c)) if len(G) else []
    cid = {a: k for k, c in enumerate(comms) for a in c}
    order = sorted(G.nodes, key=lambda a: (cid[a], -len(ev_by_acc[a])))
    lab = {a: f"A{k + 1}" for k, a in enumerate(order)}
    nodes = []
    for a in order:
        evs = ev_by_acc[a]
        first = min(evs, key=lambda e: e["t"])
        nodes.append({"id": lab[a], "insert_share": round(sum(e["kind"] == "insert" for e in evs) / len(evs), 3),
                      "events": len(evs), "articles": len({e["title"] for e in evs}), "community": cid[a],
                      "age_bucket": age_bucket(first.get("age_d"))})
    out_edges = []
    for pid, sig, ps, main, w in recs:
        a, b = pid // E.NA, pid % E.NA
        det = E.pair_detail(a, b)
        m = ps[main]
        out_edges.append({"source": lab[a], "target": lab[b], "weight": round(w, 3), "basis": main, "significant_on": sig,
                          "observed": m["observed"], "null_mean": m["null_mean"], "null_p95": m["null_p95"], "p": m["p"],
                          "windows": {k: ps[k] for k in WINDOWS}, "shared_articles": ps["shared"],
                          "same_direction_share": det["same_direction_share"], "example_article_pairs": det["example_article_pairs"],
                          "shared_article_examples": det["shared_articles_examples"], "time_span": det["time_span"]})
    communities = []
    for k, c in enumerate(comms):
        s = community_summary(E, c, ew, ev_by_acc, D, lp)
        if len(c) >= MIN_BLOC:
            st = E.set_test(c)
            share = E.calib_share("network", len(c), s["density"], s["strength"])
            setp = min(st["articles_3plus"]["p"], st["sync_t30"]["p"])
            s["significance"] = {"fixed_set_null": st, "null_worlds_with_community_this_large_dense_and_strong": share,
                                 "null_worlds": len(E.calib)}
            s["confidence"] = confidence(setp, share, st["sync_t30"]["p"])   # high needs timing too
        else:
            s["significance"], s["confidence"] = None, "n/a (pair)"
        s["id"] = k; s["members"] = [lab[a] for a in sorted(c, key=lambda a: lab[a])]
        s["_m"] = sorted(c)
        communities.append(s)
    cc = E.calib_counts("network")
    return {"nodes": nodes, "edges": out_edges, "communities": communities,
            "counts": {"accounts_tested": len(E.accs), "articles": len(E.arts), "events": len(E.ev),
                       "edges": len(out_edges), "communities_3plus": sum(1 for c in communities if c["size"] >= MIN_BLOC),
                       "communities_significant": sum(1 for c in communities if c["confidence"] in ("high", "medium")),
                       "expected_by_chance": cc}}


def blocs(E, D, ev_by_acc):
    import networkx as nx
    edges = E.edges("bloc")
    ew, lp = {}, {}
    G = nx.Graph()
    for i, pid, sig in edges:
        ps = E.pair_stats(i)["shared"]
        ew[pid] = math.log2((ps["observed"] + 1) / (ps["null_mean"] + 1)); lp[pid] = nlp(ps["p"], E.n)
        G.add_edge(pid // E.NA, pid % E.NA, weight=lp[pid])
    comms = [c for c in (nx.community.louvain_communities(G, weight="weight", seed=11) if len(G) else []) if len(c) >= MIN_BLOC]
    res = []
    for c in sorted(comms, key=lambda c: -len(c)):
        s = community_summary(E, c, ew, ev_by_acc, D, lp)
        st = E.set_test(c)
        tri = sum(1 for x in nx.enumerate_all_cliques(G.subgraph(c)) if len(x) == 3)
        share = E.calib_share("bloc", len(c), s["density"], s["strength"])
        s.update({"null": st, "null_worlds_with_bloc_this_large_dense_and_strong": share, "significant_triads": tri,
                  "synchrony": synchrony_summary(E, c),
                  "confidence": confidence(st["articles_3plus"]["p"], share, st["sync_t60"]["p"]), "_m": sorted(c)})
        res.append(s)
    return {"edges": len(edges), "blocs": res, "expected_by_chance": E.calib_counts("bloc")}


def synchrony_summary(E, members):
    """Median gap between different members' events on the same article; share of members' events with another member's
    event (any article) within 10 min / 24 h."""
    S = set(members)
    idx = np.where(np.isin(E.acc, list(S)))[0]
    gaps, n10, n24 = [], 0, 0
    for i in idx:
        other = idx[E.acc[idx] != E.acc[i]]
        dt = np.abs(E.t[other] - E.t[i])
        same = other[E.art[other] == E.art[i]]
        if len(same):
            gaps.append(np.abs(E.t[same] - E.t[i]).min())
        n10 += bool((dt <= 600).any()); n24 += bool((dt <= 86400).any())
    return {"median_same_article_gap_h": round(float(np.median(gaps)) / 3600, 2) if gaps else None,
            "share_events_with_member_within_10min": round(n10 / len(idx), 3) if len(idx) else None,
            "share_events_with_member_within_24h": round(n24 / len(idx), 3) if len(idx) else None}


def sync_pairs(E):
    edges = E.edges("sync")
    rows = []
    for i, pid, sig in edges:
        ps = E.pair_stats(i)["t10"]
        rows.append({"observed": ps["observed"], "null_mean": ps["null_mean"], "p": ps["p"], "p_article_shuffle": ps["p_article_shuffle"],
                     "_pid": pid, **{k: v for k, v in E.pair_detail(pid // E.NA, pid % E.NA, 600).items()
                                     if k in ("same_direction_share", "example_article_pairs", "time_span")}})
    robust = [r for r in rows if r["p_article_shuffle"] < P_EDGE]
    return {"pairs": rows, "n_pairs": len(rows), "n_also_beat_article_shuffle": len(robust),
            "accounts": len({x for r in rows for x in (r["_pid"] // E.NA, r["_pid"] % E.NA)}),
            "expected_by_chance": E.calib_counts("sync")}


# ------------------------------------------------------------------ time alignment with documented windows (e)
def _d(x):
    return ep(x + "T00:00:00Z")


def window_alignment(E, members, rng, n=1000):
    """Activity of an account set inside the documented coordination windows, and its change after the sanction dates.
    window_share: share of the set's events inside the window (95% CI: bootstrap over member accounts).
    expected_window_share: mean share for n random account sets matched member-by-member on event count (95% interval),
    p_high / p_low: share of matched sets at or above / at or below the observed share. Also: the share expected from the
    members' own active spans (events spread evenly between each member's first and last event) and the share of all
    other accounts' events. post_sanction_drop: (set's events in the 365 d after / before the date) divided by the same
    ratio for all other accounts; < 1 = the set fell off more than everyone else. p = share of matched sets with a ratio at
    least as low; CI by bootstrap over members."""
    S = np.array(sorted(members))
    acc_ev = [np.where(E.acc == a)[0] for a in range(E.NA)]
    n_ev = np.array([len(x) for x in acc_ev])
    others = np.setdiff1d(np.arange(E.NA), S)
    pool_sorted = others[np.argsort(n_ev[others], kind="stable")]
    def matched():
        out = []
        for a in S:
            k = np.searchsorted(n_ev[pool_sorted], n_ev[a])
            lo, hi = max(0, k - 15), min(len(pool_sorted), k + 15)
            out.append(pool_sorted[rng.integers(lo, hi)] if hi > lo else pool_sorted[rng.integers(0, len(pool_sorted))])
        return np.array(out)
    def times(set_):
        return E.t[np.concatenate([acc_ev[a] for a in set_])] if len(set_) else np.zeros(0)
    nonm = np.isin(E.acc, S, invert=True)
    nulls = [matched() for _ in range(n)] if len(pool_sorted) else []
    boots = [S[rng.integers(0, len(S), len(S))] for _ in range(n)]
    res = {"windows": {}, "post_sanction": {}}
    for k, (a, b, note) in DOC_WINDOWS.items():
        ta, tb = _d(a), _d(b)
        share = lambda ts: float(((ts >= ta) & (ts < tb)).mean()) if len(ts) else float("nan")
        obs = share(times(S))
        nv = np.array([share(times(x)) for x in nulls]) if nulls else np.array([np.nan])
        bv = np.array([share(times(x)) for x in boots])
        own = []
        for m in S:
            ts = E.t[acc_ev[m]]; f, l = ts.min(), ts.max()
            frac = (max(0, min(l, tb) - max(f, ta)) / (l - f)) if l > f else float(ta <= f < tb)
            own += [frac] * len(ts)
        res["windows"][k] = {"window": [a, b], "note": note, "window_share": round(obs, 3),
                             "window_share_ci95": [round(float(np.nanpercentile(bv, 2.5)), 3), round(float(np.nanpercentile(bv, 97.5)), 3)],
                             "expected_window_share": round(float(np.nanmean(nv)), 3),
                             "expected_ci95": [round(float(np.nanpercentile(nv, 2.5)), 3), round(float(np.nanpercentile(nv, 97.5)), 3)],
                             "p_high": round((int((nv >= obs).sum()) + 1) / (len(nv) + 1), 4),
                             "p_low": round((int((nv <= obs).sum()) + 1) / (len(nv) + 1), 4),
                             "expected_from_own_active_span": round(float(np.mean(own)), 3) if own else None,
                             "other_accounts_share": round(share(E.t[nonm]), 3) if nonm.any() else None}
    for d, note in SANCTIONS.items():
        td, w = _d(d), DROP_WINDOW_D * 86400
        def ratio(ts):
            bef = ((ts >= td - w) & (ts < td)).sum(); aft = ((ts >= td) & (ts < td + w)).sum()
            return (aft + 0.5) / (bef + 0.5), int(bef), int(aft)
        r_non, nb, na = ratio(E.t[nonm])
        r_obs, mb, ma = ratio(times(S))
        nv = np.array([ratio(times(x))[0] / r_non for x in nulls]) if nulls else np.array([np.nan])
        bv = np.array([ratio(times(x))[0] / r_non for x in boots])
        obs = r_obs / r_non
        res["post_sanction"][d] = {"note": note, "set_events_before": mb, "set_events_after": ma,
                                   "others_before": nb, "others_after": na, "post_sanction_drop": round(obs, 3),
                                   "ci95": [round(float(np.nanpercentile(bv, 2.5)), 3), round(float(np.nanpercentile(bv, 97.5)), 3)],
                                   "matched_null_mean": round(float(np.nanmean(nv)), 3),
                                   "matched_null_ci95": [round(float(np.nanpercentile(nv, 2.5)), 3), round(float(np.nanpercentile(nv, 97.5)), 3)],
                                   "p_drop": round((int((nv <= obs).sum()) + 1) / (len(nv) + 1), 4),
                                   "testable": mb >= 5}
    return res


# ------------------------------------------------------------------ profiles (d)
def profile(D, ev_by_acc, accts, E, rng, n=1000):
    def vals(S):
        ages, ecs, bl, ind, ext, sock = [], [], 0, 0, 0, 0
        for a in S:
            f = D["accounts"].get(E.accs[a]) or {}
            first = min(ev_by_acc[a], key=lambda e: e["t"])
            if first.get("age_d") is not None:
                ages.append(first["age_d"])
            if f.get("ec") is not None:
                ecs.append(f["ec"])
            bl += bool(f.get("blocked")); ind += bool(f.get("indef")); ext += bool(f.get("ext")); sock += f.get("breason") == "sock"
        k = len(S)
        return {"median_age_days": float(np.median(ages)) if ages else None,
                "share_age_lt30d": sum(x < 30 for x in ages) / len(ages) if ages else None,
                "share_age_lt1y": sum(x < 365 for x in ages) / len(ages) if ages else None,
                "median_editcount": float(np.median(ecs)) if ecs else None,
                "share_editcount_lt500": sum(x < 500 for x in ecs) / len(ecs) if ecs else None,
                "share_extended_confirmed": ext / k, "share_blocked_now": bl / k, "share_indef_now": ind / k,
                "share_sock_block": sock / k}
    obs = vals(accts)
    pool = [a for a in range(len(E.accs)) if E.deg[a] >= 2] or list(range(len(E.accs)))
    base = vals(range(len(E.accs)))
    draws = [vals(rng.choice(pool, size=min(len(accts), len(pool)), replace=False)) for _ in range(n)]
    out = {}
    for k, v in obs.items():
        nv = [d[k] for d in draws if d[k] is not None]
        out[k] = {"bloc": None if v is None else round(v, 3), "base_rate": None if base[k] is None else round(base[k], 3),
                  "null_p95": round(float(np.percentile(nv, 95)), 3) if nv else None,
                  "null_p05": round(float(np.percentile(nv, 5)), 3) if nv else None,
                  "percentile_vs_random_sets": round(sum(x <= v for x in nv) / len(nv), 3) if nv and v is not None else None}
    return out


# ------------------------------------------------------------------ copy-paste sweeps (c)
def sweeps(D, rng, n=1000):
    arts = D["articles"]
    items = []
    for r in D["revisions"]:
        if not any(e["kind"] == "insert" for e in r["events"]) or not r.get("ts"):
            continue
        for x in r.get("added") or []:
            sh = shingles(x["s"])
            if sh:
                items.append({"title": r["title"], "t": ep(r["ts"]), "u": r.get("u"), "anon": r.get("anon"), "s": x["s"],
                              "terms": x.get("terms") or [], "sh": sh, "group": (arts.get(r["title"]) or {}).get("group"),
                              "village": bool((arts.get(r["title"]) or {}).get("village"))})
    inv = defaultdict(list)
    for i, it in enumerate(items):
        for z in it["sh"]:
            inv[z].append(i)
    par = list(range(len(items)))
    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    cand = Counter()
    for z, lst in inv.items():
        if 1 < len(lst) <= 3000:
            for k, i in enumerate(lst):
                for j in lst[k + 1:]:
                    cand[(i, j)] += 1
    for (i, j), c in cand.items():
        a, b = items[i]["sh"], items[j]["sh"]
        if c / len(a | b) >= JACCARD:
            par[find(i)] = find(j)
    cl = defaultdict(list)
    for i in range(len(items)):
        cl[find(i)].append(items[i])
    pool_t = {g: np.array([it["t"] for it in items if it["group"] == g]) for g in ("topic", "comparison")}
    def w5(ts_arts):
        """Shortest span (days) containing insertions into SWEEP_MIN_ARTICLES distinct articles."""
        ts_arts = sorted(ts_arts)
        best, j, cnt = None, 0, Counter()
        for i in range(len(ts_arts)):
            cnt[ts_arts[i][1]] += 1
            while len(cnt) >= SWEEP_MIN_ARTICLES:
                span = (ts_arts[i][0] - ts_arts[j][0]) / 86400
                best = span if best is None else min(best, span)
                cnt[ts_arts[j][1]] -= 1
                if not cnt[ts_arts[j][1]]:
                    del cnt[ts_arts[j][1]]
                j += 1
        return best
    out = []
    for members in cl.values():
        na = len({m["title"] for m in members})
        if na < SWEEP_MIN_ARTICLES:
            continue
        g = Counter(m["group"] for m in members).most_common(1)[0][0]
        obs = w5([(m["t"], m["title"]) for m in members])
        pool = pool_t.get(g, np.array([]))
        k = len(members)
        null = []
        for _ in range(n):
            ts = rng.choice(pool, size=k, replace=len(pool) < k)
            null.append(w5([(t, i) for i, t in enumerate(ts)]))
        null = np.array(null, float)
        p = (int((null <= obs).sum()) + 1) / (n + 1)
        texts = Counter(" ".join(norm_words(m["s"])) for m in members)
        rep_n = texts.most_common(1)[0][0]
        rep = next(m["s"] for m in members if " ".join(norm_words(m["s"])) == rep_n)
        accts = Counter(m["u"] for m in members if m["u"] and not m["anon"])
        vshare = sum(m["village"] for m in members) / len(members)
        nak = bool(NAKBA.search(rep)) or any("nakba_expulsion" in m["terms"] for m in members)
        ts_all = [m["t"] for m in members]
        conf = "high" if p < 0.01 else "medium" if (p < 0.05 or na >= 10) else "low"
        out.append({"group": g, "n_sentences": k, "n_articles": na, "first": iso(min(ts_all)), "last": iso(max(ts_all)),
                    "distinct_accounts": len(accts), "anon_or_hidden_insertions": sum(1 for m in members if not m["u"] or m["anon"]),
                    "top_account_share": round(accts.most_common(1)[0][1] / k, 3) if accts else None,
                    "exact_identical_share": round(texts.most_common(1)[0][1] / k, 3),
                    "phrase": f"“{rep[:400]}”", "terms": sorted({t for m in members for t in m["terms"]}),
                    "village_share": round(vshare, 3), "nakba_on_village_pages": nak and vshare >= 0.5,
                    "articles": sorted({m["title"] for m in members})[:15],
                    "null": {"stat": f"shortest span (days) covering insertions into {SWEEP_MIN_ARTICLES} distinct articles",
                             "observed_days": round(obs, 2), "null_median_days": round(float(np.median(null)), 2),
                             "null_p05_days": round(float(np.percentile(null, 5)), 2), "p": round(p, 4),
                             "null": "same number of insertion times drawn at random from all term insertions in the group"},
                    "confidence": conf})
    out.sort(key=lambda x: (-x["n_articles"], x["first"]))
    vil = [it for it in items if it["village"] and ("nakba_expulsion" in it["terms"] or NAKBA.search(it["s"]))]
    return {"n_inserted_sentences": len(items), "clusters": out,
            "village_nakba": {"sentences": len(vil), "articles": len({v["title"] for v in vil}),
                              "accounts": len({v["u"] for v in vil if v["u"] and not v["anon"]})}}


# ------------------------------------------------------------------ main analysis
def analyze_data(D, n_null=1000, n_calib=200, seed=7, log=print, directions=("any", "insert", "remove")):
    ev, excl = build_events(D)
    rng = np.random.default_rng(seed)
    R = {"meta": {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "null_draws": n_null,
                  "calibration_worlds": n_calib, "events": len(ev), "excluded_revisions": dict(excl),
                  "collection": D.get("summary")}, "engines": {}}
    for g in ("topic", "comparison"):
        for d in directions:
            sub = [e for e in ev if e["group"] == g and (d == "any" or e["kind"] == d)]
            E = Engine(sub, f"{g}/{d}", n_null, n_calib, seed=seed + zlib.crc32(f"{g}/{d}".encode()) % 1000).run(log)
            eba = defaultdict(list)
            for e in sub:
                eba[E.ai[e["u"]]].append(e)
            rec = {"blocs": blocs(E, D, eba)}
            for b in rec["blocs"]["blocs"]:
                b["profile"] = profile(D, eba, b["_m"], E, rng)
                b["time_alignment"] = window_alignment(E, b["_m"], rng)
            if d == "any":
                rec["network"] = network(E, D, eba, log)
                rec["sync"] = sync_pairs(E)
                for c in rec["network"]["communities"]:
                    if c["size"] >= MIN_BLOC:
                        c["profile"] = profile(D, eba, c["_m"], E, rng)
                        ta = window_alignment(E, c["_m"], rng)
                        c["time_alignment"] = ta
                        c["window_share"] = {k: v["window_share"] for k, v in ta["windows"].items()}
                        c["expected_window_share"] = {k: {"mean": v["expected_window_share"], "ci95": v["expected_ci95"],
                                                          "p_high": v["p_high"], "p_low": v["p_low"]} for k, v in ta["windows"].items()}
                        c["post_sanction_drop"] = {d: {"ratio": v["post_sanction_drop"], "ci95": v["ci95"], "p_drop": v["p_drop"],
                                                       "testable": v["testable"]} for d, v in ta["post_sanction"].items()}
            rec["_accs"] = E.accs
            R["engines"][f"{g}/{d}"] = rec
    R["sweeps"] = sweeps(D, rng, n_null)
    return R


# ------------------------------------------------------------------ cards
def _strip(x):
    """Drop internal keys (account indices / pair ids) before anything is written."""
    if isinstance(x, dict):
        return {k: _strip(v) for k, v in x.items() if not k.startswith("_")}
    if isinstance(x, list):
        return [_strip(v) for v in x]
    return x


def card(cid, title, what, conf, null, so_what, caveat, numbers=None, chart=None):
    return {"id": cid, "title": title, "what_we_see": what, "confidence": conf, "null_model": null, "so_what": so_what,
            "caveat": caveat, "numbers": numbers or {}, "chart": chart}


def fmt_p(p):
    return f"p={p:.3f}" if p >= 0.001 else "p<0.001"


def build_cards(R):
    cards, letter = [], [0]
    m = R["meta"]; col = m.get("collection") or {}
    cards.append(card("coord_data", "What the coordination tier covers",
                      f"{col.get('n_revisions', 'n/a')} critical-term event revisions in {col.get('n_articles', 'n/a')} articles "
                      f"(diff status {col.get('diff_status')}); {m['events']} account events used after excluding "
                      f"{m['excluded_revisions']} (anonymous, hidden-user, bot, deleted). One run-wide pseudonymous ID per account.",
                      "descriptive", {"draws": m["null_draws"], "calibration_worlds": m["calibration_worlds"]},
                      "All tests below share these events; topic and comparison articles are tested separately.",
                      "Lead events come from mass2's grid (exact events only) and the ratchet key articles; edits outside "
                      "those events are invisible here. IP and temporary accounts are excluded from account-level tests.",
                      numbers={"collection": col, "excluded": m["excluded_revisions"]}))
    for key, rec in R["engines"].items():
        g, d = key.split("/")
        B = rec["blocs"]; ex = B["expected_by_chance"]
        lines = []
        sig = [b for b in B["blocs"] if b["confidence"] in ("high", "medium")]
        for b in B["blocs"]:                       # only groups that pass the bloc test get a name
            if b in sig:
                b["name"] = f"Bloc {bloc_name(letter[0])} ({b['size']} accounts)"; letter[0] += 1
        for b in sig:
            n3 = b["null"]["articles_3plus"]; s60 = b["null"]["sync_t60"]; sy = b["synchrony"]
            lines.append(f"{b['name']} [{b['confidence']}]: {b['n_articles']} articles (top: "
                         f"{', '.join(a['title'] for a in b['articles'][:4])}); {b['direction']['insert']} insertions / "
                         f"{b['direction']['remove']} removals; articles touched by 3+ members {n3['observed']} vs null "
                         f"{n3['null_mean']} (95th {n3['null_p95']}, {fmt_p(n3['p'])}); 60-min cross-article co-activity "
                         f"{s60['observed']} vs {s60['null_mean']} ({fmt_p(s60['p'])}, article-shuffle {fmt_p(s60['p_article_shuffle'])}); "
                         f"median same-article gap {sy['median_same_article_gap_h']} h, events with another member within "
                         f"10 min {sy['share_events_with_member_within_10min']}; {b['significant_triads']} significant triads; "
                         f"null worlds with a bloc this large and dense: {b['null_worlds_with_bloc_this_large_dense_and_strong']}; "
                         f"active {b['active']['first']} to {b['active']['last']}")
        conf = "high" if any(b["confidence"] == "high" for b in sig) else "medium" if sig else "not detected"
        what = (f"{g} articles, {d} events: {B['edges']} account pairs share articles above the rewiring null "
                f"(p<{P_EDGE}, >={MIN_OBS} shared); null worlds give {ex.get('edges_mean')} such pairs on average "
                f"(95th {ex.get('edges_p95')}). {len(B['blocs'])} candidate groups of 3+ (null worlds: {ex.get('communities_mean')} "
                f"on average, 95th {ex.get('communities_p95')}); {len(sig)} pass the bloc test. " +
                (" | ".join(lines) if lines else "No bloc detected."))
        cards.append(card(f"blocs_{g}_{d}", f"(a) Bloc detection: {g} articles, {d} events", what, conf,
                          {"pairs": f"degree-preserving rewiring, {m['null_draws']} draws", "bloc": "articles with 3+ members vs "
                           "rewiring; selection-aware share of null worlds; synchrony vs account day-shift (1-7 d) and time "
                           "shuffle within article", "expected_by_chance": ex},
                          "A bloc is a set of accounts whose overlap in critical-term articles is not explained by how active "
                          "each account is and how popular each article is." if sig else
                          "Account overlap is what the rewiring null predicts from activity and article popularity alone.",
                          "Shared interest (WikiProject members, watchlists, talk-page RfCs) also produces overlap beyond a "
                          "degree-preserving null; synchrony and direction help separate it but do not prove coordination.",
                          numbers={"blocs": [_strip({k: v for k, v in b.items() if k != "members"}) for b in B["blocs"]]},
                          chart="chart_data/blocs.json"))
        if d != "any":
            continue
        S = rec["sync"]; ex = S["expected_by_chance"]
        cards.append(card(f"sync_{g}", f"(b) Synchrony: {g} account pairs acting on different articles within 10 minutes",
                          f"{S['n_pairs']} pairs ({S['accounts']} accounts) acted on 3+ distinct article pairs within 10 min of "
                          f"each other more often than the account day-shift null (p<{P_EDGE}); {S['n_also_beat_article_shuffle']} also "
                          f"beat the within-article time-shuffle null. Null worlds give {ex.get('edges_mean')} pairs on average "
                          f"(95th {ex.get('edges_p95')}).",
                          "high" if S["n_also_beat_article_shuffle"] > (ex.get("edges_p95") or 0) else
                          "medium" if S["n_pairs"] > (ex.get("edges_p95") or 0) else "not detected (consistent with chance)",
                          {"null": f"each account's timeline shifted by a random 1-7 days (either sign), {m['null_draws']} draws; secondary: timestamps "
                                   "permuted within article",
                           "expected_by_chance": ex},
                          "Pairs that repeatedly move together across different articles within minutes are the classic "
                          "canvassing / sockpuppet signature, if they are more than the null expects.",
                          "Both accounts may react to the same external trigger (news, an RfC closing, a noticeboard thread).",
                          numbers={"pairs": [_strip(p) for p in S["pairs"][:50]]}, chart="chart_data/sync.json"))
        N = rec["network"]; c = N["counts"]; ex = c["expected_by_chance"]
        cards.append(card(f"network_{g}", f"Co-activity network: {g} articles (time + direction)",
                          f"{c['edges']} significant edges among {len(N['nodes'])} accounts (of {c['accounts_tested']} tested); "
                          f"expected by chance {ex.get('edges_mean')} (95th {ex.get('edges_p95')}). {c['communities_3plus']} "
                          f"communities of 3+ (chance {ex.get('communities_mean')}, 95th {ex.get('communities_p95')}), "
                          f"{c['communities_significant']} significant.",
                          "high" if any(x["confidence"] == "high" for x in N["communities"]) else
                          "medium" if c["communities_significant"] else "not detected (consistent with chance)",
                          {"edge": f"p<{P_EDGE} and observed>={MIN_OBS} on 30-min cross-article co-activity (account day-shift) or "
                                   "shared articles (rewiring)", "expected_by_chance": ex},
                          "The page's network graph; edges carry direction agreement, so insert-blocs and remove-blocs are visible.",
                          "Edges are tested one by one at p<0.01; compare the edge count with the chance expectation, not with zero.",
                          chart="chart_data/network.json"))
    # (c) sweeps
    SW = R["sweeps"]
    for g in ("topic", "comparison"):
        cl = [x for x in SW["clusters"] if x["group"] == g]
        cards.append(card(f"sweeps_{g}", f"(c) Copy-paste sweeps: {g} articles",
                          f"{len(cl)} near-identical inserted sentences (5-word shingle Jaccard >= {JACCARD}) appear in "
                          f"{SWEEP_MIN_ARTICLES}+ articles. " + " | ".join(
                              f"{x['n_articles']} articles, {x['first']} to {x['last']}, {x['distinct_accounts']} accounts "
                              f"(+{x['anon_or_hidden_insertions']} anon/hidden insertions), {x['phrase']} "
                              f"[{x['confidence']}; 5-article span {x['null']['observed_days']} d vs null median "
                              f"{x['null']['null_median_days']} d, {fmt_p(x['null']['p'])}]" for x in cl[:8]),
                          max((x["confidence"] for x in cl), key=["low", "medium", "high"].index) if cl else "n/a (none found)",
                          {"null": f"same number of insertion times drawn from all term insertions in the group, {m['null_draws']} draws; "
                                   "statistic: shortest span covering 5 distinct articles"},
                          "A sweep is the same wording placed into many articles; a short span and few accounts point to a "
                          "campaign, a long span and many accounts to a shared standard phrase.",
                          "Standard wording (WikiProject templates, a source's stock phrase) also repeats; the temporal null "
                          "separates bursts from slow diffusion, not intent.",
                          numbers={"clusters": cl[:30]}, chart="chart_data/sweeps.json"))
    vn = SW["village_nakba"]; vc = [x for x in SW["clusters"] if x["nakba_on_village_pages"]]
    cards.append(card("sweeps_nakba_villages", "(c) Nakba wording on Palestinian village pages",
                      f"{vn['sentences']} inserted Nakba / expulsion sentences on {vn['articles']} village pages by "
                      f"{vn['accounts']} registered accounts. Sweeps (5+ village articles, same wording): {len(vc)}. " +
                      " | ".join(f"{x['n_articles']} articles {x['first']} to {x['last']}, {x['distinct_accounts']} accounts: "
                                 f"{x['phrase']} [{x['confidence']}, {fmt_p(x['null']['p'])}]" for x in vc[:5]),
                      max((x["confidence"] for x in vc), key=["low", "medium", "high"].index) if vc else "n/a (no sweep)",
                      {"null": "as for (c)"},
                      "Flags whether the village-page Nakba wording arrived as one sweep or piecemeal.",
                      "Village articles share a WikiProject structure (Khalidi / Morris sourcing), so similar wording is "
                      "expected; only a short-span, few-account cluster suggests a sweep.", numbers={"clusters": vc}))
    # (e) documented windows, both directions
    rows = []
    for key, rec in R["engines"].items():
        g, d = key.split("/")
        sets = [(b["name"], b) for b in rec["blocs"]["blocs"] if b["confidence"] in ("high", "medium")]
        if d == "any" and "network" in rec:
            sets += [(f"{g} network community {c['id']} ({c['size']} accounts)", c) for c in rec["network"]["communities"]
                     if c["confidence"] in ("high", "medium") and c.get("time_alignment")]
        for nm, b in sets:
            ta = b["time_alignment"]
            w = "; ".join(f"{k}: {v['window_share']:.0%} of events in window [CI {v['window_share_ci95'][0]:.0%}-"
                          f"{v['window_share_ci95'][1]:.0%}] vs matched sets {v['expected_window_share']:.0%} "
                          f"[{v['expected_ci95'][0]:.0%}-{v['expected_ci95'][1]:.0%}], own-span {v['expected_from_own_active_span']}, "
                          f"others {v['other_accounts_share']}, p_high {v['p_high']}" for k, v in ta["windows"].items())
            ps = "; ".join(f"after {dd}: drop ratio {v['post_sanction_drop']} [CI {v['ci95'][0]}-{v['ci95'][1]}] vs matched "
                           f"{v['matched_null_mean']}, p_drop {v['p_drop']}" + ("" if v["testable"] else " (too few events before)")
                           for dd, v in ta["post_sanction"].items())
            rows.append({"set": nm, "scope": key, "direction": d, "text": f"{nm} [{key}]: {w}. {ps}",
                         "time_alignment": ta})
    by_dir = Counter(r["direction"] for r in rows)
    sig_any = [r for r in rows if any(v["p_high"] < 0.01 for v in r["time_alignment"]["windows"].values())
               or any(v["testable"] and v["p_drop"] < 0.01 for v in r["time_alignment"]["post_sanction"].values())]
    cards.append(card("windows", "(e) Do detected blocs line up with the documented canvassing windows and sanctions?",
                      (f"Sets tested: {len(rows)} (insert-direction blocs {by_dir.get('insert', 0)}, remove-direction "
                       f"{by_dir.get('remove', 0)}, any-direction blocs and communities {by_dir.get('any', 0)}). "
                       f"{len(sig_any)} show window concentration or a post-sanction drop beyond matched random sets (p<0.01). "
                       + " | ".join(r["text"] for r in rows)) if rows else
                      "No bloc or community passed the significance tests, so alignment with the documented windows (email "
                      "canvassing Oct 2023-Jan 2024; TfP Discord Jan-Sep 2024; sanctions ~9 Dec 2024 and 25 Apr 2025) is not "
                      "detected. Not detected is not the same as did not happen: off-wiki canvassing of talk-page votes, edits "
                      "outside these critical-term lead events and small groups below the test's power are invisible here.",
                      "medium" if sig_any else ("low" if rows else "n/a (nothing to align)"),
                      {"window_share": "matched random account sets (member-by-member on event count), 1,000 draws; CI = "
                                       "bootstrap over members", "post_sanction_drop": "365 d after vs before each date, relative "
                                       "to all other accounts; same matched-set null", "windows": DOC_WINDOWS, "sanctions": SANCTIONS},
                      "Alignment in time is not attribution: a set active during the Discord months is not shown to be the "
                      "Discord group. It is a test of whether the documented windows left a footprint in who edited these terms.",
                      "Dates come from ORGS.md snippets (marked there as needing verification); only critical-term lead "
                      "events are counted; a drop after a sanction can also reflect the war-news cycle, which the "
                      "comparison with all other accounts only partly removes.",
                      numbers={"sets": [_strip({k: v for k, v in r.items() if k != "text"}) for r in rows]},
                      chart="chart_data/windows.json"))
    # (d) profiles
    prof = []
    for key, rec in R["engines"].items():
        for b in rec["blocs"]["blocs"]:
            if b["confidence"] in ("high", "medium"):
                prof.append({"bloc": b["name"], "scope": key, "profile": b["profile"]})
    cards.append(card("profiles", "(d) Account profiles of the blocs (aggregate)",
                      " | ".join(f"{p['bloc']} {p['scope']}: median age {p['profile']['median_age_days']['bloc']} d "
                                 f"(base {p['profile']['median_age_days']['base_rate']}), editcount<500 "
                                 f"{p['profile']['share_editcount_lt500']['bloc']} (base {p['profile']['share_editcount_lt500']['base_rate']}), "
                                 f"blocked now {p['profile']['share_blocked_now']['bloc']} (base {p['profile']['share_blocked_now']['base_rate']}, "
                                 f"random-set 95th {p['profile']['share_blocked_now']['null_p95']})" for p in prof) or
                      "No bloc passed the bloc test, so no profile is reported.",
                      "medium" if prof else "n/a", {"null": "1,000 random account sets of the same size from accounts with 2+ "
                                                            "articles in the same scope; base rate = all accounts in scope"},
                      "Young, low-editcount or since-blocked blocs are the sockpuppet profile; veteran blocs look like "
                      "WikiProject regulars.", "Block status is as of collection, not as of the edit.",
                      numbers={"profiles": prof}))
    return cards


def render_md(cards, R):
    out = ["# Coordinated editing: blocs, synchrony, sweeps", "",
           f"Generated {R['meta']['generated']}. Nulls: {R['meta']['null_draws']} draws; pipeline calibration on "
           f"{R['meta']['calibration_worlds']} null worlds. No usernames or account hashes appear here; blocs are lettered.", ""]
    for c in cards:
        out += [f"## {c['title']}", "", f"**Confidence:** {c['confidence']}", "", c["what_we_see"], "",
                f"**Null model:** {json.dumps(c['null_model'], ensure_ascii=False)}", "", f"**So what:** {c['so_what']}", "",
                f"**Caveat:** {c['caveat']}", ""]
    return "\n".join(out)


def write_outputs(R, out_dir=OUT):
    os.makedirs(os.path.join(out_dir, "chart_data"), exist_ok=True)
    cards = build_cards(R)
    net = {"generated": R["meta"]["generated"],
           "method": {"edge": f"empirical p<{P_EDGE} and observed>={MIN_OBS}; co-activity = events on different articles within "
                              "10 / 30 (default) / 60 min, null = each account's timeline shifted by a random 1-7 days (within-article time shuffle "
                              "reported as p_article_shuffle); plus shared article sets, null = "
                              "degree-preserving rewiring; 1,000 draws", "communities": "Louvain (networkx, seed 11), weight = "
                              "log2((obs+1)/(null mean+1))", "labels": "A1, A2... per network; no hashes or usernames"}}
    for g in ("topic", "comparison"):
        rec = R["engines"].get(f"{g}/any")
        if rec:
            net[g] = _strip(rec["network"])
    json.dump(net, open(os.path.join(out_dir, "chart_data", "network.json"), "w"), indent=1, ensure_ascii=False)
    json.dump({k: _strip(v["blocs"]) for k, v in R["engines"].items()}, open(os.path.join(out_dir, "chart_data", "blocs.json"), "w"),
              indent=1, ensure_ascii=False)
    json.dump({k: _strip(v["sync"]) for k, v in R["engines"].items() if "sync" in v},
              open(os.path.join(out_dir, "chart_data", "sync.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(_strip(R["sweeps"]), open(os.path.join(out_dir, "chart_data", "sweeps.json"), "w"), indent=1, ensure_ascii=False)
    json.dump({k: {"network": v["network"]["counts"]["expected_by_chance"] if "network" in v else None,
                   "bloc": v["blocs"]["expected_by_chance"]} for k, v in R["engines"].items()},
              open(os.path.join(out_dir, "chart_data", "calibration.json"), "w"), indent=1)
    json.dump([c["numbers"] for c in cards if c["id"] == "windows"][0], open(os.path.join(out_dir, "chart_data", "windows.json"), "w"),
              indent=1, ensure_ascii=False)
    json.dump([c["numbers"] for c in cards if c["id"] == "profiles"][0], open(os.path.join(out_dir, "chart_data", "profiles.json"), "w"),
              indent=1)
    json.dump(_strip({"meta": R["meta"], "cards": cards}), open(os.path.join(out_dir, "cards.json"), "w"), indent=1, ensure_ascii=False)
    open(os.path.join(out_dir, "cards.md"), "w").write(render_md(cards, R))
    return cards


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=DATA)
    ap.add_argument("--null", type=int, default=int(os.environ.get("COORD_NULL", "1000")))
    ap.add_argument("--calib", type=int, default=int(os.environ.get("COORD_CALIB", "200")))
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    D = json.load(gzip.open(a.data, "rt"))
    R = analyze_data(D, a.null, a.calib)
    cards = write_outputs(R, a.out)
    for c in cards:
        print(f"[{c['confidence']}] {c['title']}")


if __name__ == "__main__":
    main()
