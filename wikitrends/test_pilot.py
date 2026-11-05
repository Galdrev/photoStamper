"""Offline test for pilot.py: a fake Wikipedia behind wt_net.get_json / post_json (no network).

  python test_pilot.py        -> runs the whole pilot on the real sample against mocked responses; exits non-zero on failure
Covers: missing pages, redirects resolving to the same page (dedupe), no talk page, no Wikidata item, no revisions since
2021, hidden revisions, pageviews 404, abuse-log permission error, LiftWing failure, protection/move history, RfC archives,
continuation, and the >5% error rule. Also checks that no raw username reaches the output files.
"""
import hashlib, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("WT_SALT", "test-salt")
os.environ["WT_JOB"] = "pilot-test"
import wt_net   # noqa: E402

USERS = ["Alice", "Bob Editor", "SockMaster9", "NewbieX", "OldHand", "192.0.2.1", "~2025-12345-67", "CleanupBot"]
REAL_USERS = [u for u in USERS if not re.match(r"^\d|^~", u)]
MISSING = {"Masalit massacres", "El Geneina massacre", "Kosovo Serbs"}
REDIRECT = {"Al-Aqsa": "Al-Aqsa Mosque", "Bosnian genocide": "Uyghur genocide", "Yazidi genocide": "Genocide of Yazidis by the Islamic State",
            "Jewish exodus from Arab and Muslim countries": "Jewish exodus from the Muslim world"}
NO_TALK = {"Shusha", "Hebrews"}
NO_QID = {"Shusha", "Tibet"}
NO_REVS = {"Plantation of Ulster"}
FAIL = set()                      # titles whose requests fail after retries (None)
WDATES = ["2021-01-01", "2023-07-01"]


def hsh(s):
    return int(hashlib.md5(s.encode()).hexdigest(), 16)


def canon(t):
    return REDIRECT.get(t, t)


def article_text(t, date):
    era = 0 if date < "2021-06" else (1 if date < "2023-10" else 2)
    crit = ["", " It has been described as apartheid.", " Scholars describe genocide and the Nakba; Palestinians were expelled in 1948."][era]
    jew = " The Farhud preceded the Jewish exodus from Arab countries." if era == 2 and hsh(t) % 2 else ""
    sd = ["Region in the Middle East", "Region in West Asia", "Contested region in West Asia"][era]
    cats = ["[[Category:Foo]]", "[[Category:Foo]][[Category:Bar|x]]", "[[Category:Bar]][[Category:Disputed territories]]"][era]
    return (f"{{{{Short description|{sd}}}}}\n{{{{pp-extended|small=yes}}}}\n{{{{About|the region|other uses|{t} (disambiguation)}}}}\n"
            f"{{{{Infobox country\n| name = {t}\n| image = Flag_{era}.svg\n| caption = Caption {era} with [[Jerusalem|link]]\n"
            f"| capital = [[Jerusalem]]\n| population = {1000 + era}\n}}}}\n"
            f"'''{t}''' is a place in the [[Middle East]].{crit}{jew}<ref>{{{{cite web|url=https://www.hrw.org/x|title=a}}}}</ref>"
            f"<ref>{{{{cite book|title=b|isbn=123}}}}</ref> More text{{{{citation needed|date=May 2024}}}}.\n\n"
            f"[[File:Map {era}.png|thumb|upright=1.2|A map, era {era}]]\n"
            f"== History ==\nLong history of [[Canaan]] and [[{'Nakba' if era == 2 else 'Ottoman Empire'}]].{{{{POV section|date=2024}}}}"
            f"<ref>https://www.timesofisrael.com/y</ref>\n"
            f"== See also ==\n* [[Zionism]]\n* [[{'Settler colonialism' if era else 'Colonialism'}]]\n"
            f"== References ==\n{{{{Reflist}}}}\n{{{{Israeli–Palestinian conflict}}}}\n{{{{Authority control}}}}\n{cats}\n")


