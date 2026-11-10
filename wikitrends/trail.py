"""Editor-trail collector: who makes the critical-term lead edits of the scoped articles, and where else do they edit.
Runs inside ONE workflow job under one in-job salt (WT_SALT, coord.h); see analyze_trail.py for the analysis.

  python trail.py plan        -> data/trail/plan.json (offline: guard.py scope, topic + comparison pool)
  python trail.py collect     -> data/trail/raw.json.gz (network; time-budgeted)
  TRAIL_LIMIT=6 TRAIL_N=5 ... -> test mode (first 6 matched pairs, top 5 accounts per group)

Phases (each with its own share of TRAIL_BUDGET_MIN; a phase that ends early hands its time to the next):
  scope     guard.plan / guard.resolve / guard.match (same scope and 1:1 matching as guard.py); PageAssessments of the
            scoped articles
  history   prop=revisions since 2021-01-01 (rvdir=newer) + the last revision before 2021 (baseline), rvprop
            ids|timestamp|user|sha1|size|tags|comment; usernames hashed at once, comments reduced to flags (revert-like,
            undo / restore position, source-editor section edit). Until 14%.
  leads     section-0 wikitext (rvsection=0, 50 revids per call) of every revision since 2021 except source-editor
            section edits (lead unchanged by construction) and repeats of an earlier sha1 (same content): critical and
            connection counts only (analyze_trail.lead_counts_text). Articles in seeded random order. Until 50%.
  population top TRAIL_N registered non-bot accounts by number of lead edits that change the critical count, topic
            articles and comparison articles (an account in both lists stays in the topic group only)
  contribs  list=usercontribs 2021-01-01..now for each population account: namespace 0 in full (ids, title, timestamp,
            sizediff, flags, tags; the summary only as a section-edit / revert flag), talk namespaces as a count. The
            account name is used for this request only, in memory. Until 62%.
  assess    prop=pageassessments for every edited title (random order). Until 70%.
  discovery section-0 counts before / after each population edit of outside articles edited by >= 3 accounts of the same
            population (both populations, interleaved by number of accounts). Until 90%.
  extras    for the top topic-population discovery articles: lead at 2021-01-01 and now (first sentence, counts),
            short description, PageAssessments, mean monthly user pageviews over the last 12 months. Until 97%.
User-Agent: wt_net.UA (project name and repository URL; no e-mail address).
Privacy: usernames exist only in memory (one dict, for the usercontribs requests) and are dropped before anything is
written; raw outputs (hashed accounts, revids) stay on the runner and are deleted by the workflow. Nothing here prints a
name, a hash or a revision id.
"""
import argparse, gzip, json, os, random, re, sys, threading, time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wt_net                   # noqa: E402
import analyze as A             # noqa: E402
import coord as CO              # noqa: E402
import guard as G               # noqa: E402
import analyze_guard as AG      # noqa: E402
import analyze_trail as AT      # noqa: E402

OUT = os.path.join(HERE, "data", "trail")
EN = "https://en.wikipedia.org/w/api.php"
PV = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{t}/monthly/{a}/{b}"
SEED = 20261110
THREADS = int(os.environ.get("TRAIL_THREADS", "3"))
BUDGET_MIN = float(os.environ.get("TRAIL_BUDGET_MIN", "290"))
N_POP = int(os.environ.get("TRAIL_N", "40"))
MAX_CONTRIBS = int(os.environ.get("TRAIL_MAX_CONTRIBS", "120000"))
MAX_TALK = int(os.environ.get("TRAIL_MAX_TALK", "60000"))
MAX_DISC_EDITS = int(os.environ.get("TRAIL_MAX_DISC_EDITS", "300"))
N_EXTRAS = int(os.environ.get("TRAIL_EXTRAS", "60"))
PHASE_END = {"history": 0.14, "leads": 0.50, "contribs": 0.62, "assess": 0.70, "discovery": 0.90, "extras": 0.97}
SECT_RX = re.compile(r"^\s*/\*.*?\*/")
TALK_NS = "1|3|5|7|9|11|13|15|101|119|711|829"
_NAMES = {}                     # hash -> username, in memory only (cleared before writing)
_NLOCK = threading.Lock()


def q(params):
    p = {"format": "json", "formatversion": 2, **params}
    j = wt_net.get_json(EN, p)
    if j is None:
        raise RuntimeError("API request failed after retries")
    return j


