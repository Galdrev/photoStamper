"""Offline tests for trail.py and analyze_trail.py (no network: a fake Wikipedia behind wt_net.get_json).

  python test_trail.py           -> exits non-zero on any failed check
Collector: guard.py scope matching, 2021+ histories with a pre-2021 baseline, usernames hashed at once, section edits
not fetched (lead inherited), sha1 repeats copied, critical / connection counts via rvsection=0, population ranking,
usercontribs (namespace 0 in full, talk namespaces counted, names used only in memory), PageAssessments, discovery
measurements of outside articles edited by >= 3 accounts, extras (2021 vs now first sentence, pageviews), and no username
or salt anywhere in the raw file or the published outputs.
Analysis (synthetic, planted): the topic population is concentrated on Israel / Palestine, one-directional, persistent
across articles, re-inserts after reverts and spikes after calendar events; the comparison population is not. Checks: each
planted pattern gives a "consistent with" verdict; a no-plant world gives "not distinguishable from" for the core metrics;
the discovery list needs >= 3 distinct accounts and excludes scoped titles; outputs pass analyze_coord.privacy_scan, carry
no hash / username / salt / per-account rows, and small cells are <3.
"""
import glob, gzip, json, os, re, shutil, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SALT = "trail-test-salt-5d1e"
os.environ["WT_SALT"] = SALT
os.environ["WT_JOB"] = "trail-test"
import numpy as np            # noqa: E402
import wt_net                 # noqa: E402
import coord as CO            # noqa: E402
import analyze as A           # noqa: E402
import analyze_guard as AG    # noqa: E402
import analyze_trail as AT    # noqa: E402
import trail as T             # noqa: E402

FAILS = []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg, flush=True)
    if not cond:
        FAILS.append(msg)


def ts(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))


# ------------------------------------------------------------------ fake wiki
TOPIC_USERS = ["Alicewriter", "Bobpusher", "Carol Editor", "Danwiki"]
COMP_USERS = ["Evegnome", "Frankfixer", "Gretamaps"]
OTHER = ["203.0.113.9", "ClueBot NG", "Hankrandom"]
REV = {}          # revid -> dict(title, user, t, lead, comment, sha, tags, parent)
PAGES = {}        # title -> [revids] chronological
CALLS = {"revids": 0}
BASE = "Lead text."


def add_rev(title, user, t, lead, comment="", tags=None, rid=[3000000]):
    rid[0] += 1
    prev = PAGES.setdefault(title, [])
    REV[rid[0]] = {"title": title, "user": user, "t": t, "lead": lead, "comment": comment, "tags": tags or [],
                   "sha": f"{abs(hash(lead)) % (16 ** 12):040x}", "parent": prev[-1] if prev else 0}
    prev.append(rid[0])
    return rid[0]


def build_fake():
    REV.clear(); PAGES.clear()
    t0 = 1577836800 + 86400 * 200       # mid 2020 (baseline)
    t1 = 1612137600                      # 2021-02-01
    for title, base, users in (("Israel", "Israel is a country.", TOPIC_USERS),
                               ("Hamas", "Hamas is an organisation.", TOPIC_USERS),
                               ("Ireland", "Ireland is an island.", COMP_USERS),
                               ("Ukraine", "Ukraine is a country.", COMP_USERS)):
        add_rev(title, "Hankrandom", t0, base)
        t = t1
        crit = base + " It is accused of apartheid and genocide."
        for k, u in enumerate(users):
            t += 86400 * 3
            add_rev(title, u, t, REV[PAGES[title][-1]]["lead"] + f" Edit {k}.")    # neutral lead edit
            if k < 3:
                t += 3600
                add_rev(title, u, t, crit if k % 2 == 0 else base + " Under occupation.")  # critical-term edit
            t += 3600
            add_rev(title, "Hankrandom", t, REV[PAGES[title][-1]]["lead"], comment="/* History */ body tweak")  # section edit
        add_rev(title, "203.0.113.9", t + 100, base)                                   # IP removes
        add_rev(title, "ClueBot NG", t + 200, crit, tags=["mw-rollback"])              # bot restores (sha repeat)
    # outside articles: three topic accounts insert critical terms in "Jewish town Q", two in "Small place"
    for title, users in (("Jewish town Q", TOPIC_USERS[:3]), ("Small place", TOPIC_USERS[:2]), ("Map article", COMP_USERS)):
        add_rev(title, "Hankrandom", t0, f"{title} is a town with a Jewish community.")
        t = t1 + 86400 * 400
        for k, u in enumerate(users):
            t += 86400
            add_rev(title, u, t, f"{title} is a town in the occupied West Bank." + " Occupied territories." * k)
            t += 60
            add_rev(title, u, t, REV[PAGES[title][-1]]["lead"], comment="/* Geography */ x")


