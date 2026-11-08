"""Cross-wiki collector: how narrative terms travel between language editions, and who carries them.

  python crosswiki.py estimate          -> request / runtime estimate (offline: ratchet revision counts x language ratios)
  python crosswiki.py collect           -> data/crosswiki/{titles.json, wikidata.json, leads/*.json, pages/*.json.gz}
  python crosswiki.py merge             -> data/crosswiki.json.gz, data/crosswiki_summary.json (fails if incomplete)
  CW_LIMIT=4 ...                        -> test mode (first 4 pages)

Scope: CONCEPTS (10 key topics, 11 English titles) x the languages of data/crosslang.json (en + he ar es fr de ru it pt nl pl).
Titles: live langlinks from the English title (redirects followed; a disambiguation page falls back to the next English
candidate, e.g. Palestine -> State of Palestine); the crosslang.json mapping is the fallback when the live call fails.

Per page (one language edition of one key article), 2021-01-01 -> now:
  metadata  every revision (rvlimit=500): user (hashed at once), timestamp, size, comment (class labels only,
            coord.comment_classes), tags (coord.TAGS_KEEP), sha1, flags; the first revision ever (creation date); the last
            revision before 2021 (seed state)
  lead      section 0 (rvprop=ids|content, rvsection=0, 50 revids per request, as ratchet / mass2.fetch_leads). Pages up to
            CW_FULL_REQ x 50 revisions are read in full (every flip exact). Heavier pages: mass2's time-stratified grid
            (stride <= 50); every grid interval whose end states differ is read in full, then every interval holding a
            revert-tagged revision (a hidden insert-and-revert double flip), while the per-page budget lasts. A known sha1 is
            never re-read.
  terms     per revision and term family (FAMILIES): 0 absent, 1 present only in attributed sentences, 2 in the
            encyclopedia's own voice (a term sentence without an attribution marker of that language). English uses
            analyze.F (ratchet / mass2 lexicon); other languages crosslang.LEX split per language, with the gaps found in
            patterns/langs/LANGS.md fixed (Arabic definite forms «الإبادة الجماعية», «التطهير العرقي», «الفصل العنصري», «الأراضي
            المحتلة»; Hebrew «כבוש», «תפיסה לוחמתית», «רצח העם»; Russian «оккупированн…»; German inflected «ethnischen
            Säuberung»; French «épuration ethnique»). Arabic / Hebrew text is normalised first (bidi marks, harakat, niqqud,
            tatweel, alef / ta-marbuta / yaa forms, geresh).
  narrative per read revision (features): sentence count; index of the first terror-word sentence (the Hamas designation
            sentence); hostage mentions (count, first sentence); how the first sentence names October 7 (attack /
            massacre / incursion / operation / terror classes); court-ruling overstatement flags (COURT_FLAGS, from
            LANGS.md finding 7)
  sources   for every insertion event, the <ref> domains of section 0 at that revision and its parent (mass2.lead_citations,
            explore.SOURCE_CLASSES): which domains / classes arrived with the term
  talk      talk-page revision metadata 2021 -> now (user hashed, timestamp, size, comment classes)
  logs      protection log (type=protect: dates, levels, expiry) and verified renames (type=move, source titles taken from
            move null-revision comments and confirmed in the move log; only log titles are kept)
  views     monthly user pageviews 2021 -> last full month (REST, all-access, agent=user), summed over current + former titles
  English   key articles already in data/ratchet.json reuse its exact events; this collector adds the account of each event,
            the voice at event revisions and the seed, and reads revisions newer than ratchet's run in full. English talk:
            the current page and every archive touched since 2021 are parsed for RfCs and requested moves (open date =
            earliest signature, close date = first signature after the close template, outcome class via mass2.result_class).
Per concept: Wikidata label / description changes per language with dates (item revision summaries
  wbsetlabel / wbsetdescription carry the new value; bulk edits are recorded as value-not-shown) and the current values.
Accounts: ONE run-wide salt for all wikis: hash = coord.h(username), so the same global (SUL) account has the same hash on every
  wiki inside this run. Each account that made an exact term event is checked on meta.wikimedia.org (meta=globaluserinfo); if
  it is not attached on that wiki it is local and hashed with the wiki code (never linked). Kept per hash: global registration
  month, edit count (2 significant digits), home wiki, attached-wiki count. Talk-page editors are hashed the same way.
Privacy: usernames live in memory only for the page being processed; WT_SALT is made in the single workflow job, masked, never
  written. Raw outputs (revids + hashes) stay on the runner and are deleted; only analyze_crosswiki.py's aggregate cards are
  published, after analyze_coord.privacy_scan passes.
Fail-loud: a page whose requests fail after wt_net's retries is an error; collect exits non-zero if more than 5% of pages (or any
  English page) failed, merge if fewer than 95% of resolved pages are present. Re-running resumes: finished pages and read lead
  states are reused (lead states carry no account data; page records carry a salt check and are dropped if the salt changed).
"""
import argparse, gzip, json, math, os, re, sys, threading, time, unicodedata
from collections import Counter
from datetime import datetime, timezone
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wt_net                   # noqa: E402
import analyze as A             # noqa: E402
import coord as CO              # noqa: E402  (salt, h, comment classes, tag allow-list)
import pilot as P               # noqa: E402  (signature dates, close templates)
import mass2 as M2              # noqa: E402  (spread, lead_citations, result_class, RfC / RM templates)

