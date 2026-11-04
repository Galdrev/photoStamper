"""Turn raw article histories into measurable framing and editing trends.

Implements SPEC.md (pre-registered). Usage: python analyze.py -> data/results.json,
data/leads.json (for blind coding), data/kwic.json (for lexicon precision checks).
"""
import difflib, glob, gzip, json, os, random, re
from collections import Counter, defaultdict

import numpy as np

from corpus import CONTROL_CONTAMINATED, CONTROL_SHOCKED, VALIDATION, KEY_ARTICLES, KEY_ARTICLES_CONTROL

KEY_SET = set(KEY_ARTICLES) | set(KEY_ARTICLES_CONTROL)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
ART = os.environ.get("WIKITRENDS_ART", os.path.join(DATA, "articles"))
OUTDIR = os.environ.get("WIKITRENDS_OUT", DATA)
RNG = np.random.default_rng(7)
N_PERM, N_BOOT = 5000, 2000
MIN_WORDS_FULL, MIN_WORDS_LEAD = 300, 40
FIRST_POST_WAR = "2024-01"     # first quarterly snapshot after 7 Oct 2023
PRE_WAR = "2023-07"            # last clean pre-war snapshot (2023-10-01 is a week before)

# --- Lexicons --------------------------------------------------------------
# Each frame: include patterns, exclude patterns (matches subtracted).
# Anchors are deliberately symmetric so comparison articles can score too
# ("occupied Crimea" counts the same as "occupied West Bank").
F = {
    "settler_colonial": ([r"settler[- ]colonial\w*", r"\bcoloni[sz](?:ation|ations|e|es|ed|ing|er|ers)\b",
                          r"colonial (?:project|enterprise|state|regime|venture)", r"\bcolonialis[mt]s?\b"],
                         [r"(?:greek|phoenician|roman|spanish|portuguese|space|mars) coloni[sz]"]),
    "apartheid": ([r"\bapartheid\b"], []),
    "genocide": ([r"\bgenocid\w*"], []),
    "ethnic_cleansing": ([r"ethnic(?:ally)? cleans\w*"], []),
    "occupation": ([r"occupied territor\w*", r"(?:military|belligerent|illegal|foreign|israeli|russian|turkish|moroccan|indian|pakistani|chinese|armenian|azerbaijani) occupation",
                    r"occupying (?:power|forces?|army)", r"under occupation",
                    r"occupation of (?:the )?(?:west bank|gaza|palestin\w*|golan|east jerusalem|crimea|northern cyprus|kashmir|tibet|western sahara|donbas|nagorno)",
                    r"occupied (?:west bank|gaza|palestin\w*|golan|east jerusalem|crimea|northern cyprus|kashmir|tibet|western sahara|ukrain\w*)"],
                   [r"(?:german|nazi|axis|japanese|ottoman|british|roman|allied|soviet) (?:military )?occupation"]),
    "nakba_expulsion": ([r"\bnakba\b", r"\bdispossess\w*", r"\bexpul\w*", r"\bexpell\w*"],
                        [r"expul\w* of (?:the )?jews", r"expell\w* (?:the )?jews", r"jews (?:were|was) expell\w*",
                         r"jewish expul\w*", r"expul\w* of jews", r"alhambra", r"edict of expulsion"]),
    "war_crimes": ([r"war crimes?", r"crimes? against humanity", r"collective punishment"], []),
    "indigenous_homeland": ([r"\bindigenous\b", r"ancestral homeland", r"\bhomeland\b", r"self-determination",
                             r"land of israel", r"\beretz\b", r"jewish (?:connection|continuity|presence) (?:to|in|with)"],
                            [r"palestinian (?:homeland|self-determination)", r"indigenous palestin\w*",
                             r"palestinians? (?:as|are) (?:the )?indigenous", r"kurdish (?:homeland|self-determination)"]),
    "persecution_antisemitism": ([r"\bantisemit\w*", r"\banti-semit\w*", r"\bpersecut\w*", r"\bpogroms?\b"], []),
    "terrorism": ([r"\bterroris[mt]\w*"], []),
    "militant": ([r"\bmilitants?\b", r"\bmilitancy\b"], []),
    # placebo lexicon: geography/climate vocabulary that should not move by group
    "placebo_geography": ([r"\brivers?\b", r"\bmountains?\b", r"\bdeserts?\b", r"\bclimate\b", r"\brainfall\b",
                           r"\bcoast(?:al|line)?\b", r"\bvalleys?\b"], []),
}
CRITICAL = ["settler_colonial", "apartheid", "genocide", "ethnic_cleansing", "occupation", "nakba_expulsion", "war_crimes"]
CONNECTION = ["indigenous_homeland", "persecution_antisemitism"]
FRAMES = list(F)
RXI = {k: [re.compile(p, re.I) for p in inc] for k, (inc, exc) in F.items()}
RXE = {k: [re.compile(p, re.I) for p in exc] for k, (inc, exc) in F.items()}

