"""Offline tests for guard.py and analyze_guard.py (no network: a fake Wikipedia behind wt_net.get_json).

  python test_guard.py           -> exits non-zero on any failed check
Collector: scope matching, paged histories with usernames hashed at once and undo / restore references turned into
history positions (no raw comments kept), talk-page RfC / RM / AfD !vote parsing with hashed signatures, lead critical
counts via rvsection=0, ArbCom redaction (User: links, {{userlinks}}, {{u}}, {{admin}}, party lists; headings with an
unlinked name withheld), and no username or salt anywhere in the raw files.
Analysis (synthetic, planted): a small guard group reverts critical-term REMOVALS fast on topic articles and tag-teams
toward the same version across articles; a planted voting bloc; the guards are also the planted coord bloc (coord edges
recomputed from test_coord.synthetic with the same hashing). Checks: Q1 finds removals reverted faster and more
concentrated than additions (topic) and not in comparison; Q2 finds recurrent pairs above the article-month shuffle in
topic only; Q3 finds the bloc and few / no blocs in comparison; Q4 overlap above matched random sets; a no-plant world
gives no Q1-Q3 signal; outputs pass analyze_coord.privacy_scan and carry no hash, username or salt; small cells are <3.
"""
import glob, gzip, json, os, re, shutil, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SALT = "guard-test-salt-91c2"
os.environ["WT_SALT"] = SALT
os.environ["WT_JOB"] = "guard-test"
import numpy as np        # noqa: E402
import wt_net             # noqa: E402
import coord as CO        # noqa: E402
import analyze as A       # noqa: E402
import analyze_guard as AG  # noqa: E402
import guard as G         # noqa: E402

FAILS = []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg, flush=True)
    if not cond:
        FAILS.append(msg)


def ts(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))


# ------------------------------------------------------------------ fake wiki for the collector
NAMES = ["Alicewriter", "Bobguard", "Carolrv", "Dave Q", "203.0.113.9", "ClueBot NG"]
LEADS = {"Israel": ["Israel is a country.", "Israel is a country under occupation accused of apartheid."],
         "Ireland": ["Ireland is an island.", "Ireland is an island with a history of occupation."]}
HIST = {}
REVTEXT = {}


def build_fake():
    HIST.clear(); REVTEXT.clear()
    rid = 2000000
    for title in ("Israel", "Ireland", "Hamas", "Ukraine"):
        revs = []
        t = 1640995200          # 2022-01-01
        texts = LEADS.get(title, [f"{title} is a thing.", f"{title} is a thing linked to genocide claims."])
        seq = [(0, 0, ""), (1, 1, "add"), (2, 0, "remove crit"), (3, 1, None), (4, 0, "c/e"), (5, 1, ""), (2, 0, "")]
        for k, (ui, st, cm) in enumerate(seq):
            rid += 1
            comment = cm or ""
            if k == 3:
                comment = f"Undid revision {rid - 1} by [[Special:Contributions/{NAMES[2]}|{NAMES[2]}]] ([[User talk:{NAMES[2]}|talk]])"
            sha = f"{st:040x}" if k != 3 else "a" * 40      # the undo is not an identity revert
            revs.append({"revid": rid, "timestamp": ts(t), "user": NAMES[ui], "comment": comment, "size": 1000 + st,
                         "sha1": sha, "tags": ["mw-undo"] if k == 3 else []})
            REVTEXT[rid] = texts[st] + "\n\n== History ==\nBody text."
            t += 3600 * (k + 1)
        revs.append({"revid": rid + 1, "timestamp": ts(t + 99), "userhidden": True, "comment": "", "size": 5, "sha1": "e" * 40, "tags": []})
        REVTEXT[rid + 1] = texts[0]
        rid += 1
        HIST[title] = revs


