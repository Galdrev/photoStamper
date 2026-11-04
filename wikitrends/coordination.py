"""Organic vs organised editing signals (exploratory). Aggregate only; usernames are salted hashes.

  python coordination.py  -> merges `coordination` into data/results.json

Signals, each topic vs comparison, pre-war vs post-war, against a null model:
  C1 overlap      do the most active editors' article sets overlap more than a popularity-preserving null?
  C2 tailgating   recurring editor pairs where B edits the same article within 30 min of A, on >= 5 articles,
                  vs a null where each editor's timeline is circularly shifted (keeps rhythm, breaks synchrony)
  C3 sweeps       editor-days touching >= 5 different articles in the group, per 1,000 active editors
  C4 concentration share of edits by the top 1% / top 10 editors, per quarter
  C5 newcomers    share of edits by accounts first seen in that quarter (from 2022, to avoid left-censoring)
  C6 clock        hour-of-day (UTC) distribution of edits
  C7 lead authors how many distinct editors made the traced first-sentence changes (from trace_changes)
Coincident editing is also produced by shared watchlists and breaking news; these are signals, not proof.
"""
import glob, gzip, hashlib, json, os, random, re
from collections import Counter, defaultdict
from datetime import datetime, timezone

import numpy as np

import analyze as A
from corpus import CONTROL_CONTAMINATED

SALT = os.environ.get("WT_SALT") or os.urandom(16).hex()   # never written anywhere
WAR = datetime(2023, 10, 7, tzinfo=timezone.utc)
RNG = random.Random(5)


def h(u):
    return hashlib.sha256((SALT + u).encode()).hexdigest()[:12]


def ts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def load():
    manifest_p = os.path.join(A.DATA, "manifest.json")
    manifest = json.load(open(manifest_p)) if os.path.exists(manifest_p) else {}
    arts = []
    for fn in sorted(glob.glob(os.path.join(A.ART, "*.json.gz"))):
        rec = json.load(gzip.open(fn, "rt", encoding="utf-8"))
        g = manifest.get(rec["title"], [rec["group"]])[0]
        if g == "control" and rec["title"] in CONTROL_CONTAMINATED:
            continue
        edits = [(ts(r["timestamp"]), h(r["user"])) for r in rec["revisions"]
                 if r.get("user") and not A.BOT.search(r["user"]) and not A.ANON.match(r["user"])]
        arts.append({"title": rec["title"], "group": g, "edits": edits})
    return arts


def period_edits(arts, pre):
    out = []
    for a in arts:
        e = [(t, u) for t, u in a["edits"] if (t < WAR) == pre]
        out.append((a["title"], e))
    return out


def c1_overlap(arts_edits, top=150, reps=20):
    ed = defaultdict(set); cnt = Counter()
    for t, e in arts_edits:
        for _, u in e:
            ed[u].add(t); cnt[u] += 1
    users = [u for u, _ in cnt.most_common(top)]
    if len(users) < 20:
        return None
    def mean_j(sets):
        js = []
        for i in range(len(sets)):
            for j in range(i + 1, len(sets)):
                a, b = sets[i], sets[j]
                js.append(len(a & b) / len(a | b))
        return float(np.mean(js))
    obs = mean_j([ed[u] for u in users])
    pop = Counter(t for u in users for t in ed[u]); titles = list(pop); w = [pop[t] for t in titles]
    nulls = []
    for _ in range(reps):
        sets = []
        for u in users:
            k = len(ed[u]); s = set()
            while len(s) < min(k, len(titles)):
                s.add(RNG.choices(titles, w)[0])
            sets.append(s)
        nulls.append(mean_j(sets))
    return {"observed": obs, "null": float(np.mean(nulls)), "ratio": obs / np.mean(nulls) if np.mean(nulls) else None}


def c2_tailgating(arts_edits, window=1800, min_articles=5, shuffle=False):
    if shuffle:   # circularly shift each editor's timeline by a random offset within the period
        allt = [t.timestamp() for _, e in arts_edits for t, _ in e]
        if not allt:
            return None
        t0, span = min(allt), max(allt) - min(allt) or 1
        off = {}
        new = []
        for title, e in arts_edits:
            ee = []
            for t, u in e:
                o = off.setdefault(u, RNG.random() * span)
                ee.append((t0 + ((t.timestamp() - t0 + o) % span), u))
            new.append((title, sorted(ee)))
        arts_edits = new
    else:
        arts_edits = [(title, sorted((t.timestamp(), u) for t, u in e)) for title, e in arts_edits]
    pair_articles = defaultdict(set); n_edits = 0
    for title, e in arts_edits:
        n_edits += len(e)
        for i, (t, u) in enumerate(e):
            j = i + 1
            while j < len(e) and e[j][0] - t <= window:
                v = e[j][1]
                if v != u:
                    pair_articles[(u, v)].add(title)
                j += 1
    pairs = [p for p, s in pair_articles.items() if len(s) >= min_articles]
    editors = {u for p in pairs for u in p}
    return {"recurring_pairs": len(pairs), "editors_in_pairs": len(editors),
            "pairs_per_10k_edits": len(pairs) * 1e4 / max(1, n_edits), "edits": n_edits}


