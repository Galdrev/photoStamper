"""Offline tests for random_baseline.py: a fake Wikipedia behind wt_net.get_json (no network).

  python test_random_baseline.py      (or: pytest test_random_baseline.py)  -> exits non-zero on any failed check
Covers: sampling (dedupe across rounds, redirects and disambiguation pages excluded, draw records), groups_for("random"),
missing 2021 lead (created later vs redirect in 2021 vs deleted), strict lead fetch (network failure is an error, not
"no lead"), pageviews last 12 months, checkpoint resume, fail-loud above 5% errors, merge math on a toy set, analyze.
"""
import gzip, json, os, shutil, sys, tempfile, threading

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ["WT_JOB"] = "random-test"
os.environ["WT_NOW"] = "2026-11-06"
import wt_net                       # noqa: E402
import mass_narr as MN              # noqa: E402
import random_baseline as R         # noqa: E402

NOW = "2026-11-06T00:00:00Z"
TMP = tempfile.mkdtemp(prefix="wt-random-test-")
wt_net.STATUS_DIR = os.path.join(TMP, "status")

# ------------------------------------------------------------------ fake wiki
PLAIN = [f"Plain {i}" for i in range(16)]
DISAMBIG = {"Mercury (disambiguation)", "Springfield"}
SNEAKY_REDIRECT = {"Sneaky redirect"}            # list=random filter missed it; info still flags it
CREATED_LATER = {"New page"}                     # first revision 2022
WAS_REDIRECT_2021 = {"Was redirect"}             # history before 2021, but a redirect then
GONE = {"Gone page"}                             # deleted between draw and shard
POOL = PLAIN + sorted(DISAMBIG) + sorted(SNEAKY_REDIRECT) + sorted(CREATED_LATER) + sorted(WAS_REDIRECT_2021) + sorted(GONE)
PID = {t: 1000 + i for i, t in enumerate(POOL)}
TITLE = {v: k for k, v in PID.items()}
FAIL = set()
CALLS = []
_lock = threading.Lock()

BASE = ("{{Short description|Something}}\n'''%s''' is a small place in a region of the world. It has a long history of "
        "farming, trade and local government, and its people speak several languages. The town hosts a weekly market and a school.")
PRE_ADD = " Historians describe an episode of its past as a genocide."           # residual sentence
POST_EVENT = " In 2024, a report accused the government of apartheid."            # event sentence (names a 2022+ year)


def lead_text(t, date):
    if t in GONE:
        return None
    if t in CREATED_LATER and date < "2022-03-01":
        return None
    if t in WAS_REDIRECT_2021 and date < "2021-06-01":
        return "#REDIRECT [[Plain 0]]"
    txt = BASE % t
    k = int(t.split()[-1]) if t.startswith("Plain ") else 99
    if k in (0, 1) and date >= "2023-01-01":
        txt += PRE_ADD                    # gained pre-war (2021 -> 2023-07), in the residual
    if k in (2, 3, 4) and date >= "2024-06-01":
        txt += POST_EVENT                 # gained post-war, event sentence
    if k == 5 and date >= "2024-06-01":
        txt += PRE_ADD                    # gained post-war, residual
    return txt


def created(t):
    return "2022-03-01T10:00:00Z" if t in CREATED_LATER else "2009-05-05T00:00:00Z"


ROUNDS = [POOL[:12], POOL[8:]]       # overlap -> duplicates across rounds


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
    if p.get("list") == "random":
        assert p["rnnamespace"] == 0 and p["rnfilterredir"] == "nonredirects" and p["rnlimit"] == 500
        k = sum(1 for _, q in CALLS if q.get("list") == "random") - 1
        batch = ROUNDS[k % len(ROUNDS)]
        return {"query": {"random": [{"id": PID[t], "ns": 0, "title": t} for t in batch]}}
    if "pageprops" in p.get("prop", ""):
        assert p["ppprop"] == "disambiguation"
        ids = [int(x) for x in p["pageids"].split("|")]
        assert len(ids) <= 50
        pages = []
        for i in ids:
            t = TITLE[i]
            pg = {"pageid": i, "ns": 0, "title": t}
            if t in DISAMBIG:
                pg["pageprops"] = {"disambiguation": ""}
            if t in SNEAKY_REDIRECT:
                pg["redirect"] = True
            pages.append(pg)
        return {"query": {"pages": pages}}
    if p.get("prop") == "revisions":
        t = p["titles"]
        if t in FAIL:
            return None
        if t in GONE:
            return {"query": {"pages": [{"title": t, "missing": True}]}}
        if p.get("rvdir") == "newer":
            return {"query": {"pages": [{"title": t, "revisions": [{"timestamp": created(t)}]}]}}
        wt = lead_text(t, p["rvstart"])
        if wt is None:
            return {"query": {"pages": [{"title": t}]}}
        return {"query": {"pages": [{"title": t, "revisions": [{"slots": {"main": {"content": wt}}}]}]}}
    raise AssertionError(f"unexpected request {url} {p}")


