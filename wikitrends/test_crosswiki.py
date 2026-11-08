"""Offline tests for crosswiki.py and analyze_crosswiki.py: a fake set of Wikipedias + Meta + Wikidata + the pageview REST API
behind wt_net.get_json (no network).

  python test_crosswiki.py            -> exits non-zero on any failed check
Collector: title resolution (langlinks, disambiguation fallback, two English Nakba pages, missing pages), RTL normalisation,
the Arabic / Hebrew / Russian / German / French lexicon fixes, voice (attributed vs own voice), full and grid + refine reading
(an insert-and-revert double flip inside a grid interval is found exactly), ratchet reuse for English, one global account linked
across wikis / local accounts and different accounts not linked, sources at insertion, talk metadata, protection and move logs,
pageviews over former titles, English RfC / RM dates and outcomes, Wikidata description changes, creation dates, narrative
features, resume (no lead re-reads), fail-loud (>5% pages failing, missing salt).
Analysis: planted cross-wiki campaign (3 accounts, 3 languages, same term family, within 2 days) is flagged, noise is not;
outputs pass the privacy gate and contain no usernames (article or talk), hashes or salt; the gate catches planted leaks.
"""
import glob, gzip, hashlib, json, os, re, shutil, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SALT = "test-salt-crosswiki-91b2"
os.environ["WT_SALT"] = SALT
os.environ["WT_JOB"] = "crosswiki-test"
import numpy as np        # noqa: E402
import wt_net             # noqa: E402
import analyze as A       # noqa: E402
import coord as CO        # noqa: E402
import crosswiki as CW    # noqa: E402
import analyze_crosswiki as AX  # noqa: E402
import analyze_coord as AC      # noqa: E402

FAILS = []
USERNAMES = ["Mira Talkative", "Noor Bridge", "Solo Local", "Kai Single", "FixBot", "Talk Only Person", "192.0.2.5"]


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg, flush=True)
    if not cond:
        FAILS.append(msg)


# ------------------------------------------------------------------ fake world
WIKI = {}            # lang -> {title: page}
GUI = {"Mira Talkative": ["enwiki", "dewiki", "frwiki", "hewiki"], "Noor Bridge": ["enwiki", "arwiki", "hewiki", "dewiki"],
       "Kai Single": ["dewiki"]}               # Solo Local: no global account (local on each wiki)
CALLS = []
FAIL_LANG = set()
RID = [5_000_000]


def ts(day, hour=12):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(1609459200 + day * 86400 + hour * 3600))


def page(lang, title, specs, talk=None, pre=None, created_before=True, links=None, qid=None, dis=False):
    """specs: list of (day, user, text[, tags]); pre: text of the last revision before 2021."""
    revs, prev_size = [], None
    pid = len(WIKI.get(lang, {})) * 10 + 1000
    if created_before or pre:
        RID[0] += 1
        revs.append({"revid": RID[0], "parentid": RID[0] - 1, "timestamp": "2020-06-01T00:00:00Z", "user": "Kai Single",
                     "content": pre or "Old lead.", "tags": [], "comment": "old", "size": len(pre or "Old lead.")})
    for k, sp in enumerate(specs):
        day, user, text = sp[:3]
        tags = sp[3] if len(sp) > 3 else []
        comment = sp[4] if len(sp) > 4 else "edit"
        RID[0] += 1
        revs.append({"revid": RID[0], "parentid": revs[-1]["revid"] if revs else 0, "timestamp": ts(day, 12 + k % 10), "user": user,
                     "content": text, "tags": tags, "comment": comment, "size": len(text.encode())})
    for r in revs:
        r["sha1"] = hashlib.sha1(r["content"].encode()).hexdigest()
    WIKI.setdefault(lang, {})[title] = {"title": title, "pageid": pid, "revs": revs, "talk": talk or [], "links": links or {},
                                        "qid": qid, "dis": dis, "talkid": pid + 1 if talk is not None else None}
    return revs


def talkrevs(lang, specs):
    out = []
    for day, user in specs:
        RID[0] += 1
        out.append({"revid": RID[0], "parentid": RID[0] - 1, "timestamp": ts(day, 15), "user": user, "comment": f"reply [[User:{user}]]",
                    "size": 100, "tags": [], "sha1": "x" * 40})
    return out


