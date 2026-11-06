"""Offline tests for mass3.py: a fake Wikipedia behind wt_net.get_json (no network).

  python test_mass3.py      (or: pytest test_mass3.py)  -> exits non-zero on any failed check
Covers: exact project-name resolution (no Indiana for India, task forces, required/optional), projectpages pagination,
redirect resolution and dedupe, multi-project assignment, population counts; allocation (floor 40, census below 40,
proportional, target met), inclusion probabilities summing to n, weighted totals recovering N, HT unbiasedness on a toy
population, seeded determinism; mass2 reuse (marked, never fetched, merged from mass2), checkpoint resume, fail-loud above
5% errors, merge fail-loud below 95%, and the design-weighted analysis on a toy set with a known answer.
"""
import gzip, json, os, random, shutil, sys, tempfile, threading
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ["WT_JOB"] = "mass3-test"
os.environ["WT_NOW"] = "2026-11-07"
os.environ.setdefault("WT_BOOT", "200")
import wt_net                       # noqa: E402
import mass3 as M3                  # noqa: E402
import random_baseline as RB        # noqa: E402

NOW = "2026-11-07T00:00:00Z"
TMP = tempfile.mkdtemp(prefix="wt-mass3-test-")
wt_net.STATUS_DIR = os.path.join(TMP, "status")
CALLS, FAIL = [], set()
_lock = threading.Lock()

# ------------------------------------------------------------------ fake PageAssessments
PROJECTS = ["Israel", "Palestine", "Judaism", "Jewish history", "Israel Palestine Collaboration",
            "Military history/Arab–Israeli conflict task force", "Kurdistan", "Ukraine", "Turkey", "Turkey/Turkish cuisine",
            "Serbia", "Serbia/Kosovo", "Armenia", "Azerbaijan", "Cyprus", "India", "Indiana", "Indianapolis",
            "India/Jammu and Kashmir", "Pakistan", "Ireland"]
# pages: title -> (pageid, ns); redirects: title -> target title
PAGES = {}
def _pid(t, ns=0):
    if t not in PAGES:
        PAGES[t] = (1000 + len(PAGES), ns)
    return PAGES[t][0]
REDIRECTS = {"Redir T1": "T1", "Redir Ku1": "Ku1", "Redir out": "Wikipedia:Something"}
DISAMBIG = {"D1"}
MISSING = {"Gone"}
ASSESS = {   # project -> [(title, class, importance, ns)]
    "Israel": [("A", "B", "Top", 0), ("B", "C", "Mid", 0), ("Redir T1", "Redirect", "Low", 0), ("Category:Israel", "Category", "NA", 14),
               ("D1", "Disambig", "NA", 0), ("Gone", "Stub", "Low", 0), ("I1", "Start", "Low", 0), ("I2", "Stub", "Low", 0),
               ("I3", "Stub", "Unknown", 0), ("Redir out", "Redirect", "Low", 0)],
    "Palestine": [("B", "C", "High", 0), ("P1", "Start", "Mid", 0), ("T1", "C", "High", 0)],
    "Judaism": [("J1", "B", "High", 0), ("A", "B", "Unknown", 0)],
    "Jewish history": [("H1", "Stub", "", 0)],
    "Israel Palestine Collaboration": [("X1", "C", "Mid", 0)],
    "Military history/Arab–Israeli conflict task force": [("X2", "C", "Mid", 0)],
    "Kurdistan": [("Redir Ku1", "Redirect", "Low", 0), ("Ku1", "B", "High", 0), ("Ku2", "Stub", "Bottom", 0)],
    "Ukraine": [("U1", "C", "Top", 0)], "Turkey": [("K1", "B", "Top", 0), ("P1", "Start", "Low", 0)],
    "Turkey/Turkish cuisine": [("Food", "Stub", "Low", 0)],
    "Serbia": [("S1", "C", "Mid", 0)], "Serbia/Kosovo": [("S1", "C", "Low", 0), ("KV1", "Stub", "Low", 0)],
    "Armenia": [("Am1", "C", "Mid", 0)], "Azerbaijan": [("Az1", "C", "Mid", 0)], "Cyprus": [("Cy1", "C", "", 0)],
    "India": [("Delhi", "B", "Top", 0)], "Indiana": [("Seal of Indiana", "C", "Mid", 0)], "Indianapolis": [("Indy", "C", "Mid", 0)],
    "India/Jammu and Kashmir": [("KS1", "C", "Mid", 0)], "Pakistan": [("Lahore", "B", "Top", 0)], "Ireland": [("Dublin", "B", "Top", 0)],
}
for proj, L in ASSESS.items():
    for t, _, _, ns in L:
        _pid(t, ns)
