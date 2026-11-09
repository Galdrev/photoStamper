"""Build the flash edition of the report.

Usage: python build_flash.py OUT.html

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
assert "23 Oct 2023 → since 9 Dec 2023" in tpl and "Their first lines" not in tpl and "· first lines, then" not in tpl, "hero stack dates or header"
assert 'data-share="flRw"' in tpl and 'data-share="c5vs"' in tpl and "foot:[" in tpl and "scope" in tpl[tpl.index("function shSpec"):], "share cards carry the scope line"
print(f"flash: hero stack, {len(RW_ROWS)} rows, now phrases current and then phrases gone in the 5 Nov 2026 copies")

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

# 5. assemble
data = json.dumps(R, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
body = tpl
for k, v in SLOTS.items():
    body = body.replace(f"<!--R:{k}-->", v)
out = (body.replace("/*RESEARCH_CSS*/", css)
          .replace("/*RESEARCH_JS*/", lib.replace("const R=/*DATA*/null;", "const R=" + data + ";", 1))
          .replace("@@R@@", RESEARCH_URL))
assert "@@R@@" not in out and "/*RESEARCH_" not in out and "<!--R:" not in out
for k in SLOTS:
    assert out.count(f'id="{k}"') == 1, f"#{k} must appear exactly once"
out = re.sub(r"<!--VERIFY:[^>]*?-->", "", out)
# a standalone page: doctype, charset and viewport first (the research edition gets the same wrapper when published)
out = '<!DOCTYPE html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n' + out
open(sys.argv[1], "w").write(out)
print(f"wrote {sys.argv[1]} ({len(out)/1e6:.2f} MB)")