def c3_sweeps(arts_edits, k=5):
    day = defaultdict(set); active = set()
    for title, e in arts_edits:
        for t, u in e:
            day[(u, t.date())].add(title); active.add(u)
    sweeps = sum(1 for s in day.values() if len(s) >= k)
    return {"sweep_editor_days": sweeps, "per_1000_active_editors": sweeps * 1000 / max(1, len(active)),
            "active_editors": len(active)}


def quarter(t):
    return f"{t.year}-Q{(t.month - 1) // 3 + 1}"


def c4_c5_c6(arts):
    byq = defaultdict(Counter); first_seen = {}
    hours = {"pre": Counter(), "post": Counter()}
    for a in arts:
        for t, u in a["edits"]:
            byq[quarter(t)][u] += 1
            first_seen[u] = min(first_seen.get(u, t), t)
            hours["pre" if t < WAR else "post"][t.hour] += 1
    conc, newc = [], []
    for q in sorted(byq)[:-1]:
        c = byq[q]; tot = sum(c.values())
        if not tot:
            continue
        vals = sorted(c.values(), reverse=True)
        top1 = vals[:max(1, len(vals) // 100)]
        conc.append({"q": q, "top1pct_share": sum(top1) / tot, "top10_share": sum(vals[:10]) / tot, "editors": len(vals)})
        if q >= "2022-Q1":
            new = sum(n for u, n in c.items() if quarter(first_seen[u]) == q)
            newc.append({"q": q, "newcomer_edit_share": new / tot})
    hrs = {k: [v[i] / max(1, sum(v.values())) for i in range(24)] for k, v in hours.items()}
    return conc, newc, hrs


def main():
    arts = load()
    groups = {"topic": [a for a in arts if a["group"] == "treatment"], "comparison": [a for a in arts if a["group"] == "control"]}
    n_eq = min(len(v) for v in groups.values())
    if n_eq == 0:
        print("WARNING: a group has no articles; coordination signals are empty", flush=True)
    out = {"note": "Exploratory. Aggregate signals only; editors are salted hashes, not stored. "
                   "Coincident editing also arises from shared watchlists and breaking news.",
           "articles_per_group_sample": n_eq}
    for g, A_ in groups.items():
        # equal-size article samples so the two groups are comparable
        samp = RNG.sample(A_, n_eq)
        res = {}
        for label, pre in (("pre_war", True), ("post_war", False)):
            pe = period_edits(samp, pre)
            obs, null = c2_tailgating(pe), c2_tailgating(pe, shuffle=True)
            res[label] = {"overlap": c1_overlap(pe), "tailgating": obs, "tailgating_null": null,
                          "tailgating_ratio": (obs["recurring_pairs"] / null["recurring_pairs"]) if obs and null and null["recurring_pairs"] else None,
                          "sweeps": c3_sweeps(pe)}
        conc, newc, hrs = c4_c5_c6(A_)
        res["concentration"] = conc; res["newcomers"] = newc; res["hours"] = hrs
        out[g] = res
    # C7 lead authorship of traced first-sentence changes
    tp = os.path.join(A.DATA, "bisect.json")
    if os.path.exists(tp):
        from corpus import KEY_ARTICLES, KEY_ARTICLES_CONTROL
        tr = json.load(open(tp)); out["lead_authors"] = {}
        for g, titles in (("topic", KEY_ARTICLES), ("comparison", KEY_ARTICLES_CONTROL)):
            ch = [c for t in titles for c in tr.get(t, []) if not c.get("reverted")]
            auth = Counter(c.get("editor") for c in ch if c.get("editor")); n = sum(auth.values())
            per_article = [len(tr.get(t, [])) for t in titles if t in tr]
            out["lead_authors"][g] = {"articles": len(per_article), "changes": n, "distinct_editors": len(auth),
                                      "changes_per_article": float(np.mean(per_article)) if per_article else None,
                                      "top3_share": sum(v for _, v in auth.most_common(3)) / n if n else None,
                                      "top10_share": sum(v for _, v in auth.most_common(10)) / n if n else None,
                                      "editors_on_3plus_articles": sum(1 for e in auth if len({t for t in titles for c in tr.get(t, []) if c.get("editor") == e}) >= 3)}
    rp = os.path.join(A.OUTDIR, "results.json")
    r = json.load(open(rp)) if os.path.exists(rp) else {}
    r["coordination"] = out
    json.dump(r, open(rp, "w"), default=float)
    for g in groups:
        for p in ("pre_war", "post_war"):
            x = out[g][p]
            print(g, p, "overlap", x["overlap"], "| tailgate", x["tailgating"], "null", x["tailgating_null"], "| sweeps", x["sweeps"])


if __name__ == "__main__":
    main()