REVERTING = {"mw-undo", "mw-rollback", "mw-manual-revert"}
ANON = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$|^[0-9a-f]{0,4}(:[0-9a-f]{0,4}){2,7}$|^~\d{4}-", re.I)
BOT = re.compile(r"bot\b", re.I)
BACKMATTER = re.compile(r"^==\s*(See also|Notes|References|Citations|Further reading|External links|Bibliography|Sources|Footnotes)\s*==",
                        re.M | re.I)


# Words for the "word race" playground (exploratory, descriptive only)
WORD_RACE = ["colonial", "colonization", "settler", "settlers", "apartheid", "genocide", "occupation", "occupied",
             "Nakba", "indigenous", "homeland", "Zionist", "Zionism", "antisemitism", "antisemitic", "terrorist",
             "terrorism", "militant", "resistance", "massacre", "pogrom", "Holocaust", "displacement", "expulsion",
             "refugees", "ethnic cleansing", "war crimes", "human rights", "international law", "illegal",
             "self-determination", "Jewish", "Jews", "Palestinian", "Palestinians", "Israeli", "Arab", "Hamas",
             "Gaza", "West Bank", "democracy", "ethnostate", "supremacy", "racism", "liberation", "martyr",
             "hostage", "hostages", "rape", "children", "civilians", "famine", "starvation", "siege", "blockade",
             "ceasefire", "peace", "two-state", "diaspora", "persecution", "survivors", "ancestral", "biblical",
             "ancient", "Temple", "Jerusalem", "Holy Land", "Canaan", "Judea", "Samaria", "Levant", "Ottoman",
             "British Mandate", "UN", "ICJ", "Amnesty", "B'Tselem", "scholars", "historians", "critics", "alleged"]
WORD_RX = {w: re.compile(r"\b" + re.escape(w) + (r"s?\b" if w[-1].isalpha() else r"\b"), re.I) for w in WORD_RACE}


# --- Wikitext -> prose ------------------------------------------------------
def strip_nested(t, open_, close, keep=None):
    """Remove nested open_...close blocks (e.g. {{ }} or [[File: ]])."""
    out, depth, i = [], 0, 0
    while i < len(t):
        if t.startswith(open_, i):
            depth += 1; i += len(open_); continue
        if depth and t.startswith(close, i):
            depth -= 1; i += len(close); continue
        if not depth:
            out.append(t[i])
        i += 1
    return "".join(out)


def table_text(t):
    """Keep wikitable cell text (list articles hold their content in tables)."""
    out = []
    for line in t.split("\n"):
        ls = line.lstrip()
        if ls.startswith(("{|", "|}", "|-", "|+")):
            continue
        if ls.startswith(("|", "!")):
            cells = re.split(r"\|\||!!", ls[1:])
            vals = []
            for c in cells:
                # drop cell attributes:  style="..." | content  (but not [[a|b]] links)
                m = re.match(r'^\s*[a-z\-]+\s*=\s*"[^"]*"(?:\s*[a-z\-]+\s*=\s*"[^"]*")*\s*\|(?!\|)(.*)$', c, re.I)
                vals.append((m.group(1) if m else c).strip())
            out.append(". ".join(v for v in vals if v))
        else:
            out.append(line)
    return "\n".join(out)


def strip_files(t):
    out, i = [], 0
    pat = re.compile(r"\[\[(?:File|Image):", re.I)
    while True:
        m = pat.search(t, i)
        if not m:
            out.append(t[i:]); break
        out.append(t[i:m.start()])
        j, depth = m.start(), 0
        while j < len(t):
            if t.startswith("[[", j): depth += 1; j += 2; continue
            if t.startswith("]]", j):
                depth -= 1; j += 2
                if depth == 0: break
                continue
            j += 1
        i = j
    return "".join(out)