def lead_of(rid):
    return REV[rid]["lead"] + "\n\n== History ==\nBody."


def api_rev(rid, content=False):
    r = REV[rid]
    d = {"revid": rid, "parentid": r["parent"], "timestamp": ts(r["t"]), "user": r["user"], "comment": r["comment"],
         "size": len(r["lead"]), "sha1": r["sha"], "tags": r["tags"]}
    if content:
        d["slots"] = {"main": {"content": A.split_lead(lead_of(rid))}}
    return d


def mock_get(url, params, tries=8, ok404=False):
    p = params
    if url.startswith("https://wikimedia.org/"):
        assert "/monthly/" in url
        return {"items": [{"timestamp": "2026010100", "views": 3000}, {"timestamp": "2026020100", "views": 1000}]}
    if p.get("prop") == "info":
        return {"query": {"pages": [{"title": t, "missing": True} if t.startswith("Missing") else
                                    {"title": t, "length": 1000 + 37 * len(t)} for t in p["titles"].split("|")]}}
    if p.get("prop") in ("pageassessments", "description|pageassessments"):
        pages = []
        for t in p["titles"].split("|"):
            pa = {"Israel": {}, "Palestine": {}} if t in ("Israel", "Hamas", "Jewish town Q", "Small place") else \
                 {"Jewish history": {}} if t == "Jewish town Q" else {"Ukraine": {}} if t in ("Ukraine", "Map article") else \
                 {"Ireland": {}} if t == "Ireland" else {}
            if t == "Jewish town Q":
                pa = {"Israel": {}, "Jewish history": {}}
            pg = {"title": t, "pageassessments": pa}
            if "description" in p["prop"]:
                pg["description"] = "town in the West Bank"
            pages.append(pg)
        return {"query": {"pages": pages}}
    if p.get("list") == "usercontribs":
        u = p["ucuser"]
        if p["ucnamespace"] != 0:
            return {"query": {"usercontribs": [{"timestamp": ts(1650000000)}] * 3}}
        mine = [rid for rid in sorted(REV) if REV[rid]["user"] == u and REV[rid]["t"] >= AG.ep(AT.FROM)]
        start = int(p.get("uccontinue", 0))
        chunk = mine[start:start + 2]
        out = {"query": {"usercontribs": [{"revid": r, "parentid": REV[r]["parent"], "title": REV[r]["title"],
                                           "timestamp": ts(REV[r]["t"]), "comment": REV[r]["comment"],
                                           "sizediff": 5, "tags": REV[r]["tags"]} for r in chunk]}}
        if start + 2 < len(mine):
            out["continue"] = {"uccontinue": str(start + 2), "continue": "-||"}
        return out
    if p.get("prop") == "revisions" and "revids" in p:
        assert str(p.get("rvsection")) == "0"
        ids = [int(x) for x in str(p["revids"]).split("|")]
        CALLS["revids"] += len(ids)
        return {"query": {"pages": [{"title": "x", "revisions": [api_rev(r, True) for r in ids if r in REV]}]}}
    if p.get("prop") == "revisions" and "titles" in p:
        t = p["titles"]
        revs = PAGES.get(t, [])
        if p.get("rvdir") == "older":
            lim = AG.ep(p["rvstart"]) if p.get("rvstart") else 1e12
            old = [r for r in revs if REV[r]["t"] <= lim]
            sel = old[-1:] if old else []
        elif p.get("rvlimit") == 1:
            sel = revs[-1:]
        else:
            new = [r for r in revs if REV[r]["t"] >= AG.ep(p["rvstart"])]
            start = int(p.get("rvcontinue", 0))
            sel = new[start:start + 4]
            if start + 4 < len(new):
                out = {"query": {"pages": [{"title": t, "revisions": [api_rev(r) for r in sel]}]},
                       "continue": {"rvcontinue": str(start + 4), "continue": "||"}}
                return out
        content = "content" in p.get("rvprop", "")
        return {"query": {"pages": [{"title": t, "revisions": [api_rev(r, content) for r in sel]}]}}
    raise AssertionError(f"unmocked request {params}")


