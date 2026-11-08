"""Cross-wiki collector: how narrative terms travel between language editions, and who carries them.

  python crosswiki.py estimate          -> request / runtime estimate (offline: ratchet revision counts x language ratios)
  python crosswiki.py collect           -> data/crosswiki/{titles.json, leads/*.json, pages/*.json.gz} (checkpointed)
  python crosswiki.py merge             -> data/crosswiki.json.gz, data/crosswiki_summary.json (fails if incomplete)
  CW_LIMIT=4 ...                        -> test mode (first 4 pages)

Scope: CONCEPTS (10 key topics, 11 English titles) x the languages of data/crosslang.json (en + he ar es fr de ru it pt nl pl).
Titles: live langlinks from the English title (redirects followed; a disambiguation page falls back to the next English
candidate, e.g. Palestine -> State of Palestine); the crosslang.json mapping is the fallback when the live call fails.
Per page (one language edition of one key article), 2021-01-01 -> now:
  metadata  every revision (prop=revisions, rvlimit=500): user (hashed at once), timestamp, size, comment (class labels only,
            coord.comment_classes), tags (coord.TAGS_KEEP), sha1, flags
  lead      section 0 (rvprop=ids|content, rvsection=0, 50 revids per request, as ratchet / mass2.fetch_leads), plus the last
            revision before 2021 as the seed state. Pages up to CW_FULL_REQ x 50 revisions are read in full (every flip
            exact). Heavier pages: mass2's time-stratified grid (stride <= 50), every grid interval whose end states differ
            is read in full, and then every interval that contains a revert-tagged revision (a hidden insert-and-revert
            double flip) is read in full while the per-page refinement budget lasts. Revisions with a known sha1 are never
            re-read.
  terms     per revision and term family (FAMILIES): 0 absent, 1 present only in attributed sentences, 2 present in the
            encyclopedia's own voice (a sentence with the term and no attribution marker of that language). English uses
            analyze.F (the ratchet / mass2 lexicon); other languages use crosslang.LEX split per language, with the gaps
            found in patterns/langs/LANGS.md fixed (Arabic definite forms such as «الإبادة الجماعية», «التطهير العرقي»,
            «الفصل العنصري», «الأراضي المحتلة»; Hebrew «כבוש», «תפיסה לוחמתית», «רצח העם»; Russian «оккупированн…»; German
            inflected «ethnischen Säuberung»; French «épuration ethnique»). Arabic / Hebrew text is normalised first (bidi
            marks, harakat, niqqud, tatweel, alef / ta-marbuta / yaa forms, geresh).
  English   key articles already in data/ratchet.json reuse its exact events (every revision since 2021 was read there);
            this collector adds the account of each event (metadata), the voice at each event revision and at the seed, and
            reads the revisions made after ratchet's run in full. English pages not in ratchet are collected like the rest.
  accounts  ONE run-wide salt across all wikis: hash = coord.h(username) = HMAC-SHA256(WT_SALT, username)[:16], so the same
            global (SUL) account has the same hash on every wiki inside this run. Every account that made an exact term
            event is checked on meta.wikimedia.org (meta=globaluserinfo, merged wikis): if it is not attached on that wiki it
            is a local account and is hashed with the wiki's code (never linked across wikis). Kept per hash, aggregated
            later: global registration month, global edit count (2 significant digits), home wiki, attached-wiki count.
Privacy: usernames live in memory only for the page being processed; WT_SALT is made in the single workflow job, masked,
never written. Raw outputs (revids + hashes) stay on the runner and are deleted; only analyze_crosswiki.py's aggregate cards
are published, after analyze_coord.privacy_scan passes.
Fail-loud: a page whose requests fail after wt_net's retries is an error; collect exits non-zero if more than 5% of pages
(or any English page) failed, merge if fewer than 95% of resolved pages are present. Re-running resumes: finished pages and
read lead states are reused (lead states carry no account data; finished page records carry a salt check and are dropped
if the salt changed).
"""
import argparse, glob, gzip, json, math, os, re, sys, threading, time, unicodedata
from collections import Counter
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wt_net                   # noqa: E402
import analyze as A             # noqa: E402
import coord as CO              # noqa: E402  (salt, h, comment classes, tag allow-list)
from mass2 import spread        # noqa: E402  (time-interleaved refinement order)

OUT = os.path.join(HERE, "data", "crosswiki")
START = "2021-01-01T00:00:00Z"
META = "https://meta.wikimedia.org/w/api.php"
FULL_REQ = int(os.environ.get("CW_FULL_REQ", "80"))       # read every revision up to 80 x 50 = 4,000 unknown revisions
GRID_REQ = int(os.environ.get("CW_GRID_REQ", "40"))       # heavier pages: grid of <= 40 requests ...
REFINE_REQ = int(os.environ.get("CW_REFINE_REQ", "60"))   # ... + <= 60 requests around state changes and reverts
GUI_MAX = int(os.environ.get("CW_GUI_MAX", "3500"))       # globaluserinfo lookups (one request per account)
THREADS = int(os.environ.get("CW_THREADS", "3"))
MAX_REQ = int(os.environ.get("CW_MAX_REQUESTS", "15000"))  # soft cap: refinement stops above 90% of it