wt_net.get_json = mock_get


def reset(sub):
    d = os.path.join(TMP, sub)
    shutil.rmtree(d, ignore_errors=True); os.makedirs(os.path.join(d, "random"))
    R.DATA, R.RDIR = d, os.path.join(d, "random")
    CALLS.clear(); FAIL.clear()
    return d


def make_frame(titles):
    rows = [{"title": t, "pageid": PID[t], "group": "random", "project": None, "importance": None, "draw_round": 1,
             "draw_pos": i, "drawn_at": "2026-11-06T01:00:00Z"} for i, t in enumerate(titles)]
    json.dump({"now": NOW, "rows": rows, "generated": "2026-11-06T01:00:00Z", "rounds": 1}, open(os.path.join(R.RDIR, "frame.json"), "w"))
    return rows


# ------------------------------------------------------------------ tests
def test_sample_dedupe_redirect_disambig():
    reset("sample")
    target = len(POOL) - len(DISAMBIG) - len(SNEAKY_REDIRECT)
    fr = R.sample(target=target)
    titles = [r["title"] for r in fr["rows"]]
    assert len(titles) == len(set(titles)) == target, titles
    assert not (set(titles) & DISAMBIG), "disambiguation page kept"
    assert not (set(titles) & SNEAKY_REDIRECT), "redirect kept"
    assert fr["excluded_counts"]["duplicate"] == 4 and fr["excluded_counts"]["disambiguation"] == 2
    assert fr["excluded_counts"]["redirect"] == 1 and fr["rounds"] == 2
    assert all(r["drawn_at"] and r["draw_round"] in (1, 2) and r["pageid"] for r in fr["rows"])
    assert fr["seed"] == R.SEED and "not seedable" in fr["seed_note"]
    assert os.path.exists(os.path.join(R.RDIR, "frame.json"))


def test_sample_truncates_deterministically():
    reset("sample2")
    fr = R.sample(target=5)
    assert [r["title"] for r in fr["rows"]] == PLAIN[:5]


def test_groups_for_random():
    g, ms = MN.groups_for({"group": "random", "project": None})
    assert g == {} and ms == {}


def test_collect_cases():
    reset("collect")
    R.set_now(NOW)
    by = {t: R.collect({"title": t, "group": "random", "project": None, "importance": None}, NOW)
          for t in ["Plain 0", "Plain 2", "New page", "Was redirect", "Gone page"]}
    p0 = by["Plain 0"]
    assert p0["existed_2021"] and not p0["created_later"] and p0["created"] is None
    assert all(s is not None for s in p0["snaps"]) and [s["date"] for s in p0["snaps"]] == ["2021-01-01", "2023-07-01", "2026-11-06"]
    assert p0["snaps"][0]["counts"]["genocide"] == 0 and p0["snaps"][1]["counts"]["genocide"] == 1
    assert p0["snaps"][1]["vals"] == {} and not any(k.startswith("G_") for k in p0["snaps"][1]["c"])
    p2 = by["Plain 2"]["snaps"]
    assert p2[2]["counts"]["apartheid"] == 1 and p2[2]["ev"]["sentence"]["res_counts"]["apartheid"] == 0, p2[2]["ev"]
    n = by["New page"]
    assert n["snaps"][0] is None and n["snaps"][2] is not None
    assert n["existed_2021"] is False and n["created_later"] is True and n["created"].startswith("2022")
    w = by["Was redirect"]
    assert w["snaps"][0] is None and w["existed_2021"] is True and not w["created_later"]
    gpage = by["Gone page"]
    assert gpage["deleted"] and not gpage["created_later"] and not gpage["existed_2021"]
    assert p0["pageviews"]["views_12m"] == 120 and sorted(p0["pageviews"]["monthly"]) == [f"2025{m:02d}" for m in range(11, 13)] + [f"2026{m:02d}" for m in range(1, 11)]
    pv = [u for u, _ in CALLS if "pageviews" in u and "Plain_0" in u]
    assert len(pv) == 1, pv
    newer = [q for _, q in CALLS if q.get("rvdir") == "newer"]
    assert {q["titles"] for q in newer} == {"New page", "Was redirect", "Gone page"}, "creation check only when the 2021 lead is missing"