def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# ------------------------------------------------------------------ plan (offline)
def plan():
    old = G.OUT
    G.OUT = OUT
    try:
        return G.plan()
    finally:
        G.OUT = old


# ------------------------------------------------------------------ scope assessments
def assessments(titles, deadline=None):
    """-> {title: [project names]} (empty list = no assessment); 50 titles per call, following continuation."""
    out = {}
    for i in range(0, len(titles), 50):
        if deadline and time.time() > deadline:
            break
        chunk = titles[i:i + 50]
        cont = {}
        got = {t: [] for t in chunk}
        norm = {}
        for _ in range(30):
            j = q({"action": "query", "prop": "pageassessments", "titles": "|".join(chunk), "palimit": "max", **cont})
            qy = j.get("query") or {}
            for n in qy.get("normalized") or []:
                norm[n["to"]] = n["from"]
            for p in qy.get("pages") or []:
                pa = p.get("pageassessments") or {}
                t = norm.get(p["title"], p["title"])
                got.setdefault(t, [])
                got[t] += list(pa.keys()) if isinstance(pa, dict) else [x.get("project") for x in pa if isinstance(x, dict)]
            if "continue" in j:
                cont = dict(j["continue"]); continue
            break
        for t in chunk:
            out[t] = sorted(set(got.get(t) or []))
    return out


# ------------------------------------------------------------------ histories (since 2021)
def _rev_tuple(r, shas, undo_ref, rest_ref, skip):
    u = r.get("user")
    hidden = bool(r.get("userhidden")) or not u
    fl = 0
    if hidden:
        fl |= AG.F_HIDDEN
    else:
        if A.ANON.match(u):
            fl |= AG.F_ANON
        if A.BOT.search(u):
            fl |= AG.F_BOT
    c = r.get("comment") or ""
    tags = set(r.get("tags") or [])
    if G.RV_RX.search(c):
        fl |= AG.F_RVSUM
    if tags & G.REVERT_TAGS:
        fl |= AG.F_RVTAG
    m1, m2 = G.UNDO_RX.search(c), G.RESTORE_RX.search(c)
    undo_ref.append(int(m1.group(1)) if m1 else None)
    rest_ref.append(int(m2.group(1)) if m2 else None)
    ve = any(t.startswith("visualeditor") for t in tags)
    skip.append(bool(SECT_RX.match(c)) and not ve and not r.get("commenthidden"))
    s = r.get("sha1") if not r.get("sha1hidden") else None
    sid = shas.setdefault(s, len(shas)) if s else -1
    hu = None
    if not hidden:
        hu = CO.h(u)
        if not (fl & (AG.F_ANON | AG.F_BOT)):
            with _NLOCK:
                _NAMES[hu] = u
    return [int(r["revid"]), AG.ep(r["timestamp"]), hu, fl, sid, r.get("size"), -1, -1, None, None]


RVPROP = "ids|timestamp|user|sha1|comment|size|tags"


def history(title, deadline):
    """-> (revs, skip flags, truncated). revs[0] is the baseline (last revision before 2021) when there is one."""
    revs, shas, undo_ref, rest_ref, skip = [], {}, [], [], []
    j = q({"action": "query", "prop": "revisions", "titles": title, "rvprop": RVPROP, "rvlimit": 1, "rvdir": "older",
           "rvstart": AT.FROM})
    for p in (j.get("query") or {}).get("pages") or []:
        for r in p.get("revisions") or []:
            t = _rev_tuple(r, shas, undo_ref, rest_ref, skip)
            t[3] |= AT.F_BASE
            skip[-1] = False
            revs.append(t)
    cont, truncated = {}, False
    while True:
        j = q({"action": "query", "prop": "revisions", "titles": title, "rvprop": RVPROP, "rvlimit": "max", "rvdir": "newer",
               "rvstart": AT.FROM, **cont})
        if j.get("error"):
            raise RuntimeError(f"history API error {j['error'].get('code')}")
        for p in (j.get("query") or {}).get("pages") or []:
            for r in p.get("revisions") or []:
                revs.append(_rev_tuple(r, shas, undo_ref, rest_ref, skip))
        if "continue" in j and time.time() < deadline:
            cont = dict(j["continue"]); continue
        truncated = "continue" in j
        break
    pos = {r[0]: k for k, r in enumerate(revs)}
    for k, (a, b) in enumerate(zip(undo_ref, rest_ref)):
        revs[k][6] = pos.get(a, -1) if a else -1
        revs[k][7] = pos.get(b, -1) if b else -1
    return revs, skip, truncated