CONCEPTS = [("Zionism", ["Zionism"]), ("Israel", ["Israel"]), ("Gaza war", ["Gaza war"]),
            ("Gaza genocide", ["Gaza genocide"]), ("Nakba", ["Nakba", "1948 Palestinian expulsion and flight"]),
            ("Hamas", ["Hamas"]), ("October 7 attacks", ["October 7 attacks"]), ("Israeli apartheid", ["Israeli apartheid"]),
            ("Israeli-occupied territories", ["Israeli-occupied territories"]), ("Palestine", ["Palestine", "State of Palestine"])]
MULTI = {"Nakba"}                     # every English candidate is its own page; others: first non-disambiguation candidate
FAMILIES = ["colonial", "genocide", "apartheid", "occupation", "ethnic_cleansing"]
EN_TERM = {"colonial": "settler_colonial", "genocide": "genocide", "apartheid": "apartheid", "occupation": "occupation",
           "ethnic_cleansing": "ethnic_cleansing"}


def _langs():
    try:
        return json.load(open(os.path.join(A.DATA, "crosslang.json")))["langs"]
    except Exception:
        import crosslang
        return ["en"] + crosslang.LANGS


LANGS = _langs()

# ------------------------------------------------------------------ text normalisation (RTL scripts)
BIDI = re.compile("[‎‏‪-‮⁦-⁩؜﻿]")
AR_DIAC = re.compile("[ؐ-ًؚ-ٰٟۖ-ۭـ]")     # harakat, Quranic marks, tatweel
HE_NIQQUD = re.compile("[֑-ׇֽֿׁׂׅׄ]")
AR_MAP = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ة": "ه", "ى": "ي", "ؤ": "و", "ئ": "ي"})
HE_MAP = str.maketrans({"׳": "'", "’": "'", "‘": "'", "`": "'", "״": '"', "“": '"', "”": '"',
                        "־": "-"})


def norm(text):
    """NFC, bidi controls out, Arabic harakat / tatweel out and letter variants folded, Hebrew niqqud out and geresh /
    gershayim / maqaf folded to ASCII, lower case, whitespace collapsed."""
    t = unicodedata.normalize("NFC", text or "")
    t = BIDI.sub("", t)
    t = AR_DIAC.sub("", t).translate(AR_MAP)
    t = HE_NIQQUD.sub("", t).translate(HE_MAP)
    return re.sub(r"\s+", " ", t.lower()).strip()


# ------------------------------------------------------------------ per-language lexicon (crosslang.LEX split + fixes)
# Patterns apply to norm()-ed text (lower case; Arabic ة->ه, أ/إ/آ->ا; Hebrew niqqud removed, ׳->').
LEX_LANG = {
    "de": {"colonial": r"koloni", "genocide": r"genozid|völkermord", "apartheid": r"apartheid",
           "occupation": r"besatz|besetzt|okkup", "ethnic_cleansing": r"ethnisch\w* säuberung"},
    "fr": {"colonial": r"coloni", "genocide": r"génocid|genocid", "apartheid": r"apartheid",
           "occupation": r"occupation|occupé|occupant", "ethnic_cleansing": r"nettoyage ethnique|épuration ethnique"},
    "es": {"colonial": r"coloni", "genocide": r"genocid", "apartheid": r"apartheid",
           "occupation": r"ocupaci|ocupad|ocupante", "ethnic_cleansing": r"limpieza étnica"},
    "it": {"colonial": r"coloni", "genocide": r"genocid", "apartheid": r"apartheid",
           "occupation": r"occupazion|occupat|occupant", "ethnic_cleansing": r"pulizia etnica"},
    "pt": {"colonial": r"coloni", "genocide": r"genocíd|genocid", "apartheid": r"apartheid",
           "occupation": r"ocupaç|ocupad|ocupant", "ethnic_cleansing": r"limpeza étnica"},
    "nl": {"colonial": r"koloni|coloni", "genocide": r"genocid|volkerenmoord", "apartheid": r"apartheid",
           "occupation": r"bezett|bezet\b|bezettingsmacht", "ethnic_cleansing": r"etnische zuivering"},
    "pl": {"colonial": r"koloni", "genocide": r"ludobójstw|ludobójcz|genocyd", "apartheid": r"apartheid",
           "occupation": r"okupac|okupow|okupant", "ethnic_cleansing": r"czystk\w* etniczn"},
    "ru": {"colonial": r"колони", "genocide": r"геноцид", "apartheid": r"апартеид",
           "occupation": r"оккуп", "ethnic_cleansing": r"этническ\w* чистк"},
    "he": {"colonial": r"קולוני", "genocide": r"רצח ה?עם|ג'נוסייד|ג'נוסיד", "apartheid": r"אפרטהייד|אפרטהיד",
           "occupation": r"כיבוש|כבוש|תפיס\S* לוחמתית", "ethnic_cleansing": r"טיהור ה?אתני"},
    "ar": {"colonial": r"استعمار|استيطان|كولونيال", "genocide": r"اباد(?:ه|ات)\s+(?:ال)?جماعي|جينوسايد",
           "apartheid": r"ابارتهايد|ابارتايد|فصل\s+(?:ال)?عنصري", "occupation": r"احتلال|محتل",
           "ethnic_cleansing": r"تطهير\s+(?:ال)?عرقي"},
}
LEX_RX = {l: {f: re.compile(p, re.I) for f, p in d.items()} for l, d in LEX_LANG.items()}
# Attribution markers: a term sentence containing one is "attributed" (heuristic; sentence level, not a coded reading).
ATTR = {
    "en": r"according to|accus|alleg|critics|described as|characteri[sz]|consider|claim|argu|label|charg|has been called|"
          r"denounc|contested|disputed|controvers|analogy|compar|scholars|historians|some |others ",
    "de": r"\blaut\b|nach ansicht|vorwurf|vorwürf|vorgeworfen|wirft|werfen|bezeichne|kritiker|behaupt|angeblich|umstritten|vergleich|gelten",
    "fr": r"selon|accus|allég|critiques|qualifi|considè|estim|affirm|dénonc|analogie|compar|controvers|d'après|désignation",
    "es": r"según|acus|aleg|críticos|denunci|califica|consider|afirma|sostien|analog|compar|controvers",
    "it": r"secondo|accus|critici|definit|considera|sostengono|affermano|presunt|analogia|paragon|controvers",
    "pt": r"segundo|acus|aleg|críticos|consider|afirma|denunci|de acordo com|analogia|compar|controvers",
    "nl": r"volgens|beschuldig|beweer|critici|noem|beschouw|verwijt|aantijging|omstreden|vergelijk|stellen dat",
    "pl": r"według|oskarż|zarzut|uznawan|określan|krytyc|twierdz|rzekom|porówna|kontrowers",
    "ru": r"по мнению|по словам|обвин|утвержда|считают|считается|критик|якобы|называ|согласно|сравнен|спорн",
    "he": r"לפי|לטענת|טוענ|טענו|טענות|האשמ|מואשמ|האשימ|מבקרי|ביקורת|לדברי|לדעת|נטען|מכונה|כינו|השוואה|מחלוקת",
    "ar": r"بحسب|حسب|وفقا|اتهام|اتهم|يتهم|تتهم|يري|يزعم|زعم|مزاعم|ادعاء|يدعي|منتقد|يعتبر|تعتبر|يصف|توصف|يصنف",
}
ATTR_RX = {l: re.compile(p, re.I) for l, p in ATTR.items()}
REDIRECT = re.compile(r"\s*#(redirect|weiterleitung|redirection|redirección|rinvio|redirecionamento|doorverwijzing|"
                      r"przekieruj|перенаправление|הפניה|تحويل)", re.I)