def test_strict_lead_failure_is_error():
    reset("strict")
    FAIL.add("Plain 3")
    try:
        R.collect({"title": "Plain 3", "group": "random", "project": None}, NOW)
    except RuntimeError as e:
        assert "lead fetch failed" in str(e)
    else:
        raise AssertionError("a failed lead fetch must raise, not count as a missing lead")
    assert MN.lead_at("Plain 3", "2021-01-01T00:00:00Z") is None     # non-strict default unchanged (mass_narr / mass2)


def test_resume():
    reset("resume")
    rows = make_frame(PLAIN[:8])
    R.run_shard(0, 1)
    p = os.path.join(R.RDIR, "rand_0.json.gz")
    done = json.load(gzip.open(p, "rt"))
    assert len(done) == 8
    json.dump(done[:5], gzip.open(p, "wt"))          # simulate an interrupted shard
    CALLS.clear()
    R.run_shard(0, 1)
    done2 = json.load(gzip.open(p, "rt"))
    assert sorted(r["title"] for r in done2) == sorted(r["title"] for r in rows)
    fetched = {q.get("titles") for _, q in CALLS if q.get("prop") == "revisions"}
    assert fetched == {r["title"] for r in done[5:]}, fetched


def test_fail_loud():
    reset("failloud")
    make_frame(PLAIN[:10])
    FAIL.update({"Plain 1", "Plain 6"})               # 2/10 = 20% > 5%
    try:
        R.run_shard(0, 1)
    except SystemExit as e:
        assert "failed (>5%)" in str(e), e
    else:
        raise AssertionError("shard with 20% errors must exit non-zero")
    done = json.load(gzip.open(os.path.join(R.RDIR, "rand_0.json.gz"), "rt"))
    assert len(done) == 8, "successful rows are still checkpointed"


def snap(w, crit, res):
    """Toy snap: `crit` genocide hits, `res` of them in the residual."""
    cnt = {k: 0 for k in R.CRIT}; cnt["genocide"] = crit
    rc = {k: 0 for k in R.CRIT}; rc["genocide"] = res
    return {"date": "x", "words": w, "crit": crit * 1e4 / w, "counts": cnt, "lead_prose": "p",
            "ev": {"sentence": {"event_share": 0.0, "event_sentences": 0, "res_words": w, "res_counts": rc, "ev_words": 0, "ev_counts": None}}}


