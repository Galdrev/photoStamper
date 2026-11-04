"""Find the exact revision where each article's first sentence changed (needs Wikipedia API; runs in CI).

  python trace_changes.py -> data/bisect.json
For each pair of consecutive quarterly snapshots whose first sentence differs, binary-search the
revisions in between for the first revision whose first sentence differs from the earlier snapshot's.
Usernames are deliberately not recorded.
"""
import gzip, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor

import fetch as F
import analyze as A
from corpus import KEY_ARTICLES

ART = os.path.join(A.DATA, "articles")
_cache = {}


def text_of(revid):
    if revid not in _cache:
        j = F.api(action="query", prop="revisions", revids=revid, rvprop="content|ids", rvslots="main")
        p = j["query"]["pages"][0]
        _cache[revid] = p["revisions"][0]["slots"]["main"].get("content", "") if p.get("revisions") else ""
    return _cache[revid]


def fs(wt):
    s = A.sentences(A.prose(A.split_lead(wt)))
    return s[0] if s else ""


def bisect_article(title):
    fn = os.path.join(ART, re.sub(r"[^\w\-]+", "_", title)[:150] + ".json.gz")
    if not os.path.exists(fn):
        return title, []
    rec = json.load(gzip.open(fn, "rt", encoding="utf-8"))
    revs = rec["revisions"]; idx = {r["revid"]: i for i, r in enumerate(revs)}
    snaps, last = [], None
    for s in rec["snapshots"]:
        if s.get("text") is not None:
            last = s
        if last and last["revid"] in idx:
            snaps.append((last["revid"], fs(last["text"])))
    changes = []
    for (r0, f0), (r1, f1) in zip(snaps, snaps[1:]):
        if f0 == f1 or r0 == r1:
            continue
        lo, hi = idx[r0], idx[r1]          # fs(lo) == f0, fs(hi) != f0
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if fs(text_of(revs[mid]["revid"])) == f0:
                lo = mid
            else:
                hi = mid
        r = revs[hi]
        before = f0 if lo == idx[r0] else fs(text_of(revs[lo]["revid"]))
        after = fs(text_of(r["revid"]))
        changes.append({"revid": r["revid"], "parentid": r.get("parentid"), "timestamp": r["timestamp"],
                        "comment": (r.get("comment") or "")[:300], "tags": r.get("tags") or [],
                        "size_delta": r["size"] - revs[lo]["size"], "reverted": "mw-reverted" in (r.get("tags") or []),
                        "before": before, "after": after, "snapshot_after": f1})
    return title, changes


def main():
    out = {}
    with ThreadPoolExecutor(4) as ex:
        for t, ch in ex.map(bisect_article, KEY_ARTICLES):
            out[t] = ch
            print(f"{t}: {len(ch)} first-sentence changes traced", flush=True)
    json.dump(out, open(os.path.join(A.DATA, "bisect.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