def talk_text(t, date):
    era = 0 if date < "2021-06" else (1 if date < "2023-10" else 2)
    ct = "{{Contentious topics/talk notice|topic=a-i}}\n" if era >= 1 else ""
    return (f"{ct}{{{{WikiProject banner shell|class={['C', 'B', 'GA'][era]}|\n{{{{WikiProject Israel|importance=top}}}}\n"
            f"{{{{WikiProject Palestine|importance=High}}}}}}}}\n"
            f"{{{{Article history|action1=GAN|action1date=2022-03-01|action1result=listed|currentstatus=GA|dykdate=5 May 2022|itndate=8 October 2023}}}}\n"
            f"{{{{Press|org=The Guardian|date=1 Jan 2024|title=x|org2=Haaretz|date2=2 Feb 2024}}}}\n{{{{Top 25 Report|Oct 8 2023|Oct 15 2023}}}}\n"
            f"{{{{Old moves|title1=Old name|date1=1 June 2024|result1=moved|title2=Older|date2=2 July 2022|result2=not moved}}}}\n"
            f"{{{{Old AfD multi|page={t}|date=2022|result='''keep'''}}}}\n{{{{FAQ}}}}\n"
            f"== RfC on the first sentence ==\n{{{{rfc|pol|rfcid=ABC}}}}\nShould we? [[User:Alice|Alice]] 10:00, 3 March 2024 (UTC)\n"
            f"== Requested move 5 June 2024 ==\n{{{{requested move/dated|New}}}}\nThe result of the move request was: '''moved'''. "
            f"[[User:Bob Editor|Bob]] 11:11, 5 June 2024 (UTC)\n"
            f"== Unrelated ==\nchat {{{{ping|SockMaster9}}}} 09:00, 1 January 2025 (UTC)\n")


def archive_text(i):
    return (f"== RfC: wording {i} ==\n{{{{closed rfc top|result=done}}}}\nText. 12:00, {i + 1} February 2022 (UTC)\n{{{{closed rfc bottom}}}}\n"
            f"== Request for comment on lead ==\nx 13:00, {i + 1} November 2023 (UTC)\n"
            f"== Requested move 1 Jan 2024 ==\nThe result of the move request was: '''not moved'''. 14:00, 1 January 2024 (UTC)\n")


def revisions(t, start, end, n=130):
    out = []
    for i in range(n):
        y = 2021 + i * 5 // n
        ts = f"{y}-{(i % 12) + 1:02d}-{(i % 27) + 1:02d}T{i % 24:02d}:00:00Z"
        if not (start <= ts and (end is None or ts < end)):
            continue
        u = USERS[(hsh(t) + i) % len(USERS)]
        r = {"revid": 1000 + i, "parentid": 0 if (i == 0 and hsh(t) % 3 == 0) else 999 + i, "timestamp": ts, "user": u,
             "size": 5000 + 37 * i - (3000 if i % 17 == 0 else 0), "minor": i % 5 == 0, "sha1": "x",
             "comment": ["rv sock per WP:BANREVERT", "per talk consensus, see WP:ONUS", "added sources", "", "/* History */",
                         "rm undue weight, WP:NPOV", "ECR: reverted non-EC edit (WP:ARBECR)",
                         f"Alice moved page [[Old {t}]] to [[{t}]]: per requested move"][i % 8],
             "tags": [["mw-reverted"], ["mw-undo"], ["mobile edit", "mobile web edit"], ["visualeditor"], [], ["mw-rollback"], [], []][i % 8]}
        if i % 23 == 0:
            r.pop("user"); r["userhidden"] = True
        out.append(r)
    return sorted(out, key=lambda r: r["timestamp"])


def page_list(items, params, key, size):
    off = int(params.get("rvcontinue") or params.get("cont") or 0)
    chunk = items[off:off + size]
    j = {"query": {"pages": [{"title": params.get("titles"), key: chunk}]}}
    if off + size < len(items):
        j["continue"] = {"rvcontinue": str(off + size), "continue": "||"}
    return j