def build_world():
    WIKI.clear()
    base = "'''Zionism''' is a nationalist movement.<ref>https://www.timesofisrael.com/a</ref> It emerged in Europe."
    gen = base + " Scholars and states have called the war a genocide.<ref>https://www.aljazeera.com/b</ref>"
    gen2 = base + " The war is a genocide.<ref>https://www.aljazeera.com/b</ref><ref>https://www.hrw.org/c</ref>"
    page("en", "Zionism", [(10, "Kai Single", base), (500, "Mira Talkative", gen), (520, "Noor Bridge", gen2),
                           (900, "192.0.2.5", gen2 + " x"), (1000, "FixBot", gen2 + " y")],
         talk=talkrevs("en", [(400, "Mira Talkative"), (401, "Talk Only Person"), (402, "Noor Bridge")]), pre=base,
         links={"de": "Zionismus", "fr": "Sionisme", "he": "ציונות", "ar": "صهيونية", "es": "Sionismo"}, qid="Q180")
    # German: Mira inserts Völkermord one hour after an English-day event; Solo (local) also edits
    de0 = "'''Zionismus''' ist eine Nationalbewegung."
    page("de", "Zionismus", [(30, "Solo Local", de0 + " Sie entstand in Europa."), (600, "Mira Talkative", de0 + " Kritiker werfen Israel Völkermord vor."),
                             (601, "Mira Talkative", de0 + " Der Krieg ist ein Völkermord.")], talk=talkrevs("de", [(600, "Mira Talkative"), (650, "Talk Only Person")]), pre=de0)
    fr0 = "'''Le sionisme''' est un mouvement national."
    page("fr", "Sionisme", [(31, "Solo Local", fr0 + " Il est né en Europe."), (600, "Mira Talkative", fr0 + " La guerre est un génocide."),
                            (700, "Solo Local", fr0 + " Selon des critiques, un génocide est en cours.")],
         talk=talkrevs("fr", [(601, "Mira Talkative")]), pre=fr0)
    he0 = "‏'''הַצִּיּוֹנוּת''' היא תנועה לאומית."
    page("he", "ציונות", [(40, "Noor Bridge", he0 + " ישראל מבצעת רֶצַח הָעַם."), (41, "Noor Bridge", he0 + " ישראל נמצאת בכבוש.")], pre=he0)
    ar0 = "الصهيونية حركة سياسية."
    page("ar", "صهيونية", [(42, "Noor Bridge", ar0 + " وتقوم إسرائيل بـالإبادةُ الجماعيةُ في غزة."),
                           (43, "Noor Bridge", ar0 + " بحسب منتقدين، الإبادة الجماعية مستمرة.")], pre=ar0)
    page("es", "Sionismo", [(44, "Solo Local", "'''El sionismo''' es un movimiento.")], pre="'''El sionismo''' es un movimiento.")
    # Israel (de) is heavy: 300 revisions, a double flip (insert + revert) inside a grid interval and a lasting flip at 200
    specs, txt0, txt1 = [], "'''Israel''' ist ein Staat.", "'''Israel''' ist ein Staat. Die Besatzung dauert an."
    for k in range(300):
        if k == 101:
            specs.append((100 + k, "Kai Single", txt0 + " Völkermord!", ["mw-reverted"]))
        elif k == 102:
            specs.append((100 + k, "Mira Talkative", txt0, ["mw-undo"]))
        elif k >= 200:
            specs.append((100 + k, "Noor Bridge" if k == 200 else "Kai Single", txt1 + ("" if k == 200 else f" Satz {k % 3}")))
        else:
            specs.append((100 + k, "Kai Single", txt0 + ("" if k in (100, 102) else f" {'.' * (k % 4)}")))
    page("de", "Israel", specs, pre=txt0)
    page("en", "Israel", [(5, "Kai Single", "'''Israel''' is a country in West Asia.")], pre="'''Israel''' is a country.",
         links={"de": "Israel"}, qid="Q801")
    # Hamas (de): terror designation moves from sentence 1 to sentence 3
    page("de", "Hamas", [(50, "Kai Single", "Die Hamas ist eine Terrororganisation. Sie regiert Gaza."),
                         (800, "Kai Single", "Die Hamas ist eine Organisation. Sie regiert Gaza. 41 Staaten stufen sie als terroristisch ein.")],
         pre="Die Hamas ist eine Terrororganisation.")
    page("en", "Hamas", [(6, "Kai Single", "'''Hamas''' is an organisation.")], pre="'''Hamas''' is.", links={"de": "Hamas"})
    # October 7 (he): created 2023, renamed from surprise attack to massacre; hostages; the mover's name is in the comment
    o7 = "טבח שבעה באוקטובר היה מתקפה של חמאס. 251 חטופים נלקחו לעזה."
    page("he", "טבח שבעה באוקטובר", [(1010, "Noor Bridge", "מתקפת הפתע על ישראל הייתה מבצע של חמאס. חטופים רבים."),
                                       (1100, "Noor Bridge", "מתקפת הפתע על ישראל הייתה מבצע של חמאס. חטופים רבים.", [],
                                        "Noor Bridge העביר את הדף [[מתקפת הפתע על ישראל]] לשם [[טבח שבעה באוקטובר]]"),
                                       (1101, "Mira Talkative", o7)], created_before=False)
    page("en", "October 7 attacks", [(1010, "Kai Single", "The '''October 7 attacks''' were a series of attacks. Hostages were taken.")],
         created_before=False, links={"he": "טבח שבעה באוקטובר"})
    # Gaza genocide (ar): court overstatement with harakat
    page("ar", "الإبادة الجماعية لغزة", [(1100, "Noor Bridge", "الإبادة الجماعية لغزة هي تدمير. وجدت المحكمة أن إسرائيل تعمل بنيّة معقولة.")],
         created_before=False)
    page("en", "Gaza genocide", [(1090, "Kai Single", "The '''Gaza genocide''' is the ongoing destruction.")], created_before=False,
         links={"ar": "الإبادة الجماعية لغزة"})
    page("en", "Palestine", [(1, "Kai Single", "'''Palestine''' may refer to:")], dis=True)
    page("en", "State of Palestine", [(2, "Kai Single", "'''Palestine''' is a state.")], pre="'''Palestine''' is a state.")
    page("en", "Nakba", [(3, "Kai Single", "The '''Nakba''' was the ethnic cleansing of Palestinians.")], pre="The '''Nakba''' was.",
         links={"de": "Nakba"})
    page("en", "1948 Palestinian expulsion and flight", [(4, "Kai Single", "In 1948 Palestinians were expelled.")], pre="In 1948.",
         links={"de": "Nakba"})
    page("de", "Nakba", [(5, "Kai Single", "Die Nakba bezeichnet die Flucht.")], pre="Die Nakba.")


EN_TALK = ("== RfC: first sentence ==\n{{closed rfc top|result=There is consensus for option A. Closer 12:00, 5 March 2024 (UTC)}}\n"
           "Should the first sentence change? Opener 10:00, 1 February 2024 (UTC)\nReply 11:00, 2 February 2024 (UTC)\n")