OUT = os.path.join(HERE, "data", "crosswiki")
START = "2021-01-01T00:00:00Z"
META = "https://meta.wikimedia.org/w/api.php"
WD = "https://www.wikidata.org/w/api.php"
PV = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{lang}.wikipedia/all-access/user/{t}/monthly/2021010100/{end}"
FULL_REQ = int(os.environ.get("CW_FULL_REQ", "80"))       # read every revision up to 80 x 50 = 4,000 unknown revisions
GRID_REQ = int(os.environ.get("CW_GRID_REQ", "40"))       # heavier pages: grid of <= 40 requests ...
REFINE_REQ = int(os.environ.get("CW_REFINE_REQ", "60"))   # ... + <= 60 requests around state changes and reverts
GUI_MAX = int(os.environ.get("CW_GUI_MAX", "3500"))       # globaluserinfo lookups (one request per account)
MAX_ARCHIVES = int(os.environ.get("CW_MAX_ARCHIVES", "80"))
THREADS = int(os.environ.get("CW_THREADS", "3"))
MAX_REQ = int(os.environ.get("CW_MAX_REQUESTS", "20000"))  # soft cap: refinement stops above 90% of it

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
# Patterns apply to norm()-ed text (lower case; Arabic ة->ه, أ/إ/آ->ا, ى->ي; Hebrew niqqud removed, ׳->').
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
# Narrative traces (normalised text; one union per signal, all languages)
TERROR = re.compile(r"terror|terreur|террор|טרור|ارهاب", re.I)
HOSTAGE = re.compile(r"hostage|captive|abduct|geisel|entführ|otage|rehén|rehenes|secuestr|ostagg|rapit[io]|refém|reféns|"
                     r"sequestr|gijzel|zakładni|porwan|заложни|похищ|חטופ|חטיפ|בני ה?ערובה|رهائن|رهين|اسري|محتجز|مختطف", re.I)
O7_NAMES = {"attack": r"attack|angriff|attaque|attentat|ataque|attacco|aanval|\batak|нападени|атак|מתקפ|התקפ|هجوم",
            "massacre": r"massac|massaker|masacre|bloedbad|masakr|резн|бойн|טבח|مجزر|مذبح",
            "incursion": r"incursion|invasion|invasi|einfall|eindring|infiltr|inval|вторжени|проникл|חדיר|פליש|اقتحام|توغل|تسلل",
            "operation": r"operation|opération|operación|operação|operazione|operatie|operacj|операци|מבצע|عمليه|طوفان الاقصي",
            "terror": TERROR.pattern}
O7_RX = {k: re.compile(v, re.I) for k, v in O7_NAMES.items()}
# Court-ruling overstatements described in LANGS.md (finding 7) + the English equivalent; what the courts said is in the card.
COURT_FLAGS = {
    "icj_found_plausible_intent": r"نيه معقوله|plausible intent",
    "icj_plausibly_genocidal": r"plausibilmente genocid|plausibly genocidal",
    "court_found_israel_guilty": r"признал\w* израил\w* виновн|found israel guilty|reconnu israël coupable",
    "icj_recognised_apartheid": r"(?:cour|cij|icj|court)[^.]{0,40}reconna\w*[^.]{0,60}(?:israël|israel)[^.]{0,120}apartheid|"
                                r"(?:icj|court of justice)[^.]{0,60}(?:found|ruled) that israel[^.]{0,60}apartheid",
    "icj_ruled_genocide": r"(?:icj|international court of justice|cij|corte internacional|cour internationale)[^.]{0,80}"
                          r"(?:ruled|found|concluded|determined|dictaminó|conclu\w*) (?:that )?israel (?:is|was|has been|had been|"
                          r"est|estaba|está)? ?(?:committ\w*|commet\w*|comet\w*) (?:a )?(?:genocide|génocide|genocidio)",
}
COURT_RX = {k: re.compile(v, re.I) for k, v in COURT_FLAGS.items()}
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


def sentences(p):
    return [s for s in SENT_SPLIT.split(p) if s.strip()] if p else []


def voice_state(lang, p):
    """-> 5-character code, one digit per family: 0 absent, 1 attributed only, 2 in the encyclopedia's own voice."""
    sents = sentences(p)
    out = []
    for f in FAMILIES:
        has = [s for s in sents if term_in(lang, f, s)]
        out.append("0" if not has else "2" if any(not ATTR_RX[lang].search(s) for s in has) else "1")
    return "".join(out)


def narrative_features(p):
    """Compact narrative traces of one lead: n sentences, terror sentence index, hostage count / first index, first-sentence
    October 7 naming classes, court-overstatement flags. Only non-empty keys are kept."""
    ss = sentences(p)
    f = {"n": len(ss)}
    tr = next((i for i, s in enumerate(ss) if TERROR.search(s)), None)
    if tr is not None:
        f["tr"] = tr
    hg = [i for i, s in enumerate(ss) for _ in HOSTAGE.finditer(s)]
    if hg:
        f["hg"] = [len(hg), hg[0]]
    if ss:
        o7 = sorted(k for k, rx in O7_RX.items() if rx.search(ss[0]))
        if o7:
            f["o7"] = o7
    ct = sorted(k for k, rx in COURT_RX.items() if rx.search(p))
    if ct:
        f["ct"] = ct
    return f


def lead_state(lang, wt):
    """-> (state code or HID / RED, features or None)."""
    if wt is None:
        return HID, None
    if REDIRECT.match(wt):
        return RED, None
    p = lead_text(wt)
    return voice_state(lang, p), narrative_features(p)


def known(s):
    return s not in (UNK, HID, RED)


# ------------------------------------------------------------------ API
def api_url(lang):
    return f"https://{lang}.wikipedia.org/w/api.php"