# ------------------------------------------------------------------ lead counts
def lead_fetch(revids):
    """-> {revid: [crit, conn] or None (hidden / missing)}; 50 per call, rvsection=0."""
    out = {}
    def parse(j):
        for p in (j.get("query") or {}).get("pages") or []:
            for r in p.get("revisions") or []:
                c = ((r.get("slots") or {}).get("main") or {}).get("content")
                out[int(r["revid"])] = None if c is None else list(AT.lead_counts_text(c))
    for i in range(0, len(revids), 50):
        chunk = revids[i:i + 50]
        j = q({"action": "query", "prop": "revisions", "revids": "|".join(map(str, chunk)), "rvprop": "ids|content",
               "rvslots": "main", "rvsection": 0})
        if j.get("error"):
            for r in chunk:
                j1 = q({"action": "query", "prop": "revisions", "revids": str(r), "rvprop": "ids|content", "rvslots": "main",
                        "rvsection": 0})
                if not j1.get("error"):
                    parse(j1)
            continue
        parse(j)
    for r in revids:
        out.setdefault(int(r), None)
    return out


def lead_plan(revs, skip):
    """Revisions whose section 0 must be fetched (not a section edit, first occurrence of its sha1)."""
    seen, need = set(), []
    for r, sk in zip(revs, skip):
        if sk:
            if r[4] >= 0:
                seen.add(r[4])
            continue
        if r[4] >= 0 and r[4] in seen:
            continue
        need.append(r[0])
        if r[4] >= 0:
            seen.add(r[4])
    return need


def lead_fill(revs, skip, meas):
    """Fill crit / conn of every revision from the measured ones (section edits inherit, sha1 repeats copy)."""
    prev, shaval = None, {}
    for r, sk in zip(revs, skip):
        if r[0] in meas:
            v = meas[r[0]]
        elif sk:
            v = prev
        elif r[4] >= 0 and r[4] in shaval:
            v = shaval[r[4]]
        else:
            v = None
        if v is not None:
            r[8], r[9] = v[0], v[1]
            if r[4] >= 0:
                shaval[r[4]] = v
        prev = v
    return revs


def lead_article(a, deadline):
    need = lead_plan(a["revs"], a["_skip"])
    meas, done = {}, 0
    for i in range(0, len(need), 50):
        if time.time() > deadline:
            break
        meas.update(lead_fetch(need[i:i + 50])); done = i + 50
    lead_fill(a["revs"], a["_skip"], meas)
    return {"needed": len(need), "measured": min(done, len(need)), "complete": done >= len(need)}


# ------------------------------------------------------------------ contributions
def contribs(name, titles_ix, deadline):
    """-> {"ns0": rows, "talk": n, "truncated": bool}; row = [revid, parentid, title_id, ts, sizediff, flags]."""
    rows, cont, trunc = [], {}, False
    while True:
        j = q({"action": "query", "list": "usercontribs", "ucuser": name, "ucnamespace": 0, "ucdir": "newer",
               "ucstart": AT.FROM, "uclimit": "max", "ucprop": "ids|title|timestamp|comment|sizediff|flags|tags", **cont})
        if j.get("error"):
            raise RuntimeError(f"usercontribs API error {j['error'].get('code')}")
        for c in (j.get("query") or {}).get("usercontribs") or []:
            fl = 0
            cm = c.get("comment") or ""
            tags = set(c.get("tags") or [])
            if SECT_RX.match(cm) and not c.get("commenthidden"):
                fl |= AT.C_SECT
            if any(t.startswith("visualeditor") for t in tags):
                fl |= AT.C_VE
            if c.get("minor"):
                fl |= AT.C_MINOR
            if c.get("new"):
                fl |= AT.C_NEW
            if G.RV_RX.search(cm) or tags & G.REVERT_TAGS:
                fl |= AT.C_RV
            rows.append([int(c["revid"]), int(c.get("parentid") or 0), titles_ix(c["title"]), AG.ep(c["timestamp"]),
                         c.get("sizediff"), fl])
        if "continue" in j and len(rows) < MAX_CONTRIBS and time.time() < deadline:
            cont = dict(j["continue"]); continue
        trunc = "continue" in j
        break
    talk, cont = 0, {}
    while True:
        j = q({"action": "query", "list": "usercontribs", "ucuser": name, "ucnamespace": TALK_NS, "ucdir": "newer",
               "ucstart": AT.FROM, "uclimit": "max", "ucprop": "timestamp", **cont})
        talk += len((j.get("query") or {}).get("usercontribs") or [])
        if "continue" in j and talk < MAX_TALK and time.time() < deadline:
            cont = dict(j["continue"]); continue
        break
    return {"ns0": rows, "talk": talk, "truncated": trunc}


