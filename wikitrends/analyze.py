"""Turn raw article histories into measurable framing and editing trends.

Usage: python analyze.py   -> data/results.json
"""
import difflib, glob, gzip, json, os, re, statistics as st
from collections import Counter, defaultdict
import random

HERE = os.path.dirname(__file__)
ART = os.path.join(HERE, "data", "articles")

# --- Lexicons -------------------------------------------------------------
# Each frame is a set of regexes. Counts are per 10,000 words of prose.
FRAMES = {
    "settler_colonial": [r"settler[- ]colonial\w*", r"\bcoloni[sz]\w*", r"\bcolonial\w*", r"\bcolonist\w*"],
    "apartheid": [r"\bapartheid\b"],
    "genocide": [r"\bgenocid\w*"],
    "ethnic_cleansing": [r"ethnic(?:ally)? cleans\w*"],
    "occupation": [r"\boccupation\b", r"\boccupied\b", r"\boccupying\b"],
    "nakba_expulsion": [r"\bnakba\b", r"\bexpul\w*", r"\bexpell\w*", r"\bdispossess\w*"],
    "war_crimes": [r"war crimes?", r"crimes? against humanity", r"collective punishment"],
    "indigenous_homeland": [r"\bindigenous\b", r"ancestral homeland", r"\bhomeland\b",
                            r"self-determination", r"land of israel", r"\beretz\b"],
    "persecution_antisemitism": [r"\bantisemit\w*", r"\banti-semit\w*", r"\bpersecut\w*", r"\bpogroms?\b"],
    "terrorism": [r"\bterroris[mt]\w*"],
    "militant": [r"\bmilitants?\b", r"\bmilitancy\b"],
}
# "critical" = frames associated with the anti-colonial narrative;
# "connection" = frames associated with Jewish historical/indigenous narrative.
CRITICAL = ["settler_colonial", "apartheid", "genocide", "ethnic_cleansing",
            "occupation", "nakba_expulsion", "war_crimes"]
CONNECTION = ["indigenous_homeland", "persecution_antisemitism"]
RX = {k: re.compile("|".join(v), re.I) for k, v in FRAMES.items()}

REVERTING = {"mw-undo", "mw-rollback", "mw-manual-revert"}
IP = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$|^[0-9a-f:]+:[0-9a-f:]+$", re.I)
WAR = "2023-10"


# --- Wikitext -> prose -----------------------------------------------------
def strip_templates(t):
    out, depth, i = [], 0, 0
    while i < len(t):
        if t.startswith("{{", i):
            depth += 1; i += 2; continue
        if t.startswith("}}", i) and depth:
            depth -= 1; i += 2; continue
        if not depth:
            out.append(t[i])
        i += 1
    return "".join(out)


def prose(wt):
    t = re.sub(r"<!--.*?-->", "", wt, flags=re.S)
    t = re.sub(r"<ref[^>/]*/>", "", t)
    t = re.sub(r"<ref[^>]*>.*?</ref>", "", t, flags=re.S | re.I)
    t = strip_templates(t)
    t = re.sub(r"\{\|.*?\|\}", "", t, flags=re.S)                 # tables
    t = re.sub(r"\[\[(?:File|Image|Category):[^\]]*\]\]", "", t, flags=re.I)
    t = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"\[https?://\S+ ([^\]]*)\]", r"\1", t)
    t = re.sub(r"'{2,}", "", t)
    t = re.sub(r"<[^>]+>", "", t)
    return t


def split_lead(wt):
    m = re.search(r"^==[^=]", wt, flags=re.M)
    return wt[:m.start()] if m else wt


def first_sentence(p):
    p = re.sub(r"\s+", " ", p).strip()
    m = re.search(r"(.{40,600}?[.!?])(\s|$)", p)
    return m.group(1) if m else p[:400]


def measure(p):
    words = max(1, len(re.findall(r"\w+", p)))
    c = {k: len(r.findall(p)) for k, r in RX.items()}
    rate = {k: v * 1e4 / words for k, v in c.items()}
    crit = sum(c[k] for k in CRITICAL); conn = sum(c[k] for k in CONNECTION)
    return {"words": words, "counts": c, "rate": rate,
            "critical_rate": crit * 1e4 / words,
            "connection_rate": conn * 1e4 / words,
            "critical_share": crit / (crit + conn) if crit + conn else None}


def quarter(ts):
    return f"{ts[:4]}-Q{(int(ts[5:7]) - 1) // 3 + 1}"