def all_text(d):
    out = []
    for f in glob.glob(os.path.join(d, "**", "*"), recursive=True):
        if os.path.isfile(f):
            b = open(f, "rb").read()
            if f.endswith(".gz"):
                b = gzip.decompress(b)
            out.append((f, b.decode("utf-8", "replace")))
    return out


def test_collector(tmp):
    build_fake()
    wt_net.get_json = mock_get
    wt_net._wait_slot = lambda: None
    wt_net.STATUS_DIR = os.path.join(tmp, "status")
    T.OUT = os.path.join(tmp, "trail"); os.makedirs(T.OUT, exist_ok=True)
    T.N_POP = 3
    plan = {"topic": [{"title": "Israel", "tier": "core"}, {"title": "Hamas", "tier": "High"}, {"title": "Missing page", "tier": "Top"}],
            "pool": [{"title": "Ireland", "tier": "core"}, {"title": "Ukraine", "tier": "High"}]}
    json.dump(plan, open(os.path.join(T.OUT, "plan.json"), "w"))
    T.collect()
    D = json.load(gzip.open(os.path.join(T.OUT, "raw.json.gz"), "rt"))
    arts = {a["title"]: a for a in D["articles"]}
    check(set(arts) == {"Israel", "Hamas", "Ireland", "Ukraine"}, f"scope: 2 topic + 2 comparison matched ({sorted(arts)})")
    r = arts["Israel"]["revs"]
    n_israel = len(PAGES["Israel"])
    check(len(r) == n_israel and r[0][3] & AT.F_BASE, f"history since 2021 paged, baseline first ({len(r)} of {n_israel})")
    check(all(x[8] is not None for x in r), "every revision has a lead count (section edits inherited, sha repeats copied)")
    sect = [k for k, x in enumerate(PAGES["Israel"]) if REV[x]["comment"].startswith("/*")]
    check(all(r[k][8] == r[k - 1][8] for k in sect), "section edits inherit the previous lead count")
    crit_k = [k for k, x in enumerate(PAGES["Israel"]) if "apartheid" in REV[x]["lead"]]
    check(r[crit_k[0]][8] == 2, f"critical count of 'apartheid and genocide' is 2 ({r[crit_k[0]][8]})")
    check(r[0][2] == CO.h("Hankrandom") and r[-2][3] & AG.F_ANON and r[-1][3] & AG.F_BOT, "hashed, IP and bot flagged")
    pt = D["population"]["topic"]; pc = D["population"]["comparison"]
    check(len(pt) == 3 and all(u in {CO.h(n) for n in TOPIC_USERS} for u in pt), "topic population = top topic editors (hashed)")
    check(len(pc) == 3 and all(u in {CO.h(n) for n in COMP_USERS} for u in pc), "comparison population from comparison articles")
    c = D["contribs"][pt[0]]
    check(c["talk"] == 3 and len(c["ns0"]) > 2 and not c["truncated"], "usercontribs paged, talk counted")
    ti = D["titles"]
    check(any(ti[x[2]] == "Jewish town Q" for x in c["ns0"]) or any(ti[x[2]] == "Jewish town Q" for u in pt for x in D["contribs"][u]["ns0"]),
          "outside edits present in contributions")
    check(any(rw[5] & AT.C_SECT for u in pt for rw in D["contribs"][u]["ns0"]), "section-edit flag kept (no raw summary)")
    check(D["assess"].get("Jewish town Q") == ["Israel", "Jewish history"], f"assessments ({D['assess'].get('Jewish town Q')})")
    check(len(D["disc"]) > 0, f"outside-article leads measured ({len(D['disc'])})")
    ex = D["extras"]
    check("Jewish town Q" in ex and "Small place" not in ex, f"extras for qualifying outside articles only ({sorted(ex)})")
    e = ex.get("Jewish town Q") or {}
    check(e.get("first_2021_terms") == ["jewish community"] and "occupied west bank" in (e.get("first_now_terms") or []),
          f"first-sentence key terms 2021 vs now ({e.get('first_2021_terms')} -> {e.get('first_now_terms')})")
    check(e.get("views_month") == 2000, "mean monthly pageviews")
    for f, txt in all_text(T.OUT):
        for n in TOPIC_USERS + COMP_USERS + ["Hankrandom", SALT]:
            check(n not in txt, f"{os.path.basename(f)}: no {n!r}")
    check(not T._NAMES, "in-memory name map cleared")
    # analysis on the collector's raw output (smoke) + privacy gate
    out = os.path.join(tmp, "pub_small")
    R = AT.analyze(D, B=100, P=100)
    AT.write_outputs(R, out)
    lst = R["discovery"]["topic"]["articles"]
    check([a["title"] for a in lst] == ["Jewish town Q"], f"discovery: >=3 editors only, scoped excluded ({[a['title'] for a in lst]})")
    check(lst and lst[0]["distinct_editors_qualifying"] == 3 and lst[0]["net_critical_insertions"] > 0, "discovery counts")
    check(AT.scan(out) == [], f"privacy gate passes on the small run ({AT.scan(out)[:3]})")
    for f, txt in all_text(out):
        for n in TOPIC_USERS + COMP_USERS + ["Hankrandom", SALT] + [CO.h(x) for x in TOPIC_USERS + COMP_USERS]:
            check(n not in txt, f"published {os.path.basename(f)}: no {n[:6]!r}…")


