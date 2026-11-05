"""Pilot collector: new signals we have never collected, for a ~160-article sample (step 3 of the widening plan).

  python pilot.py            -> data/pilot/pilot.json + data/pilot/summary.json   (needs network; runs in CI)
  python pilot.py --sample   -> print the sample only (offline)
  PILOT_LIMIT=8 python pilot.py   -> test mode, first 8 articles

Sample (deterministic, seed 2026):
  60 topic       all KEY_ARTICLES, then a draw from corpus narrative list, then a draw from mass-frame topic rows
  40 comparison  all NARRATIVE_DISPUTES articles, topped up from KEY_ARTICLES_CONTROL     (stratum comparison_dispute)
  60 comparison  random mass-frame comparison rows                                          (stratum comparison_random)

Signals (per article; "at" = value at 2021-01-01, 2023-07-01 and now; "win" = flow inside a window):
  S1  page info now          length, watchers, protection, short description + its source (local/Wikidata), page image,
                             WikiProject assessments, Wikidata QID, redirects to the page (alternative names)
  S2  article wikitext  at   short description, infobox type/fields/caption, lead image+caption, hatnotes, maintenance and
                             dispute tags, pp-templates, explicit categories, See also, navboxes, outlinks (+ watch-list links),
                             section headings, citation classes by domain
  S3  talk wikitext     at   contentious-topic notices, WikiProject class/importance, article history (GA/FA/DYK/ITN/OTD/TFA),
                             AfD/merge/move banners, press coverage, Top-25 reports, FAQ, RfC and requested-move headings
  S4  talk archives     now  number, bytes, archives last touched per window
  S5  revisions         win  sizes (bytes added/removed), tags (mobile, VisualEditor, reverts), hidden revisions,
                             edit-summary classes (sock/ban reverts, ECR/ARBPIA, NPOV, sources, consensus, ...), page moves
  S6  talk revisions    win  volume, participants, overlap of article editors with talk participants
  S7  editor accounts   win  account age at edit, edit count, extended-confirmed, currently (indef) blocked  - aggregate only
  S8  protection log    at   edit/move protection level reconstructed from the log
  S9  moves             at   title at each date (from move null-revisions)
  S10 pageviews         win  monthly user views, all-access and desktop (mobile = all - desktop)
  S11 inbound links     now  number of articles linking here (CirrusSearch linksto:)
  S12 AfD pages         now  deletion discussions under the current title
  S13 edit-filter log   win  public abuse-filter hits on the page (attempted edits, incl. ECR enforcement)
  S14 Wikidata          at   labels / descriptions / aliases in 7 languages, sitelinks, P31
  S15 lead term events  win  lead (section 0) of every revision in w1 and w2 (capped): who inserts vs removes critical terms
                             and P/J displacement terms; account facts of inserters vs removers (aggregate), revert fate
  S16 LiftWing          win  revert-risk (language-agnostic model, no auth) for a capped sample of those insert/remove revisions
  S17 RfCs / moves      win  RfC and requested-move sections in the talk page + archives touched since 2021: count, date
                             (first signature), closed, RM result
Also at each date: citation domains of the lead's own refs, and critical-term counts with nakba/expulsion split into
Palestinian (DISP_P) vs Jewish (DISP_J) displacement (narrative.py lexicon).
Sample adds an atrocity comparison stratum (Uyghur, Rohingya, Tigray, Darfur, Yazidi, Bosnian, Masalit/El Geneina).
Records are deduplicated by resolved (canonical) title.
Privacy: no username or raw edit summary is ever stored. Editors are salted hashes (salt from WT_SALT, never written);
account facts are reduced to per-article shares. Edit summaries are reduced to class flags.
"""
import argparse, gzip, hashlib, json, os, random, re, statistics, sys, threading, time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

import requests

import wt_net

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze as A             # noqa: E402
import explore as E             # noqa: E402
import narrative as N           # noqa: E402
from corpus import KEY_ARTICLES, KEY_ARTICLES_CONTROL, NARRATIVE_DISPUTES, TREATMENT_SEED   # noqa: E402

OUT = os.path.join(HERE, "data", "pilot")
FRAME = os.path.join(HERE, "data", "mass", "frame.json")
EN = "https://en.wikipedia.org/w/api.php"
WD = "https://www.wikidata.org/w/api.php"
PV = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/{acc}/user/{t}/monthly/2021010100/{end}"
SALT = os.environ.get("WT_SALT") or os.urandom(16).hex()
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
DATES = {"2021-01-01": "2021-01-01T00:00:00Z", "2023-07-01": "2023-07-01T00:00:00Z", "now": NOW}
WAR = "2023-10-07T00:00:00Z"
WINDOWS = {"w1": ("2021-01-01T00:00:00Z", "2023-07-01T00:00:00Z"), "w2": ("2023-07-01T00:00:00Z", NOW), "war": (WAR, NOW)}
WD_LANGS = ["en", "he", "ar", "de", "fr", "ru", "es"]
MAX_PAGES = 60              # cap on paginated history requests per list (60 x 500 revisions); flagged when hit
N_TOPIC, N_DISPUTE, N_RANDOM = 60, 40, 60
SEED = 2026
ATROCITY = ["Uyghur genocide", "Rohingya genocide", "War crimes in the Tigray war", "Darfur genocide", "Yazidi genocide",
            "Bosnian genocide", "Masalit massacres", "El Geneina massacre"]
LEAD_PAGES = int(os.environ.get("PILOT_LEAD_PAGES", "40"))   # per window, 50 revisions per page (2,000 revisions)
LIFTWING = "https://api.wikimedia.org/service/lw/inference/v1/models/revertrisk-language-agnostic:predict"
LW_ON = [os.environ.get("PILOT_LIFTWING", "1") == "1"]
LW_MAX = int(os.environ.get("PILOT_LW_MAX", "12"))          # scored events per article
_lw_fail = [0, 0]                                             # [calls, failures]; disabled after 5 failures in the first 8 calls
TERMS = A.CRITICAL + ["disp_P", "disp_J"]

# links whose presence in an article (outlinks at each date) marks a framing choice; topic and comparison analogues
WATCH_LINKS = ["Nakba", "Gaza genocide", "Israeli apartheid", "Zionism as settler colonialism", "Settler colonialism",
               "Israeli occupation of the West Bank", "Israeli-occupied territories", "Occupied Palestinian territories",
               "Ethnic cleansing", "Genocide", "Apartheid", "Colonialism", "Indigenous peoples", "Antisemitism",
               "New antisemitism", "Anti-Zionism", "Zionism", "Palestinians", "State of Palestine", "1948 Palestinian expulsion and flight",
               "Jewish exodus from the Muslim world", "Land of Israel", "Jewish history", "Israelites", "Terrorism", "War crimes",
               "Armenian genocide", "Islamophobia", "Hindu nationalism", "Russian occupation of Ukraine", "Kashmir conflict",
               "Turkish occupation of Northern Cyprus", "Persecution of Uyghurs in China", "Hinduphobia", "Anti-Armenian sentiment"]
WATCH_SET = {w.lower(): w for w in WATCH_LINKS}

# edit-summary classes (applied to raw summaries in memory; only counts are kept)
CMT = {k: re.compile(v, re.I) for k, v in {
    "revert": r"\b(?:rv\w?|revert\w*|undid|undo|rollback|restor\w*)\b",
    "sock_ban": r"\b(?:sock\w*|ban ?revert\w*|WP:BAN\w*|block evasion|WP:EVADE|evad\w+|LTA|blocked (?:user|editor))\b",
    "ecr_arbpia": r"\b(?:WP:ECR|ARBECR|ECR|extended[- ]confirmed|ARBPIA\d*|WP:PIA|500/30|not EC|non-EC|CT/A-I|A-I)\b",
    "npov": r"\b(?:N?POV|WP:NPOV|neutral\w*|bias\w*|one-sided)\b",
    "sources": r"\b(?:WP:RSP?|RSP?|reliabl\w*|unreliabl\w*|unsourced|sourc\w+|citations?|cites?|cn)\b",
    "consensus": r"\b(?:consensus|WP:ONUS|ONUS|WP:BRD|BRD|talk ?page|per talk|see talk|discuss\w*|RfC|status quo|WP:QUO)\b",
    "undue": r"\b(?:WP:UNDUE|undue|weight|WP:DUE|FRINGE)\b",
    "or_synth": r"\b(?:WP:OR|original research|WP:SYNTH|SYNTH)\b",
    "vandal": r"\bvandal\w*\b",
    "voice": r"\b(?:wikivoice|WP:WIKIVOICE|WP:YESPOV|attribut\w*|in-text attribution|alleged\w*)\b",
    "lead": r"\b(?:lead|lede|first sentence|opening sentence|MOS:LEAD|LEADFOLLOWSBODY|WP:LEAD)\b",
    "title_name": r"\b(?:rename\w*|retitle\w*|WP:COMMONNAME|COMMONNAME|terminology|wording)\b",
}.items()}
MOVE = re.compile(r"moved page \[\[([^\]]+)\]\] to \[\[([^\]]+)\]\](?:\s*(?:over redirect|over a redirect))?(?::\s*(.*))?", re.I | re.S)
RM_REASON = re.compile(r"requested move|WP:RM|\bRM\b|move request|closed|consensus|per discussion", re.I)
SECTION_ONLY = re.compile(r"^\s*/\*.*?\*/\s*$")