NS_LINK = re.compile(r"\[\[\s*(?:Datei|Bild|Fichier|Image|Archivo|Imagen|File|Immagine|Ficheiro|Imagem|Arquivo|Bestand|"
                     r"Afbeelding|Plik|Grafika|Файл|Изображение|קובץ|תמונה|ملف|صورة|Kategorie|Catégorie|Categoría|Categoria|"
                     r"Categorie|Kategoria|Категория|קטגוריה|تصنيف|Category)\s*:[^\[\]]*(?:\[\[[^\[\]]*\]\][^\[\]]*)*\]\]", re.I)
SENT_SPLIT = re.compile(r"(?<=[.!?؟।])\s+")
UNK, HID, RED = None, "h", "r"


def term_in(lang, fam, s):
    if lang == "en":
        return A.count(EN_TERM[fam], s) > 0
    return bool(LEX_RX[lang][fam].search(s))


def lead_text(wt):
    t = wt or ""
    for _ in range(3):
        t2 = NS_LINK.sub("", t)
        if t2 == t:
            break
        t = t2
    return norm(A.prose(A.split_lead(t)))


def voice_state(lang, p):
    """-> 5-character code, one digit per family: 0 absent, 1 attributed only, 2 in the encyclopedia's own voice."""
    sents = [s for s in SENT_SPLIT.split(p) if s.strip()] if p else []
    out = []
    for f in FAMILIES:
        has = [s for s in sents if term_in(lang, f, s)]
        out.append("0" if not has else "2" if any(not ATTR_RX[lang].search(s) for s in has) else "1")
    return "".join(out)


def lead_state(lang, wt):
    if wt is None:
        return HID
    if REDIRECT.match(wt):
        return RED
    return voice_state(lang, lead_text(wt))


def known(s):
    return s not in (UNK, HID, RED)


def present(s, k):
    return s[k] != "0"


# ------------------------------------------------------------------ API
def api_url(lang):
    return f"https://{lang}.wikipedia.org/w/api.php"


def call(url, **p):
    p.update(format="json", formatversion=2)
    j = wt_net.get_json(url, p)
    if j is None:
        raise RuntimeError(f"request failed after retries ({p.get('prop') or p.get('meta') or p.get('list')})")
    return j


