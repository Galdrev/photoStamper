"""Build the flash edition of the report.

Usage: python build_flash.py OUT.html              (English)
       python build_flash.py --lang he OUT.html    (Hebrew: flash_he.py, strings in flash_i18n_he.json; the English
                                                    page is built and checked first, in memory)
       python build_flash.py --bilingual OUT.html  (ONE page, English and Hebrew, with a עברית / English switch: flash_bi.py;
                                                    both pages are built and checked as above, then packed together)

The flash edition is a separate page (page_flash_template.html) on the research edition's data, design and chart code:
  * the research build (build_page.py) runs first, unchanged, with all its assertions; its output goes to a temporary file
    and is thrown away, and its in-memory data (res) is reused here. No data logic is duplicated.
  * the research edition's CSS and its JS library (helpers, word diff and focus catchers, tooltips, #kChart, #o7Fig and
    #ziFig data functions, #xwGG) are copied from page_template.html at build time, so a design change there reaches
    both editions.
  * R is a slice of the research data: only what the flash cards draw.
Accuracy checks (the build fails on any of them): every curly-quoted string must be a substring of the stored text it
names (data-q="en:Title", "he:Title", "ar:…", "es:…", "arb" for the ArbCom extract; quotes outside a data-q element are
checked against all stored texts); every number must appear in the research edition's template; the messaging vetoes
(patterns/flash/messaging_check.md) and the no-names rule are asserted.
"""
import contextlib, gzip, html as _html, io, json, os, re, runpy, sys, tempfile
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
PAT = os.path.join(HERE, "patterns")
RESEARCH_URL = "https://claude.ai/artifact/6NCLCkohWsfvKwz9MtCTPv"
LANG = "en"
if "--bilingual" in sys.argv:
    sys.argv.remove("--bilingual")
    LANG = "bi"
if "--lang" in sys.argv:
    _i = sys.argv.index("--lang")
    LANG = sys.argv[_i + 1]
    del sys.argv[_i:_i + 2]
    assert LANG in ("en", "he"), f"unknown --lang {LANG}"

# 1. the research build, unchanged (all its assertions run); keep its data
_tmp = tempfile.NamedTemporaryFile(suffix=".html", delete=False).name
_argv = sys.argv
sys.argv = [os.path.join(HERE, "build_page.py"), _tmp]
_log = io.StringIO()
try:
    with contextlib.redirect_stdout(_log):
        G = runpy.run_path(os.path.join(HERE, "build_page.py"), run_name="build_page")
finally:
    sys.argv = _argv
    os.path.exists(_tmp) and os.remove(_tmp)
print("research build: " + " | ".join(l for l in _log.getvalue().splitlines() if l.startswith(("K_STEPS", "#against", "ArbCom", "wrote"))))
res = G["res"]

# 2. the research edition's CSS and JS library
rtpl = open(os.path.join(HERE, "page_template.html")).read()
css = rtpl[rtpl.index("<style>") + len("<style>"):rtpl.index("</style>")].replace("/*LABCSS*/", "")
js0 = rtpl.index("<script>\nconst R=/*DATA*/null;") + len("<script>\n")
lib = rtpl[js0:rtpl.index("/* ---------- init ---------- */", js0)]
assert lib.startswith("const R=/*DATA*/null;") and "function drawKey(" in lib and "function o7Data(" in lib and "function tnApply(" in lib
# v2.1, no-courts rule: the language-grid legend, call-out and state words drop the court-case symbol and label (flash copy only)
for a, b in (('<span class="key">${xTile("legal","")}§: reported only as a court case</span>', ""),
             ('["legal","court case only"],', ""),
             ('${fa.length&&he?"; ":""}${he?"he → court case only":""}', ""),
             (' (for example, moved later in the section, or now reported as a court case)', ' (for example, moved later in the section)'),
             ('A:"attributed, disputed or a court case"', 'A:"attributed or disputed"'),
             # the grid's coding note names only the five flash columns and drops the court-ruling pointer
             (" Whether an edition overstates a court ruling is in the evidence room, with its sentences.", ""),
             ("Genocide, colonization, apartheid, occupation and the Hamas label", "Genocide, colonization, apartheid and the Hamas label"),
             ("The October 7 and hostages columns are our reading", "The October 7 column is our reading")):
    assert lib.count(a) == 1, f"no-courts patch target changed in page_template.html: {a[:50]}"
    lib = lib.replace(a, b)

# 3. the data slice
ARTS = ["Zionism", "Hamas", "October 7 attacks", "Gaza genocide"]
# v2: the language grid (#xmFig) shows five claims; the court column and the court moments stay in the research edition
XM_COLS = ["gen", "col", "apa", "o7", "ter"]
_L = res["langs"]
XM_ARTS = sorted({c["a"] for k in XM_COLS for c in _L["cells"][k].values() if c and c.get("a")})
_arts = {}
for a in XM_ARTS:
    _arts[a] = {}
    for l, A in _L["arts"][a].items():
        A = dict(A, sl={s: v for s, v in A["sl"].items() if s != "k_icj"})
        _arts[a][l] = A