HATNOTES = {"main", "main article", "about", "for", "other uses", "distinguish", "redirect", "further", "see also", "hatnote",
            "other people", "redirect-distinguish", "for multi", "about-distinguish", "selfref", "broader", "details", "redirect2"}
MAINT = {"pov", "npov", "pov section", "pov statement", "pov-check", "disputed", "disputed inline", "disputed section", "dubious",
         "unbalanced", "unbalanced section", "neutrality", "undue weight", "undue", "undue weight section", "undue-inline",
         "contradictory", "self-contradictory", "citation needed", "cn", "fact", "better source needed", "better source",
         "unreliable source?", "according to whom", "by whom", "who", "weasel", "weasel inline", "peacock", "peacock inline",
         "lead too long", "lead too short", "lead rewrite", "update", "recentism", "cleanup", "original research", "or",
         "synthesis", "synthesis inline", "globalize", "fringe theories", "systemic bias", "one source", "primary sources",
         "third-party", "too few opinions", "missing information", "controversial", "toofewopinions", "copy edit", "tone"}
DISPUTE_TAGS = {"pov", "npov", "pov section", "pov statement", "pov-check", "disputed", "disputed section", "unbalanced",
                "unbalanced section", "neutrality", "undue weight", "undue", "undue weight section", "contradictory",
                "systemic bias", "fringe theories", "too few opinions", "toofewopinions"}
NON_NAVBOX = re.compile(r"^(?:reflist|refend|refbegin|references|notelist|notes|authority control|portal|portal bar|portals|commons|"
                        r"commons category|commonscat|wikiquote|wiktionary|wikisource|sister project links|taxonbar|coord|clear|"
                        r"defaultsort|short description|good article|featured article|pp\S*|div col|div col end|col-begin|col-end|"
                        r"use \w+ dates|use \w+ english|cite\b.*|webarchive|official website|subject bar|stack end|-|clr|s-end|"
                        r"spoken wikipedia.*|library resources box|wikivoyage|wikinews|wikibooks|dmoz|curlie|tfa title|"
                        r"italic title|lowercase title|engvarb|good article|featured list|external links|ref\w*)$", re.I)
CT_NAME = re.compile(r"contentious|arbitration|arbpia|discretionary|^ds/|^ct/|community sanctions|^gs/|general sanctions|"
                     r"^calm$|controversial|round in circles|^faq$|^1rr|editnotice|^american politics|^ipa$|^aa2|^arbcom", re.I)
NS_PREFIX = re.compile(r"^(?:file|image|category|wikipedia|wp|template|help|portal|user|user talk|talk|special|draft|module|"
                       r"mediawiki|wikt|wiktionary|commons|s|q|n|b|v|voy|species|meta|m|mw|d|wikidata|w|[a-z]{2,3}(?:-[a-z]+)?)\s*:", re.I)


# ------------------------------------------------------------------ HTTP
class Missing(Exception):
    pass


def q(params, url=EN, core=True):
    """One API call. Network failure after retries -> exception (article error, retried on resume).
    Non-retryable API error -> exception if core, else None (recorded as a missing signal)."""
    p = {**params, "format": "json", "formatversion": 2}
    j = wt_net.get_json(url, p)
    if j is None:
        raise RuntimeError(f"request failed after retries: {params.get('action')} {params.get('prop') or params.get('list')} "
                           f"{params.get('titles') or params.get('aftitle') or params.get('letitle') or params.get('srsearch') or ''}"[:200])
    if isinstance(j, dict) and j.get("error"):
        if core:
            raise RuntimeError(f"API error {j['error'].get('code')}: {params.get('prop') or params.get('list')}")
        return None
    return j


def paged(params, url=EN, core=True, max_pages=MAX_PAGES):
    """Yield successive result pages following `continue`. Last item yielded is a dict {'_truncated': bool}."""
    cont, n = {}, 0
    while True:
        j = q({**params, **cont}, url, core)
        if j is None:
            yield {"_failed": True}; return
        yield j
        n += 1
        if "continue" not in j:
            yield {"_truncated": False}; return
        if n >= max_pages:
            yield {"_truncated": True}; return
        cont = j["continue"]


def h(u):
    return hashlib.sha256((SALT + u).encode()).hexdigest()[:12]