# --- Per-article -----------------------------------------------------------
def analyze_article(rec):
    snaps, last_text, series = rec["snapshots"], None, []
    for s in snaps:
        if s.get("text") is not None:
            last_text = s["text"]
        if last_text is None:
            continue
        lead_wt = split_lead(last_text)
        lp, fp = prose(lead_wt), prose(last_text)
        series.append({"date": s["date"][:7], "revid": s["revid"],
                       "full": measure(fp), "lead": measure(lp),
                       "first_sentence": first_sentence(lp), "lead_text": lp})

    q = defaultdict(lambda: Counter())
    editors_q = defaultdict(set)
    editors = Counter()
    for r in rec["revisions"]:
        k = quarter(r["timestamp"]); tags = set(r.get("tags") or [])
        u = r.get("user") or ""
        q[k]["edits"] += 1
        q[k]["reverted"] += "mw-reverted" in tags
        q[k]["reverting"] += bool(tags & REVERTING)
        q[k]["anon"] += bool(IP.match(u))
        q[k]["ec_protect_hint"] += "extendedconfirmed" in (r.get("comment") or "").lower()
        editors_q[k].add(u); editors[u] += 1
    for k in q:
        q[k]["editors"] = len(editors_q[k])
    talk = Counter(quarter(r["timestamp"]) for r in rec["talk_revisions"])
    for k, v in talk.items():
        q[k]["talk_edits"] = v

    n = sum(editors.values())
    top10 = sum(c for _, c in editors.most_common(10)) / n if n else None
    return {"title": rec["title"], "group": rec["group"], "subgroup": rec["subgroup"],
            "series": series, "quarters": {k: dict(v) for k, v in sorted(q.items())},
            "n_edits": n, "n_editors": len(editors), "top10_share": top10,
            "editor_set": set(editors), "pageviews": rec.get("pageviews", {})}


def at(series, ym):
    """Snapshot closest to (on/before) ym."""
    c = [s for s in series if s["date"] <= ym]
    return c[-1] if c else None


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def boot_ci(t, c, n=2000, seed=1):
    rnd = random.Random(seed); d = []
    for _ in range(n):
        tt = [rnd.choice(t) for _ in t]; cc = [rnd.choice(c) for _ in c]
        d.append(mean(tt) - mean(cc))
    d.sort()
    return d[int(.025 * n)], d[int(.975 * n)]


def lead_diff(a, b):
    sa, sb = re.split(r"(?<=[.!?])\s+", a.strip()), re.split(r"(?<=[.!?])\s+", b.strip())
    out = []
    for op in difflib.SequenceMatcher(None, sa, sb).get_opcodes():
        tag, i1, i2, j1, j2 = op
        if tag == "equal":
            out += [{"t": "=", "s": s} for s in sa[i1:i2]]
        else:
            out += [{"t": "-", "s": s} for s in sa[i1:i2]]
            out += [{"t": "+", "s": s} for s in sb[j1:j2]]
    return out