TALK = {"Talk:Israel": """== Requested move 3 May 2023 ==
{{requested move/dated|Israel (state)}}
* '''Support''' per nom. [[User:Alicewriter|Alicewriter]] ([[User talk:Alicewriter|talk]]) 10:00, 3 May 2023 (UTC)
* '''Oppose''' no. [[User:Bobguard|Bob]] 11:00, 3 May 2023 (UTC)
*: '''Support''' reply that should not count [[User:Zed|Zed]] 11:30, 3 May 2023 (UTC)
* '''Strong oppose''' [[User:Carolrv|C]] ([[User talk:Carolrv|talk]]) 12:00, 3 May 2023 (UTC)
* '''Note''' this is not a vote [[User:Dave Q|D]] 12:10, 3 May 2023 (UTC)
== Other chat ==
* '''Support''' not a discussion we parse [[User:Alicewriter|A]] 13:00, 3 May 2023 (UTC)
{{Old AfD multi|page=Israel (2nd nomination)|result=keep}}
""",
        "Talk:Israel/Archive 1": """== RfC: lead wording ==
{{rfc|pol|rfcid=ABC}}
* '''Include''' [[User:Bobguard|B]] 09:00, 1 June 2022 (UTC)
* '''Exclude''' [[User:Carolrv|C]] 09:30, 1 June 2022 (UTC)
* '''Include''' {{unsigned|Dave Q}}
""",
        "Wikipedia:Articles for deletion/Israel (2nd nomination)": """* '''Keep''' obviously [[User:Alicewriter|A]] 01:00, 2 February 2020 (UTC)
* '''Delete''' [[User:Carolrv|C]] 02:00, 2 February 2020 (UTC)
* '''Speedy keep''' [[User:Bobguard|B]] 03:00, 2 February 2020 (UTC)
"""}

ARB_PAGES = {
    "Wikipedia:Arbitration/Requests/Case/Palestine-Israel_articles_5": """{{Casenav}}
=== Involved parties ===
*{{userlinks|Alicewriter}}
*{{admin|Bobguard}}
* Carolrv (filing party)
== Final decision ==
=== Principles ===
==== Canvassing ====
Canvassing is the practice of notifying editors off-wiki to influence discussion; it is disruptive.
=== Findings of fact ===
==== Off-wiki coordination ====
A group of editors used a private Discord server and an email list to coordinate edits, a pro-Palestinian group according to evidence presented by {{u|Dave Q}}. Huldra noted that [[User:Carolrv|Carolrv]] took part.
:Passed 9 to 0 at 21:03, 23 January 2025 (UTC)
==== Alicewriter ====
Alicewriter engaged in proxying for a banned editor through email.
:Passed 8 to 1 at 21:05, 23 January 2025 (UTC)
==== Zorbabuddy's conduct ====
Zorbabuddy canvassed via email on behalf of pro-Israel editors.
:Passed 7 to 2 at 21:06, 23 January 2025 (UTC)
==== Edit warring ====
Editors edit warred on many pages.
=== Remedies ===
==== Alicewriter topic banned ====
Alicewriter is topic banned from the Arab-Israeli conflict for off-wiki coordination via email.
:Passed 9 to 0 at 21:10, 23 January 2025 (UTC)
==== Off-wiki canvassing site ban ====
The editor engaged in off-wiki canvassing is site banned. See https://en.wikipedia.org/w/index.php?oldid=1234567890&diff=prev
:Passed 9 to 0 at 21:11, 23 January 2025 (UTC)
""",
    "Wikipedia:Arbitration/Requests/Case/Palestine-Israel_articles_5/Proposed_decision": """== Proposed findings of fact ==
=== Discord coordination ===
1) Editors coordinated on Discord, including [[User:Bobguard|Bobguard]].
:Support:
:# Per evidence. [[User:Arbone|Arbone]] ([[User talk:Arbone|talk]]) 10:00, 10 January 2025 (UTC)
""",
    "Wikipedia:Arbitration/Requests/Case/Palestine-Israel_articles_4": None,
    "Wikipedia:Arbitration/Requests/Case/Palestine-Israel_articles_5/Evidence": "== Evidence presented by Huldra ==\n[[User:Huldra|Huldra]] 10:00, 1 December 2024 (UTC)\n",
}


