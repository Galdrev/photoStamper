"""Mass v2 analysis: twelve pattern cards from the mass2 crawl (mass2.py merge outputs).

  python analyze_mass2.py [--data DIR] [--out DIR] [--boot N] [--workers N] [--ref FILE]
      reads   DIR/mass2.json (or mass2.json.gz), mass2_events.json.gz, mass2_editors.json.gz, mass2_leads.json.gz,
              mass2_summary.json, wikidata_types.json            (default DIR = wikitrends/data)
      writes  OUT/cards.json, OUT/cards.md, OUT/chart_data/*.json, OUT/event_mass2_leads.txt
              (default OUT = wikitrends/patterns/mass2)

Design
  * Groups: topic vs comparison (stratum "comparison"; the atrocity stratum is kept out of the comparison pool and used
    only in card 11). Every comparison is run on all articles and on the "relevant" subset, defined as in cohere.py:
    Wikidata type keep (data/wikidata_types.json, falling back to the 2023 P31 of the record) AND baseline relevance from
    the earliest lead snapshot (both narrative groups named, or >= 2 land/conflict words per 1,000).
  * Uncertainty: article-level bootstrap (resample articles within group) for every headline number; where the
    clustering matters a second CI resamples whole WikiProjects within group ("cl" CI). Topic has only 4 projects, so the
    cluster CI is coarse and conservative.
  * Lead text: critical counts, event-filter residual and first sentences are computed from mass2_leads.json.gz (the
    same prose mass_narr stores). Without the leads file the narr features or lex_lead counts are used instead.
  * Robustness: every field is read through safe getters; a card that still fails is written as an error card and the
    run continues. Missing files reduce the cards that depend on them.
  * Privacy: no username, hash or account-level row is written; accounts appear only as counts. The script refuses to
    write outputs that contain any editor hash found in the input.
"""
import argparse, gzip, json, math, os, re, sys, time, traceback
from collections import Counter, defaultdict
from datetime import datetime, timezone

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze as A           # noqa: E402
import explore as E           # noqa: E402
import event_filter as EF     # noqa: E402
try:
    import mass_narr as MN    # noqa: E402  (narrative group names for the relevance baseline)
except Exception:             # pragma: no cover
    MN = None
try:
    from wikidata import DROP as WD_DROP   # noqa: E402
except Exception:             # pragma: no cover
    WD_DROP = {}
try:
    from corpus import KEY_ARTICLES, KEY_ARTICLES_CONTROL   # noqa: E402
except Exception:             # pragma: no cover
    KEY_ARTICLES, KEY_ARTICLES_CONTROL = [], []

CRIT = list(A.CRITICAL)
DATES = ["2021-01-01", "2023-07-01", "now"]
G2 = ("topic", "comparison")
NB = int(os.environ.get("WT_BOOT", "1000"))
RNG = np.random.default_rng(2026)
WORD = re.compile(r"\w+")
DAY = 86400.0
HASH12 = re.compile(r"\b[0-9a-f]{12}\b")
REF_DEFAULT = os.path.join(HERE, "study3", "holdout_results", "event_mass_leads.txt")
DEFAULT_OUT = os.path.join(HERE, "patterns", "mass2")

# ratchet / SYNTHESIS reference numbers (25 topic + 15 comparison key leads; data/ratchet.json, D5 in SYNTHESIS)
RATCHET_REF = {"topic": {"insert_30d": 0.363, "remove_30d": 0.297, "asym_30d": 0.066, "failed_before_stick": 3.34,
                         "editors_in_attempts": 3.4, "events_per_article": 10.7, "entered": 25, "left": 6},
               "comparison": {"insert_30d": 0.56, "remove_30d": 0.276, "asym_30d": 0.284, "failed_before_stick": 1.44,
                              "editors_in_attempts": 2.2, "events_per_article": 5.0, "entered": 4, "left": 5}}

FRAMING_CAT = re.compile(r"genocid|colonial|apartheid|occupation|occupied|massacre|terror|zionis|antisemit|ethnic cleansing|"
                         r"nakba|expuls|war crime|persecution|crimes against humanity|islamophob", re.I)
# concept group (mass2 alias table) -> lead terms it is about
CONCEPT_TERMS = {"nakba_1948": ["nakba_expulsion"], "apartheid_il": ["apartheid"], "settler_colonialism": ["settler_colonial"],
                 "gaza_genocide": ["genocide"], "occupation_il": ["occupation"], "genocide_generic": ["genocide", "ethnic_cleansing"],
                 "Apartheid": ["apartheid"], "Colonialism": ["settler_colonial"], "War crimes": ["war_crimes"],
                 "Armenian genocide": ["genocide"], "Russian occupation of Ukraine": ["occupation"],
                 "Turkish occupation of Northern Cyprus": ["occupation"], "Persecution of Uyghurs in China": ["genocide"]}
HOT_CORE = ["nakba_1948", "apartheid_il", "settler_colonialism", "gaza_genocide", "occupation_il", "genocide_generic"]
ATTR = re.compile(E.HEDGE.pattern + r"|\b(?:states? that|stated that|says?|said|found|find|concluded?|ruled|determined|"
                  r"recogni[sz]\w*|consider\w*|describ\w*|call\w*|termed|den(?:y|ies|ied)|deni\w*|scholars|experts|"
                  r"historians|organi[sz]ations|according|plausib\w*|whether|risk of)\b", re.I)
GAZA_RX = re.compile(r"^(?:Gaza genocide|Gaza war|Israel[–-]Hamas war|Allegations of genocide in the 2023 Israeli attack on Gaza)$")


# ================================================================== safe access
def g(d, *ks, default=None):
    for k in ks:
        if isinstance(d, dict):
            d = d.get(k)
        elif isinstance(d, list) and isinstance(k, int) and -len(d) <= k < len(d):
            d = d[k]
        else:
            return default
        if d is None:
            return default
    return d


def num(x, default=None):
    if isinstance(x, bool) or x is None:
        return default
    if isinstance(x, (int, float, np.integer, np.floating)) and math.isfinite(float(x)):
        return float(x)
    return default


def dct(x):
    return x if isinstance(x, dict) else {}


def lst(x):
    return x if isinstance(x, list) else []