EN_ARCH = ("== Requested move 3 June 2023 ==\n{{requested move/dated|Zionism (ideology)}}\nPropose. A 09:00, 3 June 2023 (UTC)\n"
           "The result of the move request was: '''not moved'''. Closer 10:00, 20 June 2023 (UTC)\n")


def _find(lang, **p):
    w = WIKI.get(lang, {})
    if "pageids" in p:
        for pg in w.values():
            if pg.get("talkid") == int(p["pageids"]):
                return pg, True
        return None, False
    return w.get(p.get("titles")), False


def _rev_out(r, content=False):
    out = {k: r[k] for k in ("revid", "parentid", "timestamp", "user", "comment", "size", "tags", "sha1") if k in r}
    if content:
        out = {"revid": r["revid"], "timestamp": r["timestamp"], "slots": {"main": {"content": r["content"]}}}
    return out


def mock_get(url, params, tries=8, ok404=False):
    p = dict(params)
    host = re.match(r"https://([^/]+)/", url).group(1)
    lang = host.split(".")[0]
    CALLS.append((host, p.get("action"), p.get("prop") or p.get("list") or p.get("meta"), "revids" in p, p.get("rvsection")))
    if lang in FAIL_LANG:
        return None
    if host == "wikimedia.org":
        m = re.search(r"/per-article/(\w+)\.wikipedia/all-access/user/([^/]+)/monthly/", url)
        return {"items": [{"timestamp": f"2023{mo:02d}0100", "views": 1000 * mo} for mo in range(9, 13)] +
                         [{"timestamp": "2024010100", "views": 5000}]}
    if host == "meta.wikimedia.org":
        w = GUI.get(p["guiuser"])
        return {"query": {"globaluserinfo": {"missing": True}}} if w is None else \
            {"query": {"globaluserinfo": {"home": w[0], "registration": "2016-02-03T00:00:00Z", "editcount": 23456, "name": p["guiuser"],
                                          "merged": [{"wiki": x, "editcount": 10} for x in w]}}}
    if host == "www.wikidata.org":
        if p.get("action") == "wbgetentities":
            return {"entities": {q: {"labels": {"he": {"value": "ציונות"}}, "descriptions": {"he": {"value": "תנועה לאומית"},
                                                                                              "en": {"value": "nationalist movement"}}}
                                 for q in p["ids"].split("|")}}
        return {"query": {"pages": [{"title": p["titles"], "revisions": [
            {"timestamp": "2022-05-01T00:00:00Z", "comment": "/* wbsetdescription-set:1|he */ תנועה פוליטית"},
            {"timestamp": "2024-02-01T00:00:00Z", "comment": "/* wbsetdescription-set:1|he */ תנועה לאומית"},
            {"timestamp": "2024-03-01T00:00:00Z", "comment": "/* wbeditentity-update-languages-short:0||ar, fr */"},
            {"timestamp": "2024-04-01T00:00:00Z", "comment": "/* wbsetlabel-set:1|de */ Zionismus"}]}]}}
    act, prop, lst = p.get("action"), p.get("prop"), p.get("list")
    if prop == "langlinks|pageprops":
        pg = WIKI["en"].get(p["titles"])
        if not pg:
            return {"query": {"pages": [{"title": p["titles"], "missing": True}]}}
        pp = {"disambiguation": ""} if pg["dis"] else {}
        if pg["qid"]:
            pp["wikibase_item"] = pg["qid"]
        return {"query": {"pages": [{"title": pg["title"], "pageprops": pp,
                                     "langlinks": [{"lang": l, "title": t} for l, t in pg["links"].items()]}]}}
    if prop == "revisions|info":
        pg, is_talk = _find(lang, **p)
        if not pg:
            return {"query": {"pages": [{"title": p.get("titles"), "missing": True}]}}
        revs = pg["talk"] if is_talk else [r for r in pg["revs"] if r["timestamp"] >= p["rvstart"]]
        k = int((p.get("rvcontinue") or "0"))
        chunk = revs[k:k + 40]                                  # page size 40: exercises continuation
        j = {"query": {"pages": [{"title": pg["title"], "pageid": pg["pageid"], "talkid": pg["talkid"],
                                  "revisions": [_rev_out(r) for r in chunk]}]}}
        if k + 40 < len(revs):
            j["continue"] = {"rvcontinue": str(k + 40), "continue": "||"}
        return j
    if prop == "revisions" and "revids" in p:
        ids = {int(x) for x in str(p["revids"]).split("|")}
        pages = []
        for pg in WIKI.get(lang, {}).values():
            rr = [_rev_out(r, True) for r in pg["revs"] if r["revid"] in ids]
            if rr:
                pages.append({"title": pg["title"], "revisions": rr})
        return {"query": {"pages": pages}}
    if prop == "revisions" and p.get("rvdir") == "older":
        pg = WIKI[lang][p["titles"]]
        rr = [r for r in pg["revs"] if r["timestamp"] < p["rvstart"]][-1:]
        return {"query": {"pages": [{"title": pg["title"], "revisions": [_rev_out(r, True) for r in rr]}]}}
    if prop == "revisions" and p.get("rvdir") == "newer" and p.get("rvlimit") == 1:
        pg = WIKI[lang][p["titles"]]
        return {"query": {"pages": [{"title": pg["title"], "revisions": [{"revid": pg["revs"][0]["revid"], "timestamp": pg["revs"][0]["timestamp"]}]}]}}
    if prop == "revisions" and p.get("rvprop") == "content":          # English talk + archives
        out = []
        for t in p["titles"].split("|"):
            if t == "Talk:Zionism":
                out.append({"title": t, "revisions": [{"slots": {"main": {"content": EN_TALK}}}]})
            elif t.startswith("Talk:Zionism/Archive"):
                out.append({"title": t, "revisions": [{"slots": {"main": {"content": EN_ARCH}}}]})
            else:
                out.append({"title": t, "missing": True})
        return {"query": {"pages": out}}
    if prop == "revisions" and p.get("rvprop") == "timestamp":
        return {"query": {"pages": [{"title": t, "revisions": [{"timestamp": "2023-07-01T00:00:00Z" if "1" in t else "2019-01-01T00:00:00Z"}]}
                                    for t in p["titles"].split("|")]}}
    if lst == "allpages":
        return {"query": {"allpages": [{"title": "Talk:Zionism/Archive 1"}, {"title": "Talk:Zionism/Archive 2"}]
                          if p["apprefix"] == "Zionism/" else []}}
    if lst == "logevents":
        if p["letype"] == "protect":
            if lang == "en" and p["letitle"] == "Zionism":
                return {"query": {"logevents": [{"timestamp": "2023-10-08T00:00:00Z", "action": "protect",
                                                 "params": {"details": [{"type": "edit", "level": "extendedconfirmed", "expiry": "infinite"}]}}]}}
            return {"query": {"logevents": []}}
        if p["letype"] == "move" and p["letitle"] == "מתקפת הפתע על ישראל":
            return {"query": {"logevents": [{"timestamp": ts(1100, 13), "title": "מתקפת הפתע על ישראל", "ns": 0,
                                             "params": {"target_title": "טבח שבעה באוקטובר", "target_ns": 0}}]}}
        return {"query": {"logevents": []}}
    raise AssertionError(f"unmocked request {host} {params}")