def ep(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()


def iso(t):
    return datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slug(s):
    return re.sub(r"[^\w\-]+", "_", s)[:120]


# ------------------------------------------------------------------ titles
def _en_page(title):
    """-> (resolved title, is_disambiguation, {lang: title}) or None if missing. Raises on request failure."""
    links, cont, res, dis = {}, {}, None, False
    while True:
        j = call(api_url("en"), action="query", titles=title, prop="langlinks|pageprops", lllimit="max",
                 ppprop="disambiguation", redirects=1, **cont)
        if j.get("error"):
            raise RuntimeError(f"langlinks API error {j['error'].get('code')}")
        p = ((j.get("query") or {}).get("pages") or [{}])[0]
        if p.get("missing") or p.get("invalid"):
            return None
        res = p.get("title", title)
        dis = dis or "disambiguation" in (p.get("pageprops") or {})
        for l in p.get("langlinks") or []:
            if l["lang"] in LANGS:
                links[l["lang"]] = l.get("title") or l.get("*")
        if "continue" not in j:
            break
        cont = j["continue"]
    return res, dis, links


def resolve_titles():
    """-> {"pages": [{"lang", "title", "concepts", "en_title", "source"}], "notes": {...}} (data/crosswiki/titles.json)."""
    p = os.path.join(OUT, "titles.json")
    if os.path.exists(p):
        return json.load(open(p))
    try:
        cl = json.load(open(os.path.join(A.DATA, "crosslang.json")))["articles"]
    except Exception:
        cl = {}
    pages, notes, seen = [], {"fallback_to_crosslang": [], "disambiguation_skipped": [], "missing": [],
                              "crosslang_agree": 0, "crosslang_differ": 0}, {}
    def add(lang, title, concept, en_title, src):
        k = (lang, title)
        if k in seen:
            if concept not in seen[k]["concepts"]:
                seen[k]["concepts"].append(concept)
            return
        seen[k] = {"lang": lang, "title": title, "concepts": [concept], "en_title": en_title, "source": src}
        pages.append(seen[k])
    for concept, cands in CONCEPTS:
        got_any = False
        for cand in cands:
            try:
                r = _en_page(cand)
            except RuntimeError:
                r = "failed"
            if r == "failed":
                old = cl.get(cand)
                if old:
                    notes["fallback_to_crosslang"].append(cand)
                    for lang, v in old.items():
                        if lang in LANGS:
                            add(lang, v["title"], concept, cand, "crosslang.json")
                    got_any = True
                    if concept not in MULTI:
                        break
                continue
            if r is None:
                notes["missing"].append(cand); continue
            res, dis, links = r
            if dis:
                notes["disambiguation_skipped"].append(cand); continue
            add("en", res, concept, res, "en")
            for lang, t in sorted(links.items()):
                add(lang, t, concept, res, "langlinks")
                old = (cl.get(cand) or {}).get(lang)
                if old:
                    notes["crosslang_agree" if old["title"] == t else "crosslang_differ"] += 1
            got_any = True
            if concept not in MULTI:
                break
        if not got_any:
            notes["missing"].append(concept)
    out = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "pages": pages, "notes": notes}
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(p + ".tmp", "w"), ensure_ascii=False, indent=1); os.replace(p + ".tmp", p)
    return out


# ------------------------------------------------------------------ revision metadata
RVPROP = "ids|timestamp|user|comment|size|tags|sha1|flags"


def history(lang, title):
    """All revisions since START, oldest first (usernames in memory only), and the seed revision id before START."""
    revs, cont, resolved, missing = [], {}, title, False
    while True:
        j = call(api_url(lang), action="query", prop="revisions", titles=title, rvprop=RVPROP, rvdir="newer", rvstart=START,
                 rvlimit="max", rvslots="main", redirects=1, **cont)
        if j.get("error"):
            raise RuntimeError(f"history API error {j['error'].get('code')}")
        p = ((j.get("query") or {}).get("pages") or [{}])[0]
        if p.get("missing") or p.get("invalid"):
            missing = True; break
        resolved = p.get("title", title)
        revs += p.get("revisions") or []
        if "continue" not in j:
            break
        cont = j["continue"]
    seed = None
    if not missing:
        j = call(api_url(lang), action="query", prop="revisions", titles=resolved, rvprop="ids|timestamp|content",
                 rvdir="older", rvstart=START, rvlimit=1, rvslots="main", rvsection=0, redirects=1)
        p = ((j.get("query") or {}).get("pages") or [{}])[0]
        for r in p.get("revisions") or []:
            c = (r.get("slots") or {}).get("main", {})
            seed = {"revid": r["revid"], "ts": r.get("timestamp"),
                    "state": HID if (c.get("texthidden") or "content" not in c) else lead_state(lang, c["content"])}
    return resolved, missing, revs, seed


# ------------------------------------------------------------------ lead states (mass2.lead_events, generalised)
def fetch_states(lang, revids, budget):
    """Section-0 state of the given revisions, 50 per request. budget = [requests left, requests used]."""
    got = {}
    for i in range(0, len(revids), 50):
        if budget[0] <= 0:
            break
        chunk = revids[i:i + 50]
        cont, pages = {}, 0
        while True:
            j = call(api_url(lang), action="query", prop="revisions", revids="|".join(map(str, chunk)), rvprop="ids|content",
                     rvslots="main", rvsection=0, **cont)
            budget[0] -= 1; budget[1] += 1
            if j.get("error"):
                raise RuntimeError(f"lead API error {j['error'].get('code')}")
            for p in (j.get("query") or {}).get("pages") or []:
                for r in p.get("revisions") or []:
                    c = (r.get("slots") or {}).get("main", {})
                    got[r["revid"]] = HID if (c.get("texthidden") or "content" not in c) else lead_state(lang, c["content"])
            pages += 1
            if "continue" not in j or pages >= 5:
                break
            cont = j["continue"]
        for rid in chunk:
            got.setdefault(rid, HID)
    return got


def _over_budget():
    return wt_net.C["requests"] > 0.9 * MAX_REQ