# ------------------------------------------------------------------ synthetic world for the analysis
def synth(seed=3, plant=True, n_acc=40, n_art=30):
    rng = np.random.default_rng(seed)
    cal = json.load(open(AT.CAL))["events"]
    ip_weeks = sorted({AT.week_of(AG.ep(e["date"] + "T00:00:00Z")) for e in cal if e["type"] != "comparison"})
    ip_weeks = [w for w in ip_weeks if w >= 0]
    topic_t = [f"Topic article {k}" for k in range(n_art)]
    comp_t = [f"Comparison article {k}" for k in range(n_art)]
    tu = [CO.h(f"topicacct{k}") for k in range(n_acc)]
    cu = [CO.h(f"compacct{k}") for k in range(n_acc)]
    bg = [CO.h(f"background{k}") for k in range(30)]
    titles, tix = [], {}
    def tid(t):
        if t not in tix:
            tix[t] = len(titles); titles.append(t)
        return tix[t]
    contribs = {u: {"ns0": [], "talk": int(rng.integers(50, 500)), "truncated": False} for u in tu + cu}
    rid = [5000000]
    arts = []
    t_start, t_end = AG.ep("2021-02-01T00:00:00Z"), AG.ep("2026-10-01T00:00:00Z")
    def push_art(title, group, accts, p_dir, p_re):
        revs, c, sha = [], 3, 0
        rid[0] += 1
        revs.append([rid[0], t_start - 86400, bg[0], AT.F_BASE, sha, 100, -1, -1, c, 1])
        t = t_start
        shas = [sha]
        for k in range(60):
            t += int(rng.integers(3, 30)) * 86400
            if t > t_end:
                break
            u = accts[int(rng.integers(len(accts)))] if rng.random() < 0.7 else bg[int(rng.integers(len(bg)))]
            crit_edit = rng.random() < 0.5
            d = 0
            if crit_edit:
                d = 1 if rng.random() < (p_dir if u in accts else 0.5) else -1
                if c + d < 0:
                    d = 1
            sha += 1
            c += d
            rid[0] += 1
            revs.append([rid[0], t, u, 0, sha, 100 + c, -1, -1, c, 1]); shas.append(sha)
            if u in contribs:
                contribs[u]["ns0"].append([rid[0], revs[-2][0], tid(title), t, 5, 0])
            if d != 0 and u in accts and rng.random() < 0.4:
                # identity revert by a background account, then maybe re-insertion by the same account
                t += 3600; c -= d; rid[0] += 1
                revs.append([rid[0], t, bg[1], 0, shas[-2], 100 + c, -1, -1, c, 1]); shas.append(shas[-2])
                if rng.random() < p_re:
                    t += 86400 * 2; c += d; sha += 1; rid[0] += 1
                    revs.append([rid[0], t, u, 0, sha, 100 + c, -1, -1, c, 1]); shas.append(sha)
                    contribs[u]["ns0"].append([rid[0], revs[-2][0], tid(title), t, 5, 0])
        arts.append({"title": title, "group": group, "revs": revs})
    for t in topic_t:
        push_art(t, "topic", tu, 0.9 if plant else 0.5, 0.7 if plant else 0.25)
    for t in comp_t:
        push_art(t, "comparison", cu, 0.5, 0.25)
    assess = {t: ["Israel", "Palestine"] for t in topic_t}
    assess.update({t: ["Ukraine"] for t in comp_t})
    scope_pa = dict(assess)
    # outside mainspace edits: home share and spikes
    disc = {}
    for g, us in (("topic", tu), ("comparison", cu)):
        for u in us:
            share = 0.75 if (plant and g == "topic") else 0.35
            n = int(rng.integers(150, 400))
            if plant and g == "topic":
                hot = [ip_weeks[int(rng.integers(len(ip_weeks)))] + int(rng.integers(0, 2)) for _ in range(4)]
            else:
                hot = [int(rng.integers(0, 290)) for _ in range(4)]
            for k in range(n):
                home = rng.random() < share
                title = (f"IP outside {int(rng.integers(300))}" if g == "topic" else f"UA outside {int(rng.integers(300))}") \
                    if home else f"General article {int(rng.integers(3000))}"
                assess.setdefault(title, (["Israel"] if g == "topic" else ["Ukraine"]) if home else ["Science"])
                if rng.random() < 0.4:
                    tt = AT.WEEK0 + hot[int(rng.integers(4))] * 7 * 86400 + int(rng.integers(0, 6 * 86400))
                else:
                    tt = int(rng.integers(t_start, t_end))
                rid[0] += 1
                contribs[u]["ns0"].append([rid[0], rid[0] - 1, tid(title), tt, 3, AT.C_SECT if rng.random() < 0.6 else 0])
    # discovery: 5 topic accounts insert critical terms in "Jewish town Q"; 2 in "Small place"; a scoped title is excluded
    for title, us in (("Jewish town Q", tu[:5]), ("Small place", tu[5:7]), (topic_t[0], tu[7:12])):
        for u in us:
            rid[0] += 2
            contribs[u]["ns0"].append([rid[0], rid[0] - 1, tid(title), t_start + 86400 * 500, 40, 0])
            disc[str(rid[0] - 1)] = [0, 2]; disc[str(rid[0])] = [1, 1]
    assess["Jewish town Q"] = ["Israel", "Jewish history"]
    for u in tu + cu:
        contribs[u]["ns0"].sort(key=lambda r: r[3])
    extras = {"Jewish town Q": {"first_2021": "Jewish town Q is a town with a Jewish community.",
                                "first_now": "Jewish town Q is a town in the occupied West Bank.",
                                "first_2021_terms": ["jewish community"], "first_now_terms": ["occupied west bank"],
                                "lead_crit": [0, 1], "lead_conn": [2, 1], "created_after_2021": False,
                                "description": "town in the West Bank", "projects": ["Israel", "Jewish history"],
                                "views_month": 12345678, "in_wider_corpus": False}}
    return {"summary": {"window_end": "2026-11-01T00:00:00Z", "population_target": n_acc, "population_overlap": 0,
                        "history": {"done": 2 * n_art}, "leads": {"complete": 2 * n_art}},
            "scope": {"topic": topic_t, "comparison": comp_t}, "scope_assess": scope_pa, "articles": arts,
            "population": {"topic": tu, "comparison": cu}, "contribs": contribs, "titles": titles, "assess": assess,
            "disc": disc, "extras": extras}


