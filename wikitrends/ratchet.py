"""The ratchet test: push, revert, push again ... until it sticks?  (exploratory; needs network; runs in CI)

For each key article (topic and comparison), download the OPENING SECTION of EVERY revision since 2021
(API rvsection=0, 50 revisions per request). For each framing term, reconstruct the presence timeline in the lead
and extract insertion / removal events.

Metrics, topic vs comparison:
  survival     share of insertions (and of removals) still standing after 1, 7, 30, 90 days
  attempts     failed insertions (inserted, then removed within 30 days) before the final, standing insertion
  asymmetry    P(insertion survives 30d) - P(removal survives 30d), for critical vs connection terms
  persistence  distinct (hashed) editors among the attempts: one persistent hand or many?
  definitions  every distinct first sentence, how long each was live, and how often it was contested

  python ratchet.py -> data/ratchet.json
"""
import hashlib, json, os, re, time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import numpy as np

import analyze as A
import fetch as F
from corpus import KEY_ARTICLES, KEY_ARTICLES_CONTROL

SALT = os.environ.get("WT_SALT") or os.urandom(16).hex()
START = "2021-01-01T00:00:00Z"
TERMS = A.CRITICAL + A.CONNECTION + ["terrorism", "militant"]
DAY = 86400.0


def ep(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()


def lead_history(title):
    revs, cont = [], {}
    while True:
        j = F.api(action="query", prop="revisions", titles=title, rvprop="ids|timestamp|user|tags|content|size",
                  rvslots="main", rvsection=0, rvdir="newer", rvstart=START, rvlimit=50, redirects=1, **cont)
        p = j["query"]["pages"][0]
        for r in p.get("revisions", []):
            wt = r.get("slots", {}).get("main", {}).get("content")
            if wt is None:                       # revision text hidden/suppressed
                continue
            lp = A.prose(wt)
            sents = A.sentences(lp)
            revs.append({"revid": r["revid"], "t": ep(r["timestamp"]), "ts": r["timestamp"],
                         "u": hashlib.sha256((SALT + (r.get("user") or "")).encode()).hexdigest()[:10],
                         "reverted": "mw-reverted" in (r.get("tags") or []),
                         "reverting": bool(set(r.get("tags") or []) & A.REVERTING),
                         "words": len(re.findall(r"\w+", lp)),
                         "terms": {k: A.count(k, lp) > 0 for k in TERMS},
                         "fs": (sents[0] if sents else "")[:400]})
        if "continue" not in j:
            break
        cont = j["continue"]
    return revs


def events(revs, term, end_t):
    """Insertion/removal events for one term with survival times (censored at end)."""
    ev, state = [], None
    for r in revs:
        s = r["terms"][term]
        if state is not None and s != state:
            ev.append({"kind": "insert" if s else "remove", "t": r["t"], "u": r["u"], "revid": r["revid"]})
        state = s
    for i, e in enumerate(ev):
        nxt = ev[i + 1]["t"] if i + 1 < len(ev) else None
        e["survived"] = (nxt or end_t) - e["t"]
        e["censored"] = nxt is None
    return ev


def article_metrics(title):
    revs = lead_history(title)
    if not revs:
        return title, None
    end_t = time.time()
    per_term = {}
    for term in TERMS:
        ev = events(revs, term, end_t)
        ins = [e for e in ev if e["kind"] == "insert"]
        final_present = revs[-1]["terms"][term]
        failed_before_stick, attempt_editors = 0, set()
        if final_present and ins:
            final_t = ins[-1]["t"] if ins[-1]["censored"] else None
            for e in ins[:-1]:
                if e["survived"] < 30 * DAY:
                    failed_before_stick += 1; attempt_editors.add(e["u"])
            attempt_editors.add(ins[-1]["u"])
        per_term[term] = {"events": [{k: e[k] for k in ("kind", "t", "survived", "censored", "revid")} for e in ev],
                          "present_start": revs[0]["terms"][term], "present_end": final_present,
                          "failed_attempts_before_stick": failed_before_stick if final_present else None,
                          "attempt_editors": len(attempt_editors) if final_present and ins else None}
    # first-sentence variants: how many, how long live, contested?
    var, order = {}, []
    for i, r in enumerate(revs):
        k = r["fs"]
        nxt_t = revs[i + 1]["t"] if i + 1 < len(revs) else end_t
        if k not in var:
            var[k] = {"id": len(var), "first_seen": r["ts"], "live_days": 0.0, "entries": 0}
            order.append(k)
        var[k]["live_days"] += (nxt_t - r["t"]) / DAY
        if i == 0 or revs[i - 1]["fs"] != k:
            var[k]["entries"] += 1
    variants = sorted(({"s": k, **v} for k, v in var.items()), key=lambda x: -x["live_days"])
    # definition timeline compressed: (t, variant id) at each change
    tl, prev = [], None
    for r in revs:
        vid = var[r["fs"]]["id"]
        if vid != prev:
            tl.append([r["ts"][:10], vid, int(r["reverted"])]); prev = vid
    # large lead rewrites and their fate
    big = []
    for a, b in zip(revs, revs[1:]):
        if a["words"] >= 40 and abs(b["words"] - a["words"]) / a["words"] > 0.3:
            big.append({"ts": b["ts"], "delta": b["words"] - a["words"], "reverted": b["reverted"]})
    return title, {"revisions": len(revs), "editors": len({r["u"] for r in revs}),
                   "lead_revert_rate": float(np.mean([r["reverted"] for r in revs])),
                   "terms": per_term, "fs_variants": variants[:150], "fs_n_variants": len(variants),
                   "fs_timeline": tl[:3000], "big_rewrites": big}


def survival(evs, days):
    xs = [e for e in evs if not (e["censored"] and e["survived"] < days * DAY)]
    return float(np.mean([e["survived"] >= days * DAY for e in xs])) if xs else None


def aggregate(arts, titles):
    out = {}
    for fam, terms in (("critical", A.CRITICAL), ("connection", A.CONNECTION), ("terror", ["terrorism"]), ("militant", ["militant"])):
        ins, rem, failed, editors = [], [], [], []
        for t in titles:
            a = arts.get(t)
            if not a:
                continue
            for term in terms:
                d = a["terms"][term]
                ins += [e for e in d["events"] if e["kind"] == "insert"]
                rem += [e for e in d["events"] if e["kind"] == "remove"]
                if d["failed_attempts_before_stick"] is not None and d["events"]:
                    failed.append(d["failed_attempts_before_stick"]); editors.append(d["attempt_editors"])
        out[fam] = {"insertions": len(ins), "removals": len(rem),
                    "insert_survival": {f"{d}d": survival(ins, d) for d in (1, 7, 30, 90)},
                    "remove_survival": {f"{d}d": survival(rem, d) for d in (1, 7, 30, 90)},
                    "asymmetry_30d": (survival(ins, 30) - survival(rem, 30)) if survival(ins, 30) is not None and survival(rem, 30) is not None else None,
                    "terms_that_stuck": len(failed), "mean_failed_attempts_before_stick": float(np.mean(failed)) if failed else None,
                    "share_stuck_after_retries": float(np.mean([f > 0 for f in failed])) if failed else None,
                    "mean_distinct_editors_in_attempts": float(np.mean(editors)) if editors else None}
    n_rev = [arts[t]["revisions"] for t in titles if t in arts]
    out["articles"] = len(n_rev); out["revisions"] = int(sum(n_rev))
    out["fs_variants_per_article"] = float(np.mean([arts[t]["fs_n_variants"] for t in titles if t in arts])) if n_rev else None
    out["lead_revert_rate"] = float(np.mean([arts[t]["lead_revert_rate"] for t in titles if t in arts])) if n_rev else None
    big = [b for t in titles if t in arts for b in arts[t]["big_rewrites"]]
    out["big_rewrites"] = len(big); out["big_rewrites_reverted_share"] = float(np.mean([b["reverted"] for b in big])) if big else None
    return out


def main():
    arts = {}
    with ThreadPoolExecutor(4) as ex:
        for t, m in ex.map(article_metrics, KEY_ARTICLES + KEY_ARTICLES_CONTROL):
            if m:
                arts[t] = m
                print(f"{t}: {m['revisions']} revisions, {m['fs_n_variants']} first-sentence variants", flush=True)
    res = {"note": "Exploratory. Lead (section 0) of every revision since 2021. Editors are salted hashes.",
           "topic": aggregate(arts, KEY_ARTICLES), "comparison": aggregate(arts, KEY_ARTICLES_CONTROL),
           "articles": {t: {k: v for k, v in m.items() if k != "terms"} | {
               "terms": {term: {kk: vv for kk, vv in d.items() if kk != "events"} | {"n_events": len(d["events"])}
                         for term, d in m["terms"].items()}} for t, m in arts.items()},
           "events": {t: {term: d["events"] for term, d in m["terms"].items() if d["events"]} for t, m in arts.items()}}
    json.dump(res, open(os.path.join(A.DATA, "ratchet.json"), "w"))
    for g in ("topic", "comparison"):
        c = res[g]["critical"]
        print(g, "critical: insert survives 30d", c["insert_survival"]["30d"], "| removal survives 30d", c["remove_survival"]["30d"],
              "| stuck after retries", c["share_stuck_after_retries"], "| failed attempts", c["mean_failed_attempts_before_stick"])


if __name__ == "__main__":
    main()
