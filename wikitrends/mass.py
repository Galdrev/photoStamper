"""Mass tier: thousands of articles, sampled from Wikipedia's own WikiProject importance ratings,
in English plus 10 other languages. Features only (no raw text kept).

  python mass.py frame                 -> data/mass/frame.json
  python mass.py en   --shard I --of N -> data/mass/en_I.json.gz
  python mass.py lang --shard I --of N -> data/mass/lang_I.json.gz
  python mass.py analyze               -> merges `mass` into data/results.json (or data/mass_results.json)

Sampling frame: talk pages in "Category:{Top,High,Mid}-importance <Project> articles".
Topic = Israel, Judaism, Jewish history, Palestine, Zionism projects.
Comparison = national / religious / conflict projects of similar kind.
"""
import argparse, glob, gzip, hashlib, json, os, random, re, sys, time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
import requests

import wt_net

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze as A          # noqa: E402
import explore as E          # noqa: E402
from crosslang import LEX as XLEX, LANGS   # noqa: E402

OUT = os.path.join(HERE, "data", "mass")
UA = "WikiFramingTrends/1.0 (https://github.com/Galdrev/photoStamper; research script) python-requests"
S = requests.Session(); S.headers["User-Agent"] = UA
SALT = os.environ.get("WT_SALT") or os.urandom(16).hex()
DATES = ["2021-01-01T00:00:00Z", "2023-07-01T00:00:00Z", time.strftime("%Y-%m-%dT00:00:00Z")]
XRX = {k: re.compile(v, re.I) for k, v in XLEX.items()}

TOPIC_PROJECTS = ["Israel", "Judaism", "Jewish history", "Palestine", "Zionism", "Jewish culture", "Arab–Israeli conflict"]
CONTROL_PROJECTS = ["India", "Pakistan", "Turkey", "Kurdistan", "Armenia", "Azerbaijan", "Ukraine", "Russia", "Ireland",
                    "Taiwan", "Tibet", "Cyprus", "Greece", "Poland", "Iran", "Sri Lanka", "Bangladesh", "Serbia",
                    "Bosnia and Herzegovina", "Hinduism", "Islam", "Catholicism", "Sikhism", "Buddhism", "Armenian history"]
LEVELS = ["Top", "High", "Mid"]
CAP_PER_GROUP = 4000
LANG_TOP_PER_GROUP = 400


def api(lang="en", **p):
    p.update(format="json", formatversion=2)
    j = wt_net.get_json(f"https://{lang}.wikipedia.org/w/api.php", p)
    return j if j and "error" not in j else None


def cat_talk_titles(cat):
    out, cont = [], {}
    while True:
        j = api(action="query", list="categorymembers", cmtitle=cat, cmnamespace=1, cmlimit="max", **cont)
        if not j:
            break
        out += [m["title"][5:] for m in j["query"]["categorymembers"] if m["title"].startswith("Talk:")]
        if "continue" not in j:
            break
        cont = j["continue"]
    return out


# ---------------------------------------------------------------- frame
def discover(keyword):
    """Real category names, e.g. 'Top-importance Israel-related articles'. Returns the suffixes after the level."""
    suf = set()
    for lev in LEVELS:
        j = api(action="query", list="allcategories", acprefix=f"{lev}-importance {keyword}", aclimit=50)
        for c in (j or {}).get("query", {}).get("allcategories", []):
            name = c["category"]
            rest = name[len(f"{lev}-importance "):]
            if rest.endswith("articles") and len(rest) <= len(keyword) + 20:
                suf.add(rest)
    return sorted(suf)


REQUIRED_TOPIC = ["Israel", "Palestine", "Judaism"]
CAP_PER_PROJECT = {"topic": 1400, "comparison": 260}