def read_states(lang, seq, cache, full_req=None, grid_req=None, refine_req=None):
    """seq: revisions (dicts with revid, sha1, tags), oldest first. cache: {revid: state} already read (resume).
    -> (states list aligned with seq, coverage dict). Full read when the unknown revisions fit in full_req requests;
    otherwise grid + refinement around differing intervals, then around revert-tagged intervals (double flips)."""
    full_req = FULL_REQ if full_req is None else full_req
    grid_req = GRID_REQ if grid_req is None else grid_req
    refine_req = REFINE_REQ if refine_req is None else refine_req
    n = len(seq)
    st = [cache.get(r["revid"], UNK) for r in seq]
    by_sha = {}
    for i, r in enumerate(seq):
        if known(st[i]) and r.get("sha1"):
            by_sha[r["sha1"]] = st[i]
    used = [0, 0]

    def fill_sha():
        for i, r in enumerate(seq):
            if st[i] is UNK and r.get("sha1") in by_sha:
                st[i] = by_sha[r["sha1"]]

    def load(idx, cap):
        fill_sha()
        need, shas = [], set()
        for i in idx:                                     # one read per distinct sha1 (reverts restore known texts)
            sh = seq[i].get("sha1")
            if st[i] is UNK and not (sh and sh in shas):
                need.append(i)
                if sh:
                    shas.add(sh)
        b = [cap, 0]
        got = fetch_states(lang, [seq[i]["revid"] for i in need], b)
        used[1] += b[1]
        for i in need:
            if seq[i]["revid"] in got:
                st[i] = got[seq[i]["revid"]]
                cache[seq[i]["revid"]] = st[i]
                if known(st[i]) and seq[i].get("sha1"):
                    by_sha[seq[i]["sha1"]] = st[i]
        fill_sha()

    fill_sha()
    unknown = [i for i in range(n) if st[i] is UNK]
    cov = {"n_revs": n, "mode": "full", "stride": 1}
    if math.ceil(len(unknown) / 50) <= full_req:
        load(unknown, 10 ** 6)
    else:
        k = min(50, max(1, math.ceil(n / (grid_req * 50))))
        grid = sorted(set(range(0, n, k)) | {n - 1})
        load(grid, 10 ** 6)                                     # the grid is always read in full: coverage reaches the end
        cov.update(mode="grid", stride=k, grid=len(grid))
        def intervals():
            out, last = [], None
            for a, b in zip(grid, grid[1:]):
                if known(st[a]):
                    last = a
                if b - a > 1 and known(st[b]) and last is not None:
                    out.append((last, b))
            return out
        iv = intervals()
        diff = [(a, b) for a, b in iv if st[a] != st[b]]
        rev_tag = [(a, b) for a, b in iv if st[a] == st[b] and any(
            "mw-reverted" in (seq[i].get("tags") or []) or set(seq[i].get("tags") or []) & A.REVERTING for i in range(a + 1, b + 1))]
        left, refined = refine_req, {"differing": 0, "revert_tagged": 0}
        for name, lst in (("differing", diff), ("revert_tagged", rev_tag)):
            for j in spread(len(lst)):
                if left <= 0 or _over_budget():
                    break
                a, b = lst[j]
                need = [i for i in range(a + 1, b) if st[i] is UNK and seq[i].get("sha1") not in by_sha]
                c = math.ceil(len(need) / 50)
                if c > left:
                    continue
                before = used[1]
                load(need, c)
                left -= used[1] - before; refined[name] += 1
        cov.update({"differing_intervals": len(diff), "revert_tagged_intervals": len(rev_tag),
                    "refined_differing": refined["differing"], "refined_revert_tagged": refined["revert_tagged"]})
    kn = [i for i in range(n) if known(st[i])]
    cov.update({"requests": used[1], "known": len(kn), "hidden": sum(1 for s in st if s == HID)})
    return st, cov


def derive_events(seq, st, seed_state):
    """Presence flips (insert / remove) and voice changes per family over the known states, seeded with the pre-2021 state.
    exact = the previous revision's state is known (the flip is pinned to this revision and its account)."""
    events, voice, prev, prev_i, seen_sha = [], [], (seed_state if known(seed_state) else None), -1, set()
    for i, r in enumerate(seq):
        s, sha = st[i], r.get("sha1")
        if known(s):
            creation = prev is None and i == 0 and not r.get("parentid")
            base = prev if prev is not None else ("0" * len(FAMILIES) if creation else None)
            if base is not None:
                exact = prev_i == i - 1 or creation
                tg = set(r.get("tags") or [])
                for k, f in enumerate(FAMILIES):
                    a, b = base[k] != "0", s[k] != "0"
                    rec = {"i": i, "family": f, "exact": exact, "creation": creation,
                           "after_i": None if exact or prev_i < 0 else prev_i, "voice_before": base[k], "voice_after": s[k]}
                    if a != b:
                        events.append({**rec, "kind": "insert" if b else "remove", "reverted": "mw-reverted" in tg,
                                       "restore": bool(tg & A.REVERTING) or bool(sha and sha in seen_sha)})
                    elif a and b and base[k] != s[k]:
                        voice.append({**rec, "kind": "to_stated" if s[k] == "2" else "to_attributed"})
            prev, prev_i = s, i
        if sha:
            seen_sha.add(sha)
    return events, voice


# ------------------------------------------------------------------ global accounts
_gui, _gui_lock, _gui_n = {}, threading.Lock(), [0]


