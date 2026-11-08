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

# 3. the data slice
ARTS = ["Zionism", "Hamas", "October 7 attacks", "Gaza genocide"]
R = {
    "zionism": res["zionism"], "oct7": res["oct7"], "v3": res["v3"], "xw": res["xw"],
    "langs": {"order": (res.get("langs") or {}).get("order")},
    "ratchet": {"articles": {t: res["ratchet"]["articles"][t] for t in ARTS}},
    "articles": [{k: a.get(k) for k in ("title", "pv_monthly", "w_edits")} for a in res["articles"] if a["title"] in ARTS],
    "week0": res.get("week0"), "n_weeks": res.get("n_weeks"),
}
assert len(R["articles"]) == len(ARTS), "a flash article is missing from the research data"
assert [r["date"] for r in R["oct7"]["designation"]][::3] == ["2021-01-01", "2026-10-31"], "Hamas designation rows changed"

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

# the messaging check's vetoes and the no-names rule
low = vis.lower()
VETO = ["afterthought", "the world reads first", "64 of", "47 of", "336", "650", "386", "both sides", "in 2021 / before the war",
        "before the war, these first lines", "documented"]
hit = [v for v in VETO if v in low]
assert not hit, f"vetoed wording on the flash page: {hit}"
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

# 5. assemble
data = json.dumps(R, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
out = (tpl.replace("/*RESEARCH_CSS*/", css)
          .replace("/*RESEARCH_JS*/", lib.replace("const R=/*DATA*/null;", "const R=" + data + ";", 1))
          .replace("@@R@@", RESEARCH_URL))
assert "@@R@@" not in out and "/*RESEARCH_" not in out
out = re.sub(r"<!--VERIFY:[^>]*?-->", "", out)
# a standalone page: doctype, charset and viewport first (the research edition gets the same wrapper when published)
out = '<!DOCTYPE html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n' + out
open(sys.argv[1], "w").write(out)
print(f"wrote {sys.argv[1]} ({len(out)/1e6:.2f} MB)")