def call(url, **p):
    p.update(format="json", formatversion=2)
    j = wt_net.get_json(url, p)
    if j is None:
        raise RuntimeError(f"request failed after retries ({p.get('prop') or p.get('meta') or p.get('list') or p.get('action')})")
    return j


def paged(url, key, max_pages=200, **p):
    """Follow `continue`; raise on API error; yield each result page."""
    cont, n = {}, 0
    while True:
        j = call(url, **p, **cont)
        if j.get("error"):
            raise RuntimeError(f"{key} API error {j['error'].get('code')}")
        yield j
        n += 1
        if "continue" not in j or n >= max_pages:
            return
        cont = j["continue"]


def ep(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()


def iso(t):
    return datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slug(s):
    return re.sub(r"[^\w\-]+", "_", s)[:120]


# ------------------------------------------------------------------ titles
def _en_page(title):
    """-> (resolved title, is_disambiguation, {lang: title}, qid) or None if missing. Raises on request failure."""
    links, res, dis, qid = {}, None, False, None
    for j in paged(api_url("en"), "langlinks", titles=title, prop="langlinks|pageprops", lllimit="max",
                   ppprop="disambiguation|wikibase_item", redirects=1):
        p = ((j.get("query") or {}).get("pages") or [{}])[0]
        if p.get("missing") or p.get("invalid"):
            return None
        res = p.get("title", title)
        pp = p.get("pageprops") or {}
        dis = dis or "disambiguation" in pp
        qid = qid or pp.get("wikibase_item")
        for l in p.get("langlinks") or []:
            if l["lang"] in LANGS:
                links[l["lang"]] = l.get("title") or l.get("*")
    return res, dis, links, qid


def resolve_titles():
    """-> {"pages": [{"lang", "title", "concepts", "en_title", "source"}], "qids": {concept: qid}, "notes": {...}}."""
    p = os.path.join(OUT, "titles.json")
    if os.path.exists(p):
        return json.load(open(p))
    try:
        cl = json.load(open(os.path.join(A.DATA, "crosslang.json")))["articles"]
    except Exception:
        cl = {}
    pages, qids, seen = [], {}, {}
    notes = {"fallback_to_crosslang": [], "disambiguation_skipped": [], "missing": [], "crosslang_agree": 0, "crosslang_differ": 0}

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
                if cand not in notes["missing"]:
                    notes["missing"].append(cand)
                continue
            res, dis, links, qid = r
            if dis:
                notes["disambiguation_skipped"].append(cand); continue
            add("en", res, concept, res, "en")
            if qid and concept not in qids:
                qids[concept] = qid
            for lang, t in sorted(links.items()):
                add(lang, t, concept, res, "langlinks")
                old = (cl.get(cand) or {}).get(lang)
                if old:
                    notes["crosslang_agree" if old["title"] == t else "crosslang_differ"] += 1
            got_any = True
            if concept not in MULTI:
                break
        if not got_any and concept not in notes["missing"]:
            notes["missing"].append(concept)
    out = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "pages": pages, "qids": qids, "notes": notes}
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(p + ".tmp", "w"), ensure_ascii=False, indent=1); os.replace(p + ".tmp", p)
    return out


# ------------------------------------------------------------------ revision metadata
RVPROP = "ids|timestamp|user|comment|size|tags|sha1|flags"


def revisions(lang, **sel):
    """All revisions since START of one page (titles= or pageids=), oldest first; -> (page dict, revs) or (None, [])."""
    revs, page = [], None
    for j in paged(api_url(lang), "history", action="query", prop="revisions|info", inprop="talkid", rvprop=RVPROP,
                   rvdir="newer", rvstart=START, rvlimit="max", redirects=1, **sel):
        p = ((j.get("query") or {}).get("pages") or [{}])[0]
        if p.get("missing") or p.get("invalid"):
            return None, []
        page = page or p
        revs += p.get("revisions") or []
    return page, revs


def history(lang, title):
    """Revisions since START (usernames in memory only), the seed state before START, the creation date, the talk page id."""
    page, revs = revisions(lang, titles=title)
    if page is None:
        return {"missing": True}
    resolved = page.get("title", title)
    j = call(api_url(lang), action="query", prop="revisions", titles=resolved, rvprop="ids|timestamp|content",
             rvdir="older", rvstart=START, rvlimit=1, rvslots="main", rvsection=0)
    seed = None
    for r in (((j.get("query") or {}).get("pages") or [{}])[0].get("revisions") or []):
        c = (r.get("slots") or {}).get("main", {})
        s, f = (HID, None) if (c.get("texthidden") or "content" not in c) else lead_state(lang, c["content"])
        seed = {"revid": r["revid"], "ts": r.get("timestamp"), "state": s, "feat": f}
    if revs and not revs[0].get("parentid"):
        created = revs[0]["timestamp"]
    else:
        j = call(api_url(lang), action="query", prop="revisions", titles=resolved, rvprop="ids|timestamp", rvdir="newer", rvlimit=1)
        rr = ((j.get("query") or {}).get("pages") or [{}])[0].get("revisions") or []
        created = rr[0]["timestamp"] if rr else None
    return {"missing": False, "resolved": resolved, "revs": revs, "seed": seed, "created": created,
            "talkid": page.get("talkid"), "pageid": page.get("pageid")}