def ep(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()


def in_win(ts, w):
    a, b = WINDOWS[w]
    return a <= ts < b or (w != "w1" and ts == b)


def months(w):
    a, b = WINDOWS[w]
    return max(1e-9, (ep(b) - ep(a)) / (86400 * 30.4375))


# ------------------------------------------------------------------ wikitext parsing
_BR = re.compile(r"[{}]")
_BR2 = re.compile(r"[{}\[\]|]")


def templates(wt):
    """All templates (nested included): list of (start, name, inner_text). Skips {{{params}}} and parser functions."""
    out, stack, i, n = [], [], 0, len(wt)
    while True:
        m = _BR.search(wt, i)
        if not m:
            break
        i = m.start()
        two = wt[i:i + 2]
        if two == "{{":
            if wt[i:i + 3] == "{{{":
                stack.append((i, True)); i += 3; continue
            stack.append((i, False)); i += 2; continue
        if two == "}}" and stack:
            s, triple = stack.pop()
            if triple and wt[i:i + 3] == "}}}":
                i += 3; continue
            if not triple:
                inner = wt[s + 2:i]
                name = re.split(r"[|\n]", inner, 1)[0].strip()
                if name and not name.startswith("#"):
                    out.append((s, norm_name(name), inner))
            i += 2; continue
        i += 1
    return sorted(out, key=lambda x: x[0])


def norm_name(name):
    name = re.sub(r"<!--.*?-->", "", name, flags=re.S)
    name = re.sub(r"^(?:template|subst|safesubst|msgnw)\s*:", "", name.strip(), flags=re.I)
    return re.sub(r"[\s_]+", " ", name).strip().lower()


def split_top(s, sep="|"):
    """Split on top-level pipes (not inside {{ }} or [[ ]])."""
    parts, dc, dl, start, i = [], 0, 0, 0, 0
    while True:
        m = _BR2.search(s, i)
        if not m:
            break
        i = m.start(); two = s[i:i + 2]
        if two == "{{": dc += 1; i += 2; continue
        if two == "}}": dc -= 1; i += 2; continue
        if two == "[[": dl += 1; i += 2; continue
        if two == "]]": dl -= 1; i += 2; continue
        if s[i] == sep and dc <= 0 and dl <= 0:
            parts.append(s[start:i]); start = i + 1
        i += 1
    parts.append(s[start:])
    return parts


def file_link(wt):
    """First [[File:...]] in wt: (file name, caption) using bracket matching (no backtracking regex)."""
    m = re.search(r"\[\[\s*(?:File|Image)\s*:", wt, re.I)
    if not m:
        return None
    depth, i = 0, m.start()
    while i < len(wt) - 1:
        two = wt[i:i + 2]
        if two == "[[": depth += 1; i += 2; continue
        if two == "]]":
            depth -= 1; i += 2
            if depth == 0:
                break
            continue
        i += 1
    parts = split_top(wt[m.start() + 2:i - 2])
    fname = parts[0].split(":", 1)[1].strip().replace("_", " ")
    cap = next((p for p in reversed(parts[1:]) if p.strip() and not re.match(
        r"\s*(?:thumb|thumbnail|frame|frameless|left|right|center|centre|upright[=\d.]*|x?\d+(?:x\d+)?px|alt=.*|border|none|link=.*|lang=.*)\s*$", p, re.I)), None)
    return fname, cap


def tparams(inner):
    parts = split_top(inner)[1:]
    pos, named = [], {}
    for p in parts:
        m = re.match(r"\s*([^=\[\]{}]+?)\s*=(.*)", p, re.S)
        if m:
            named[m.group(1).strip().lower()] = m.group(2).strip()
        else:
            pos.append(p.strip())
    return pos, named


def clean(s, n=300):
    s = A.prose(s or "") if s else ""
    return re.sub(r"\s+", " ", s).strip()[:n]


def link_target(t):
    t = t.split("|", 1)[0].split("#", 1)[0].strip().replace("_", " ")
    t = re.sub(r"\s+", " ", t)
    if not t or t.startswith(":") or NS_PREFIX.match(t):
        return None
    return t[0].upper() + t[1:]


def wikilinks(wt):
    wt = re.sub(r"<!--.*?-->", "", wt, flags=re.S)
    return {x for x in (link_target(m) for m in re.findall(r"\[\[([^\[\]]+)\]\]", wt)) if x}


def section(wt, title_rx):
    m = re.search(r"^==\s*" + title_rx + r"\s*==\s*$", wt, re.M | re.I)
    if not m:
        return None
    rest = wt[m.end():]
    m2 = re.search(r"^==[^=]", rest, re.M)
    return rest[:m2.start()] if m2 else rest


def parse_article(wt):
    if wt is None:
        return None
    if re.match(r"\s*#redirect", wt, re.I):
        return {"redirect": True}
    tps = templates(wt)
    lead = A.split_lead(wt)
    lead_end = len(lead)
    names = Counter(n for _, n, _ in tps)
    sd = next((tparams(inner)[0][0] if tparams(inner)[0] else "" for _, n, inner in tps if n == "short description"), None)
    if sd is None:
        m = re.search(r"\{\{\s*SHORTDESC\s*:([^}]*)\}\}", wt, re.I)
        sd = m.group(1).strip() if m else None
    info = None
    for s, n, inner in tps:
        if s < lead_end and n.startswith("infobox"):
            pos, named = tparams(inner)
            img = next((named[k] for k in ("image", "image_name", "image_map", "image_flag", "flag", "image1", "logo", "map")
                        if named.get(k)), None)
            cap = next((named[k] for k in ("caption", "image_caption", "map_caption", "imagecaption", "alt") if named.get(k)), None)
            info = {"type": n, "n_fields": sum(1 for v in named.values() if v),
                    "fields": {k: clean(v, 150) for k, v in named.items() if v and not re.match(r"(?:image|logo|map|flag)\w*_?(?:size|alt|upright)$", k)},
                    "image": clean_file(img), "caption": clean(cap, 300) if cap else None}
            break
    lead_img = None
    if info and info["image"]:
        lead_img = {"file": info["image"], "caption": info["caption"], "via": "infobox"}
    else:
        fl = file_link(lead)
        if fl:
            lead_img = {"file": fl[0][:200], "caption": clean(fl[1], 300) if fl[1] else None, "via": "lead"}
    see = section(wt, r"see also")
    tail_start = [m.start() for m in re.finditer(r"^==[^=].*?==\s*$", wt, re.M)]
    tail = wt[tail_start[-1]:] if tail_start else ""
    navboxes = sorted({norm_name(x) for x in re.findall(r"^\{\{\s*([^{}|\n]+?)\s*\}\}\s*$", tail, re.M)
                       if not NON_NAVBOX.match(norm_name(x))})
    links = wikilinks(wt)
    lead_links = wikilinks(lead)
    heads = [re.sub(r"\s+", " ", clean(x, 120)) for x in re.findall(r"^={2,3}\s*([^=].*?)\s*={2,3}\s*$", wt, re.M)]
    refs = E.refs_of(wt)
    fp = A.prose(wt)
    lp = A.prose(lead)
    return {"bytes": len(wt.encode("utf-8")), "short_desc": sd,
            "infobox": info, "lead_image": lead_img,
            "hatnotes": sorted({n for s, n, _ in tps if s < lead_end and n in HATNOTES}),
            "lead_templates": sorted({n for s, n, _ in tps if s < lead_end and not n.startswith("cite") and n not in ("efn", "sfn", "r", "refn")})[:80],
            "maint": {n: c for n, c in names.items() if n in MAINT},
            "dispute_tag": any(n in DISPUTE_TAGS for n in names),
            "pp": sorted({n for n in names if re.match(r"pp(?:-|$)", n)}),
            "categories": sorted({re.sub(r"\s+", " ", c.split("|")[0].strip().replace("_", " "))
                                  for c in re.findall(r"\[\[\s*Category\s*:([^\]]+)\]\]", wt, re.I)}),
            "see_also": sorted(wikilinks(see)) if see is not None else None,
            "navboxes": navboxes,
            "n_links": len(links), "links": sorted(links),
            "watch_links": sorted(WATCH_SET[l.lower()] for l in links if l.lower() in WATCH_SET),
            "watch_links_lead": sorted(WATCH_SET[l.lower()] for l in lead_links if l.lower() in WATCH_SET),
            "headings": heads[:150], "n_sections": len(heads),
            "refs": dict(refs), "lead_refs": dict(E.refs_of(lead)), "lead_words": len(lp.split()), "lead_links": len(lead_links),
            "full_words": len(fp.split()), "lex_lead": lex(lp), "lex_full": lex(fp)}


def lex(p):
    """Critical-term counts (analyze.py lexicon) plus Palestinian vs Jewish displacement counted separately."""
    out = {k: A.count(k, p) for k in A.CRITICAL}
    out["disp_P"] = len(N.DISP_P.findall(p)); out["disp_J"] = len(N.DISP_J.findall(p))
    return out


def clean_file(s):
    if not s:
        return None
    s = re.sub(r"^\s*\[\[(?:File|Image):", "", s, flags=re.I)
    s = re.sub(r"^(?:File|Image):", "", s.strip(), flags=re.I)
    return re.split(r"[|\]]", s)[0].strip().replace("_", " ")[:200] or None


def parse_talk(wt):
    if wt is None:
        return None
    if re.match(r"\s*#redirect", wt, re.I):
        return {"redirect": True}
    tps = templates(wt)
    first_head = re.search(r"^==[^=]", wt, re.M)
    hdr_end = first_head.start() if first_head else len(wt)
    names = Counter(n for _, n, _ in tps)
    projects, cls = {}, None
    ct, ah, dyk, itn, otd, afd, merges, moves, press, top25 = [], None, [], [], [], [], [], 0, [], 0
    for s, n, inner in tps:
        pos, named = tparams(inner)
        if n in ("wikiproject banner shell", "wpbs", "wikiprojectbannershell", "wikiproject banners", "banner shell", "wpb"):
            cls = cls or (named.get("class") or "").strip().lower() or None
        elif n.startswith("wikiproject ") or n.startswith("wp "):
            proj = n.split(" ", 1)[1]
            projects[proj] = (named.get("importance") or "").strip().lower() or None
            if named.get("class") and not cls:
                cls = named["class"].strip().lower()
        if s < hdr_end and CT_NAME.search(n):
            ct.append({"t": n, "topic": (named.get("topic") or (pos[0] if pos else "") or "").strip().lower()[:20]})
        if n in ("article history", "articlehistory", "article milestones"):
            acts = []
            for k in sorted(named, key=lambda k: (len(k), k)):
                m = re.match(r"action(\d+)$", k)
                if m:
                    i = m.group(1)
                    acts.append({"a": named[k].strip().upper()[:10], "date": clean(named.get(f"action{i}date"), 40),
                                 "result": (named.get(f"action{i}result") or "").strip().lower()[:30]})
            ah = {"actions": acts, "status": (named.get("currentstatus") or "").strip().upper()[:12] or None,
                  "dyk": clean(named.get("dykdate"), 40) or None,
                  "itn": [clean(named[k], 40) for k in named if re.match(r"itndate\d*$", k) and named[k]],
                  "otd": [clean(named[k], 40) for k in named if re.match(r"otd\d*date$|otddate\d*$", k) and named[k]],
                  "tfa": clean(named.get("maindate"), 40) or None}
        elif n in ("dyk talk", "dyktalk"):
            dyk.append(" ".join(pos[:2])[:40])
        elif n in ("itn talk", "itntalk"):
            itn += [clean(v, 40) for k, v in named.items() if re.match(r"date\d*$", k) and v] + [clean(p, 40) for p in pos if p]
        elif n in ("on this day", "onthisday", "otd talk"):
            otd += [clean(v, 40) for k, v in named.items() if re.match(r"date\d*$", k) and v]
        elif n in ("old afd multi", "old afd", "oldafdmulti", "old afd full", "afd-merged-from", "old xfd multi", "old prod", "old prod full",
                   "oldafdfull", "old xfd"):
            res = [v.strip().lower()[:30] for k, v in named.items() if re.match(r"result\d*$", k)] or [n]
            afd += [{"t": n, "result": r} for r in res]
        elif n in ("merged-from", "merged-to", "old merge", "merge from", "merge to", "merge", "mergedfrom", "merged from", "afd-merged-to",
                   "merge portion from", "merged-from multi"):
            merges.append(n)
        elif n in ("old moves", "old move", "old requested move", "oldmoves", "old rm", "moved", "moved from", "old move multi"):
            idx = {re.sub(r"^\D+", "", kk) for kk in named if re.match(r"(?:title|from|date|result|link|destination)\d*$", kk)}
            moves += max(1, len(idx))
        elif n in ("press", "press 2", "press coverage", "presscoverage", "press multi"):
            orgs = [(clean(v, 60), clean(named.get(re.sub(r"org", "date", k)), 30)) for k, v in named.items() if re.match(r"org\d*$", k) and v]
            press += [{"org": o, "date": d} for o, d in orgs] or [{"org": None, "date": None}]
        elif n in ("top 25 report", "top25", "top 25"):
            top25 += max(1, len([p for p in pos if p]))
    heads = re.findall(r"^==\s*([^=].*?)\s*==\s*$", wt, re.M)
    return {"bytes": len(wt.encode("utf-8")), "threads": len(heads),
            "header_templates": sorted({n for s, n, _ in tps if s < hdr_end})[:80],
            "class": cls, "projects": projects, "ct": ct, "ct_notice": bool(ct), "article_history": ah,
            "dyk": dyk, "itn": itn, "otd": otd, "afd": afd, "merges": merges, "old_moves": moves, "press": press[:60],
            "n_press": len(press), "top25": top25, "faq": "faq" in names,
            "rfc_active": names.get("rfc", 0) + names.get("rfc top", 0),
            "rfc_headings": sum(1 for x in heads if re.search(r"\brfc\b|request for comment", x, re.I)),
            "rm_headings": sum(1 for x in heads if re.search(r"requested move|move request|\brm\b", x, re.I))}


def parse_wikidata(content):
    if not content:
        return None
    try:
        e = json.loads(content)
    except ValueError:
        return None
    pick = lambda d: {l: (d.get(l) or {}).get("value") for l in WD_LANGS if d.get(l)}
    al = e.get("aliases") or {}
    claims = e.get("claims") or {}
    return {"labels": pick(e.get("labels") or {}), "descriptions": pick(e.get("descriptions") or {}),
            "aliases": {l: [a.get("value") for a in al.get(l, [])][:30] for l in WD_LANGS if al.get(l)},
            "n_sitelinks": len(e.get("sitelinks") or {}), "n_claims": sum(len(v) for v in claims.values()) if isinstance(claims, dict) else 0,
            "p31": [c.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id") for c in (claims.get("P31") or [])
                    if isinstance(claims, dict)][:10]}


# ------------------------------------------------------------------ collectors
def page_info(title):
    rec, redirs = None, []
    for j in paged({"action": "query", "titles": title, "redirects": 1,
                    "prop": "info|pageprops|description|pageassessments|pageimages|redirects",
                    "inprop": "protection|watchers|visitingwatchers|talkid", "ppprop": "wikibase_item|disambiguation",
                    "piprop": "name", "rdlimit": "max", "rdnamespace": 0, "rdprop": "title", "palimit": "max"}, max_pages=5):
        if "_truncated" in j:
            if rec is not None:
                rec["redirects_truncated"] = j["_truncated"]
            break
        pages = j.get("query", {}).get("pages") or [{}]
        p = pages[0]
        if p.get("missing") or p.get("invalid"):
            raise Missing(title)
        if rec is None:
            pp = p.get("pageprops") or {}
            rec = {"title": p["title"], "pageid": p.get("pageid"), "length": p.get("length"),
                   "watchers": p.get("watchers"), "visitingwatchers": p.get("visitingwatchers"),
                   "protection": [{"type": x.get("type"), "level": x.get("level"), "expiry": x.get("expiry")} for x in p.get("protection") or []],
                   "description": p.get("description"), "description_source": p.get("descriptionsource"),
                   "pageimage": p.get("pageimage"), "assessments": p.get("pageassessments") or {},
                   "qid": pp.get("wikibase_item"), "disambiguation": "disambiguation" in pp,
                   "talk_exists": bool(p.get("talkid"))}
        redirs += [r["title"] for r in p.get("redirects") or []]
    rec["redirects"] = sorted(set(redirs)); rec["n_redirects"] = len(rec["redirects"])
    return rec


def wikitext_at(title, date, url=EN, core=True):
    j = q({"action": "query", "prop": "revisions", "titles": title, "rvlimit": 1, "rvdir": "older", "rvstart": date,
           "rvprop": "ids|timestamp|content", "rvslots": "main"}, url, core)
    if j is None:
        return None, None
    p = (j.get("query", {}).get("pages") or [{}])[0]
    if p.get("missing") or not p.get("revisions"):
        return None, None
    r = p["revisions"][0]
    c = (r.get("slots") or {}).get("main", {})
    if c.get("texthidden") or "content" not in c:
        return {"revid": r.get("revid"), "ts": r.get("timestamp"), "hidden": True}, None
    return {"revid": r.get("revid"), "ts": r.get("timestamp")}, c.get("content")


def history(title, props, start="2021-01-01T00:00:00Z", core=True):
    revs, trunc = [], False
    for j in paged({"action": "query", "prop": "revisions", "titles": title, "rvprop": props, "rvdir": "newer",
                    "rvstart": start, "rvlimit": "max"}, core=core):
        if "_truncated" in j:
            trunc = j["_truncated"]; break
        if "_failed" in j:
            return None, False
        p = (j.get("query", {}).get("pages") or [{}])[0]
        revs += p.get("revisions") or []
    return revs, trunc


def rev_aggregates(revs, prev_size=None):
    """Per window: sizes, tags, hidden, summary classes; moves list. Raw summaries and usernames are dropped here."""
    win = {w: Counter() for w in WINDOWS}
    tags = {w: Counter() for w in WINDOWS}
    eds = {w: Counter() for w in WINDOWS}
    moves, last = [], prev_size
    created = None
    for r in revs:
        ts = r["timestamp"]; size = r.get("size"); u = r.get("user") or ""
        if r.get("parentid") == 0:
            created = ts
        delta = (size - last) if size is not None and last is not None else None
        last = size if size is not None else last
        cm = r.get("comment") or ""
        tg = set(r.get("tags") or [])
        mv = MOVE.search(cm)
        if mv:
            moves.append({"ts": ts, "from": mv.group(1).strip(), "to": mv.group(2).strip(), "rm": bool(RM_REASON.search(mv.group(3) or ""))})
        anon = bool(A.ANON.match(u)) if u else False
        bot = bool(A.BOT.search(u)) if u else False
        for w in WINDOWS:
            if not in_win(ts, w):
                continue
            c = win[w]
            c["edits"] += 1
            c["reverted"] += "mw-reverted" in tg
            c["reverting"] += bool(tg & A.REVERTING)
            c["minor"] += bool(r.get("minor"))
            c["anon"] += anon; c["bot"] += bot
            c["mobile"] += bool({"mobile edit", "mobile web edit", "mobile app edit"} & tg)
            c["visualeditor"] += any(t.startswith("visualeditor") for t in tg)
            c["hidden"] += bool(r.get("userhidden") or r.get("commenthidden") or r.get("texthidden") or r.get("suppressed") or r.get("sha1hidden"))
            c["empty_summary"] += (not cm and not r.get("commenthidden"))
            c["section_only_summary"] += bool(SECTION_ONLY.match(cm))
            for k, rx in CMT.items():
                c[f"cmt_{k}"] += bool(rx.search(cm))
            if delta is not None:
                if delta > 0: c["bytes_added"] += delta
                else: c["bytes_removed"] += -delta
                c["big_add"] += delta >= 2000; c["big_remove"] += delta <= -2000
            for t in tg:
                tags[w][t] += 1
            if u and not anon and not bot:
                eds[w][u] += 1
    out = {}
    for w in WINDOWS:
        c = dict(win[w]); e = eds[w]; n = sum(e.values())
        c["editors"] = len(e)
        c["top1_share"] = (max(e.values()) / n) if n else None
        c["edits_per_month"] = c.get("edits", 0) / months(w)
        c["tags"] = dict(tags[w].most_common(25))
        out[w] = c
    return out, moves, eds, created


_ucache, _ulock = {}, threading.Lock()


def user_facts(names):
    """Account facts for a set of usernames: registration, edit count, groups, block. Cached in memory only."""
    with _ulock:
        todo = sorted(n for n in names if n not in _ucache)
    for i in range(0, len(todo), 50):
        chunk = todo[i:i + 50]
        j = q({"action": "query", "list": "users", "ususers": "|".join(chunk), "usprop": "editcount|registration|groups|blockinfo"}, core=False)
        got = {}
        for u in (j or {}).get("query", {}).get("users", []):
            if u.get("missing") or u.get("invalid"):
                got[u.get("name")] = None; continue
            got[u["name"]] = {"reg": u.get("registration"), "ec": u.get("editcount"),
                              "ext": bool({"extendedconfirmed", "sysop"} & set(u.get("groups") or [])),
                              "blocked": "blockid" in u, "indef": "blockid" in u and str(u.get("blockexpiry")) in ("infinite", "infinity")}
        with _ulock:
            for n in chunk:
                _ucache[n] = got.get(n)
    with _ulock:
        return {n: _ucache.get(n) for n in names}


def user_aggregates(revs):
    users = {r.get("user") for r in revs if r.get("user") and not A.ANON.match(r["user"]) and not A.BOT.search(r["user"])}
    facts = user_facts(users) if users else {}
    out = {}
    for w in WINDOWS:
        c, ages, n = Counter(), [], 0
        for r in revs:
            u = r.get("user")
            if not u or not in_win(r["timestamp"], w) or u not in facts or facts[u] is None:
                continue
            f = facts[u]; n += 1
            age = (ep(r["timestamp"]) - ep(f["reg"])) / 86400 if f["reg"] else 9999.0
            ages.append(age)
            c["age_lt30"] += age < 30; c["age_lt365"] += age < 365
            c["ec_now"] += f["ext"]; c["editcount_lt500"] += (f["ec"] or 0) < 500; c["editcount_lt100"] += (f["ec"] or 0) < 100
            c["blocked_now"] += f["blocked"]; c["indef_now"] += f["indef"]
        out[w] = {"n_edits": n, **{f"share_{k}": (c[k] / n if n else None) for k in
                                  ("age_lt30", "age_lt365", "ec_now", "editcount_lt500", "editcount_lt100", "blocked_now", "indef_now")},
                  "median_age_days": statistics.median(ages) if ages else None,
                  "distinct": len({r.get("user") for r in revs if r.get("user") in facts and facts.get(r["user"]) and in_win(r["timestamp"], w)})}
    return out


def protection_at(log, date):
    state = {}
    for e in sorted(log, key=lambda e: e["ts"]):
        if e["ts"] > date:
            break
        if e["action"] == "unprotect":
            state = {}
        elif e["action"] in ("protect", "modify", "move_prot"):
            if e["action"] != "move_prot":
                state = {}
            for d in e.get("details") or []:
                state[d.get("type")] = (d.get("level"), d.get("expiry"))
    out = {}
    for t, (lev, exp) in state.items():
        if exp and exp not in ("infinite", "infinity") and exp < date:
            continue
        out[t] = lev
    return out


def protect_log(title):
    log = []
    for j in paged({"action": "query", "list": "logevents", "letype": "protect", "letitle": title, "ledir": "newer",
                    "lelimit": "max", "leprop": "timestamp|details|type|user"}, core=False, max_pages=5):
        if "_truncated" in j or "_failed" in j:
            if "_failed" in j: return None
            break
        for e in j.get("query", {}).get("logevents", []):
            pr = e.get("params") or {}
            log.append({"ts": e.get("timestamp"), "action": e.get("action"),
                        "details": [{"type": d.get("type"), "level": d.get("level"), "expiry": d.get("expiry")} for d in pr.get("details") or []],
                        "by": h(e["user"]) if e.get("user") else None})
    return log


def abuse_log(title):
    hits = []
    for j in paged({"action": "query", "list": "abuselog", "aftitle": title, "afdir": "newer", "afstart": "2021-01-01T00:00:00Z",
                    "aflimit": "max", "afprop": "ids|filter|user|timestamp|result"}, core=False, max_pages=6):
        if "_failed" in j:
            return None
        if "_truncated" in j:
            break
        for e in j.get("query", {}).get("abuselog", []):
            u = e.get("user") or ""
            hits.append({"ts": e.get("timestamp"), "filter": (e.get("filter") or "")[:80], "result": e.get("result") or "",
                         "anon": bool(A.ANON.match(u)), "u": h(u) if u else None})
    out = {}
    for w in WINDOWS:
        hw = [x for x in hits if x["ts"] and in_win(x["ts"], w)]
        out[w] = {"hits": len(hw), "disallowed": sum("disallow" in x["result"] for x in hw), "anon_share": (sum(x["anon"] for x in hw) / len(hw)) if hw else None,
                  "distinct_actors": len({x["u"] for x in hw if x["u"]}), "filters": dict(Counter(x["filter"] for x in hw).most_common(8))}
    return out


def pageviews(title):
    t = requests.utils.quote(title.replace(" ", "_"), safe="")
    end = time.strftime("%Y%m0100", time.gmtime())
    res = {}
    for acc in ("all-access", "desktop"):
        j = wt_net.get_json(PV.format(acc=acc, t=t, end=end), {}, tries=4, ok404=True)
        res[acc] = {i["timestamp"][:6]: i["views"] for i in j["items"]} if j and "items" in j else None
    return res


def linksto(title):
    j = q({"action": "query", "list": "search", "srsearch": 'linksto:"%s"' % title.replace('"', '\\"'), "srnamespace": 0,
           "srlimit": 1, "srinfo": "totalhits", "srprop": ""}, core=False)
    return None if j is None else (j.get("query", {}).get("searchinfo") or {}).get("totalhits")


def afd_pages(title):
    j = q({"action": "query", "list": "allpages", "apnamespace": 4, "apprefix": f"Articles for deletion/{title}", "aplimit": 50}, core=False)
    if j is None:
        return None
    pre = f"Wikipedia:Articles for deletion/{title}"
    return [p["title"][len("Wikipedia:Articles for deletion/"):] for p in j.get("query", {}).get("allpages", [])
            if p["title"] == pre or p["title"].startswith(pre + " (")]


def talk_archives(title):
    pages = {}
    for j in paged({"action": "query", "generator": "allpages", "gapnamespace": 1, "gapprefix": f"{title}/", "gaplimit": "max",
                    "prop": "info|revisions", "rvprop": "timestamp"}, core=False, max_pages=10):
        if "_failed" in j:
            return None
        if "_truncated" in j:
            break
        for p in j.get("query", {}).get("pages", []) or []:
            d = pages.setdefault(p["pageid"], {"title": p["title"]})
            if p.get("length") is not None: d["length"] = p["length"]
            if p.get("revisions"): d["ts"] = p["revisions"][0]["timestamp"]
    arch = [p for p in pages.values() if re.search(r"/archive", p["title"], re.I)]
    return {"_pages": [(p["title"], p.get("ts")) for p in arch], "n": len(arch), "bytes": sum(p.get("length") or 0 for p in arch), "n_subpages": len(pages),
            "touched": {w: sum(1 for p in arch if p.get("ts") and in_win(p["ts"], w)) for w in WINDOWS},
            "bytes_touched": {w: sum(p.get("length") or 0 for p in arch if p.get("ts") and in_win(p["ts"], w)) for w in WINDOWS}}


MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August", "September",
                                      "October", "November", "December"], 1)}