def mock_get(url, params, tries=8, ok404=False):
    p = params
    if p.get("prop") == "info":
        pages = []
        for t in p["titles"].split("|"):
            pages.append({"title": t, "missing": True} if t.startswith("Missing") else {"title": t, "length": 1000 + 37 * len(t)})
        return {"query": {"pages": pages}}
    if p.get("list") == "allpages":
        pre = p["apprefix"]
        return {"query": {"allpages": [{"title": t} for t in TALK if t.startswith("Talk:" + pre)]}}
    if p.get("prop") == "revisions" and "revids" in p:
        assert str(p.get("rvsection")) == "0"
        revs = []
        for r in str(p["revids"]).split("|"):
            txt = REVTEXT.get(int(r))
            revs.append({"revid": int(r), "slots": {"main": {"content": A.split_lead(txt)}}} if txt else {"revid": int(r), "slots": {"main": {"texthidden": True}}})
        return {"query": {"pages": [{"title": "x", "revisions": revs}]}}
    if p.get("prop") == "revisions" and p.get("rvlimit") == "max":
        t = p["titles"]
        revs = HIST.get(t, [])
        start = int(p.get("rvcontinue", 0))
        chunk = revs[start:start + 3]
        out = {"query": {"pages": [{"title": t, "revisions": chunk}]}}
        if start + 3 < len(revs):
            out["continue"] = {"rvcontinue": str(start + 3), "continue": "||"}
        return out
    if p.get("prop") == "revisions" and p.get("rvprop") == "content":
        pages = []
        for t in p["titles"].split("|"):
            if t in TALK:
                pages.append({"title": t, "revisions": [{"slots": {"main": {"content": TALK[t]}}}]})
            elif t in ARB_PAGES and ARB_PAGES[t]:
                pages.append({"title": t, "revisions": [{"slots": {"main": {"content": ARB_PAGES[t]}}}]})
            else:
                pages.append({"title": t, "missing": True})
        return {"query": {"pages": pages}}
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
    G.OUT = os.path.join(tmp, "guard"); os.makedirs(G.OUT, exist_ok=True)
    G.raw_page = lambda title: ARB_PAGES.get(title)
    plan = {"topic": [{"title": "Israel", "tier": "core"}, {"title": "Hamas", "tier": "High"}, {"title": "Missing page", "tier": "Top"}],
            "pool": [{"title": "Ireland", "tier": "core"}, {"title": "Ukraine", "tier": "High"}, {"title": "Ukraine2", "tier": "Top"}]}
    json.dump(plan, open(os.path.join(G.OUT, "plan.json"), "w"))
    G.collect()
    D = json.load(gzip.open(os.path.join(G.OUT, "raw.json.gz"), "rt"))
    arts = {a["title"]: a for a in D["articles"]}
    check(set(arts) == {"Israel", "Hamas", "Ireland", "Ukraine"}, f"scope: matched 2 topic + 2 comparison, missing topic dropped ({sorted(arts)})")
    check(arts["Israel"]["group"] == "topic" and arts["Ireland"]["group"] == "comparison", "groups kept")
    r = arts["Israel"]["revs"]
    check(len(r) == 8, "paged history complete (8 revisions over 3 pages)")
    check(r[3][6] == 2, "undo reference converted to a history position")
    check(r[0][2] == CO.h("Alicewriter") and r[7][2] is None and r[7][3] & AG.F_HIDDEN, "usernames hashed; hidden user kept as state")
    check(r[4][3] & AG.F_ANON and r[5][3] & AG.F_BOT, "IP and bot flagged")
    rv = AG.find_reverts(r)
    check(any(x["kind"] == "undo" for x in rv) and any(x["kind"] == "identity" for x in rv),
          f"reverts found: kinds {sorted({x['kind'] for x in rv})}")
    check(len(D["leads"]) > 0 and all(v in (0, 1, 2, 3, None) for v in D["leads"].values()), f"lead counts measured ({len(D['leads'])})")
    ds = [d for d in D["discussions"] if d["a"] == "Israel"]
    kinds = sorted(d["kind"] for d in ds)
    check(kinds == ["afd", "rfc", "rm"], f"RfC, RM and AfD discussions parsed ({kinds})")
    rm = [d for d in ds if d["kind"] == "rm"][0]
    check(len(rm["votes"]) == 3 and rm["ym"] == "2023-05", f"RM: 3 top-level !votes (reply and 'Note' skipped), month ({len(rm['votes'])}, {rm['ym']})")
    check(sorted(s for _, s in rm["votes"]) == ["neg", "neg", "pos"], "stances normalised")
    rfc = [d for d in ds if d["kind"] == "rfc"][0]
    check(len(rfc["votes"]) == 3, "unsigned template counts as a signature")
    afd = [d for d in ds if d["kind"] == "afd"][0]
    check(sorted(s for _, s in afd["votes"]) == ["neg", "pos", "pos"], "AfD keep / delete / speedy keep")
    ab = D["arbcom"]
    titles = [it["title"] for it in ab["items"]]
    check(ab["pages"]["PIA4 case"]["found"] is False and ab["pages"]["PIA5 case"]["found"], "missing ArbCom page recorded")
    check(any("Off-wiki coordination" == t for t in titles), f"finding title kept ({titles})")
    check(not any("Edit warring" in t for t in titles) and not any("Canvassing" == t for t in titles),
          "non-matching finding and principles excluded")
    check(any("withheld" in t for t in titles), "heading with an unlinked name withheld")
    check(any(it["kind"] == "remedy" and it["remedy_type"] == "topic ban" for it in ab["items"]) and
          any(it["remedy_type"] == "site ban" for it in ab["items"]), "remedy types classified")
    off = [it for it in ab["items"] if it["title"] == "Off-wiki coordination"][0]
    check(off["side"] == ["pro-Palestinian"] and off["date"] == "23 January 2025", f"side and date ({off['side']}, {off['date']})")
    check("Editor" in off["quote"], f"linked names redacted in quote: {off['quote'][:160]}")
    zq = [it["quote"] for it in ab["items"] if "pro-Israel" in it["side"]]
    check(zq and "[redacted]" in zq[0], f"unlinked name scrubbed from quote: {zq[:1]}")
    blob = json.dumps(ab)
    for n in ("Alicewriter", "Bobguard", "Carolrv", "Dave Q", "Huldra", "Zorbabuddy", "Arbone", "oldid", "1234567890"):
        check(n.lower() not in blob.lower(), f"ArbCom extract free of {n!r}")
    for f, txt in all_text(G.OUT):
        for n in ("Alicewriter", "Bobguard", "Carolrv", "Dave Q", "Huldra", SALT, "Special:Contributions"):
            check(n not in txt, f"{os.path.basename(f)}: no {n!r}")