def global_info(name):
    """meta=globaluserinfo (merged wikis, edit count), cached in memory only. None = not looked up (cap reached)."""
    with _gui_lock:
        if name in _gui:
            return _gui[name]
        if _gui_n[0] >= GUI_MAX:
            return None
        _gui_n[0] += 1
    j = call(META, action="query", meta="globaluserinfo", guiuser=name, guiprop="merged|editcount")
    g = (j.get("query") or {}).get("globaluserinfo") or {}
    if j.get("error") or "missing" in g or not g:
        info = {"missing": True}
    else:
        merged = g.get("merged") or []
        info = {"missing": False, "home": g.get("home"), "reg": (g.get("registration") or "")[:10] or None,
                "ec": g.get("editcount"), "wikis": sorted({m.get("wiki") for m in merged if m.get("wiki")})}
    with _gui_lock:
        _gui[name] = info
    return info


def _ec2(x):
    return int(float(f"{x:.2g}")) if x else (0 if x == 0 else None)


def account_record(info, lang):
    if info is None:
        return {"looked_up": False}
    if info.get("missing"):
        return {"looked_up": True, "global": False}
    return {"looked_up": True, "global": f"{lang}wiki" in info["wikis"], "reg": (info.get("reg") or "")[:7] or None,
            "ec": _ec2(info.get("ec")), "home": info.get("home"), "n_wikis": len(info["wikis"])}


# ------------------------------------------------------------------ ratchet reuse (English)
_RATCHET = [None]


def ratchet():
    if _RATCHET[0] is None:
        p = os.path.join(A.DATA, "ratchet.json")
        if not os.path.exists(p):
            _RATCHET[0] = {}
        else:
            rj = json.load(open(p))
            end = 0.0
            for terms in (rj.get("events") or {}).values():
                for lst in terms.values():
                    for e in lst:
                        if e.get("censored"):
                            end = max(end, e["t"] + e["survived"])
            _RATCHET[0] = {"events": rj.get("events") or {}, "articles": rj.get("articles") or {}, "end": end or None}
    return _RATCHET[0]


def ratchet_states(seq, title, cache):
    """English page in ratchet.json: rebuild the per-revision presence sequence from its exact events, then read the voice at
    the event revisions and every revision after ratchet's run. -> (states aligned with seq or None, coverage)."""
    R = ratchet()
    a = (R.get("articles") or {}).get(title)
    if not a or not R.get("end"):
        return None, None
    ev = (R["events"].get(title) or {})
    idx = {r["revid"]: i for i, r in enumerate(seq)}
    flips = {}
    for k, f in enumerate(FAMILIES):
        for e in ev.get(EN_TERM[f]) or []:
            if e.get("revid") in idx:
                flips.setdefault(idx[e["revid"]], {})[k] = e["kind"] == "insert"
    pres = [bool((a.get("terms") or {}).get(EN_TERM[f], {}).get("present_start")) for f in FAMILIES]
    end = R["end"]
    after = [i for i, r in enumerate(seq) if ep(r["timestamp"]) > end]
    first_after = after[0] if after else len(seq)
    pres_seq = []
    for i in range(first_after):
        for k, v in flips.get(i, {}).items():
            pres[k] = v
        pres_seq.append(list(pres))
    st = [UNK] * len(seq)
    # voice: read the event revisions, their parents and the newer-than-ratchet revisions (full); fill the rest from presence
    need = sorted({i for i in flips} | {i - 1 for i in flips if i > 0} | {0} | set(after))
    sub = [seq[i] for i in need]
    sst, cov = read_states("en", sub, cache, full_req=10 ** 6)
    got = dict(zip(need, sst))
    last_voice = None
    for i in range(len(seq)):
        if i in got and known(got[i]):
            st[i] = got[i]
            if i < first_after:                                  # ratchet's presence is authoritative before its end
                st[i] = "".join(("0" if not pres_seq[i][k] else (got[i][k] if got[i][k] != "0" else "2"))
                                for k in range(len(FAMILIES)))
            last_voice = st[i]
        elif i < first_after:
            base = last_voice or "2" * len(FAMILIES)
            st[i] = "".join(("0" if not pres_seq[i][k] else (base[k] if base[k] != "0" else "2")) for k in range(len(FAMILIES)))
            last_voice = st[i]
    cov = {**cov, "mode": "ratchet", "ratchet_end": iso(end), "after_ratchet": len(after), "n_revs": len(seq),
           "voice_note": "voice read at event revisions, their parents and after ratchet's run; carried between them"}
    return st, cov


# ------------------------------------------------------------------ one page
def _pfile(kind, pg):
    return os.path.join(OUT, kind, f"{pg['lang']}__{slug(pg['title'])}.json" + (".gz" if kind == "pages" else ""))


def salt_check():
    return CO.h("__crosswiki_salt_check__")