LANGS_R = {
    "order": _L["order"], "voice": _L["voice"], "missing": {a: v for a, v in _L["missing"].items() if a in _arts},
    "cols": [c for c in _L["cols"] if c[0] in XM_COLS], "cells": {k: _L["cells"][k] for k in XM_COLS}, "arts": _arts,
    "moments": [m for m in _L["moments"] if m[0] in _arts and m[1] in _arts[m[0]] and m[2] in _arts[m[0]][m[1]]["sl"]],
}
# v2.1, no-courts rule: the legal code ("reported only as a court case") is folded into "attributed" in the flash display
# only (langs.json and the research edition keep it); the moment and cell texts lose the court-case label
def _fold(o):
    if isinstance(o, dict):
        return {k: _fold(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_fold(v) for v in o]
    if o == "legal":
        return "attributed"
    if isinstance(o, str):
        return (o.replace("Hebrew: genocide only as a court case", "Hebrew: the Gaza war article does not state the charge")
                 .replace("the court-case clause is its only genocide mention", "this attributed clause is its only genocide mention"))
    return o
LANGS_R = {k: (v if k == "voice" else _fold(v)) for k, v in LANGS_R.items()}
LANGS_R["voice"] = {k: v for k, v in LANGS_R["voice"].items() if k != "legal"}
_lj = json.dumps(LANGS_R, ensure_ascii=False)
assert '"legal"' not in _lj and "court case" not in _lj.lower() and "court-case" not in _lj.lower(), "the flash grid must not carry the court-case code or label"
R = {
    "zionism": res["zionism"], "oct7": res["oct7"], "v3": res["v3"], "xw": res["xw"],
    "langs": LANGS_R,
    "ratchet": {"articles": {t: res["ratchet"]["articles"][t] for t in ARTS + ["Nakba"]}},
    "articles": [{k: a.get(k) for k in ("title", "pv_monthly", "w_edits")} for a in res["articles"] if a["title"] in ARTS],
    "week0": res.get("week0"), "n_weeks": res.get("n_weeks"),
    "dates": res["dates"],
}
assert len(R["articles"]) == len(ARTS), "a flash article is missing from the research data"
assert [r["date"] for r in R["oct7"]["designation"]][::3] == ["2021-01-01", "2026-10-31"], "Hamas designation rows changed"
# v2 data slices, checked
_d1 = next(r for r in R["oct7"]["designation"] if r["date"] == "2026-10-01")
assert _d1["sentence"] == "22 of 23" and _d1["quote"].startswith("Australia, Canada, ") and _d1["quote"].endswith(
    ", and the European Union have designated Hamas as a terrorist organisation."), "the 1 Oct 2026 Hamas designation row changed"
assert R["dates"][-1] == "2026-10", "dates changed"
assert len(LANGS_R["order"]) == 11, "the language grid has eleven editions (the card says so)"
assert [c[0] for c in LANGS_R["cols"]] == XM_COLS and "icj" not in LANGS_R["cells"], "the court column must stay out"
assert not any(m[2] == "k_icj" for m in LANGS_R["moments"]) and not any(x in (m[3] + m[4]).lower() for m in LANGS_R["moments"] for x in ("did not make", "found israel guilty")), "court moments must stay out"
for a, l, s in (("Gaza genocide", "ar", "s1"), ("Gaza war", "es", "s1"), ("Gaza war", "he", "k_genocide")):
    S = LANGS_R["arts"][a][l]["sl"][s]
    assert S["m"].get("n"), f"morph slide sentence missing: {a} {l} {s}"
    assert (a, l, s) == ("Gaza war", "he", "k_genocide") or S["m"].get("f"), f"morph slide needs a then copy: {a} {l} {s}"
_nk = R["ratchet"]["articles"]["Nakba"]
_nkv = {v["id"]: v.get("s") or "" for v in _nk["fs_variants"]}
_nkl = [_nkv.get(i, "") for _, i, _ in _nk["fs_timeline"]]
for term in ("destruction of Palestinian society", "ethnic cleansing", "by Zionists"):
    assert any(term in s for s in _nkl), f"Nakba lane term not in the stored first sentences: {term}"
assert "by Zionists" in [s for s in _nkl if s][-1], "the Nakba first sentence now says by Zionists"
print(f"flash: R.langs sliced to {len(_arts)} articles, {len(LANGS_R['moments'])} moments, columns {XM_COLS}")

tpl = open(os.path.join(HERE, "page_flash_template.html")).read()


# 4. accuracy checks on the template text
class _Text(HTMLParser):
    """Visible text, bucketed by the nearest data-q source ("" = no source named)."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.buckets, self.skip, self.runs = [], {}, 0, []
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag in ("br", "meta", "link", "input", "img"):
            return
        a = dict(attrs)
        self.stack.append((tag, a.get("data-q"), a.get("dir") == "rtl"))
    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
        while self.stack:
            t = self.stack.pop()[0]
            if t == tag:
                break
    def handle_data(self, d):
        if self.skip:
            return
        q = next((x[1] for x in reversed(self.stack) if x[1]), "")
        self.buckets.setdefault(q, []).append(d)
        if d.strip():
            self.runs.append((d.strip(), any(x[2] for x in self.stack)))


page = _Text()
page.feed(re.sub(r"<!--.*?-->", "", tpl, flags=re.S))
text = {k: "".join(v) for k, v in page.buckets.items()}

norm = lambda t: re.sub(r"\s+", " ", (t or "").replace("’", "'").replace(" ", " "))
M2 = json.load(gzip.open(os.path.join(HERE, "data", "mass2_leads.json.gz")))["leads"]
LJ = json.load(open(os.path.join(HERE, "data", "leads.json")))
RA = json.load(open(os.path.join(HERE, "data", "ratchet.json")))["articles"]
LANGS = json.load(open(os.path.join(PAT, "langs", "langs.json")))["articles"]
ARB = open(os.path.join(PAT, "guard", "arbcom_named.md")).read()


def en_corpus(title):
    T = [x or "" for x in M2.get(title, [])]
    T += [v[k] for v in LJ if v["title"] == title for k in ("lead0", "lead1")]
    T += [v.get("s") or "" for v in (RA.get(title) or {}).get("fs_variants", [])]
    return T


def lang_corpus(lang, title):
    T = []
    for s in ((LANGS.get(title) or {}).get(lang) or {}).get("slots", {}).values():
        for w in ("first", "latest"):
            if s.get(w):
                T += [s[w]["orig"], s[w]["tr"]] + [x.get("gloss", "") for x in s[w].get("terms") or []]
    return T


def corpus(src):
    out = []
    for one in src.split("|"):
        kind, _, title = one.partition(":")
        if kind == "en":
            out += en_corpus(title)
        elif kind == "arb":
            out += [ARB]
        else:
            out += lang_corpus(kind, title)
        assert out, f"no stored text for data-q={one}"
    return [norm(t) for t in out]


ALL = None
def all_corpus():
    global ALL
    if ALL is None:
        T = [x or "" for v in M2.values() for x in v] + [v[k] for v in LJ for k in ("lead0", "lead1")]
        T += [v.get("s") or "" for a in RA.values() for v in a.get("fs_variants", [])]
        T += [t for a in LANGS for l in LANGS[a] for t in lang_corpus(l, a)] + [ARB]
        ALL = "\n".join(norm(t) for t in T)
    return ALL


def quotes(t):
    q = re.findall(r"“([^”]+)”", t)
    q += re.findall(r"‘([^‘’]+)’(?=[\s.,;:)]|$)", t)  # single quotes inside the dinner sentence (apostrophes are ’ only)
    return q


bad, nq = [], 0
for src, t in text.items():
    C = corpus(src) if src else None
    for q in quotes(t):
        for part in re.split(r"…|\.\.\.", q):
            part = norm(part).strip(" ,.;:")
            if len(part) < 3:
                continue
            nq += 1
            ok = any(part in c for c in C) if C is not None else part in all_corpus()
            if not ok:
                bad.append((src or "any", part))
assert not bad, f"flash quotes not found in the stored text: {bad}"
print(f"flash: {nq} quoted strings found in the stored texts")

# numbers: every number on the flash page is already in the research edition's template (story, evidence room or the
# strings its chart code prints). Exceptions, each from the research edition's own code at run time:
COMPUTED = {"13.7": "kStat(), #after step 1 (printed in the research scrolly); the smoke test checks it", "3.8": "kStat(), same line",
            "187": "R.xw.gg, printed by drawXwGG", "849": "R.xw.gg, printed by drawXwGG"}
_gg = {(r[0], r[4]) for r in R["xw"]["gg"]}
assert ("en", 187) in _gg and ("pl", 849) in _gg and ("en", "2024-07-03") in {(r[0], r[3]) for r in R["xw"]["gg"]}, "title-rename days changed"
vis = " ".join(text.values())
# merge r1, item 3: the reach figure. Every number in it is taken from patterns/exposure/exposure.json (daily Wikimedia pageviews,
# run 42651558741) and rebuilt here; the build fails if the page drifts from the file. Views = window views_total; share = the
# critical-wording view share (Gaza genocide: own voice); the surge window is 7 Oct - 31 Dec 2023.
# final round, step 1: Benjamin Netanyahu and Palestine are back (spin_review R3), from the same source (the same workflow and
# endpoint, run 42704500939, the same window); their critical wording is "genocide" in the opening section, Israel's test.
EXP = json.load(open(os.path.join(PAT, "exposure", "exposure.json")))["articles"]
_HERO6 = ["Israel", "Zionism", "Nakba", "October 7 attacks", "Hamas", "Gaza genocide"]
assert sorted(EXP) == sorted(_HERO6 + ["Benjamin Netanyahu", "Palestine"]), f"exposure.json articles: {sorted(EXP)}"
assert all(EXP[a]["rule_text"] == "opening section (section 0)" and EXP[a]["critical"] == ["genocide"] for a in ("Benjamin Netanyahu", "Palestine"))
assert EXP["Palestine"]["titles_views_main"] == {"State of Palestine": "start", "Palestine": "2025-01-07 20:06"}, "Palestine: views of the old title, then of the new one from the move"
_W = {a: EXP[a]["windows"]["last_12_months"] for a in EXP}
assert all(w["from"] == "20251109" and w["to"] == "20261108" for w in _W.values()), "exposure window changed (the page says 9 Nov 2025 - 8 Nov 2026)"
assert "9 Nov 2025 – 8 Nov 2026 (daily sums)" in tpl
_mil = lambda v: f"{v/1e6:.1f}"
_pc = lambda s: "100%" if s == 1 else f"{s*100:.1f}%"
_crit = {a: (_W[a]["view_share"]["own_voice"] if a == "Gaza genocide" else _W[a]["critical"]["view_share"]) for a in _W}
_ord = sorted(_W, key=lambda a: -_W[a]["views_total"])
_mx = _W[_ord[0]]["views_total"]
EXP_NUMS = set()
for a in _ord:
    v = _W[a]["views_total"]
    row = (f'<li><span class="n">{a}</span><span class="t"><span class="b" style="width:{round(100*v/_mx,1)}%"><i style="width:{round(100*_crit[a],1)}%"></i></span></span>'
           f'<span class="v">{_mil(v)} million · <b>{_pc(_crit[a])}</b></span></li>')
    assert row in tpl, f"reach figure row does not match exposure.json: {a}"
    EXP_NUMS |= {_mil(v), _pc(_crit[a]).rstrip("%")}
_sw = {a: EXP[a]["windows"]["surge_7_oct_to_31_dec_2023"] for a in EXP}
assert _ord[0] == "Benjamin Netanyahu" and tpl.count('<ul class="fl-bars fl-exb">') == 1 and tpl[tpl.index('<ul class="fl-bars fl-exb">'):].count("<li>", 0, tpl[tpl.index('<ul class="fl-bars fl-exb">'):].index("</ul>")) == 8, "reach figure: eight bars, Netanyahu (the largest) on top"
assert "Page views of the six articles above and of Benjamin Netanyahu and Palestine, 9 Nov 2025 – 8 Nov 2026 (daily sums)." in tpl
_hx = lambda a: _pc(_W[a]["hero_exact_phrase"]["now"]["view_share"])
for frag in (f'({_hx("Israel")} of Israel’s views met “began committing genocide”, {_hx("Benjamin Netanyahu")} of Netanyahu’s “orchestrating the Gaza genocide”, {_hx("Palestine")} of Palestine’s “recognised as constituting genocide”)',
             f'(the other {_pc(_W["Nakba"]["view_share"]["ec_other"])} met another “ethnic cleansing” wording)',
             f'Israel, {_mil(_sw["Israel"]["views_total"])} million views, {_pc(_sw["Israel"]["softer"]["view_share"])} with no genocide charge',
             f'Hamas, {_mil(_sw["Hamas"]["views_total"])} million, none with “political organisation”)',
             "Page views, not unique readers"):
    assert frag in tpl, f"reach figure text does not match exposure.json: {frag}"
    EXP_NUMS |= set(n.rstrip("%") for n in re.findall(r"\d[\d.]*%?", frag))
assert _sw["Hamas"]["view_share"]["political_org"] == 0, "the surge line says none"
assert sum(1 for a in _ord if _crit[a] >= 0.95) == 7 and _crit["Nakba"] < 0.5, "'nearly every view ... except Nakba' must hold"
COMPUTED["12%"] = "treemap headline, computed from data/mass2.json (asserted below)"
COMPUTED["12"] = COMPUTED["12%"]
for n in EXP_NUMS:
    COMPUTED[n] = "exposure.json (merge r1 reach figure), asserted above"
COMPUTED.update({"2025": "exposure window", "2026": "exposure window"})
print(f"flash: reach figure: {len(_ord)} rows and the surge line match exposure.json")
nums = set(re.findall(r"(?<![\w.])\d[\d,]*(?:\.\d+)?", vis))
missing = sorted(n for n in nums if n not in COMPUTED and not re.search(r"(?<![\d,.])" + re.escape(n) + r"(?![\d])", rtpl))
assert not missing, f"numbers on the flash page that the research edition does not print: {missing}"
print(f"flash: {len(nums)} numbers, all printed by the research edition")

# impact r1: the hero rewrite stack. Six rows in card order; each "now" phrase is in the latest stored copy (5 Nov 2026
# crawl) and each "then" phrase is not; Israel had no "genocide" in its opening in Jan 2021 or Jul 2023; the denial line stays.
RW_ROWS = re.findall(r'<li data-q="en:([^"]+)">.*?<del>(.*?)</del>.*?<ins>(.*?)</ins>', tpl[tpl.index('id="flRw"'):tpl.index('</figure>', tpl.index('id="flRw"'))], flags=re.S)
assert [r[0] for r in RW_ROWS] == ["Israel", "Zionism", "Nakba", "October 7 attacks", "Hamas", "Gaza genocide"], f"hero stack rows changed: {RW_ROWS}"
for title, then, now in RW_ROWS:
    snaps = [norm(x or "") for x in M2[title]]
    nw, th = norm(now).strip("“”"), norm(then).strip("“”")
    assert nw in snaps[-1], f"hero stack: the now phrase is not in the latest {title} copy: {nw}"
    if title == "Israel":
        assert then == "no genocide charge" and not any("genocide" in x.lower() for x in snaps[:2]), "hero stack: Israel then"
    else:
        assert th not in snaps[-1], f"hero stack: the then phrase is still in the latest {title} copy: {th}"
assert "In the Israel article, the next sentence: “Israel has denied that its actions constitute genocide.”" in tpl, "hero stack: the denial line must stay"
# fact check r1: each stack row dates its own phrase ("coordinated armed incursions" since 9 Dec 2023, not the 8 Oct 2026
# full-sentence date); the stack header says "opening lines" because the Israel row is in the opening section
# fact check r2: the Hebrew "terror organisation" is not new (Hebrew said it in 2021), so it gets the neutral mark, never the
# added-word blue; the close heading names the list it heads (most-read gainers of critical vocabulary, research #reach)
assert '<b class="mk">ארגון טרור</b>' in tpl and 'class="tnm"' not in tpl, "Hebrew mirror: neutral mark only"
assert "How many page views met the new wording</h2>" in tpl and "how many people read" not in tpl, "close heading / transition wording"
assert "Other words changed too" in tpl, "#breathe caption must say that other words changed"
assert "23 Oct 2023 → since 9 Dec 2023" in tpl and "Their first lines" not in tpl and "· first lines, then" not in tpl, "hero stack dates or header"
assert 'data-share="flRw"' in tpl and 'data-share="c5vs"' in tpl and "foot:[" in tpl and "scope" in tpl[tpl.index("function shSpec"):], "share cards carry the scope line"
print(f"flash: hero stack, {len(RW_ROWS)} rows, now phrases current and then phrases gone in the 5 Nov 2026 copies")

# impact r2: the two credibility lines (owner decision)
# (1) card 4: "terrorist" left the first sentences of Islamic State, al-Shabaab and Boko Haram; Hamas's 2021 first sentence did not have it.
#     No contrast clause: the research edition's nine-groups comparison shows Hezbollah and PIJ were also reframed as political or
#     paramilitary bodies, so "only Hamas became a political organisation" is not supported and must not appear.
_fs = lambda t: re.split(r"(?<=[a-z\)])\.\s", re.sub(r"\s+", " ", (t or "").strip()), 1)[0].lower()
_isv = {v["id"]: v.get("s") or "" for v in RA["Islamic State"]["fs_variants"]}
_ist = [_isv.get(i, "") for _, i, *_ in RA["Islamic State"]["fs_timeline"]]
assert any("terrorist" in x.lower() for x in _ist) and "terror" not in [x for x in _ist if x][-1].lower(), "Islamic State: terrorist once in, now out of the first sentence"
for _t in ("Al-Shabaab (militant group)", "Boko Haram"):
    _v = next(v for v in LJ if v["title"] == _t)
    assert "terrorist" in _fs(_v["lead0"]) and "terror" not in _fs(_v["lead1"]), f"{_t}: terrorist in the 2021 first sentence, not now"
assert "terror" not in _fs(M2["Hamas"][0]), "Hamas: no terrorist in the 2021 first sentence"
_grp = {g["article"]: g for g in json.load(open(os.path.join(PAT, "angle", "chart_data", "oct7_02_designated_groups.json")))["groups"]}
assert "political" in _grp["Hezbollah"]["now"]["first_sentence"] or "paramilitary" in _grp["Hezbollah"]["now"]["first_sentence"], "Hezbollah reframing check"
assert "Context: in line with Wikipedia-wide style on contentious labels, “terrorist” left the first sentences of Islamic State, al-Shabaab and Boko Haram. Hamas’s first sentence did not have it in 2021." in tpl
assert not re.search(r"no other (group|armed group)|only hamas", low if "low" in dir() else vis.lower()), "no unsupported contrast clause"
# (2) card 5: the killings in Wikipedia's own voice, from the latest stored October 7 copy (2 Nov 2026)
_o7 = norm(M2["October 7 attacks"][-1])
for _q in ("massacring civilians in 21 communities", "at least 1,195 people were killed by the attacks"):
    assert _q in _o7, f"card 5 own-voice quote not in the latest October 7 copy: {_q}"
assert 'id="c5own"' in tpl and tpl.index('id="c5own"') > tpl.index('id="car1"') and tpl.index('id="c5own"') < tpl.index('id="c6"'), "the own-voice line is card 5's last line"
# card 4 mirror: the English definition is the latest stored Hamas first sentence
assert norm("is a Sunni Islamist Palestinian nationalist political organisation with a military wing known as the al-Qassam Brigades") in norm(M2["Hamas"][-1])
# share cards: five, each carrying the scope line (shSpec reads .fl-scope); the saves go through claude.use("downloads") when hosted
for _id in ("flRw", "c3", "c4vs", "c5vs"):
    assert f'data-share="{_id}"' in tpl and f'id==="{_id}"' in tpl, f"share card {_id}"
assert 'window.claude.use("downloads")' in tpl and "window.claude.downloads" not in tpl, "downloads capability via use() only"
print("flash: credibility lines verified (three groups' terrorist removal; October 7 own-voice toll), share cards and downloads wired")

# the messaging check's vetoes and the no-names rule
low = vis.lower()
VETO = ["afterthought", "the world reads first", "64 of", "47 of", "336", "650", "386", "both sides", "in 2021 / before the war",
        "before the war, these first lines", "documented"]
hit = [v for v in VETO if v in low]
assert not hit, f"vetoed wording on the flash page: {hit}"
# spin-risk review (patterns/flash/spin_review.md): the scope line is in both editions, and no talking-point phrasing
SCOPE = "does not assess the conduct of the war or of any government"
assert SCOPE in vis and SCOPE in rtpl, "the scope line must be in both editions"
SPIN = ["the world reads", "israel’s way", "why it matters", "the score.", "israel’s own article"]
_rvis = re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>", " ", rtpl, flags=re.S)).lower()
assert not [v for v in SPIN if v in low or v in _rvis], f"spin-review wording back on a page: {[v for v in SPIN if v in low or v in _rvis]}"
assert "undone within a day" not in low.replace("“colonial” was taken out and put back 10 times from november 2024 to august 2026; each removal was undone within a day", "") \
    .replace("from november 2024 each removal of “colonial” was undone within a day", ""), "\"undone within a day\" outside its Zionism scope"
for who in ("Smallangryplanet", "Aquillion", "Zero0000", "Nableezy", "CaptainEek", "Elli", "AndreJustAndre"):
    assert not re.search(r"\b%s\b" % who, tpl), f"flash page names an account ArbCom did not sanction here: {who}"
assert vis.count("Ïvana") == 1, "the flash names exactly one sanctioned account, once (owner exception, card 7)"
assert all(f'{RESEARCH_URL}#{a}"' in tpl.replace("@@R@@", RESEARCH_URL) for a in
           ("ev-charge", "ev-zionism", "ev-1948", "ev-oct7", "ev-xl", "ev-organised", "o7Fig", "when", "reads", "ziFig"))
for a in ("ev-charge", "ev-zionism", "ev-1948", "ev-oct7", "ev-xl", "ev-organised", "o7Fig", "when", "reads", "ziFig"):
    assert f'id="{a}"' in rtpl, f"evidence anchor not in the research edition: #{a}"
# Hebrew and Arabic: any text run that is mostly Hebrew or Arabic letters sits inside a dir="rtl" element
rtl_bad = [t[:40] for t, rtl in page.runs if not rtl and
           len(re.findall(r"[\u0590-\u05FF\u0600-\u06FF]", t)) > 0.5 * max(1, len(re.findall(r"[^\W\d_]", t)))]
assert not rtl_bad, f"Hebrew or Arabic text without dir=rtl: {rtl_bad}"
print(f"flash: {sum(1 for t, r in page.runs if r)} right-to-left runs, all inside dir=rtl")

# 4b. quoted words that the flash's own script draws (lane labels, tooltip heads): each must be stored text of its article
fjs = tpl[tpl.index("/* ---------- flash edition ---------- */"):]
JSQ = {"Zionism": ["colonial", "colonization", "re-establishment"], "Hamas": ["militant", "terrorist", "political organisation with a (military) wing"],
       "October 7 attacks": ["armed incursions", "massacre"], "Nakba": ["the destruction of Palestinian society", "ethnic cleansing", "by Zionists"]}
for art, terms in JSQ.items():
    C = corpus("en:" + art)
    for t in terms:
        probe = t.replace("(military) ", "military ") if "(military)" in t else t
        assert "“" + t + "”" in fjs or "“" + t.capitalize() + "”" in fjs, f"flash script no longer quotes {t}"
        assert any(probe.lower() in c.lower() for c in C), f"script quote not in the stored {art} text: {t}"
# merge r1: the fight-lane gloss "land outside" + "(of) Europe" holds for every stored Zionism wording that has the phrase; the longer
# phrase "a land outside of Europe" does not hold for every lane interval (some wordings say "a land outside Europe"), so the label stays short
_zv = [norm(v.get("s") or "") for v in RA["Zionism"]["fs_variants"]]
_lo = [s for s in _zv if "land outside" in s.lower()]
assert _lo and all(re.search(r"land outside (of )?Europe", s, re.I) for s in _lo), "fight-lane gloss: every 'land outside' wording continues '(of) Europe'"
assert any("land outside Europe" in s for s in _lo) and any("land outside of Europe" in s for s in _lo), "both 'outside Europe' and 'outside of Europe' occur (so the long label would not hold)"
assert 'const FB_GL={"land outside":{g:"(of) Europe",re:/land outside (of )?Europe/i}};' in tpl
_jsq = {q for q in re.findall(r"“([^”]+)”", fjs) if not re.search(r'[$"|+]', q)}  # skip code that builds quote marks
_jsq -= {x for v in JSQ.values() for x in v} | {t.capitalize() for v in JSQ.values() for t in v}
assert not _jsq, f"an unchecked quote in the flash script: {_jsq}"

# 4c. the research edition's interactives, sliced from page_template.html by id (outer HTML, balanced tags)
def cut(rid):
    m = re.search(r'<(figure|section)\b[^>]*\bid="%s"' % re.escape(rid), rtpl)
    assert m, f"research markup not found: #{rid}"
    tag, i, depth = m.group(1), m.start(), 0
    for t in re.finditer(r"<(/?)%s\b[^>]*>" % tag, rtpl[i:]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return rtpl[i:i + t.end()]
    raise AssertionError(f"unbalanced #{rid}")
SLOTS = {k: cut(k) for k in ("breathe", "xmFig", "ziFig", "o7Fig", "xrFig")}
for k in SLOTS:
    assert tpl.count(f"<!--R:{k}-->") == 1, f"slot for #{k} missing in the flash template"
assert "xmIcj" not in "".join(SLOTS.values()) and "Court ruling" not in "".join(SLOTS.values()), "the court grid stays out of the flash"
_vis_courts = re.sub(r"<[^>]+>", " ", SLOTS["xmFig"]).lower()
assert "court" not in _vis_courts, "the sliced language grid must not mention courts"
assert not any(x in lib for x in ("reported only as a court case", '["legal","court case only"]', "he → court case only", "or a court case\"", "overstates a court ruling")), \
    "the flash language-grid legend must not carry the court-case symbol or label"
_sl = _Text()
_sl.feed(re.sub(r"<!--.*?-->", "", "".join(SLOTS.values())))
slow = " ".join("".join(v) for v in _sl.buckets.values()).lower()
assert not [v for v in VETO if v in slow], "vetoed wording in a sliced research figure"
for who in ("Smallangryplanet", "Aquillion", "Zero0000", "Nableezy", "CaptainEek", "Elli", "AndreJustAndre", "Ïvana"):
    assert who.lower() not in slow, f"a sliced research figure names an account: {who}"
print("flash: research interactives sliced: " + ", ".join(f"#{k} ({len(v)//1000} kB)" for k, v in SLOTS.items()))

# merge r1, item 4: the treemap of the 150 most-read opening sections (patterns/angle/PERP.md: the 150 most-viewed topic-group
# articles of the mass crawl, views summed Jan 2021 - Oct 2026, with a lead at all three dates). Tile area = views in the last 12
# stored months (Nov 2025 - Oct 2026, data/mass2.json monthly user views; exposure.json has daily views for the six hero articles
# only, so the treemap uses the crawl's monthly sums and says so). The charge per tile comes from patterns/angle/perp_codes.jsonl:
# a sentence that charges Israel with genocide (clause perpetrator I, charge G), own voice or attributed, never the denial.
_MS = json.load(open(os.path.join(HERE, "data", "mass2.json")))
_mon = lambda a: ((a.get("pageviews") or {}).get("monthly") or {})
_tot = lambda a: sum(x or 0 for x in (_mon(a).get("views") or []))
_set = [a for a in _MS["articles"] if a["group"] == "topic" and a["title"] in M2 and len(M2[a["title"]]) >= 3 and all(M2[a["title"]][i] for i in range(3))]
_set = sorted(_set, key=lambda a: -_tot(a))[:150]
assert len(_set) == 150 and _mon(_set[0])["start"] == "202101" and len(_mon(_set[0])["views"]) == 70, "treemap: 150 articles, monthly views Jan 2021 - Oct 2026"
assert _tot(next(a for a in _set if a["title"] == "Israel")) == 42920851, "treemap set: Israel's views since 2021 as in PERP.md (42.9M)"
_PC = [json.loads(l) for l in open(os.path.join(PAT, "angle", "perp_codes.jsonl"))]
assert {r["title"] for r in _PC if r["group"] == "topic"} <= {a["title"] for a in _set}, "treemap set = the coded 150"
_ch = {}
for r in _PC:
    if r["group"] != "topic":
        continue
    for c in r["clauses"]:
        for g in c["charges"]:
            if c["perp_code"] == "I" and g["code"] == "G" and g["voice"] != "denied_or_disputed":
                assert r["date"] == "now", f"a genocide charge against Israel before the war: {r['title']} {r['date']}"
                v = 2 if g["voice"] == "wikipedia_voice" else 1
                if v > _ch.get(r["title"], (0,))[0]:
                    _ch[r["title"]] = (v, r["text"])
assert len(_ch) == 7 and sorted(k for k, v in _ch.items() if v[0] == 2) == ["Benjamin Netanyahu", "Israel"], f"treemap: 7 charged, 2 as fact: {_ch}"
for k, (v, s) in _ch.items():
    assert norm(s) in norm(M2[k][2]), f"treemap: the charge sentence is not in the stored {k} lead"
_l12 = lambda a: sum(_mon(a)["views"][-12:])
TM_ROWS = sorted([[a["title"], _l12(a), _ch.get(a["title"], (0, ""))[0], _ch.get(a["title"], (0, ""))[1]] for a in _set], key=lambda r: -r[1])
_share = sum(r[1] for r in TM_ROWS if r[2]) / sum(r[1] for r in TM_ROWS)
assert f"<b>Now 7 of 150 do</b>, two as fact, and they got <b>{round(100*_share)}%</b> of the views of all 150 (Nov 2025 – Oct 2026)." in tpl, f"treemap headline: {_share:.4f}"
R["tm"] = {"rows": TM_ROWS}
for _k, (_v, _s) in _ch.items():  # numbers inside the seven quoted charge sentences (tile tooltips; the Hebrew overlay translates them)
    for _n in re.findall(r"(?<![\w.])\d[\d,]*(?:\.\d+)?", _s):
        COMPUTED[_n] = f"inside the quoted {_k} charge sentence (treemap tooltip)"
print(f"flash: treemap: 150 openings, 7 with the charge ({sum(r[2]==2 for r in TM_ROWS)} as fact) get {100*_share:.1f}% of their views, Nov 2025 - Oct 2026")

# final round, step 5 (patterns/flash/FACTCHECK_merge.md): the numbers the page computes at run time, recomputed here from the same
# stored data, so a data change cannot move them unseen. (1) The fight lanes (#flFb, the page's fbBuild): 100 fought-over words since
# Jan 2021 in the Zionism first sentence, and the 8 lanes with their change counts. (2) The treemap share, to the decimal (12.4%).
def _fb_recount(RA):
    vt = {v["id"]: v["s"] for v in RA["fs_variants"]}
    ev = sorted(((x[0], vt.get(x[1])) for x in RA["fs_timeline"]), key=lambda e: e[0])
    base = next(e[1] for e in ev if e[1])
    SW = []
    for k in range(len(ev)):
        SW.append(next((ev[i][1] for i in range(k, -1, -1) if ev[i][1] is not None), base))
    K = len(SW); U = list(dict.fromkeys(SW)); st = [U.index(x) for x in SW]
    STOP = set("a an the of and or to in on by for at as is was be its it that this with from through which what whose but also into while where who whom".split())
    HEDGE = set("roughly corresponding corresponds aimed aiming region area outside central late known seeks sought".split())
    key = lambda w: re.sub(r'[“”"\'‘’)\].,;:!?]+$', "", re.sub(r'^[“”"\'‘’(\[]+', "", w.lower()))
    UK = [[k for k in (key(w) for w in x.split()) if k] for x in U]; US = [" " + " ".join(T) + " " for T in UK]
    C = {" ".join(T[x:x + n]) for T in UK for n in (1, 2, 3) for x in range(len(T) - n + 1) if T[x] not in STOP and T[x + n - 1] not in STOP}
    MIN = {"b": 0, "r": 1, "a": 1, "g": 2}; Rr = []
    for g in C:
        up = [1 if " " + g + " " in x else 0 for x in US]; pp = [up[u] for u in st]; ch = [k for k in range(1, K) if pp[k] != pp[k - 1]]
        stt = ("b" if pp[-1] else "r") if pp[0] else ("a" if pp[-1] else "g")
        if len(ch) >= 2 and len(ch) > MIN[stt]:
            Rr.append({"g": g, "p": pp, "f": len(ch)})
    Rr.sort(key=lambda r: (-r["f"], -len(r["g"].split()), r["g"]))
    stem = lambda g: [re.sub(r"^re-", "", w)[:6] for w in g.split() if w not in STOP]
    ham = lambda x, y: sum(a != b for a, b in zip(x, y)); nw = lambda g: len(g.split())
    Ls = []
    for r in Rr:
        if all(w in HEDGE or w in STOP for w in r["g"].split()):
            continue
        S = stem(r["g"])
        if any(any(x in S for x in q["S"]) or ham(q["p0"], r["p"]) <= K * .12 for q in Ls):
            continue
        c = r
        for x in Rr:
            if nw(x["g"]) > nw(c["g"]) and (" " + r["g"] + " ") in (" " + x["g"] + " ") and x["f"] >= r["f"] * .8 and ham(x["p"], r["p"]) <= K * .08:
                c = x
        Ls.append(dict(c, S=list(set(S + stem(c["g"]))), p0=r["p"]))
        if len(Ls) >= 8:
            break
    Ls.sort(key=lambda l: -l["f"])
    return sum(1 for r in Rr if " " not in r["g"]), [(l["g"], l["f"]) for l in Ls]
_fbw, _fbl = _fb_recount(R["ratchet"]["articles"]["Zionism"])
assert (_fbw, _fbl) == (100, [("colonization", 81), ("land outside", 54), ("palestine a region", 40), ("land of israel", 40), ("jewish history", 37),
                              ("homeland", 35), ("jewish people", 35), ("jewish state", 29)]), f"fight lanes recount: {_fbw} {_fbl}"
assert round(100 * _share, 1) == 12.4, f"treemap share {_share:.4f}"
print(f"flash: fight lanes recounted: {_fbw} words fought over, lanes " + ", ".join(f"{g} {f}" for g, f in _fbl))

# final round, step 2: the Data lab tab. lab/lab_flash.py is a slim, flash-only fork of the research lab (it reads lab.html, lab.js and
# lab.css and never writes them, so the research edition is unchanged). Its data: only the flash's articles (the six hero articles and
# the treemap's 150 openings), only the flipbook and the language prism; parsed and run on the first visit to the tab.
sys.path.insert(0, os.path.join(HERE, "lab"))
import lab_flash
LAB_TITLES = sorted(set(_HERO6) | {r[0] for r in TM_ROWS})
LAB_D = lab_flash.data(res, LAB_TITLES)
LAB_JSON = json.dumps(LAB_D, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
LAB_BLOCK = '<script type="application/json" id="flLabData">' + LAB_JSON + "</script>"
assert len(LAB_JSON.encode()) < 1.0e6, f"slim lab data: {len(LAB_JSON.encode())/1e6:.2f} MB"
assert "</script" not in lab_flash.js("en") + lab_flash.js("he")
_lab_en = re.sub(r"<[^>]*>", " ", lab_flash.html("en")).lower()
assert not [v for v in VETO if v in _lab_en], f"vetoed wording in the lab markup: {[v for v in VETO if v in _lab_en]}"
for _k in ("<!--LAB-->", "/*FLLABCSS*/", "/*LABJS*/", "<!--LABDATA-->"):
    assert tpl.count(_k) == 1, f"lab slot {_k}"
def lab_fill(body, lang):
    return (body.replace("<!--LAB-->", lab_flash.html(lang)).replace("/*FLLABCSS*/", lab_flash.css(lang))
                .replace("/*LABJS*/", lab_flash.js(lang)).replace("<!--LABDATA-->", LAB_BLOCK))
print(f"flash: data lab: {len(LAB_D['ratchet']['articles'])} flipbook and {len(LAB_D['crosslang']['articles'])} prism articles "
      f"({len(LAB_JSON.encode())/1e6:.2f} MB of data, {len(lab_flash.js('en'))//1000} kB of code)")

# 5. assemble
data = json.dumps(R, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
body = tpl
for k, v in SLOTS.items():
    body = body.replace(f"<!--R:{k}-->", v)
body = lab_fill(body, "en")
out = (body.replace("/*RESEARCH_CSS*/", css)
          .replace("/*RESEARCH_JS*/", lib.replace("const R=/*DATA*/null;", "const R=" + data + ";", 1))
          .replace("@@R@@", RESEARCH_URL))
assert "@@R@@" not in out and "/*RESEARCH_" not in out and "<!--R:" not in out
assert out.count(data) == 1 and out.count(css) == 1, "the data and the research CSS are in the page once (merge r1: the build comment used to receive a second copy)"
for k in SLOTS:
    assert out.count(f'id="{k}"') == 1, f"#{k} must appear exactly once"
out = re.sub(r"<!--VERIFY:[^>]*?-->", "", out)
# a standalone page: doctype, charset and viewport first (the research edition gets the same wrapper when published)
out = '<!DOCTYPE html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n' + out
if LANG in ("he", "bi"):
    import flash_he
    he_out = flash_he.build(dict(tpl=tpl, lib=lib, css=css, SLOTS=SLOTS, data=data, R=R, RESEARCH_URL=RESEARCH_URL, text=text, vis=vis,
                        _Text=_Text, norm=norm, quotes=quotes, corpus=corpus, all_corpus=all_corpus, VETO=VETO, SPIN=SPIN,
                        COMPUTED=COMPUTED, en_out=out, lab_fill=lab_fill, lab_check=lab_flash.check_he), sys.argv[1] if LANG == "he" else None)
    if LANG == "bi":
        import flash_bi
        flash_bi.build(out, he_out, data, sys.argv[1])
    sys.exit(0)
open(sys.argv[1], "w").write(out)
print(f"wrote {sys.argv[1]} ({len(out)/1e6:.2f} MB)")