# ------------------------------------------------------------------ extras
def lead_at(title, start=None):
    p = {"action": "query", "prop": "revisions", "titles": title, "rvprop": "ids|timestamp|content", "rvslots": "main",
         "rvsection": 0, "rvlimit": 1}
    if start:
        p.update({"rvstart": start, "rvdir": "older"})
    j = q(p)
    for pg in (j.get("query") or {}).get("pages") or []:
        for r in pg.get("revisions") or []:
            return ((r.get("slots") or {}).get("main") or {}).get("content")
    return None


def views_month(title):
    end = time.strftime("%Y%m01", time.gmtime())
    y, m = int(end[:4]), int(end[4:6])
    start = f"{y - 1}{m:02d}01"
    t = quote(title.replace(" ", "_"), safe="")
    j = wt_net.get_json(PV.format(t=t, a=start + "00", b=end + "00"), {}, tries=4, ok404=True)
    if not j or "items" not in j:
        return None
    v = [i["views"] for i in j["items"]][-12:]
    return round(sum(v) / len(v)) if v else None


def wider_corpus():
    s = set()
    try:
        s |= set(json.load(open(os.path.join(A.DATA, "manifest.json"))))
    except Exception:
        pass
    for f in ("mass/frame.json", "mass3/frame.json", "random/frame.json"):
        try:
            for r in json.load(open(os.path.join(A.DATA, f)))["rows"]:
                s.add(r["title"])
        except Exception:
            pass
    return s


def extras(title, wider):
    old, new = lead_at(title, AT.FROM), lead_at(title)
    j = q({"action": "query", "prop": "description|pageassessments", "titles": title, "palimit": "max"})
    desc, proj = None, []
    for p in (j.get("query") or {}).get("pages") or []:
        desc = p.get("description")
        pa = p.get("pageassessments") or {}
        proj = sorted(pa.keys()) if isinstance(pa, dict) else []
    f21, fnow = AT.first_sentence(old), AT.first_sentence(new)
    c21 = AT.lead_counts_text(old) if old else (None, None)
    cn = AT.lead_counts_text(new) if new else (None, None)
    return {"first_2021": f21, "first_now": fnow,
            "first_2021_terms": AT.key_terms(f21) if f21 else None, "first_now_terms": AT.key_terms(fnow) if fnow else None,
            "lead_crit": [c21[0], cn[0]], "lead_conn": [c21[1], cn[1]], "created_after_2021": old is None,
            "description": desc, "projects": proj, "views_month": views_month(title), "in_wider_corpus": title in wider}


# ------------------------------------------------------------------ collect
def _pool(fn, items, deadline, label, threads=THREADS):
    """Thread pool until the deadline -> (results by index, errors, skipped). Errors print the exception TYPE only."""
    res, errs, skipped = {}, 0, 0
    lock = threading.Lock()
    def wrap(k, it):
        if time.time() > deadline:
            return k, "skip", None
        try:
            return k, "ok", fn(it)
        except Exception as e:
            print("ERR", label, type(e).__name__, file=sys.stderr, flush=True)
            return k, "err", None
    with ThreadPoolExecutor(threads) as ex:
        futs = [ex.submit(wrap, k, it) for k, it in enumerate(items)]
        for n, f in enumerate(as_completed(futs), 1):
            k, st, v = f.result()
            with lock:
                if st == "ok":
                    res[k] = v
                elif st == "err":
                    errs += 1
                else:
                    skipped += 1
            wt_net.heartbeat(f"trail-{label}", n, len(items), errors=errs, skipped=skipped)
    return res, errs, skipped