def ep(ts):
    try:
        return datetime.strptime(str(ts)[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc).timestamp()
    except (ValueError, TypeError):
        return None


def quarter(ts):
    try:
        return f"{ts[:4]}-Q{(int(ts[5:7]) - 1) // 3 + 1}"
    except (ValueError, TypeError, IndexError):
        return None


def r3(x, k=3):
    return None if x is None else (round(float(x), k) if isinstance(x, (float, np.floating)) else x)


def pct(x, k=1):
    return "n/a" if x is None else f"{100 * x:.{k}f}%"


def sgn(x, k=2, unit=""):
    return "n/a" if x is None else f"{x:+.{k}f}{unit}"


def ci_txt(d, scale=1.0, k=2, unit=""):
    """'+2.30 [+1.40, +3.20]' (article CI; cluster CI in braces when present)."""
    if not d or d.get("est") is None:
        return "n/a"
    s = f"{d['est'] * scale:+.{k}f}{unit}"
    if d.get("lo") is not None:
        s += f" [{d['lo'] * scale:+.{k}f}, {d['hi'] * scale:+.{k}f}]"
    if d.get("cl_lo") is not None:
        s += f" {{project CI {d['cl_lo'] * scale:+.{k}f}, {d['cl_hi'] * scale:+.{k}f}}}"
    return s


def ci_pct(d, k=1):
    """'3.6% [2.4, 4.9]' for a share (no sign)."""
    if not d or d.get("est") is None:
        return "n/a"
    s = f"{100 * d['est']:.{k}f}%"
    if d.get("lo") is not None:
        s += f" [{100 * d['lo']:.{k}f}, {100 * d['hi']:.{k}f}]"
    if d.get("cl_lo") is not None:
        s += f" {{project CI {100 * d['cl_lo']:.{k}f}, {100 * d['cl_hi']:.{k}f}}}"
    return s


def sig(d, cluster=False):
    if not d or d.get("est") is None:
        return False
    lo, hi = (d.get("cl_lo"), d.get("cl_hi")) if cluster else (d.get("lo"), d.get("hi"))
    return lo is not None and hi is not None and (lo > 1e-9 or hi < -1e-9)


def pos(d):
    return sig(d) and d["est"] > 0


def neg(d):
    return sig(d) and d["est"] < 0


def warn(msg):
    print("WARNING: " + msg, file=sys.stderr, flush=True)


# ================================================================== loading
def load_any(path):
    for p in (path, path + ".gz") if not path.endswith(".gz") else (path,):
        if os.path.exists(p):
            try:
                with (gzip.open(p, "rt", encoding="utf-8") if p.endswith(".gz") else open(p, encoding="utf-8")) as f:
                    return json.load(f)
            except Exception as ex:
                warn(f"could not read {p}: {ex}")
                return None
    return None


def load(data_dir):
    M = load_any(os.path.join(data_dir, "mass2.json"))
    if not isinstance(M, dict) or not isinstance(M.get("articles"), list):
        sys.exit(f"analyze_mass2: no usable mass2.json in {data_dir}")
    EV = dct(g(load_any(os.path.join(data_dir, "mass2_events.json.gz")), "articles"))
    ED = load_any(os.path.join(data_dir, "mass2_editors.json.gz"))
    LD = load_any(os.path.join(data_dir, "mass2_leads.json.gz"))
    SU = load_any(os.path.join(data_dir, "mass2_summary.json"))
    TY = None
    for d in dict.fromkeys([data_dir, A.DATA, os.path.join(HERE, "data")]):
        TY = load_any(os.path.join(d, "wikidata_types.json"))
        if TY:
            break
    if not TY:
        warn("no wikidata_types.json found: relevance uses the 2023 Wikidata P31 of each record only")
    return M, EV, dct(ED), dct(LD), dct(SU), dct(TY)


# ================================================================== lead text metrics
def first_sentence(text):
    for p in re.split(r"\n\s*\n", text or ""):
        if len(WORD.findall(p)) >= 5:
            ss = A.sentences(p)
            return ss[0][:400] if ss else None
    return None


def lead_metrics(text):
    if not isinstance(text, str) or not text.strip():
        return None
    w = len(WORD.findall(text))
    c = {k: A.count(k, text) for k in CRIT}
    res, ev, st = EF.split(text, "sentence")
    cr = lambda t: sum(A.count(k, t) for k in CRIT) if t else 0
    return {"w": w, "c": c, "crit": sum(c.values()), "res": cr(res), "ev": cr(ev), "evs": st.get("event_share"),
            "fs": first_sentence(text), "h": hash(re.sub(r"\s+", " ", text).strip()), "src": "text"}


def _lm_chunk(texts):
    return [lead_metrics(t) for t in texts]


def metrics_from_snapshot(narr, art):
    """Fallback when the lead text is missing: mass_narr features, else the article's lex_lead counts."""
    if isinstance(narr, dict) and narr.get("words") is not None:
        cnt = dct(narr.get("counts"))
        ev = dct(g(narr, "ev", "sentence"))
        c = {k: int(num(cnt.get(k), 0)) for k in CRIT}
        rc = dct(ev.get("res_counts")); ec = dct(ev.get("ev_counts"))
        return {"w": int(num(narr.get("words"), 0)), "c": c, "crit": sum(c.values()),
                "res": sum(int(num(rc.get(k), 0)) for k in CRIT), "ev": sum(int(num(ec.get(k), 0)) for k in CRIT),
                "evs": num(ev.get("event_share")), "fs": None, "h": None, "src": "narr"}
    if isinstance(art, dict) and not art.get("redirect") and art.get("lead_words") is not None:
        lx = dct(art.get("lex_lead"))
        c = {k: int(num(lx.get(k), 0)) for k in CRIT}
        return {"w": int(num(art.get("lead_words"), 0)), "c": c, "crit": sum(c.values()), "res": None, "ev": None, "evs": None,
                "fs": None, "h": None, "src": "lex_lead"}
    return None


# ================================================================== article model
class Art:
    __slots__ = ("t", "r", "grp", "cl", "case", "snap", "L", "rel", "win", "v12", "vw2", "tbt", "titles", "ev", "proj", "ce")


def resolve_snaps(r):
    at = dct(r.get("at"))
    snaps = {k: dict(dct(at.get(k))) for k in DATES}
    for k in DATES:
        for f in ("article", "narr"):
            v = snaps[k].get(f)
            if isinstance(v, dict) and "same_as" in v:
                ref = g(snaps, v.get("same_as"), f)
                snaps[k][f] = None if (not isinstance(ref, dict) or "same_as" in ref) else ref
        a = snaps[k].get("article")
        if not isinstance(a, dict) or a.get("redirect"):
            snaps[k]["article"] = None
        if not isinstance(snaps[k].get("narr"), dict):
            snaps[k]["narr"] = None
    return snaps


def views_of(r):
    pv = dct(r.get("pageviews"))
    mon = pv.get("monthly")
    labels, vals = [], []
    if isinstance(mon, dict) and isinstance(mon.get("views"), list):
        y, m = int(str(mon.get("start") or "202101")[:4]), int(str(mon.get("start") or "202101")[4:6])
        for v in mon["views"]:
            labels.append(f"{y}{m:02d}"); vals.append(num(v))
            y, m = (y, m + 1) if m < 12 else (y + 1, 1)
    elif isinstance(mon, dict):                       # shard (full) form: {"YYYYMM": views}
        for k in sorted(mon):
            labels.append(str(k)); vals.append(num(mon[k]))
    have = [v for v in vals if v is not None]
    v12 = sum(v for v in vals[-12:] if v is not None) if have else None
    vw2 = sum(v for lab, v in zip(labels, vals) if v is not None and lab >= "202307") if have else None
    tbt = {str(k): num(v) for k, v in dct(pv.get("total_by_title")).items()}
    return v12, vw2, tbt, [str(x) for x in lst(pv.get("titles"))]


def wd_keep(a, TY):
    for t in [a.t] + [x for x in lst(a.r.get("frame_titles")) if isinstance(x, str)]:
        if t in TY and isinstance(TY[t], dict):
            return bool(TY[t].get("keep", True))
    p31 = lst(g(a.r, "wikidata_2023", "p31"))
    return not any(p in WD_DROP for p in p31)


def baseline_relevant(a):
    c = None
    for k in DATES:
        c = g(a.snap, k, "narr", "c")
        if isinstance(c, dict):
            break
    if not isinstance(c, dict):
        return False
    if MN is not None:
        try:
            gk = ["G_" + x for x in MN.groups_for({"group": a.r.get("group"), "project": a.r.get("project")})[0]]
        except Exception:
            gk = [k for k in c if str(k).startswith("G_")]
    else:
        gk = [k for k in c if str(k).startswith("G_")]
    both = all(num(c.get(k), 0) > 0 for k in gk) if gk else False
    land = num(c.get("LANDCONF"), 0) * 1000 / max(1.0, num(c.get("_words"), 0))
    return bool(both or land >= 2)


def build(M, EV, LD, TY, workers=0):
    leads = dct(LD.get("leads"))
    ldates = [str(x) for x in lst(LD.get("dates"))]
    li = {k: (ldates.index(k) if k in ldates else (ldates.index(k[:10]) if k[:10] in ldates else None)) for k in DATES}
    if li["now"] is None and len(ldates) == 3:
        li["now"] = 2
    arts = []
    for r in M.get("articles") or []:
        if not isinstance(r, dict) or not isinstance(r.get("title"), str):
            continue
        a = Art()
        a.t, a.r = r["title"], r
        st = r.get("stratum") or r.get("group")
        a.grp = "topic" if r.get("group") == "topic" else ("atrocity" if st == "atrocity" else "comparison")
        a.proj = r.get("project") if isinstance(r.get("project"), str) else None
        a.cl = a.proj or f"_{a.grp}:{r.get('atrocity_case') or 'none'}"
        a.case = r.get("atrocity_case")
        a.snap = resolve_snaps(r)
        a.win = dct(r.get("win"))
        a.v12, a.vw2, a.tbt, a.titles = views_of(r)
        a.ev = dct(EV.get(a.t))
        a.L = {}
        a.ce = None
        arts.append(a)
    # lead metrics: text first (parallel if asked), fallback per date
    jobs = []
    for a in arts:
        ls = leads.get(a.t)
        for k in DATES:
            txt = ls[li[k]] if isinstance(ls, list) and li[k] is not None and li[k] < len(ls) else None
            jobs.append(txt if isinstance(txt, str) else None)
    res = None
    if workers and workers > 1 and len(jobs) > 3000:
        try:
            from concurrent.futures import ProcessPoolExecutor
            ch = [jobs[i:i + 600] for i in range(0, len(jobs), 600)]
            with ProcessPoolExecutor(max_workers=workers) as ex:
                res = [x for part in ex.map(_lm_chunk, ch) for x in part]
        except Exception as ex_:
            warn(f"parallel lead pass failed ({ex_}); running serially"); res = None
    if res is None:
        res = _lm_chunk(jobs)
    i = 0
    for a in arts:
        for k in DATES:
            m = res[i]; i += 1
            a.L[k] = m if m is not None else metrics_from_snapshot(a.snap[k]["narr"], a.snap[k]["article"])
        a.rel = wd_keep(a, TY) and baseline_relevant(a)
    return arts


# ================================================================== bootstrap
def resample_idx(n, members, mode):
    if mode == "article":
        return RNG.integers(0, n, n)
    pick = RNG.integers(0, len(members), len(members))
    return np.concatenate([members[p] for p in pick]) if len(members) else np.zeros(0, int)


def boot(fn, data, cluster=True, B=None):
    """data: {group: {"_cl": labels, col: np.array}}; fn(data) -> float or None. Returns est + article (and cluster) CIs."""
    B = NB if B is None else B
    try:
        est = fn(data)
    except Exception:
        est = None
    if est is None or not math.isfinite(est):
        return {"est": None, "n": {k: int(len(v["_cl"])) for k, v in data.items()}}
    out = {"est": float(est), "n": {k: int(len(v["_cl"])) for k, v in data.items()}}
    mem = {}
    for k, v in data.items():
        cl = v["_cl"]
        u = {}
        for i, c in enumerate(cl):
            u.setdefault(c, []).append(i)
        mem[k] = [np.array(x, int) for x in u.values()]
    out["k"] = {k: len(m) for k, m in mem.items()}
    for mode in (("article", "cluster") if cluster else ("article",)):
        if mode == "cluster" and min((len(m) for m in mem.values()), default=0) < 2:
            continue
        sims = []
        for _ in range(B):
            d = {k: Lazy(v, resample_idx(len(v["_cl"]), mem[k], mode)) for k, v in data.items()}
            try:
                s = fn(d)
            except Exception:
                s = None
            if s is not None and math.isfinite(s):
                sims.append(s)
        if len(sims) >= 0.5 * B and B > 0:
            lo, hi = np.percentile(sims, [2.5, 97.5])
            if mode == "article":
                out["lo"], out["hi"] = float(lo), float(hi)
            else:
                out["cl_lo"], out["cl_hi"] = float(lo), float(hi)
    return out


class Lazy(dict):
    """One bootstrap replicate of a group: columns are indexed only when a statistic reads them."""
    def __init__(self, cols, idx):
        super().__init__()
        self._c, self._i = cols, idx

    def __missing__(self, k):
        v = self._c[k]
        v = v[self._i] if isinstance(v, np.ndarray) else v
        self[k] = v
        return v


def R(d, gname, a, b):
    x, y = d[gname][a], d[gname][b]
    m = np.isfinite(x) & np.isfinite(y)
    s = float(y[m].sum())
    return float(x[m].sum()) / s if s > 0 else None


def MEAN(d, gname, a):
    x = d[gname][a]
    x = x[np.isfinite(x)]
    return float(x.mean()) if len(x) else None


def minus(a, b):
    return None if a is None or b is None else a - b


class Ctx:
    def __init__(self, arts, M, SU, ED, out, ref):
        self.arts, self.M, self.SU, self.ED, self.out, self.ref = arts, M, SU, ED, out, ref
        self.now = str(M.get("now") or "")
        self.now_ep = ep(self.now) or time.time()
        wins = dct(M.get("windows"))
        self.W = {w: tuple(wins[w]) for w in ("w1", "w2", "war") if isinstance(wins.get(w), list) and len(wins[w]) == 2}
        self.W.setdefault("w1", ("2021-01-01T00:00:00Z", "2023-07-01T00:00:00Z"))
        self.W.setdefault("w2", ("2023-07-01T00:00:00Z", self.now or "2100"))
        self.W.setdefault("war", ("2023-10-07T00:00:00Z", self.now or "2100"))
        self.charts = {}

    def sub(self, s, groups=G2):
        return [a for a in self.arts if a.grp in groups and (s == "all" or a.rel)]

    def data(self, arts, cols, groups=G2):
        out = {}
        for gname in groups:
            ga = [a for a in arts if a.grp == gname]
            d = {"_cl": np.array([a.cl for a in ga], dtype=object)}
            for c, f in cols.items():
                vals = []
                for a in ga:
                    try:
                        v = f(a)
                    except Exception:
                        v = None
                    vals.append(np.nan if v is None else float(v))
                d[c] = np.array(vals, float)
            out[gname] = d
        return out

    def in_win(self, ts, w):
        a, b = self.W[w]
        return isinstance(ts, str) and a <= ts < b

    def chart(self, name, obj):
        self.charts[name] = obj
        return f"chart_data/{name}.json"


# ------------------------------------------------------------------ shared per-article helpers
def crit(a, k):
    return num(g(a.L, k, "crit"))


def term(a, k, t):
    return num(g(a.L, k, "c", t))


def gained(a, k0="2023-07-01", k1="now"):
    c0, c1 = crit(a, k0), crit(a, k1)
    return None if c0 is None or c1 is None else float(c1 > c0)


def lead_changed(a, k0="2023-07-01", k1="now"):
    c0, c1 = crit(a, k0), crit(a, k1)
    return None if c0 is None or c1 is None else float(c1 != c0)


def wv(a, w, *ks):
    return num(g(a.win, w, *ks))


def edits(a, w):
    if not isinstance(a.win.get(w), dict):
        return None
    return num(a.win[w].get("edits"), 0.0)


def art_at(a, k):
    return a.snap[k]["article"]


def card(cid, title, what, chart, conf, so_what, caveat, examples=None, numbers=None, extra=None):
    what = re.sub(r"\bNone\b", "n/a", what or "")
    c = {"id": cid, "title": title, "what_we_see": what, "chart": chart, "confidence": conf, "so_what": so_what,
         "caveat": caveat, "examples": examples or [], "numbers": numbers or {}}
    if extra:
        c.update(extra)
    return c


def conf_rule(primary_all, primary_rel, n_ok=True, cluster_matters=False):
    sa, sr = sig(primary_all), sig(primary_rel)
    if sa and sr and n_ok and (not cluster_matters or sig(primary_all, True) or primary_all.get("cl_lo") is None):
        return "STRONG"
    if (sa or sr) and n_ok:
        return "SUGGESTIVE"
    return "SUGGESTIVE" if n_ok else "ANECDOTE"


def both_subsets(C, fn):
    return {s: fn(C.sub(s)) for s in ("all", "relevant")}


def ngrp(arts):
    c = Counter(a.grp for a in arts)
    return f"{c.get('topic', 0):,} topic / {c.get('comparison', 0):,} comparison"


# ================================================================== card 1: who edits
ACC = ["share_age_lt30", "share_age_lt365", "share_editcount_lt500", "share_ec_now", "share_indef_now"]


def acc_num(a, w, f):
    s, n = wv(a, w, "accounts", f), wv(a, w, "accounts", "n_edits")
    return None if s is None or n is None else s * n


def acc_den(a, w, f):
    s, n = wv(a, w, "accounts", f), wv(a, w, "accounts", "n_edits")
    return None if s is None or n is None else n


def crit_events(a):
    if a.ce is not None:
        return a.ce
    out = []
    for e in lst(a.ev.get("lead_events")):
        if isinstance(e, dict) and e.get("term") in CRIT and e.get("kind") in ("insert", "remove") and isinstance(e.get("ts"), str):
            out.append(e)
    a.ce = sorted(out, key=lambda e: e["ts"])
    return a.ce


def card_who(C):
    rows, stats = [], {}
    for s in ("all", "relevant"):
        arts = C.sub(s)
        for w in ("w1", "w2", "war"):
            cols = {}
            for f in ACC:
                cols[f"{f}:n"] = lambda a, w=w, f=f: acc_num(a, w, f)
                cols[f"{f}:d"] = lambda a, w=w, f=f: acc_den(a, w, f)
            cols["anon:n"] = lambda a, w=w: wv(a, w, "anon")
            cols["anon:d"] = lambda a, w=w: edits(a, w)
            cols["age"] = lambda a, w=w: wv(a, w, "accounts", "median_age_days")
            D = C.data(arts, cols)
            for gname in G2:
                row = {"subset": s, "window": w, "group": gname, "articles": int(np.isfinite(D[gname]["anon:d"]).sum())}
                for f in ACC + ["anon"]:
                    row[f] = r3(R(D, gname, f + ":n", f + ":d"))
                ag = D[gname]["age"][np.isfinite(D[gname]["age"])]
                row["median_of_article_median_age_days"] = r3(float(np.median(ag)), 0) if len(ag) else None
                row["edits"] = int(np.nansum(D[gname]["anon:d"]))
                rows.append(row)
            if w in ("w2", "war"):
                for f in ("share_editcount_lt500", "share_age_lt30", "anon"):
                    stats[f"{s}:{w}:{f}:diff"] = boot(lambda d, f=f: minus(R(d, "topic", f + ":n", f + ":d"), R(d, "comparison", f + ":n", f + ":d")), D)
        # DiD in new-account share (w2 vs w1), resample articles once for both windows
        cols = {}
        for w in ("w1", "w2"):
            cols[f"{w}:n"] = lambda a, w=w: acc_num(a, w, "share_age_lt365")
            cols[f"{w}:d"] = lambda a, w=w: acc_den(a, w, "share_age_lt365")
        D = C.data(arts, cols)
        did = lambda d: minus(minus(R(d, "topic", "w2:n", "w2:d"), R(d, "topic", "w1:n", "w1:d")),
                              minus(R(d, "comparison", "w2:n", "w2:d"), R(d, "comparison", "w1:n", "w1:d")))
        stats[f"{s}:did_age_lt365"] = boot(did, D)
    # adders vs removers: per-event account flags (exact events by registered accounts)
    ar = []
    for s in ("all", "relevant"):
        arts = C.sub(s)
        for w in ("w1", "w2", "war"):
            for gname in G2:
                for kind in ("insert", "remove"):
                    for scope in ("all", "new_only"):
                        ev_n = acct_n = 0
                        fl = Counter(); ages = []; acc = Counter(); acc_indef = Counter(); arts_with = 0
                        base_n = base_d = 0.0
                        per_art_num, per_art_den, per_base_n, per_base_d, cls = [], [], [], [], []
                        for a in arts:
                            if a.grp != gname:
                                continue
                            evs = [e for e in crit_events(a) if e["kind"] == kind and C.in_win(e["ts"], w)
                                   and (scope == "all" or not e.get("restore"))]
                            if not evs:
                                continue
                            arts_with += 1
                            an = ad = 0
                            for e in evs:
                                ev_n += 1
                                x = e.get("acct")
                                if isinstance(x, dict):
                                    acct_n += 1; ad += 1
                                    age = num(x.get("age_d"))
                                    if age is not None:
                                        ages.append(age); fl["age_lt30"] += age < 30; fl["age_lt365"] += age < 365
                                    fl["lt500"] += bool(x.get("lt500")); fl["ec"] += bool(x.get("ext"))
                                    ind = bool(x.get("indef")); fl["indef"] += ind; an += ind
                                    fl["indef_sitewide"] += ind and not x.get("partial")
                                    fl["indef_sock"] += ind and x.get("breason") == "sock"
                                    u = e.get("u")
                                    if isinstance(u, str):
                                        acc[u] += 1
                                        if ind:
                                            acc_indef[u] += 1
                            bn, bd = acc_num(a, w, "share_indef_now"), acc_den(a, w, "share_indef_now")
                            if bn is not None and bd:
                                base_n += bn; base_d += bd
                            per_art_num.append(an); per_art_den.append(ad)
                            per_base_n.append(bn if bn is not None and bd else np.nan); per_base_d.append(bd if bn is not None and bd else np.nan)
                            cls.append(a.cl)
                        top3 = sum(v for _, v in acc_indef.most_common(3))
                        row = {"subset": s, "window": w, "group": gname, "kind": kind, "scope": scope, "articles": arts_with,
                               "events": ev_n, "events_with_account_facts": acct_n,
                               "distinct_accounts": len(acc), "distinct_indef_accounts": len(acc_indef),
                               "indef_events": fl["indef"], "indef_events_by_top3_indef_accounts": top3,
                               "share_indef": r3(fl["indef"] / acct_n) if acct_n else None,
                               "share_indef_sitewide": r3(fl["indef_sitewide"] / acct_n) if acct_n else None,
                               "share_indef_sock": r3(fl["indef_sock"] / acct_n) if acct_n else None,
                               "share_lt500": r3(fl["lt500"] / acct_n) if acct_n else None,
                               "share_ec": r3(fl["ec"] / acct_n) if acct_n else None,
                               "share_age_lt30": r3(fl["age_lt30"] / len(ages)) if ages else None,
                               "share_age_lt365": r3(fl["age_lt365"] / len(ages)) if ages else None,
                               "median_age_days": r3(float(np.median(ages)), 0) if ages else None,
                               "base_share_indef_same_articles": r3(base_n / base_d) if base_d else None}
                        if scope == "all" and acct_n >= 5:
                            D = {"x": {"_cl": np.array(cls, dtype=object), "n": np.array(per_art_num, float), "d": np.array(per_art_den, float),
                                       "bn": np.array(per_base_n, float), "bd": np.array(per_base_d, float)}}
                            row["excess_over_base"] = boot(lambda d: minus(R(d, "x", "n", "d"), R(d, "x", "bn", "bd")), D)
                        ar.append(row)
        # base rate of all editors, all group articles
        for w in ("w1", "w2", "war"):
            D = C.data(arts, {"n": lambda a, w=w: acc_num(a, w, "share_indef_now"), "d": lambda a, w=w: acc_den(a, w, "share_indef_now")})
            for gname in G2:
                ar.append({"subset": s, "window": w, "group": gname, "kind": "all_edits", "scope": "base",
                           "edits_with_account_facts": int(np.nansum(D[gname]["d"])),
                           "share_indef": r3(R(D, gname, "n", "d"))})
    fn = C.chart("01_who_edits", {"x": "window (w1 = 2021-01 to 2023-07, w2 = 2023-07 to now, war = 2023-10-07 to now)",
                                  "y": "edit-weighted share of registered non-bot edits", "rows": rows})
    fn2 = C.chart("01_adders_removers_blocked", {"note": "critical lead-term flips by registered accounts with account facts; "
                                                 "accounts are counted, never listed; base = all registered edits",
                                                 "rows": ar})
    get = lambda s, w, gname, f: next((r[f] for r in rows if r["subset"] == s and r["window"] == w and r["group"] == gname), None)
    gx = lambda s, w, gname, kind, f, scope="all": next((r.get(f) for r in ar if r["subset"] == s and r["window"] == w and r["group"] == gname
                                                         and r["kind"] == kind and r["scope"] == scope), None)
    d_all, d_rel = stats.get("all:war:share_editcount_lt500:diff"), stats.get("relevant:war:share_editcount_lt500:diff")
    what = (f"Mass tier, {ngrp(C.sub('all'))} articles. Edits by accounts with under 500 edits, war window: topic "
            f"{pct(get('all', 'war', 'topic', 'share_editcount_lt500'))}, comparison {pct(get('all', 'war', 'comparison', 'share_editcount_lt500'))} "
            f"(difference {ci_txt(d_all, 100, 1, ' pp')}; relevant subset {ci_txt(d_rel, 100, 1, ' pp')}). Accounts under a year old: topic "
            f"{pct(get('all', 'w1', 'topic', 'share_age_lt365'))} in w1 and {pct(get('all', 'w2', 'topic', 'share_age_lt365'))} in w2; comparison "
            f"{pct(get('all', 'w1', 'comparison', 'share_age_lt365'))} and {pct(get('all', 'w2', 'comparison', 'share_age_lt365'))} "
            f"(DiD {ci_txt(stats.get('all:did_age_lt365'), 100, 1, ' pp')}). Anonymous edits, war window: topic {pct(get('all', 'war', 'topic', 'anon'))}, "
            f"comparison {pct(get('all', 'war', 'comparison', 'anon'))}. Critical lead-term flips, war window, topic: "
            f"{gx('all', 'war', 'topic', 'insert', 'events')} insertions by {gx('all', 'war', 'topic', 'insert', 'distinct_accounts')} accounts, now indef-blocked: "
            f"{gx('all', 'war', 'topic', 'insert', 'distinct_indef_accounts')} ({pct(gx('all', 'war', 'topic', 'insert', 'share_indef'))} of "
            f"insertions with account facts; base rate on the same articles {pct(gx('all', 'war', 'topic', 'insert', 'base_share_indef_same_articles'))}); "
            f"{gx('all', 'war', 'topic', 'remove', 'events')} removals by {gx('all', 'war', 'topic', 'remove', 'distinct_accounts')} accounts, "
            f"{gx('all', 'war', 'topic', 'remove', 'distinct_indef_accounts')} now indef-blocked ({pct(gx('all', 'war', 'topic', 'remove', 'share_indef'))}; base "
            f"{pct(gx('all', 'war', 'topic', 'remove', 'base_share_indef_same_articles'))}). Comparison: insertions {pct(gx('all', 'war', 'comparison', 'insert', 'share_indef'))} "
            f"and removals {pct(gx('all', 'war', 'comparison', 'remove', 'share_indef'))} by now-indef accounts (base "
            f"{pct(gx('all', 'war', 'comparison', 'insert', 'base_share_indef_same_articles'))}). Pre-war (w1) topic: insertions "
            f"{pct(gx('all', 'w1', 'topic', 'insert', 'share_indef'))}, removals {pct(gx('all', 'w1', 'topic', 'remove', 'share_indef'))}, base "
            f"{pct(gx('all', 'w1', 'topic', 'insert', 'base_share_indef_same_articles'))}; the top 3 indef accounts made "
            f"{gx('all', 'w1', 'topic', 'insert', 'indef_events_by_top3_indef_accounts')} of {gx('all', 'w1', 'topic', 'insert', 'indef_events')} indef insertions.")
    ex_t = gx("all", "war", "topic", "insert", "excess_over_base") or {}
    ex_r = gx("all", "war", "topic", "remove", "excess_over_base") or {}
    what += f" Excess over base, war topic: insertions {ci_txt(ex_t, 100, 1, ' pp')}, removals {ci_txt(ex_r, 100, 1, ' pp')}."
    so = ("Topic pages are edited by more established accounts than comparison pages: fewer low-edit-count accounts. " if neg(d_all) else
          "Topic pages draw more low-edit-count accounts than comparison pages. " if pos(d_all) else
          "Topic editors are not clearly more or less established than comparison editors at this scale. ") + \
         ("Now-blocked accounts are over-represented in critical-term flips on topic leads, in both directions. " if pos(ex_t) and pos(ex_r) else
          "Now-blocked accounts are over-represented among topic insertions of critical terms. " if pos(ex_t) else
          "Now-blocked accounts are over-represented among topic removals of critical terms. " if pos(ex_r) else
          "Flips by now-blocked accounts are not clearly above the base rate of all edits on the same pages. ") + \
         "This describes who made flips, not which side they were on, and says nothing about coordination."
    return card("who_edits", "Who edits: account age and experience, and now-blocked accounts among adders and removers",
                what, {"type": "grouped bars by window, plus a table of adders vs removers", "x": "window", "y": "share of edits / of flips",
                       "series": "topic vs comparison; insert vs remove; base rate", "data": f"{fn}, {fn2}"},
                conf_rule(d_all, d_rel, True, True), so,
                "Block status and edit count are as of collection, not at the time of the edit; older windows have had more time "
                "at risk of a block. 'Insert' includes restoring a term by revert (scope new_only drops tagged restorations). "
                "Account facts exist only for exact events by registered accounts. Distinct-account counts rely on one salt per run.",
                numbers={"stats": stats})


# ================================================================== card 2: protection and CT notices
def plevel(p):
    if not isinstance(p, dict):
        return None
    e = str(p.get("edit") or "").lower()
    return {"": "none", "extendedconfirmed": "EC", "autoconfirmed": "semi", "sysop": "full", "templateeditor": "full"}.get(e, "other")


def card_protection(C):
    rows = []
    for s in ("all", "relevant"):
        arts = C.sub(s)
        for gname in G2:
            ga = [a for a in arts if a.grp == gname]
            for k in DATES:
                lv = Counter(plevel(a.snap[k].get("protection")) for a in ga if a.snap[k].get("rev") or k == "now")
                known = sum(v for kk, v in lv.items() if kk)
                rows.append({"subset": s, "group": gname, "date": k, "articles": known, **{x: r3(lv[x] / known) if known else None
                                                                                         for x in ("EC", "semi", "full", "none", "other")}})
            ct = [g(a.r, "talk_now", "ct_notice") for a in ga if isinstance(a.r.get("talk_now"), dict)]
            rows.append({"subset": s, "group": gname, "date": "now", "metric": "ct_notice", "articles": len(ct),
                         "share": r3(sum(bool(x) for x in ct) / len(ct)) if ct else None})
    # protection log actions per year (EC and other)
    yr = defaultdict(Counter)
    for a in C.sub("all"):
        for e in lst(a.ev.get("protection_log")):
            if isinstance(e, dict) and e.get("action") in ("protect", "modify") and isinstance(e.get("ts"), str):
                lev = next((d.get("level") for d in lst(e.get("details")) if isinstance(d, dict) and d.get("type") == "edit"), None)
                yr[(a.grp, e["ts"][:4])]["EC" if lev == "extendedconfirmed" else "other"] += 1
    log_rows = [{"group": gname, "year": y, **dict(c)} for (gname, y), c in sorted(yr.items())]
    # protection vs change at similar edit volume (pooled quintiles of log w2 edits)
    st, strat_rows = {}, []
    for s in ("all", "relevant"):
        arts = [a for a in C.sub(s) if gained(a) is not None and plevel(a.snap["2023-07-01"].get("protection")) is not None]
        ed = np.array([math.log1p(edits(a, "w2") or 0) for a in arts])
        qs = np.quantile(ed, [0.2, 0.4, 0.6, 0.8]) if len(ed) else []
        qbin = {id(a): int(np.searchsorted(qs, x, side="right")) for a, x in zip(arts, ed)}
        cols = {"gain": gained, "prot": lambda a: float(plevel(a.snap["2023-07-01"].get("protection")) == "EC"),
                "newprot": lambda a: float(plevel(a.snap["2023-07-01"].get("protection")) != "EC" and plevel(a.snap["now"].get("protection")) == "EC"),
                "bin": lambda a: qbin[id(a)]}
        D = C.data(arts, cols)

        def strat(d, gname, flag="prot", only_unprot_2023=False):
            x = d[gname]
            diffs, ws = [], []
            for b in range(5):
                m = x["bin"] == b
                if only_unprot_2023:
                    m = m & (x["prot"] == 0)
                p1, p0 = x["gain"][m & (x[flag] == 1)], x["gain"][m & (x[flag] == 0)]
                if len(p1) >= 3 and len(p0) >= 3:
                    diffs.append(p1.mean() - p0.mean()); ws.append(m.sum())
            return float(np.average(diffs, weights=ws)) if diffs else None
        for gname in G2:
            st[f"{s}:{gname}:ec2023_vs_not"] = boot(lambda d, gname=gname: strat(d, gname), D)
            st[f"{s}:{gname}:newly_ec_vs_not"] = boot(lambda d, gname=gname: strat(d, gname, "newprot", True), D)
        st[f"{s}:did"] = boot(lambda d: minus(strat(d, "topic"), strat(d, "comparison")), D)
        for gname in G2:
            x = D[gname]
            for b in range(5):
                for pv in (1, 0):
                    m = (x["bin"] == b) & (x["prot"] == pv)
                    strat_rows.append({"subset": s, "group": gname, "edit_quintile": b + 1, "ec_at_2023_07": bool(pv),
                                       "articles": int(m.sum()), "share_gaining": r3(float(x["gain"][m].mean())) if m.sum() else None})
    fn = C.chart("02_protection_ct", {"x": "snapshot date", "y": "share of articles by edit-protection level; CT notice share now",
                                      "rows": rows, "protection_log_actions_per_year": log_rows})
    fn2 = C.chart("02_protection_vs_change", {"x": "w2 edit-volume quintile (pooled)", "y": "share gaining lead critical terms 2023-07 to now",
                                              "series": "EC-protected at 2023-07 vs not, by group", "rows": strat_rows})
    gr = lambda s, gname, k, f: next((r.get(f) for r in rows if r["subset"] == s and r["group"] == gname and r["date"] == k and "metric" not in r), None)
    ct = lambda gname: next((r.get("share") for r in rows if r["subset"] == "all" and r["group"] == gname and r.get("metric") == "ct_notice"), None)
    a_t, a_c = st.get("all:topic:ec2023_vs_not"), st.get("all:comparison:ec2023_vs_not")
    what = (f"EC edit protection, topic: {pct(gr('all', 'topic', '2021-01-01', 'EC'))} (2021) -> {pct(gr('all', 'topic', '2023-07-01', 'EC'))} (2023-07) -> "
            f"{pct(gr('all', 'topic', 'now', 'EC'))} (now); comparison {pct(gr('all', 'comparison', '2021-01-01', 'EC'))} -> {pct(gr('all', 'comparison', '2023-07-01', 'EC'))} -> "
            f"{pct(gr('all', 'comparison', 'now', 'EC'))}. Contentious-topic notice on the talk page now: topic {pct(ct('topic'))}, comparison {pct(ct('comparison'))}. "
            f"Within pooled quintiles of post-2023 edit volume, topic pages EC-protected in Jul 2023 gained lead critical terms "
            f"{ci_txt(a_t, 100, 1, ' pp')} more often than unprotected ones; comparison {ci_txt(a_c, 100, 1, ' pp')}; difference "
            f"{ci_txt(st.get('all:did'), 100, 1, ' pp')}. Relevant subset: topic {ci_txt(st.get('relevant:topic:ec2023_vs_not'), 100, 1, ' pp')}, "
            f"comparison {ci_txt(st.get('relevant:comparison:ec2023_vs_not'), 100, 1, ' pp')}. Pages newly EC-protected after Jul 2023 vs pages "
            f"still unprotected: topic {ci_txt(st.get('all:topic:newly_ec_vs_not'), 100, 1, ' pp')}.")
    rel = sig(a_t)
    so = ("At the same edit volume, protected topic pages still changed more often, so protection marks the core pages; "
          "it is not shown to cause or block change." if rel and (a_t or {}).get("est", 0) > 0 else
          "Once edit volume is held similar, protection level is not clearly related to lead change.") + \
         " The topic's extended-confirmed restriction applies whether or not a page is technically protected."
    return card("protection_ct", "Protection and contentious-topic coverage over time, and whether protection relates to change",
                what, {"type": "line by date (EC share) plus grouped bars by edit quintile", "x": "date / edit-volume quintile",
                       "y": "share EC-protected / share gaining", "series": "topic vs comparison; protected vs not", "data": f"{fn}, {fn2}"},
                conf_rule(a_t, st.get("relevant:topic:ec2023_vs_not"), True, True), so,
                "Protection at past dates is reconstructed from the log (lower bound for old entries; 'now' is page info). CT notices are only "
                "known now. Edit quintiles are pooled over both groups; quintiles with fewer than 3 articles per arm are skipped.",
                numbers={"stats": st})


# ================================================================== card 3: RfCs and requested moves
def discussions(C, a):
    items = [d for d in lst(a.ev.get("discussions")) if isinstance(d, dict) and d.get("kind") in ("rfc", "rm")]
    return items


def card_rfc(C):
    q = defaultdict(Counter)
    have_items = any(a.ev.get("discussions") for a in C.arts)
    per = {}
    for a in C.sub("all"):
        cnt = Counter()
        if have_items:
            for d in discussions(C, a):
                ts = d.get("ts")
                if isinstance(ts, str):
                    q[(a.grp, quarter(ts))][d["kind"]] += 1
                    for w in ("w1", "w2"):
                        if C.in_win(ts, w):
                            cnt[(d["kind"], w)] += 1
                            if d["kind"] == "rm":
                                cnt[("rm_res:" + str(d.get("result") or "unknown"), w)] += 1
                            else:
                                cnt[("rfc_closed", w)] += bool(d.get("closed"))
                                cnt[("rfc_res:" + str(d.get("result") or "unknown"), w)] += 1
        else:
            for w in ("w1", "w2"):
                dw = dct(g(a.r, "discussions", w))
                cnt[("rfc", w)] += int(num(dw.get("rfc"), 0)); cnt[("rm", w)] += int(num(dw.get("rm"), 0))
                cnt[("rfc_closed", w)] += int(num(dw.get("rfc_closed"), 0))
                cnt[("rm_res:moved", w)] += int(num(dw.get("rm_moved"), 0)); cnt[("rm_res:not moved", w)] += int(num(dw.get("rm_not_moved"), 0))
        for m in lst(a.r.get("moves")):
            if isinstance(m, dict) and m.get("rm") and not (m.get("reverted") or m.get("revert_of_move")):
                for w in ("w1", "w2"):
                    cnt[("rm_moves_done", w)] += C.in_win(m.get("ts"), w)
        per[a.t] = cnt
    yrs = {w: max(0.1, ((ep(C.W[w][1]) or 0) - (ep(C.W[w][0]) or 0)) / (365.25 * DAY)) for w in ("w1", "w2")}
    rows, st = [], {}
    for s in ("all", "relevant"):
        arts = [a for a in C.sub(s) if a.r.get("discussions") is not None or a.ev.get("discussions")]
        for gname in G2:
            ga = [a for a in arts if a.grp == gname]
            for w in ("w1", "w2"):
                tot = Counter()
                for a in ga:
                    for (k, ww), v in per[a.t].items():
                        if ww == w:
                            tot[k] += v
                by_page = sorted((per[a.t][("rfc", w)] for a in ga), reverse=True)
                n_r = sum(by_page)
                top1 = sum(by_page[:max(1, len(ga) // 100)])
                rows.append({"subset": s, "group": gname, "window": w, "articles": len(ga), "rfc": tot["rfc"], "rm": tot["rm"],
                             "rfc_per_100_articles_per_year": r3(100 * tot["rfc"] / max(1, len(ga)) / yrs[w]),
                             "rm_per_100_articles_per_year": r3(100 * tot["rm"] / max(1, len(ga)) / yrs[w]),
                             "articles_with_rfc": sum(1 for x in by_page if x), "share_rfc_on_top1pct_pages": r3(top1 / n_r) if n_r else None,
                             "share_rfc_on_top5_pages": r3(sum(by_page[:5]) / n_r) if n_r else None,
                             "rfc_closed": tot["rfc_closed"], "rm_moves_done": tot["rm_moves_done"],
                             "rm_results": {k[7:]: v for k, v in tot.items() if k.startswith("rm_res:")},
                             "rfc_results": {k[8:]: v for k, v in tot.items() if k.startswith("rfc_res:")}})
        D = C.data(arts, {"w1": lambda a: per[a.t][("rfc", "w1")] / yrs["w1"], "w2": lambda a: per[a.t][("rfc", "w2")] / yrs["w2"],
                          "m1": lambda a: per[a.t][("rm", "w1")] / yrs["w1"], "m2": lambda a: per[a.t][("rm", "w2")] / yrs["w2"]})
        st[f"{s}:did_rfc_per_article_year"] = boot(lambda d: minus(minus(MEAN(d, "topic", "w2"), MEAN(d, "topic", "w1")),
                                                                    minus(MEAN(d, "comparison", "w2"), MEAN(d, "comparison", "w1"))), D)
        st[f"{s}:did_rm_per_article_year"] = boot(lambda d: minus(minus(MEAN(d, "topic", "m2"), MEAN(d, "topic", "m1")),
                                                                   minus(MEAN(d, "comparison", "m2"), MEAN(d, "comparison", "m1"))), D)
    top = sorted(((per[a.t][("rfc", "w2")], per[a.t][("rm", "w2")], a.t) for a in C.sub("all") if a.grp == "topic"), reverse=True)[:10]
    topc = sorted(((per[a.t][("rfc", "w2")], per[a.t][("rm", "w2")], a.t) for a in C.sub("all") if a.grp == "comparison"), reverse=True)[:5]
    qrows = [{"group": gname, "quarter": qq, **dict(c)} for (gname, qq), c in sorted(q.items(), key=lambda x: (x[0][0], x[0][1] or ""))
             if qq and qq >= "2021"]
    fn = C.chart("03_rfc_rm", {"x": "window / quarter", "y": "RfCs and requested moves", "rows": rows, "quarterly": qrows,
                               "top_topic_pages_w2": [{"title": t, "rfc": a_, "rm": b_} for a_, b_, t in top if a_ or b_]})
    gr = lambda s, gname, w, f: next((r.get(f) for r in rows if r["subset"] == s and r["group"] == gname and r["window"] == w), None)
    rmres = gr("all", "topic", "w2", "rm_results") or {}
    known = sum(v for k, v in rmres.items() if k != "unknown")
    what = (f"Talk pages and archives of {ngrp(C.sub('all'))} articles. RfCs: topic {gr('all', 'topic', 'w1', 'rfc')} in w1 -> {gr('all', 'topic', 'w2', 'rfc')} in w2 "
            f"({gr('all', 'topic', 'w1', 'rfc_per_100_articles_per_year')} -> {gr('all', 'topic', 'w2', 'rfc_per_100_articles_per_year')} per 100 articles per year); "
            f"comparison {gr('all', 'comparison', 'w1', 'rfc')} -> {gr('all', 'comparison', 'w2', 'rfc')} ({gr('all', 'comparison', 'w1', 'rfc_per_100_articles_per_year')} -> "
            f"{gr('all', 'comparison', 'w2', 'rfc_per_100_articles_per_year')}). DiD per article-year {ci_txt(st.get('all:did_rfc_per_article_year'), 1, 3)} "
            f"(relevant {ci_txt(st.get('relevant:did_rfc_per_article_year'), 1, 3)}). Requested moves: topic {gr('all', 'topic', 'w1', 'rm')} -> {gr('all', 'topic', 'w2', 'rm')}, "
            f"comparison {gr('all', 'comparison', 'w1', 'rm')} -> {gr('all', 'comparison', 'w2', 'rm')}. Concentration (w2, topic): {gr('all', 'topic', 'w2', 'articles_with_rfc')} "
            f"pages had an RfC; the top 5 pages hold {pct(gr('all', 'topic', 'w2', 'share_rfc_on_top5_pages'))} and the top 1% {pct(gr('all', 'topic', 'w2', 'share_rfc_on_top1pct_pages'))}. "
            f"Outcomes: {gr('all', 'topic', 'w2', 'rfc_closed')} of {gr('all', 'topic', 'w2', 'rfc')} topic w2 RfCs closed; RM results known for {known} of "
            f"{gr('all', 'topic', 'w2', 'rm')} ({', '.join(f'{k} {v}' for k, v in sorted(rmres.items(), key=lambda x: -x[1]))}); "
            f"{gr('all', 'topic', 'w2', 'rm_moves_done')} RM-tagged moves were carried out (not reverted).")
    exs = [{"article": t, "note": f"w2: {a_} RfCs, {b_} requested moves"} for a_, b_, t in top[:5] if a_ or b_]
    exs += [{"article": t, "note": f"(comparison) w2: {a_} RfCs, {b_} requested moves"} for a_, b_, t in topc[:2] if a_ or b_]
    so = ("Formal processes multiplied on topic pages after the war, but on a few pages: the battlegrounds are where RfCs happen. "
          if pos(st.get("all:did_rfc_per_article_year")) else "RfC activity did not rise clearly more on topic pages than on comparison pages. ") + \
         "Close results are parsed class labels; treat outcome shares as indicative."
    return card("rfc_rm", "RfCs and requested moves: counts by window, concentration on a few pages, and outcomes", what,
                {"type": "bars by quarter plus a Pareto of RfCs by page", "x": "quarter", "y": "RfCs / RMs started",
                 "series": "topic vs comparison", "data": fn},
                conf_rule(st.get("all:did_rfc_per_article_year"), st.get("relevant:did_rfc_per_article_year"), True, True), so,
                "Discussion dates are the first signature in each section; undated sections are excluded. Archives are capped at 60 per "
                "talk page. RM outcomes rely on the close wording; RfC results are often 'other'.",
                examples=exs, numbers={"stats": st})


# ================================================================== card 4: short descriptions and Wikidata descriptions
def sd(a, k):
    x = g(art_at(a, k) or {}, "short_desc")
    return x.strip() if isinstance(x, str) else None


def wd_desc(a, which, lang="en"):
    src = g(a.r, "wikidata_2023") if which == "2023" else g(a.r, "now", "wikidata")
    x = g(src, "descriptions", lang)
    return x.strip() if isinstance(x, str) else None


def ccount(s):
    return sum(A.count(k, s) for k in CRIT) if s else 0


def card_sd(C):
    st, rows = {}, []

    def chg(x0, x1):
        return None if x0 is None or x1 is None else float(x0.lower() != x1.lower())
    for s in ("all", "relevant"):
        arts = C.sub(s)
        cols = {"lead": lead_changed, "sd": lambda a: chg(sd(a, "2023-07-01"), sd(a, "now")),
                "wd": lambda a: chg(wd_desc(a, "2023"), wd_desc(a, "now")),
                "wd_he": lambda a: chg(wd_desc(a, "2023", "he"), wd_desc(a, "now", "he")),
                "wd_ar": lambda a: chg(wd_desc(a, "2023", "ar"), wd_desc(a, "now", "ar")),
                "sd_crit23": lambda a: None if sd(a, "2023-07-01") is None else float(ccount(sd(a, "2023-07-01")) > 0),
                "sd_critnow": lambda a: None if sd(a, "now") is None else float(ccount(sd(a, "now")) > 0)}
        D = C.data(arts, cols)

        def cond(d, gname, col, lv):
            x = d[gname]
            m = np.isfinite(x["lead"]) & np.isfinite(x[col]) & (x["lead"] == lv)
            return float(x[col][m].mean()) if m.sum() else None
        for col in ("sd", "wd"):
            for gname in G2:
                st[f"{s}:{gname}:{col}:instep_minus_base"] = boot(lambda d, gname=gname, col=col: minus(cond(d, gname, col, 1), cond(d, gname, col, 0)), D)
            st[f"{s}:{col}:did"] = boot(lambda d, col=col: minus(minus(cond(d, "topic", col, 1), cond(d, "topic", col, 0)),
                                                                minus(cond(d, "comparison", col, 1), cond(d, "comparison", col, 0))), D)
        for gname in G2:
            x = D[gname]
            rows.append({"subset": s, "group": gname,
                         "sd_changed_if_lead_changed": r3(cond(D, gname, "sd", 1)), "sd_changed_if_lead_unchanged": r3(cond(D, gname, "sd", 0)),
                         "wd_en_changed_if_lead_changed": r3(cond(D, gname, "wd", 1)), "wd_en_changed_if_lead_unchanged": r3(cond(D, gname, "wd", 0)),
                         "n_lead_changed": int(np.nansum(x["lead"] == 1)), "n_lead_unchanged": int(np.nansum(x["lead"] == 0)),
                         "sd_changed": r3(MEAN(D, gname, "sd")), "wd_en_changed": r3(MEAN(D, gname, "wd")),
                         "wd_he_changed": r3(MEAN(D, gname, "wd_he")), "wd_ar_changed": r3(MEAN(D, gname, "wd_ar")),
                         "sd_with_critical_term_2023": int(np.nansum(x["sd_crit23"])), "sd_with_critical_term_now": int(np.nansum(x["sd_critnow"])),
                         "n_sd_2023": int(np.isfinite(x["sd_crit23"]).sum()), "n_sd_now": int(np.isfinite(x["sd_critnow"]).sum())})
    # biggest moves: SD / Wikidata description gained or lost critical terms, by views
    moves = []
    for a in C.sub("all", ("topic", "comparison", "atrocity")):
        for kind, x0, x1 in (("short description", sd(a, "2023-07-01"), sd(a, "now")), ("Wikidata (en)", wd_desc(a, "2023"), wd_desc(a, "now"))):
            if x0 is None or x1 is None or x0.lower() == x1.lower():
                continue
            dc = ccount(x1) - ccount(x0)
            if dc:
                moves.append((dc, a.v12 or 0, a, kind, x0, x1))
    moves.sort(key=lambda m: -(m[1] or 0))
    ups = [m for m in moves if m[0] > 0][:8]
    downs = [m for m in moves if m[0] < 0][:4]
    exs = [{"article": m[2].t, "group": m[2].grp, "note": f"{m[3]}: '{m[4]}' -> '{m[5]}'" + (f" ({int(m[1]):,} views in the last 12 months)" if m[1] else "")}
           for m in ups + downs]
    fn = C.chart("04_sd_wikidata", {"x": "lead critical count changed 2023-07 -> now (yes/no)", "y": "share whose description also changed",
                                    "rows": rows, "moves": [{"title": m[2].t, "group": m[2].grp, "surface": m[3], "before": m[4], "after": m[5],
                                                             "critical_terms_delta": m[0], "views_12m": m[1]} for m in moves[:60]]})
    gr = lambda s, gname, f: next((r.get(f) for r in rows if r["subset"] == s and r["group"] == gname), None)
    what = (f"Articles with a short description at both Jul 2023 and now. Topic: the short description changed in "
            f"{pct(gr('all', 'topic', 'sd_changed_if_lead_changed'))} of articles whose lead critical count changed (n={gr('all', 'topic', 'n_lead_changed')}) vs "
            f"{pct(gr('all', 'topic', 'sd_changed_if_lead_unchanged'))} of the rest (difference {ci_txt(st.get('all:topic:sd:instep_minus_base'), 100, 1, ' pp')}). "
            f"Comparison: {pct(gr('all', 'comparison', 'sd_changed_if_lead_changed'))} vs {pct(gr('all', 'comparison', 'sd_changed_if_lead_unchanged'))} "
            f"({ci_txt(st.get('all:comparison:sd:instep_minus_base'), 100, 1, ' pp')}); DiD {ci_txt(st.get('all:sd:did'), 100, 1, ' pp')}, relevant "
            f"{ci_txt(st.get('relevant:sd:did'), 100, 1, ' pp')}. English Wikidata description: topic {pct(gr('all', 'topic', 'wd_en_changed_if_lead_changed'))} vs "
            f"{pct(gr('all', 'topic', 'wd_en_changed_if_lead_unchanged'))}; overall change topic {pct(gr('all', 'topic', 'wd_en_changed'))}, comparison "
            f"{pct(gr('all', 'comparison', 'wd_en_changed'))}; Hebrew {pct(gr('all', 'topic', 'wd_he_changed'))} vs {pct(gr('all', 'comparison', 'wd_he_changed'))}. "
            f"Short descriptions containing a critical term: topic {gr('all', 'topic', 'sd_with_critical_term_2023')} -> {gr('all', 'topic', 'sd_with_critical_term_now')}, "
            f"comparison {gr('all', 'comparison', 'sd_with_critical_term_2023')} -> {gr('all', 'comparison', 'sd_with_critical_term_now')}. "
            f"{len([m for m in moves if m[0] > 0])} descriptions gained a critical term and {len([m for m in moves if m[0] < 0])} lost one.")
    so = ("Descriptions move with the lead in both groups, so co-movement itself is ordinary maintenance; what matters is the few "
          "high-traffic descriptions that now carry a framing term, because search, apps and AI answers show them first."
          if not pos(st.get("all:sd:did")) else
          "Topic descriptions move with the lead more than comparison descriptions do; these reuse surfaces echo the lead change.")
    return card("sd_wikidata", "Short descriptions and Wikidata descriptions: how often they changed in step with the lead", what,
                {"type": "paired bars plus a quote table", "x": "lead changed vs not", "y": "share whose description changed",
                 "series": "topic vs comparison; short description vs Wikidata (en)", "data": fn},
                conf_rule(st.get("all:topic:sd:instep_minus_base"), st.get("relevant:topic:sd:instep_minus_base"), True), so,
                "Lead change here means the lead critical-term count changed between Jul 2023 and now; wording changes without those "
                "terms count as unchanged. Short descriptions from templates count as text; 'none' is a value. Wikidata 'now' comes "
                "from the batched resolve step.", examples=exs, numbers={"stats": st})


# ================================================================== card 5: lead citation domains
CLASSES = list(E.SOURCE_CLASSES) + ["Other"]


def refs(a, k):
    x = g(art_at(a, k) or {}, "lead_refs_resolved")
    if not isinstance(x, dict):
        return None
    tot = num(x.get("_total"))
    if tot is None:
        tot = sum(num(v, 0) for kk, v in x.items() if not str(kk).startswith("_"))
    return {**{c: num(x.get(c), 0) for c in CLASSES}, "_total": tot}


def card_cites(C):
    rows, st = [], {}
    for s in ("all", "relevant"):
        arts = [a for a in C.sub(s) if refs(a, "2023-07-01") is not None and refs(a, "now") is not None]
        cols = {"t23": lambda a: refs(a, "2023-07-01")["_total"], "tnow": lambda a: refs(a, "now")["_total"]}
        for c in CLASSES:
            cols[c + ":23"] = lambda a, c=c: refs(a, "2023-07-01")[c]
            cols[c + ":now"] = lambda a, c=c: refs(a, "now")[c]
        D = C.data(arts, cols)
        for c in CLASSES:
            ch = lambda d, gname, c=c: minus(R(d, gname, c + ":now", "tnow"), R(d, gname, c + ":23", "t23"))
            st[f"{s}:{c}:did"] = boot(lambda d, c=c, ch=ch: minus(ch(d, "topic"), ch(d, "comparison")), D,
                                      cluster=c in ("Arab & Palestinian press, pro-Palestinian outlets", "Pro-Israel advocacy", "Rights orgs & UN",
                                                    "Scholarly (books, journals)"))
            for gname in G2:
                rows.append({"subset": s, "group": gname, "class": c, "share_2023": r3(R(D, gname, c + ":23", "t23"), 4),
                             "share_now": r3(R(D, gname, c + ":now", "tnow"), 4)})
        for gname in G2:
            rows.append({"subset": s, "group": gname, "class": "_citations", "articles": int(len(D[gname]["_cl"])),
                         "total_2023": int(np.nansum(D[gname]["t23"])), "total_now": int(np.nansum(D[gname]["tnow"]))})
        # 2021 share for context (articles with all three)
        for gname in G2:
            ga = [a for a in arts if a.grp == gname and refs(a, "2021-01-01") is not None]
            tot = sum(refs(a, "2021-01-01")["_total"] for a in ga)
            for c in CLASSES:
                rows.append({"subset": s, "group": gname, "class": c, "share_2021": r3(sum(refs(a, "2021-01-01")[c] for a in ga) / tot, 4) if tot else None,
                             "articles_with_2021": len(ga)})
    # domain shifts (topic, all articles)
    dom = {gname: {k: Counter() for k in ("2023-07-01", "now")} for gname in G2}
    for a in C.sub("all"):
        if a.grp not in G2:
            continue
        for k in ("2023-07-01", "now"):
            for d_, v in dct(g(art_at(a, k) or {}, "lead_domains")).items():
                dom[a.grp][k][str(d_)] += int(num(v, 0))
    shifts = {}
    for gname in G2:
        allk = set(dom[gname]["2023-07-01"]) | set(dom[gname]["now"])
        dd = sorted(((dom[gname]["now"][k] - dom[gname]["2023-07-01"][k], k) for k in allk), reverse=True)
        shifts[gname] = [{"domain": k, "class": E.classify(k) or "Other", "2023": dom[gname]["2023-07-01"][k], "now": dom[gname]["now"][k], "delta": v}
                         for v, k in dd[:15] + dd[-10:] if v]
    fn = C.chart("05_lead_citation_classes", {"x": "source class", "y": "share of lead citations (pooled, articles present at Jul 2023 and now)",
                                              "rows": rows, "domain_shifts": shifts})
    gs = lambda s, gname, c, f: next((r.get(f) for r in rows if r["subset"] == s and r["group"] == gname and r["class"] == c and f in r), None)
    key = ["Scholarly (books, journals)", "Rights orgs & UN", "Arab & Palestinian press, pro-Palestinian outlets", "Pro-Israel advocacy", "Israeli press",
           "Western wire & papers"]
    parts = [f"{c}: topic {pct(gs('all', 'topic', c, 'share_2023'))} -> {pct(gs('all', 'topic', c, 'share_now'))}, comparison "
             f"{pct(gs('all', 'comparison', c, 'share_2023'))} -> {pct(gs('all', 'comparison', c, 'share_now'))} (DiD {ci_txt(st.get('all:' + c + ':did'), 100, 2, ' pp')})"
             for c in key]
    nt = next((r for r in rows if r["subset"] == "all" and r["group"] == "topic" and r["class"] == "_citations"), {})
    nc = next((r for r in rows if r["subset"] == "all" and r["group"] == "comparison" and r["class"] == "_citations"), {})
    what = (f"Lead citations with named refs resolved, {nt.get('articles', 0):,} topic and {nc.get('articles', 0):,} comparison articles present at Jul 2023 and now. "
            f"Topic lead citations {nt.get('total_2023')} -> {nt.get('total_now')}; comparison {nc.get('total_2023')} -> {nc.get('total_now')}. " + "; ".join(parts) +
            ". Top topic domains gained: " + ", ".join(f"{x['domain']} ({x['delta']:+d})" for x in shifts.get("topic", [])[:6] if x["delta"] > 0) + ".")
    mains = [st.get(f"all:{c}:did") for c in key[1:4]]
    anysig = any(sig(x) and sig(st.get("relevant:" + c + ":did")) for x, c in zip(mains, key[1:4]))
    so = ("The source mix behind topic leads shifted relative to comparison leads in at least one partisan or rights class; check which "
          "outlets drive it before quoting." if anysig else
          "The source mix behind topic leads moved about as comparison leads did; the reframing did not come with a visible swap of sources.")
    return card("lead_citations", "Lead citation domains: the shift in source classes behind lead sentences", what,
                {"type": "small multiples, share by source class, Jul 2023 vs now", "x": "snapshot", "y": "share of lead citations",
                 "series": "topic vs comparison", "data": fn},
                conf_rule(st.get("all:Rights orgs & UN:did"), st.get("relevant:Rights orgs & UN:did"), True, True) if anysig else "SUGGESTIVE", so,
                "Classes are the explore.py domain lists (25-50% 'Other'); 'Arab & pro-Palestinian' mixes Al Jazeera, +972 and Anadolu. "
                "Pooled shares weight citation-heavy leads; lead_domains is capped at 60 domains per lead.",
                numbers={"stats": st})


# ================================================================== card 6: categories, infobox, See also
def cats(a, k):
    x = g(art_at(a, k) or {}, "categories")
    return set(str(c) for c in x) if isinstance(x, list) else None


def ib_crit(a, k):
    ib = g(art_at(a, k) or {}, "infobox")
    if art_at(a, k) is None:
        return None
    if not isinstance(ib, dict):
        return 0
    return ccount(" ; ".join(str(v) for v in dct(ib.get("fields")).values()))


def see_also(a, k):
    x = g(art_at(a, k) or {}, "see_also")
    return [str(v) for v in x] if isinstance(x, list) else ([] if art_at(a, k) is not None else None)


def card_structure(C):
    cg = {str(k).lower(): v for k, v in dct(C.M.get("concept_groups")).items()}
    st, rows = {}, []

    def fc_add(a):
        c0, c1 = cats(a, "2023-07-01"), cats(a, "now")
        return None if c0 is None or c1 is None else len([c for c in c1 - c0 if FRAMING_CAT.search(c)])

    def fc_rem(a):
        c0, c1 = cats(a, "2023-07-01"), cats(a, "now")
        return None if c0 is None or c1 is None else len([c for c in c0 - c1 if FRAMING_CAT.search(c)])

    def ib_up(a):
        x0, x1 = ib_crit(a, "2023-07-01"), ib_crit(a, "now")
        return None if x0 is None or x1 is None else float(x1 > x0)

    def sa_concept(a, k):
        s_ = see_also(a, k)
        return None if s_ is None else len({cg[x.lower()] for x in s_ if x.lower() in cg})
    for s in ("all", "relevant"):
        arts = C.sub(s)
        cols = {"add": fc_add, "rem": fc_rem, "any_add": lambda a: None if fc_add(a) is None else float(fc_add(a) > 0), "ib_up": ib_up,
                "sa_d": lambda a: None if see_also(a, "2023-07-01") is None or see_also(a, "now") is None else len(see_also(a, "now")) - len(see_also(a, "2023-07-01")),
                "sac_d": lambda a: None if sa_concept(a, "2023-07-01") is None or sa_concept(a, "now") is None else sa_concept(a, "now") - sa_concept(a, "2023-07-01"),
                "ncat_d": lambda a: None if cats(a, "2023-07-01") is None or cats(a, "now") is None else len(cats(a, "now")) - len(cats(a, "2023-07-01"))}
        D = C.data(arts, cols)
        for c in ("any_add", "ib_up", "sac_d", "add"):
            st[f"{s}:{c}:diff"] = boot(lambda d, c=c: minus(MEAN(d, "topic", c), MEAN(d, "comparison", c)), D)
        for gname in G2:
            x = D[gname]
            rows.append({"subset": s, "group": gname, "articles": int(np.isfinite(x["add"]).sum()),
                         "framing_categories_added_per_100": r3(100 * MEAN(D, gname, "add")) if MEAN(D, gname, "add") is not None else None,
                         "framing_categories_removed_per_100": r3(100 * MEAN(D, gname, "rem")) if MEAN(D, gname, "rem") is not None else None,
                         "share_adding_framing_category": r3(MEAN(D, gname, "any_add")), "share_infobox_gained_critical": r3(MEAN(D, gname, "ib_up")),
                         "mean_see_also_change": r3(MEAN(D, gname, "sa_d")), "mean_see_also_concept_change": r3(MEAN(D, gname, "sac_d")),
                         "mean_category_count_change": r3(MEAN(D, gname, "ncat_d"))})
    added = {gname: Counter() for gname in G2}; removed = {gname: Counter() for gname in G2}
    ibx = []
    for a in C.sub("all"):
        c0, c1 = cats(a, "2023-07-01"), cats(a, "now")
        if c0 is not None and c1 is not None:
            for c in c1 - c0:
                if FRAMING_CAT.search(c):
                    added[a.grp][c] += 1
            for c in c0 - c1:
                if FRAMING_CAT.search(c):
                    removed[a.grp][c] += 1
        x0, x1 = ib_crit(a, "2023-07-01"), ib_crit(a, "now")
        if x0 is not None and x1 is not None and x1 > x0:
            f1 = dct(g(art_at(a, "now"), "infobox", "fields"))
            fld = next(((k, v) for k, v in f1.items() if ccount(str(v))), None)
            if fld:
                ibx.append((a.v12 or 0, a, fld))
    ibx.sort(key=lambda x: -x[0])
    fn = C.chart("06_categories_infobox_seealso", {"x": "group", "y": "per-article changes Jul 2023 -> now", "rows": rows,
                                                   "framing_categories_added": {k: v.most_common(25) for k, v in added.items()},
                                                   "framing_categories_removed": {k: v.most_common(25) for k, v in removed.items()}})
    gr = lambda s, gname, f: next((r.get(f) for r in rows if r["subset"] == s and r["group"] == gname), None)
    what = (f"Jul 2023 -> now. Framing categories (genocide, colonial, apartheid, occupation, massacre, terror, Zionism, antisemitism, ...) added per 100 "
            f"articles: topic {gr('all', 'topic', 'framing_categories_added_per_100')} (removed {gr('all', 'topic', 'framing_categories_removed_per_100')}), comparison "
            f"{gr('all', 'comparison', 'framing_categories_added_per_100')} (removed {gr('all', 'comparison', 'framing_categories_removed_per_100')}). Share of articles adding at "
            f"least one: topic {pct(gr('all', 'topic', 'share_adding_framing_category'))}, comparison {pct(gr('all', 'comparison', 'share_adding_framing_category'))} "
            f"(difference {ci_txt(st.get('all:any_add:diff'), 100, 2, ' pp')}; relevant {ci_txt(st.get('relevant:any_add:diff'), 100, 2, ' pp')}). Infobox fields "
            f"gained a critical term in {pct(gr('all', 'topic', 'share_infobox_gained_critical'))} of topic vs {pct(gr('all', 'comparison', 'share_infobox_gained_critical'))} "
            f"of comparison articles ({ci_txt(st.get('all:ib_up:diff'), 100, 2, ' pp')}). See also: mean change {gr('all', 'topic', 'mean_see_also_change')} links topic vs "
            f"{gr('all', 'comparison', 'mean_see_also_change')} comparison; watch-concept See-also links {ci_txt(st.get('all:sac_d:diff'), 1, 3)}. "
            "Most added topic framing categories: " + ", ".join(f"{c} ({n})" for c, n in added["topic"].most_common(6)) + ".")
    exs = [{"article": a.t, "note": f"infobox {k} now: '{str(v)[:160]}'"} for _, a, (k, v) in ibx[:5]]
    so = ("Structural reframing is visible at scale but small: a few framing categories and infobox fields per hundred topic pages."
          if pos(st.get("all:any_add:diff")) else "Categories, infoboxes and See also show no reframing at scale beyond what comparison pages show.") + \
         " Additions run in both directions (terrorist-designation and massacres-of-Jews categories count as framing too)."
    return card("structure", "Categories, infobox and See also: reframing at scale?", what,
                {"type": "dot plot per 100 articles plus a top-categories table", "x": "metric", "y": "per 100 articles / share",
                 "series": "topic vs comparison", "data": fn},
                conf_rule(st.get("all:any_add:diff"), st.get("relevant:any_add:diff"), True), so,
                "Categories are explicit [[Category:]] links only (template-added categories are missed). The framing-category regex is broad "
                "and direction-blind. Infobox fields are the stored subset (type/result/status/... or fields with a critical term).",
                examples=exs, numbers={"stats": st})


# ================================================================== card 7: concept-link diffusion
def cgroups(a, k):
    x = g(art_at(a, k) or {}, "concept_groups")
    return set(str(v) for v in x) if isinstance(x, list) else None


def card_links(C):
    st, rows = {}, []
    # articles linking to each concept group by date
    for gname in G2:
        for k in DATES:
            c = Counter()
            n = 0
            for a in C.sub("all"):
                if a.grp != gname:
                    continue
                cs = cgroups(a, k)
                if cs is None:
                    continue
                n += 1
                c.update(cs)
            rows.append({"group": gname, "date": k, "articles": n, **{x: c[x] for x in HOT_CORE + ["jewish_history", "antisemitism", "jewish_exodus"]}})
    pairs = {}

    def build_pairs(arts):
        out = []
        for a in arts:
            c0, c1 = cgroups(a, "2023-07-01"), cgroups(a, "now")
            if c0 is None or c1 is None or a.L.get("2023-07-01") is None or a.L.get("now") is None:
                continue
            for cc in HOT_CORE:
                ts = CONCEPT_TERMS[cc]
                if any((term(a, "2023-07-01", t) or 0) > 0 for t in ts):
                    continue                                   # term already in the lead: not at risk
                out.append((a, float(cc in c0), float(any((term(a, "now", t) or 0) > 0 for t in ts)), float(cc not in c0 and cc in c1)))
        return out
    for s in ("all", "relevant"):
        P = build_pairs(C.sub(s))
        pairs[s] = P
        ed = np.array([math.log1p(edits(p[0], "w2") or 0) for p in P]) if P else np.zeros(0)
        qs = np.quantile(ed, [0.25, 0.5, 0.75]) if len(ed) else []
        data = {}
        for gname in G2:
            sel = [(i, p) for i, p in enumerate(P) if p[0].grp == gname]
            # cluster = article (pairs of one article move together); second CI by project
            data[gname] = {"_cl": np.array([p[0].t for _, p in sel], dtype=object), "_proj": np.array([p[0].cl for _, p in sel], dtype=object),
                           "x": np.array([p[1] for _, p in sel]), "y": np.array([p[2] for _, p in sel]), "new": np.array([p[3] for _, p in sel]),
                           "bin": np.array([int(np.searchsorted(qs, ed[i], side="right")) for i, _ in sel], float)}

        def strat(d, gname):
            x = d[gname]
            diffs, ws = [], []
            for b in range(4):
                m = x["bin"] == b
                y1, y0 = x["y"][m & (x["x"] == 1)], x["y"][m & (x["x"] == 0)]
                if len(y1) >= 3 and len(y0) >= 3:
                    diffs.append(y1.mean() - y0.mean()); ws.append(m.sum())
            return float(np.average(diffs, weights=ws)) if diffs else None
        dart = {k: {kk: vv for kk, vv in v.items() if kk != "_proj"} for k, v in data.items()}
        dproj = {k: {**{kk: vv for kk, vv in v.items() if kk not in ("_cl", "_proj")}, "_cl": v["_proj"]} for k, v in data.items()}
        for gname in G2:
            b1 = boot(lambda d, gname=gname: strat(d, gname), dart, cluster=False)
            b2 = boot(lambda d, gname=gname: strat(d, gname), dproj, cluster=True)
            if b2.get("cl_lo") is not None:
                b1["cl_lo"], b1["cl_hi"] = b2["cl_lo"], b2["cl_hi"]
            st[f"{s}:{gname}:linked_vs_not"] = b1
            x = data[gname]
            for lab, m in (("linked_2023", x["x"] == 1), ("not_linked_2023", x["x"] == 0), ("link_added_after_2023", x["new"] == 1)):
                rows.append({"subset": s, "group": gname, "pairs": lab, "n": int(m.sum()), "share_term_in_lead_now": r3(float(x["y"][m].mean())) if m.sum() else None})
        st[f"{s}:did"] = boot(lambda d: minus(strat(d, "topic"), strat(d, "comparison")), dart, cluster=False)
    inbound = dct(C.M.get("concept_inbound_now"))
    fn = C.chart("07_concept_links", {"x": "date / exposure", "y": "articles linking to a hot-core concept; share picking up its term",
                                      "rows": rows, "inbound_links_now": inbound,
                                      "note": "alias-resolved concept groups; pair = article x hot-core concept with the concept's term absent from the lead in Jul 2023"})
    lr = lambda s, gname, lab: next((r for r in rows if r.get("subset") == s and r["group"] == gname and r.get("pairs") == lab), {})
    cnt = lambda gname, k, c: next((r.get(c) for r in rows if r["group"] == gname and r.get("date") == k and "pairs" not in r), None)
    what = (f"Alias-resolved links to hot-core concepts (Nakba/1948, Israeli apartheid, settler colonialism, Gaza genocide, occupation, genocide/ethnic cleansing). "
            f"Topic articles linking to Gaza genocide: {cnt('topic', '2021-01-01', 'gaza_genocide')} -> {cnt('topic', '2023-07-01', 'gaza_genocide')} -> {cnt('topic', 'now', 'gaza_genocide')}; "
            f"Nakba/1948: {cnt('topic', '2021-01-01', 'nakba_1948')} -> {cnt('topic', '2023-07-01', 'nakba_1948')} -> {cnt('topic', 'now', 'nakba_1948')}; Israeli apartheid "
            f"{cnt('topic', '2021-01-01', 'apartheid_il')} -> {cnt('topic', '2023-07-01', 'apartheid_il')} -> {cnt('topic', 'now', 'apartheid_il')}. Among article-concept pairs whose term "
            f"was absent from the lead in Jul 2023, topic articles that already linked to the concept picked up its term by now in "
            f"{pct(lr('all', 'topic', 'linked_2023').get('share_term_in_lead_now'))} of {lr('all', 'topic', 'linked_2023').get('n')} pairs, against "
            f"{pct(lr('all', 'topic', 'not_linked_2023').get('share_term_in_lead_now'))} of {lr('all', 'topic', 'not_linked_2023').get('n')} without the link; within edit-volume "
            f"quartiles the difference is {ci_txt(st.get('all:topic:linked_vs_not'), 100, 2, ' pp')} (comparison {ci_txt(st.get('all:comparison:linked_vs_not'), 100, 2, ' pp')}; "
            f"DiD {ci_txt(st.get('all:did'), 100, 2, ' pp')}; relevant topic {ci_txt(st.get('relevant:topic:linked_vs_not'), 100, 2, ' pp')}). Pairs where the link was added "
            f"after Jul 2023: {pct(lr('all', 'topic', 'link_added_after_2023').get('share_term_in_lead_now'))} have the term now (n={lr('all', 'topic', 'link_added_after_2023').get('n')}).")
    so = ("Linking to a hot-core concept comes before the concept's vocabulary reaching the lead more often than chance at the same edit volume; "
          "the vocabulary travels partly along links." if pos(st.get("all:topic:linked_vs_not")) else
          "Links to hot-core concepts do not clearly predict that the concept's vocabulary later reaches the lead; diffusion along links is modest.")
    return card("concept_diffusion", "Concept-link diffusion: do articles linking to the hot core later pick up its terms?", what,
                {"type": "line (articles linking per concept by date) plus bars (pick-up linked vs not)", "x": "date / exposure",
                 "y": "articles / share picking up the term", "series": "topic vs comparison", "data": fn},
                conf_rule(st.get("all:topic:linked_vs_not"), st.get("relevant:topic:linked_vs_not"), True), so,
                "We have the alias-resolved links to watch concepts at three dates, not the full link graph or hot-core outlinks, so this "
                "tests 'links to a core concept' rather than 'linked from a core article'. Pick-up is term presence in the lead (any of the "
                "concept's terms), which can also come from unrelated edits. Inbound link counts exist only for now.",
                numbers={"stats": st})


# ================================================================== card 8: edit sizes
def card_sizes(C):
    st, rows = {}, []
    months = {w: max(0.1, ((ep(C.W[w][1]) or 0) - (ep(C.W[w][0]) or 0)) / (30.44 * DAY)) for w in ("w1", "w2", "war")}
    for s in ("all", "relevant"):
        arts = C.sub(s)
        cols = {}
        for w in ("w1", "w2", "war"):
            cols[f"{w}:e"] = lambda a, w=w: edits(a, w)
            cols[f"{w}:add"] = lambda a, w=w: (wv(a, w, "bytes_added") or 0) if edits(a, w) is not None else None
            cols[f"{w}:rem"] = lambda a, w=w: (wv(a, w, "bytes_removed") or 0) if edits(a, w) is not None else None
            cols[f"{w}:ba"] = lambda a, w=w: (wv(a, w, "big_add") or 0) if edits(a, w) is not None else None
            cols[f"{w}:br"] = lambda a, w=w: (wv(a, w, "big_remove") or 0) if edits(a, w) is not None else None
        cols["gain"] = gained
        cols["lw_d"] = lambda a: None if g(a.L, "2023-07-01", "w") is None or g(a.L, "now", "w") is None else a.L["now"]["w"] - a.L["2023-07-01"]["w"]
        cols["net_w2"] = lambda a: None if edits(a, "w2") is None else (wv(a, "w2", "bytes_added") or 0) - (wv(a, "w2", "bytes_removed") or 0)
        D = C.data(arts, cols)
        for gname in G2:
            for w in ("w1", "w2", "war"):
                x = D[gname]
                e, ad, rm = np.nansum(x[f"{w}:e"]), np.nansum(x[f"{w}:add"]), np.nansum(x[f"{w}:rem"])
                n = int(np.isfinite(x[f"{w}:e"]).sum())
                rows.append({"subset": s, "group": gname, "window": w, "articles": n, "edits_per_article_month": r3(e / max(1, n) / months[w]),
                             "bytes_added": int(ad), "bytes_removed": int(rm), "removed_over_added": r3(rm / ad) if ad else None,
                             "net_bytes_per_edit": r3((ad - rm) / e, 1) if e else None,
                             "big_adds_per_1000_edits": r3(1000 * np.nansum(x[f"{w}:ba"]) / e) if e else None,
                             "big_removes_per_1000_edits": r3(1000 * np.nansum(x[f"{w}:br"]) / e) if e else None})
            x = D[gname]
            for lab, m in (("gainers", x["gain"] == 1), ("non_gainers", x["gain"] == 0)):
                lw = x["lw_d"][m & np.isfinite(x["lw_d"])]
                nb = x["net_w2"][m & np.isfinite(x["net_w2"])]
                rows.append({"subset": s, "group": gname, "window": "w2", "lead_gain": lab, "articles": int(m.sum()),
                             "median_lead_word_change": r3(float(np.median(lw)), 1) if len(lw) else None,
                             "share_lead_grew": r3(float((lw > 0).mean())) if len(lw) else None,
                             "share_lead_shrank": r3(float((lw < 0).mean())) if len(lw) else None,
                             "median_net_bytes_w2": r3(float(np.median(nb)), 0) if len(nb) else None})
        rat = lambda d, gname, w: R(d, gname, f"{w}:rem", f"{w}:add")
        st[f"{s}:did_removed_over_added"] = boot(lambda d: minus(minus(rat(d, "topic", "w2"), rat(d, "topic", "w1")),
                                                                  minus(rat(d, "comparison", "w2"), rat(d, "comparison", "w1"))), D)
        npe = lambda d, gname, w: minus(R(d, gname, f"{w}:add", f"{w}:e"), R(d, gname, f"{w}:rem", f"{w}:e"))
        st[f"{s}:did_net_bytes_per_edit"] = boot(lambda d: minus(minus(npe(d, "topic", "w2"), npe(d, "topic", "w1")),
                                                                  minus(npe(d, "comparison", "w2"), npe(d, "comparison", "w1"))), D)

        def grew(d, gname):
            x = d[gname]; m = (x["gain"] == 1) & np.isfinite(x["lw_d"])
            return float((x["lw_d"][m] > 0).mean()) if m.sum() else None
        st[f"{s}:topic_gainers_lead_grew"] = boot(lambda d: grew(d, "topic"), D)
        st[f"{s}:gainers_grew_minus_half"] = boot(lambda d: minus(grew(d, "topic"), 0.5), D)
    # events: insertions vs removals of critical terms in w2 (new only)
    evc = Counter()
    for a in C.sub("all"):
        for e in crit_events(a):
            if C.in_win(e["ts"], "w2") and not e.get("restore"):
                evc[(a.grp, e["kind"])] += 1
    fn = C.chart("08_edit_sizes", {"x": "window", "y": "edit volume and bytes", "rows": rows,
                                   "critical_lead_events_w2_new_only": {f"{k[0]}:{k[1]}": v for k, v in evc.items()}})
    gr = lambda s, gname, w, f, lg=None: next((r.get(f) for r in rows if r["subset"] == s and r["group"] == gname and r["window"] == w and r.get("lead_gain") == lg), None)
    what = (f"Edits per article-month, topic {gr('all', 'topic', 'w1', 'edits_per_article_month')} (w1) -> {gr('all', 'topic', 'w2', 'edits_per_article_month')} (w2); "
            f"comparison {gr('all', 'comparison', 'w1', 'edits_per_article_month')} -> {gr('all', 'comparison', 'w2', 'edits_per_article_month')}. Removed/added bytes, topic "
            f"{gr('all', 'topic', 'w1', 'removed_over_added')} -> {gr('all', 'topic', 'w2', 'removed_over_added')}, comparison {gr('all', 'comparison', 'w1', 'removed_over_added')} -> "
            f"{gr('all', 'comparison', 'w2', 'removed_over_added')} (DiD {ci_txt(st.get('all:did_removed_over_added'), 1, 3)}; relevant {ci_txt(st.get('relevant:did_removed_over_added'), 1, 3)}). "
            f"Net bytes per edit, topic {gr('all', 'topic', 'w1', 'net_bytes_per_edit')} -> {gr('all', 'topic', 'w2', 'net_bytes_per_edit')}; comparison "
            f"{gr('all', 'comparison', 'w1', 'net_bytes_per_edit')} -> {gr('all', 'comparison', 'w2', 'net_bytes_per_edit')}. Topic articles whose lead gained critical terms "
            f"(n={gr('all', 'topic', 'w2', 'articles', 'gainers')}): the lead grew in {pct(gr('all', 'topic', 'w2', 'share_lead_grew', 'gainers'))} "
            f"(median {gr('all', 'topic', 'w2', 'median_lead_word_change', 'gainers')} words; {ci_pct(st.get('all:topic_gainers_lead_grew'))}) vs "
            f"{pct(gr('all', 'topic', 'w2', 'share_lead_grew', 'non_gainers'))} of non-gainers; comparison gainers {pct(gr('all', 'comparison', 'w2', 'share_lead_grew', 'gainers'))}. "
            f"New (non-restore) critical lead events in w2: topic {evc[('topic', 'insert')]} insertions vs {evc[('topic', 'remove')]} removals; comparison "
            f"{evc[('comparison', 'insert')]} vs {evc[('comparison', 'remove')]}.")
    so = ("Change came mostly as added text: leads that gained critical terms usually grew, and removal did not rise relative to addition."
          if (gr("all", "topic", "w2", "share_lead_grew", "gainers") or 0) > 0.5 and not (sig(st.get("all:did_removed_over_added")) and st["all:did_removed_over_added"]["est"] > 0)
          else "Gaining leads did not mostly grow, or removal rose relative to addition: part of the change came as rewriting, not only as added text.")
    return card("edit_sizes", "Edit sizes: added vs removed bytes, and whether change comes as added text", what,
                {"type": "grouped bars by window plus a gainers/non-gainers panel", "x": "window", "y": "edits per article-month; removed/added",
                 "series": "topic vs comparison", "data": fn},
                conf_rule(st.get("all:gainers_grew_minus_half"), st.get("relevant:gainers_grew_minus_half"), True), so,
                "Byte deltas are revision-size differences (a move or a revert counts as add/remove). Lead growth is in prose words "
                "between two snapshots and cannot separate added sentences from rewrites of equal length.", numbers={"stats": st})


# ================================================================== card 9: lead term events (ratchet at scale)
def term_sequences(C, a):
    """{term: [event dicts with 'surv' (s) and 'cens']} plus final presence per term."""
    seqs = defaultdict(list)
    for e in crit_events(a):
        t = ep(e["ts"])
        if t is not None:
            seqs[e["term"]].append({**e, "t": t})
    for tm, ev in seqs.items():
        for i, e in enumerate(ev):
            nxt = ev[i + 1]["t"] if i + 1 < len(ev) else None
            e["surv"] = (nxt or C.now_ep) - e["t"]; e["cens"] = nxt is None
    return seqs


def archetype(ev, present_start):
    n = len(ev)
    if n == 0:
        return "frozen"
    if n == 1:
        return "single step"
    if n == 2:
        return "tried & reverted" if ev[0]["surv"] < 30 * DAY else "two steps"
    return "back-and-forth" if n <= 5 else "tug-of-war"


def km_at(durs, cens, d):
    if not durs:
        return None
    order = np.argsort(durs)
    durs, cens = np.asarray(durs)[order], np.asarray(cens)[order]
    s, n = 1.0, len(durs)
    for i in range(len(durs)):
        if durs[i] > d:
            break
        if not cens[i]:
            s *= 1 - 1 / n
        n -= 1
        if n <= 0:
            break
    return s


def card_events(C):
    per = {}
    arch = {gname: Counter() for gname in G2}
    stick = {gname: [] for gname in G2}
    flips = {gname: Counter() for gname in G2}
    km = {(gname, k): ([], []) for gname in G2 for k in ("insert", "remove")}
    exact = Counter()
    for a in C.sub("all"):
        te = a.r.get("term_events")
        if a.grp not in G2 or not isinstance(te, dict):
            continue
        seqs = term_sequences(C, a)
        c = Counter()
        for tm in CRIT:
            ev = seqs.get(tm, [])
            p0 = (term(a, "2021-01-01", tm) or 0) > 0
            arch[a.grp][archetype(ev, p0)] += 1
            flips[a.grp][a.t] += len(ev)
            for e in ev:
                exact[(a.grp, bool(e.get("exact")))] += 1
                k = e["kind"]
                km[(a.grp, k)][0].append(e["surv"]); km[(a.grp, k)][1].append(e["cens"])
                for d in (1, 7, 30, 90):
                    if not (e["cens"] and e["surv"] < d * DAY):
                        c[f"{k}:{d}:el"] += 1; c[f"{k}:{d}:ok"] += e["surv"] >= d * DAY
                        if not e.get("restore"):
                            c[f"{k}:{d}:el:new"] += 1; c[f"{k}:{d}:ok:new"] += e["surv"] >= d * DAY
                        for w in ("w1", "w2"):
                            if C.in_win(e["ts"], w):
                                c[f"{k}:{d}:el:{w}"] += 1; c[f"{k}:{d}:ok:{w}"] += e["surv"] >= d * DAY
            ins = [e for e in ev if e["kind"] == "insert"]
            final_present = ev[-1]["kind"] == "insert" if ev else p0
            if final_present and ins and ev[-1]["kind"] == "insert":
                fail = [e for e in ins[:-1] if e["surv"] < 30 * DAY]
                eds = {e.get("u") for e in fail + [ins[-1]] if isinstance(e.get("u"), str)}
                stick[a.grp].append({"failed": len(fail), "editors": len(eds), "days": (ins[-1]["t"] - ins[0]["t"]) / DAY,
                                     "held_30d": ins[-1]["surv"] >= 30 * DAY})
            c["events"] += len(ev)
        c["has_te"] = 1
        per[a.t] = c
    st, srows = {}, []
    for s in ("all", "relevant"):
        arts = [a for a in C.sub(s) if a.t in per]
        cols = {"events": lambda a: per[a.t]["events"]}
        for k in ("insert", "remove"):
            for d in (1, 7, 30, 90):
                for suf in ("", ":new", ":w1", ":w2"):
                    cols[f"{k}:{d}:el{suf}"] = lambda a, k=k, d=d, suf=suf: per[a.t][f"{k}:{d}:el{suf}"]
                    cols[f"{k}:{d}:ok{suf}"] = lambda a, k=k, d=d, suf=suf: per[a.t][f"{k}:{d}:ok{suf}"]
        D = C.data(arts, cols)
        sv = lambda d, gname, k, dd=30, suf="": R(d, gname, f"{k}:{dd}:ok{suf}", f"{k}:{dd}:el{suf}")
        for gname in G2:
            st[f"{s}:{gname}:asym30"] = boot(lambda d, gname=gname: minus(sv(d, gname, "insert"), sv(d, gname, "remove")), D)
            for k in ("insert", "remove"):
                for suf in ("", ":new", ":w1", ":w2"):
                    srows.append({"subset": s, "group": gname, "kind": k, "events": suf.strip(":") or "all",
                                  **{f"{d}d": r3(sv(D, gname, k, d, suf)) for d in (1, 7, 30, 90)},
                                  "n_30d": int(np.nansum(D[gname][f"{k}:30:el{suf}"]))})
        st[f"{s}:insert30_diff"] = boot(lambda d: minus(sv(d, "topic", "insert"), sv(d, "comparison", "insert")), D)
        st[f"{s}:asym_did"] = boot(lambda d: minus(minus(sv(d, "topic", "insert"), sv(d, "topic", "remove")),
                                                  minus(sv(d, "comparison", "insert"), sv(d, "comparison", "remove"))), D)
        st[f"{s}:events_per_article_diff"] = boot(lambda d: minus(MEAN(d, "topic", "events"), MEAN(d, "comparison", "events")), D)
    # entries / exits 2021 -> now (article-term pairs), all and key articles
    ee = {}
    for lab, keys in (("all", None), ("key", set(KEY_ARTICLES) | set(KEY_ARTICLES_CONTROL))):
        for gname in G2:
            ent = lft = n = 0
            for a in C.sub("all"):
                if a.grp != gname or (keys and a.t not in keys) or a.L.get("2021-01-01") is None or a.L.get("now") is None:
                    continue
                n += 1
                for tm in CRIT:
                    p0, p1 = (term(a, "2021-01-01", tm) or 0) > 0, (term(a, "now", tm) or 0) > 0
                    ent += (not p0) and p1; lft += p0 and not p1
            ee[f"{lab}:{gname}"] = {"articles": n, "entered": ent, "left": lft}
    sk = {gname: {"pairs_stuck": len(v), "mean_failed_before_stick": r3(float(np.mean([x["failed"] for x in v]))) if v else None,
                  "share_after_retries": r3(float(np.mean([x["failed"] > 0 for x in v]))) if v else None,
                  "mean_editors_in_attempts": r3(float(np.mean([x["editors"] for x in v]))) if v else None,
                  "median_days_first_try_to_stick": r3(float(np.median([x["days"] for x in v])), 1) if v else None,
                  "median_days_if_retried": r3(float(np.median([x["days"] for x in v if x["failed"]])), 1) if any(x["failed"] for x in v) else None,
                  "pairs_stuck_and_held_30d": sum(x["held_30d"] for x in v)} for gname, v in stick.items()}
    kmr = {f"{gname}:{k}": {f"{d}d": r3(km_at(*km[(gname, k)], d * DAY)) for d in (1, 7, 30, 90)} for gname in G2 for k in ("insert", "remove")}
    conc = {}
    for gname in G2:
        tot = sum(flips[gname].values())
        top = flips[gname].most_common(5)
        conc[gname] = {"flips": tot, "top4_share": r3(sum(v for _, v in top[:4]) / tot) if tot else None, "top5": top}
    fn = C.chart("09_lead_term_events", {"x": "days after the event", "y": "share still standing", "survival": srows,
                                         "kaplan_meier": kmr, "archetypes": {k: dict(v) for k, v in arch.items()}, "stick": sk,
                                         "entries_exits": ee, "flip_concentration": conc,
                                         "ratchet_reference": RATCHET_REF, "exact_events": {f"{k[0]}:{'exact' if k[1] else 'interval'}": v for k, v in exact.items()}})
    sr = lambda s, gname, k, f, ev="all": next((r.get(f) for r in srows if r["subset"] == s and r["group"] == gname and r["kind"] == k and r["events"] == ev), None)
    nart = {gname: sum(1 for a in C.sub("all") if a.grp == gname and a.t in per) for gname in G2}
    epa = {gname: (sum(per[a.t]["events"] for a in C.sub("all") if a.grp == gname and a.t in per) / nart[gname]) if nart[gname] else None for gname in G2}
    epa_act = {}
    for gname in G2:
        xs = [per[a.t]["events"] for a in C.sub("all") if a.grp == gname and a.t in per and per[a.t]["events"]]
        epa_act[gname] = (sum(xs) / len(xs), len(xs)) if xs else (None, 0)
    what = (f"Exact lead term events, one continuous sequence 2021 -> now, {nart['topic']:,} topic and {nart['comparison']:,} comparison articles "
            f"({sum(v for k, v in exact.items() if k[1]):,} exact events, {sum(v for k, v in exact.items() if not k[1]):,} attributed to an interval). "
            f"30-day survival of critical insertions: topic {pct(sr('all', 'topic', 'insert', '30d'))}, comparison {pct(sr('all', 'comparison', 'insert', '30d'))} "
            f"(difference {ci_txt(st.get('all:insert30_diff'), 100, 1, ' pp')}); removals {pct(sr('all', 'topic', 'remove', '30d'))} vs {pct(sr('all', 'comparison', 'remove', '30d'))}. "
            f"Asymmetry (insert minus remove survival): topic {ci_txt(st.get('all:topic:asym30'), 1, 2)}, comparison {ci_txt(st.get('all:comparison:asym30'), 1, 2)}; "
            f"relevant subset topic {ci_txt(st.get('relevant:topic:asym30'), 1, 2)}. New (non-restore) insertions survive 30 days {pct(sr('all', 'topic', 'insert', '30d', 'new'))} "
            f"topic vs {pct(sr('all', 'comparison', 'insert', '30d', 'new'))} comparison; Kaplan-Meier 30-day: {pct(kmr['topic:insert']['30d'])} vs {pct(kmr['comparison:insert']['30d'])}. "
            f"Terms that stuck: {sk['topic']['pairs_stuck']} topic article-term pairs after {sk['topic']['mean_failed_before_stick']} failed tries on average "
            f"({pct(sk['topic']['share_after_retries'])} after retries, {sk['topic']['mean_editors_in_attempts']} editors per pair, median "
            f"{sk['topic']['median_days_if_retried']} days from first try when retried); comparison {sk['comparison']['pairs_stuck']} pairs, "
            f"{sk['comparison']['mean_failed_before_stick']} failed tries. Events per article: topic {r3(epa['topic'], 2)}, comparison {r3(epa['comparison'], 2)} "
            f"(among articles with any event: {r3(epa_act['topic'][0], 1)} vs {r3(epa_act['comparison'][0], 1)}). Article-terms entering vs leaving the lead 2021 -> now: "
            f"topic {ee['all:topic']['entered']} in / {ee['all:topic']['left']} out, comparison {ee['all:comparison']['entered']} / {ee['all:comparison']['left']}; key articles "
            f"{ee['key:topic']['entered']} / {ee['key:topic']['left']} vs {ee['key:comparison']['entered']} / {ee['key:comparison']['left']}. The top 4 topic pages hold "
            f"{pct(conc['topic']['top4_share'])} of topic flips. Archetypes among topic pairs with events: " +
            ", ".join(f"{k} {v}" for k, v in arch["topic"].most_common() if k != "frozen") + ". Ratchet (25 + 15 key leads): insertions 36% vs 56% at 30 days, "
            "asymmetry +0.07 vs +0.28, 3.3 vs 1.4 failed tries, 25 in / 6 out vs 4 / 5.")
    lower = st.get("all:insert30_diff") and st["all:insert30_diff"].get("est") is not None and st["all:insert30_diff"]["est"] < 0
    so = ("At scale, as in the key-article ratchet, topic insertions survive less well than comparison insertions: more churn, not a stronger "
          "push-until-it-sticks mechanism." if lower else
          "At scale, topic insertions do not survive worse than comparison insertions, unlike in the key-article ratchet; the ratchet result may be "
          "specific to the battlegrounds.") + " Persistence describes these leads; it is not shown to be the mechanism."
    return card("lead_events", "Exact lead term events: survival, time to stick, failed attempts and archetypes, against the ratchet", what,
                {"type": "survival curves (1/7/30/90 days) plus stacked archetype bars", "x": "days after the event", "y": "share still standing",
                 "series": "insert vs remove x topic vs comparison", "data": fn},
                conf_rule(st.get("all:insert30_diff"), st.get("relevant:insert30_diff"), True, True), so,
                "Events are presence flips of each critical term in section 0; one rewrite can flip several terms. Survival uses the ratchet "
                "rule (events censored before d days are excluded); Kaplan-Meier is given for comparison. Interval (non-exact) events carry "
                "the interval's end time. Archetypes are our definitions (0 events frozen, 1 single step, 2 tried & reverted if the first "
                "lasted < 30 days else two steps, 3-5 back-and-forth, 6+ tug-of-war). Restorations are tagged by revert tags or sha1 reuse.",
                numbers={"stats": st, "stick": sk, "kaplan_meier": kmr, "entries_exits": ee})


# ================================================================== card 10: pageviews exposure
def card_views(C):
    st, rows = {}, []
    for s in ("all", "relevant"):
        arts = [a for a in C.sub(s) if a.v12 is not None]
        D = C.data(arts, {"v": lambda a: a.v12, "gain": gained, "chg": lead_changed,
                          "vg": lambda a: None if gained(a) is None else a.v12 * gained(a),
                          "vc": lambda a: None if lead_changed(a) is None else a.v12 * lead_changed(a),
                          "vl": lambda a: None if crit(a, "now") is None or crit(a, "2023-07-01") is None else a.v12 * float(crit(a, "now") < crit(a, "2023-07-01"))})
        for gname in G2:
            st[f"{s}:{gname}:view_share_gained"] = boot(lambda d, gname=gname: R(d, gname, "vg", "v"), D)
            x = D[gname]
            rows.append({"subset": s, "group": gname, "articles": int(np.isfinite(x["gain"]).sum()), "share_articles_gained": r3(MEAN(D, gname, "gain")),
                         "share_views_gained": r3(R(D, gname, "vg", "v")), "share_views_changed": r3(R(D, gname, "vc", "v")),
                         "share_views_lost": r3(R(D, gname, "vl", "v")), "views_12m": int(np.nansum(x["v"]))})
        st[f"{s}:did_views_minus_articles"] = boot(lambda d: minus(minus(R(d, "topic", "vg", "v"), MEAN(d, "topic", "gain")),
                                                                    minus(R(d, "comparison", "vg", "v"), MEAN(d, "comparison", "gain"))), D)
    # former titles: share of all-period views under former titles, exposure with vs without them
    ft = {}
    for gname in G2:
        tot = cur = gtot = gcur = 0.0
        n_with = 0
        for a in C.sub("all"):
            if a.grp != gname or not a.tbt:
                continue
            vals = [v for v in a.tbt.values() if v is not None]
            if not vals:
                continue
            t_all = sum(vals); t_cur = a.tbt.get(a.titles[0] if a.titles else a.t) or a.tbt.get(a.t) or 0.0
            n_with += len(a.tbt) > 1
            tot += t_all; cur += t_cur
            if gained(a) == 1:
                gtot += t_all; gcur += t_cur
        ft[gname] = {"articles_with_former_titles": n_with, "share_views_under_former_titles": r3(1 - cur / tot) if tot else None,
                     "exposure_share_all_titles": r3(gtot / tot) if tot else None, "exposure_share_current_title_only": r3(gcur / cur) if cur else None}
    top = sorted((a for a in C.sub("all") if a.grp == "topic" and gained(a) == 1 and a.v12), key=lambda a: -a.v12)[:10]
    fn = C.chart("10_pageviews_exposure", {"x": "group", "y": "share of last-12-month views on articles whose lead gained critical terms (Jul 2023 -> now)",
                                           "rows": rows, "former_titles": ft,
                                           "top_topic_gainers_by_views": [{"title": a.t, "views_12m": int(a.v12), "lead_critical_2023": crit(a, "2023-07-01"),
                                                                           "lead_critical_now": crit(a, "now")} for a in top]})
    gr = lambda s, gname, f: next((r.get(f) for r in rows if r["subset"] == s and r["group"] == gname), None)
    what = (f"Monthly user views summed over current and former titles, last 12 complete months. Topic: {pct(gr('all', 'topic', 'share_articles_gained'))} of articles "
            f"gained lead critical terms since Jul 2023 and they carry {ci_pct(st.get('all:topic:view_share_gained'))} of topic views "
            f"({gr('all', 'topic', 'views_12m'):,} views); comparison {pct(gr('all', 'comparison', 'share_articles_gained'))} of articles carry "
            f"{ci_pct(st.get('all:comparison:view_share_gained'))} of views. Views meeting any changed lead count (gain or loss): topic "
            f"{pct(gr('all', 'topic', 'share_views_changed'))}, comparison {pct(gr('all', 'comparison', 'share_views_changed'))}; leads that lost terms: topic "
            f"{pct(gr('all', 'topic', 'share_views_lost'))}. Views-share minus article-share, DiD {ci_txt(st.get('all:did_views_minus_articles'), 100, 1, ' pp')} "
            f"(relevant {ci_txt(st.get('relevant:did_views_minus_articles'), 100, 1, ' pp')}). Former titles hold {pct(ft['topic']['share_views_under_former_titles'])} of topic "
            f"views since 2021 ({ft['topic']['articles_with_former_titles']} articles); counting them moves the gainers' all-period view share from "
            f"{pct(ft['topic']['exposure_share_current_title_only'])} (current title only) to {pct(ft['topic']['exposure_share_all_titles'])}.")
    exs = [{"article": a.t, "note": f"{int(a.v12):,} views in the last 12 months; lead critical terms {int(crit(a, '2023-07-01') or 0)} -> {int(crit(a, 'now') or 0)}"} for a in top[:5]]
    hi = (st.get("all:topic:view_share_gained") or {}).get("est")
    so = ("Count articles and the change is small; count readers and it is about four times larger: the few changed topic leads carry roughly 15% of topic reading, against 5% in comparison articles."
          if hi is not None and hi > (gr("all", "topic", "share_articles_gained") or 1) * 1.5 else
          "Reader exposure to changed leads is roughly proportional to the number of changed articles.")
    return card("pageviews_exposure", "Pageviews exposure: the share of reader views that now meet changed leads, former titles included", what,
                {"type": "paired bars (share of articles vs share of views)", "x": "group", "y": "share", "series": "articles vs views; topic vs comparison",
                 "data": fn},
                conf_rule(st.get("all:did_views_minus_articles"), st.get("relevant:did_views_minus_articles"), True, True), so,
                "A handful of very large pages drive the view share; the project-cluster CI shows how much. Views are by month, not by "
                "revision, so 'meet' means the article's lead differs now from Jul 2023, not that each reader saw the new wording.",
                examples=exs, numbers={"stats": st, "former_titles": ft})


# ================================================================== card 11: atrocity voice
def voice(text):
    if not isinstance(text, str) or not text.strip():
        return None, None, None
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    sents = [s for p in paras for s in A.sentences(p)]
    gs = [s for s in sents if A.count("genocide", s) > 0]
    fs = next((s for p in paras if len(WORD.findall(p)) >= 5 for s in A.sentences(p)[:1]), None)
    fsv = None if fs is None else ("absent" if A.count("genocide", fs) == 0 else ("attributed" if ATTR.search(fs) else "stated"))
    if not gs:
        return "absent", fsv, None
    stated = [s for s in gs if not ATTR.search(s)]
    return ("stated" if stated else "attributed"), fsv, (stated or gs)[0][:300]


def card_atrocity(C, LD):
    leads = dct(LD.get("leads"))
    ldates = [str(x) for x in lst(LD.get("dates"))]
    sel = [a for a in C.arts if a.case or (a.grp == "topic" and GAZA_RX.match(a.t)) or a.t == "Armenian genocide"]
    rows = []
    for a in sel:
        ls = leads.get(a.t) if isinstance(leads.get(a.t), list) else []
        row = {"title": a.t, "set": a.case or ("gaza" if a.grp == "topic" else "reference"), "group": a.grp}
        for i, k in enumerate(DATES):
            j = ldates.index(k) if k in ldates else i
            txt = ls[j] if j < len(ls) else None
            v, fsv, ex = voice(txt)
            row[f"lead_{k}"] = v; row[f"first_sentence_{k}"] = fsv
            if k == "now":
                row["example_now"] = ex
            if k == "2023-07-01":
                row["example_2023"] = ex
            tt = a.snap[k].get("title")
            row[f"title_{k}"] = (("stated" if A.count("genocide", tt) else "absent") if isinstance(tt, str) else None)
            sdx = sd(a, k)
            row[f"sd_{k}"] = None if sdx is None else ("absent" if not A.count("genocide", sdx) else ("attributed" if ATTR.search(sdx) else "stated"))
            cs = cats(a, k)
            row[f"genocide_categories_{k}"] = None if cs is None else sum(1 for c in cs if re.search(r"genocid", c, re.I))
            ib = dct(g(art_at(a, k) or {}, "infobox", "fields"))
            row[f"infobox_genocide_{k}"] = None if art_at(a, k) is None else any(A.count("genocide", str(v)) for v in ib.values())
        for lab, src in (("2023", g(a.r, "wikidata_2023")), ("now", g(a.r, "now", "wikidata"))):
            d = g(src, "descriptions", "en")
            row[f"wikidata_en_{lab}"] = None if not isinstance(d, str) else ("absent" if not A.count("genocide", d) else ("attributed" if ATTR.search(d) else "stated"))
        gev = [e for e in crit_events(a) if e["term"] == "genocide"]
        row["genocide_lead_events"] = len(gev)
        row["first_genocide_insert"] = next((e["ts"][:10] for e in gev if e["kind"] == "insert"), None)
        last = gev[-1] if gev else None
        row["last_genocide_event"] = f"{last['kind']} {last['ts'][:10]}" if last else None
        mv = [m for m in lst(a.r.get("moves")) if isinstance(m, dict) and not (m.get("reverted") or m.get("revert_of_move"))
              and (A.count("genocide", str(m.get("to"))) != A.count("genocide", str(m.get("from"))))]
        row["genocide_title_moves"] = [f"{m.get('ts', '')[:10]}: {'to' if A.count('genocide', str(m.get('to'))) else 'away from'} a genocide title"
                                       + (" (RM)" if m.get("rm") else "") for m in mv][:5]
        row["created_in_window"] = a.r.get("created_in_window")
        rows.append(row)
    fn = C.chart("11_atrocity_voice", {"note": "voice of the genocide label: stated (Wikipedia's voice), attributed (hedge/attribution in the sentence), absent",
                                       "rows": rows})
    cnt = lambda k, sets: Counter(r[f"lead_{k}"] for r in rows if r["set"] in sets)
    atro = {r["set"] for r in rows if r["set"] not in ("gaza", "reference")}
    gz = [r for r in rows if r["set"] == "gaza"]
    what = (f"{len([r for r in rows if r['set'] in atro])} atrocity-set pages across {len(atro)} cases, {len(gz)} Gaza pages and "
            f"{len([r for r in rows if r['set'] == 'reference'])} reference page(s). Lead voice of 'genocide' in the atrocity set, 2021 / 2023 / now: " +
            " / ".join(", ".join(f"{k} {v}" for k, v in sorted(cnt(d, atro).items(), key=lambda x: str(x[0]))) for d in DATES) + ". Gaza: " +
            "; ".join(f"{r['title']}: {r['lead_2021-01-01']} -> {r['lead_2023-07-01']} -> {r['lead_now']} (first sentence now {r['first_sentence_now']}; "
                      f"title {r['title_now']}; first lead insert {r['first_genocide_insert']}; {r['genocide_lead_events']} genocide flips)" for r in gz) + ".")
    exs = []
    for r in rows:
        if r.get("example_now"):
            exs.append({"article": r["title"], "note": f"[{r['set']}] lead now {r['lead_now']} (2023: {r['lead_2023-07-01']}); "
                                                       f"short description {r['sd_now']}; Wikidata {r['wikidata_en_now']}; '{r['example_now']}'"})
    return card("atrocity_voice", "Atrocity comparison: voice of the genocide label, stated vs attributed, across the atrocity set and Gaza", what,
                {"type": "table / heat strip, one row per page, columns = surfaces x dates", "x": "surface x date", "y": "page",
                 "series": "stated / attributed / absent", "data": fn}, "ANECDOTE",
                "Stating 'genocide' in Wikipedia's voice is the comparison to make page by page: check whether Gaza differs in timing and "
                "in how far the label reached (title, short description, infobox, categories) rather than in the label itself.",
                "Voice is a rule-based classifier (a hedge or attribution word in the same sentence = attributed); it misreads denials and "
                "quotations and needs hand checking before quoting. n is a few pages per case.", examples=exs[:12])


# ================================================================== card 12: narrative residual (event filter)
REF_RX = re.compile(r"^\s*(pre-war|post-war)\s+\S+\s+(unfiltered|narrative residual|event sentences)\s+topic ([+-]?\d+\.\d+) comp ([+-]?\d+\.\d+) "
                    r"DiD ([+-]?\d+\.\d+) \[([+-]?\d+\.\d+),([+-]?\d+\.\d+)\] n=(\d+),(\d+)")


def parse_ref(path):
    if not path or not os.path.exists(path):
        return {}
    out, sec = {}, None
    for line in open(path, encoding="utf-8"):
        if line.startswith("=="):
            sec = "relevant" if "RELEVANT" in line else "all"; continue
        m = REF_RX.match(line)
        if m and sec:
            out[(sec, m.group(1), m.group(2))] = {"topic": float(m.group(3)), "comp": float(m.group(4)), "did": float(m.group(5)),
                                                  "lo": float(m.group(6)), "hi": float(m.group(7)), "n_t": int(m.group(8)), "n_c": int(m.group(9))}
    return out


def card_residual(C):
    ref = parse_ref(C.ref)
    src = Counter(g(a.L, k, "src") for a in C.sub("all") for k in DATES)
    use = "text" if src.get("text") else None          # with a leads file, only text-based leads (as in the reference)
    ok = lambda a: all(a.L.get(k) is not None and a.L[k].get("res") is not None and a.L[k]["w"] >= 20
                       and (use is None or a.L[k].get("src") == use) for k in DATES)
    lines, res, cmp_rows = [], {}, []
    allok = [a for a in C.sub("all") if ok(a)]
    lines.append(f"articles with 3 leads: {len(allok)} {dict(Counter(a.grp for a in allok))}")
    for s in ("all", "relevant"):
        arts = [a for a in C.sub(s) if ok(a)]
        lines.append(f"== {s.upper()}")
        rate = lambda a, k, f: a.L[k][f] * 1e4 / a.L[k]["w"]
        cols = {}
        for wn, k0, k1 in (("pre-war", "2021-01-01", "2023-07-01"), ("post-war", "2023-07-01", "now")):
            for lab, f in (("unfiltered", "crit"), ("narrative residual", "res"), ("event sentences", "ev")):
                cols[f"{wn}|{lab}"] = lambda a, k0=k0, k1=k1, f=f: rate(a, k1, f) - rate(a, k0, f)
        for k in DATES:
            cols[f"evs|{k}"] = lambda a, k=k: a.L[k].get("evs")
        D = C.data(arts, cols)
        for wn, rng_ in (("pre-war", "2021→2023-07"), ("post-war", "2023-07→now")):
            for lab in ("unfiltered", "narrative residual", "event sentences"):
                c = f"{wn}|{lab}"
                b = boot(lambda d, c=c: minus(MEAN(d, "topic", c), MEAN(d, "comparison", c)), D)
                mt, mc = MEAN(D, "topic", c), MEAN(D, "comparison", c)
                res[f"{s}:{wn}:{lab}"] = {**b, "topic": mt, "comp": mc}
                nt, nc = int(np.isfinite(D["topic"][c]).sum()), int(np.isfinite(D["comparison"][c]).sum())
                if b.get("est") is not None:
                    lines.append(f"  {wn:9} {rng_:20} {lab:20} topic {mt:+.2f} comp {mc:+.2f} DiD {b['est']:+.2f} "
                                 f"[{b.get('lo', float('nan')):+.2f},{b.get('hi', float('nan')):+.2f}] n={nt},{nc}")
                rf = ref.get((s, wn, lab))
                if rf and b.get("est") is not None:
                    tol = max(0.15, 0.25 * abs(rf["did"]))
                    cmp_rows.append({"subset": s, "window": wn, "outcome": lab, "did": r3(b["est"], 2), "ref_did": rf["did"], "topic": r3(mt, 2),
                                     "ref_topic": rf["topic"], "comp": r3(mc, 2), "ref_comp": rf["comp"], "n": [nt, nc], "ref_n": [rf["n_t"], rf["n_c"]],
                                     "match": abs(b["est"] - rf["did"]) <= tol and (rf["lo"] > 0) == ((b.get("lo") or 0) > 0)})
        for gname in G2:
            lines.append(f"  event-sentence share of leads ({gname}): " + " → ".join(f"{(MEAN(D, gname, 'evs|' + k) or 0):.3f}" for k in DATES))
    txt = "\n".join(lines) + "\n"
    with open(os.path.join(C.out, "event_mass2_leads.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    fn = C.chart("12_narrative_residual", {"note": "lead critical hits per 10k words of all lead text: unfiltered = narrative residual + event sentences "
                                                   "(event_filter.py, sentence level); articles with all three leads >= 20 words",
                                           "results": {k: {kk: r3(vv, 3) if isinstance(vv, float) else vv for kk, vv in v.items()} for k, v in res.items()},
                                           "vs_reference": cmp_rows, "reference_file": os.path.relpath(C.ref, HERE) if C.ref else None,
                                           "lead_metric_source": dict(src)})
    n_match = sum(r["match"] for r in cmp_rows)
    pa, pr = res.get("all:post-war:narrative residual"), res.get("relevant:post-war:narrative residual")
    ua = res.get("all:post-war:unfiltered")
    share = (pa["est"] / ua["est"]) if pa and ua and pa.get("est") is not None and ua.get("est") else None
    what = (f"Event filter (sentences naming 2022+ years, recent events or recency wording are set aside) on {len(allok):,} mass2 leads with all "
            f"three snapshots. Post-war (Jul 2023 -> now) DiD in lead critical hits per 10k words: unfiltered {ci_txt(ua, 1, 2)}, narrative residual "
            f"{ci_txt(pa, 1, 2)}, event sentences {ci_txt(res.get('all:post-war:event sentences'), 1, 2)}; the residual is {pct(share, 0)} of the unfiltered DiD. "
            f"Relevant subset: residual {ci_txt(pr, 1, 2)}. Pre-war residual DiD {ci_txt(res.get('all:pre-war:narrative residual'), 1, 2)}. "
            f"Against study3/holdout_results/event_mass_leads.txt: {n_match} of {len(cmp_rows)} rows match (DiD within max(0.15, 25%) and same sign of the CI's lower bound)." +
            ("" if src.get("text", 0) else " WARNING: no lead text found; computed from narr features."))
    return card("narrative_residual", "The narrative residual: most of the post-war lead change is not news about recent events", what,
                {"type": "stacked bar (residual + event part) per group and window", "x": "window", "y": "change in lead critical hits per 10k words",
                 "series": "topic vs comparison; residual vs event sentences", "data": fn + ", event_mass2_leads.txt"},
                conf_rule(pa, pr, True, True),
                ("The lead change is a re-telling of older history and the land, not war coverage: filtering out sentences about recent "
                 "events leaves most of the topic-vs-comparison difference in place." if pos(pa) and share is not None and share >= 0.5 else
                 "Much of the post-war lead change sits in sentences about recent events: here the shift is partly news coverage, so the "
                 "'re-telling of history' reading needs the residual to be checked page by page." if pos(ua) else
                 "There is no clear post-war topic-vs-comparison lead change to decompose in this data."),
                "The filter is a fixed regex list (frozen in SPEC_STUDY3 amendment D) and misses some event sentences that name no year; "
                "matching the reference is approximate because mass2 deduplicates redirects and recrawled every lead.",
                numbers={"vs_reference": cmp_rows, "results": res})


# ================================================================== output
def write_md(out, cards, meta):
    L = [f"# Mass v2: twelve cards from the full crawl ({meta.get('n', 0):,} articles, now = {meta.get('now', '')[:10]})", "",
         "Generated by `wikitrends/analyze_mass2.py`. Every comparison is topic vs comparison (atrocity pages kept out of the comparison pool) "
         "and is repeated on the relevant subset (Wikidata type + baseline relevance, as in cohere.py). CIs are article-level bootstraps; "
         "'project CI' resamples whole WikiProjects. Chart files are relative to `wikitrends/patterns/mass2/`.", ""]
    for c in cards:
        L += [f"## {c['rank']}. {c['title']}  [{c['confidence']}]", "", f"**What we see:** {c['what_we_see']}", ""]
        ch = c.get("chart") or {}
        L += ["**Chart:** " + "; ".join(f"{k}: {v}" if k != "type" else str(v) for k, v in ch.items()), ""]
        L += [f"**So what:** {c['so_what']}", "", f"**Caveat:** {c['caveat']}", ""]
        if c.get("examples"):
            L += ["**Examples:**"] + [f"- *{e.get('article')}*: {e.get('note')}" if isinstance(e, dict) else f"- {e}" for e in c["examples"]] + [""]
        if c.get("error"):
            L += [f"**Not computed:** {c['error']}", ""]
    with open(os.path.join(out, "cards.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))


def jsonable(x):
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating, float)):
        return None if not math.isfinite(float(x)) else float(x)
    if isinstance(x, np.bool_):
        return bool(x)
    return x


def editor_hashes(arts, ED):
    hs = set()
    for a in arts:
        for e in lst(a.ev.get("lead_events")):
            if isinstance(e, dict) and isinstance(e.get("u"), str):
                hs.add(e["u"])
    for v in dct(ED.get("editors")).values():
        for w in dct(v).values():
            hs.update(x for x in lst(w) if isinstance(x, str))
    return hs


CARDS = [("who_edits", card_who), ("protection_ct", card_protection), ("rfc_rm", card_rfc), ("sd_wikidata", card_sd),
         ("lead_citations", card_cites), ("structure", card_structure), ("concept_diffusion", card_links), ("edit_sizes", card_sizes),
         ("lead_events", card_events), ("pageviews_exposure", card_views), ("atrocity_voice", None), ("narrative_residual", card_residual)]


def main(argv=None):
    global NB
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--data", default=A.DATA)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--boot", type=int, default=None, help="bootstrap replicates (default WT_BOOT or 1000)")
    ap.add_argument("--workers", type=int, default=min(4, os.cpu_count() or 1))
    ap.add_argument("--ref", default=REF_DEFAULT)
    a = ap.parse_args(argv)
    if a.boot is not None:
        NB = a.boot
    t0 = time.time()
    M, EV, ED, LD, SU, TY = load(a.data)
    arts = build(M, EV, LD, TY, a.workers)
    t1 = time.time()
    os.makedirs(os.path.join(a.out, "chart_data"), exist_ok=True)
    C = Ctx(arts, M, SU, ED, a.out, a.ref)
    cards = []
    for i, (cid, fn) in enumerate(CARDS, 1):
        ts = time.time()
        try:
            c = card_atrocity(C, LD) if cid == "atrocity_voice" else fn(C)
        except Exception as ex:
            warn(f"card {cid} failed: {ex}")
            traceback.print_exc(file=sys.stderr)
            c = card(cid, f"{cid}: not computed", "", {}, "ANECDOTE", "", "The card could not be computed from this data.",
                     extra={"error": f"{type(ex).__name__}: {ex}"})
        c["rank"] = i
        c["seconds"] = round(time.time() - ts, 1)
        cards.append(c)
    hs = editor_hashes(arts, ED)
    cnt = Counter(x.grp for x in arts)
    meta = {"n": len(arts), "now": C.now}
    out = {"angle": "mass2: the pilot's best signals at full scale (who edits, protection, RfCs, reuse surfaces, sources, structure, links, "
                    "edit sizes, exact lead events, exposure, atrocity voice, narrative residual)",
           "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "now": C.now, "data_dir": os.path.abspath(a.data),
           "n_articles": dict(cnt), "n_relevant": dict(Counter(x.grp for x in arts if x.rel)),
           "files": {"events": bool(EV), "leads": bool(LD.get("leads")), "editors": bool(ED.get("editors")), "summary": bool(SU)},
           "collection_summary": {k: SU.get(k) for k in ("n_expected", "n_records", "failed_signals", "coverage") if k in SU},
           "bootstrap": {"replicates": NB, "levels": ["article", "WikiProject cluster"]},
           "cards": [{k: v for k, v in c.items() if k != "seconds"} for c in cards],
           "new_questions": [
               {"question": "Do now-blocked flip accounts concentrate on the same pages across windows, and were they blocked for socking or AE?",
                "data_we_have": "per-event breason class and hashes within one run", "needed": "nothing new; a per-page cut of card 1"},
               {"question": "Does the hot-core link effect hold with the full link graph (outlinks of core articles) instead of concept links?",
                "data_we_have": "alias-resolved concept links at 3 dates", "needed": "pagelinks dumps at 2023-07 and now"},
               {"question": "Is the atrocity voice classifier right?", "data_we_have": "lead sentences in chart_data/11_atrocity_voice.json",
                "needed": "hand coding of the ~30 genocide sentences by two coders"}]}
    files = {"cards.json": json.dumps(jsonable(out), ensure_ascii=False, indent=1)}
    files.update({f"chart_data/{k}.json": json.dumps(jsonable(v), ensure_ascii=False, indent=1) for k, v in C.charts.items()})
    leak = [h for h in hs if any(h in s for s in files.values())]
    leak = [h for h in leak if HASH12.search(h)]
    if leak:
        sys.exit(f"analyze_mass2: refusing to write outputs: {len(leak)} editor hash(es) would be written")
    for k, v in files.items():
        with open(os.path.join(a.out, k), "w", encoding="utf-8") as f:
            f.write(v)
    write_md(a.out, out["cards"], meta)
    # summary
    print(f"analyze_mass2: {len(arts):,} articles ({dict(cnt)}), relevant {out['n_relevant']}; lead pass {t1 - t0:.0f}s, total {time.time() - t0:.0f}s")
    for c in cards:
        flag = "ERROR " if c.get("error") else ""
        print(f"  {c['rank']:2}. [{c['confidence']:10}] {flag}{c['id']:20} ({c['seconds']}s) {c['what_we_see'][:150]}")
    nr = next((c for c in cards if c["id"] == "narrative_residual"), {})
    vr = g(nr, "numbers", "vs_reference") or []
    if vr:
        print(f"  narrative residual vs reference: {sum(r['match'] for r in vr)}/{len(vr)} rows match")
    print(f"  wrote {a.out}/cards.json, cards.md, {len(C.charts)} chart files, event_mass2_leads.txt")
    return out


if __name__ == "__main__":
    main()