SIG = re.compile(r"(\d{1,2}):(\d{2}), (\d{1,2}) (" + "|".join(MONTHS) + r") (\d{4}) \(UTC\)")
CLOSED = re.compile(r"\{\{\s*(?:closed rfc top|rfc top|archive top|atop|discussion top|dtop|closed top|hidden archive top|rm top|requested move/end)"
                    r"|the following (?:discussion|request for comments?) is (?:closed|an archived)", re.I)
RM_RESULT = re.compile(r"result of the move request was:?\s*'*\s*([a-z ]{2,30}?)\s*'{2,}", re.I)


def sig_ts(text):
    m = SIG.search(text)
    if not m:
        return None
    hh, mm, d, mon, y = m.groups()
    return f"{y}-{MONTHS[mon]:02d}-{int(d):02d}T{int(hh):02d}:{mm}:00Z"


def discussions(wt):
    """RfC and requested-move sections of one talk page: [{kind, ts, closed, result}]. No headings or names kept."""
    out = []
    parts = re.split(r"^==\s*([^=].*?)\s*==\s*$", wt, flags=re.M)
    for i in range(1, len(parts) - 1, 2):
        head, body = parts[i], parts[i + 1]
        rfc = bool(re.search(r"\brfc\b|request for comments?", head, re.I) or re.search(r"\{\{\s*rfc\s*[|}]|rfcid\s*=", body[:3000], re.I))
        rm = bool(re.search(r"requested move|move request", head, re.I) or re.search(r"\{\{\s*requested move/dated", body[:3000], re.I))
        if not (rfc or rm):
            continue
        res = RM_RESULT.search(body)
        out.append({"kind": "rfc" if rfc else "rm", "ts": sig_ts(body), "closed": bool(CLOSED.search(body)),
                    "result": res.group(1).strip().lower() if (rm and res) else None})
    return out