def main():
    arts = []
    for fn in sorted(glob.glob(os.path.join(ART, "*.json.gz"))):
        with gzip.open(fn, "rt", encoding="utf-8") as f:
            a = analyze_article(json.load(f))
        if a["series"]:
            arts.append(a)
    T = [a for a in arts if a["group"] == "treatment"]
    C = [a for a in arts if a["group"] == "control"]
    dates = sorted({s["date"] for a in arts for s in a["series"]})
    first, pre, last = dates[0], f"{WAR[:4]}-07", dates[-1]

    # 1. Frame trends over time (mean rate across articles, full text + lead)
    trends = {}
    for g, A in (("treatment", T), ("control", C)):
        trends[g] = {}
        for part in ("full", "lead"):
            rows = []
            for d in dates:
                ss = [at(a["series"], d) for a in A]
                ss = [s for s in ss if s]
                row = {"date": d, "n": len(ss),
                       "critical_rate": mean([s[part]["critical_rate"] for s in ss]),
                       "connection_rate": mean([s[part]["connection_rate"] for s in ss])}
                for k in FRAMES:
                    row[k] = mean([s[part]["rate"][k] for s in ss])
                rows.append(row)
            trends[g][part] = rows

    # 2. Difference-in-differences per frame (article-level change)
    def change(A, part, k, d0, d1):
        out = []
        for a in A:
            s0, s1 = at(a["series"], d0), at(a["series"], d1)
            if s0 and s1:
                v0 = s0[part][k] if k in ("critical_rate", "connection_rate") else s0[part]["rate"][k]
                v1 = s1[part][k] if k in ("critical_rate", "connection_rate") else s1[part]["rate"][k]
                out.append(v1 - v0)
        return out
    did = []
    for part in ("full", "lead"):
        for k in ["critical_rate", "connection_rate"] + list(FRAMES):
            for label, d0, d1 in (("whole window", first, last),
                                  ("pre-war (2021→Jul 2023)", first, pre),
                                  ("post-war (Jul 2023→now)", pre, last)):
                t, c = change(T, part, k, d0, d1), change(C, part, k, d0, d1)
                if len(t) > 5 and len(c) > 5:
                    lo, hi = boot_ci(t, c)
                    did.append({"part": part, "frame": k, "window": label,
                                "treat": mean(t), "control": mean(c),
                                "did": mean(t) - mean(c), "lo": lo, "hi": hi,
                                "n_t": len(t), "n_c": len(c)})

    # 3. Edit dynamics per quarter
    qs = sorted({k for a in arts for k in a["quarters"]})
    dyn = {}
    for g, A in (("treatment", T), ("control", C)):
        rows = []
        for k in qs:
            agg = Counter()
            for a in A:
                agg.update(a["quarters"].get(k, {}))
            e = agg["edits"] or 1
            rows.append({"q": k, "edits_per_article": agg["edits"] / len(A),
                         "talk_per_article": agg["talk_edits"] / len(A),
                         "editors_per_article": agg["editors"] / len(A),
                         "revert_rate": agg["reverted"] / e,
                         "anon_share": agg["anon"] / e})
        dyn[g] = rows

    # 4. Editor concentration across the treatment topic (anonymised)
    ecount = Counter()
    for a in T:
        for u in a["editor_set"]:
            ecount[u] += 1
    breadth = sorted(ecount.values(), reverse=True)
    conc = {"editors_total": len(ecount),
            "editors_on_10plus_articles": sum(v >= 10 for v in breadth),
            "editors_on_25plus_articles": sum(v >= 25 for v in breadth),
            "top_breadth": breadth[:50]}
    ccount = Counter()
    for a in C:
        for u in a["editor_set"]:
            ccount[u] += 1
    cb = sorted(ccount.values(), reverse=True)
    conc_c = {"editors_total": len(ccount),
              "editors_on_10plus_articles": sum(v >= 10 for v in cb),
              "editors_on_25plus_articles": sum(v >= 25 for v in cb),
              "top_breadth": cb[:50]}

    # 5. Per-article table + lead evolution
    table = []
    for a in arts:
        s0, s1 = a["series"][0], a["series"][-1]
        sp = at(a["series"], pre) or s0
        table.append({
            "title": a["title"], "group": a["group"], "subgroup": a["subgroup"],
            "edits": a["n_edits"], "editors": a["n_editors"], "top10": a["top10_share"],
            "views": sum(a["pageviews"].values()),
            "crit0": s0["full"]["critical_rate"], "crit1": s1["full"]["critical_rate"],
            "conn0": s0["full"]["connection_rate"], "conn1": s1["full"]["connection_rate"],
            "lcrit0": s0["lead"]["critical_rate"], "lcrit1": s1["lead"]["critical_rate"],
            "critpre": sp["full"]["critical_rate"],
            "words0": s0["full"]["words"], "words1": s1["full"]["words"],
            "frames0": s0["full"]["counts"], "frames1": s1["full"]["counts"],
            "lead_frames0": s0["lead"]["counts"], "lead_frames1": s1["lead"]["counts"],
            "first_sentences": [{"date": s["date"], "s": s["first_sentence"]} for s in a["series"]],
            "lead_diff": lead_diff(s0["lead_text"], s1["lead_text"]),
            "d0": s0["date"], "d1": s1["date"],
            "crit_series": [round(s["full"]["critical_rate"], 2) for s in a["series"]],
            "conn_series": [round(s["full"]["connection_rate"], 2) for s in a["series"]],
        })

    res = {"dates": dates, "frames": list(FRAMES), "critical": CRITICAL,
           "connection": CONNECTION, "lexicon": FRAMES,
           "n_treatment": len(T), "n_control": len(C),
           "total_revisions": sum(a["n_edits"] for a in arts),
           "trends": trends, "did": did, "dynamics": dyn,
           "concentration": {"treatment": conc, "control": conc_c},
           "articles": table}
    with open(os.path.join(HERE, "data", "results.json"), "w") as f:
        json.dump(res, f)
    print(f"analyzed {len(T)} treatment / {len(C)} control articles, "
          f"{res['total_revisions']} revisions")


if __name__ == "__main__":
    main()