# ------------------------------------------------------------------ synthetic world for the analysis
def synth(seed=5, plant=True, guards=None, n_art=36):
    rng = np.random.default_rng(seed)
    guards = guards or [CO.h(f"guard{k}") for k in range(5)]
    arts, leads, rid = [], {}, 10 ** 8
    t_start = 1609459200 + 86400 * 30            # 2021-01-31
    for g in ("topic", "comparison"):
        editors = [CO.h(f"{g}-ed{k}") for k in range(120)]
        for ai in range(n_art):
            revs, shas = [], {}
            crit = 3; sha = 0; t = t_start + rng.uniform(0, 86400 * 30)
            state_crit = {0: 3}
            nsha = [1]
            def add(u, new_sha, c, fl=0, undo=-1):
                nonlocal rid
                rid += 1
                revs.append([rid, int(t), u, fl, new_sha, 1000 + c, undo, -1])
                leads[str(rid)] = c
            add(rng.choice(editors), 0, 3)
            for step in range(120):
                t += rng.exponential(86400 * 1)
                u = rng.choice(editors); d = int(rng.choice([-1, 0, 1]))
                c2 = max(0, crit + d); s2 = nsha[0]; nsha[0] += 1
                add(u, s2, c2)
                prev_sha, prev_c = sha, crit
                sha, crit = s2, c2
                if rng.random() < 0.35:                      # this edit gets reverted
                    guarded = plant and g == "topic" and d < 0
                    if guarded:
                        ga, gb = rng.choice(len(guards), 2, replace=False)
                        t += rng.uniform(600, 3600); add(guards[ga], prev_sha, prev_c, AG.F_RVTAG)
                        if rng.random() < 0.6:               # the remover re-applies, a second guard reverts again
                            t += rng.uniform(600, 7200); add(u, s2, c2)
                            t += rng.uniform(600, 7200); add(guards[gb], prev_sha, prev_c, AG.F_RVTAG)
                    else:
                        t += rng.exponential(86400 * 2) + 600
                        rv = rng.choice(editors)
                        while rv == u:
                            rv = rng.choice(editors)
                        add(rv, prev_sha, prev_c, AG.F_RVTAG)
                    sha, crit = prev_sha, prev_c
            arts.append({"title": f"{g[0].upper()}{ai}", "group": g, "tier": "core", "revs": revs})
    discs = []
    for g in ("topic", "comparison"):
        voters = [CO.h(f"{g}-voter{k}") for k in range(70)]
        for k in range(40):
            vs = list(rng.choice(voters, size=int(rng.integers(8, 16)), replace=False))
            votes = [[v, "pos" if rng.random() < 0.5 else "neg"] for v in vs]
            if plant and g == "topic" and k < 18:
                st = "pos" if rng.random() < 0.5 else "neg"
                votes += [[gg, st] for gg in guards[:4]]
            discs.append({"a": f"{g[0].upper()}{k % n_art}", "group": g, "kind": "rfc" if k % 2 else "rm", "ym": "2024-01", "votes": votes})
    return {"summary": {"test": True}, "articles": arts, "discussions": discs, "leads": leads,
            "arbcom": {"pages": {}, "items": [], "editors_redacted": 0, "headings_withheld": 0, "redaction_leak_check": "passed"}}, guards