def rfc_scan(now_talk_wt, arch_pages, max_archives=60):
    """Scan the current talk page and archives last touched since 2021 for RfCs / RMs, dated by first signature."""
    found = discussions(now_talk_wt or "")
    recent = sorted((t for t, ts in arch_pages if ts and ts >= WINDOWS["w1"][0]), reverse=True)
    trunc = len(recent) > max_archives
    recent = recent[:max_archives]
    for i in range(0, len(recent), 10):
        for j in paged({"action": "query", "prop": "revisions", "titles": "|".join(recent[i:i + 10]), "rvprop": "content",
                        "rvslots": "main"}, core=False, max_pages=5):
            if "_failed" in j:
                return None
            if "_truncated" in j:
                break
            for p in j.get("query", {}).get("pages", []) or []:
                for r in p.get("revisions") or []:
                    c = (r.get("slots") or {}).get("main", {}).get("content")
                    if c:
                        found += discussions(c)
    seen, uniq = set(), []
    for d in found:                                   # the same section can sit on two pages mid-archiving
        k = (d["kind"], d["ts"])
        if d["ts"] and k in seen:
            continue
        seen.add(k); uniq.append(d)
    out = {"archives_scanned": len(recent), "archives_truncated": trunc, "undated": sum(1 for d in uniq if not d["ts"])}
    for w in WINDOWS:
        dw = [d for d in uniq if d["ts"] and in_win(d["ts"], w)]
        rf = [d for d in dw if d["kind"] == "rfc"]; rm = [d for d in dw if d["kind"] == "rm"]
        out[w] = {"rfc": len(rf), "rfc_closed": sum(d["closed"] for d in rf), "rm": len(rm),
                  "rm_moved": sum(1 for d in rm if d["result"] and d["result"].startswith("moved")),
                  "rm_not_moved": sum(1 for d in rm if d["result"] and re.match(r"not moved|no consensus", d["result"]))}
    return out


def lead_terms(lp):
    return {**{k: (A.count(k, lp) > 0) for k in A.CRITICAL}, "disp_P": bool(N.DISP_P.search(lp)), "disp_J": bool(N.DISP_J.search(lp))}


def lead_events(title):
    """Section-0 text of every revision in w1 and w2 (each capped at LEAD_PAGES x 50): term insert/remove events.
    Raw usernames stay in memory only (hashed or aggregated before anything is written)."""
    events, trunc = [], {}
    for w in ("w1", "w2"):
        a, b = WINDOWS[w]
        prev, trunc[w] = None, False
        for j in paged({"action": "query", "prop": "revisions", "titles": title, "rvprop": "ids|timestamp|user|tags|content",
                        "rvslots": "main", "rvsection": 0, "rvdir": "newer", "rvstart": a, "rvend": b, "rvlimit": 50},
                       core=False, max_pages=LEAD_PAGES):
            if "_failed" in j:
                return None, trunc
            if "_truncated" in j:
                trunc[w] = j["_truncated"]; break
            for r in ((j.get("query", {}).get("pages") or [{}])[0].get("revisions") or []):
                c = (r.get("slots") or {}).get("main", {}).get("content")
                if c is None:
                    continue
                cur = lead_terms(A.prose(c))
                if prev is not None:
                    for k in TERMS:
                        if cur[k] != prev[k]:
                            events.append({"ts": r["timestamp"], "term": k, "kind": "insert" if cur[k] else "remove",
                                           "revid": r.get("revid"), "user": r.get("user") or "",
                                           "reverted": "mw-reverted" in (r.get("tags") or [])})
                prev = cur
    return events, trunc


def liftwing(revid):
    if not LW_ON[0]:
        return None
    j = wt_net.post_json(LIFTWING, {"rev_id": int(revid), "lang": "en"})
    _lw_fail[0] += 1
    if j is None:
        _lw_fail[1] += 1
        if _lw_fail[0] <= 8 and _lw_fail[1] >= 5:
            LW_ON[0] = False
            print("WARNING: LiftWing failing; disabled for the rest of the run", file=sys.stderr, flush=True)
        return None
    pr = (j.get("output") or {}).get("probabilities") or {}
    return pr.get("true")