for t in set(REDIRECTS.values()):
    _pid(t, 4 if t.startswith("Wikipedia:") else 0)
TITLE = {v[0]: k for k, v in PAGES.items()}
PP_CHUNK = 3


def _page(t):
    pid, ns = PAGES[t]
    p = {"pageid": pid, "ns": ns, "title": t}
    if t in MISSING:
        return {"pageid": pid, "ns": ns, "title": t, "missing": True}
    if t in DISAMBIG:
        p["pageprops"] = {"disambiguation": ""}
    return p


def lead_text(t, date):
    base = (f"'''{t}''' is a place in a region of the world. It has a long history of farming, trade and local government, "
            "and its people speak several languages. The town hosts a weekly market and a school.")
    if t.endswith("gain") and date >= "2024-06-01":
        base += " Historians describe an episode of its past as a genocide."
    return base


def mock_get(url, params, tries=8, ok404=False):
    p = dict(params)
    with _lock:
        CALLS.append((url, p))
    if "rest_v1/metrics/pageviews" in url:
        t = url.split("/user/")[1].split("/monthly")[0].replace("_", " ")
        if t in FAIL:
            return None
        assert url.endswith("/2026100100"), url
        return {"items": [{"timestamp": f"{y}{m:02d}0100", "views": 10} for y in range(2021, 2027) for m in range(1, 13)
                          if f"{y}{m:02d}" <= "202610"]}
    if p.get("list") == "projects":
        assert p.get("pjsubprojects") == 1
        return {"query": {"projects": {n: n for n in PROJECTS}}}
    if p.get("list") == "projectpages":
        assert p["wppassessments"] == 1 and p["wpplimit"] == "max" and "|" not in p["wppprojects"]
        name = p["wppprojects"]
        L = ASSESS.get(name, [])
        off = int(p.get("wppcontinue", 0))
        chunk = L[off:off + PP_CHUNK]
        j = {"query": {"projects": {name: [{"pageid": PAGES[t][0], "ns": ns, "title": t,
                                             "assessment": {"class": c, "importance": imp}} for t, c, imp, ns in chunk]}}}
        if off + PP_CHUNK < len(L):
            j["continue"] = {"wppcontinue": str(off + PP_CHUNK), "continue": "-||"}
        return j
    if p.get("pageids"):
        assert p["redirects"] == 1 and "info" in p["prop"]
        ids = [int(x) for x in p["pageids"].split("|")]
        assert len(ids) <= 50
        pages, redir = [], []
        for i in ids:
            t = TITLE[i]
            if t in REDIRECTS:
                redir.append({"from": t, "to": REDIRECTS[t]}); pages.append(_page(REDIRECTS[t]))
            else:
                pages.append(_page(t))
        return {"query": {"pages": pages, "redirects": redir}}
    if p.get("prop") == "revisions":
        t = p["titles"]
        if t in FAIL:
            return None
        if p.get("rvdir") == "newer":
            return {"query": {"pages": [{"title": t, "revisions": [{"timestamp": "2009-01-01T00:00:00Z"}]}]}}
        return {"query": {"pages": [{"title": t, "revisions": [{"slots": {"main": {"content": lead_text(t, p["rvstart"])}}}]}]}}
    raise AssertionError(f"unexpected request {url} {p}")


wt_net.get_json = mock_get


def reset(sub):
    d = os.path.join(TMP, sub)
    shutil.rmtree(d, ignore_errors=True); os.makedirs(os.path.join(d, "mass3"))
    M3.DATA, M3.MDIR = d, os.path.join(d, "mass3")
    CALLS.clear(); FAIL.clear()
    return d


def snap(w, crit, res):
    cnt = {k: 0 for k in RB.CRIT}; cnt["genocide"] = crit
    rc = {k: 0 for k in RB.CRIT}; rc["genocide"] = res
    return {"date": "x", "words": w, "crit": crit * 1e4 / w, "counts": cnt, "lead_prose": "p",
            "ev": {"sentence": {"event_share": 0.0, "event_sentences": 0, "res_words": w, "res_counts": rc, "ev_words": 0, "ev_counts": None}}}


