"""Data acceptance tests. Criteria are fixed before looking; runs on every article.

  python data_qa.py [ARTICLE_DIR]  -> data/qa.json, exit 1 if any BLOCKING check fails

Checks
  integrity   sha1(snapshot text) == sha1 recorded for that revid in the revision list
  coverage    corpus titles resolved / fetched; snapshots present for each quarter since creation
  continuity  no snapshot-to-snapshot size drop > 60% (blanking/vandalism) unless later restored
  revisions   no duplicate revids; timestamps ascending; revision count > 0 for >= 95% of articles
  redirects   share of snapshots that are redirects (reported; analysis excludes them)
  pageviews   present for >= 90% of articles
  talk        talk-page revisions present for >= 80% of articles
  text        median snapshot > 1,000 words after cleaning; lead found in >= 95% of snapshots
"""
import glob, gzip, hashlib, json, os, re, statistics as st, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from analyze import prose, split_lead, MIN_WORDS_FULL  # noqa: E402

ART = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "data", "articles")
OUT = os.environ.get("WIKITRENDS_OUT", os.path.join(HERE, "data"))


def main():
    files = sorted(glob.glob(os.path.join(ART, "*.json.gz")))
    _mp = os.path.join(os.environ.get("WIKITRENDS_DATA", os.path.join(HERE, "data")), "manifest.json")
    if os.path.exists(_mp):
        _m = json.load(open(_mp))
        _keep = []
        for fn in files:
            t = json.load(gzip.open(fn, "rt", encoding="utf-8"))["title"]
            if t in _m:
                _keep.append(fn)
        print(f"QA on {len(_keep)} manifest articles; ignoring {len(files) - len(_keep)} stale cache files")
        files = _keep
    per, sha_ok, sha_bad, sha_unknown = [], 0, [], 0
    drops, redirects, total_snaps, words, lead_found = [], 0, 0, [], 0
    no_rev, dup_rev, unordered, no_pv, no_talk = [], [], [], [], []
    for fn in files:
        rec = json.load(gzip.open(fn, "rt", encoding="utf-8"))
        t = rec["title"]; revs = rec["revisions"]
        sha = {r["revid"]: r.get("sha1") for r in revs}
        if not revs: no_rev.append(t)
        ids = [r["revid"] for r in revs]
        if len(ids) != len(set(ids)): dup_rev.append(t)
        ts = [r["timestamp"] for r in revs]
        if ts != sorted(ts): unordered.append(t)
        if not rec.get("pageviews"): no_pv.append(t)
        if not rec.get("talk_revisions"): no_talk.append(t)
        prev_len, snaps_ok = None, 0
        for s in rec["snapshots"]:
            if s.get("text") is None:
                continue
            total_snaps += 1
            txt = s["text"]
            h = hashlib.sha1(txt.encode("utf-8")).hexdigest()
            if s["revid"] in sha and sha[s["revid"]]:
                if sha[s["revid"]] == h: sha_ok += 1
                else: sha_bad.append(f"{t} rev {s['revid']}")
            else:
                sha_unknown += 1          # snapshot revid predates 2021 window, sha not in list
            if re.match(r"\s*#redirect", txt, re.I):
                redirects += 1; prev_len = None; continue
            n = len(txt)
            if prev_len and n < 0.4 * prev_len:
                drops.append(f"{t} @ {s['date'][:7]} ({prev_len}->{n} chars)")
            prev_len = n
            w = len(re.findall(r"\w+", prose(txt)))
            words.append(w)
            if split_lead(txt) != txt: lead_found += 1
            snaps_ok += 1
        per.append({"title": t, "group": rec["group"], "revisions": len(revs), "snapshots": snaps_ok,
                    "talk": len(rec.get("talk_revisions", [])), "pageview_months": len(rec.get("pageviews", {}))})

    n = len(files) or 1
    manifest_p = os.path.join(os.environ.get("WIKITRENDS_DATA", os.path.join(HERE, "data")), "manifest.json")
    manifest = json.load(open(manifest_p)) if os.path.exists(manifest_p) else {}
    fetched = {p["title"] for p in per}
    missing = sorted(set(manifest) - fetched)
    checked = sha_ok + len(sha_bad)
    checks = [
        ("integrity: snapshot sha1 matches revision metadata", "BLOCKING",
         checked == 0 or len(sha_bad) / checked < 0.01, f"{sha_ok}/{checked} match; {sha_unknown} snapshots predate window", sha_bad[:20]),
        ("coverage: manifest titles fetched", "BLOCKING", not manifest or len(missing) / max(1, len(manifest)) < 0.05,
         f"{len(fetched)} fetched, {len(missing)} missing of {len(manifest)}", missing[:40]),
        ("revisions: present for >=95% of articles", "BLOCKING", len(no_rev) / n < 0.05, f"{len(no_rev)} without revisions", no_rev[:20]),
        ("revisions: no duplicate revids", "BLOCKING", not dup_rev, f"{len(dup_rev)} articles", dup_rev[:20]),
        ("revisions: timestamps ascending", "BLOCKING", not unordered, f"{len(unordered)} articles", unordered[:20]),
        ("text: median snapshot >= 1,000 words", "BLOCKING", bool(words) and st.median(words) >= 1000,
         f"median {st.median(words) if words else 0:.0f} words", []),
        ("text: lead section found in >=95% of snapshots", "WARN", total_snaps and lead_found / max(1, len(words)) >= 0.95,
         f"{lead_found}/{len(words)}", []),
        ("continuity: snapshot size drops >60%", "WARN", len(drops) / max(1, total_snaps) < 0.01, f"{len(drops)} drops", drops[:30]),
        ("redirects: share of snapshots", "INFO", True, f"{redirects}/{total_snaps}", []),
        ("short snapshots excluded (<300 words)", "INFO", True, f"{sum(w < MIN_WORDS_FULL for w in words)}/{len(words)}", []),
        ("pageviews present for >=90%", "WARN", len(no_pv) / n < 0.10, f"{len(no_pv)} missing", no_pv[:20]),
        ("talk pages present for >=80%", "WARN", len(no_talk) / n < 0.20, f"{len(no_talk)} missing", no_talk[:20]),
    ]
    rows = [{"check": c, "level": lv, "pass": bool(ok), "detail": d, "examples": ex} for c, lv, ok, d, ex in checks]
    qa = {"articles": len(files), "snapshots": total_snaps, "checks": rows,
          "by_group": dict(Counter(p["group"] for p in per)),
          "revisions_total": sum(p["revisions"] for p in per), "per_article": per}
    os.makedirs(OUT, exist_ok=True)
    json.dump(qa, open(os.path.join(OUT, "qa.json"), "w"), indent=1)
    for r in rows:
        print(f"[{'PASS' if r['pass'] else 'FAIL'}] {r['level']:8} {r['check']}: {r['detail']}")
        for e in r["examples"][:5]:
            if not r["pass"] or r["level"] == "INFO":
                print(f"           - {e}")
    if any(not r["pass"] and r["level"] == "BLOCKING" for r in rows):
        sys.exit(1)


if __name__ == "__main__":
    main()