def mock_get(url, params, tries=8, ok404=False):
    p = dict(params)
    t = p.get("titles") or p.get("aftitle") or p.get("letitle") or ""
    base = re.sub(r"^Talk:", "", t)
    if any(f in (t, base) for f in FAIL):
        return None
    if "rest_v1/metrics/pageviews" in url:
        title = url.split("/user/")[1].split("/monthly")[0]
        if hsh(title) % 4 == 0:
            return None                                         # 404 / no data
        acc = "desktop" if "/desktop/" in url else "all"
        return {"items": [{"timestamp": f"{y}{m:02d}0100", "views": (1000 if acc == "all" else 400) + y}
                          for y in range(2021, 2027) for m in range(1, 13) if f"{y}{m:02d}" <= "202610"]}
    if "wikidata.org" in url:
        q = p["titles"]
        d = p.get("rvstart", "")[:10]
        era = 0 if d < "2021-06" else (1 if d < "2023-10" else 2)
        ent = {"labels": {"en": {"value": f"L{q}"}, "he": {"value": "ישראל"}, "ar": {"value": "إسرائيل"}},
               "descriptions": {"en": {"value": ["country in the Middle East", "country in West Asia", "state in West Asia"][era]},
                                "ar": {"value": "دولة"}},
               "aliases": {"en": [{"value": f"A{i}"} for i in range(era + 1)]}, "sitelinks": {"enwiki": {}, "dewiki": {}},
               "claims": {"P31": [{"mainsnak": {"datavalue": {"value": {"id": "Q6256"}}}}]}}
        return {"query": {"pages": [{"title": q, "revisions": [{"revid": 5 + era, "timestamp": d + "T00:00:00Z",
                                                                "slots": {"main": {"content": json.dumps(ent)}}}]}]}}
    a = p.get("action"); prop = p.get("prop", ""); lst = p.get("list", "")
    if a == "query" and "pageassessments" in prop:
        if t in MISSING:
            return {"query": {"pages": [{"title": t, "missing": True}]}}
        c = canon(t)
        page = {"title": c, "pageid": hsh(c) % 10 ** 6, "length": 12345, "watchers": 300 if hsh(c) % 2 else None,
                "protection": [{"type": "edit", "level": "extendedconfirmed", "expiry": "infinity"}],
                "description": "Region", "descriptionsource": "local" if hsh(c) % 3 else "central", "pageimage": "Flag.svg",
                "pageassessments": {"Israel": {"class": "B", "importance": "Top"}},
                "pageprops": {} if c in NO_QID else {"wikibase_item": f"Q{hsh(c) % 1000}"},
                "redirects": [{"title": f"{c} (alt {i})"} for i in range(3)]}
        if c not in NO_TALK:
            page["talkid"] = 1
        if page["watchers"] is None:
            page.pop("watchers")
        j = {"query": {"pages": [page]}}
        if t in REDIRECT:
            j["query"]["redirects"] = [{"from": t, "to": c}]
        if hsh(c) % 5 == 0 and not p.get("rdcontinue"):          # continuation of the redirects list
            j["continue"] = {"rdcontinue": "1", "continue": "||"}
        if p.get("rdcontinue"):
            page["redirects"] = [{"title": f"{c} (alt more)"}]
        return j
    if a == "query" and prop == "revisions" and p.get("rvlimit") == 1:
        d = p["rvstart"][:10]
        if base in NO_REVS and d == "2021-01-01":
            return {"query": {"pages": [{"title": t, "revisions": []}]}}
        if t.startswith("Talk:"):
            return {"query": {"pages": [{"title": t, "revisions": [{"revid": 77, "timestamp": d + "T00:00:00Z",
                                                                    "slots": {"main": {"content": talk_text(base, d)}}}]}]}}
        if d == "2023-07-01" and hsh(t) % 7 == 0:                   # hidden revision text
            return {"query": {"pages": [{"title": t, "revisions": [{"revid": 88, "timestamp": d + "T00:00:00Z",
                                                                    "slots": {"main": {"texthidden": True}}}]}]}}
        return {"query": {"pages": [{"title": t, "revisions": [{"revid": hash(d) % 10 ** 6, "timestamp": d + "T00:00:00Z",
                                                                "slots": {"main": {"content": article_text(t, d)}}}]}]}}
    if a == "query" and prop == "revisions" and p.get("rvsection") == 0:
        revs = [] if base in NO_REVS else revisions(t, p["rvstart"], p.get("rvend"), 90)
        for i, r in enumerate(revs):
            d = r["timestamp"][:7]
            r["slots"] = {"main": {"content": article_text(t, d + "-01").split("== History")[0]}} if i % 19 else {"main": {"texthidden": True}}
        return page_list(revs, p, "revisions", 50)
    if a == "query" and prop == "revisions" and "content" in p.get("rvprop", "") and "|" in t or (a == "query" and prop == "revisions" and "/Archive" in t):
        return {"query": {"pages": [{"title": x, "revisions": [{"slots": {"main": {"content": archive_text(i)}}}]}
                                    for i, x in enumerate(t.split("|"))]}}
    if a == "query" and prop == "revisions":
        revs = [] if base in NO_REVS else revisions(t, p["rvstart"], None)
        if t.startswith("Talk:"):
            revs = [{k: r.get(k) for k in ("timestamp", "user", "size") if k in r} for r in revs[::2]]
        return page_list(revs, p, "revisions", 50)
    if lst == "users":
        out = []
        for n in p["ususers"].split("|"):
            if n == "OldHand":
                out.append({"name": n, "missing": True}); continue
            u = {"name": n, "editcount": {"Alice": 40000, "Bob Editor": 600, "SockMaster9": 520, "NewbieX": 12}.get(n, 1),
                 "registration": {"NewbieX": "2024-01-01T00:00:00Z", "SockMaster9": "2023-09-01T00:00:00Z"}.get(n, "2010-01-01T00:00:00Z"),
                 "groups": ["*", "user", "extendedconfirmed"] if n in ("Alice", "Bob Editor", "SockMaster9") else ["*", "user"]}
            if n == "SockMaster9":
                u.update({"blockid": 1, "blockexpiry": "infinite"})
            out.append(u)
        return {"query": {"users": out}}
    if lst == "logevents":
        return {"query": {"logevents": [
            {"timestamp": "2020-05-01T00:00:00Z", "action": "protect", "user": "Alice",
             "params": {"details": [{"type": "edit", "level": "autoconfirmed", "expiry": "2022-01-01T00:00:00Z"}]}},
            {"timestamp": "2023-10-08T00:00:00Z", "action": "protect", "user": "Bob Editor",
             "params": {"details": [{"type": "edit", "level": "extendedconfirmed", "expiry": "infinite"},
                                    {"type": "move", "level": "sysop", "expiry": "infinite"}]}}]}}
    if lst == "abuselog":
        if hsh(t) % 2:
            return {"error": {"code": "permissiondenied", "info": "no"}}
        return {"query": {"abuselog": [{"timestamp": "2024-01-0%dT00:00:00Z" % (i + 1), "filter": "ECR enforcement", "user": "NewbieX",
                                        "result": "disallow"} for i in range(3)]}}
    if lst == "search":
        return {"query": {"searchinfo": {"totalhits": hsh(t + p["srsearch"]) % 5000}, "search": []}}
    if lst == "allpages":
        return {"query": {"allpages": [{"title": f"Wikipedia:{p['apprefix']}"}, {"title": f"Wikipedia:{p['apprefix']} (2nd nomination)"},
                                       {"title": f"Wikipedia:{p['apprefix']}ism"}]}}
    if p.get("generator") == "allpages":
        pre = p["gapprefix"]
        return {"query": {"pages": [{"pageid": i, "title": f"Talk:{pre}Archive {i}", "length": 100000,
                                     "revisions": [{"timestamp": f"{2019 + i}-03-01T00:00:00Z"}]} for i in range(1, 8)] +
                          [{"pageid": 99, "title": f"Talk:{pre}FAQ", "length": 2000}]}}
    raise AssertionError(f"unmocked request: {url} {p}")