def prose(wt):
    t = BACKMATTER.split(wt)[0]
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = re.sub(r"<ref[^>]*?/\s*>", "", t, flags=re.I)
    t = re.sub(r"<ref[^>]*>.*?</ref\s*>", "", t, flags=re.S | re.I)
    t = re.sub(r"\{\{\s*(?:lang|transl|langx)\|[^|{}]*\|([^|{}]*)(?:\|[^{}]*)?\}\}", r"\1", t, flags=re.I)
    t = strip_nested(t, "{{", "}}")
    t = table_text(t)
    t = strip_files(t)
    t = re.sub(r"\[\[Category:[^\]]*\]\]", "", t, flags=re.I)
    t = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"\[https?://\S+ ([^\]]*)\]", r"\1", t)
    t = re.sub(r"'{2,}", "", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"\(\s*(?:[;,]\s*)*\)", "", t)          # parentheses emptied by template stripping
    t = re.sub(r"\(\s*(?:[;,]\s*)+", "(", t)
    t = re.sub(r" +([,.;])", r"\1", t)
    return t


def split_lead(wt):
    m = re.search(r"^==[^=]", wt, flags=re.M)
    return wt[:m.start()] if m else wt


ABBR = re.compile(r"\b(?:c|ca|U\.S|U\.K|St|Mr|Dr|e\.g|i\.e|vs|BCE|CE|BC|AD)\.$")


def sentences(p):
    p = re.sub(r"\s+", " ", p).strip()
    parts, buf = [], ""
    for chunk in re.split(r"(?<=[.!?])\s+", p):
        buf = f"{buf} {chunk}".strip() if buf else chunk
        if not ABBR.search(buf):
            parts.append(buf); buf = ""
    if buf:
        parts.append(buf)
    return [s for s in parts if s]


def count(k, p):
    inc = sum(len(r.findall(p)) for r in RXI[k])
    exc = sum(len(r.findall(p)) for r in RXE[k])
    return max(0, inc - exc)


def measure(p, min_words):
    words = len(re.findall(r"\w+", p))
    if words < min_words:
        return None
    c = {k: count(k, p) for k in FRAMES}
    rate = {k: v * 1e4 / words for k, v in c.items()}
    crit = sum(c[k] for k in CRITICAL); conn = sum(c[k] for k in CONNECTION)
    rate["critical_rate"] = crit * 1e4 / words
    rate["connection_rate"] = conn * 1e4 / words
    return {"words": words, "counts": c, "rate": rate}


WEEK0 = "2021-01-01"
_W0 = np.datetime64(WEEK0)
N_WEEKS = int((np.datetime64("today") - _W0) / np.timedelta64(7, "D")) + 1


def week_index(ts):
    return int((np.datetime64(ts[:10]) - _W0) / np.timedelta64(7, "D"))


def weekly(c):
    """Comma-joined weekly counts, empty string for zero (compact)."""
    return ",".join(str(c[i]) if c.get(i) else "" for i in range(N_WEEKS))


def quarter(ts):
    return f"{ts[:4]}-Q{(int(ts[5:7]) - 1) // 3 + 1}"


# --- Per-article --------------------------------------------------------------
def analyze_article(rec):
    rev_tags = {r["revid"]: set(r.get("tags") or []) for r in rec["revisions"]}
    series, last_text, last_rev = [], None, None
    for s in rec["snapshots"]:
        t = s.get("text")
        if t is not None:
            # skip snapshots that are redirects or that landed on a later-reverted edit
            if re.match(r"\s*#redirect", t, re.I) or "mw-reverted" in rev_tags.get(s["revid"], ()):
                if re.match(r"\s*#redirect", t, re.I):
                    last_text = None
                continue
            last_text, last_rev = t, s["revid"]
        if last_text is None:
            continue
        lead_wt = split_lead(last_text)
        fp, lp = prose(last_text), prose(lead_wt)
        full, lead = measure(fp, MIN_WORDS_FULL), measure(lp, MIN_WORDS_LEAD)
        if full is None:
            continue
        sents = sentences(lp)
        series.append({"date": s["date"][:7], "revid": last_rev, "full": full, "lead": lead,
                       "first_sentence": sents[0] if sents else "", "lead_text": lp.strip(), "_fp": fp})

    weeks, weeks_rev = Counter(), Counter()
    for r in rec["revisions"]:
        w = week_index(r["timestamp"])
        weeks[w] += 1
        if "mw-reverted" in (r.get("tags") or []):
            weeks_rev[w] += 1
    q = defaultdict(Counter)
    editors_q = defaultdict(set)
    editors = Counter()
    for r in rec["revisions"]:
        u = r.get("user") or ""
        if not u or BOT.search(u):
            continue
        k = quarter(r["timestamp"]); tags = set(r.get("tags") or [])
        q[k]["edits"] += 1
        q[k]["reverted"] += "mw-reverted" in tags
        q[k]["reverting"] += bool(tags & REVERTING)
        q[k]["anon"] += bool(ANON.match(u))
        editors_q[k].add(u); editors[u] += 1
    for k in q:
        q[k]["editors"] = len(editors_q[k])
    for r in rec["talk_revisions"]:
        u = r.get("user") or ""
        if u and not BOT.search(u):
            q[quarter(r["timestamp"])]["talk_edits"] += 1
    n = sum(editors.values())
    return {"title": rec["title"], "group": rec["group"], "subgroup": rec["subgroup"],
            "series": series, "quarters": {k: dict(v) for k, v in sorted(q.items())},
            "n_edits": n, "n_editors": len(editors),
            "top10_share": sum(c for _, c in editors.most_common(10)) / n if n else None,
            "editor_set": set(editors), "pageviews": rec.get("pageviews", {}),
            "weeks": weeks, "weeks_rev": weeks_rev}