def write_mass2(d, recs):
    """recs: [(title, pageid, gained?)] -> mass2.json.gz with narr snaps and compact pageviews."""
    arts = []
    for t, pid, g in recs:
        arts.append({"title": t, "group": "topic", "project": "Israel", "importance": "Mid", "stratum": "topic",
                     "frame_titles": [t, t + " (old title)"], "now": {"pageid": pid}, "created_in_window": False,
                     "pageviews": {"monthly": {"start": "202101", "views": [5] * 70}},
                     "at": {"2021-01-01": {"narr": snap(100, 0, 0)}, "2023-07-01": {"narr": {"same_as": "2021-01-01"}},
                            "now": {"narr": snap(100, 1 if g else 0, 1 if g else 0)}}})
    arts.append({"title": "Atro", "group": "comparison", "stratum": "atrocity", "now": {"pageid": 1}, "at": {}})
    json.dump({"now": "2026-11-05T00:00:00Z", "articles": arts}, gzip.open(os.path.join(d, "mass2.json.gz"), "wt"))


# ------------------------------------------------------------------ tests: population
def test_resolve_projects_exact():
    projects, skipped = M3.resolve_projects(PROJECTS)
    names = [p["name"] for p in projects]
    assert names[:4] == ["Israel", "Palestine", "Judaism", "Jewish history"], names
    assert "Israel Palestine Collaboration" in names and "Military history/Arab–Israeli conflict task force" in names
    assert "Serbia/Kosovo" in names and "India/Jammu and Kashmir" in names and "Cyprus" in names
    for bad in ("India", "Indiana", "Indianapolis", "Pakistan", "Ireland", "Turkey/Turkish cuisine"):
        assert bad not in names, bad
    assert {s["family"] for s in skipped} == {"Zionism", "Russo-Ukrainian war", "Northern Ireland", "The Troubles"}, skipped
    assert all(p["side"] == "topic" for p in projects[:6]) and all(p["side"] == "comparison" for p in projects[6:])
    try:
        M3.resolve_projects([n for n in PROJECTS if n != "Palestine"])
    except SystemExit as e:
        assert "Palestine" in str(e)
    else:
        raise AssertionError("a missing required project must exit")


def test_pagination():
    CALLS.clear()
    rows, n = M3.project_pages("Israel")
    assert n == 4 and len(rows) == len(ASSESS["Israel"]), (n, len(rows))       # 10 pages in chunks of 3
    assert [r["title"] for r in rows] == [t for t, *_ in ASSESS["Israel"]]
    conts = [q.get("wppcontinue") for _, q in CALLS if q.get("list") == "projectpages"]
    assert conts == [None, "3", "6", "9"], conts


def test_population_redirects_dupes_assignment():
    reset("pop")
    pop = M3.population()
    A = {r["title"]: r for r in pop["articles"]}
    # redirects resolved and merged, dropped pages counted
    assert "Redir T1" not in A and "T1" in A and A["T1"]["redirects_merged"] == ["Redir T1"]
    assert A["T1"]["project"] == "Israel" and A["T1"]["importance"] == "Low"            # first topic project, via redirect
    assert A["T1"]["assess"]["Palestine"] == {"class": "C", "importance": "High", "via_redirect": False}
    assert A["Ku1"]["assess"]["Kurdistan"]["importance"] == "High", "direct assessment beats the redirect's"
    assert pop["dropped"] == {"namespace": 1, "disambiguation": 1, "missing": 1, "redirect_out_of_namespace": 1}, pop["dropped"]
    for t in ("D1", "Gone", "Category:Israel", "Seal of Indiana", "Indy", "Delhi", "Lahore", "Dublin", "Food"):
        assert t not in A, t
    assert len({r["pageid"] for r in pop["articles"]}) == len(pop["articles"])
    # multi-project assignment
    assert A["A"]["project"] == "Israel" and A["A"]["importance"] == "Top" and A["A"]["assess"]["Judaism"]["importance"] == "Unknown"
    assert A["B"]["project"] == "Israel" and A["B"]["importance"] == "Mid"
    assert A["P1"]["side"] == "topic" and A["P1"]["project"] == "Palestine" and A["P1"]["also_comparison"]
    assert A["S1"]["project"] == "Serbia" and A["KV1"]["project"] == "Serbia/Kosovo"
    assert A["H1"]["importance"] == "Unrated" and A["Ku2"]["importance"] == "Low" and A["Cy1"]["importance"] == "Unrated"
    assert A["KS1"]["side"] == "comparison" and A["X2"]["project"].startswith("Military history/")
    # counts
    st = pop["strata"]
    assert sum(st.values()) == len(pop["articles"]) == sum(pop["side_totals"].values())
    assert st["topic|Israel|Low"] == 3 and st["topic|Palestine|Mid"] == 1          # I1, I2, T1 ; P1
    assert pop["counts_by_project_importance"]["topic"]["Palestine"] == {"High": 2, "Mid": 1}
    assert pop["counts_by_project_importance"]["comparison"]["Turkey"] == {"Top": 1, "Low": 1}
    assert pop["side_totals"] == {"topic": 11, "comparison": 10}, pop["side_totals"]
    assert os.path.exists(os.path.join(M3.MDIR, "population.json"))