# ------------------------------------------------------------------ lead states (mass2.lead_events, generalised)
def fetch_states(lang, revids, budget):
    """Section-0 (state, features) of the given revisions, 50 per request. budget = [requests left, requests used]."""
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
                    got[r["revid"]] = (HID, None) if (c.get("texthidden") or "content" not in c) else lead_state(lang, c["content"])
            pages += 1
            if "continue" not in j or pages >= 5:
                break
            cont = j["continue"]
        for rid in chunk:
            got.setdefault(rid, (HID, None))
    return got


def _over_budget():
    return wt_net.C["requests"] > 0.9 * MAX_REQ


def read_states(lang, seq, cache, feats, full_req=None, grid_req=None, refine_req=None):
    """seq: revisions (revid, sha1, tags), oldest first. cache {revid: state} / feats {revid: features}: already read (resume),
    updated in place. -> (states aligned with seq, coverage). Full read when the unknown revisions fit in full_req requests;
    otherwise grid + refinement around differing intervals, then around revert-tagged intervals (double flips)."""
    full_req = FULL_REQ if full_req is None else full_req
    grid_req = GRID_REQ if grid_req is None else grid_req
    refine_req = REFINE_REQ if refine_req is None else refine_req
    n = len(seq)
    st = [cache.get(r["revid"], UNK) for r in seq]
    by_sha = {}
    for i, r in enumerate(seq):
        if known(st[i]) and r.get("sha1"):
            by_sha[r["sha1"]] = (st[i], feats.get(r["revid"]))
    used = [0, 0]

    def fill_sha():
        for i, r in enumerate(seq):
            if st[i] is UNK and r.get("sha1") in by_sha:
                st[i], f = by_sha[r["sha1"]]
                cache[r["revid"]] = st[i]
                if f is not None:
                    feats[r["revid"]] = f

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
            rid = seq[i]["revid"]
            if rid in got:
                st[i], f = got[rid]
                cache[rid] = st[i]
                if f is not None:
                    feats[rid] = f
                if known(st[i]) and seq[i].get("sha1"):
                    by_sha[seq[i]["sha1"]] = (st[i], f)
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
        iv, last = [], None
        for a, b in zip(grid, grid[1:]):
            if known(st[a]):
                last = a
            if b - a > 1 and known(st[b]) and last is not None:
                iv.append((last, b))
        diff = [(a, b) for a, b in iv if st[a] != st[b]]
        rev_tag = [(a, b) for a, b in iv if st[a] == st[b] and any(
            "mw-reverted" in (seq[i].get("tags") or []) or set(seq[i].get("tags") or []) & A.REVERTING for i in range(a + 1, b + 1))]
        left, refined = refine_req, {"differing": 0, "revert_tagged": 0}
        for name, lst in (("differing", diff), ("revert_tagged", rev_tag)):
            for j in M2.spread(len(lst)):
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


# ------------------------------------------------------------------ sources at insertion moments
def fetch_refs(lang, revids):
    """{revid: {"d": [domains], "c": {class: n}}} of section 0 (mass2.lead_citations; named refs defined outside section 0
    are not resolved)."""
    out = {}
    for i in range(0, len(revids), 50):
        chunk = revids[i:i + 50]
        cont, pages = {}, 0
        while True:
            j = call(api_url(lang), action="query", prop="revisions", revids="|".join(map(str, chunk)), rvprop="ids|content",
                     rvslots="main", rvsection=0, **cont)
            if j.get("error"):
                raise RuntimeError(f"refs API error {j['error'].get('code')}")
            for p in (j.get("query") or {}).get("pages") or []:
                for r in p.get("revisions") or []:
                    c = (r.get("slots") or {}).get("main", {})
                    if c.get("texthidden") or "content" not in c:
                        continue
                    doms, cls = M2.lead_citations(c["content"], c["content"])
                    out[r["revid"]] = {"d": sorted(doms), "c": {k: v for k, v in cls.items() if not k.startswith("_")}}
            pages += 1
            if "continue" not in j or pages >= 5:
                break
            cont = j["continue"]
    return out


# ------------------------------------------------------------------ logs, views, talk
def protect_log(lang, titles):
    out = []
    for t in titles:
        for j in paged(api_url(lang), "protect log", action="query", list="logevents", letype="protect", letitle=t, ledir="newer",
                       lelimit="max", leprop="timestamp|details|type|comment"):
            for e in (j.get("query") or {}).get("logevents") or []:
                pr = e.get("params") or {}
                det = [{"type": d.get("type"), "level": d.get("level"), "expiry": d.get("expiry")} for d in pr.get("details") or []]
                if not det and e.get("action") in ("protect", "modify"):
                    txt = " ".join(str(x) for x in (pr.get("description"), e.get("comment")) if x)
                    det = [{"type": a.lower(), "level": lv, "expiry": "parsed"} for a, lv, _ in M2.PROT_OLD.findall(txt)]
                out.append({"ts": e.get("timestamp"), "action": e.get("action"), "details": det})
    return sorted(out, key=lambda e: e["ts"] or "")


LINK = re.compile(r"\[\[([^\]\|#]+)")


def move_candidates(raw):
    """Source titles of probable renames: null revisions (size unchanged) whose comment holds two wikilinks."""
    cands, prev = [], None
    for r in raw:
        c = r.get("comment") or ""
        if prev is not None and r.get("size") == prev and not r.get("commenthidden"):
            ls = [x.strip() for x in LINK.findall(c)]
            if len(ls) >= 2:
                cands.append(ls)
        prev = r.get("size")
    return cands