def frame():
    rnd = random.Random(42)
    seen, counts, found = {}, {}, {}
    for group, projects in (("topic", TOPIC_PROJECTS), ("comparison", CONTROL_PROJECTS)):
        for proj in projects:
            sufs = discover(proj)
            found[proj] = sufs
            print(f"{group} {proj}: categories {sufs}", flush=True)
            for suf in sufs:
                for lev in LEVELS:
                    cat = f"Category:{lev}-importance {suf}"
                    ts = cat_talk_titles(cat)
                    counts[cat] = len(ts)
                    print(f"  {cat}: {len(ts)}", flush=True)
                    for t in ts:
                        if t in seen:
                            if seen[t]["group"] != group:
                                seen[t]["group"] = "both"
                            elif LEVELS.index(lev) < LEVELS.index(seen[t]["importance"]):
                                seen[t]["importance"] = lev
                            continue
                        seen[t] = {"title": t, "group": group, "project": proj, "importance": lev}
    missing = [p for p in REQUIRED_TOPIC if not found.get(p)]
    if missing:
        raise SystemExit(f"FRAME INVALID: no categories found for required topic projects {missing}")
    rows = [r for r in seen.values() if r["group"] != "both"]
    out = []
    for g in ("topic", "comparison"):
        byp = defaultdict(list)
        for r in rows:
            if r["group"] == g:
                byp[r["project"]].append(r)
        for proj, G in byp.items():
            rnd.shuffle(G)
            G.sort(key=lambda r: LEVELS.index(r["importance"]))          # Top, then High, then Mid
            out += G[:CAP_PER_PROJECT[g]]
    rnd.shuffle(out)
    os.makedirs(OUT, exist_ok=True)
    comp = {g: dict(Counter(r["project"] for r in out if r["group"] == g)) for g in ("topic", "comparison")}
    json.dump({"rows": out, "category_counts": counts, "composition": comp,
               "excluded_both": sum(1 for r in seen.values() if r["group"] == "both")},
              open(os.path.join(OUT, "frame.json"), "w"))
    print("composition:", json.dumps(comp, indent=1))
    print(f"frame: {Counter(r['group'] for r in out)}")
    if min(Counter(r["group"] for r in out).values()) < 1000:
        raise SystemExit("FRAME INVALID: fewer than 1,000 articles in a group")


# ---------------------------------------------------------------- English features
def snap(lang, title, date):
    j = api(lang, action="query", prop="revisions", titles=title, rvlimit=1, rvdir="older", rvstart=date,
            rvprop="ids|timestamp|content", rvslots="main", redirects=1)
    if not j:
        return None
    p = j["query"]["pages"][0]
    if not p.get("revisions"):
        return None
    r = p["revisions"][0]
    wt = r["slots"]["main"].get("content", "")
    if re.match(r"\s*#\w+\s*\[\[", wt):
        return None
    return r["revid"], wt


def en_features(row):
    t = row["title"]
    snaps = []
    for d in DATES:
        s = snap("en", t, d)
        if not s:
            snaps.append(None); continue
        revid, wt = s
        fp, lp = A.prose(wt), A.prose(A.split_lead(wt))
        full, lead = A.measure(fp, 150), A.measure(lp, 25)
        sents = A.sentences(lp)
        h, hd = E.hedged_share(fp)
        snaps.append({"revid": revid, "full": full and {"words": full["words"], "counts": full["counts"]},
                      "lead": lead and {"words": lead["words"], "counts": lead["counts"]},
                      "fs": (sents[0] if sents else "")[:300], "hedge": [h, hd],
                      "refs": {k: v for k, v in E.refs_of(wt).items()}})
    # revision activity since 2021 (hashed editors, kept for coordination tests)
    edits, cont = [], {}
    while True:
        j = api(action="query", prop="revisions", titles=t, rvprop="timestamp|user|tags", rvdir="newer",
                rvstart=DATES[0], rvlimit="max", redirects=1, **cont)
        if not j:
            break
        p = j["query"]["pages"][0]
        for r in p.get("revisions", []):
            u = r.get("user") or ""
            edits.append([r["timestamp"], hashlib.sha256((SALT + u).encode()).hexdigest()[:10] if u else "",
                          int(bool(A.ANON.match(u))), int(bool(A.BOT.search(u))), int("mw-reverted" in (r.get("tags") or []))])
        if "continue" not in j:
            break
        cont = j["continue"]
    return {**row, "snaps": snaps, "edits": edits}


def shard(rows, i, n):
    return [r for k, r in enumerate(rows) if k % n == i]