def test_merge_math():
    d = reset("merge")
    toy = {  # title: snaps (w, crit, res) at 2021, 2023-07, now
        "A": [(100, 0, 0), (100, 0, 0), (100, 1, 0)],     # post-war gain, event part: +100/10k unfiltered, residual 0
        "B": [(100, 0, 0), (200, 2, 2), (200, 2, 2)],     # pre-war gain, residual: +100/10k pre
        "C": [(50, 1, 1), (50, 1, 1), (100, 1, 1)],       # no count change; rate falls post-war: -100/10k, residual -100
        "D": [(100, 0, 0), (100, 0, 0), (100, 0, 0)],     # nothing
        "E": [(10, 0, 0), (100, 0, 0), (100, 1, 1)],      # 2021 lead < 20 words -> outside the panel
    }
    rows = [{"title": t, "pageid": i, "group": "random", "project": None, "importance": None, "drawn_at": "t"}
            for i, t in enumerate(list(toy) + ["F", "G"])]
    json.dump({"now": NOW, "rows": rows, "rounds": 1}, open(os.path.join(R.RDIR, "frame.json"), "w"))
    out = [{**r, "snaps": [snap(*x) for x in toy[r["title"]]], "existed_2021": True, "created_later": False, "created": None,
            "deleted": False, "pageviews": {"views_12m": 5}} for r in rows[:5]]
    out.append({**rows[5], "snaps": [None, snap(100, 0, 0), snap(100, 5, 0)], "existed_2021": False, "created_later": True,
                "created": "2022-01-01T00:00:00Z", "deleted": False, "pageviews": {"views_12m": None}})
    json.dump(out[:3], gzip.open(os.path.join(R.RDIR, "rand_0.json.gz"), "wt"))
    json.dump(out[3:], gzip.open(os.path.join(R.RDIR, "rand_1.json.gz"), "wt"))
    try:
        R.merge()                                     # 6/7 rows < 95% -> fails loudly, files still written
    except SystemExit as e:
        assert "<95%" in str(e)
    else:
        raise AssertionError("merge with 6/7 rows must exit non-zero")
    res = json.load(open(os.path.join(d, "random_baseline.json")))
    s = res["summary"]
    assert s["n"] == 4 and s["collected"] == 6 and s["flags"]["created_later"] == 1 and s["flags"]["lead_2021_missing"] == 1
    pre, post = s["pre"], s["post"]
    assert pre["share_gaining"] == 0.25 and post["share_gaining"] == 0.25 and post["share_losing"] == 0.0
    assert abs(pre["mean_change_per10k"] - 25.0) < 1e-9, pre          # (0 + 100 + 0 + 0) / 4
    assert abs(post["mean_change_per10k"] - 0.0) < 1e-9, post         # (100 + 0 - 100 + 0) / 4
    assert abs(post["residual_change_per10k"] + 25.0) < 1e-9          # (0 + 0 - 100 + 0) / 4
    assert abs(post["event_change_per10k"] - 25.0) < 1e-9             # A's event sentence
    assert post["residual_share"] is None                             # unfiltered change 0 -> undefined
    assert abs(pre["residual_share"] - 1.0) < 1e-9 and pre["share_gaining_residual"] == 0.25
    assert abs(post["pooled_change_per10k"] - (4 / 500 - 3 / 450) * 1e4) < 1e-3
    assert post["share_lead_words_changed"] == 0.25 and pre["share_lead_words_changed"] == 0.25
    lo, hi = pre["mean_change_per10k_ci"]; assert lo <= 25.0 <= hi
    a = res["articles"]["A"]
    assert set(a["snaps"][0]) == {"date", "words", "crit", "counts", "ev"} and "lead_prose" not in a["snaps"][0]
    assert a["snaps"][2]["ev"]["sentence"]["res_counts"]["genocide"] == 0
    leads = json.load(gzip.open(os.path.join(d, "random_leads.json.gz"), "rt"))
    assert leads["leads"]["A"] == ["p", "p", "p"]
    return d


def test_analyze():
    d = test_merge_math()
    R.NB = 200
    mk = lambda tri: [snap(*x) for x in tri]
    topic = {f"T{i}": {"group": "topic", "snaps": mk([(100, 0, 0), (100, 0, 0), (100, 2, 2)] if i % 2 else [(100, 0, 0)] * 3)} for i in range(40)}
    comp = {f"C{i}": {"group": "comparison", "snaps": mk([(100, 0, 0), (100, 0, 0), (100, 1, 0)] if i % 4 == 0 else [(100, 0, 0)] * 3)} for i in range(40)}
    json.dump({"articles": {**topic, **comp}}, open(os.path.join(d, "mass_narr.json"), "w"))
    m2 = [{"title": t, "group": a["group"], "stratum": a["group"],
           "at": {"2021-01-01": {"narr": a["snaps"][0]}, "2023-07-01": {"narr": {"same_as": "2021-01-01"}}, "now": {"narr": a["snaps"][2]}}}
          for t, a in {**topic, **comp}.items()]
    m2.append({"title": "Atro", "group": "comparison", "stratum": "atrocity", "at": {k: {"narr": snap(100, 9, 9)} for k in ("2021-01-01", "2023-07-01", "now")}})
    json.dump({"articles": m2}, gzip.open(os.path.join(d, "mass2.json.gz"), "wt"))
    md = os.path.join(d, "random_baseline.md")
    out = R.analyze(d, md)
    txt = open(md).read()
    for k in range(1, 6):
        assert f"## {k}. " in txt, k
    s = out["summaries"]
    assert s["mass_narr/topic"]["n"] == 40 and s["mass2/comparison"]["n"] == 40, "atrocity stratum excluded from mass2 comparison"
    assert abs(s["mass2/topic"]["post"]["mean_change_per10k"] - 100.0) < 1e-9   # same_as resolved: 2023 = 2021 snap
    dd = out["diffs"][("mass_narr", "topic", "chg", "post")]
    assert abs(dd["est"] - 100.0) < 1e-9 and dd["ci"][0] > 0
    assert "**What we see:**" in txt and "**Caveat:**" in txt


TESTS = [test_sample_dedupe_redirect_disambig, test_sample_truncates_deterministically, test_groups_for_random,
         test_collect_cases, test_strict_lead_failure_is_error, test_resume, test_fail_loud, test_merge_math, test_analyze]

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