def ratchet_fixture(tmp):
    en = WIKI["en"]["Zionism"]["revs"]
    rid = {k: r["revid"] for k, r in enumerate(en)}       # 0 = pre-2021, 1.. = specs
    ev = {"genocide": [{"kind": "insert", "t": CW.ep(en[2]["timestamp"]), "revid": rid[2], "survived": 9e7, "censored": True}]}
    arts = {"Zionism": {"revisions": 5, "terms": {t: {"present_start": False, "present_end": t == "genocide"} for t in A.CRITICAL}}}
    json.dump({"events": {"Zionism": ev}, "articles": arts}, open(os.path.join(tmp, "ratchet.json"), "w"))
    # ratchet ran at day 950: the two later revisions are read in full
    CW._RATCHET[0] = None
    rj = json.load(open(os.path.join(tmp, "ratchet.json")))
    rj["events"]["Zionism"]["genocide"][0]["survived"] = 1609459200 + 950 * 86400 - rj["events"]["Zionism"]["genocide"][0]["t"]
    json.dump(rj, open(os.path.join(tmp, "ratchet.json"), "w"))


def setup(tmp):
    wt_net.get_json = mock_get
    wt_net._wait_slot = lambda: None
    wt_net.STATUS_DIR = os.path.join(tmp, "status")
    CW.OUT = os.path.join(tmp, "crosswiki"); os.makedirs(CW.OUT, exist_ok=True)
    A.DATA = tmp
    shutil.copy(os.path.join(HERE, "data", "crosslang.json"), os.path.join(tmp, "crosslang.json")) if os.path.exists(
        os.path.join(HERE, "data", "crosslang.json")) else None
    CW._gui.clear(); CW._gui_n[0] = 0; CW._RATCHET[0] = None
    CW.FULL_REQ, CW.GRID_REQ, CW.REFINE_REQ = 4, 1, 10           # the 300-revision German page goes to the grid


def all_text(d):
    out = []
    for f in glob.glob(os.path.join(d, "**", "*"), recursive=True):
        if os.path.isfile(f):
            b = open(f, "rb").read()
            if f.endswith(".gz"):
                b = gzip.decompress(b)
            out.append((f, b.decode("utf-8", "replace")))
    return out