def move_log(lang, cands, resolved):
    """Verified renames since 2021: the move log of each candidate source title, keeping main-namespace moves only."""
    out, seen = [], set()
    for ls in cands:
        for src in ls[:-1]:
            if src in seen or src == resolved:
                continue
            seen.add(src)
            for j in paged(api_url(lang), "move log", max_pages=3, action="query", list="logevents", letype="move",
                           letitle=src, ledir="newer", lestart=START, lelimit="max", leprop="timestamp|title|details|type"):
                for e in (j.get("query") or {}).get("logevents") or []:
                    pr = e.get("params") or {}
                    tgt = pr.get("target_title")
                    if e.get("ns", 0) == 0 and pr.get("target_ns", 0) == 0 and tgt:
                        out.append({"ts": e.get("timestamp"), "from": e.get("title"), "to": tgt})
            break                                         # the first link that is not the current title is the source
    return sorted({(m["ts"], m["from"], m["to"]): m for m in out}.values(), key=lambda m: m["ts"] or "")


def former_titles(resolved, moves):
    seen = []
    for m in moves:
        for t in (m["from"], m["to"]):
            if t != resolved and t not in seen:
                seen.append(t)
    return seen[:6]


def pageviews(lang, titles, now=None):
    now = now or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    y, m = int(now[:4]), int(now[5:7])
    py, pm = (y, m - 1) if m > 1 else (y - 1, 12)
    end, cur = f"{py}{pm:02d}0100", f"{y}{m:02d}"
    tot, per = Counter(), {}
    for t in titles:
        j = wt_net.get_json(PV.format(lang=lang, t=quote(t.replace(" ", "_"), safe=""), end=end), {}, tries=4, ok404=True)
        items = (j or {}).get("items") if isinstance(j, dict) else None
        per[t] = None if items is None else 0
        for it in items or []:
            k = it["timestamp"][:6]
            if k < cur:
                tot[k] += it["views"]; per[t] += it["views"]
    return {"by_title_available": {t: v is not None for t, v in per.items()}, "monthly": dict(sorted(tot.items()))}


SECTION = re.compile(r"^==\s*([^=].*?)\s*==\s*$", re.M)


def discussions_dated(wt):
    """RfC / RM sections of one talk page: kind, open date (earliest signature), close date (first signature after the close
    template), closed, formal, outcome class (mass2.result_class). No headings, text or names kept."""
    out = []
    parts = SECTION.split(wt or "")
    for i in range(1, len(parts) - 1, 2):
        head, body = parts[i], parts[i + 1]
        rfc_h = bool(re.search(r"\brfc\b|request for comments?", head, re.I)); rfc_t = bool(M2.RFC_TPL.search(body[:5000]))
        rm_h = bool(re.search(r"requested move|move request", head, re.I)); rm_t = bool(M2.RM_TPL.search(body))
        if not (rfc_h or rfc_t or rm_h or rm_t):
            continue
        kind = "rfc" if (rfc_t or (rfc_h and not rm_t)) else "rm"
        sigs = []
        for mm in P.SIG.finditer(body):
            hh, mi, d, mon, y = mm.groups()
            sigs.append((f"{y}-{P.MONTHS[mon]:02d}-{int(d):02d}T{int(hh):02d}:{mi}:00Z", mm.start()))
        opened = min((s for s, _ in sigs), default=None)
        cm = P.CLOSED.search(body)
        res = P.RM_RESULT.search(body) if kind == "rm" else None
        closed_at = None
        if cm or res:
            pos = (cm or res).start()
            closed_at = next((s for s, at in sigs if at >= pos), None)
            if closed_at and opened and closed_at < opened:
                closed_at = None
        cr = M2.CLOSE_RESULT.search(body)
        rtxt = res.group(1) if res else (cr.group(1) if cr else None)
        out.append({"kind": kind, "opened": opened, "closed": bool(cm) or bool(res), "closed_at": closed_at,
                    "formal": rfc_t if kind == "rfc" else rm_t, "result": M2.result_class(rtxt)})
    return out


def rfc_scan_en(talk_title):
    """English talk page + archives touched since 2021 -> dated RfC / RM items (deduplicated on kind + open date)."""
    found, arch = [], []
    j = call(api_url("en"), action="query", prop="revisions", titles=talk_title, rvprop="content", rvslots="main")
    for p in (j.get("query") or {}).get("pages") or []:
        for r in p.get("revisions") or []:
            found += discussions_dated((r.get("slots") or {}).get("main", {}).get("content") or "")
    for j in paged(api_url("en"), "archives", max_pages=5, action="query", list="allpages", apnamespace=1,
                   apprefix=talk_title.split(":", 1)[1] + "/", aplimit="max"):
        arch += [p["title"] for p in (j.get("query") or {}).get("allpages") or []]
    recent = []
    for i in range(0, len(arch), 50):
        j = call(api_url("en"), action="query", prop="revisions", titles="|".join(arch[i:i + 50]), rvprop="timestamp")
        for p in (j.get("query") or {}).get("pages") or []:
            rr = p.get("revisions") or []
            if rr and rr[0]["timestamp"] >= START:
                recent.append(p["title"])
    recent = sorted(recent)[-MAX_ARCHIVES:]
    for i in range(0, len(recent), 5):
        for j in paged(api_url("en"), "archive content", max_pages=5, action="query", prop="revisions",
                       titles="|".join(recent[i:i + 5]), rvprop="content", rvslots="main"):
            for p in (j.get("query") or {}).get("pages") or []:
                for r in p.get("revisions") or []:
                    found += discussions_dated((r.get("slots") or {}).get("main", {}).get("content") or "")
    seen, uniq = set(), []
    for d in found:
        k = (d["kind"], d["opened"])
        if d["opened"] and k in seen:
            continue
        seen.add(k); uniq.append(d)
    return {"archives": len(arch), "archives_scanned": len(recent), "archives_truncated": len(recent) >= MAX_ARCHIVES,
            "items": sorted(uniq, key=lambda d: d["opened"] or "9")}


