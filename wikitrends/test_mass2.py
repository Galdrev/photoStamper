"""Offline test for mass2.py: a fake Wikipedia behind wt_net.get_json / post_json (no network), like test_pilot.py.

  python test_mass2.py      -> exits non-zero on any failed check
Covers: resolve + dedupe by resolved title (redirects, atrocity candidates), missing and disambiguation pages, empty page,
page created later, snapshot that was a redirect, no talk / no QID / no revisions since 2021, hidden snapshot text,
alias-resolved concept links across a rename, old-format protection log + move_prot + "now" anchored on page info,
pageviews over former titles without the partial month, RfC/RM per-discussion dates, restore tagging, checkpoint resume,
fail-loud above 5% errors, no usernames in any output, and lead-event coverage up to "now" on a heavy 2021-2026 history.
"""
import functools, glob, gzip, hashlib, json, os, re, shutil, sys, tempfile, threading

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("WT_SALT", "test-salt")
os.environ["WT_JOB"] = "mass2-test"
os.environ["WT_NOW"] = "2026-11-05"
os.environ.pop("WT_LIFTWING", None)
os.environ.pop("WT_LEAD_SCOPE", None)
import wt_net                      # noqa: E402
import test_pilot as TP            # noqa: E402  (text generators and fake users)

USERS = TP.USERS
REAL_USERS = TP.REAL_USERS
NOW = "2026-11-05T00:00:00Z"
TOPIC = ["Zionism", "Israel", "Nakba", "Palestine", "Palestinian state", "Gaza war", "Ghost page", "Gaza genocide", "West Bank",
         "Hebron", "Empty page"] + [f"Topic page {i}" for i in range(12)]
COMP = ["Darfur genocide", "Shusha", "Plantation of Ulster", "Kosovo", "Kashmir"] + [f"Comparison page {i}" for i in range(14)]
MISSING = {"Ghost page", "Masalit massacre", "El Geneina massacre", "El Geneina massacres", "2023 Masalit massacres",
           "2023 El Geneina massacre", "Massacres of Masalit", "Darfur genocide (2023–present)", "Darfur genocide (2023-present)",
           "Second Darfur genocide", "West Darfur massacres", "War crimes in the Sudanese civil war (2023–present)", "Tigray genocide"}
REDIRECT = {"Palestinian state": "Palestine", "Uyghur genocide": "Persecution of Uyghurs in China",
            "Yazidi genocide": "Genocide of Yazidis by the Islamic State", "Masalit massacres": "Masalit genocide",
            "Darfur genocide (2003-2005)": "Darfur genocide (2003–2005)",
            "Jewish exodus from the Muslim world": "Jewish exodus from Arab and Muslim countries"}
CONCEPT_REDIRECTS = {"1948 Palestinian expulsion and flight": ["1948 Palestinian exodus", "Palestinian exodus"],
                     "Israeli apartheid": ["Israel and the apartheid analogy", "Israel and apartheid"]}
DISAMBIG = {"Darfur genocide"}
NO_TALK = {"Hebron", "Shusha", "Empty page"}
NO_QID = {"Shusha", "Empty page"}
NO_REVS = {"Plantation of Ulster", "Empty page"}
CREATED_LATER = {"Gaza genocide"}
WAS_REDIRECT_2021 = {"West Bank"}
HIDDEN_2023 = {"Hebron"}
MOVED = {"Israel"}                    # one real RM move at mid-history: "Old Israel" -> "Israel"
VANDAL_MOVE = {"Zionism"}             # vandal move + revert pair
HEAVY = "Gaza war"
N_HEAVY = 3000
FAIL = set()
CALLS = {"n": 0}
REVMAP = {}
_lock = threading.Lock()
hsh = TP.hsh


def canon(t):
    return REDIRECT.get(t, t)