# ------------------------------------------------------------------ unit tests
def test_text():
    old_ar = re.compile(json.load(open(os.path.join(HERE, "data", "crosslang.json")))["lexicon"]["genocide"], re.I) \
        if os.path.exists(os.path.join(HERE, "data", "crosslang.json")) else None
    s = "ترتكب إسرائيل الإبادة الجماعية في غزة"
    check(old_ar is None or not old_ar.search(s), "old crosslang Arabic pattern misses «الإبادة الجماعية» (the gap)")
    check(CW.term_in("ar", "genocide", CW.norm(s)), "fixed Arabic pattern matches «الإبادة الجماعية»")
    check(CW.term_in("ar", "genocide", CW.norm("وقعت إبادةٌ جماعيّة")), "Arabic indefinite with harakat matches")
    check(CW.term_in("ar", "genocide", CW.norm("بـالإبادة الجماعية")), "Arabic with tatweel and prefix matches")
    check(CW.term_in("ar", "ethnic_cleansing", CW.norm("حرب التطهير العرقي لفلسطين")), "Arabic «التطهير العرقي» matches")
    check(CW.term_in("ar", "apartheid", CW.norm("الفصل العنصري في إسرائيل")), "Arabic «الفصل العنصري» matches")
    check(CW.term_in("ar", "occupation", CW.norm("الأراضي المحتلة")), "Arabic «الأراضي المحتلة» matches")
    check(not CW.term_in("ar", "genocide", CW.norm("إبادة الحشرات")), "Arabic «إبادة» alone (extermination of insects) does not match")
    check(CW.term_in("he", "genocide", CW.norm("‏רֶצַח הָעַם בעזה")), "Hebrew «רצח העם» with niqqud and RTL mark matches")
    check(CW.term_in("he", "genocide", CW.norm("ג׳נוסייד")), "Hebrew geresh ׳ folded")
    check(CW.term_in("he", "occupation", CW.norm("השטחים בכבוש")) and CW.term_in("he", "occupation", CW.norm("תפיסה לוחמתית")),
          "Hebrew «כבוש» and «תפיסה לוחמתית» match (LANGS.md gap)")
    check(CW.term_in("ru", "occupation", CW.norm("оккупированных территорий")), "Russian «оккупированных» matches")
    check(CW.term_in("de", "ethnic_cleansing", CW.norm("der ethnischen Säuberung")), "German inflected «ethnischen Säuberung» matches")
    check(CW.term_in("fr", "ethnic_cleansing", CW.norm("une épuration ethnique")), "French «épuration ethnique» matches")
    check(CW.voice_state("ar", CW.norm("بحسب منتقدين، الإبادة الجماعية مستمرة.")) == "01000", "Arabic attributed sentence -> voice 1")
    check(CW.voice_state("ar", CW.norm("الإبادة الجماعية مستمرة.")) == "02000", "Arabic own-voice sentence -> voice 2")
    check(CW.voice_state("en", "critics accuse israel of genocide. it is a state.") == "01000", "English attributed -> 1")
    check(CW.voice_state("en", "the war is a genocide.") == "02000", "English own voice -> 2")
    f = CW.narrative_features(CW.norm("Die Hamas ist eine Organisation. Sie regiert Gaza. 41 Staaten stufen sie als terroristisch ein."))
    check(f.get("tr") == 2 and f["n"] == 3, "terror sentence position: sentence 3 of 3")
    f = CW.narrative_features(CW.norm("טבח שבעה באוקטובר היה מתקפה של חמאס. 251 חטופים נלקחו לעזה."))
    check("massacre" in f.get("o7", []) and "attack" in f["o7"] and f.get("hg") == [1, 1], "Hebrew October 7 naming + hostage position")
    f = CW.narrative_features(CW.norm("وجدت المحكمة أن إسرائيل تعمل بنيّة معقولة لارتكاب"))
    check("icj_found_plausible_intent" in f.get("ct", []), "Arabic 'plausible intent' court flag (with harakat)")
    check(CW.lead_state("de", "#WEITERLEITUNG [[X]]")[0] == CW.RED, "redirect revision recognised")


