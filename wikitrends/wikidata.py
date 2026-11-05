"""Outcome-blind relevance filter (SPEC_NARRATIVE amendment C2a): Wikidata 'instance of' (P31) for every article.

  python wikidata.py  -> data/wikidata_types.json  {title: {"qid","p31":[labels], "keep": bool}}
Titles: the deep-tier manifest plus the mass frame (data/mass/frame.json, if present).
"""
import json, os

import analyze as A
import wt_net

API = "https://www.wikidata.org/w/api.php"
# Types that cannot carry a land/peoples narrative. Anything else is kept.
DROP = {
    "Q5": "human", "Q4167410": "disambiguation page", "Q476028": "association football club", "Q12973014": "sports team",
    "Q847017": "sports club", "Q4830453": "business", "Q783794": "company", "Q6881511": "enterprise", "Q11424": "film",
    "Q5398426": "television series", "Q571": "book", "Q7725634": "literary work", "Q47461344": "written work",
    "Q7366": "song", "Q482994": "album", "Q134556": "single", "Q16521": "taxon", "Q215380": "musical group",
    "Q13442814": "scholarly article", "Q732577": "publication", "Q1002697": "periodical", "Q41298": "magazine",
    "Q11032": "newspaper", "Q3305213": "painting", "Q17537576": "creative work", "Q7397": "software", "Q1344": "opera",
    "Q2188189": "musical work", "Q105543609": "musical work/composition", "Q3331189": "version/edition",
}


def fetch(titles):
    out = {}
    for i in range(0, len(titles), 50):
        chunk = titles[i:i + 50]
        j = wt_net.get_json(API, {"action": "wbgetentities", "sites": "enwiki", "titles": "|".join(chunk),
                                  "props": "claims|sitelinks", "sitefilter": "enwiki", "format": "json"})
        for qid, e in ((j or {}).get("entities") or {}).items():
            if qid.startswith("-") or "missing" in e:
                continue
            t = e.get("sitelinks", {}).get("enwiki", {}).get("title")
            p31 = [c["mainsnak"].get("datavalue", {}).get("value", {}).get("id") for c in e.get("claims", {}).get("P31", [])]
            p31 = [p for p in p31 if p]
            if t:
                out[t] = {"qid": qid, "p31": p31, "drop_types": [DROP[p] for p in p31 if p in DROP],
                          "keep": not any(p in DROP for p in p31)}
        wt_net.heartbeat("wikidata", min(i + 50, len(titles)), len(titles))
    return out


def main():
    titles = list(json.load(open(os.path.join(A.DATA, "manifest.json"))))
    fp = os.path.join(A.DATA, "mass", "frame.json")
    if os.path.exists(fp):
        titles += [r["title"] for r in json.load(open(fp))["rows"]]
    titles = sorted(set(titles))
    out = fetch(titles)
    json.dump(out, open(os.path.join(A.DATA, "wikidata_types.json"), "w"))
    kept = sum(v["keep"] for v in out.values())
    print(f"wikidata: {len(out)}/{len(titles)} titles typed; keep {kept}, drop {len(out) - kept}")


if __name__ == "__main__":
    main()
