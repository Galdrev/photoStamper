"""Offline tests for coord.py and analyze_coord.py: a fake Wikipedia behind wt_net.get_json (no network).

  python test_coord.py            -> exits non-zero on any failed check
  python test_coord.py collector  -> collector checks only (fast; the workflow's shard self-test)
Collector: missing / deleted revisions, suppressed (hidden) users, texthidden revisions, an empty diff, page creation, term
sentence extraction + shingles, one consistent hash per account across shards, resume from checkpoint (no re-fetch), fail-loud
above 5% revision errors, no usernames or salt in any output.
Analysis: planted bloc (5 accounts co-editing 8 articles in a 2-hour window) among random noise, 1,000 null draws: the bloc
is found (bloc card and network.json community) and no noise-only group is flagged; planted copy-paste sweep found; outputs
carry no hashes, usernames or salt.
"""
import glob, gzip, html, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SALT = "test-salt-7f3a9c"
os.environ["WT_SALT"] = SALT
os.environ["WT_JOB"] = "coord-test"
import wt_net            # noqa: E402
import coord as CO       # noqa: E402
import mass as M         # noqa: E402
import analyze as A      # noqa: E402

FAILS = []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg, flush=True)
    if not cond:
        FAILS.append(msg)


# ------------------------------------------------------------------ fake wiki
USERS = {"AlphaEditor": {"registration": "2015-03-01T00:00:00Z", "editcount": 41000, "groups": ["*", "user", "autoconfirmed", "extendedconfirmed"]},
         "BetaNewbie": {"registration": "2024-09-20T00:00:00Z", "editcount": 120, "groups": ["*", "user", "autoconfirmed"],
                        "blockid": 5, "blockexpiry": "infinite", "blockreason": "Abusing multiple accounts: [[User:AlphaEditor]]"},
         "GammaRegular": {"registration": "2019-01-01T00:00:00Z", "editcount": 2300, "groups": ["*", "user", "autoconfirmed", "rollbacker"]},
         "DeltaGone": None}
REVS = {}
FAIL_DIFF = set()
CALLS = []


def add_rev(revid, title, user, ts, parent, **kw):
    REVS[revid] = {"revid": revid, "parentid": parent, "user": user, "timestamp": ts, "title": title,
                   "comment": kw.pop("comment", f"rv edits by [[User:{user}]]"), "size": 5000 + revid % 97, "tags": kw.pop("tags", ["mw-undo"]),
                   "sha1": f"{revid:040x}", **kw}


def build_wiki(n_articles=30):
    REVS.clear(); FAIL_DIFF.clear()
    rows, rid = [], 1000
    users = ["AlphaEditor", "BetaNewbie", "GammaRegular", "DeltaGone", "192.0.2.4", "CleanupBot"]
    for i in range(n_articles):
        t = f"Article {i}"
        revs = []
        for k in range(3):
            rid += 1
            u = users[(i + k) % len(users)]
            add_rev(rid, t, u, f"2024-0{1 + k}-{10 + i % 18:02d}T12:{k:02d}:00Z", rid - 1 if k else (rid - 500))
            revs.append({"revid": rid, "ts": REVS[rid]["timestamp"], "events": [{"term": "genocide", "kind": "insert" if k % 2 == 0 else "remove", "src": "mass2"}]})
        rows.append({"title": t, "group": "topic" if i % 2 == 0 else "comparison", "stratum": None, "village": i == 4, "revs": revs})
    # special cases on Article 0..3
    s = rows[0]["revs"]
    REVS.pop(s[0]["revid"])                                                    # missing / deleted revision -> badrevids
    REVS[s[1]["revid"]].update(userhidden=True, suppressed=True, user=None)    # suppressed user
    REVS[s[2]["revid"]]["empty"] = True                                        # empty diff
    s = rows[1]["revs"]
    REVS[s[0]["revid"]]["texthidden"] = True                                   # revision-deleted text
    REVS[s[1]["revid"]]["parentid"] = 0                                        # page creation
    REVS[s[2]["revid"]]["parent_deleted"] = True                               # compare -> nosuchrevid
    return rows