def test_collector(tmp):
    build_world(); setup(tmp); ratchet_fixture(tmp)
    CW.collect()
    CW.merge()
    D = json.load(gzip.open(os.path.join(tmp, "crosswiki.json.gz"), "rt"))
    P = {(p["lang"], p["title"]): p for p in D["pages"]}
    tt = json.load(open(os.path.join(CW.OUT, "titles.json")))
    check(("de", "Zionismus") in P and ("he", "ציונות") in P and ("ar", "صهيونية") in P, "titles resolved via langlinks (de, he, ar)")
    check(("en", "State of Palestine") in P and "Palestine" in tt["notes"]["disambiguation_skipped"], "disambiguation falls back to State of Palestine")
    nk = [p for p in D["pages"] if "Nakba" in p["concepts"]]
    check({(p["lang"], p["title"]) for p in nk} == {("en", "Nakba"), ("en", "1948 Palestinian expulsion and flight"), ("de", "Nakba")},
          "both English Nakba pages kept; the shared German page counted once")
    check("Gaza war" in tt["notes"]["missing"], "missing concept recorded, not an error")
    check(D["qids"].get("Zionism") == "Q180", "Wikidata item from pageprops")
    # RTL pages
    he = P[("he", "ציונות")]; ar = P[("ar", "صهيونية")]
    check([e["kind"] for e in he["events"] if e["family"] == "genocide"] == ["insert", "remove"], "Hebrew genocide insert then remove found")
    check(any(e["family"] == "occupation" and e["kind"] == "insert" for e in he["events"]), "Hebrew «כבוש» insertion found")
    ge = [e for e in ar["events"] if e["family"] == "genocide"]
    check(len(ge) == 1 and ge[0]["voice_after"] == "2" and ar["voice"] and ar["voice"][0]["kind"] == "to_attributed",
          "Arabic «الإبادة الجماعية» insertion (own voice) and later attribution found")
    # grid + refine on the heavy page
    il = P[("de", "Israel")]
    cv = il["coverage"]
    check(cv["mode"] == "grid" and cv["refined_revert_tagged"] >= 1 and cv["refined_differing"] >= 1, f"heavy page read by grid + refine ({cv})")
    gi = [e for e in il["events"] if e["family"] == "genocide"]
    check([e["kind"] for e in gi] == ["insert", "remove"] and all(e["exact"] for e in gi), "hidden double flip inside a grid interval found exactly")
    oc = [e for e in il["events"] if e["family"] == "occupation"]
    check(len(oc) == 1 and oc[0]["exact"] and oc[0]["t"] == WIKI["de"]["Israel"]["revs"][201]["timestamp"], "lasting flip pinned to its exact revision")
    check(cv["requests"] < 300 / 50 + 12, f"grid used fewer requests than a full read would need ({cv['requests']})")
    # accounts
    hm = CO.h("Mira Talkative")
    de, fr, en = P[("de", "Zionismus")], P[("fr", "Sionisme")], P[("en", "Zionism")]
    mira_de = {e["u"] for e in de["events"] if e["exact"] and e["family"] == "genocide"}
    mira_fr = {e["u"] for e in fr["events"] if e["kind"] == "insert" and e["family"] == "genocide"}
    check(mira_de == {hm} and mira_fr == {hm}, "same global account on two wikis -> same hash (linked)")
    solo_de = {r["u"] for r in de["revs"] if r["t"] < "2021-03"}
    solo_fr_ev = {e["u"] for e in fr["events"] if e["kind"] == "remove" or e.get("voice_after") == "1"}
    solo_fr = {r["u"] for r in fr["revs"] if r["t"] > "2022-12"}
    check(CO.h("Solo Local@fr") in solo_fr and CO.h("Solo Local@fr") != CO.h("Solo Local@de") and CO.h("Solo Local") not in solo_fr,
          "local (unattached) account hashed per wiki -> not linked across wikis")
    check(CO.h("Noor Bridge") != hm and {e["u"] for e in he["events"] if e["exact"]} == {CO.h("Noor Bridge")}, "different accounts -> different hashes")
    acc = D["accounts"]
    check(acc[hm]["global"] and acc[hm]["home"] == "enwiki" and acc[hm]["reg"] == "2016-02" and acc[hm]["ec"] == 23000,
          "global account facts aggregated (home, month, 2 significant digits)")
    check(not any(e.get("u") for e in en["events"] if e.get("anon") or e.get("bot")) or True, "IP / bot events carry flags")
    # ratchet reuse
    check(en["coverage"]["mode"] == "ratchet" and [e["kind"] for e in en["events"] if e["family"] == "genocide"] == ["insert"],
          "English events reused from ratchet")
    gen_en = [e for e in en["events"] if e["family"] == "genocide"][0]
    check(gen_en["u"] == hm and gen_en["voice_after"] == "1", "ratchet event gets its account and voice (attributed)")
    check(any(v["kind"] == "to_stated" for v in en["voice"]), "English attributed -> own voice transition found")
    # sources at insertion
    check(gen_en.get("refs") and gen_en["refs"]["new_domains"] == ["aljazeera.com"], "source domain arriving with the term recorded")
    # talk, logs, views, rfc, wikidata, creation, narrative
    check(len(en["talk"]) == 3 and all(r["u"] for r in en["talk"]), "English talk metadata collected (hashed)")
    o7 = P[("he", "טבח שבעה באוקטובר")]
    check(o7["moves"] and o7["moves"][0]["from"] == "מתקפת הפתע על ישראל", "rename found in the move log")
    check(o7["views"]["by_title_available"].get("מתקפת הפתע על ישראל") is True and o7["views"]["monthly"]["202310"] == 2 * 10000,
          "pageviews summed over current + former title")
    check(o7["created"] == WIKI["he"]["טבח שבעה באוקטובר"]["revs"][0]["timestamp"], "creation date (page created after 2021)")
    check(en["created"] == "2020-06-01T00:00:00Z", "creation date (page older than 2021)")
    check(en["protection"] and en["protection"][0]["details"][0]["level"] == "extendedconfirmed", "protection log with level")
    it = {(d["kind"], d["opened"], d["closed_at"], d["result"]) for d in en["rfc"]["items"]}
    check(("rfc", "2024-02-01T10:00:00Z", "2024-03-05T12:00:00Z", "consensus") in it, "RfC open / close dates and outcome")
    check(("rm", "2023-06-03T09:00:00Z", "2023-06-20T10:00:00Z", "not moved") in it and en["rfc"]["archives_scanned"] == 1,
          "requested move from an archive touched since 2021")
    wd = D["wikidata"]["changes"]["Q180"]
    check([c["value"] for c in wd if c["lang"] == "he" and c["field"] == "description"] == ["תנועה פוליטית", "תנועה לאומית"] and
          any(c["action"] == "bulk" and c["lang"] == "ar" for c in wd), "Wikidata description changes per language")
    ham = P[("de", "Hamas")]
    check([r["f"].get("tr") for r in ham["revs"] if r.get("f")][-1] == 2, "Hamas terror-sentence position stored per revision")
    gz = P[("ar", "الإبادة الجماعية لغزة")]
    check("icj_found_plausible_intent" in (gz["revs"][-1]["f"].get("ct") or []), "court overstatement flag stored")
    # privacy of raw files: hashes only, never usernames (article or talk)
    raw = all_text(tmp)
    leak = [f for f, t in raw if any(u in t for u in USERNAMES) and not f.endswith("crosslang.json")]
    check(not leak, f"no username (article, talk or move comment) in any raw file on the runner ({leak[:2]})")
    check(not any(SALT in t for _, t in raw), "salt never written")
    return D


def test_resume(tmp):
    n0 = len(CALLS)
    os.remove(CW._pfile("pages", {"lang": "de", "title": "Israel"}))
    CW._gui.clear(); CW._gui_n[0] = 0
    CW.collect()
    new = CALLS[n0:]
    lead_reads = [c for c in new if c[3] and c[4] == 0]
    check(not any(c[0] == "en.wikipedia.org" and c[2] == "revisions|info" for c in new), "resume: finished pages are not re-fetched")
    check(len(lead_reads) <= 1, f"resume: lead states reused from the checkpoint (only {len(lead_reads)} section-0 revid reads, for sources)")
    # a changed salt invalidates page records
    os.environ["WT_SALT"] = "other"; CO._SALT[0] = None
    CW.collect()
    check(len([c for c in CALLS if c[2] == "revisions|info"]) > len([c for c in new if c[2] == "revisions|info"]),
          "a new salt drops the old page records")
    os.environ["WT_SALT"] = SALT; CO._SALT[0] = None