def event_aggregates(events):
    users = {e["user"] for e in events if e["user"] and not A.ANON.match(e["user"]) and not A.BOT.search(e["user"])}
    facts = user_facts(users) if users else {}
    fam = lambda e: "critical" if e["term"] in A.CRITICAL else e["term"]
    out = {}
    for w in WINDOWS:
        ew = [e for e in events if in_win(e["ts"], w)]
        res = {}
        for f_ in ("critical", "disp_P", "disp_J"):
            for kind in ("insert", "remove"):
                ek = [e for e in ew if fam(e) == f_ and e["kind"] == kind]
                reg = [(e, facts.get(e["user"])) for e in ek if facts.get(e["user"])]
                ages = [((ep(e["ts"]) - ep(x["reg"])) / 86400 if x["reg"] else 9999.0) for e, x in reg]
                nr = len(reg)
                lw = [e["lw"] for e in ek if e.get("lw") is not None]
                res[f"{f_}_{kind}"] = {
                    "n": len(ek), "reverted_share": (sum(e["reverted"] for e in ek) / len(ek)) if ek else None,
                    "anon_share": (sum(bool(A.ANON.match(e["user"])) for e in ek if e["user"]) / len(ek)) if ek else None,
                    "actors": len({e["user"] for e in ek if e["user"]}),
                    "acct_n": nr, "acct_age_lt30": (sum(a < 30 for a in ages) / nr) if nr else None,
                    "acct_age_lt365": (sum(a < 365 for a in ages) / nr) if nr else None,
                    "acct_median_age_days": statistics.median(ages) if ages else None,
                    "acct_editcount_lt500": (sum((x["ec"] or 0) < 500 for _, x in reg) / nr) if nr else None,
                    "acct_ec_now": (sum(x["ext"] for _, x in reg) / nr) if nr else None,
                    "acct_indef_now": (sum(x["indef"] for _, x in reg) / nr) if nr else None,
                    "lw_n": len(lw), "lw_mean_risk": (sum(lw) / len(lw)) if lw else None}
        out[w] = res
    return out


def wikidata_at(qid):
    out = {}
    for k, d in DATES.items():
        meta, content = wikitext_at(qid, d, url=WD, core=False)
        out[k] = None if content is None else {**(parse_wikidata(content) or {}), "revid": meta["revid"], "ts": meta["ts"]}
    return out


def title_at(current, moves, date):
    for m in sorted(moves, key=lambda m: m["ts"]):
        if m["ts"] > date:
            return m["from"]
    return current


def collect(row):
    t0 = row["title"]
    failed = []
    try:
        info = page_info(t0)
    except Missing:
        return {**row, "missing": True}
    title = info["title"]
    rec = {**row, "canonical": title, "missing": False, "now": info, "at": {}, "win": {}}
    # S2 article wikitext at dates
    prev_rev = None
    for k, d in DATES.items():
        meta, wt = wikitext_at(title, d)
        if meta and prev_rev and meta.get("revid") == prev_rev[0]:
            parsed = prev_rev[1]
        else:
            parsed = parse_article(wt) if wt is not None else None
        rec["at"][k] = {"rev": meta, "article": parsed}
        if meta:
            prev_rev = (meta.get("revid"), parsed)
    # S3 talk wikitext at dates
    talk = f"Talk:{title}"
    now_talk_wt = None
    for k, d in DATES.items():
        if info["talk_exists"]:
            meta, wt = wikitext_at(talk, d)
            if k == "now":
                now_talk_wt = wt
            rec["at"][k]["talk"] = parse_talk(wt) if wt is not None else None
            rec["at"][k]["talk_rev"] = meta
        else:
            rec["at"][k]["talk"] = None
    # S5 revisions since 2021 (+ size of the revision just before 2021 for the first delta)
    revs, trunc = history(title, "ids|timestamp|user|size|comment|tags|flags|sha1")
    if revs is None:
        raise RuntimeError(f"revisions failed: {title}")
    meta0 = rec["at"]["2021-01-01"]["rev"]
    prev_size = None
    if meta0 and revs and meta0.get("revid") != revs[0].get("revid") and rec["at"]["2021-01-01"]["article"]:
        prev_size = rec["at"]["2021-01-01"]["article"].get("bytes")
    agg, moves, eds, created = rev_aggregates(revs, prev_size)
    rec["created_in_window"] = created
    rec["revisions_truncated"] = trunc
    rec["moves"] = moves
    # S6 talk revisions + overlap of article editors with talk participants
    trevs, ttrunc = (history(talk, "timestamp|user|size") if info["talk_exists"] else ([], False))
    if trevs is None:
        failed.append("talk_revisions"); trevs = []
    tagg, _, teds, _ = rev_aggregates(trevs)
    for w in WINDOWS:
        a_eds, t_eds = eds[w], set(teds[w])
        n = sum(a_eds.values())
        agg[w]["talk"] = {"edits": tagg[w].get("edits", 0), "editors": tagg[w]["editors"],
                          "bytes_added": tagg[w].get("bytes_added", 0), "edits_per_month": tagg[w]["edits_per_month"],
                          "talk_to_article_edits": (tagg[w].get("edits", 0) / agg[w]["edits"]) if agg[w].get("edits") else None,
                          "article_edits_by_talk_participants": (sum(c for u, c in a_eds.items() if u in t_eds) / n) if n else None,
                          "article_editors_on_talk": (sum(1 for u in a_eds if u in t_eds) / len(a_eds)) if a_eds else None}
        agg[w]["editor_hashes"] = sorted(h(u) for u in a_eds)
    rec["talk_revisions_truncated"] = ttrunc
    # S7 editor accounts (aggregate only)
    ua = user_aggregates(revs)
    for w in WINDOWS:
        agg[w]["accounts"] = ua[w]
    # S13 edit filter log
    ab = abuse_log(title)
    if ab is None: failed.append("abuselog")
    for w in WINDOWS:
        agg[w]["abuselog"] = ab[w] if ab else None
    # S10 pageviews
    pv = pageviews(title)
    rec["pageviews"] = pv
    for w in WINDOWS:
        a, b = WINDOWS[w]
        mon = [m for m in (pv.get("all-access") or {}) if a[:4] + a[5:7] <= m < b[:4] + b[5:7]]
        tot = sum(pv["all-access"][m] for m in mon) if mon else None
        desk = sum((pv.get("desktop") or {}).get(m, 0) for m in mon) if mon and pv.get("desktop") is not None else None
        agg[w]["views"] = {"per_month": (tot / len(mon)) if mon else None, "mobile_share": (1 - desk / tot) if tot and desk is not None else None}
    rec["win"] = agg
    # S8 protection, S9 title at dates
    log = protect_log(title)
    if log is None: failed.append("protect_log")
    rec["protect_log"] = log
    for k, d in DATES.items():
        rec["at"][k]["protection"] = protection_at(log, d) if log is not None else None
        rec["at"][k]["title"] = title_at(title, moves, d)
    # S11, S12, S4 talk archives
    rec["now"]["inbound_links"] = linksto(title)
    rec["now"]["afd"] = afd_pages(title)
    rec["now"]["talk_archives"] = talk_archives(title) if info["talk_exists"] else {"n": 0, "bytes": 0, "n_subpages": 0}
    for k in ("inbound_links", "afd", "talk_archives"):
        if rec["now"][k] is None: failed.append(k)
    # S17 RfCs / requested moves (current talk + archives touched since 2021)
    arch_pages = rec["now"]["talk_archives"].pop("_pages", []) if rec["now"]["talk_archives"] else []
    rec["discussions"] = rfc_scan(now_talk_wt, arch_pages) if info["talk_exists"] else None
    if info["talk_exists"] and rec["discussions"] is None: failed.append("discussions")
    # S15/S16 lead term events, inserter vs remover accounts, LiftWing revert risk on a capped spread of events
    ev, ltrunc = lead_events(title)
    if ev is None:
        failed.append("lead_events"); rec["term_events"] = None
    else:
        pick = ev if len(ev) <= LW_MAX else [ev[int(i * len(ev) / LW_MAX)] for i in range(LW_MAX)]
        for e in pick:
            if e.get("revid"):
                e["lw"] = liftwing(e["revid"])
        rec["term_events"] = {"truncated": ltrunc, "by_window": event_aggregates(ev),
                              "events": [{"ts": e["ts"], "term": e["term"], "kind": e["kind"], "revid": e["revid"],
                                          "reverted": e["reverted"], "u": h(e["user"]) if e["user"] else None,
                                          "anon": bool(A.ANON.match(e["user"])) if e["user"] else None, "lw": e.get("lw")}
                                         for e in ev][:2000]}
    # S14 Wikidata
    if info.get("qid"):
        wd = wikidata_at(info["qid"])
        for k in DATES:
            rec["at"][k]["wikidata"] = wd[k]
    else:
        for k in DATES:
            rec["at"][k]["wikidata"] = None
    rec["failed_signals"] = failed
    return rec