def test_analysis(tmp):
    D = synth(plant=True)
    R = AT.analyze(D, B=300, P=300)
    out = os.path.join(tmp, "pub")
    AT.write_outputs(R, out)
    V = R["verdicts"]
    for k in ("topic_concentration", "direction_consistency", "cross_article_persistence", "reinsertion", "single_purpose", "timing"):
        check(V[k].startswith("consistent with"), f"planted {k}: {V[k][:90]}")
    P = R["patterns"]
    check(P["topic_concentration_ip"]["topic"] > 0.7 and P["topic_concentration_ip"]["comparison"] < 0.1,
          f"IP share topic {P['topic_concentration_ip']['topic']} vs comparison {P['topic_concentration_ip']['comparison']}")
    check(P["direction_consistency"]["difference_ci95"][0] > 0, "direction consistency CI above 0")
    lst = R["discovery"]["topic"]["articles"]
    names = [a["title"] for a in lst]
    check(names == ["Jewish town Q"], f"discovery list: >=3 editors, scoped excluded ({names})")
    check(lst[0]["distinct_editors_qualifying"] == 5 and lst[0]["net_critical_insertions"] == 5, "discovery counts (5 editors, +5)")
    cards = open(os.path.join(out, "cards.md")).read()
    arts_md = open(os.path.join(out, "articles.md")).read()
    check("NOT by itself evidence of a vendetta" in cards, "cards say concentration is not by itself evidence of a vendetta")
    check("12.3M" in arts_md and "12345678" not in arts_md, "large view counts formatted (privacy gate safe)")
    check(AT.scan(out) == [], f"privacy gate passes ({AT.scan(out)[:3]})")
    blob = "\n".join(t for _, t in all_text(out))
    hs = D["population"]["topic"] + D["population"]["comparison"]
    check(not any(h in blob for h in hs), "no account hash in outputs")
    check(SALT not in blob and "topicacct" not in blob and "compacct" not in blob, "no salt / account name in outputs")
    check(not re.search(r"\bE\d+\b", blob), "no per-account labels or rows published")
    check('"<3"' in open(os.path.join(out, "results.json")).read(), "small cells written <3")
    # privacy gate catches a planted leak
    bad = os.path.join(tmp, "bad"); shutil.copytree(out, bad)
    open(os.path.join(bad, "cards.md"), "a").write(f"\nleak {hs[0]} revision 1234567890\n")
    check(len(AT.scan(bad)) >= 2, "privacy gate catches a hash and a revid")
    # null world
    D0 = synth(seed=8, plant=False)
    R0 = AT.analyze(D0, B=300, P=300)
    V0 = R0["verdicts"]
    for k in ("topic_concentration", "direction_consistency", "reinsertion", "single_purpose"):
        check(V0[k].startswith("not distinguishable"), f"null {k}: {V0[k][:90]}")


def main():
    tmp = tempfile.mkdtemp()
    try:
        test_collector(tmp)
        test_analysis(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"\n{len(FAILS)} failure(s)")
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