def _run(kind, fn, rows, i):
    """Checkpointed shard runner: resumes from a partial file, writes every 100 articles."""
    out_p = os.path.join(OUT, f"{kind}_{i}.json.gz")
    done = []
    if os.path.exists(out_p):
        try:
            done = json.load(gzip.open(out_p, "rt"))
        except Exception:
            done = []
    have = {r["title"] for r in done}
    todo = [r for r in rows if r["title"] not in have]
    print(f"{kind} shard {i}: {len(have)} already done, {len(todo)} to do", flush=True)
    out, fails = list(done), 0
    wt_net.heartbeat(f"{kind}-{i}", len(out), len(rows), force=True)
    def save():
        tmp = out_p + ".tmp"
        json.dump(out, gzip.open(tmp, "wt")); os.replace(tmp, out_p)
    with ThreadPoolExecutor(6) as ex:
        futs = [ex.submit(fn, r) for r in todo]
        for k, f in enumerate(as_completed(futs), 1):
            try:
                out.append(f.result())
            except Exception as e:
                fails += 1; print("ERR", e, file=sys.stderr, flush=True)
            wt_net.heartbeat(f"{kind}-{i}", len(out), len(rows), article_errors=fails)
            if k % 100 == 0:
                save()
    save()
    wt_net.heartbeat(f"{kind}-{i}-done", len(out), len(rows), force=True, article_errors=fails)
    if todo and fails > 0.05 * len(todo):          # fail loudly: a shard that mostly errors must not report success
        sys.exit(f"{kind} shard {i}: {fails}/{len(todo)} articles failed (>5%) - see ERR lines")


def run_en(i, n):
    rows = shard(json.load(open(os.path.join(OUT, "frame.json")))["rows"], i, n)
    lim = int(os.environ.get("MASS_LIMIT", "0"))
    _run("en", en_features, rows[:lim] if lim else rows, i)


# ---------------------------------------------------------------- other languages
def lang_features(row):
    j = api(action="query", titles=row["title"], prop="langlinks", lllimit="max", redirects=1)
    links = {}
    if j:
        p = j["query"]["pages"][0]
        links = {l["lang"]: l["title"] for l in p.get("langlinks", []) if l["lang"] in LANGS}
    res = {}
    for lang, lt in links.items():
        two = []
        for d in (DATES[0], DATES[-1]):
            s = snap(lang, lt, d)
            if not s:
                two.append(None); continue
            wt = s[1]; fp = A.prose(wt); lp = A.prose(A.split_lead(wt))
            fw, lw = max(1, len(fp.split())), max(1, len(lp.split()))
            two.append({"revid": s[0], "fw": fw, "lw": lw,
                        "full": {k: len(rx.findall(fp)) for k, rx in XRX.items()},
                        "lead": {k: len(rx.findall(lp)) for k, rx in XRX.items()},
                        "fs": re.sub(r"\s+", " ", lp).strip()[:300]})
        res[lang] = {"title": lt, "snaps": two}
    return {"title": row["title"], "group": row["group"], "project": row["project"], "importance": row["importance"], "langs": res}