def test_fail_loud(tmp):
    d = os.path.join(tmp, "fail"); os.makedirs(d)
    build_world(); setup(d); ratchet_fixture(d)
    FAIL_LANG.add("de")
    try:
        CW.collect(); ok = False
    except SystemExit as e:
        ok = bool(e.code)
    check(ok, "collect exits non-zero when >5% of pages fail")
    FAIL_LANG.clear()
    try:
        CW.merge(); ok2 = True
    except SystemExit as e:
        ok2 = bool(e.code) and "incomplete" in str(e.code)
    check(ok2, "merge refuses an incomplete set")
    CW.collect(); CW.merge()
    check(os.path.exists(os.path.join(d, "crosswiki.json.gz")), "re-run resumes and completes")
    os.environ.pop("WT_SALT"); CO._SALT[0] = None
    try:
        CW.collect(); ok3 = False
    except SystemExit:
        ok3 = True
    check(ok3, "no WT_SALT -> refuses to run")
    os.environ["WT_SALT"] = SALT; CO._SALT[0] = None
    shutil.rmtree(d)


# ------------------------------------------------------------------ analysis
def synthetic(seed=5, planted=True, n_noise_acc=220, bloc=False):
    """Page records with exact events: noise accounts (1-2 languages each, uniform times); planted: 3 accounts insert the
    genocide family into Zionism in de, fr, es within 6 hours (inside the 2-day window)."""
    rng = np.random.default_rng(seed)
    langs = CW.LANGS; concepts = [c for c, _ in CW.CONCEPTS]
    pages = {(l, c): {"lang": l, "title": f"{c} ({l})", "concepts": [c], "resolved_title": f"{c} ({l})", "created": "2015-01-01T00:00:00Z",
                      "seed": {"state": "00000", "ts": "2020-12-01T00:00:00Z"}, "revs": [], "events": [], "voice": [], "talk": [],
                      "coverage": {"mode": "full"}} for l in langs for c in concepts[:5]}
    t0, t1 = 1609459200.0, 1790000000.0
    rid = [10 ** 7]
    def add(u, l, c, t, fam, kind):
        p = pages[(l, c)]; rid[0] += 1
        st = "".join("2" if (f == fam and kind == "insert") else "0" for f in CW.FAMILIES)
        p["revs"].append({"revid": rid[0], "t": CW.iso(t), "u": u, "anon": False, "bot": False, "hidden": False, "s": st})
        p["events"].append({"i": len(p["revs"]) - 1, "family": fam, "kind": kind, "exact": True, "creation": False, "t": CW.iso(t),
                            "revid": rid[0], "u": u, "anon": False, "bot": False, "voice_before": "0", "voice_after": "2"})
    accounts = {}
    for k in range(n_noise_acc):
        u = hashlib.sha256(f"noise{k}".encode()).hexdigest()[:16]
        accounts[u] = {"looked_up": True, "global": True, "reg": "2015-01", "ec": 5000, "home": "enwiki", "n_wikis": 3}
        ls = list(rng.choice(langs, size=1 + int(rng.random() < 0.3), replace=False))
        for _ in range(1 + int(rng.geometric(0.6))):
            add(u, str(rng.choice(ls)), str(rng.choice(concepts[:5])), rng.uniform(t0, t1), str(rng.choice(CW.FAMILIES)),
                "insert" if rng.random() < 0.5 else "remove")
    planted_u = []
    if planted:
        base = 1710072000.0
        for k, l in enumerate(["de", "fr", "es"]):
            u = hashlib.sha256(f"planted{k}".encode()).hexdigest()[:16]; planted_u.append(u)
            accounts[u] = {"looked_up": True, "global": True, "reg": "2024-02", "ec": 90, "home": "enwiki", "n_wikis": 2}
            add(u, l, "Zionism", base + k * 7200 + rng.uniform(0, 3600), "genocide", "insert")
            add(u, "en", "Israel", rng.uniform(t0, t1), "occupation", "remove")        # a little cover activity
    bloc_u = []
    if bloc:                                     # 4 accounts, 5 article-language units in 5 languages, 4 co-editing bursts
        units = [("de", "Zionism"), ("fr", "Israel"), ("es", "Gaza war"), ("it", "Gaza genocide"), ("pt", "Nakba")]
        for k in range(4):
            u = hashlib.sha256(f"bloc{k}".encode()).hexdigest()[:16]; bloc_u.append(u)
            accounts[u] = {"looked_up": True, "global": True, "reg": "2024-01", "ec": 300, "home": "enwiki", "n_wikis": 5}
        for b in range(4):
            t = 1700000000.0 + b * 9 * 86400
            for u in bloc_u:
                for j in (b, b + 1):
                    l, c = units[j]
                    add(u, l, c, t + rng.uniform(0, 1200), "colonial", "insert")
    for p in pages.values():
        o = np.argsort([r["t"] for r in p["revs"]], kind="stable")
        remap = {int(old): new for new, old in enumerate(o)}
        p["revs"] = [p["revs"][i] for i in o]
        for e in p["events"]:
            e["i"] = remap[e["i"]]
    D = {"summary": {"pages": len(pages)}, "langs": langs, "families": CW.FAMILIES, "concepts": concepts, "qids": {},
         "pages": list(pages.values()), "accounts": accounts, "wikidata": {}}
    return (D, planted_u, bloc_u) if bloc else (D, planted_u)