def at(series, ym):
    c = [s for s in series if s["date"] <= ym]
    return c[-1] if c else None


def exact(series, ym):
    for s in series:
        if s["date"] == ym:
            return s
    return None


def val(s, part, k):
    if s is None or s[part] is None:
        return None
    return s[part]["rate"][k]


# --- Statistics ----------------------------------------------------------------
# Primary scale (SPEC): absolute change in hits per 10k words. R7 re-runs on a log scale.
_SCALE = {"c": None}


def TF(v):
    return v if _SCALE["c"] is None else np.log(v + _SCALE["c"])
def changes(A, part, k, d0, d1, log=True):
    out = []
    for a in A:
        v0, v1 = val(exact(a["series"], d0), part, k), val(at(a["series"], d1), part, k)
        if v0 is not None and v1 is not None:
            out.append(TF(v1) - TF(v0))
    return np.array(out)


def did_test(t, c, weights_c=None):
    if len(t) < 5 or len(c) < 5:
        return None
    est = t.mean() - (np.average(c, weights=weights_c) if weights_c is not None else c.mean())
    pooled = np.concatenate([t, c]); nt = len(t)
    perm = np.empty(N_PERM)
    for i in range(N_PERM):
        RNG.shuffle(pooled)
        perm[i] = pooled[:nt].mean() - pooled[nt:].mean()
    p = (np.sum(np.abs(perm) >= abs(est)) + 1) / (N_PERM + 1)
    bt = RNG.choice(t, (N_BOOT, len(t))).mean(1) - RNG.choice(c, (N_BOOT, len(c))).mean(1)
    lo, hi = np.percentile(bt, [2.5, 97.5])
    return {"did": float(est), "treat": float(t.mean()), "control": float(c.mean()),
            "lo": float(lo), "hi": float(hi), "p_perm": float(p), "n_t": int(len(t)), "n_c": int(len(c)),
            "_perm": perm, "_t": t, "_c": c}


def bh(rows, key="p_perm"):
    ps = sorted(((r[key], i) for i, r in enumerate(rows)), key=lambda x: x[0])
    m = len(ps); qs = [0.0] * m; prev = 1.0
    for rank in range(m, 0, -1):
        p, i = ps[rank - 1]
        prev = min(prev, p * m / rank); qs[i] = prev
    for r, qv in zip(rows, qs):
        r["q_bh"] = qv


def mean(xs):
    xs = [x for x in xs if x is not None]
    return float(np.mean(xs)) if xs else None


def lead_diff(a, b):
    sa, sb = sentences(a), sentences(b)
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, sa, sb).get_opcodes():
        if tag == "equal":
            out += [{"t": "=", "s": s} for s in sa[i1:i2]]
        else:
            out += [{"t": "-", "s": s} for s in sa[i1:i2]]
            out += [{"t": "+", "s": s} for s in sb[j1:j2]]
    return out


