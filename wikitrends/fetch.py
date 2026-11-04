"""Download revision history, quarterly text snapshots and pageviews.

Usage:  python fetch.py [--max-cat-pages N] [--workers N]
Writes one JSON(.gz) per article into data/articles/.
"""
import argparse, gzip, json, os, random, re, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

import wt_net

from corpus import (TREATMENT_SEED, CONTROL_SEED, TREATMENT_CATEGORIES,
                    START, SNAPSHOT_DATES)

API = "https://en.wikipedia.org/w/api.php"
PV = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
      "en.wikipedia/all-access/user/{t}/monthly/2021010100/2026110100")
UA = "WikiFramingTrends/1.0 (https://github.com/Galdrev/photoStamper; research script) python-requests"
OUT = os.path.join(os.path.dirname(__file__), "data", "articles")
S = requests.Session()
S.headers["User-Agent"] = UA


def api(**p):
    p.update(format="json", formatversion=2)
    j = wt_net.get_json(API, p)
    if j is None:
        raise RuntimeError(f"API failed after retries: {p.get('titles') or p.get('cmtitle') or p.get('revids')}")
    if "error" in j:
        raise RuntimeError(f"API error {j['error']}")
    return j


def category_members(cat, depth=1, seen=None):
    seen = seen if seen is not None else set()
    pages = set()
    if cat in seen:
        return pages
    seen.add(cat)
    cont = {}
    while True:
        j = api(action="query", list="categorymembers", cmtitle=cat,
                cmtype="page|subcat", cmlimit="max", **cont)
        for m in j["query"]["categorymembers"]:
            if m["ns"] == 0:
                pages.add(m["title"])
            elif m["ns"] == 14 and depth > 0:
                try:
                    pages |= category_members(m["title"], depth - 1, seen)
                except Exception as e:
                    print(f"subcategory {m['title']} failed: {e}", file=sys.stderr, flush=True)
        if "continue" not in j:
            break
        cont = j["continue"]
    return pages


def resolve(titles):
    """Follow redirects; return {input_title: canonical_title} for existing pages."""
    out = {}
    titles = list(titles)
    for i in range(0, len(titles), 50):
        chunk = titles[i:i + 50]
        j = api(action="query", titles="|".join(chunk), redirects=1)
        q = j["query"]
        m = {t: t for t in chunk}
        for n in q.get("normalized", []):
            m = {k: (n["to"] if v == n["from"] else v) for k, v in m.items()}
        for r in q.get("redirects", []):
            m = {k: (r["to"] if v == r["from"] else v) for k, v in m.items()}
        exist = {p["title"] for p in q["pages"] if not p.get("missing")}
        out.update({k: v for k, v in m.items() if v in exist})
    return out


def revisions(title, ns_prefix=""):
    revs, cont = [], {}
    while True:
        j = api(action="query", prop="revisions", titles=ns_prefix + title,
                rvprop="ids|timestamp|user|size|comment|tags|sha1",
                rvdir="newer", rvstart=START, rvlimit="max", **cont)
        p = j["query"]["pages"][0]
        for r in p.get("revisions", []):
            revs.append({k: r.get(k) for k in
                         ("revid", "parentid", "timestamp", "user", "size",
                          "comment", "tags", "sha1")})
        if "continue" not in j:
            break
        cont = j["continue"]
    return revs


def snapshot(title, date):
    j = api(action="query", prop="revisions", titles=title, rvlimit=1,
            rvdir="older", rvstart=date, rvprop="ids|timestamp|content",
            rvslots="main")
    p = j["query"]["pages"][0]
    if not p.get("revisions"):
        return None
    r = p["revisions"][0]
    return {"date": date, "revid": r["revid"], "timestamp": r["timestamp"],
            "text": r["slots"]["main"].get("content", "")}


def pageviews(title):
    t = requests.utils.quote(title.replace(" ", "_"), safe="")
    j = wt_net.get_json(PV.format(t=t), {}, tries=4, ok404=True)
    return {i["timestamp"][:6]: i["views"] for i in j["items"]} if j and "items" in j else {}


def fetch_article(title, group, subgroup):
    fn = os.path.join(OUT, re.sub(r"[^\w\-]+", "_", title)[:150] + ".json.gz")
    if os.path.exists(fn):
        return title, "cached"
    snaps, last = [], None
    for d in SNAPSHOT_DATES:
        s = snapshot(title, d)
        if s is None:
            continue
        if last and s["revid"] == last["revid"]:
            s = {**s, "text": None, "same_as_previous": True}
        else:
            last = s
        snaps.append(s)
    rec = {
        "title": title, "group": group, "subgroup": subgroup,
        "revisions": revisions(title),
        "talk_revisions": [{"timestamp": r["timestamp"], "user": r["user"]}
                           for r in revisions(title, "Talk:")],
        "snapshots": snaps,
        "pageviews": pageviews(title),
    }
    with gzip.open(fn + ".tmp", "wt", encoding="utf-8") as f:
        json.dump(rec, f)
    os.replace(fn + ".tmp", fn)
    return title, f"{len(rec['revisions'])} revs"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cat-pages", type=int, default=350)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--only", default="", help="'|'-separated titles; skip corpus and categories")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)

    jobs = {}
    if a.only:
        for t in a.only.split("|"):
            jobs[t] = ("sample", "sample")
        with ThreadPoolExecutor(a.workers) as ex:
            for t, msg in ex.map(lambda t: fetch_article(t, "sample", "sample"), jobs):
                print(t, msg, flush=True)
        return
    for group, seed in (("treatment", TREATMENT_SEED), ("control", CONTROL_SEED)):
        flat = {t: sg for sg, ts in seed.items() for t in ts}
        for src, canon in resolve(flat).items():
            jobs.setdefault(canon, (group, flat[src]))
    print(f"seed articles resolved: {len(jobs)}", flush=True)

    cat_pages = set()
    for c in TREATMENT_CATEGORIES:
        try:
            cat_pages |= category_members(c, depth=1)
        except Exception as e:
            print(f"category {c} failed: {e}", file=sys.stderr, flush=True)
    cat_pages = sorted(cat_pages - set(jobs))
    random.Random(42).shuffle(cat_pages)
    cat_pages = cat_pages[:a.max_cat_pages]
    for t in resolve(cat_pages).values():
        jobs.setdefault(t, ("treatment", "category-sample"))
    print(f"total articles: {len(jobs)}", flush=True)
    with open(os.path.join(OUT, "..", "manifest.json"), "w") as f:
        json.dump(jobs, f, indent=1)

    lim = int(os.environ.get("WT_LIMIT", "0"))
    if lim:
        jobs = dict(list(jobs.items())[:lim])
    errors = 0
    wt_net.heartbeat("fetch", 0, len(jobs), force=True)
    with ThreadPoolExecutor(a.workers) as ex:
        futs = {ex.submit(fetch_article, t, g, sg): t for t, (g, sg) in jobs.items()}
        for i, fu in enumerate(as_completed(futs), 1):
            try:
                t, msg = fu.result()
                print(f"[{i}/{len(jobs)}] {t}: {msg}", flush=True)
            except Exception as e:  # keep going
                errors += 1
                print(f"[{i}/{len(jobs)}] {futs[fu]}: ERROR {e}", file=sys.stderr, flush=True)
            wt_net.heartbeat("fetch", i, len(jobs), article_errors=errors)
    wt_net.heartbeat("fetch-done", len(jobs), len(jobs), force=True, article_errors=errors)


if __name__ == "__main__":
    main()