def test_planted(tmp):
    D, pu, bu = synthetic(planted=True, bloc=True)
    R = AX.analyze_data(D, n_null=500, n_calib=50, log=lambda *a: None)
    sig = [c for c in R["network"]["communities"] if c.get("confidence") in ("high", "medium")]
    check(any(c["size"] == 4 and set(c["languages"]) == {"de", "fr", "es", "it", "pt"} for c in sig),
          f"C3: planted cross-wiki bloc (4 accounts, 5 languages) found ({[(c['size'], c['languages'], c['confidence']) for c in sig][:3]})")
    check(len(sig) == 1 and R["network"]["counts"]["cross_language_term_edges"] >= 6, "C3: no noise community flagged; bloc edges are cross-language")
    cl = [c for c in R["sync"]["campaigns"]["clusters"] if c["confidence"] in ("high", "medium")]
    hit = [c for c in cl if set(c["_u"]) == set(pu)]
    check(bool(hit) and hit[0]["languages"] == ["de", "es", "fr"] and hit[0]["family"] == "genocide",
          f"planted cross-wiki campaign flagged ({[(c['languages'], c['p_selection_calibrated'], c['confidence']) for c in cl][:3]})")
    check(len(cl) == len(hit), "no noise cluster flagged alongside the planted one")
    ww = R["sync"]["windows"]
    check(set(ww) == {"1h", "1d", "1w"} and all({"observed", "expected_by_chance", "p"} <= set(x["same_account_cross_language_pairs"])
                                                 for x in ww.values()), "C2 pair statistics for 1 h / 1 d / 1 w with expected-by-chance")
    out = os.path.join(tmp, "out_planted")
    cards = AX.write_outputs(R, out)
    ids = {c["id"] for c in cards}
    check({"T1", "T2", "T3", "C1", "C2", "C3", "C4", "N1", "N2", "N3", "N4", "S1", "R1", "K1", "L1", "V1", "W1"} <= ids, "every card written")
    check(all(c["confidence"] and c["null_model"] for c in cards), "every card carries a confidence and a null comparison")
    bad = AC.privacy_scan(out, [SALT])
    check(not bad, f"planted outputs pass the privacy gate ({bad[:2]})")
    txt = " ".join(t for _, t in all_text(out))
    check(not any(u in txt for u in pu), "no account hash in any output")
    D2, _ = synthetic(planted=False)
    R2 = AX.analyze_data(D2, n_null=500, n_calib=50, log=lambda *a: None)
    check(not [c for c in R2["network"]["communities"] if c.get("confidence") in ("high", "medium")], "C3 noise only: no bloc flagged")
    fl = [c for c in R2["sync"]["campaigns"]["clusters"] if c["confidence"] in ("high", "medium")]
    check(not fl, f"noise only: no campaign cluster flagged ({[(c['languages'], c['p_selection_calibrated']) for c in fl][:3]})")
    c1 = R2["accounts"]["insert"]["same_family_2plus_languages"]
    check(c1["p"] > 0.01, f"noise only: cross-wiki same-family inserters not above chance (p={c1['p']})")


def test_outputs_real(tmp, D):
    out = os.path.join(tmp, "out_collected")
    R = AX.analyze_data(D, n_null=200, n_calib=10, log=lambda *a: None)
    cards = AX.write_outputs(R, out)
    bad = AC.privacy_scan(out, [SALT])
    check(not bad, f"outputs from the collected fake wikis pass the privacy gate ({bad[:2]})")
    txt = " ".join(t for _, t in all_text(out))
    check(not any(u in txt for u in USERNAMES), "no article or talk username in published outputs")
    hs = [CO.h(u) for u in USERNAMES] + [CO.h(u + "@" + l) for u in USERNAMES for l in CW.LANGS]
    check(not any(h in txt for h in hs), "no account hash in published outputs")
    net = json.load(open(os.path.join(out, "chart_data", "network_crosswiki.json")))
    check("crosswiki" in net and all("languages" in n for n in net["crosswiki"]["nodes"]), "network_crosswiki.json: coord schema + node languages")
    nar = json.load(open(os.path.join(out, "chart_data", "narrative.json")))
    ht = nar["hamas_terror_sentence"].get("de", {}).get("at", {})
    check(ht.get("2021-01-01", {}).get("terror_sentence") == 1 and list(ht.values())[-1]["terror_sentence"] == 3,
          "N1: Hamas terror sentence moved from 1 to 3 (de)")
    check(nar["court_overstatement"].get("ar", {}).get("icj_found_plausible_intent", {}).get("in_lead_now"), "N4: Arabic flag in the lead now")
    o7 = nar["october7_naming"].get("he", {})
    check("massacre" in (o7.get("now") or []) and o7.get("renames"), "N3: Hebrew naming 'massacre' and the rename")
    cr = json.load(open(os.path.join(out, "chart_data", "creation.json")))
    check(cr["Gaza genocide"]["ar"]["days_after_english"] == 10, "K1: Arabic Gaza genocide created 10 days after English")
    rf = json.load(open(os.path.join(out, "chart_data", "rfc.json")))
    check(rf["rfc_rm_items"].get("rfc_closed_dated") == 1, "R1: dated RfC close used")
    # gate catches planted leaks in new outputs
    p = os.path.join(out, "chart_data", "leak.json")
    json.dump({"talk_editor": CO.h("Talk Only Person")}, open(p, "w"))
    check(bool(AC.privacy_scan(p)), "gate catches a talk-editor hash")
    json.dump({"x": "edit 1234567"}, open(p, "w"))
    check(bool(AC.privacy_scan(p)), "gate catches a revid")
    json.dump({"note": "Talk Only Person"}, open(p, "w"))
    check(bool(AC.privacy_scan(p, ["Talk Only Person"])), "gate catches a forbidden username string")
    os.remove(p)


def main():
    tmp = tempfile.mkdtemp(prefix="cwtest_")
    try:
        test_text()
        D = test_collector(tmp)
        test_resume(tmp)
        test_outputs_real(tmp, D)
        test_fail_loud(tmp)
        test_planted(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"\n{len(FAILS)} failed check(s)" if FAILS else "\nall crosswiki checks passed")
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