def collect_page(pg):
    lang, title = pg["lang"], pg["title"]
    resolved, missing, raw, seed = history(lang, title)
    if missing:
        return {**pg, "missing": True, "revs": [], "events": [], "voice": [], "accounts": {}, "coverage": {}}
    seq = [{"revid": r["revid"], "parentid": r.get("parentid"), "timestamp": r["timestamp"], "sha1": None if r.get("sha1hidden") else r.get("sha1"),
            "tags": r.get("tags") or [], "_user": None if r.get("userhidden") else r.get("user"), "size": r.get("size"),
            "minor": bool(r.get("minor")), "cc": CO.comment_classes(r.get("comment")) if not r.get("commenthidden") else ["hidden"]}
           for r in raw if r.get("revid")]
    lp = _pfile("leads", pg)
    cache = {}
    if os.path.exists(lp):
        cache = {int(k): v for k, v in json.load(open(lp)).items()}
    st, cov = (None, None)
    if lang == "en":
        st, cov = ratchet_states(seq, resolved, cache)
        if st is None and resolved != title:
            st, cov = ratchet_states(seq, title, cache)
    if st is None:
        st, cov = read_states(lang, seq, cache)
    os.makedirs(os.path.dirname(lp), exist_ok=True)
    json.dump({str(k): v for k, v in cache.items()}, open(lp + ".tmp", "w")); os.replace(lp + ".tmp", lp)
    seed_state = seed["state"] if seed else None
    events, voice = derive_events(seq, st, seed_state)
    # accounts: exact event makers are checked globally; the rest follow SUL (same name = same global account)
    local = set()
    acc = {}
    for e in events:
        u = seq[e["i"]]["_user"]
        if not e["exact"] or not u or A.ANON.match(u) or A.BOT.search(u):
            continue
        rec = account_record(global_info(u), lang)
        if rec.get("looked_up") and not rec.get("global"):
            local.add(u)
        acc[u] = rec
    def hh(u):
        return CO.h(u + "@" + lang) if u in local else CO.h(u)
    accounts = {hh(u): rec for u, rec in acc.items()}
    revs = []
    for i, r in enumerate(seq):
        u = r.pop("_user")
        anon = bool(u and A.ANON.match(u)); bot = bool(u and A.BOT.search(u))
        revs.append({"revid": r["revid"], "t": r["timestamp"], "u": hh(u) if u else None, "anon": anon, "bot": bot,
                     "hidden": not u, "size": r["size"], "minor": r["minor"], "cc": r["cc"],
                     "tags": sorted(set(r["tags"]) & CO.TAGS_KEEP), "parentid": r["parentid"], "s": st[i]})
    for e in events + voice:
        r = revs[e["i"]]
        e.update({"t": r["t"], "revid": r["revid"], "u": r["u"] if e["exact"] else None, "anon": r["anon"], "bot": r["bot"]})
    created = seq[0]["timestamp"] if seq and not seq[0].get("parentid") else None
    return {**pg, "resolved_title": resolved, "missing": False, "seed": {"state": seed_state, "ts": seed["ts"]} if seed else None,
            "created_since_2021": created, "revs": revs, "events": events, "voice": voice, "accounts": accounts,
            "coverage": cov, "salt_check": salt_check()}


# ------------------------------------------------------------------ run
def collect():
    CO.salt()
    tt = resolve_titles()
    pages = tt["pages"]
    lim = int(os.environ.get("CW_LIMIT", "0"))
    pages = pages[:lim] if lim else pages
    os.makedirs(os.path.join(OUT, "pages"), exist_ok=True)
    todo, done = [], 0
    for pg in pages:
        pf = _pfile("pages", pg)
        if os.path.exists(pf):
            try:
                rec = json.load(gzip.open(pf, "rt"))
                if rec.get("salt_check") == salt_check():
                    done += 1; continue
            except Exception:
                pass
            os.remove(pf)
        todo.append(pg)
    print(f"crosswiki: {len(pages)} pages ({Counter(p['lang'] for p in pages)}), {done} reused, {len(todo)} to do", flush=True)
    from concurrent.futures import ThreadPoolExecutor, as_completed
    fails, en_fail = [], False
    wt_net.heartbeat("crosswiki", done, len(pages), force=True)
    with ThreadPoolExecutor(THREADS) as ex:
        futs = {ex.submit(collect_page, pg): pg for pg in todo}
        for f in as_completed(futs):
            pg = futs[f]
            try:
                rec = f.result()
                pf = _pfile("pages", pg)
                with gzip.open(pf + ".tmp", "wt") as fh:
                    json.dump(rec, fh, ensure_ascii=False)
                os.replace(pf + ".tmp", pf)
                done += 1
                cv = rec.get("coverage") or {}
                print(f"{pg['lang']} {pg['concepts'][0]}: {len(rec['revs'])} revisions, {len(rec['events'])} term events, "
                      f"mode={cv.get('mode')} lead requests={cv.get('requests')}", flush=True)
            except Exception as e:
                fails.append(pg); en_fail = en_fail or pg["lang"] == "en"
                print("ERR", pg["lang"], type(e).__name__, str(e)[:200], file=sys.stderr, flush=True)
            wt_net.heartbeat("crosswiki", done, len(pages), page_errors=len(fails), gui_lookups=_gui_n[0])
    wt_net.heartbeat("crosswiki-done", done, len(pages), force=True, page_errors=len(fails))
    print(f"crosswiki collect: {done}/{len(pages)} pages, {len(fails)} failed, {wt_net.C['requests']} requests, "
          f"{_gui_n[0]} global account lookups", flush=True)
    if todo and (len(fails) > 0.05 * len(pages) or en_fail):
        sys.exit(f"crosswiki collect: {len(fails)} page(s) failed (>5% or an English page) - re-run to resume")