def test_unresolved_fails_loud():
    reset("unres")
    saved = mock_get.__globals__["TITLE"].copy()
    try:
        def broken(url, params, **kw):
            if params.get("pageids"):
                return {"query": {"pages": [], "redirects": []}}
            return mock_get(url, params, **kw)
        wt_net.get_json = broken
        try:
            M3.population()
        except SystemExit as e:
            assert "could not be resolved" in str(e), e
        else:
            raise AssertionError("unresolvable page ids must exit")
    finally:
        wt_net.get_json = mock_get; TITLE.update(saved)


# ------------------------------------------------------------------ tests: stratification math
def test_allocate():
    N = {"t|a|Top": 1000, "t|a|Mid": 9000, "t|b|Top": 30, "t|b|Mid": 45, "t|c|Low": 20000, "t|d|NA": 3}
    n = M3.allocate(N, 1500)
    assert sum(n.values()) == 1500, n
    assert n["t|b|Top"] == 30 and n["t|d|NA"] == 3, "census below 40"
    assert n["t|b|Mid"] == 40, "floor 40"
    assert all(n[h] <= N[h] for h in N)
    free = ["t|a|Top", "t|a|Mid", "t|c|Low"]
    r = [n[h] / N[h] for h in free]
    assert max(r) - min(r) < 2 / 1000, r                                   # proportional among the rest
    big = M3.allocate({"x": 100, "y": 100, "z": 100}, 60)                  # floors exceed the target: floors win
    assert big == {"x": 40, "y": 40, "z": 40}
    allin = M3.allocate({"x": 50, "y": 60}, 500)                           # target above N: census everywhere
    assert allin == {"x": 50, "y": 60}


def toy_population(d):
    rng = random.Random(1)
    arts, pid = [], 1
    spec = {("topic", "Israel", "Top"): 120, ("topic", "Israel", "Mid"): 3000, ("topic", "Israel", "Low"): 9000,
            ("topic", "Palestine", "Mid"): 800, ("topic", "Judaism", "Unknown"): 25,
            ("comparison", "Turkey", "Top"): 90, ("comparison", "Turkey", "Low"): 15000, ("comparison", "Cyprus", "Unrated"): 12}
    for (s, p, imp), k in spec.items():
        for _ in range(k):
            arts.append({"pageid": pid, "title": f"P{pid}", "side": s, "project": p, "importance": imp, "class": "Stub",
                         "assess": {p: {}}, "redirects_merged": [], "also_comparison": False, "y": rng.random() < 0.1})
            pid += 1
    pop = {"generated": "g", "now": NOW, "articles": arts}
    json.dump(pop, open(os.path.join(d, "mass3", "population.json"), "w"))
    return pop, spec


