"""Cross-language mirror: the same key articles in other Wikipedias (same process, different communities).

  python crosslang.py -> data/crosslang.json   (needs network; runs in CI)

For each key article: follow interlanguage links, take quarterly snapshots of the lead in each language,
and count a small multilingual frame lexicon (colonial / genocide / apartheid / occupation / ethnic cleansing)
per 1,000 lead words. Lead text (first ~1,200 chars) is kept so coders can compare definitions.
"""
import json, os, re, time
from concurrent.futures import ThreadPoolExecutor

import requests

import analyze as A
import wt_net
from corpus import SNAPSHOT_DATES

LANGS = ["de", "fr", "es", "it", "nl", "ru", "he", "ar", "pl", "pt"]
TITLES = ["Zionism", "Israel", "Hamas", "Nakba", "October 7 attacks", "Gaza genocide", "Gaza war",
          "Israeli–Palestinian conflict", "Antisemitism", "Anti-Zionism", "History of Israel", "Jews",
          "Israeli apartheid", "West Bank", "Israeli settlement", "Balfour Declaration",
          # comparison anchors (same languages, other topics)
          "Kurdish nationalism", "Russo-Ukrainian War", "Armenian genocide", "Kashmir conflict"]
LEX = {
    "colonial": r"coloni|koloni|kolonial|colonis|coloniz|colonizz|колони|קולוני|استعمار|استيطان",
    "genocide": r"genocid|genozid|völkermord|génocid|genocidio|genocídio|ludobójstw|геноцид|רצח עם|ג'נוסייד|جينوسايد|إبادة جماعية|ابادة جماعية",
    "apartheid": r"apartheid|апартеид|אפרטהייד|أبارتهايد|فصل عنصري",
    "occupation": r"besatz|besetzt|occupation|occupé|ocupaci|ocupad|occupazion|occupat|bezett|bezetting|okupac|okupow|оккупац|כיבוש|احتلال|ocupaç",
    "ethnic_cleansing": r"ethnische säuberung|nettoyage ethnique|limpieza étnica|pulizia etnica|etnische zuivering|этническ\w* чистк|טיהור אתני|تطهير عرقي|czystk\w* etniczn|limpeza étnica",
}
RX = {k: re.compile(v, re.I) for k, v in LEX.items()}
S = requests.Session()
S.headers["User-Agent"] = "WikiFramingTrends/1.0 (https://github.com/Galdrev/photoStamper; research script) python-requests"


def api(lang, **p):
    p.update(format="json", formatversion=2)
    j = wt_net.get_json(f"https://{lang}.wikipedia.org/w/api.php", p)
    return j if j and "error" not in j else None


def langlinks(title):
    j = api("en", action="query", titles=title, prop="langlinks", lllimit="max", redirects=1)
    if not j:
        return {}
    p = j["query"]["pages"][0]
    return {l["lang"]: l["title"] for l in p.get("langlinks", []) if l["lang"] in LANGS}


def lead_series(lang, title):
    out, last = [], None
    for d in SNAPSHOT_DATES:
        j = api(lang, action="query", prop="revisions", titles=title, rvlimit=1, rvdir="older", rvstart=d,
                rvprop="ids|timestamp|content", rvslots="main")
        if not j:
            continue
        p = j["query"]["pages"][0]
        if not p.get("revisions"):
            continue
        r = p["revisions"][0]
        if last and r["revid"] == last["revid"]:
            out.append({**last, "date": d[:7]}); continue
        wt = r["slots"]["main"].get("content", "")
        if re.match(r"\s*#(redirect|weiterleitung|redirection|перенаправление|הפניה|تحويل)", wt, re.I):
            continue
        lp = re.sub(r"\s+", " ", A.prose(A.split_lead(wt))).strip()
        words = max(1, len(lp.split()))
        rec = {"date": d[:7], "revid": r["revid"], "words": words, "lead": lp[:1200],
               "rates": {k: len(rx.findall(lp)) * 1000 / words for k, rx in RX.items()}}
        out.append(rec); last = rec
    return out


def one(title):
    links = {"en": title, **langlinks(title)}
    res = {}
    for lang, t in links.items():
        res[lang] = {"title": t, "series": lead_series(lang, t)}
    return title, res


_n = [0]
_N = 0


def main():
    global _N
    _LIST = (TITLES)[:2] if os.environ.get('WT_LIMIT') else (TITLES)
    _N = len(_LIST)
    out = {}
    with ThreadPoolExecutor(4) as ex:
        for title, res in ex.map(one, _LIST):
            out[title] = res
            print(title, {l: len(v["series"]) for l, v in res.items()}, flush=True)
            _n[0] += 1; wt_net.heartbeat('crosslang', _n[0], _N)
    json.dump({"langs": ["en"] + LANGS, "lexicon": LEX, "articles": out},
              open(os.path.join(A.DATA, "crosslang.json"), "w"), ensure_ascii=False)


if __name__ == "__main__":
    main()