# ------------------------------------------------------------------ sample
def build_sample():
    rows = json.load(open(FRAME))["rows"] if os.path.exists(FRAME) else []
    by_title = {r["title"]: r for r in rows}
    rnd = random.Random(SEED)
    out, seen = [], set()

    def add(t, group, stratum, src):
        if t in seen:
            return False
        seen.add(t)
        fr = by_title.get(t, {})
        out.append({"title": t, "group": group, "stratum": stratum, "source": src,
                    "project": fr.get("project"), "importance": fr.get("importance")})
        return True

    for t in KEY_ARTICLES:
        add(t, "topic", "topic", "key")
    narr = [t for t in dict.fromkeys(TREATMENT_SEED["narrative"]) if t not in seen]
    rnd.shuffle(narr)
    n_narr = (N_TOPIC - len(out)) * 4 // 7
    for t in narr[:n_narr]:
        add(t, "topic", "topic", "narrative")
    trows = [r for r in rows if r["group"] == "topic" and r["title"] not in seen]
    rnd.shuffle(trows)
    for r in trows:
        if sum(1 for x in out if x["group"] == "topic") >= N_TOPIC:
            break
        add(r["title"], "topic", "topic", "mass")
    for t in narr[n_narr:]:                                    # top up if the frame is absent (offline)
        if sum(1 for x in out if x["group"] == "topic") >= N_TOPIC:
            break
        add(t, "topic", "topic", "narrative")
    disp = [t for spec in NARRATIVE_DISPUTES.values() for t in spec["articles"]]
    for t in disp:
        add(t, "comparison", "comparison_dispute", "dispute")
    for t in ATROCITY:
        add(t, "comparison", "comparison_atrocity", "atrocity")
    ctrl = [t for t in KEY_ARTICLES_CONTROL if t not in seen]
    rnd.shuffle(ctrl)
    for t in ctrl:
        if sum(1 for x in out if x["stratum"] == "comparison_dispute") >= N_DISPUTE:
            break
        add(t, "comparison", "comparison_dispute", "key_control")
    crows = [r for r in rows if r["group"] == "comparison" and r["title"] not in seen]
    rnd.shuffle(crows)
    for r in crows[:N_RANDOM]:
        add(r["title"], "comparison", "comparison_random", "mass")
    return out


# ------------------------------------------------------------------ summary
CLASS_RANK = {"stub": 0, "start": 1, "c": 2, "b": 3, "ga": 4, "a": 5, "fa": 6, "fl": 6, "list": None}


def flat(r):
    """Per-article screening metrics (numbers or None) for the topic-vs-comparison look in summary.json."""
    f = {}
    at = r.get("at") or {}
    g = lambda k, *path: _dig(at.get(k), path)
    for k in DATES:
        f[f"dispute_tag@{k}"] = _b(g(k, "article", "dispute_tag"))
        f[f"ct_notice@{k}"] = _b(g(k, "talk", "ct_notice"))
        f[f"ec_protected@{k}"] = None if g(k, "protection") is None else float(g(k, "protection").get("edit") in ("extendedconfirmed", "sysop", "templateeditor"))
        f[f"talk_kb@{k}"] = (g(k, "talk", "bytes") or 0) / 1e3 if g(k, "talk") else None
        f[f"watch_links@{k}"] = _len(g(k, "article", "watch_links"))
        f[f"watch_links_lead@{k}"] = _len(g(k, "article", "watch_links_lead"))
        f[f"n_categories@{k}"] = _len(g(k, "article", "categories"))
        f[f"n_see_also@{k}"] = _len(g(k, "article", "see_also"))
        f[f"n_navboxes@{k}"] = _len(g(k, "article", "navboxes"))
        f[f"n_links@{k}"] = g(k, "article", "n_links")
        f[f"citation_needed@{k}"] = None if g(k, "article") is None or g(k, "article", "maint") is None else float(
            sum(v for n, v in g(k, "article", "maint").items() if n in ("citation needed", "cn", "fact")))
        c = g(k, "talk", "class")
        f[f"class_rank@{k}"] = CLASS_RANK.get((c or "").lower()) if c else None
        f[f"wd_aliases_en@{k}"] = _len(_dig(g(k, "wikidata"), ("aliases", "en"))) if g(k, "wikidata") else None
    for a, b in (("2021-01-01", "now"), ("2023-07-01", "now")):
        A_, B_ = g(a, "article"), g(b, "article")
        ok = A_ and B_ and not A_.get("redirect") and not B_.get("redirect")
        tag = f"{a[:4]}→now"
        f[f"short_desc_changed {tag}"] = float(A_.get("short_desc") != B_.get("short_desc")) if ok else None
        f[f"infobox_caption_changed {tag}"] = float(_dig(A_, ("infobox", "caption")) != _dig(B_, ("infobox", "caption"))) if ok and A_.get("infobox") and B_.get("infobox") else None
        f[f"lead_image_changed {tag}"] = float(_dig(A_, ("lead_image", "file")) != _dig(B_, ("lead_image", "file"))) if ok else None
        f[f"categories_added {tag}"] = float(len(set(B_["categories"]) - set(A_["categories"]))) if ok else None
        f[f"categories_removed {tag}"] = float(len(set(A_["categories"]) - set(B_["categories"]))) if ok else None
        f[f"links_added {tag}"] = float(len(set(B_["links"]) - set(A_["links"]))) if ok else None
        f[f"watch_links_added {tag}"] = float(len(set(B_["watch_links"]) - set(A_["watch_links"]))) if ok else None
        f[f"headings_new {tag}"] = float(len(set(B_["headings"]) - set(A_["headings"]))) if ok else None
        wa, wb = g(a, "wikidata"), g(b, "wikidata")
        for l in ("en", "he", "ar"):
            f[f"wd_desc_{l}_changed {tag}"] = float(_dig(wa, ("descriptions", l)) != _dig(wb, ("descriptions", l))) if wa and wb else None
    for k in DATES:
        art = g(k, "article")
        if art and not art.get("redirect"):
            ll, lf = art.get("lex_lead") or {}, art.get("lex_full") or {}
            lw_, fw_ = max(1, art.get("lead_words") or 0), max(1, art.get("full_words") or 0)
            f[f"lead_disp_P_per10k@{k}"] = ll.get("disp_P", 0) * 1e4 / lw_
            f[f"lead_disp_J_per10k@{k}"] = ll.get("disp_J", 0) * 1e4 / lw_
            f[f"full_disp_P_per10k@{k}"] = lf.get("disp_P", 0) * 1e4 / fw_
            f[f"full_disp_J_per10k@{k}"] = lf.get("disp_J", 0) * 1e4 / fw_
            f[f"lead_critical_per10k@{k}"] = sum(ll.get(t, 0) for t in A.CRITICAL) * 1e4 / lw_
            lr = art.get("lead_refs") or {}
            tot = lr.get("_total", 0)
            f[f"lead_refs@{k}"] = float(tot)
            for cls in ("Rights orgs & UN", "Scholarly (books, journals)", "Israeli press", "Arab & Palestinian press, pro-Palestinian outlets"):
                f[f"lead_refs_share[{cls[:22]}]@{k}"] = (lr.get(cls, 0) / tot) if tot else None
    te = r.get("term_events") or {}
    for w in WINDOWS:
        bw = (te.get("by_window") or {}).get(w) or {}
        for fam in ("critical", "disp_P"):
            ins, rem = bw.get(f"{fam}_insert") or {}, bw.get(f"{fam}_remove") or {}
            f[f"{fam}_inserts_per_month@{w}"] = (ins.get("n", 0) / months(w)) if bw else None
            f[f"{fam}_net_inserts@{w}"] = float(ins.get("n", 0) - rem.get("n", 0)) if bw else None
            for k in ("acct_age_lt365", "acct_editcount_lt500", "acct_indef_now", "reverted_share", "lw_mean_risk"):
                f[f"{fam}_insert_{k}@{w}"] = ins.get(k)
                f[f"{fam}_remove_{k}@{w}"] = rem.get(k)
        d = (r.get("discussions") or {}).get(w)
        if d:
            f[f"rfc_per_year@{w}"] = d["rfc"] * 12 / months(w)
            f[f"rm_per_year@{w}"] = d["rm"] * 12 / months(w)
    f["moved_since_2021"] = float(bool(r.get("moves"))) if "moves" in r else None
    n = r.get("now") or {}
    f["inbound_links"] = n.get("inbound_links"); f["n_redirects"] = n.get("n_redirects"); f["watchers"] = n.get("watchers")
    f["afd_pages"] = _len(n.get("afd"))
    f["talk_archives"] = _dig(n, ("talk_archives", "n"))
    f["shortdesc_from_wikidata"] = None if not n else float(n.get("description_source") == "central")
    tn = g("now", "talk")
    if tn:
        f["n_press"] = float(tn.get("n_press", 0)); f["top25"] = float(tn.get("top25", 0))
        f["rfc_headings_now"] = float(tn.get("rfc_headings", 0)); f["rm_headings_now"] = float(tn.get("rm_headings", 0))
        f["main_page_any"] = float(bool(tn.get("dyk") or tn.get("itn") or tn.get("otd") or _dig(tn, ("article_history", "dyk"))
                                        or _dig(tn, ("article_history", "itn")) or _dig(tn, ("article_history", "otd")) or _dig(tn, ("article_history", "tfa"))))
    for w in WINDOWS:
        x = (r.get("win") or {}).get(w)
        if not x:
            continue
        e = x.get("edits", 0)
        f[f"edits_per_month@{w}"] = x.get("edits_per_month")
        for k in ("reverted", "reverting", "mobile", "visualeditor", "hidden", "big_add", "empty_summary",
                  "cmt_sock_ban", "cmt_ecr_arbpia", "cmt_npov", "cmt_sources", "cmt_consensus", "cmt_undue", "cmt_voice", "cmt_lead", "cmt_title_name"):
            f[f"{k}_share@{w}"] = (x.get(k, 0) / e) if e else None
        f[f"added_minus_removed_kb@{w}"] = (x.get("bytes_added", 0) - x.get("bytes_removed", 0)) / 1e3 if e else None
        f[f"top1_share@{w}"] = x.get("top1_share")
        for k in ("share_age_lt30", "share_age_lt365", "share_ec_now", "share_editcount_lt500", "share_indef_now", "median_age_days"):
            f[f"acct_{k}@{w}"] = _dig(x, ("accounts", k))
        for k in ("talk_to_article_edits", "article_edits_by_talk_participants", "article_editors_on_talk", "edits_per_month"):
            f[f"talk_{k}@{w}"] = _dig(x, ("talk", k))
        f[f"abuse_hits_per_month@{w}"] = (_dig(x, ("abuselog", "hits")) / months(w)) if _dig(x, ("abuselog", "hits")) is not None else None
        f[f"views_per_month@{w}"] = _dig(x, ("views", "per_month"))
        f[f"mobile_view_share@{w}"] = _dig(x, ("views", "mobile_share"))
    return f