def test_sample_pi_and_weights():
    d = reset("sample")
    pop, spec = toy_population(d)
    write_mass2(d, [("P12921", 5, True), ("Renamed", 12922, False), ("Old P200", 999999, False)])  # title / pageid / none
    old = dict(M3.TARGET); M3.TARGET.update({"topic": 600, "comparison": 300})
    try:
        fr = M3.sample()
        fr2 = M3.sample(path=os.path.join(d, "mass3", "frame2.json"))
    finally:
        M3.TARGET.clear(); M3.TARGET.update(old)
    assert [r["title"] for r in fr["rows"]] == [r["title"] for r in fr2["rows"]], "seeded: identical draw"
    by = Counter(r["stratum"] for r in fr["rows"])
    al = {a["stratum"]: a for a in fr["allocation"]}
    for side, tgt in (("topic", 600), ("comparison", 300)):
        rows = [r for r in fr["rows"] if r["group"] == side]
        assert len(rows) == tgt, (side, len(rows))
        Nside = sum(k for (s, *_), k in spec.items() if s == side)
        # sum of pi over all population units = n ; sum of 1/pi over the sample = N
        pi_of = {h: al[h]["pi"] for h in al}
        assert abs(sum(pi_of[M3.stratum(a)] for a in pop["articles"] if a["side"] == side) - tgt) < 1e-6
        assert abs(sum(r["w"] for r in rows) - Nside) < 1e-6
    for (s, p, imp), k in spec.items():
        h = f"{s}|{p}|{imp}"
        assert al[h]["N"] == k and by[h] == al[h]["n"] and abs(sum(r["w"] for r in fr["rows"] if r["stratum"] == h) - k) < 1e-6
        assert al[h]["n"] >= min(40, k)
    assert al["topic|Judaism|Unknown"]["rule"] == "census" and al["topic|Judaism|Unknown"]["pi"] == 1
    assert al["comparison|Turkey|Top"]["n"] == 40 and al["comparison|Turkey|Top"]["rule"] == "floor"
    assert len({r["pageid"] for r in fr["rows"]}) == len(fr["rows"])
    # mass2 reuse: matched by pageid or title, only if drawn; the rest are fetched
    re_ = {r["title"]: r["mass2_title"] for r in fr["rows"] if r["reused"]}
    assert re_ == {"P12921": "P12921", "P12922": "Renamed"}, re_          # census stratum: both certainly drawn
    assert fr["side_totals"]["topic"]["reused"] == 2


def test_ht_unbiased():
    """Over many seeded draws, the HT total of y and the weighted share recover the population values."""
    N = {"a": 200, "b": 5000, "c": 30}
    rng0 = random.Random(3)
    pop = {h: [1.0 if rng0.random() < q else 0.0 for _ in range(k)] for (h, k), q in zip(N.items(), (0.5, 0.05, 0.9))}
    true = sum(map(sum, pop.values()))
    n = M3.allocate(N, 300)
    tots, Ws = [], []
    for s in range(400):
        rng = random.Random(s)
        t = W = 0.0
        for h in N:
            for y in rng.sample(pop[h], n[h]):
                t += y * N[h] / n[h]; W += N[h] / n[h]
        tots.append(t); Ws.append(W)
    assert all(abs(w - sum(N.values())) < 1e-6 for w in Ws), "weights sum to N in every draw"
    assert abs(sum(tots) / len(tots) - true) / true < 0.03, (sum(tots) / len(tots), true)


# ------------------------------------------------------------------ tests: shard / reuse / resume / fail-loud / merge
def make_frame(d, fetch_titles, reused):
    rows = []
    for i, t in enumerate(fetch_titles):
        rows.append({"title": t, "pageid": 5000 + i, "group": "topic" if i % 2 == 0 else "comparison",
                     "project": "Israel" if i % 2 == 0 else "Turkey", "importance": "Low", "class": "Stub",
                     "stratum": "topic|Israel|Low" if i % 2 == 0 else "comparison|Turkey|Low", "pi": 0.5, "w": 2.0,
                     "projects": [], "also_comparison": False, "reused": False, "mass2_title": None})
    for t, pid, _ in reused:
        rows.append({"title": t + " now", "pageid": pid, "group": "topic", "project": "Israel", "importance": "Low", "class": "Stub",
                     "stratum": "topic|Israel|Low", "pi": 0.5, "w": 2.0, "projects": [], "also_comparison": False,
                     "reused": True, "mass2_title": t})
    nt = sum(1 for r in rows if r["group"] == "topic"); nc = len(rows) - nt
    fr = {"now": NOW, "seed": M3.SEED, "targets": {}, "mass2_now": "2026-11-05T00:00:00Z", "rows": rows,
          "side_totals": {}, "allocation": [{"stratum": "topic|Israel|Low", "side": "topic", "N": 2 * nt, "n": nt, "pi": 0.5, "reused": len(reused)},
                                            {"stratum": "comparison|Turkey|Low", "side": "comparison", "N": 2 * nc, "n": nc, "pi": 0.5, "reused": 0}]}
    json.dump(fr, open(os.path.join(d, "mass3", "frame.json"), "w"))
    return fr