def coord_file(tmp, plant=True):
    """test_coord.synthetic with every account replaced by its salted hash; planted accounts = guard0..4."""
    import test_coord as TC
    D, pu, pa = TC.synthetic(planted=plant)
    m = {u: CO.h(f"guard{k}") for k, u in enumerate(pu)}
    for r in D["revisions"]:
        r["u"] = m.get(r["u"], CO.h(r["u"]))
    D["accounts"] = {m.get(k, CO.h(k)): v for k, v in D["accounts"].items()}
    D["summary"].update({"n_articles": 350, "n_articles_expected": 350})
    p = os.path.join(tmp, "coord.json.gz")
    json.dump(D, gzip.open(p, "wt"))
    return p


def test_analysis(tmp):
    cp = coord_file(tmp)
    ce, meta = AG.coord_edges(cp, log=lambda *a: None, n_null=300)
    guards = [CO.h(f"guard{k}") for k in range(5)]
    gset = set(guards)
    check(meta["available"] and sum(1 for e in ce if set(e) <= gset) >= 5, f"coord edges recomputed with the same hashing: "
          f"{meta['edges']} edges, {sum(1 for e in ce if set(e) <= gset)} among the planted accounts")
    D, _ = synth(plant=True)
    R = AG.analyze(D, cp, B=200, P=200, n_vote=300, K=40, log=lambda *a: None)
    q1 = R["q1_revert_guarding"]
    rt = q1["removal_vs_addition"]["topic"]; rc = q1["removal_vs_addition"]["comparison"]
    check(rt["median_h"]["difference"] < 0 and rt["median_h"]["p_direction_permutation"] < 0.01,
          f"Q1: topic removals reverted faster ({rt['median_h']['reverts_of_removals']} h vs {rt['median_h']['reverts_of_additions']} h, p {rt['median_h']['p_direction_permutation']})")
    check(rt["top10"]["difference"] > 0 and rt["top10"]["p_direction_permutation"] < 0.01,
          f"Q1: topic removals reverted by fewer accounts (top-10 {rt['top10']['reverts_of_removals']} vs {rt['top10']['reverts_of_additions']})")
    check(rc["median_h"]["p_direction_permutation"] > 0.01, f"Q1: no direction effect in comparison (p {rc['median_h']['p_direction_permutation']})")
    check(q1["removal_vs_addition"]["topic_minus_comparison"]["median_h"]["ci95"][1] < 0, "Q1: difference in differences CI below 0")
    check("p_label_permutation" in q1["all_history"]["median_h"], "Q1: topic vs comparison test ran")
    q2 = R["q2_tag_team"]["W24h"]
    t3, c3 = q2["recurrence_topic"]["significant_recurrent_pairs"], q2["recurrence_comparison"]["significant_recurrent_pairs"]
    check(t3["observed"] >= 5 and t3["observed"] > t3["expected_p95"], f"Q2: recurrent tag-team pairs in topic ({t3})")
    check(c3["observed"] <= max(1, c3["expected_p95"]), f"Q2: none beyond chance in comparison ({c3})")
    check(q2["per_article"]["topic"] > q2["per_article"]["comparison"], "Q2: more sequences per topic article")
    q3 = R["q3_voting_blocs"]
    check(q3["topic"]["blocs"]["count"] >= 1 and 4 in q3["topic"]["blocs"]["sizes"] or any(s >= 4 for s in q3["topic"]["blocs"]["sizes"]),
          f"Q3: planted bloc found (sizes {q3['topic']['blocs']['sizes']}, chance {q3['topic']['blocs']['expected_by_chance_mean']})")
    check(q3["topic"]["significant_agreement_pairs"]["observed"] > q3["topic"]["significant_agreement_pairs"]["expected_p95"], "Q3: pairs above calibration")
    check(q3["comparison"]["blocs"]["count"] <= max(1, q3["comparison"]["blocs"]["expected_p95"]), f"Q3: comparison blocs at chance ({q3['comparison']['blocs']})")
    ov = q3["overlap_with_coord_edges"]
    check(ov["coord_accounts_in_voting_blocs"] in (4, "<3") or isinstance(ov["coord_accounts_in_voting_blocs"], int),
          f"Q3: coord overlap reported ({ov})")
    q4 = R["q4_overlap"]["remove"]
    check(isinstance(q4.get("coord_edge_accounts"), dict) and q4["coord_edge_accounts"]["p_upper"] < 0.05,
          f"Q4: fast removal reverters overlap coord accounts beyond chance ({q4.get('coord_edge_accounts')})")
    check("supports" in R["verdicts"]["q1"] and "supports" in R["verdicts"]["q2"] and "supports" in R["verdicts"]["q3"],
          f"verdicts on the planted world: {R['verdicts']}")
    out = os.path.join(tmp, "out")
    AG.write_outputs(R, out)
    bad = AG.scan(out)
    check(not bad, f"privacy gate passes on outputs ({bad[:3]})")
    txt = "".join(t for _, t in all_text(out))
    check(not any(g in txt for g in guards) and SALT not in txt, "no account hash or salt in outputs")
    check(not re.search(r"[0-9a-f]{16}", txt), "no 16-hex strings in outputs")
    # gate catches leaks
    leak = os.path.join(tmp, "leak"); os.makedirs(leak)
    json.dump({"note": guards[0], "revid": 5}, open(os.path.join(leak, "x.json"), "w"))
    check(len(AG.scan(leak)) >= 2, "privacy gate fails on a planted hash and id key")
    # null world
    D0, _ = synth(seed=8, plant=False)
    R0 = AG.analyze(D0, coord_file(tmp, plant=False), B=100, P=200, n_vote=300, K=40, log=lambda *a: None)
    v = R0["verdicts"]
    check(not v["q1"].startswith("supports") and not v["q2"].startswith("supports") and not v["q3"].startswith("supports"),
          f"no-plant world: no 'supports' verdicts ({v})")
    check(AG.sup(2) == "<3" and AG.sup(0) == 0 and AG.sup(7) == 7, "small-cell suppression")


def main():
    tmp = tempfile.mkdtemp()
    try:
        test_collector(tmp)
        test_analysis(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"\n{len(FAILS)} failed" if FAILS else "\nall checks passed")
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