# --- Main ----------------------------------------------------------------------
def main():
    manifest_p = os.path.join(DATA, "manifest.json")
    manifest = json.load(open(manifest_p)) if os.path.exists(manifest_p) else {}
    arts = []
    for fn in sorted(glob.glob(os.path.join(ART, "*.json.gz"))):
        with gzip.open(fn, "rt", encoding="utf-8") as f:
            rec = json.load(f)
        if rec["title"] in manifest:                     # labels come from the manifest, not the cache
            rec["group"], rec["subgroup"] = manifest[rec["title"]]
        a = analyze_article(rec)
        if a["series"]:
            arts.append(a)
    dates = sorted({s["date"] for a in arts for s in a["series"]})
    first, last = dates[0], dates[-1]
    for a in arts:
        a["created_in_window"] = exact(a["series"], first) is None
        if a["group"] == "control" and a["title"] in CONTROL_CONTAMINATED:
            a["group"] = "control_contaminated"
        a["shocked"] = a["title"] in CONTROL_SHOCKED
        a["primary"] = not a["created_in_window"] and a["group"] in ("treatment", "control")

    T = [a for a in arts if a["primary"] and a["group"] == "treatment"]
    C = [a for a in arts if a["primary"] and a["group"] == "control"]
    T_hand = [a for a in T if a["subgroup"] != "category-sample"]
    C_quiet = [a for a in C if not a["shocked"]]
    C_shock = [a for a in C if a["shocked"]]

    # 1. Balanced-panel trends + event study (DiD at each snapshot vs first)
    trends = {}
    for g, A in (("treatment", T), ("control", C), ("treatment_hand", T_hand), ("control_quiet", C_quiet), ("control_shocked", C_shock)):
        trends[g] = {}
        for part in ("full", "lead"):
            rows = []
            for d in dates:
                row = {"date": d, "n": len(A)}
                for k in ["critical_rate", "connection_rate"] + FRAMES:
                    row[k] = mean([val(at(a["series"], d), part, k) for a in A])
                rows.append(row)
            trends[g][part] = rows
    new_articles = [a for a in arts if a["created_in_window"] and a["group"] == "treatment"]
    trends["treatment_new"] = {"full": [{"date": d, "n": sum(1 for a in new_articles if at(a["series"], d)),
                                         "critical_rate": mean([val(at(a["series"], d), "full", "critical_rate") for a in new_articles])}
                                        for d in dates]}

    event_study = {}
    for part in ("full", "lead"):
        for k in ("critical_rate", "connection_rate"):
            rows = []
            for d in dates[1:]:
                r = did_test(changes(T, part, k, first, d), changes(C, part, k, first, d))
                if r:
                    for kk in ("_perm", "_t", "_c"):
                        r.pop(kk, None)
                    rows.append({"date": d, "did": r["did"], "lo": r["lo"], "hi": r["hi"]})
            event_study[f"{part}:{k}"] = rows

    # 2. Pre-registered tests
    windows = [("whole window", first, last), ("pre-war", first, PRE_WAR), ("post-war", PRE_WAR, last)]
    primary_defs = [("P1", "lead", "critical_rate"), ("P2", "full", "critical_rate"), ("P3", "full", "connection_rate")]
    did_rows = []
    for part in ("full", "lead"):
        for k in ["critical_rate", "connection_rate"] + FRAMES:
            for label, d0, d1 in windows:
                if d0 == d1:
                    continue
                t = changes(T, part, k, d0, d1) if d0 == first else np.array(
                    [TF(val(at(a["series"], d1), part, k)) - TF(val(at(a["series"], d0), part, k))
                     for a in T if val(at(a["series"], d0), part, k) is not None and val(at(a["series"], d1), part, k) is not None])
                c = changes(C, part, k, d0, d1) if d0 == first else np.array(
                    [TF(val(at(a["series"], d1), part, k)) - TF(val(at(a["series"], d0), part, k))
                     for a in C if val(at(a["series"], d0), part, k) is not None and val(at(a["series"], d1), part, k) is not None])
                r = did_test(t, c)
                if not r:
                    continue
                pid = next((p for p, pp, kk in primary_defs if pp == part and kk == k and label == "whole window"), None)
                r.update(part=part, frame=k, window=label, scale="change in hits per 10k words",
                         tier="primary" if pid else "secondary", id=pid)
                did_rows.append(r)
    # keep a sample of the chance distribution and the per-article changes for primaries; strip elsewhere
    for r in did_rows:
        if r["tier"] == "primary":
            r["perm_sample"] = [round(float(x), 4) for x in r["_perm"][::25]]
            r["changes_t"] = [round(float(x), 3) for x in r["_t"]]
            r["changes_c"] = [round(float(x), 3) for x in r["_c"]]
        for k in ("_perm", "_t", "_c"):
            r.pop(k, None)
    bh([r for r in did_rows if r["tier"] == "primary"])
    bh([r for r in did_rows if r["tier"] == "secondary"])

    # 3. Robustness for primaries
    robust = []
    def chk(pid, name, est_row, passed, note=""):
        if est_row:
            for k in ("_perm", "_t", "_c"):
                est_row.pop(k, None)
        robust.append({"id": pid, "check": name, "did": est_row and est_row["did"], "lo": est_row and est_row["lo"],
                       "hi": est_row and est_row["hi"], "p": est_row and est_row["p_perm"], "pass": bool(passed), "note": note})
    for pid, part, k in primary_defs:
        base = next(r for r in did_rows if r["id"] == pid)
        sign = np.sign(base["did"])
        same = lambda r: r is not None and np.sign(r["did"]) == sign and r["p_perm"] < 0.05
        r1 = did_test(changes(T_hand, part, k, first, last), changes(C, part, k, first, last))
        chk(pid, "R1 hand-picked topic articles only", r1, same(r1))
        r1b = did_test(changes(T, part, k, first, last), changes(C_quiet, part, k, first, last))
        chk(pid, "R1b quiet comparison articles only (no own war/shock)", r1b, same(r1b))
        # R2 leave-one-frame-out (for composite rates)
        comps = CRITICAL if k == "critical_rate" else CONNECTION if k == "connection_rate" else []
        worst = None
        for drop in comps:
            keep = [x for x in comps if x != drop]
            def comp_changes(A):
                out = []
                for a in A:
                    s0, s1 = exact(a["series"], first), at(a["series"], last)
                    if s0 and s1 and s0[part] and s1[part]:
                        v0 = sum(s0[part]["rate"][x] for x in keep); v1 = sum(s1[part]["rate"][x] for x in keep)
                        out.append(TF(v1) - TF(v0))
                return np.array(out)
            r = did_test(comp_changes(T), comp_changes(C))
            if r and (worst is None or abs(r["did"]) < abs(worst[1]["did"])):
                worst = (drop, r)
        if worst:
            chk(pid, f"R2 leave-one-frame-out (weakest: without {worst[0]})", worst[1], same(worst[1]))
        # R3 placebo windows: annualised DiD in 4-quarter windows before the war
        yearly = []
        pre_dates = [d for d in dates if d <= PRE_WAR]
        for i in range(len(pre_dates) - 4):
            d0, d1 = pre_dates[i], pre_dates[i + 4]
            tt = [TF(val(at(a["series"], d1), part, k)) - TF(val(at(a["series"], d0), part, k))
                  for a in T if val(at(a["series"], d0), part, k) is not None]
            cc = [TF(val(at(a["series"], d1), part, k)) - TF(val(at(a["series"], d0), part, k))
                  for a in C if val(at(a["series"], d0), part, k) is not None]
            if tt and cc:
                yearly.append(float(np.mean(tt) - np.mean(cc)))
        post = next((r for r in did_rows if r["part"] == part and r["frame"] == k and r["window"] == "post-war"), None)
        n_years_post = max(0.25, (int(last[:4]) - 2023) + (int(last[5:7]) - 7) / 12)
        post_ann = post["did"] / n_years_post if post else None
        if yearly and post_ann is not None:
            chk(pid, "R3 post-war yearly change exceeds every pre-war placebo year",
                {"did": post_ann, "lo": min(yearly), "hi": max(yearly), "p_perm": None},
                abs(post_ann) > max(abs(y) for y in yearly), f"placebo years: {', '.join(f'{y:+.3f}' for y in yearly)}")
        # R4 length-matched comparison weights
        def words0(a): s = exact(a["series"], first); return s["full"]["words"] if s else None
        tw = np.log([words0(a) for a in T if words0(a)]); cw_list = [a for a in C if words0(a)]
        bins = np.quantile(tw, np.linspace(0, 1, 6)); bins[0] -= 1; bins[-1] += 1
        tb = np.histogram(tw, bins)[0] / len(tw)
        cb_idx = np.clip(np.digitize(np.log([words0(a) for a in cw_list]), bins) - 1, 0, 4)
        cb = np.bincount(cb_idx, minlength=5) / len(cw_list)
        wmap = {a["title"]: (tb[i] / cb[i] if cb[i] else 0) for a, i in zip(cw_list, cb_idx)}
        cc, ww = [], []
        for a in C:
            s0, s1 = exact(a["series"], first), at(a["series"], last)
            if a["title"] in wmap and val(s0, part, k) is not None and val(s1, part, k) is not None:
                cc.append(TF(val(s1, part, k)) - TF(val(s0, part, k))); ww.append(wmap[a["title"]])
        r4 = did_test(changes(T, part, k, first, last), np.array(cc), weights_c=np.array(ww) if sum(ww) else None)
        chk(pid, "R4 comparison reweighted to topic article lengths", r4, same(r4))
        # R5 medians
        t, c = changes(T, part, k, first, last), changes(C, part, k, first, last)
        med = float(np.median(t) - np.median(c))
        chk(pid, "R5 median instead of mean", {"did": med, "lo": None, "hi": None, "p_perm": None}, np.sign(med) == sign)
        # R7 log scale, offset = median non-zero baseline rate across all primary articles
        base_rates = [val(exact(a["series"], first), part, k) for a in T + C]
        nz = [x for x in base_rates if x]
        _SCALE["c"] = float(np.median(nz)) if nz else 1.0
        r7 = did_test(changes(T, part, k, first, last), changes(C, part, k, first, last))
        chk(pid, f"R7 log scale (log(rate + {_SCALE['c']:.1f}))", r7, same(r7))
        _SCALE["c"] = None
        # R6 placebo lexicon
        r6 = did_test(changes(T, part, "placebo_geography", first, last), changes(C, part, "placebo_geography", first, last))
        chk(pid, "R6 placebo vocabulary (geography/climate) shows no group difference", r6,
            r6 is not None and r6["p_perm"] >= 0.05, "instrument check: should NOT be significant")

    # 4. Validation targets
    validation = []
    by_title = {a["title"]: a for a in arts}
    for v in VALIDATION:
        a = by_title.get(v["title"])
        if not a:
            validation.append({**v, "observed": "article not in data", "pass": None}); continue
        part = v.get("part", "lead")
        rx = re.compile(v["pattern"], re.I)
        def has(d):
            s = at(a["series"], d)
            if not s: return None
            txt = s["lead_text"] if part == "lead" else s["_fp"]
            return bool(rx.search(txt))
        b, af = has(v["before"]), has(v["after"])
        validation.append({**v, "observed": f"before={b}, after={af}", "pass": (b is False and af is True)})

    # 5. Edit dynamics (balanced panel, per-article means; drop the partial last quarter)
    qs = sorted({k for a in arts for k in a["quarters"]})[:-1]
    dyn = {}
    for g, A in (("treatment", T), ("control", C), ("treatment_new", new_articles)):
        rows = []
        for k in qs:
            per = [a["quarters"].get(k, {}) for a in A]
            rr = [p["reverted"] / p["edits"] for p in per if p.get("edits", 0) >= 5]
            an = [p["anon"] / p["edits"] for p in per if p.get("edits", 0) >= 5]
            rows.append({"q": k, "edits_per_article": mean([p.get("edits", 0) for p in per]),
                         "talk_per_article": mean([p.get("talk_edits", 0) for p in per]),
                         "editors_per_article": mean([p.get("editors", 0) for p in per]),
                         "revert_rate": mean(rr), "anon_share": mean(an)})
        dyn[g] = rows

    # 6. Editor breadth, equal-size subsamples
    def breadth(A, n, reps=50):
        r10, r25, tot = [], [], []
        for _ in range(reps):
            S = random.Random(_).sample(A, min(n, len(A)))
            cnt = Counter(u for a in S for u in a["editor_set"])
            r10.append(sum(v >= 10 for v in cnt.values())); r25.append(sum(v >= 25 for v in cnt.values())); tot.append(len(cnt))
        return {"articles_per_sample": min(n, len(A)), "editors_total": float(np.mean(tot)),
                "editors_on_10plus_articles": float(np.mean(r10)), "editors_on_25plus_articles": float(np.mean(r25))}
    n_eq = min(len(T), len(C))
    conc = {"treatment": breadth(T, n_eq), "control": breadth(C, n_eq)}

    # 7. Per-article ledger + exports
    table, leads, kwic = [], [], defaultdict(list)
    for a in arts:
        s0, s1 = a["series"][0], a["series"][-1]
        rv = lambda s, part, k: None if s[part] is None else round(s[part]["rate"][k], 3)
        table.append({
            "title": a["title"], "group": a["group"], "subgroup": a["subgroup"], "primary": a["primary"],
            "created_in_window": a["created_in_window"], "shocked": a["shocked"],
            "edits": a["n_edits"], "editors": a["n_editors"],
            "top10": None if a["top10_share"] is None else round(a["top10_share"], 3),
            "views": sum(a["pageviews"].values()),
            "d0": s0["date"], "d1": s1["date"], "rev0": s0["revid"], "rev1": s1["revid"],
            "crit0": rv(s0, "full", "critical_rate"), "crit1": rv(s1, "full", "critical_rate"),
            "conn0": rv(s0, "full", "connection_rate"), "conn1": rv(s1, "full", "connection_rate"),
            "lcrit0": rv(s0, "lead", "critical_rate"), "lcrit1": rv(s1, "lead", "critical_rate"),
            "words0": s0["full"]["words"], "words1": s1["full"]["words"],
            "frames0": s0["full"]["counts"], "frames1": s1["full"]["counts"],
            "lead_frames0": s0["lead"]["counts"] if s0["lead"] else None,
            "lead_frames1": s1["lead"]["counts"] if s1["lead"] else None,
            "first_sentences": [{"date": s["date"], "revid": s["revid"], "s": s["first_sentence"]} for s in a["series"]],
            "lead_diff": lead_diff(s0["lead_text"], s1["lead_text"]),
            "crit_series_dates": [s["date"] for s in a["series"]],
            "w_edits": weekly(a["weeks"]), "w_reverted": weekly(a["weeks_rev"]),
            "crit_series": [round(s["full"]["rate"]["critical_rate"], 2) for s in a["series"]],
            "conn_series": [round(s["full"]["rate"]["connection_rate"], 2) for s in a["series"]],
            "frame_series": {k: [s["full"]["counts"][k] for s in a["series"]] for k in FRAMES},
            "lead_frame_series": {k: [None if s["lead"] is None else s["lead"]["counts"][k] for s in a["series"]] for k in FRAMES},
            "words_series": [s["full"]["words"] for s in a["series"]],
            "lead_words_series": [None if s["lead"] is None else s["lead"]["words"] for s in a["series"]],
            "revert_rate": (sum(v.get("reverted", 0) for v in a["quarters"].values()) / max(1, sum(v.get("edits", 0) for v in a["quarters"].values()))),
            "talk_edits": sum(v.get("talk_edits", 0) for v in a["quarters"].values()),
            "lcrit_series": [None if s["lead"] is None else round(s["lead"]["rate"]["critical_rate"], 2) for s in a["series"]],
            "quarter_edits": {k: v.get("edits", 0) for k, v in a["quarters"].items()},
            "pv_monthly": a["pageviews"] if a["title"] in KEY_SET else None,
        })
        if s0["lead_text"] != s1["lead_text"]:
            leads.append({"title": a["title"], "group": a["group"], "primary": a["primary"],
                          "d0": s0["date"], "d1": s1["date"], "rev0": s0["revid"], "rev1": s1["revid"],
                          "lead0": s0["lead_text"], "lead1": s1["lead_text"]})
        if a["group"] in ("treatment", "control"):
            fp = s1["_fp"]
            for k in FRAMES:
                for r in RXI[k]:
                    for m in r.finditer(fp):
                        kwic[k].append({"title": a["title"], "group": a["group"],
                                        "ctx": re.sub(r"\s+", " ", fp[max(0, m.start() - 90):m.end() + 90])})
    kw = {k: random.Random(1).sample(v, min(40, len(v))) for k, v in kwic.items()}

    # Word race: pooled hits per 10k words per group per date (balanced panel)
    word_race = {"words": WORD_RACE, "dates": dates}
    for g, A_ in (("topic", T), ("comparison", C)):
        rows = {w: [] for w in WORD_RACE}
        for d in dates:
            snaps = [at(a["series"], d) for a in A_]
            snaps = [x for x in snaps if x]
            tw = sum(x["full"]["words"] for x in snaps) or 1
            for w, rx in WORD_RX.items():
                rows[w].append(round(sum(len(rx.findall(x["_fp"])) for x in snaps) * 1e4 / tw, 3))
        word_race[g] = rows

    res = {"week0": WEEK0, "word_race": word_race, "n_weeks": N_WEEKS, "dates": dates, "first": first, "last": last, "pre_war": PRE_WAR, "first_post_war": FIRST_POST_WAR,
           "frames": FRAMES, "critical": CRITICAL, "connection": CONNECTION,
           "lexicon": {k: {"include": inc, "exclude": exc} for k, (inc, exc) in F.items()},
           "n_treatment": len(T), "n_control": len(C), "n_treatment_hand": len(T_hand),
           "n_control_quiet": len(C_quiet), "n_control_shocked": len(C_shock),
           "n_new_topic_articles": len(new_articles), "n_articles_total": len(arts),
           "total_revisions": sum(a["n_edits"] for a in arts),
           "trends": trends, "event_study": event_study, "did": did_rows, "robustness": robust,
           "validation": validation, "dynamics": dyn, "concentration": conc, "blind": None,
           "articles": table}
    os.makedirs(OUTDIR, exist_ok=True)
    for name, obj in (("results.json", res), ("leads.json", leads), ("kwic.json", kw)):
        with open(os.path.join(OUTDIR, name), "w") as f:
            json.dump(obj, f, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    prim = [r for r in did_rows if r["tier"] == "primary"]
    print(f"analyzed {len(T)} topic / {len(C)} comparison (primary panel), {len(arts)} total, "
          f"{res['total_revisions']} revisions")
    for r in prim:
        print(f"  {r['id']} {r['part']}:{r['frame']} DiD={r['did']:+.3f} [{r['lo']:+.3f},{r['hi']:+.3f}] p={r['p_perm']:.4f} q={r['q_bh']:.4f}")
    for v in validation:
        print(f"  validation {v['title']}: {v['observed']} pass={v['pass']}")


if __name__ == "__main__":
    main()