# ------------------------------------------------------------------ Wikidata
WD_SET = re.compile(r"/\*\s*wbset(label|description)-(add|set|remove):\d+\|([a-z\-]+)\s*\*/\s*(.*)", re.S)
WD_BULK = re.compile(r"/\*\s*(wbeditentity[\w\-]*|wbsetlabeldescriptionaliases):\d+\|\|?([a-z\-, ]*)\s*\*/")


def wikidata(qids):
    """Current labels / descriptions in LANGS and every label / description change since 2021 per language."""
    out = {"current": {}, "changes": {}}
    if not qids:
        return out
    ids = sorted(set(qids.values()))
    j = call(WD, action="wbgetentities", ids="|".join(ids), props="labels|descriptions", languages="|".join(LANGS))
    for q, e in (j.get("entities") or {}).items():
        out["current"][q] = {k: {l: (v.get("value") if isinstance(v, dict) else v) for l, v in (e.get(k) or {}).items()}
                             for k in ("labels", "descriptions")}
    for q in ids:
        ch = []
        for j in paged(WD, "wikidata history", action="query", prop="revisions", titles=q, rvprop="timestamp|comment",
                       rvdir="newer", rvstart=START, rvlimit="max"):
            for p in (j.get("query") or {}).get("pages") or []:
                for r in p.get("revisions") or []:
                    c = r.get("comment") or ""
                    m = WD_SET.search(c)
                    if m and m.group(3) in LANGS:
                        ch.append({"ts": r["timestamp"], "field": m.group(1), "action": m.group(2), "lang": m.group(3),
                                   "value": m.group(4).strip()[:250] if m.group(2) != "remove" else None})
                        continue
                    b = WD_BULK.search(c)
                    if b:
                        for l in re.split(r"[,\s]+", b.group(2) or ""):
                            if l in LANGS:
                                ch.append({"ts": r["timestamp"], "field": "label_or_description", "action": "bulk",
                                           "lang": l, "value": None})
        out["changes"][q] = ch
    return out


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


def ratchet_states(seq, title, cache, feats):
    """English page in ratchet.json: rebuild the per-revision presence sequence from its exact events, then read the voice at
    the event revisions, their parents and every revision after ratchet's run. -> (states aligned with seq or None, coverage)."""
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
    need = sorted({i for i in flips} | {i - 1 for i in flips if i > 0} | {0} | set(after))
    sub = [seq[i] for i in need]
    sst, cov = read_states("en", sub, cache, feats, full_req=10 ** 6)
    got = dict(zip(need, sst))
    last_voice = None
    mix = lambda pr, v: "".join(("0" if not pr[k] else (v[k] if v[k] != "0" else "2")) for k in range(len(FAMILIES)))
    for i in range(len(seq)):
        if i in got and known(got[i]):
            st[i] = mix(pres_seq[i], got[i]) if i < first_after else got[i]   # ratchet's presence is authoritative
            last_voice = st[i]
        elif i < first_after:
            st[i] = mix(pres_seq[i], last_voice or "2" * len(FAMILIES))
            last_voice = st[i]
    cov = {**cov, "mode": "ratchet", "ratchet_end": iso(end), "after_ratchet": len(after), "n_revs": len(seq),
           "voice_note": "voice read at event revisions, their parents and after ratchet's run; carried between them"}
    return st, cov


# ------------------------------------------------------------------ one page
def _pfile(kind, pg):
    return os.path.join(OUT, kind, f"{pg['lang']}__{slug(pg['title'])}.json" + (".gz" if kind == "pages" else ""))


def salt_check():
    return CO.h("__crosswiki_salt_check__")


def _rev_rec(r, hh):
    u = None if r.get("userhidden") else r.get("user")
    return {"revid": r["revid"], "t": r["timestamp"], "u": hh(u) if u else None, "anon": bool(u and A.ANON.match(u)),
            "bot": bool(u and A.BOT.search(u)), "hidden": not u, "size": r.get("size"), "minor": bool(r.get("minor")),
            "cc": CO.comment_classes(r.get("comment")) if not r.get("commenthidden") else ["hidden"],
            "tags": sorted(set(r.get("tags") or []) & CO.TAGS_KEEP)}