def run_lang(i, n):
    rows = json.load(open(os.path.join(OUT, "frame.json")))["rows"]
    pick = []
    for g in ("topic", "comparison"):
        G = [r for r in rows if r["group"] == g]
        G.sort(key=lambda r: LEVELS.index(r["importance"]))
        pick += G[:LANG_TOP_PER_GROUP]
    rows = shard(pick, i, n)
    lim = int(os.environ.get("MASS_LIMIT", "0"))
    _run("lang", lang_features, rows[:max(1, lim // 4)] if lim else rows, i)


# ---------------------------------------------------------------- analysis
def did(t, c, n_boot=2000, n_perm=3000, seed=9):
    t, c = np.array(t, float), np.array(c, float)
    if len(t) < 10 or len(c) < 10:
        return None
    rng = np.random.default_rng(seed)
    est = t.mean() - c.mean()
    bt = rng.choice(t, (n_boot, len(t))).mean(1) - rng.choice(c, (n_boot, len(c))).mean(1)
    pool = np.concatenate([t, c]); nt = len(t); perm = np.empty(n_perm)
    for k in range(n_perm):
        rng.shuffle(pool); perm[k] = pool[:nt].mean() - pool[nt:].mean()
    return {"did": float(est), "treat": float(t.mean()), "control": float(c.mean()),
            "lo": float(np.percentile(bt, 2.5)), "hi": float(np.percentile(bt, 97.5)),
            "p_perm": float((np.sum(np.abs(perm) >= abs(est)) + 1) / (n_perm + 1)), "n_t": int(len(t)), "n_c": int(len(c))}


def rate(sn, part, keys):
    if not sn or not sn.get(part):
        return None
    return sum(sn[part]["counts"][k] for k in keys) * 1e4 / sn[part]["words"]


def analyze():
    en = [r for f in sorted(glob.glob(os.path.join(OUT, "en_*.json.gz"))) for r in json.load(gzip.open(f, "rt"))]
    ln = [r for f in sorted(glob.glob(os.path.join(OUT, "lang_*.json.gz"))) for r in json.load(gzip.open(f, "rt"))]
    fr = json.load(open(os.path.join(OUT, "frame.json")))
    res = {"n_frame": len(fr["rows"]), "n_en": len(en), "category_counts": fr["category_counts"], "composition": fr.get("composition"),
           "excluded_both": fr["excluded_both"], "dates": [d[:10] for d in DATES]}
    outcomes = {"critical": A.CRITICAL, "connection": A.CONNECTION, **{k: [k] for k in A.FRAMES}}
    windows = {"whole": (0, 2), "pre_war": (0, 1), "post_war": (1, 2)}
    tests = []
    strata = {"all": lambda r: True, **{f"importance:{l}": (lambda l: lambda r: r["importance"] == l)(l) for l in LEVELS}}
    for sname, sf in strata.items():
        for part in ("full", "lead"):
            for oname, keys in outcomes.items():
                for wname, (a, b) in windows.items():
                    ch = {"topic": [], "comparison": []}
                    for r in en:
                        if not sf(r) or r["group"] not in ch:
                            continue
                        v0, v1 = rate(r["snaps"][a], part, keys), rate(r["snaps"][b], part, keys)
                        if v0 is not None and v1 is not None:
                            ch[r["group"]].append(v1 - v0)
                    d = did(ch["topic"], ch["comparison"])
                    if d:
                        tests.append({"stratum": sname, "part": part, "outcome": oname, "window": wname, **d})
    # per-project change (topic and comparison projects), whole window, full text critical
    proj = defaultdict(list)
    for r in en:
        v0, v1 = rate(r["snaps"][0], "full", A.CRITICAL), rate(r["snaps"][2], "full", A.CRITICAL)
        if v0 is not None and v1 is not None:
            proj[(r["group"], r["project"])].append(v1 - v0)
    res["by_project"] = [{"group": g, "project": p, "n": len(v), "mean_change": float(np.mean(v)),
                          "share_increased": float(np.mean(np.array(v) > 0))} for (g, p), v in proj.items() if len(v) >= 10]
    # distribution of article-level change (histogram) per group
    hist = {}
    for g in ("topic", "comparison"):
        v = [rate(r["snaps"][2], "full", A.CRITICAL) - rate(r["snaps"][0], "full", A.CRITICAL) for r in en
             if r["group"] == g and rate(r["snaps"][0], "full", A.CRITICAL) is not None and rate(r["snaps"][2], "full", A.CRITICAL) is not None]
        bins = np.linspace(-40, 40, 41)
        hist[g] = {"bins": bins.tolist(), "counts": np.histogram(np.clip(v, -40, 40), bins)[0].tolist(), "n": len(v),
                   "share_up": float(np.mean(np.array(v) > 0.5)) if v else None,
                   "share_down": float(np.mean(np.array(v) < -0.5)) if v else None}
    res["histogram"] = hist
    # hedging and sourcing at scale
    def pooled(g, idx, fn):
        rr = [r["snaps"][idx] for r in en if r["group"] == g and r["snaps"][idx]]
        return fn(rr)
    res["hedging"] = {g: [pooled(g, i, lambda rr: (sum(s["hedge"][1] for s in rr) / max(1, sum(s["hedge"][0] for s in rr))))
                          for i in range(3)] for g in ("topic", "comparison")}
    res["citations"] = {g: [pooled(g, i, lambda rr: {k: sum(s["refs"].get(k, 0) for s in rr) / max(1, sum(s["refs"].get("_total", 0) for s in rr))
                                                     for k in list(E.SOURCE_CLASSES) + ["Other"]}) for i in range(3)]
                        for g in ("topic", "comparison")}
    # first sentence: share whose first sentence contains a critical term, at each date
    res["first_sentence_critical"] = {g: [pooled(g, i, lambda rr: float(np.mean([sum(A.count(k, s["fs"]) for k in A.CRITICAL) > 0 for s in rr])))
                                          for i in range(3)] for g in ("topic", "comparison")}
    res["tests"] = tests
    # compact per-article export for the data lab (counts per frame at the 3 dates)
    FR = list(A.FRAMES)
    def pack(sn, part):
        return None if not sn or not sn.get(part) else [sn[part]["words"]] + [sn[part]["counts"][k] for k in FR]
    res["lab_frames"] = FR
    res["lab_articles"] = [{"t": r["title"], "g": r["group"][0], "p": r["project"], "i": r["importance"][0],
                            "f": [pack(s, "full") for s in r["snaps"]], "l": [pack(s, "lead") for s in r["snaps"]],
                            "e": len(r["edits"]), "rv": sum(x[4] for x in r["edits"])} for r in en]
    # activity and coordination at scale (aggregate only)
    from datetime import datetime, timezone
    WAR = datetime(2023, 10, 7, tzinfo=timezone.utc).timestamp()
    def epoch(s): return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()
    coord = {}
    rnd = random.Random(3)
    for g in ("topic", "comparison"):
        G = [r for r in en if r["group"] == g]
        for label, pre in (("pre_war", True), ("post_war", False)):
            per_article = []
            for r in G:
                e = sorted((epoch(t), u) for t, u, anon, bot, rev in r["edits"] if u and not anon and not bot and ((epoch(t) < WAR) == pre))
                per_article.append((r["title"], e))
            def tail(pa, shuffle):
                if shuffle:
                    allt = [t for _, e in pa for t, _ in e]
                    if not allt: return 0, 0
                    t0, span = min(allt), (max(allt) - min(allt)) or 1; off = {}
                    pa = [(ti, sorted(((t0 + ((t - t0 + off.setdefault(u, rnd.random() * span)) % span)), u) for t, u in e)) for ti, e in pa]
                pairs = defaultdict(set); n = 0
                for ti, e in pa:
                    n += len(e)
                    for i, (t, u) in enumerate(e):
                        j = i + 1
                        while j < len(e) and e[j][0] - t <= 1800:
                            if e[j][1] != u: pairs[(u, e[j][1])].add(ti)
                            j += 1
                return sum(1 for s in pairs.values() if len(s) >= 5), n
            obs, n = tail(per_article, False); nul, _ = tail(per_article, True)
            day = defaultdict(set); act = set()
            for ti, e in per_article:
                for t, u in e:
                    day[(u, int(t // 86400))].add(ti); act.add(u)
            sweeps = sum(1 for s in day.values() if len(s) >= 5)
            coord[f"{g}:{label}"] = {"articles": len(G), "edits": n, "recurring_pairs": obs, "null_pairs": nul,
                                     "ratio": obs / nul if nul else None, "pairs_per_10k_edits": obs * 1e4 / max(1, n),
                                     "sweeps_per_1000_editors": sweeps * 1000 / max(1, len(act)), "active_editors": len(act)}
    res["coordination"] = coord
    # languages
    lang_tests = []
    for lang in ["en"] + LANGS:
        for part, wkey in (("lead", "lw"), ("full", "fw")):
            ch = {"topic": [], "comparison": []}
            for r in ln:
                if lang == "en":
                    continue
                v = r["langs"].get(lang)
                if not v or not v["snaps"][0] or not v["snaps"][1]:
                    continue
                s0, s1 = v["snaps"]
                f = lambda s: sum(s[part].values()) * 1000 / s[wkey]
                ch[r["group"]].append(f(s1) - f(s0))
            d = did(ch["topic"], ch["comparison"]) if lang != "en" else None
            if d:
                lang_tests.append({"lang": lang, "part": part, "unit": "per 1,000 words", **d})
    res["languages"] = lang_tests
    res["lang_coverage"] = {lang: sum(1 for r in ln if lang in r["langs"]) for lang in LANGS}
    json.dump({"mass": res}, open(os.path.join(A.OUTDIR, "mass_results.json"), "w"))   # always its own file
    for t in tests:
        if t["stratum"] == "all" and t["outcome"] in ("critical", "connection") and t["window"] == "whole":
            print(f"MASS {t['part']} {t['outcome']}: DiD {t['did']:+.2f} [{t['lo']:+.2f},{t['hi']:+.2f}] p={t['p_perm']:.4f} n={t['n_t']}/{t['n_c']}")
    for t in lang_tests:
        print(f"LANG {t['lang']} {t['part']}: DiD {t['did']:+.3f} [{t['lo']:+.3f},{t['hi']:+.3f}] p={t['p_perm']:.4f} n={t['n_t']}/{t['n_c']}")
    print("coordination", json.dumps(coord, indent=0))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd"); ap.add_argument("--shard", type=int, default=0); ap.add_argument("--of", type=int, default=1)
    a = ap.parse_args()
    {"frame": frame, "analyze": analyze}.get(a.cmd, lambda: None)() if a.cmd in ("frame", "analyze") else \
        (run_en if a.cmd == "en" else run_lang)(a.shard, a.of)