def test_reuse_resume_merge():
    d = reset("resume")
    reused = [("M2 a", 77, True), ("M2 b", 78, False)]
    write_mass2(d, reused)
    fetch = [f"F{i}" + (" gain" if i < 2 else "") for i in range(8)]
    make_frame(d, fetch, reused)
    M3.run_shard(0, 1)
    p = os.path.join(M3.MDIR, "m3_0.json.gz")
    done = json.load(gzip.open(p, "rt"))
    assert sorted(r["title"] for r in done) == sorted(fetch), "only non-reused rows are fetched"
    touched = {q.get("titles") for _, q in CALLS if q.get("prop") == "revisions"}
    assert not any(t.startswith("M2") for t in touched), touched
    json.dump(done[:5], gzip.open(p, "wt"))                     # simulate an interrupted shard
    CALLS.clear()
    M3.run_shard(0, 1)
    done2 = json.load(gzip.open(p, "rt"))
    assert sorted(r["title"] for r in done2) == sorted(fetch)
    assert {q.get("titles") for _, q in CALLS if q.get("prop") == "revisions"} == {r["title"] for r in done[5:]}
    res = M3.merge()
    A = {a["title"]: a for a in res["articles"]}
    assert len(A) == 10 and A["M2 a now"]["source"] == "mass2" and A["F0 gain"]["source"] == "mass3"
    assert A["M2 a now"]["views_12m"] == 60 and A["F3"]["views_12m"] == 120
    assert A["M2 a now"]["snaps"][1]["words"] == 100, "mass2 same_as resolved"
    o = M3.outcomes(A["M2 a now"]); assert o["gain"] == 1.0 and o["okL"] and abs(o["post_unf"] - 100.0) < 1e-9
    o = M3.outcomes(A["F0 gain"]); assert o["gain"] == 1.0 and o["post_res"] > 0
    assert M3.outcomes(A["F3"])["gain"] == 0.0
    assert all(a["w"] == 2.0 for a in A.values())
    lead = json.load(gzip.open(os.path.join(d, "mass3_leads.json.gz"), "rt"))
    assert set(lead["leads"]) == set(fetch)
    os.remove(p)                                                 # nothing fetched -> merge must fail loudly (files still written)
    try:
        M3.merge()
    except SystemExit as e:
        assert "<95%" in str(e), e
    else:
        raise AssertionError("merge with no fetched rows must exit non-zero")
    assert os.path.exists(os.path.join(d, "mass3.json"))


def test_fail_loud():
    d = reset("failloud")
    make_frame(d, [f"F{i}" for i in range(10)], [])
    FAIL.update({"F1", "F6"})                                    # 20% > 5%
    try:
        M3.run_shard(0, 1)
    except SystemExit as e:
        assert "failed (>5%)" in str(e), e
    else:
        raise AssertionError("shard with 20% errors must exit non-zero")
    assert len(json.load(gzip.open(os.path.join(M3.MDIR, "m3_0.json.gz"), "rt"))) == 8


def test_estimate():
    d = reset("est")
    fr = make_frame(d, [f"F{i}" for i in range(1000)], [("M", 1, False)])
    e = M3.estimate(fr, of=4)
    assert e["to_fetch"] == 1000 and e["reused"] == 1 and len(e["requests_per_shard"]) == 4
    assert abs(e["requests_total"] - 1000 * M3.REQ_PER_ARTICLE * M3.CALIBRATION) < 5
    big = make_frame(d, [f"F{i}" for i in range(20000)], [])
    try:
        M3.estimate(big, of=4, check=True)
    except SystemExit as e:
        assert "budget" in str(e)
    else:
        raise AssertionError("over-budget shards must exit with --check")