def collect_page(pg):
    lang, title = pg["lang"], pg["title"]
    H = history(lang, title)
    if H["missing"]:
        return {**pg, "missing": True, "revs": [], "events": [], "voice": [], "accounts": {}, "coverage": {}, "salt_check": salt_check()}
    resolved, raw, seed = H["resolved"], H["revs"], H["seed"]
    seq = [{"revid": r["revid"], "parentid": r.get("parentid"), "timestamp": r["timestamp"],
            "sha1": None if r.get("sha1hidden") else r.get("sha1"), "tags": r.get("tags") or [],
            "user": None if r.get("userhidden") else r.get("user")} for r in raw if r.get("revid")]
    lp = _pfile("leads", pg)
    cache, feats = {}, {}
    if os.path.exists(lp):
        L = json.load(open(lp))
        cache = {int(k): v for k, v in (L.get("s") or {}).items()}
        feats = {int(k): v for k, v in (L.get("f") or {}).items()}
    st, cov = None, None
    if lang == "en":
        for t in dict.fromkeys([resolved, title, pg.get("en_title")]):
            if t:
                st, cov = ratchet_states(seq, t, cache, feats)
                if st is not None:
                    break
    if st is None:
        st, cov = read_states(lang, seq, cache, feats)
    os.makedirs(os.path.dirname(lp), exist_ok=True)
    json.dump({"s": {str(k): v for k, v in cache.items()}, "f": {str(k): v for k, v in feats.items()}}, open(lp + ".tmp", "w"),
              ensure_ascii=False)
    os.replace(lp + ".tmp", lp)
    seed_state = seed["state"] if seed else None
    events, voice = derive_events(seq, st, seed_state)
    # sources: section-0 refs at every insertion revision and its parent (previous revision in the sequence)
    ins = [e for e in events if e["kind"] == "insert"]
    want = sorted({seq[e["i"]]["revid"] for e in ins} | {seq[e["i"] - 1]["revid"] for e in ins if e["i"] > 0} |
                  ({seed["revid"]} if seed and any(e["i"] == 0 for e in ins) else set()))
    refs = fetch_refs(lang, want) if want else {}
    for e in ins:
        cur = refs.get(seq[e["i"]]["revid"])
        prv = refs.get(seq[e["i"] - 1]["revid"]) if e["i"] > 0 else (refs.get(seed["revid"]) if seed else ({"d": [], "c": {}} if e["creation"] else None))
        if cur is not None and prv is not None:
            new = sorted(set(cur["d"]) - set(prv["d"]))
            e["refs"] = {"new_domains": new[:30], "n_new": len(new), "n_before": len(prv["d"]), "n_after": len(cur["d"]),
                         "classes_after": cur["c"], "classes_before": prv["c"]}
    # accounts: exact event makers are checked globally; the rest follow SUL (same name = same global account)
    local, acc = set(), {}
    for e in events + voice:
        u = seq[e["i"]]["user"]
        if not e["exact"] or not u or A.ANON.match(u) or A.BOT.search(u):
            continue
        rec = account_record(global_info(u), lang)
        if rec.get("looked_up") and not rec.get("global"):
            local.add(u)
        acc[u] = rec
    hh = lambda u: CO.h(u + "@" + lang) if u in local else CO.h(u)
    accounts = {hh(u): rec for u, rec in acc.items()}
    revs = []
    for i, r in enumerate(raw):
        rec = _rev_rec(r, hh)
        rec.update({"parentid": r.get("parentid"), "s": st[i]})
        if r["revid"] in feats:
            rec["f"] = feats[r["revid"]]
        revs.append(rec)
    for e in events + voice:
        r = revs[e["i"]]
        e.update({"t": r["t"], "revid": r["revid"], "u": r["u"] if e["exact"] else None, "anon": r["anon"], "bot": r["bot"]})
    # talk page (metadata only), logs, views
    talk = []
    if H.get("talkid"):
        tp, traw = revisions(lang, pageids=H["talkid"])
        talk = [_rev_rec(r, hh) for r in traw if r.get("revid")]
    moves = move_log(lang, move_candidates(raw), resolved)
    former = former_titles(resolved, moves)
    prot = protect_log(lang, [resolved] + former)
    views = pageviews(lang, [resolved] + former)
    rfc = rfc_scan_en("Talk:" + resolved) if lang == "en" else None
    for x in raw:
        x.pop("user", None); x.pop("comment", None)
    return {**pg, "resolved_title": resolved, "missing": False, "created": H["created"],
            "seed": {"state": seed_state, "ts": seed["ts"], "f": seed.get("feat")} if seed else None,
            "revs": revs, "events": events, "voice": voice, "accounts": accounts, "talk": talk, "moves": moves,
            "former_titles": former, "protection": prot, "views": views, "rfc": rfc, "coverage": cov, "salt_check": salt_check()}