def t0_heat(d):
    z = next(r for r in d["articles"] if r["title"] == "Zionism")
    return z["at"]["2021-01-01"]["talk"]["heat_notices"]


def mock_post(url, body, tries=4):
    if body["rev_id"] % 11 == 0:
        return None
    return {"output": {"prediction": False, "probabilities": {"true": (body["rev_id"] % 100) / 100, "false": 0.5}}}


def run(tmp, fail=()):
    import importlib
    import pilot
    importlib.reload(pilot)
    FAIL.clear(); FAIL.update(fail)
    wt_net.get_json = mock_get; wt_net.post_json = mock_post
    wt_net._wait_slot = lambda: None
    wt_net.STATUS_DIR = os.path.join(tmp, "status")
    pilot.OUT = os.path.join(tmp, "pilot")
    pilot._ucache.clear()
    pilot.LW_ON[0] = True; pilot._lw_fail[:] = [0, 0]
    return pilot, pilot.run(pilot.build_sample())


def main():
    ok = True
    def check(cond, msg):
        nonlocal ok
        print(("PASS " if cond else "FAIL ") + msg); ok &= bool(cond)
    tmp = tempfile.mkdtemp()
    try:
        pilot, s = run(tmp)
        out = os.path.join(tmp, "pilot")
        d = json.load(open(os.path.join(out, "pilot.json")))
        recs = {r["title"]: r for r in d["articles"]}
        check(s["n_errors"] == 0, f"no article errors ({s['n_errors']})")
        check(s["n_sample"] == 168, f"sample size 168 ({s['n_sample']})")
        check(set(s["missing_titles"]) == MISSING, f"missing pages recorded: {s['missing_titles']}")
        samp = [r["title"] for r in pilot.build_sample() if r["title"] not in MISSING]
        exp = len(samp) - len({canon(x) for x in samp})
        check(len(s["duplicates_dropped"]) == exp and len({r.get("canonical") for r in d["articles"] if not r.get("missing")}) ==
              sum(1 for r in d["articles"] if not r.get("missing")), f"redirect duplicates dropped: expected {exp}, got {s['duplicates_dropped']}")
        check("faq" in t0_heat(d), "FAQ recorded as talk heat notice, not as contentious topic")
        z = recs["Zionism"]
        a0, a2 = z["at"]["2021-01-01"]["article"], z["at"]["now"]["article"]
        check(a0["short_desc"] == "Region in the Middle East" and a2["short_desc"] == "Contested region in West Asia", "short description at dates")
        check(a2["infobox"]["type"] == "infobox country" and a2["infobox"]["caption"].startswith("Caption 2"), "infobox type + caption")
        check(a2["lead_image"]["file"] == "Flag 2.svg", f"lead image {a2['lead_image']}")
        check(a2["categories"] == ["Bar", "Disputed territories"] and a0["categories"] == ["Foo"], "categories at dates")
        check("israeli–palestinian conflict" in a2["navboxes"] and "authority control" not in a2["navboxes"], f"navboxes {a2['navboxes']}")
        check("Nakba" in a2["watch_links"] and "Nakba" not in a0["watch_links"], "watch links diffusion")
        check(a2["see_also"] == ["Settler colonialism", "Zionism"], f"see also {a2['see_also']}")
        check(a2["maint"].get("citation needed") == 1 and a2["dispute_tag"], "maintenance + dispute tags")
        check(a2["lead_refs"].get("Rights orgs & UN") == 1 and a2["refs"].get("Israeli press") == 1, f"lead refs {a2['lead_refs']}")
        check(a2["lex_lead"]["disp_P"] >= 1 and a0["lex_lead"]["disp_P"] == 0, f"P displacement split {a2['lex_lead']}")
        t2, t0 = z["at"]["now"]["talk"], z["at"]["2021-01-01"]["talk"]
        check(t2["ct_notice"] and not t0["ct_notice"] and t2["ct"][0]["topic"] == "a-i", "contentious-topic notice at dates")
        check(t2["class"] == "ga" and t0["class"] == "c" and t2["projects"].get("israel") == "top", f"class/projects {t2['class']} {t2['projects']}")
        check(t2["article_history"]["status"] == "GA" and t2["article_history"]["itn"], "article history")
        check(t2["n_press"] == 2 and t2["top25"] == 2 and t2["old_moves"] == 2 and t2["afd"][0]["result"] == "'''keep'''", f"press/top25/moves/afd {t2['n_press']} {t2['top25']} {t2['old_moves']} {t2['afd']}")
        check(t2["rfc_headings"] == 1 and t2["rm_headings"] == 1, "rfc/rm headings")
        di = z["discussions"]
        check(di and di["w1"]["rfc"] >= 1 and di["w1"]["rfc_closed"] >= 1 and di["w2"]["rm_moved"] == 1 and di["w2"]["rm_not_moved"] >= 1,
              f"RfC/RM scan {di}")
        pr = z["at"]
        check(pr["2021-01-01"]["protection"] == {"edit": "autoconfirmed"} and pr["2023-07-01"]["protection"] == {}
              and pr["now"]["protection"] == {"edit": "extendedconfirmed", "move": "sysop"}, f"protection at dates {[pr[k]['protection'] for k in pr]}")
        check(z["moves"] and pr["2021-01-01"]["title"] == "Old Zionism", f"title at 2021 {pr['2021-01-01']['title']}")
        w2 = z["win"]["w2"]
        check(w2["cmt_sock_ban"] > 0 and w2["cmt_ecr_arbpia"] > 0 and w2["hidden"] > 0 and w2["mobile"] > 0, "summary classes, hidden, mobile")
        acc = w2["accounts"]
        check(acc["n_edits"] > 0 and 0 < acc["share_indef_now"] < 1 and acc["share_age_lt30"] is not None, f"account aggregates {acc}")
        te = z["term_events"]
        ins = te["by_window"]["w2"]["critical_insert"]
        check(ins["n"] > 0 and ins["acct_n"] >= 0, f"lead term events {ins}")
        check(any(e["lw"] is not None for e in te["events"]), "LiftWing scores on events")
        check(z["now"]["afd"] == ["Zionism", "Zionism (2nd nomination)"], f"AfD pages {z['now']['afd']}")
        check(z["now"]["talk_archives"]["n"] == 7 and "_pages" not in z["now"]["talk_archives"], "talk archives")
        check(z["at"]["now"]["wikidata"]["descriptions"]["en"] == "state in West Asia", "wikidata description now")
        sh = recs["Shusha"]
        check(sh["at"]["now"]["talk"] is None and sh["at"]["now"]["wikidata"] is None and sh["discussions"] is None, "no talk / no qid")
        pl = recs["Plantation of Ulster"]
        check(pl["at"]["2021-01-01"]["article"] is None and pl["win"]["w1"].get("edits", 0) == 0, "no revisions since 2021")
        check(any(r["pageviews"]["all-access"] is None for r in d["articles"] if not r.get("missing")), "pageviews 404 tolerated")
        check(any(r["win"]["w2"]["abuselog"] is None for r in d["articles"] if not r.get("missing")) and s["failed_signals"].get("abuselog"),
              "abuse-log permission error recorded as missing signal")
        check(any(r["at"]["2023-07-01"]["rev"] and r["at"]["2023-07-01"]["rev"].get("hidden") for r in d["articles"] if not r.get("missing")),
              "hidden snapshot text tolerated")
        raw = open(os.path.join(out, "pilot.json")).read() + open(os.path.join(out, "summary.json")).read()
        leaked = [u for u in REAL_USERS if re.search(r'"%s"' % re.escape(u), raw) or ("User:" + u) in raw]
        check(not leaked, f"no raw usernames in outputs (leaked: {leaked})")
        check(len(s["screen"]) > 50 and any(r.get("p_perm") is not None for r in s["screen"]), f"screen rows {len(s['screen'])}")
        check(s["coverage"]["short_desc@now"] > 0.9, f"coverage {s['coverage']['short_desc@now']}")
        # resume: a second run reuses the checkpoint and does no new article work
        n_req = wt_net.C["requests"]
        _, s2 = run(tmp)
        check(s2["n_done"] == s["n_done"], "resume from checkpoint")
        # loud failure: 3 failing articles (<5%) -> ok; 12 failing -> SystemExit
        shutil.rmtree(os.path.join(tmp, "pilot"))
        _, s3 = run(tmp, fail={"Kosovo", "Shusha", "Tibet"})
        check(s3["n_errors"] == 3, f"3 errors tolerated ({s3['n_errors']})")
        shutil.rmtree(os.path.join(tmp, "pilot"))
        try:
            run(tmp, fail=set(sum((v["articles"] for v in __import__("corpus").NARRATIVE_DISPUTES.values()), [])))
            check(False, ">5% errors must exit non-zero")
        except SystemExit as e:
            check(bool(e.code), f">5% errors exit non-zero: {e.code}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("ALL PASS" if ok else "SOME CHECKS FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