def _dig(d, path):
    for p in path:
        if not isinstance(d, dict):
            return None
        d = d.get(p)
    return d


def _b(x):
    return None if x is None else float(bool(x))


def _len(x):
    return None if x is None else float(len(x))


def screen(recs):
    import numpy as np
    rng = np.random.default_rng(11)
    F = [(r, flat(r)) for r in recs if not r.get("missing")]
    keys = sorted({k for _, f in F for k in f})
    out = []
    for k in keys:
        vals = defaultdict(list)
        for r, f in F:
            v = f.get(k)
            if v is not None:
                vals[r["stratum"]].append(float(v))
                vals[r["group"]].append(float(v))
        t, c = np.array(vals["topic"]), np.array(vals["comparison"])
        row = {"metric": k, **{f"mean_{s}": (float(np.mean(vals[s])) if vals[s] else None) for s in ("topic", "comparison_dispute", "comparison_random")},
               **{f"n_{s}": len(vals[s]) for s in ("topic", "comparison_dispute", "comparison_random")},
               "mean_comparison_atrocity": (float(np.mean(vals["comparison_atrocity"])) if vals["comparison_atrocity"] else None),
               "n_comparison_atrocity": len(vals["comparison_atrocity"])}
        if len(t) >= 5 and len(c) >= 5:
            d = t.mean() - c.mean()
            pool = np.concatenate([t, c]); perm = np.empty(500)
            for i in range(500):
                rng.shuffle(pool); perm[i] = pool[:len(t)].mean() - pool[len(t):].mean()
            sd = pool.std() or 1.0
            row.update({"diff_topic_minus_comparison": float(d), "std_diff": float(d / sd),
                        "p_perm": float((np.sum(np.abs(perm) >= abs(d)) + 1) / 501)})
        out.append(row)
    out.sort(key=lambda r: -abs(r.get("std_diff") or 0))
    return out


def coverage(recs):
    live = [r for r in recs if not r.get("missing")]
    cov = {}
    def share(fn):
        return round(sum(1 for r in live if fn(r)) / len(live), 3) if live else None
    for k in DATES:
        cov[f"article_wikitext@{k}"] = share(lambda r: _dig(r, ("at", k, "article")) is not None)
        cov[f"talk_wikitext@{k}"] = share(lambda r: _dig(r, ("at", k, "talk")) is not None)
        cov[f"wikidata@{k}"] = share(lambda r: _dig(r, ("at", k, "wikidata")) is not None)
        cov[f"short_desc@{k}"] = share(lambda r: bool(_dig(r, ("at", k, "article", "short_desc"))))
        cov[f"infobox@{k}"] = share(lambda r: bool(_dig(r, ("at", k, "article", "infobox"))))
        cov[f"protection_known@{k}"] = share(lambda r: _dig(r, ("at", k, "protection")) is not None)
    cov["pageviews"] = share(lambda r: bool(_dig(r, ("pageviews", "all-access"))))
    cov["inbound_links"] = share(lambda r: _dig(r, ("now", "inbound_links")) is not None)
    cov["watchers_visible"] = share(lambda r: _dig(r, ("now", "watchers")) is not None)
    cov["qid"] = share(lambda r: bool(_dig(r, ("now", "qid"))))
    cov["abuselog"] = share(lambda r: _dig(r, ("win", "w2", "abuselog")) is not None)
    cov["accounts_w2"] = share(lambda r: (_dig(r, ("win", "w2", "accounts", "n_edits")) or 0) > 0)
    cov["revisions_truncated"] = share(lambda r: r.get("revisions_truncated"))
    cov["created_in_window"] = share(lambda r: bool(r.get("created_in_window")))
    return cov


# ------------------------------------------------------------------ runner (mirrors mass._run)
def _save(path, obj):
    tmp = path + ".tmp"
    with gzip.open(tmp, "wt") as f:
        json.dump(obj, f)
    os.replace(tmp, path)


def run(sample, workers=4):
    os.makedirs(OUT, exist_ok=True)
    part = os.path.join(OUT, "pilot.partial.json.gz")
    done = []
    if os.path.exists(part):
        try:
            done = json.load(gzip.open(part, "rt"))
        except Exception:
            done = []
    have = {r["title"] for r in done}
    todo = [r for r in sample if r["title"] not in have]
    print(f"pilot: {len(have)} already done, {len(todo)} to do (salt from env: {bool(os.environ.get('WT_SALT'))})", flush=True)
    out, fails, err_titles = list(done), 0, []
    wt_net.heartbeat("pilot", len(out), len(sample), force=True)
    t0 = time.time()
    with ThreadPoolExecutor(workers) as ex:
        futs = {ex.submit(collect, r): r["title"] for r in todo}
        for k, f in enumerate(as_completed(futs), 1):
            try:
                out.append(f.result())
            except Exception as e:
                fails += 1; err_titles.append(futs[f]); print(f"ERR {futs[f]}: {e}", file=sys.stderr, flush=True)
            wt_net.heartbeat("pilot", len(out), len(sample), article_errors=fails)
            if k % 5 == 0:
                _save(part, out)
    _save(part, out)
    order = {r["title"]: i for i, r in enumerate(sample)}
    out.sort(key=lambda r: order.get(r["title"], 10 ** 6))
    seen_c, dups, kept = set(), [], []
    for r in out:                                   # redirects that resolve to the same page: keep the first
        key = r.get("canonical") or r["title"]
        if key in seen_c:
            dups.append({"title": r["title"], "canonical": key, "stratum": r["stratum"]}); continue
        seen_c.add(key); kept.append(r)
    out = kept
    json.dump({"dates": DATES, "windows": WINDOWS, "note": "Pilot signals. Editors are salted hashes (per-run salt, never stored); "
               "account facts are per-article shares; edit summaries are class counts only.", "articles": out},
              open(os.path.join(OUT, "pilot.json"), "w"))
    C = dict(wt_net.C)
    summ = {"generated": NOW, "n_sample": len(sample), "n_done": len(out), "duplicates_dropped": dups,
            "liftwing": {"enabled_at_end": LW_ON[0], "calls": _lw_fail[0], "failures": _lw_fail[1]}, "n_missing": sum(1 for r in out if r.get("missing")),
            "missing_titles": [r["title"] for r in out if r.get("missing")],
            "n_errors": fails, "error_titles": err_titles,
            "by_stratum": dict(Counter(r["stratum"] for r in out)),
            "failed_signals": dict(Counter(s for r in out for s in r.get("failed_signals") or [])),
            "requests": {k: v for k, v in C.items() if k not in ("latency_sum", "started")},
            "requests_per_article": (C.get("requests", 0) / max(1, len(todo) - fails)) if todo else None,
            "runtime_min": round((time.time() - t0) / 60, 1),
            "coverage": coverage(out), "screen": screen(out)}
    json.dump(summ, open(os.path.join(OUT, "summary.json"), "w"), indent=1)
    wt_net.heartbeat("pilot-done", len(out), len(sample), force=True, article_errors=fails)
    print(f"pilot: {len(out)} records, {fails} errors, {summ['n_missing']} missing pages, "
          f"{C.get('requests', 0)} requests", flush=True)
    for row in summ["screen"][:25]:
        if row.get("p_perm") is not None:
            print(f"  {row['metric']:<55} topic {row['mean_topic']!s:.8} disp {row['mean_comparison_dispute']!s:.8} "
                  f"rand {row['mean_comparison_random']!s:.8}  d={row['std_diff']:+.2f} p={row['p_perm']:.3f}")
    if todo and fails > 0.05 * len(todo):
        sys.exit(f"pilot: {fails}/{len(todo)} articles failed (>5%) - see ERR lines")
    return summ


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", action="store_true", help="print the sample and exit")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    sample = build_sample()
    if a.sample:
        for r in sample:
            print(r["stratum"], r["source"], r["title"], sep="\t")
        print(Counter(r["stratum"] for r in sample)); return
    if not os.environ.get("WT_SALT"):
        print("WARNING: WT_SALT not set; using a random per-process salt (hashes not linkable across runs)", file=sys.stderr)
    lim = int(os.environ.get("PILOT_LIMIT", "0"))
    run(sample[:lim] if lim else sample, a.workers)


if __name__ == "__main__":
    main()