# ------------------------------------------------------------------ run
def collect():
    CO.salt()
    tt = resolve_titles()
    pages = tt["pages"]
    lim = int(os.environ.get("CW_LIMIT", "0"))
    pages = pages[:lim] if lim else pages
    wp = os.path.join(OUT, "wikidata.json")
    if not os.path.exists(wp):
        wdd = wikidata(tt.get("qids") or {})
        json.dump(wdd, open(wp + ".tmp", "w"), ensure_ascii=False); os.replace(wp + ".tmp", wp)
    os.makedirs(os.path.join(OUT, "pages"), exist_ok=True)
    todo, done = [], 0
    for pg in pages:
        pf = _pfile("pages", pg)
        if os.path.exists(pf):
            try:
                if json.load(gzip.open(pf, "rt")).get("salt_check") == salt_check():
                    done += 1; continue
            except Exception:
                pass
            os.remove(pf)
        todo.append(pg)
    print(f"crosswiki: {len(pages)} pages ({dict(Counter(p['lang'] for p in pages))}), {done} reused, {len(todo)} to do", flush=True)
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
                print(f"{pg['lang']} {pg['concepts'][0]}: {len(rec['revs'])} revisions, {len(rec.get('talk') or [])} talk, "
                      f"{len(rec['events'])} term events, mode={cv.get('mode')} lead requests={cv.get('requests')}", flush=True)
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
    wp = os.path.join(OUT, "wikidata.json")
    wdd = json.load(open(wp)) if os.path.exists(wp) else {}
    ev = [e for r in recs for e in r["events"]]
    summ = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "pages_expected": len(expected),
            "pages": len(recs), "missing_pages": sum(1 for r in recs if r.get("missing")),
            "by_lang": dict(Counter(r["lang"] for r in recs)), "revisions": sum(len(r["revs"]) for r in recs),
            "talk_revisions": sum(len(r.get("talk") or []) for r in recs),
            "events": len(ev), "exact_events": sum(1 for e in ev if e["exact"]),
            "insertions_with_sources": sum(1 for e in ev if e.get("refs")),
            "lead_modes": dict(Counter((r.get("coverage") or {}).get("mode") for r in recs)),
            "moves": sum(len(r.get("moves") or []) for r in recs), "protect_entries": sum(len(r.get("protection") or []) for r in recs),
            "rfc_items": sum(len((r.get("rfc") or {}).get("items") or []) for r in recs),
            "wikidata_changes": sum(len(v) for v in (wdd.get("changes") or {}).values()),
            "accounts_with_facts": len(accounts), "local_accounts": sum(1 for v in accounts.values() if v.get("looked_up") and not v.get("global")),
            "requests": wt_net.C["requests"], "title_notes": tt.get("notes")}
    out = {"note": "Cross-wiki lead term data. Accounts are HMAC-SHA256(run salt, username)[:16], one salt for all wikis "
                   "(local, unattached accounts are hashed with the wiki code). Raw: never published.",
           "summary": summ, "langs": LANGS, "families": FAMILIES, "concepts": [c for c, _ in CONCEPTS], "qids": tt.get("qids") or {},
           "pages": recs, "accounts": accounts, "wikidata": wdd}
    with gzip.open(os.path.join(A.DATA, "crosswiki.json.gz"), "wt") as f:
        json.dump(out, f, separators=(",", ":"), ensure_ascii=False)
    json.dump(summ, open(os.path.join(A.DATA, "crosswiki_summary.json"), "w"), indent=1, ensure_ascii=False)
    print("crosswiki merged:", json.dumps(summ, indent=1, ensure_ascii=False), flush=True)
    if len(recs) < 0.95 * len(expected):
        sys.exit(f"crosswiki merge: {len(recs)}/{len(expected)} pages - incomplete")


# ------------------------------------------------------------------ estimate (offline)
# Revisions since 2021 per page relative to English (assumption: edit volume of these articles in each edition; an upper
# guess so the estimate errs high). Talk volume assumed equal to article volume. The run prints the real counts.
LANG_RATIO = {"de": .35, "he": .30, "fr": .30, "ar": .25, "es": .25, "ru": .25, "it": .15, "pt": .15, "pl": .10, "nl": .08}
EN_NEW_GUESS = {"Israeli-occupied territories": 1500, "Palestine": 4000}
NO_PAGE = {"Gaza genocide": {"de", "he", "ru"}}


def estimate(eff_rps=1.4, retry=1.15, sha_dedupe=0.85, acct_per_event=0.6, talk_ratio=1.0, en_archives=35):
    R = ratchet()
    arts = R.get("articles") or {}
    tot = Counter()
    lead_req = lambda n: (math.ceil(n * sha_dedupe / 50) + 1) if math.ceil(n * sha_dedupe / 50) <= FULL_REQ else GRID_REQ + REFINE_REQ + 1
    events, rows, n_pages = 0, [], 0
    for concept, cands in CONCEPTS:
        use = cands if concept in MULTI else cands[:1]
        en_ns = [(arts.get(c) or {}).get("revisions") or EN_NEW_GUESS.get(concept, 2000) for c in use]
        in_ratchet = any(c in arts for c in cands)
        en_ev = sum(len(v) for c in cands for t, v in ((R.get("events") or {}).get(c) or {}).items() if t in EN_TERM.values())
        pages = [("en", n) for n in en_ns] + [(l, int(sum(en_ns) * q)) for l, q in LANG_RATIO.items() if l not in NO_PAGE.get(concept, set())]
        for l, n in pages:
            n_pages += 1
            tot["metadata"] += math.ceil(n / 500) + 1
            tot["seed_creation"] += 2
            tot["talk_metadata"] += math.ceil(n * talk_ratio / 500) + 1
            tot["protect_move_log"] += 2
            tot["pageviews"] += 2
            ev_n = (en_ev // len(en_ns)) if (l == "en" and in_ratchet) else max(2, n // 60)
            events += ev_n
            tot["lead"] += (math.ceil(2 * ev_n / 50) + 2) if (l == "en" and in_ratchet) else lead_req(n)
            tot["sources"] += math.ceil(ev_n / 2 * 2 / 50) + 1
            if l == "en":
                tot["en_rfc_archives"] += 2 + math.ceil(en_archives / 50) + math.ceil(min(MAX_ARCHIVES, en_archives) / 5) * 2
        rows.append({"concept": concept, "en_revisions": sum(en_ns), "en_from_ratchet": in_ratchet})
    tot["titles"] = sum(len(c) for _, c in CONCEPTS)
    tot["wikidata"] = 1 + len(CONCEPTS) * 8
    tot["globaluserinfo"] = min(GUI_MAX, int(events * acct_per_event))
    total = sum(tot.values())
    res = {"assumptions": {"lang_ratio_vs_en": LANG_RATIO, "talk_revisions_per_article_revision": talk_ratio,
                           "sha1_dedupe": sha_dedupe, "full_read_up_to_revisions": FULL_REQ * 50,
                           "grid_plus_refine_requests_per_heavy_page": GRID_REQ + REFINE_REQ, "accounts_per_event": acct_per_event,
                           "en_archives_touched_per_talk_page": en_archives, "effective_req_per_s": eff_rps, "retry_factor": retry},
           "pages": n_pages, "concepts": rows, "requests": dict(tot), "total": total, "total_with_retries": int(total * retry),
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