# ------------------------------------------------------------------ tests: analysis
def test_analyze_known_answer():
    d = reset("analyze")
    arts = []
    def add(title, side, proj, imp, stratum, gain, views):
        arts.append({"title": title, "group": side, "project": proj, "importance": imp, "stratum": stratum, "pi": 0, "w": 0,
                     "source": "mass3", "existed_2021": True, "views_12m": views,
                     "snaps": [snap(100, 0, 0), snap(100, 0, 0), snap(100, 1 if gain else 0, 1 if gain else 0)]})
    for i in range(10):
        add(f"TA{i}", "topic", "Palestine", "High", "topic|Palestine|High", True, 1000)   # N 1000, all gain (+100/10k)
        add(f"TB{i}", "topic", "Israel", "Low", "topic|Israel|Low", False, 10)            # N 9000, none gain
        add(f"TJ{i}", "topic", "Judaism", "Low", "topic|Judaism|Low", False, 10)          # N 2000
        add(f"C{i}", "comparison", "Turkey", "Low", "comparison|Turkey|Low", i == 0, 10)  # N 500, 10% gain
    add("TB-lost", "topic", "Israel", "Low", "topic|Israel|Low", False, 10)
    arts.pop()                                                    # (allocation says 11 drawn, 10 arrived -> weight 900)
    alloc = [{"stratum": "topic|Palestine|High", "side": "topic", "N": 1000, "n": 10, "pi": 0.01, "reused": 0},
             {"stratum": "topic|Israel|Low", "side": "topic", "N": 9000, "n": 11, "pi": 11 / 9000, "reused": 0},
             {"stratum": "topic|Judaism|Low", "side": "topic", "N": 2000, "n": 10, "pi": 0.005, "reused": 0},
             {"stratum": "comparison|Turkey|Low", "side": "comparison", "N": 500, "n": 10, "pi": 0.02, "reused": 0}]
    json.dump({"now": NOW, "seed": 1, "allocation": alloc, "articles": arts, "missing": {"not_fetched": 1}},
              open(os.path.join(d, "mass3.json"), "w"))
    rb = {"articles": {f"R{i}": {"existed_2021": True, "views_12m": 5, "snaps": [snap(100, 0, 0)] * 3} for i in range(30)}}
    json.dump(rb, open(os.path.join(d, "random_baseline.json"), "w"))
    md, cd = os.path.join(d, "out.md"), os.path.join(d, "chart")
    out = M3.analyze(d, md, cd)
    w = out["overall"]["weighted"]; u = out["overall"]["unweighted"]
    assert abs(w["N_t"] - 12000) < 1e-6 and abs(w["N_c"] - 500) < 1e-6, "weights recover N (non-response adjusted)"
    assert abs(w["b_t"] - 1000 / 12000) < 1e-9 and abs(u["b_t"] - 1 / 3) < 1e-9
    assert abs(w["a_unf_t"] - 100 * 1000 / 12000) < 1e-6 and abs(w["a_unf_c"] - 10.0) < 1e-6
    assert abs(w["gainers_t_total"] - 1000) < 1e-6
    assert abs(w["d_t"] - (1000 * 1000) / (1000 * 1000 + 11000 * 10)) < 1e-9
    assert abs(w["e"] - 1000 / 10000) < 1e-9 and abs(w["e_ju"]) < 1e-12
    ci = out["overall"]["ci"]["b_t"]; assert ci[0] <= w["b_t"] <= ci[1]
    assert out["overall"]["ci"]["b_c"][1] > out["overall"]["ci"]["b_c"][0], "non-census strata vary"
    assert abs(out["by_importance"]["High"]["weighted"]["b_t"] - 1.0) < 1e-12
    assert abs(out["random"]["diff"]["t_a"] - w["a_unf_t"]) < 1e-6
    txt = open(md).read()
    for h in ("## Population and sample", "## Headline results", "## By importance", "## Against the random-Wikipedia baseline"):
        assert h in txt, h
    assert os.path.exists(os.path.join(cd, "07_mass3_population.json")) and os.path.exists(os.path.join(cd, "08_mass3_estimates.json"))


TESTS = [test_resolve_projects_exact, test_pagination, test_population_redirects_dupes_assignment, test_unresolved_fails_loud,
         test_allocate, test_sample_pi_and_weights, test_ht_unbiased, test_reuse_resume_merge, test_fail_loud, test_estimate,
         test_analyze_known_answer]

if __name__ == "__main__":
    bad = 0
    for t in TESTS:
        try:
            t(); print("ok  ", t.__name__, flush=True)
        except BaseException as e:            # SystemExit too: a test must never exit the runner
            bad += 1; import traceback; traceback.print_exc(); print("FAIL", t.__name__, e, flush=True)
    shutil.rmtree(TMP, ignore_errors=True)
    print(f"{len(TESTS) - bad}/{len(TESTS)} passed")
    sys.exit(1 if bad else 0)