def diff_body(rev):
    t = rev["title"]
    gen = f"'''{t}''' was the site of a [[genocide]] according to several historians.<ref>Smith 2020</ref> It lies on the coast."
    old = f"'''{t}''' was the site of a massacre. It lies on the coast."
    add, rem = (html.escape(gen), html.escape(old)) if rev["revid"] % 2 else (html.escape(old), html.escape(gen))
    add = add.replace("genocide", '<ins class="diffchange">genocide</ins>', 1)
    return ('<tr><td colspan="2" class="diff-lineno">Line 1:</td></tr><tr><td class="diff-marker">-</td>'
            f'<td class="diff-deletedline diff-side-deleted"><div>{rem}</div></td><td class="diff-marker">+</td>'
            f'<td class="diff-addedline diff-side-added"><div>{add}</div></td></tr>')


def mock_get(url, params, tries=8, ok404=False):
    CALLS.append(params.get("action") + ":" + str(params.get("prop") or params.get("list")))
    p = params
    if p.get("action") == "query" and p.get("prop") == "revisions":
        ids = [int(x) for x in str(p["revids"]).split("|")]
        pages, bad = {}, {}
        for i in ids:
            r = REVS.get(i)
            if r is None:
                bad[str(i)] = {"revid": i, "missing": True}; continue
            out = {k: v for k, v in r.items() if k not in ("title", "empty", "parent_deleted") and v is not None}
            if r.get("userhidden"):
                out.pop("user", None)
            pages.setdefault(r["title"], {"title": r["title"], "revisions": []})["revisions"].append(out)
        q = {"pages": list(pages.values())}
        if bad:
            q["badrevids"] = bad
        return {"query": q}
    if p.get("action") == "compare":
        r = REVS.get(int(p["torev"]))
        if r is None or int(p["torev"]) in FAIL_DIFF:
            return None
        if r.get("parent_deleted"):
            return {"error": {"code": "nosuchrevid", "info": "There is no revision with ID"}}
        if r.get("empty"):
            return {"compare": {"fromsize": 10, "tosize": 10, "body": ""}}
        return {"compare": {"fromsize": 5000, "tosize": 5040, "body": diff_body(r)}}
    if p.get("action") == "query" and p.get("list") == "users":
        out = []
        for n in p["ususers"].split("|"):
            f = USERS.get(n)
            out.append({"name": n, "missing": True} if f is None else {"name": n, **f})
        return {"query": {"users": out}}
    raise AssertionError(f"unmocked request {params}")


def setup(tmp):
    wt_net.get_json = mock_get
    wt_net._wait_slot = lambda: None
    wt_net.STATUS_DIR = os.path.join(tmp, "status")
    CO.OUT = os.path.join(tmp, "coord"); os.makedirs(CO.OUT, exist_ok=True)
    A.DATA = tmp
    import pilot as P
    P._ucache.clear()


def all_text(tmp):
    out = []
    for f in glob.glob(os.path.join(tmp, "**", "*"), recursive=True):
        if os.path.isfile(f):
            b = open(f, "rb").read()
            if f.endswith(".gz"):
                b = gzip.decompress(b)
            out.append((f, b.decode("utf-8", "replace")))
    return out