def collect():
    CO.salt()
    t0 = time.time()
    dl = lambda ph: t0 + PHASE_END[ph] * BUDGET_MIN * 60
    pl = json.load(open(os.path.join(OUT, "plan.json")))
    summ = {"budget_min": BUDGET_MIN, "window_end": now_iso(), "population_target": N_POP}
    # scope (guard.py's matching)
    topic, pool = pl["topic"], pl["pool"]
    info = G.resolve([x["title"] for x in topic + pool])
    pairs = G.match(topic, pool, info)
    lim = int(os.environ.get("TRAIL_LIMIT", "0"))
    if lim:
        pairs = pairs[:lim]
    arts = []
    for x, c in pairs:
        arts.append({"title": info[x["title"]]["title"], "group": "topic"})
        arts.append({"title": info[c["title"]]["title"], "group": "comparison"})
    seen = set(); arts = [a for a in arts if not (a["title"] in seen or seen.add(a["title"]))]
    scope = {g: sorted(a["title"] for a in arts if a["group"] == g) for g in ("topic", "comparison")}
    scope_pa = assessments(scope["topic"] + scope["comparison"])
    summ["scope"] = {g: len(v) for g, v in scope.items()}
    print(f"trail scope: {summ['scope']}", flush=True)
    # histories
    order = list(range(len(arts))); random.Random(SEED).shuffle(order)
    H, err, skip = _pool(lambda k: history(arts[k]["title"], dl("history")), order, dl("history"), "history")
    for k, (revs, sk, tr) in H.items():
        a = arts[order[k]]
        a["revs"], a["_skip"], a["truncated"] = revs, sk, tr
    arts = [a for a in arts if "revs" in a]
    summ["history"] = {"done": len(H), "errors": err, "skipped_budget": skip,
                       "truncated": sum(1 for a in arts if a.get("truncated")),
                       "revisions_thousands": {g: round(sum(len(a["revs"]) for a in arts if a["group"] == g) / 1e3, 1)
                                               for g in ("topic", "comparison")}}
    print(f"trail history: {summ['history']}", flush=True)
    # leads (random article order)
    order = list(range(len(arts))); random.Random(SEED + 1).shuffle(order)
    L, err, skip = _pool(lambda k: lead_article(arts[k], dl("leads")), order, dl("leads"), "leads")
    st = list(L.values())
    summ["leads"] = {"articles_done": len(L), "complete": sum(1 for s in st if s["complete"]), "errors": err,
                     "skipped_budget": skip, "revisions_needed": sum(s["needed"] for s in st),
                     "revisions_measured": sum(s["measured"] for s in st),
                     "share_of_revisions_with_counts": round(sum(1 for a in arts for r in a["revs"] if r[8] is not None) /
                                                             max(1, sum(len(a["revs"]) for a in arts)), 3)}
    print(f"trail leads: {summ['leads']}", flush=True)
    for a in arts:
        a.pop("_skip", None)
    # population
    E = AT.scoped_edits(arts)
    pop_t, _ = AT.rank_population(E["topic"], N_POP)
    pop_c, _ = AT.rank_population(E["comparison"], N_POP, exclude=set(pop_t))
    summ["population_overlap"] = sum(1 for u in AT.rank_population(E["comparison"], N_POP)[0] if u in set(pop_t))
    pop = {"topic": pop_t, "comparison": pop_c}
    print(f"trail population: topic {len(pop_t)}, comparison {len(pop_c)}", flush=True)
    # contributions (names used here only)
    titles, tix, tlock = [], {}, threading.Lock()
    def titles_ix(t):
        with tlock:
            if t not in tix:
                tix[t] = len(titles); titles.append(t)
            return tix[t]
    accts = pop_t + pop_c
    with _NLOCK:
        names = {u: _NAMES.get(u) for u in accts}
        _NAMES.clear()                                   # only the population's names survive, until the next phase
    C, err, skip = _pool(lambda u: contribs(names[u], titles_ix, dl("contribs")), accts, dl("contribs"), "contribs")
    names.clear()
    contrib = {accts[k]: v for k, v in C.items()}
    summ["contribs"] = {"accounts_done": len(C), "errors": err, "skipped_budget": skip,
                        "truncated": sum(1 for v in contrib.values() if v["truncated"]),
                        "mainspace_edits_thousands": round(sum(len(v["ns0"]) for v in contrib.values()) / 1e3, 1),
                        "distinct_titles": len(titles)}
    print(f"trail contribs: {summ['contribs']}", flush=True)
    # assessments of edited titles (random order)
    tl = [t for t in titles if t not in scope_pa]
    random.Random(SEED + 2).shuffle(tl)
    batches = [tl[i:i + 50] for i in range(0, len(tl), 50)]
    S, err, skip = _pool(lambda b: assessments(b), batches, dl("assess"), "assess")
    assess = dict(scope_pa)
    for v in S.values():
        assess.update(v)
    summ["assess"] = {"titles": len(titles), "assessed": sum(1 for t in titles if t in assess), "errors": err,
                      "skipped_budget": skip}
    print(f"trail assess: {summ['assess']}", flush=True)
    # discovery measurements (both populations, interleaved by number of accounts)
    excl = set(scope["topic"]) | set(scope["comparison"])
    rnd = random.Random(SEED + 3)
    units = []
    for g in ("topic", "comparison"):
        cands = AT.discovery_candidates(contrib, pop[g], excl, titles)
        for t, by in cands.items():
            rows = [r for rs in by.values() for r in rs if not (r[5] & AT.C_SECT and not r[5] & AT.C_VE)]
            if len(rows) > MAX_DISC_EDITS:
                rows = rnd.sample(rows, MAX_DISC_EDITS)
            units.append((len(by), rnd.random(), g, t, rows))
    units.sort(key=lambda x: (-x[0], x[1]))
    disc, tried, dlock = {}, set(), threading.Lock()
    def measure(unit):
        with dlock:
            need = sorted({x for r in unit[4] for x in (r[0], r[1]) if x} - tried)
            tried.update(need)
        n = 0
        for i in range(0, len(need), 50):
            if time.time() > dl("discovery"):
                with dlock:
                    tried.difference_update(need[i:])
                break
            got = lead_fetch(need[i:i + 50]); n += len(got)
            with dlock:
                for k, v in got.items():
                    if v is not None:
                        disc[str(k)] = v
        return n
    Dm, err, skip = _pool(measure, units, dl("discovery"), "discovery")
    summ["discovery"] = {"candidate_articles": dict(Counter(u[2] for u in units)), "articles_done": len(Dm),
                         "errors": err, "skipped_budget": skip, "revisions_measured": len(disc),
                         "capped_articles": sum(1 for u in units if len(u[4]) >= MAX_DISC_EDITS)}
    print(f"trail discovery: {summ['discovery']}", flush=True)
    # extras for the top topic discovery articles
    cands_t = AT.discovery_candidates(contrib, pop["topic"], excl, titles)
    ranked, _ = AT.rank_discovery(cands_t, disc)
    top = [r["title"] for r in ranked[:N_EXTRAS]]
    wider = wider_corpus()
    X, err, skip = _pool(lambda t: extras(t, wider), top, dl("extras"), "extras")
    ext = {top[k]: v for k, v in X.items()}
    summ["extras"] = {"articles": len(top), "done": len(X), "errors": err, "skipped_budget": skip}
    print(f"trail extras: {summ['extras']}", flush=True)
    summ["requests"] = wt_net.C["requests"]; summ["failures"] = wt_net.C["failures"]
    summ["elapsed_min"] = round((time.time() - t0) / 60, 1)
    with _NLOCK:
        _NAMES.clear()
    out = {"summary": summ, "scope": scope, "scope_assess": scope_pa, "articles": arts, "population": pop,
           "contribs": contrib, "titles": titles, "assess": assess, "disc": disc, "extras": ext}
    with gzip.open(os.path.join(OUT, "raw.json.gz"), "wt") as f:
        json.dump(out, f, separators=(",", ":"))
    print(f"trail collect done in {summ['elapsed_min']} min, {summ['requests']} requests", flush=True)
    if not arts or summ["history"]["errors"] > 0.05 * max(1, len(order)) or len(pop_t) < 3 or len(pop_c) < 3:
        sys.exit("trail collect: too many history errors (>5%), no articles or a population under 3 accounts")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["plan", "collect"])
    a = ap.parse_args()
    if a.cmd == "plan":
        plan()
    else:
        collect()


if __name__ == "__main__":
    main()