def ts_at(i, n, start="2021-01-02", end="2026-11-01"):
    from datetime import datetime, timezone
    a = datetime.fromisoformat(start).replace(tzinfo=timezone.utc).timestamp()
    b = datetime.fromisoformat(end).replace(tzinfo=timezone.utc).timestamp()
    return datetime.fromtimestamp(a + (b - a) * i / n, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def heavy_lead(i):
    """Heavy page: occupation from rev 500; genocide 2950..2989; identity revert to rev 2949 for 2990..2998; last rev
    removes occupation. Text varies every 10 revisions so sha1 repeats inside buckets."""
    if 2990 <= i < 2999:
        return heavy_lead(2949)
    occ = " The territories are under occupation." if 500 <= i < 2999 else ""
    gen = " It has been called a genocide." if 2950 <= i < 2990 else ""
    return f"'''Gaza war''' is a war.{occ}{gen} Version {i // 10}.\n"


def article_text(t, date, i=0):
    if t == HEAVY:
        return heavy_lead(i) + "== Background ==\nBody.\n"
    if t in WAS_REDIRECT_2021 and date < "2021-06":
        return "#REDIRECT [[Judea and Samaria]]"
    if t == "Empty page":
        return ""
    base = TP.article_text(t, date)
    era = 0 if date < "2021-06" else (1 if date < "2023-10" else 2)
    link = "[[1948 Palestinian exodus|the 1948 events]]" if era == 0 else "[[1948 Palestinian expulsion and flight|the 1948 events]]"
    return base.replace("is a place in the [[Middle East]].", f"is a place in the [[Middle East]]. See {link}.", 1) + f"<!-- v{i % 7} -->"


@functools.lru_cache(maxsize=None)
def rev_list(t):
    """All revisions of a page: [(revid, ts, user, text, tags, comment, parentid)], incl. one just before 2021."""
    base = (hsh(t) % 10 ** 5) * 10 ** 5
    out = []
    if t not in CREATED_LATER:
        out.append((base, "2020-12-31T12:00:00Z", "OldHand", article_text(t, "2020-12-31", 0), [], "old", 1))
    if t in NO_REVS:
        return out
    n = N_HEAVY if t == HEAVY else 60
    start = "2024-01-01" if t in CREATED_LATER else "2021-01-02"
    for i in range(n):
        ts = ts_at(i, n, start)
        u = USERS[(hsh(t) + i) % len(USERS)]
        cm = ["rv sock per WP:BANREVERT", "per talk consensus", "added sources", "", "/* History */", "rm undue, WP:NPOV",
              "ECR: reverted non-EC edit (WP:ARBECR)", "copyedit"][i % 8]
        tags = [["mw-reverted"], ["mw-undo"], ["mobile edit"], ["visualeditor"], [], ["mw-rollback"], [], []][i % 8]
        if t in MOVED and i == n // 2:
            cm = f"Alice moved page [[Old {t}]] to [[{t}]]: per [[Talk:{t}#Requested move 1 May 2024|requested move]]"
        if t in VANDAL_MOVE and i == 20:
            cm = f"SockMaster9 moved page [[{t}]] to [[Make {t} Great]]: lol"
        if t in VANDAL_MOVE and i == 21:
            cm = f"Alice moved page [[Make {t} Great]] to [[{t}]]: revert vandalism"
        if t == HEAVY and 2990 <= i < 2999:
            tags = ["mw-manual-revert"] if i == 2990 else []
        out.append((base + i + 1, ts, u, article_text(t, ts[:10], i), tags, cm, 0 if (i == 0 and t in CREATED_LATER) else base + i))
    with _lock:
        for r in out:
            REVMAP[r[0]] = (t, r)
    return out


def sha(text):
    return hashlib.sha1(text.encode()).hexdigest()


def section0(text):
    m = re.search(r"^=+[^=\n].*?=+[ \t]*$", text, re.M)
    return text[:m.start()] if m else text


def snapshot(t, date):
    revs = [r for r in rev_list(t) if r[1] <= date]
    return revs[-1] if revs else None


def page_list(items, params, size):
    off = int(params.get("rvcontinue") or 0)
    j = {"query": {"pages": [{"title": params.get("titles"), "revisions": items[off:off + size]}]}}
    if off + size < len(items):
        j["continue"] = {"rvcontinue": str(off + size), "continue": "||"}
    return j


def page_record(t, cont=False):
    if t in MISSING:
        return {"title": t, "missing": True}
    c = canon(t)
    if cont:
        return {"title": c, "pageid": hsh(c) % 10 ** 6}
    page = {"title": c, "pageid": hsh(c) % 10 ** 6, "length": 12345,
            "protection": [{"type": "edit", "level": "extendedconfirmed", "expiry": "infinity"}] if c != "Shusha" else [],
            "description": "Region", "descriptionsource": "local", "pageassessments": {"Israel": {"class": "B", "importance": "Top"}},
            "pageprops": {} if c in NO_QID else {"wikibase_item": f"Q{hsh(c) % 100000}"},
            "redirects": [{"title": x} for x in CONCEPT_REDIRECTS.get(c, [])] + [{"title": f"{c} (alt)"}]}
    if hsh(c) % 2:
        page["watchers"] = 120
    if c in DISAMBIG:
        page["pageprops"]["disambiguation"] = ""
    if c not in NO_TALK:
        page["talkid"] = 1
    return page


def logevents(t):
    if t == "Zionism":                                   # old format (no details) + modern entry
        return [{"timestamp": "2010-05-01T00:00:00Z", "action": "protect",
                 "params": {"description": "‎[edit=autoconfirmed] (indefinite)‎[move=sysop] (indefinite)"},
                 "comment": "Persistent vandalism by [[User:SockMaster9]]", "user": "Alice"},
                {"timestamp": "2023-10-08T00:00:00Z", "action": "protect", "user": "Bob Editor",
                 "params": {"details": [{"type": "edit", "level": "extendedconfirmed", "expiry": "infinite"},
                                        {"type": "move", "level": "sysop", "expiry": "infinite"}]}}]
    if t == "Old Israel":                                # protection filed under the former title
        return [{"timestamp": "2022-03-01T00:00:00Z", "action": "protect", "user": "Alice",
                 "params": {"details": [{"type": "edit", "level": "autoconfirmed", "expiry": "infinite"}]}}]
    if t == "Israel":
        mv = [r for r in rev_list("Israel") if "moved page" in r[5]][0]
        return [{"timestamp": mv[1], "action": "move_prot", "user": "Alice", "params": {"oldtitle_title": "Old Israel", "oldtitle_ns": 0}}]
    if t == "Kosovo":                                    # oldest format inside the comment, with an expiry
        return [{"timestamp": "2007-01-01T00:00:00Z", "action": "protect", "comment": "[edit=sysop:move=sysop]", "params": {}},
                {"timestamp": "2008-01-01T00:00:00Z", "action": "unprotect", "params": {}},
                {"timestamp": "2022-02-01T00:00:00Z", "action": "protect", "params": {
                    "description": "[edit=autoconfirmed] (expires 12:00, 1 January 2030 (UTC))"}}]
    return []


def wd_entity(q, era=2):
    return {"id": q, "labels": {"en": {"value": f"L{q}"}, "he": {"value": "ישראל"}},
            "descriptions": {"en": {"value": ["country in the Middle East", "country in West Asia", "state in West Asia"][era]}},
            "aliases": {"en": [{"value": f"A{i}"} for i in range(era + 1)]}, "sitelinks": {"enwiki": {}, "dewiki": {}},
            "claims": {"P31": [{"mainsnak": {"datavalue": {"value": {"id": "Q6256"}}}}]}}


def req_title(url, p):
    if "rest_v1/metrics/pageviews" in url:
        return requests_unquote(url.split("/user/")[1].split("/monthly")[0]).replace("_", " ")
    if p.get("revids"):
        rid = int(str(p["revids"]).split("|")[0])
        return REVMAP.get(rid, ("",))[0]
    return re.sub(r"^Talk:", "", p.get("titles") or p.get("letitle") or "")


def requests_unquote(s):
    import urllib.parse
    return urllib.parse.unquote(s)


def mock_get(url, params, tries=8, ok404=False):
    CALLS["n"] += 1
    p = dict(params)
    t = req_title(url, p)
    if FAIL and (t in FAIL or re.sub(r"^Old ", "", t) in FAIL):
        return None
    if "rest_v1/metrics/pageviews" in url:
        assert "/all-access/" in url and url.endswith("/2026100100"), url
        if hsh(t) % 5 == 0 and not t.startswith("Old "):
            return None
        return {"items": [{"timestamp": f"{y}{m:02d}0100", "views": (100 if t.startswith("Old ") else 1000)}
                          for y in range(2021, 2027) for m in range(1, 13) if f"{y}{m:02d}" <= "202611"]}
    if "wikidata.org" in url:
        if p.get("action") == "wbgetentities":
            return {"entities": {q: wd_entity(q) for q in p["ids"].split("|")}}
        q, d = p["titles"], p.get("rvstart", "")[:10]
        era = 0 if d < "2021-06" else (1 if d < "2023-10" else 2)
        return {"query": {"pages": [{"title": q, "revisions": [{"revid": 5 + era, "timestamp": d + "T00:00:00Z",
                                                                "slots": {"main": {"content": json.dumps(wd_entity(q, era))}}}]}]}}
    a, prop, lst = p.get("action"), p.get("prop", ""), p.get("list", "")
    if a == "query" and "pageassessments" in prop:                       # resolve batch
        titles = p["titles"].split("|")
        cont = bool(p.get("rdcontinue"))
        pages, seen = [], set()
        for x in titles:
            rec = page_record(x, cont)
            if rec["title"] not in seen:
                seen.add(rec["title"]); pages.append(rec)
        if cont:
            for rec in pages:
                if rec["title"] == "Zionism":
                    rec["redirects"] = [{"title": "Zionist movement"}]
        j = {"query": {"pages": pages, "redirects": [{"from": x, "to": REDIRECT[x]} for x in titles if x in REDIRECT]}}
        if "Zionism" in titles and not cont:
            j["continue"] = {"rdcontinue": "1", "continue": "||"}
        return j
    if lst == "search":
        return {"query": {"searchinfo": {"totalhits": hsh(p["srsearch"]) % 5000}, "search": []}}
    if a == "query" and prop == "revisions" and p.get("revids"):          # lead content by revision id
        out = []
        for rid in str(p["revids"]).split("|"):
            title, r = REVMAP[int(rid)]
            slot = {"content": section0(r[3])} if int(rid) % 97 else {"texthidden": True}
            out.append({"revid": r[0], "slots": {"main": slot}})
        assert p.get("rvsection") == 0 and len(out) <= 50
        return {"query": {"pages": [{"title": title, "revisions": out}]}}
    if a == "query" and prop == "revisions" and p.get("rvlimit") == 1:   # snapshot
        d = p["rvstart"]
        if p["titles"].startswith("Talk:"):
            return {"query": {"pages": [{"title": p["titles"], "revisions": [{"revid": 77, "timestamp": d,
                                                                              "slots": {"main": {"content": TP.talk_text(t, d[:10])}}}]}]}}
        if canon(t) in MISSING:
            return {"query": {"pages": [{"title": t, "missing": True}]}}
        s = snapshot(t, d)
        if not s:
            return {"query": {"pages": [{"title": t, "revisions": []}]}}
        if t in HIDDEN_2023 and d.startswith("2023-07"):
            return {"query": {"pages": [{"title": t, "revisions": [{"revid": s[0], "timestamp": s[1], "slots": {"main": {"texthidden": True}}}]}]}}
        return {"query": {"pages": [{"title": t, "revisions": [{"revid": s[0], "timestamp": s[1], "slots": {"main": {"content": s[3]}}}]}]}}
    if a == "query" and prop == "revisions" and ("/Archive" in p.get("titles", "") or "|" in p.get("titles", "")):
        return {"query": {"pages": [{"title": x, "revisions": [{"slots": {"main": {"content": TP.archive_text(i)}}}]}
                                    for i, x in enumerate(p["titles"].split("|"))]}}
    if a == "query" and prop == "revisions":                              # history
        start = p["rvstart"]
        revs = [r for r in rev_list(t) if r[1] >= start]
        if p["titles"].startswith("Talk:"):
            items = [{"timestamp": r[1], "user": r[2], "size": 900 + k} for k, r in enumerate(revs[::2])]
        else:
            items = []
            for k, r in enumerate(revs):
                it = {"revid": r[0], "parentid": r[6], "timestamp": r[1], "user": r[2], "size": len(r[3]), "comment": r[5],
                      "tags": r[4], "minor": k % 5 == 0, "sha1": sha(r[3])}
                if k % 23 == 11:
                    it.pop("user"); it["userhidden"] = True
                items.append(it)
        return page_list(items, p, 500)
    if lst == "users":
        out = []
        for n in p["ususers"].split("|"):
            if n == "OldHand":
                out.append({"name": n, "missing": True}); continue
            u = {"name": n, "editcount": {"Alice": 40000, "Bob Editor": 600, "SockMaster9": 520, "NewbieX": 12}.get(n, 1),
                 "registration": {"NewbieX": "2024-01-01T00:00:00Z", "SockMaster9": "2023-09-01T00:00:00Z"}.get(n, "2010-01-01T00:00:00Z"),
                 "groups": ["*", "user", "extendedconfirmed"] if n in ("Alice", "Bob Editor", "SockMaster9") else ["*", "user"]}
            if n == "SockMaster9":
                u.update({"blockid": 1, "blockexpiry": "infinite", "blockedby": "Alice",
                          "blockreason": "Abusing [[WP:SOCK|multiple accounts]]: see [[User:SockMaster9]] and [[User:Bob Editor]]"})
            if n == "NewbieX":
                u.update({"blockid": 2, "blockexpiry": "infinity", "blockpartial": True, "blockedby": "Bob Editor",
                          "blockreason": "[[WP:AE]] topic ban enforcement (Alice)"})
            out.append(u)
        return {"query": {"users": out}}
    if lst == "logevents":
        return {"query": {"logevents": logevents(p["letitle"])}}
    if p.get("generator") == "allpages":
        pre = p["gapprefix"]
        return {"query": {"pages": [{"pageid": i, "title": f"Talk:{pre}Archive {i}", "length": 100000,
                                     "revisions": [{"timestamp": f"{2019 + i}-03-01T00:00:00Z"}]} for i in range(1, 8)]}}
    raise AssertionError(f"unmocked request: {url} {p}")


def mock_post(url, body, tries=4):
    return {"output": {"probabilities": {"true": 0.5}}}


def setup(tmp):
    import mass, mass2, analyze, pilot
    wt_net.get_json = mock_get; wt_net.post_json = mock_post
    wt_net._wait_slot = lambda: None
    wt_net.STATUS_DIR = os.path.join(tmp, "status")
    mass.OUT = os.path.join(tmp, "mass"); analyze.DATA = os.path.join(tmp, "data")
    os.makedirs(mass.OUT, exist_ok=True); os.makedirs(analyze.DATA, exist_ok=True)
    pilot._ucache.clear()
    rows = [{"title": x, "group": "topic", "project": "Israel", "importance": "Top"} for x in TOPIC] + \
           [{"title": x, "group": "comparison", "project": "Serbia" if x == "Kosovo" else "India", "importance": "High"} for x in COMP]
    json.dump({"rows": rows, "category_counts": {}, "excluded_both": 0}, open(os.path.join(mass.OUT, "frame.json"), "w"))
    return mass, mass2


def main():
    ok = True

    def check(cond, msg):
        nonlocal ok
        print(("PASS " if cond else "FAIL ") + msg, flush=True); ok &= bool(cond)

    tmp = tempfile.mkdtemp()
    try:
        mass, mass2 = setup(tmp)
        import pilot
        check(not pilot.LW_ON[0], "LiftWing off by default (WT_LIFTWING unset)")
        # ---------------- resolve: dedupe, missing, disambiguation, atrocity titles, alias table
        f2 = mass2.resolve()
        titles = [r["title"] for r in f2["rows"]]
        check(len(titles) == len(set(titles)), "resolved rows unique by resolved title")
        pal = next(r for r in f2["rows"] if r["title"] == "Palestine")
        check(pal["frame_titles"] == ["Palestine", "Palestinian state"], f"redirect merged into its target: {pal['frame_titles']}")
        check("Ghost page" in f2["dropped"]["missing"], "missing page dropped and listed")
        check(f2["dropped"]["disambiguation"] == ["Darfur genocide"], f"disambiguation dropped: {f2['dropped']['disambiguation']}")
        ar = f2["atrocity_resolved"]
        check(ar["sudan_2023"] == ["El Fasher massacre", "Masalit genocide"] and ar["darfur_2003"] == ["Darfur genocide (2003–2005)"]
              and ar["uyghur"] == ["Persecution of Uyghurs in China"], f"atrocity titles resolved via redirects: {ar}")
        check(all(len(v) >= 1 for v in ar.values()), "every atrocity case has a resolved page")
        check(f2["aliases"].get("1948 palestinian exodus") == "1948 Palestinian expulsion and flight"
              and f2["aliases"].get("zionist movement") == "Zionism", "alias table from redirects (incl. continuation)")
        check(f2["now"] == NOW and all(r.get("wd_now") for r in f2["rows"] if r["pi"].get("qid")), "fixed now + batched Wikidata now")
        n_rows = len(f2["rows"])
        # ---------------- shard run with one failing article (<5%), then resume
        FAIL.clear(); FAIL.add("Topic page 3")
        mass2.run_shard(0, 1)
        part = json.load(gzip.open(os.path.join(mass.OUT, "m2_0.json.gz"), "rt"))
        check(len(part) == n_rows - 1, f"one article error tolerated, checkpoint has {len(part)}/{n_rows}")
        FAIL.clear()
        c0 = CALLS["n"]
        mass2.run_shard(0, 1)
        part = json.load(gzip.open(os.path.join(mass.OUT, "m2_0.json.gz"), "rt"))
        check(len(part) == n_rows and "Topic page 3" in {r["title"] for r in part}, "resume from checkpoint completes the shard")
        check(CALLS["n"] - c0 < 120, f"resume only re-collects the missing article ({CALLS['n'] - c0} requests)")
        c1 = CALLS["n"]; mass2.run_shard(0, 1)
        check(CALLS["n"] == c1, "a finished shard does no new work on resume")
        # ---------------- merge
        mass2.merge()
        d = json.load(open(os.path.join(tmp, "data", "mass2.json")))
        R = {r["title"]: r for r in d["articles"]}
        DET = json.load(gzip.open(os.path.join(tmp, "data", "mass2_events.json.gz"), "rt"))["articles"]
        check(len(R) == n_rows and "_leads" not in R["Zionism"] and "_editors" not in R["Zionism"], "merge: one compact record per article")
        leads = json.load(gzip.open(os.path.join(tmp, "data", "mass2_leads.json.gz"), "rt"))
        check(leads["dates"] == ["2021-01-01", "2023-07-01", "now"] and leads["leads"]["Zionism"][2]
              and "Zionism" in leads["leads"]["Zionism"][2], "lead prose stored per snapshot in mass2_leads.json.gz")
        z = R["Zionism"]; za, zn = z["at"]["2021-01-01"], z["at"]["now"]
        check(za["article"]["short_desc"] == "Region in the Middle East" and zn["article"]["infobox"]["type"] == "infobox country",
              "short description + infobox from snapshots")
        check(zn["article"]["categories"] == ["Bar", "Disputed territories"], "categories")
        check("1948 Palestinian expulsion and flight" in za["article"]["concepts"] and "1948 Palestinian expulsion and flight" in zn["article"]["concepts"]
              and "nakba_1948" in zn["article"]["concept_groups"], "rename resolved: concept linked at 2021 and now despite the new title")
        check("links" not in zn["article"] and "heading_h" in zn["article"], "full link list dropped, headings hashed")
        check(zn["article"]["lead_domains"].get("hrw.org") == 1 and zn["article"]["lead_refs_resolved"].get("Rights orgs & UN") == 1,
              f"lead citation domains {zn['article']['lead_domains']}")
        check(zn["article"]["lex_lead"].get("disp_P", 0) >= 1 and za["article"]["lex_lead"].get("disp_P", 0) == 0
              and zn["article"]["lex_lead"].get("disp_J", 0) >= 1, "P/J displacement counted separately")
        nr = zn["narr"]
        check(nr and "ev" in nr and "sentence" in nr["ev"] and nr["c"].get("N4_P", 0) >= 0 and "lead_prose" not in nr,
              "mass_narr features with event filter on the same snapshot")
        ztn = z["talk_now"]
        check(ztn["ct_notice"] and ztn["class"] == "ga", "talk now parsed")
        items = DET["Zionism"]["discussions"]
        check(any(i["kind"] == "rfc" and i["ts"] == "2024-03-03T10:00:00Z" and i["formal"] for i in items)
              and any(i["kind"] == "rm" and i["result"] == "moved" for i in items)
              and any(i["kind"] == "rm" and i["result"] == "not moved" for i in items), "RfC/RM per-discussion dates and results")
        check(z["discussions"]["w2"]["rm_moved"] >= 1 and z["discussions"]["w1"]["rfc_closed"] >= 1, "RfC/RM window counts")
        pz = {k: z["at"][k]["protection"] for k in z["at"]}
        check(pz["2021-01-01"] == {"edit": "autoconfirmed", "move": "sysop"}, f"old-format protection parsed: {pz['2021-01-01']}")
        check(pz["now"] == {"edit": "extendedconfirmed"} and z["protection"]["source_now"] == "page_info", f"now anchored on page info {pz['now']}")
        isr = R["Israel"]
        check(isr["at"]["2023-07-01"]["protection"] == {"edit": "autoconfirmed"} and "Old Israel" in isr["protection"]["titles_followed"],
              f"protection followed to the former title: {isr['at']['2023-07-01']['protection']} {isr['protection']['titles_followed']}")
        check(R["Kosovo"]["at"]["2021-01-01"]["protection"] == {} and R["Kosovo"]["at"]["2023-07-01"]["protection"] == {"edit": "autoconfirmed"},
              f"oldest format + unprotect + expiry: {R['Kosovo']['at']['2021-01-01']['protection']} {R['Kosovo']['at']['2023-07-01']['protection']}")
        mv = [m for m in isr["moves"] if m["from"] == "Old Israel"]
        check(mv and mv[0]["rm"] and isr["at"]["2021-01-01"]["title"] == "Old Israel", "RM move + title at 2021")
        vm = z["moves"]
        check(len(vm) == 2 and not any(m["rm"] for m in vm) and vm[0].get("reverted") and z["at"]["2021-01-01"]["title"] == "Zionism",
              f"vandal move/revert pair flagged, not RM: {vm}")
        pv = isr["pageviews"]
        mv_ = pv["monthly"]
        check(pv["titles"] == ["Israel", "Old Israel"] and mv_["start"] == "202101" and len(mv_["views"]) == 70 and mv_["views"][-1] == 1100,
              f"pageviews summed over former titles, partial month excluded")
        check(isr["win"]["w2"]["views"]["per_month"] == 1100, "views per month over the window")
        w2 = z["win"]["w2"]
        check(w2["edits"] > 0 and w2["cmt_sock_ban"] > 0 and w2["bytes_added"] > 0 and "tags" in w2, "revision metadata signals")
        acc = w2["accounts"]
        check(acc["n_edits"] > 0 and acc["share_indef_now"] > 0 and acc["share_indef_sitewide_now"] is not None
              and acc["share_indef_sock_now"] > 0, f"account aggregates incl. partial/sock flags")
        check(z["wikidata_2023"]["descriptions"]["en"] == "country in West Asia" and z["now"]["wikidata"]["descriptions"]["en"] == "state in West Asia",
              "Wikidata now (batched) + 2023 snapshot")
        te = z["term_events"]
        check(te and te["coverage"]["stride"] == 1 and te["coverage"]["last_known_ts"] == te["coverage"]["last_ts"], "lead events full read on a normal page")
        evs = DET["Zionism"]["lead_events"]
        check(any(e["kind"] == "insert" and e["term"] == "apartheid" and e["ts"] < "2021-07" for e in evs),
              "first in-window revision is compared with the 2021 seed (window boundary fix)")
        allev = [e for x in DET.values() for e in x.get("lead_events") or []]
        check(all(e["u"] is None or re.fullmatch(r"[0-9a-f]{12}", e["u"]) for e in allev)
              and any(e["acct"] and e["acct"]["indef"] and e["acct"]["breason"] == "sock" for e in allev), "per-event hashed account flags")
        check("by_window_new_only" in te and "restores" in te, "restore split")
        # empty / missing / redirect / created-later / no-talk records
        e = R["Empty page"]
        check(e["at"]["now"]["narr"] is None and e["win"]["w2"].get("edits", 0) == 0 and e["term_events"]["coverage"]["n_revs"] == 0
              and e["talk_now"] is None and e["now"]["wikidata"] is None, "empty page with no revisions, talk or QID")
        g = R["Gaza genocide"]
        check(g["at"]["2021-01-01"]["article"] is None and g["at"]["2021-01-01"]["title"] is None and g["created_in_window"],
              "created later: no snapshot and no title before creation")
        check(g["term_events"]["coverage"]["seeded"] is False, "created later: lead events start unseeded")
        wb = R["West Bank"]
        check(wb["at"]["2021-01-01"]["article"] == {"redirect": True} and wb["at"]["2021-01-01"]["narr"] is None, "snapshot that was a redirect")
        check(R["Hebron"]["at"]["2023-07-01"]["rev"].get("hidden") and R["Hebron"]["discussions"] is None, "hidden text + no talk")
        check(R["Plantation of Ulster"]["win"]["w1"].get("edits", 0) == 0 and R["Plantation of Ulster"]["at"]["now"]["article"], "no revisions since 2021")
        check("Ghost page" not in R and "Palestinian state" not in R and "Darfur genocide" not in R, "missing / redirect / disambiguation not collected")
        check(R["Masalit genocide"]["atrocity_case"] == "sudan_2023" and R["Masalit genocide"]["stratum"] == "atrocity", "atrocity stratum")
        # ---------------- heaviest-page coverage (pilot fault: Gaza war stopped at 2023-10-07)
        hv = R[HEAVY]["term_events"]; cv = hv["coverage"]
        print("heavy coverage:", json.dumps(cv))
        check(cv["n_revs"] == N_HEAVY and cv["stride"] > 1 and cv["last_known_ts"] == cv["last_ts"] and cv["last_ts"] >= "2026-10",
              "heavy page: grid reaches the last revision (2026)")
        hev = DET[HEAVY]["lead_events"]
        got = sorted((e["ts"][:10], e["term"], e["kind"], e["exact"]) for e in hev)
        exp_i = [(500, "occupation", "insert"), (2950, "genocide", "insert"), (2990, "genocide", "remove"), (2999, "occupation", "remove")]
        exp = sorted((ts_at(i, N_HEAVY)[:10], t, k, True) for i, t, k in exp_i)
        check(got == exp, f"heavy page: every net flip found exactly, up to the end ({got})")
        rm = next(e for e in hev if e["term"] == "genocide" and e["kind"] == "remove")
        ins = next(e for e in hev if e["term"] == "genocide" and e["kind"] == "insert")
        check(rm["restore"] and not ins["restore"], "identity revert tagged as restore, new insertion not")
        check(cv["requests"] <= mass2.LEAD_GRID + 3 + mass2.LEAD_REFINE, f"heavy page bounded requests ({cv['requests']})")
        # ---------------- privacy: no usernames anywhere
        blobs = [open(f, "rb").read().decode("utf-8", "ignore") for f in glob.glob(os.path.join(tmp, "data", "*.json"))]
        blobs += [gzip.open(f, "rt").read() for f in glob.glob(os.path.join(tmp, "data", "*.gz")) + glob.glob(os.path.join(tmp, "mass", "*.gz"))]
        blobs += [open(os.path.join(tmp, "mass", "frame2.json")).read()]
        raw = "\n".join(blobs)
        leaked = [u for u in REAL_USERS if re.search(r'"%s"' % re.escape(u), raw) or ("User:" + u) in raw or ("(" + u + ")") in raw]
        check(not leaked, f"no usernames in any output (leaked: {leaked})")
        check("multiple accounts" not in raw and "topic ban" not in raw and "Persistent vandalism" not in raw, "no block reasons / log comments")
        # ---------------- empty shard
        mass._run("m2empty", mass2.collect, [], 0)
        check(os.path.exists(os.path.join(mass.OUT, "m2empty_0.json.gz")), "empty shard runs and writes an empty checkpoint")
        # ---------------- fail loudly above 5%
        mass.OUT = os.path.join(tmp, "mass_fail"); os.makedirs(mass.OUT)
        shutil.copy(os.path.join(tmp, "mass", "frame2.json"), mass.OUT)
        FAIL.clear(); FAIL.update({"Topic page 1", "Topic page 2", "Topic page 5"})
        try:
            mass2.run_shard(0, 1)
            check(False, ">5% article errors must exit non-zero")
        except SystemExit as ex:
            check(bool(ex.code), f">5% article errors exit non-zero: {ex.code}")
        FAIL.clear()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    ok &= unit_lead_coverage()
    print("ALL PASS" if ok else "SOME CHECKS FAILED")
    sys.exit(0 if ok else 1)


def unit_lead_coverage():
    """Direct test of mass2.lead_events on a 6,000-revision 2021-2026 history (stride 15), flips spread to the very end."""
    import mass2, pilot
    n = 6000
    terms = lambda i: {k: False for k in pilot.TERMS} | {"genocide": (1000 <= i < 1500) or i >= 5990, "apartheid": 3000 <= i < 5999}
    text = {}
    seq = []
    for i in range(n):
        st = terms(i)
        body = "'''X''' is a place." + (" It is a genocide." if st["genocide"] else "") + (" It is apartheid." if st["apartheid"] else "")
        body += f" v{i // 25}"
        rid = 9_000_000 + i
        text[rid] = body
        seq.append({"revid": rid, "timestamp": ts_at(i, n), "user": "Alice", "sha1": sha(body), "tags": []})
    calls = [0]

    def fake_q(params, url=None, core=True):
        calls[0] += 1
        ids = [int(x) for x in str(params["revids"]).split("|")]
        assert len(ids) <= 50
        return {"query": {"pages": [{"revisions": [{"revid": r, "slots": {"main": {"content": text[r]}}} for r in ids]}]}}
    orig = pilot.q
    pilot.q = fake_q
    try:
        ev, cov = mass2.lead_events(seq, pilot.lead_terms("'''X''' is a place."), grid_req=8, refine_req=40)
    finally:
        pilot.q = orig
    got = [(e["term"], e["kind"], e["revid"] - 9_000_000, e["exact"]) for e in ev]
    exp = [("genocide", "insert", 1000, True), ("genocide", "remove", 1500, True), ("apartheid", "insert", 3000, True),
           ("genocide", "insert", 5990, True), ("apartheid", "remove", 5999, True)]
    ok = got == exp and cov["last_known_ts"] == seq[-1]["timestamp"] and cov["last_ts"].startswith("2026") and calls[0] <= 8 + 3 + 40
    print(("PASS " if ok else "FAIL ") + f"unit: 6,000-revision history 2021-2026 -> events up to the end, exact ({got}; "
          f"stride {cov['stride']}, {calls[0]} requests, last {cov['last_known_ts']})")
    return ok


if __name__ == "__main__":
    main()