def merge():
    tt = json.load(open(os.path.join(OUT, "titles.json")))
    expected = tt["pages"]
    lim = int(os.environ.get("CW_LIMIT", "0"))
    expected = expected[:lim] if lim else expected
    recs = []
    for pg in expected:
        pf = _pfile("pages", pg)
        if os.path.exists(pf):
            r = json.load(gzip.open(pf, "rt"))
            if r.get("salt_check") == salt_check():
                r.pop("salt_check", None); recs.append(r)
    accounts = {}
    for r in recs:
        for k, v in r["accounts"].items():
            if k not in accounts or (v.get("looked_up") and not accounts[k].get("looked_up")):
                accounts[k] = v
    ev = [e for r in recs for e in r["events"]]
    summ = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "pages_expected": len(expected),
            "pages": len(recs), "missing_pages": sum(1 for r in recs if r.get("missing")),
            "by_lang": dict(Counter(r["lang"] for r in recs)), "revisions": sum(len(r["revs"]) for r in recs),
            "events": len(ev), "exact_events": sum(1 for e in ev if e["exact"]),
            "lead_modes": dict(Counter((r.get("coverage") or {}).get("mode") for r in recs)),
            "accounts_with_facts": len(accounts), "local_accounts": sum(1 for v in accounts.values() if v.get("looked_up") and not v.get("global")),
            "title_notes": tt.get("notes")}
    out = {"note": "Cross-wiki lead term data. Accounts are HMAC-SHA256(run salt, username)[:16], one salt for all wikis "
                   "(local, unattached accounts are hashed with the wiki code). Raw: never published.",
           "summary": summ, "langs": LANGS, "families": FAMILIES, "concepts": [c for c, _ in CONCEPTS],
           "pages": recs, "accounts": accounts}
    with gzip.open(os.path.join(A.DATA, "crosswiki.json.gz"), "wt") as f:
        json.dump(out, f, separators=(",", ":"), ensure_ascii=False)
    json.dump(summ, open(os.path.join(A.DATA, "crosswiki_summary.json"), "w"), indent=1, ensure_ascii=False)
    print("crosswiki merged:", json.dumps(summ, indent=1, ensure_ascii=False), flush=True)
    if len(recs) < 0.95 * len(expected):
        sys.exit(f"crosswiki merge: {len(recs)}/{len(expected)} pages - incomplete")


# ------------------------------------------------------------------ estimate (offline)
# Revisions since 2021 per page relative to English (assumption: edit volume of these articles in each edition; an upper
# guess so the estimate errs high). The run prints the real counts.
LANG_RATIO = {"de": .35, "he": .30, "fr": .30, "ar": .25, "es": .25, "ru": .25, "it": .15, "pt": .15, "pl": .10, "nl": .08}
EN_NEW_GUESS = {"Israeli-occupied territories": 1500, "Palestine": 4000}
NO_PAGE = {"Gaza genocide": {"de", "he", "ru"}}


def estimate(eff_rps=1.4, retry=1.15, sha_dedupe=0.85, acct_per_event=0.6):
    R = ratchet()
    arts = R.get("articles") or {}
    rows, tot = [], Counter()
    def lead_req(n):
        if math.ceil(n * sha_dedupe / 50) <= FULL_REQ:
            return math.ceil(n * sha_dedupe / 50) + 1
        return GRID_REQ + REFINE_REQ + 1
    events = 0
    for concept, cands in CONCEPTS:
        en_n = sum((arts.get(c) or {}).get("revisions", 0) for c in cands) or EN_NEW_GUESS.get(concept, 2000)
        in_ratchet = any(c in arts for c in cands)
        en_ev = sum(len(v) for c in cands for t, v in ((R.get("events") or {}).get(c) or {}).items()
                    if t in EN_TERM.values())
        meta = sum(math.ceil(max(1, (arts.get(c) or {}).get("revisions", en_n)) / 500) + 1 for c in cands)
        lead = (math.ceil(2 * en_ev / 50) + 2) if in_ratchet else lead_req(en_n)
        tot["metadata"] += meta; tot["lead"] += lead; events += en_ev or en_n // 60
        for l, q in LANG_RATIO.items():
            if l in NO_PAGE.get(concept, set()):
                continue
            n = int(en_n * q)
            tot["metadata"] += math.ceil(n / 500) + 1
            tot["lead"] += lead_req(n)
            events += max(2, n // 60)
        rows.append({"concept": concept, "en_revisions": en_n, "en_from_ratchet": in_ratchet})
    tot["titles"] = sum(len(c) for _, c in CONCEPTS)
    tot["globaluserinfo"] = min(GUI_MAX, int(events * acct_per_event))
    total = sum(tot.values())
    res = {"assumptions": {"lang_ratio_vs_en": LANG_RATIO, "sha1_dedupe": sha_dedupe, "full_read_up_to_revisions": FULL_REQ * 50,
                           "grid_plus_refine_requests_per_heavy_page": GRID_REQ + REFINE_REQ, "accounts_per_event": acct_per_event,
                           "effective_req_per_s": eff_rps, "retry_factor": retry},
           "concepts": rows, "requests": dict(tot), "total": total, "total_with_retries": int(total * retry),
           "collection_hours": round(total * retry / eff_rps / 3600, 2), "estimated_term_events": events}
    print(json.dumps(res, indent=1, ensure_ascii=False))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["estimate", "collect", "merge"])
    a = ap.parse_args()
    {"estimate": estimate, "collect": collect, "merge": merge}[a.cmd]()


if __name__ == "__main__":
    main()