def test_collector():
    tmp = tempfile.mkdtemp(prefix="coordtest_")
    try:
        setup(tmp)
        rows = build_wiki()
        json.dump({"rows": rows, "n_revisions": sum(len(r["revs"]) for r in rows)}, open(os.path.join(CO.OUT, "plan.json"), "w"))
        CALLS.clear()
        for i in range(2):
            CO.run_shard(i, 2)
        n_first = len(CALLS)
        recs = {r["title"]: r for i in range(2) for r in json.load(gzip.open(os.path.join(CO.OUT, f"coord_{i}.json.gz"), "rt"))}
        check(len(recs) == 30, f"all 30 articles collected ({len(recs)})")
        a0 = {r["revid"]: r for r in recs["Article 0"]["revs"]}
        r0 = rows[0]["revs"]
        check(a0[r0[0]["revid"]]["state"] == "missing" and a0[r0[0]["revid"]]["diff_status"] == "missing", "deleted revision -> state missing")
        check(a0[r0[1]["revid"]]["user_hidden"] and a0[r0[1]["revid"]]["u"] is None and a0[r0[1]["revid"]]["suppressed"],
              "suppressed user -> no hash, user_hidden + suppressed flags")
        check(a0[r0[2]["revid"]]["diff_status"] == "empty" and "added" not in a0[r0[2]["revid"]], "empty diff -> status empty, no sentences")
        a1 = {r["revid"]: r for r in recs["Article 1"]["revs"]}
        r1 = rows[1]["revs"]
        check(a1[r1[0]["revid"]]["diff_status"] == "hidden", "texthidden revision -> diff hidden, no compare call")
        check(a1[r1[1]["revid"]]["diff_status"] == "creation", "page creation -> creation")
        check(a1[r1[2]["revid"]]["diff_status"] == "deleted", "deleted parent (nosuchrevid) -> deleted, not an error")
        ok = [r for a in recs.values() for r in a["revs"] if r.get("diff_status") == "ok"]
        check(ok and all(r.get("added") or r.get("removed") for r in ok), "term sentences extracted from every ok diff")
        ins = [x for r in ok for x in r.get("added") or []]
        check(ins and all("genocide" in x["s"] and "<ref" not in x["s"] and len(x["s"]) <= 600 and x["sh"] for x in ins),
              "inserted sentences: prose-cleaned, term-bearing, capped, shingled")
        check(not any("coast" in x["s"] for r in ok for x in (r.get("added") or []) + (r.get("removed") or [])),
              "unchanged / term-free sentences are dropped")
        check(all(r.get("comment_class") for r in ok) and not any("comment" in r for r in ok), "edit summaries reduced to classes")
        hashes = {}
        for a in recs.values():
            for r in a["revs"]:
                if r.get("u"):
                    hashes.setdefault(r["u"], set()).add(a["title"])
        check(CO.h("AlphaEditor") in hashes and len(hashes[CO.h("AlphaEditor")]) > 3, "one hash per account across articles and shards")
        accs = {k: v for a in recs.values() for k, v in a["accounts"].items()}
        b = accs.get(CO.h("BetaNewbie")) or {}
        check(b.get("indef") and b.get("breason") == "sock" and b.get("reg") == "2024-09", "account facts: block class, reg month")
        check(accs.get(CO.h("DeltaGone"), {}).get("missing"), "missing user account recorded as missing")
        check(all(len(k) == 16 for k in hashes), "hashes are 16 hex chars")
        # resume: drop half of shard 0's checkpoint, re-run, only those articles re-fetched
        p0 = os.path.join(CO.OUT, "coord_0.json.gz")
        s0 = json.load(gzip.open(p0, "rt")); keep = s0[: len(s0) // 2]
        json.dump(keep, gzip.open(p0, "wt"))
        import pilot as P; P._ucache.clear()
        CALLS.clear()
        CO.run_shard(0, 2)
        s0b = json.load(gzip.open(p0, "rt"))
        n_meta = sum(1 for c in CALLS if c == "query:revisions")
        check(len(s0b) == len(s0) and len({r["title"] for r in s0b}) == len(s0), f"resume completes shard 0 without duplicates ({len(s0b)})")
        check(n_meta == len(s0) - len(keep), f"resume re-fetches only the missing articles ({n_meta} metadata calls for {len(s0) - len(keep)})")
        check(len(CALLS) < n_first, "resume makes fewer requests than the first run")
        # merge
        CO.merge()
        D = json.load(gzip.open(os.path.join(tmp, "coord.json.gz"), "rt"))
        check(D["summary"]["n_articles"] == 30 and D["coactivity"], "merge: all articles + co-activity table")
        co = D["coactivity"].get(CO.h("AlphaEditor"))
        check(co and len(co["articles"]) > 3 and co["events"][0][1], "co-activity: articles and timestamps per account")
        # fail loud above 5% revision errors
        FAIL_DIFF.update(r["revid"] for r in rows[2]["revs"] + rows[4]["revs"] + rows[6]["revs"])
        os.remove(p0); P._ucache.clear()
        rc = None
        try:
            CO.run_shard(0, 2)
        except SystemExit as e:
            rc = e.code
        check(rc is not None and ">5%" in str(rc), f"fail-loud when >5% of revisions fail ({rc})")
        left = json.load(gzip.open(p0, "rt"))
        check(not any(r.get("error") for a in left for r in a["revs"]), "failed articles dropped from checkpoint so a re-run retries them")
        FAIL_DIFF.clear()
        # missing salt refuses to run
        r = subprocess.run([sys.executable, "-c", "import os,sys; sys.path.insert(0,%r); os.environ.pop('WT_SALT',None); "
                            "import coord; coord.h('x')" % HERE], capture_output=True, text=True, env={**os.environ, "WT_SALT": ""})
        check(r.returncode != 0 and "WT_SALT is required" in r.stderr, "no WT_SALT -> refuses to run")
        # analysis on collected data, then the privacy scan over every file written
        import analyze_coord as AC
        R = AC.analyze_data(D, n_null=50, n_calib=5, log=lambda *a: None)
        AC.write_outputs(R, os.path.join(tmp, "patterns"))
        leaks = [(f, n) for f, txt in all_text(tmp) for n in list(USERS) + ["192.0.2.4", "CleanupBot", SALT] if n in txt]
        check(not leaks, f"no usernames, IPs or salt in any output file ({leaks[:3]})")
        hx = [(f, k) for f, txt in all_text(os.path.join(tmp, "patterns")) for k in hashes if k in txt]
        check(not hx, f"no account hashes in cards / chart data ({hx[:3]})")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ------------------------------------------------------------------ planted bloc
def synthetic(seed=3, n_noise=400, n_topic=200, n_comp=150, planted=True):
    import numpy as np
    rng = np.random.default_rng(seed)
    arts = {f"T{i}": {"group": "topic", "village": i < 20} for i in range(n_topic)}
    arts.update({f"C{i}": {"group": "comparison", "village": False} for i in range(n_comp)})
    t0, t1 = 1609459200.0, 1793491200.0          # 2021-01-01 .. 2026-11
    revs, rid, accounts = [], 10 ** 6, {}
    def ts(t):
        import time as _t
        return _t.strftime("%Y-%m-%dT%H:%M:%SZ", _t.gmtime(t))
    def ev(u, title, t, kind, sent=None):
        nonlocal rid
        rid += 1
        r = {"title": title, "revid": rid, "ts": ts(t), "state": "ok", "u": u, "anon": False, "bot": False, "user_hidden": False,
             "events": [{"term": "genocide", "kind": kind, "src": "mass2"}], "diff_status": "ok", "age_d": int(rng.integers(5, 4000))}
        if sent and kind == "insert":
            r["added"] = [{"s": sent, "terms": ["genocide"]}]
        revs.append(r)
    import analyze_coord as AC
    for g, n_art, pre in (("topic", n_topic, "T"), ("comparison", n_comp, "C")):
        # noise: heavy-tailed account activity and article popularity, then randomised by long curveball mixing so the noise is
        # an exact draw from the degree-preserving null (weighted sampling alone leaves hub-sharing structure behind)
        w = 1 / np.arange(1, n_art + 1) ** 0.8; w /= w.sum()
        names, rows = [], []
        for k in range(n_noise if g == "topic" else n_noise // 2):
            u = f"{g[0]}noise{k:04d}".ljust(16, "x")
            accounts[u] = {"reg": "2018-01", "ec": int(rng.integers(50, 50000)), "blocked": bool(rng.random() < 0.05), "indef": False}
            deg = min(n_art, 1 + int(rng.geometric(0.3)))
            names.append(u); rows.append(set(int(a) for a in rng.choice(n_art, size=deg, replace=False, p=w)))
        flat = next(AC.curveball(rows, 1, rng, thin=60 * len(rows), burn=0))
        off = np.concatenate([[0], np.cumsum([len(r) for r in rows])])
        for k, u in enumerate(names):
            for a in flat[off[k]:off[k + 1]]:
                for _ in range(1 + int(rng.random() < 0.3)):
                    s = f"Noise sentence {rng.integers(10 ** 9)} about genocide in place {a} with words {rng.integers(10 ** 6)}."
                    ev(u, f"{pre}{a}", rng.uniform(t0, t1), "insert" if rng.random() < 0.5 else "remove", s)
    planted_u, planted_a = [], []
    if planted:
        planted_a = [f"T{i}" for i in rng.choice(np.arange(30, n_topic), size=8, replace=False)]
        base = 1710072000.0                       # 2024-03-10 12:00
        for k in range(5):
            u = f"planted{k}".ljust(16, "y"); planted_u.append(u)
            accounts[u] = {"reg": "2024-02", "ec": 80, "blocked": True, "indef": True, "breason": "sock"}
            for a in planted_a:
                ev(u, a, base + rng.uniform(0, 7200), "insert",
                   "The campaign of mass killing in the region has been described as a genocide by several scholars.")
            for a in rng.choice(n_topic, size=2, replace=False):     # a little cover activity
                ev(u, f"T{a}", rng.uniform(t0, t1), "remove")
    return {"summary": {"n_revisions": len(revs)}, "articles": arts, "revisions": revs, "accounts": accounts}, planted_u, planted_a


def test_planted():
    import analyze_coord as AC
    D, pu, pa = synthetic()
    R = AC.analyze_data(D, n_null=1000, n_calib=50, directions=("any", "insert"))
    pset = set(pu)
    def members(rec, m):
        return {rec["_accs"][i] for i in m}
    found, noise_flags = [], []
    for key, rec in R["engines"].items():
        for b in rec["blocs"]["blocs"]:
            ms = members(rec, b["_m"])
            if len(ms & pset) >= 4:
                found.append((key, b["confidence"], len(ms), len(ms & pset)))
            elif b["confidence"] in ("high", "medium") and len(ms & pset) < len(ms) / 2:
                noise_flags.append((key, b["confidence"], len(ms)))
    top = [f for f in found if f[0] == "topic/any"]
    check(top and top[0][1] == "high" and top[0][3] == 5 and top[0][2] <= 7,
          f"planted bloc found in topic/any at high confidence with all 5 accounts ({top})")
    check(any(f[0] == "topic/insert" and f[1] == "high" for f in found), f"planted bloc found among inserters ({found})")
    check(not noise_flags, f"no noise-only bloc flagged ({noise_flags})")
    ta = R["engines"]["topic/any"]
    ex = ta["blocs"]["expected_by_chance"]
    print(f"     blocs topic/any: {len(ta['blocs']['blocs'])} groups, chance {ex}")
    # sync
    sp = ta["sync"]["pairs"]
    acc = ta["_accs"]
    sync_planted = [p for p in sp if {acc[p["_pid"] // len(acc)], acc[p["_pid"] % len(acc)]} <= pset]
    check(len(sync_planted) >= 8, f"synchrony: planted pairs flagged ({len(sync_planted)} of 10)")
    noise_sync = [p for p in sp if not ({acc[p["_pid"] // len(acc)], acc[p["_pid"] % len(acc)]} & pset)]
    check(len(noise_sync) <= max(3, 2 * (ta["sync"]["expected_by_chance"]["edges_p95"] or 0)),
          f"synchrony: noise pairs within chance ({len(noise_sync)}, chance {ta['sync']['expected_by_chance']})")
    # network community
    net = ta["network"]
    comm = [c for c in net["communities"] if len(members(ta, c["_m"]) & pset) >= 4]
    check(comm and comm[0]["confidence"] == "high", f"network: planted bloc is a high-confidence community ({[(c['size'], c['confidence']) for c in comm]})")
    nz = [c for c in net["communities"] if c["confidence"] in ("high", "medium") and not (members(ta, c["_m"]) & pset)]
    check(not nz, f"network: no noise-only community significant ({[(c['size'], c['confidence']) for c in nz]})")
    tmp = tempfile.mkdtemp(prefix="coordplant_")
    try:
        AC.write_outputs(R, tmp)
        N = json.load(open(os.path.join(tmp, "chart_data", "network.json")))
        tn = N["topic"]
        pc = [c for c in tn["communities"] if c["confidence"] == "high" and set(pa) <= {a["title"] for a in c["articles"]}]
        check(pc and pc[0]["size"] >= 5, f"network.json: planted bloc is a community covering its 8 articles ({[(c['size']) for c in pc]})")
        check(pc and pc[0]["direction"]["insert_share"] > 0.7 and pc[0]["inserted_phrases"], "network.json community: insert-dominant, phrases quoted")
        labs = {n["id"] for n in tn["nodes"]}
        check(all(re.fullmatch(r"A\d+", x) for x in labs) and all(e["source"] in labs and e["target"] in labs for e in tn["edges"]),
              "network.json: nodes labelled A1.. and edges reference them")
        e0 = tn["edges"][0] if tn["edges"] else {}
        check(all(k in e0 for k in ("weight", "observed", "null_mean", "null_p95", "p", "same_direction_share", "example_article_pairs",
                                    "time_span", "windows")), "network.json: edge fields present")
        check("comparison" in N and "expected_by_chance" in N["comparison"]["counts"], "network.json: comparison side + chance counts")
        print(f"     network topic: {tn['counts']}  comparison: {N['comparison']['counts']}")
        sw = json.load(open(os.path.join(tmp, "chart_data", "sweeps.json")))
        ps = [c for c in sw["clusters"] if c["n_articles"] >= 8 and "genocide by several scholars" in c["phrase"]]
        check(ps and ps[0]["confidence"] == "high" and ps[0]["distinct_accounts"] == 5, f"planted copy-paste sweep found ({ps[:1]})")
        check(len([c for c in sw["clusters"] if "Noise sentence" in c["phrase"]]) == 0, "noise sentences form no sweep")
        txt = "".join(t for _, t in all_text(tmp))
        leaks = [u for u in D["accounts"] if u in txt]
        check(not leaks, f"no account ids in analysis outputs ({leaks[:3]})")
        cards = json.load(open(os.path.join(tmp, "cards.json")))["cards"]
        check(all(c.get("confidence") and c.get("null_model") for c in cards), "every card has a confidence and a null model")
        check(any("Bloc A (" in c["what_we_see"] for c in cards), "blocs named 'Bloc A (n accounts)'")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    # null-only data: nothing flagged
    D0, _, _ = synthetic(seed=5, planted=False)
    R0 = AC.analyze_data(D0, n_null=1000, n_calib=50, directions=("any",))
    fl = [(k, b["size"], b["confidence"]) for k, rec in R0["engines"].items() for b in rec["blocs"]["blocs"] if b["confidence"] != "low"]
    fc = [(k, c["size"], c["confidence"]) for k, rec in R0["engines"].items() for c in rec["network"]["communities"]
          if c["confidence"] in ("high", "medium")]
    check(not fl and not fc, f"pure noise: no bloc or community flagged ({fl}, {fc})")


if __name__ == "__main__":
    test_collector()
    if len(sys.argv) < 2 or sys.argv[1] != "collector":
        test_planted()
    print(f"\n{len(FAILS)} failed check(s)" if FAILS else "\nall checks passed")
    sys.exit(1 if FAILS else 0)
