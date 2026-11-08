"""Inline results.json + findings.html into the report page.

Usage: python build_page.py OUT.html
"""
import json, os, re, sys

HERE = os.path.dirname(__file__)
res = json.load(open(os.path.join(HERE, "data", "results.json")))

for a in res["articles"]:
    fs, out = a["first_sentences"], []
    for x in fs:
        if not out or out[-1]["s"] != x["s"]:
            out.append(x)
    a["first_sentences"] = out
    # keep diffs compact: drop long unchanged runs
    d = a["lead_diff"]
    a["lead_changed"] = sum(x["t"] != "=" for x in d)
    a["lead_truncated"] = len(d) > 60
    if len(d) > 60:
        a["lead_diff"] = [x for x in d if x["t"] != "="][:60]
    for k in ("top10", "crit0", "crit1", "conn0", "conn1", "lcrit0", "lcrit1"):
        if a.get(k) is not None:
            a[k] = round(a[k], 3)

for name, key in (("bisect.json", "trace"), ("crosslang.json", "crosslang"), ("ratchet.json", "ratchet")):
    p = os.path.join(HERE, "data", name)
    res[key] = json.load(open(p)) if os.path.exists(p) else None
if res.get("ratchet"):
    res["ratchet"].pop("events", None)
if res.get("crosslang"):
    for langs in res["crosslang"]["articles"].values():
        for v in langs.values():
            s = v["series"]
            v["series"] = [s[0], s[-1]] if len(s) > 1 else s
mp = os.path.join(HERE, "data", "mass_results.json")
if os.path.exists(mp) and "mass" not in res:
    res["mass"] = json.load(open(mp)).get("mass")
qa_p = os.path.join(HERE, "data", "qa.json")
if os.path.exists(qa_p):
    qa = json.load(open(qa_p)); qa.pop("per_article", None); res["qa"] = qa

# Reader exposure: monthly pageviews x which first-sentence variant was live (from the ratchet timeline)
def exposure(res):
    if not res.get("ratchet"):
        return None
    pv = {a["title"]: a.get("pv_monthly") for a in res["articles"] if a.get("pv_monthly")}
    out = {}
    for t, a in res["ratchet"]["articles"].items():
        if t not in pv or not a.get("fs_timeline"):
            continue
        tl = a["fs_timeline"]; var = {v["id"]: v["s"] for v in a["fs_variants"]}
        views = Counter()
        for ym, n in pv[t].items():              # 'YYYYMM'
            day = f"{ym[:4]}-{ym[4:6]}-15"
            live = None
            for d, vid, _ in tl:
                if d <= day:
                    live = vid
                else:
                    break
            if live is not None:
                views[live] += n
        tot = sum(views.values())
        out[t] = {"total_views": tot, "variants": [{"s": var.get(v, "")[:300], "views": n, "share": n / tot if tot else 0}
                                                   for v, n in views.most_common(6)]}
    return out


from collections import Counter
res["exposure"] = exposure(res)


# "Be the coder" playground: 40 real masked pairs (orientation a: A = older, B = newer) with the reveal
def play_pairs():
    bd = os.path.join(HERE, "data", "blind")
    kp, fp = os.path.join(bd, "key.json"), os.path.join(bd, "finals.json")
    if not (os.path.exists(kp) and os.path.exists(fp)):
        return None
    key = json.load(open(kp))["key"]; finals = json.load(open(fp))
    texts = {}
    for f in sorted(os.listdir(bd)):
        if f.startswith("shard_"):
            for it in json.load(open(os.path.join(bd, f))):
                texts[it["id"]] = it
    import random as _r
    rnd = _r.Random(4)
    cands = [b for b, v in finals.items() if v.get("rev0") and (b + "a") in texts]
    lab = lambda b: finals[b]["final"]
    pick = [b for b in cands if lab(b) in ("B_less_favourable", "B_more_favourable")]
    flat = [b for b in cands if lab(b) not in ("B_less_favourable", "B_more_favourable")]
    pick = rnd.sample(pick, min(28, len(pick))) + rnd.sample(flat, min(12, len(flat)))
    rnd.shuffle(pick)
    out = []
    for b in pick:
        t = texts[b + "a"]; swap = rnd.random() < 0.5
        out.append({"left": t["B"] if swap else t["A"], "right": t["A"] if swap else t["B"], "newer": "left" if swap else "right",
                    "ai": {"B_less_favourable": "newer_harsher", "B_more_favourable": "newer_gentler"}.get(lab(b), "no_clear_change"),
                    **{k: finals[b].get(k) for k in ("title", "group", "rev0", "rev1", "d0", "d1")}})
    return out


res["play_pairs"] = play_pairs()

# v3: full-scale weekly timeline with the event calendar, and the half-year insertion rate (mass2)
def v3_data():
    tp = os.path.join(HERE, "patterns", "events", "chart_data", "mass2_01_weekly_timeline_events.json")
    hp = os.path.join(HERE, "data", "event_timing_mass2.json")
    if not os.path.exists(tp):
        return None
    t = json.load(open(tp))
    out = {"week0": t["week_start"][0], "n": len(t["week_start"]),
           "topic_edits": t["topic_edits"], "comparison_edits": t["comparison_edits"],
           "ins": t["topic_term_insertions"],
           "events": [{"d": e["date"], "w": e["week_start"], "l": e["label"], "t": e["type"]} for e in t["events"]]}
    if os.path.exists(hp):
        hy = json.load(open(hp)).get("half_years") or {}
        out["half"] = [{"h": k, "rate": v["ins_per_1000_edits"], "ins": v["term_ins"], "edits": v["topic_edits"]} for k, v in sorted(hy.items())]
    return out


res["v3"] = v3_data()

# Generic first-sentence tracker (ratchet.json fs_variants / fs_timeline): every change, and when each key term went in or out.
# terms: {key: regex string or callable(text) -> bool}. A wording whose text was not kept (or is blank) carries no state, so a
# move is dated to the next kept wording. Used by zionism_data() and by the October 7 / Hamas / Gaza genocide tabs.
def fs_track(ra, terms):
    import re
    V = {v["id"]: v.get("s") for v in ra["fs_variants"]}
    tl = ra["fs_timeline"]
    test = {k: (f if callable(f) else (lambda s, p=f: bool(re.search(p, s, re.I)))) for k, f in terms.items()}
    def tags(s):
        if not s:
            return None
        return [k for k in terms if test[k](s)]
    state = [tags(V.get(i)) for _, i, _ in tl]
    changes, last, flips = [], None, {}
    for k, ((d, i, rv), st) in enumerate(zip(tl, state)):
        mv = []
        if st is not None:
            if last is not None:
                for term in set(last) | set(st):
                    if (term in st) != (term in last):
                        mv.append(term + ("+" if term in st else "-"))
                        flips.setdefault(term, []).append([d, "+" if term in st else "-"])
            last = st
        if k:
            changes.append([d, tl[k - 1][1], i, int(rv), sorted(mv)])
    def stat(term):
        f = flips.get(term, [])
        return {"in": sum(x[1] == "+" for x in f), "out": sum(x[1] == "-" for x in f),
                "first_in": next((x[0] for x in f if x[1] == "+"), None), "last": f[-1] if f else None,
                "start": term in (state[0] or []), "end": term in (last or [])}
    return {"changes": changes, "flips": flips, "end_state": last, "stats": {t: stat(t) for t in terms},
            "start": {t: t in (state[0] or []) for t in terms}, "blank": [d for d, i, _ in tl if V.get(i) == ""],
            "n_wordings": ra.get("fs_n_variants") or len(set(i for _, i, _ in tl)),
            "n_kept": sum(1 for s in V.values() if s), "n_undone": sum(int(x[2]) for x in tl), "first_ts": tl[0][0]}


# "Zionism up close": the opening paragraph in Jan 2021 and now, plus every first-sentence change (ratchet.json)
def zionism_data(title="Zionism"):
    import gzip, re, datetime as _dt
    lp, mp2 = os.path.join(HERE, "data", "leads.json"), os.path.join(HERE, "data", "mass2_leads.json.gz")
    rp = os.path.join(HERE, "data", "ratchet.json")
    if not (os.path.exists(lp) and os.path.exists(rp)):
        return None
    L = next((x for x in json.load(open(lp)) if x["title"] == title), None)
    RA = json.load(open(rp))
    ra = RA["articles"].get(title)
    if not L or not ra:
        return None
    paras = lambda s: [re.sub(r"[ \t]+", " ", p).strip() for p in re.split(r"\n\s*\n", s.strip()) if p.strip()]
    then = {"text": L["lead0"], "rev": L["rev0"], "asof": L["d0"] + "-01", "saved": None}
    now = {"text": L["lead1"], "rev": L["rev1"], "asof": L["d1"] + "-01", "saved": None}
    # mass2 has a newer "now" (and the exact revisions); use it when present
    if os.path.exists(mp2):
        m2 = json.load(gzip.open(mp2))
        ml = m2["leads"].get(title)
        if ml:
            then["text"] = ml[0] or then["text"]
            if ml[-1]:
                now["text"] = ml[-1]
                m2p = os.path.join(HERE, "data", "mass2.json.gz")
                if os.path.exists(m2p):
                    M = json.load(gzip.open(m2p))
                    arts = M["articles"]
                    a = arts.get(title) if isinstance(arts, dict) else next((x for x in arts if x.get("title") == title), None)
                    if a:
                        r0, r1 = a["at"]["2021-01-01"]["rev"], a["at"]["now"]["rev"]
                        then.update(rev=r0["revid"], saved=r0["ts"][:10])
                        now.update(rev=r1["revid"], saved=r1["ts"][:10], asof=M["now"][:10])
    then["paras"], now["paras"] = paras(then.pop("text")), paras(now.pop("text"))
    # term lexicon from analyze.py (no heavy imports)
    src = open(os.path.join(HERE, "analyze.py")).read()
    ns = {}
    exec("import re\n" + src[src.index("F = {"):src.index("CRITICAL =")], ns)
    F = ns["F"]
    crit = ["settler_colonial", "apartheid", "genocide", "ethnic_cleansing", "occupation", "nakba_expulsion", "war_crimes"]
    def has(k, s):
        inc, exc = F[k]
        return sum(len(re.findall(p, s, re.I)) for p in inc) - sum(len(re.findall(p, s, re.I)) for p in exc) > 0
    terms = {k: (lambda s, k=k: has(k, s)) for k in crit}
    terms["re_establish"] = lambda s: bool(re.search(r"\bre-?establish", s, re.I))
    T = fs_track(ra, terms)
    changes, flips, last = T["changes"], T["flips"], T["end_state"]
    tl = ra["fs_timeline"]
    blank = T["blank"]
    def stat(term):
        return T["stats"][term]
    # critical terms in the rest of the opening section: exact timestamps (ratchet events; mass2_events agree)
    lead_terms = []
    for term, evs in (RA.get("events") or {}).get(title, {}).items():
        if term in crit:
            lead_terms += [[_dt.datetime.fromtimestamp(e["t"], _dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), term, e["kind"]] for e in evs]
    lead_terms.sort()
    # summary chips: exact words from the paragraph-1 diff, kept only if each quote checks out against the stored text
    t1, n1 = then["paras"][0], now["paras"][0]
    tall, nall = " ".join(then["paras"]), " ".join(now["paras"])
    want = [("-", "re-establishment", None, "p1"), ("+", "colonization", None, "p1"), ("+", "ethnic", "an ethnic nationalist movement", "p1"),
            ("-", "among the Jewish people", None, "p1"), ("~", "a Jewish state in the territory", "a Jewish homeland through colonization", "p1"),
            ("+", "as few Palestinian Arabs as possible", None, "p1"), ("-", "Canaan, the Holy Land", None, "p1"),
            ("~", "a persecuted people", "an indigenous people", "rest"), ("+", "a settler colonialist movement", None, "rest"),
            ("-", "exceptionalist", None, "rest")]
    low = str.lower
    chips = []
    for kind, a, b, where in want:
        A, B = (t1, n1) if where == "p1" else (tall, nall)
        ok = (kind == "-" and a in A and low(a) not in low(nall)) or (kind == "+" and a in B and low(a) not in low(tall)) or \
             (kind == "~" and a in A and b in B and low(a) not in low(nall) and low(b) not in low(tall))
        if ok:
            chips.append({"k": kind, "a": a, "b": b, "where": where})
    return {"title": title, "then": then, "now": now, "chips": chips, "changes": changes, "lead_terms": lead_terms,
            "n_wordings": T["n_wordings"], "n_kept": T["n_kept"], "n_undone": T["n_undone"], "blank": blank,
            "first_ts": tl[0][0], "col": stat("settler_colonial"), "re": stat("re_establish"),
            "other_terms": sorted(t for t in flips if t not in ("settler_colonial", "re_establish"))}


res["zionism"] = zionism_data()


# --- Design council round 2 -------------------------------------------------------------------------------------------
PAT = os.path.join(HERE, "patterns")
def _j(*parts):
    p = os.path.join(PAT, *parts)
    return json.load(open(p)) if os.path.exists(p) else None


# October 7, Hamas and Gaza genocide: the Zionism step-through, one tab per article (fs_track on ratchet.json)
def oct7_data():
    rp = os.path.join(HERE, "data", "ratchet.json")
    if not os.path.exists(rp):
        return None
    RA = json.load(open(rp))["articles"]
    gv = _j("angle", "chart_data", "oct7_05_genocide_voice.json") or {}
    lvl = {}
    for x in gv.get("gaza_genocide_first_sentence", []):
        lvl.setdefault(x["variant"], x["voice_level"])
    HOST = r"\bhostages?\b|\bcaptives?\b|\babduct\w*|\bkidnap\w*"          # oct7_04 regex
    cfg = {
        "Hamas": {"militant": r"\bmilitan", "polmil": r"\bwith an? (?:\w+ )?(?:military|militant|paramilitary|armed) wing",
                  "political": r"\bpolitical\b", "terrorist": r"\bterror", "hostage": HOST},
        "October 7 attacks": {"incursions": r"\bincursions?\b", "hamas": r"\bHamas\b", "massacre": r"massacr",
                              "blockaded": r"\bblockaded\b", "hostage": HOST},
        "Gaza genocide": {"own": lambda s, v=None: False, "attrib": lambda s, v=None: False, "hostage": HOST},
    }
    out = []
    for title, terms in cfg.items():
        ra = RA.get(title)
        if not ra:
            continue
        if title == "Gaza genocide":
            # voice from the analyst's ladder (oct7_05): 4 = Wikipedia's own voice; 0-2 = alleged / accused / according to.
            byText = {v.get("s"): lvl.get(v["id"]) for v in ra["fs_variants"]}
            terms = {"own": lambda s: byText.get(s) == 4, "attrib": lambda s: byText.get(s) in (0, 1, 2), "hostage": HOST}
        T = fs_track(ra, terms)
        T.pop("flips"); T.pop("end_state")
        T["title"] = title
        T["live"] = {v["id"]: [round(v.get("live_days") or 0, 4), (v.get("first_seen") or "")[:16]] for v in ra["fs_variants"]}
        if title == "Gaza genocide":
            T["attempts"] = [[a["date"], a["variant"]] for a in gv.get("attribution_attempts_after_2025-09-26", [])]
        if title == "October 7 attacks":
            tm = _j("angle", "chart_data", "oct7_03_oct7_first_sentence_and_title.json") or {}
            T["titles"] = [[m["ts"], m["from"], m["to"]] for m in tm.get("title_moves", []) if not m.get("reverted") and not m.get("revert_of_move")]
        out.append(T)
    pos = _j("angle", "chart_data", "oct7_08_hamas_designation_position.json") or {}
    grp = _j("angle", "chart_data", "oct7_02_designated_groups.json") or {}
    groups = [{"a": g["article"], "t0": g["then"].get("terror_word_offset_share"), "t1": g["now"].get("terror_word_offset_share"),
               "m1": g["now"].get("fs_has_militant"), "fs0": g["then"].get("first_sentence", "")[:400], "fs1": g["now"].get("first_sentence", "")[:400],
               "d0": g["then"].get("date"), "d1": (g["now"].get("date") or "")[:10]} for g in grp.get("groups", [])]
    return {"tabs": out, "designation": pos.get("position_of_first_terror_mention"), "groups": groups}


res["oct7"] = oct7_data()


# Who is charged with what, in whose voice: patterns/angle/perp_codes.jsonl (counts reproduce perp_results.json exactly)
def perp_data():
    pc = os.path.join(PAT, "angle", "perp_codes.jsonl")
    if not os.path.exists(pc):
        return None
    rows = [json.loads(l) for l in open(pc)]
    sides = {"isr": ("topic", {"I", "J"}), "pal": ("topic", {"H", "P", "H+O"}), "cmp": ("comparison", {"A"})}
    charges = [("G", "Genocide"), ("AP", "Apartheid"), ("EC", "Ethnic cleansing / expulsion"), ("OC", "Occupation"),
               ("M", "Massacre / killing"), ("WC", "War crimes"), ("T", "Terrorism")]
    dates = ["2021-01-01", "2023-07-01", "now"]
    cells, receipts = {}, {}
    for sd, (grp, codes) in sides.items():
        for code, _ in charges:
            for d in dates:
                key = f"{sd}|{code}|{d}"
                rec = []
                for r in rows:
                    if r["group"] != grp or r["date"] != d:
                        continue
                    hit = next((ch["voice"] for c in r["clauses"] if c["perp_code"] in codes for ch in c["charges"] if ch["code"] == code), None)
                    if hit is not None:
                        rec.append([r["title"], r["text"], {"wikipedia_voice": "own", "attributed": "att", "denied_or_disputed": "den"}[hit], r.get("views") or 0])
                rec.sort(key=lambda x: (x[2] != "own", -x[3]))
                cells[key] = [len(rec), sum(x[2] == "own" for x in rec)]
                if rec:
                    receipts[key] = [x[:3] for x in rec]
    PR = json.load(open(os.path.join(PAT, "angle", "perp_results.json")))
    return {"charges": charges, "dates": dates, "cells": cells, "receipts": receipts,
            "n": PR["n_articles"], "snapshot": "2026-11-05"}


res["perp"] = perp_data()


# Coordination network (analyze_coord.py -> patterns/coord/chart_data/network.json). Inlined when present; WT_NETWORK overrides
# the path (used to test the component on a synthetic file). Slimmed: no per-community profiles or raw alignment tables.
def network_data():
    p = os.environ.get("WT_NETWORK") or os.path.join(PAT, "coord", "chart_data", "network.json")
    if not os.path.exists(p):
        return None
    N = json.load(open(p))
    keep_c = ("id", "size", "density", "strength", "n_articles", "articles", "direction", "active", "inserted_phrases", "confidence",
              "significance", "window_share", "expected_window_share", "post_sanction_drop", "members", "weekly")
    keep_e = ("source", "target", "weight", "basis", "observed", "null_mean", "null_p95", "p", "same_direction_share",
              "example_article_pairs", "time_span", "shared_articles")
    out = {"generated": N.get("generated"), "method": N.get("method")}
    for g in ("topic", "comparison"):
        G = N.get(g)
        if not G:
            out[g] = None
            continue
        cs = []
        for c in G.get("communities", []):
            c = {k: c[k] for k in keep_c if k in c}
            if c.get("significance"):
                c["significance"] = {"share": c["significance"].get("null_worlds_with_community_this_large_dense_and_strong"),
                                     "worlds": c["significance"].get("null_worlds")}
            cs.append(c)
        out[g] = {"nodes": G.get("nodes", []), "edges": [{k: e[k] for k in keep_e if k in e} for e in G.get("edges", [])],
                  "communities": cs, "counts": G.get("counts", {})}
    # Bloc names from the bloc test (blocs.json, "Bloc A", "Bloc B"): name the matching network community, and add the
    # blocs found only in the direction-specific tests (insertions only / removals only) as extra group cards.
    bp = os.path.join(os.path.dirname(p), "blocs.json")
    if os.path.exists(bp) and not os.environ.get("WT_NETWORK"):
        B = json.load(open(bp))
        sig_key = lambda b: (b.get("size"), b.get("n_articles"), (b.get("active") or {}).get("first"))
        for g in ("topic", "comparison"):
            if not out.get(g):
                continue
            named = {}
            for b in (B.get(f"{g}/any") or {}).get("blocs", []):
                if b.get("name"):
                    named[sig_key(b)] = b["name"]
            for c in out[g]["communities"]:
                if sig_key(c) in named:
                    c["name"] = named[sig_key(c)]
            extra = []
            for d in ("insert", "remove"):
                for b in (B.get(f"{g}/{d}") or {}).get("blocs", []):
                    if b.get("confidence") in (None, "low") or sig_key(b) in named:
                        continue
                    ta = (b.get("time_alignment") or {})
                    ws = {k: v.get("window_share") for k, v in (ta.get("windows") or {}).items()}
                    es = {k: {"mean": v.get("expected_window_share"), "ci95": v.get("expected_ci95"), "p_high": v.get("p_high")}
                          for k, v in (ta.get("windows") or {}).items()}
                    psd = {k: {"ratio": v.get("post_sanction_drop"), "ci95": v.get("ci95"), "p_drop": v.get("p_drop"), "testable": v.get("testable")}
                           for k, v in (ta.get("post_sanction") or {}).items()}
                    extra.append({"id": f"{d[0]}{len(extra)}", "name": b.get("name"), "test": d, "size": b["size"], "density": b.get("density"),
                                  "n_articles": b["n_articles"], "articles": b.get("articles", [])[:10], "direction": b.get("direction"),
                                  "active": b.get("active"), "inserted_phrases": b.get("inserted_phrases", []), "confidence": b.get("confidence"),
                                  "significance": {"share": b.get("null_worlds_with_bloc_this_large_dense_and_strong"),
                                                   "worlds": ((B[f"{g}/{d}"].get("expected_by_chance") or {}).get("null_worlds"))},
                                  "window_share": ws, "expected_window_share": es, "post_sanction_drop": psd,
                                  "median_gap_h": (b.get("synchrony") or {}).get("median_same_article_gap_h")})
            out[g]["extra_blocs"] = extra
    return out


res["network"] = network_data()

# Sampling audit: unweighted vs design-weighted vs matched (patterns/sampling/chart_data/03_weighted_vs_unweighted.json)
_a = _j("sampling", "chart_data", "03_weighted_vs_unweighted.json")
res["audit"] = {"rows": [{k: r.get(k) for k in ("subset", "statistic", "label", "unweighted", "design_weighted", "cem", "ps_nn",
                                                 "topic_weighted_only")} for r in _a["rows"] if r.get("subset") == "all"]} if _a else None

# Mass v3: design-weighted estimates for the full populations (patterns/sampling/chart_data/08_mass3_estimates.json)
def mass3_data():
    m = _j("sampling", "chart_data", "08_mass3_estimates.json")
    if not m:
        return None
    keys = ("a_unf", "a_res", "b_t", "b_c", "b", "d_t", "d_c", "d", "e", "e_ip", "e_ju", "e_ju_vs_c", "gainers_t_total")
    pick = lambda blk: {k: {"est": blk["weighted"][k], "lo": (blk.get("ci", {}).get(k) or [None, None])[0],
                            "hi": (blk.get("ci", {}).get(k) or [None, None])[1]} for k in keys if blk["weighted"].get(k) is not None}
    tiers = {}
    for lv, blk in m["by_importance"].items():
        t = pick(blk)
        t.update({k: blk["weighted"][k] for k in ("N_t", "N_c", "n_t", "n_c")})
        tiers[lv] = t
    o = pick(m["overall"])
    o.update({k: m["overall"]["weighted"][k] for k in ("N_t", "N_c", "n_t", "n_c")})
    return {"overall": o, "tiers": tiers, "random": m.get("random")}


res["mass3"] = mass3_data()

# ---------- cross-language reader + matrix (#crosslang): exact quotes from patterns/langs/langs.json ----------
def langs_data():
    import re, difflib
    lp = os.path.join(HERE, "patterns", "langs", "langs.json")
    if not os.path.exists(lp):
        return None
    L = json.load(open(lp))
    ARTS = L["articles"]
    ORDER = L["meta"]["lang_order"]

    def ver(a, l, s, w):
        X = ARTS.get(a, {}).get(l) or {}
        S = (X.get("slots") or {}).get(s) or {}
        return S.get(w)

    # matrix: column -> article / evidence; manual codings carry a note and the slot that shows the evidence
    COLS = [("gen", "Genocide", ["Gaza genocide", "Gaza war"]), ("col", "Zionism as colonization", ["Zionism"]),
            ("apa", "Apartheid", ["Israeli apartheid"]), ("occ", "Occupation (West Bank)", ["West Bank"]),
            ("o7", "7 October called terror or massacre", ["October 7 attacks"]), ("ter", "Hamas called terrorist", ["Hamas"]),
            ("hos", "The hostages", ["October 7 attacks"]), ("icj", "Court ruling overstated", ["Gaza genocide", "Israeli apartheid", "Gaza war"])]
    O7 = {"he": ("fact", "fact", "s1", "Title and first sentence: “massacre”, carried out by “the Palestinian terror organisations”."),
          "ar": ("none", "none", "s1", "“an extended military operation” by “the Palestinian resistance factions”; now aimed “against the Israeli occupation”."),
          "en": ("none", "none", "s1", "“a series of coordinated armed incursions” by “Palestinian militant groups”. A later sentence says “massacring civilians”."),
          "de": ("fact", "fact", "s1", "“The Hamas terror attack”; now also “the largest massacre and crime against humanity against Jews since the Holocaust”."),
          "fr": ("fact", "fact", "s1", "“a series of coordinated terrorist attacks”; now “a series of Palestinian terrorist attacks”."),
          "es": ("none", "none", "s1", "“the name used by the Palestinian Islamist militant group Hamas”; now “a series of coordinated attacks”. A later sentence says the militiamen “massacred civilians”."),
          "it": ("fact", "fact", "s1", "“terrorist attacks and massacres of civilians”; now “a series of terrorist attacks by armed groups”."),
          "pt": ("none", "none", "s1", "“A series of coordinated attacks”; now “coordinated attacks [atentados]”, a sharper noun."),
          "nl": ("none", "fact", "s1", "“a coordinated surprise attack by the militant movement Hamas”; now “surprise attack or terror attack”."),
          "ru": ("none", "none", "s1", "“The invasion of Israel”. A later sentence calls it “the largest act of Palestinian terrorism in history”.")}
    HOS = {"he": ("fact", "fact", ("October 7 attacks", "k_hostages"), "“the abduction of 251 civilians and soldiers – among them elderly people, women, children and babies”."),
           "ar": ("absent", "captive", ("October 7 attacks", "k_hostages"), "Now: “they captured a number of soldiers and civilians”. A prisoner-of-war word, not the Arabic word for hostages."),
           "en": ("outside", "outside", ("Gaza war", "k_hostages"), "In the attack article’s opening section, beyond the 1,200 characters we hold: sentence 9 of 16 now reads “251 Israeli and non-Israeli civilians and soldiers were taken as hostages to the Gaza Strip” (sentence 7 of 11 in January 2024). The Gaza war article says “251 were taken hostage”."),
           "de": ("absent", "absent", ("Gaza war", "k_hostages"), "Not in the text we hold of the attack article. The Gaza war article names “freeing the hostages” as Israel’s aim."),
           "fr": ("absent", "absent", ("October 7 attacks", "s1"), "Not in the 1,200 characters we hold, at either date, of the attack article or of the Gaza war article."),
           "es": ("fact", "absent", ("October 7 attacks", "k_hostages"), "2024: “Israeli soldiers and civilians, including women and children, were taken as hostages”. Not in the 2026 text we hold; it may appear later in the opening section, beyond the text we hold."),
           "it": ("fact", "fact", ("October 7 attacks", "s1"), "Now in the first sentence: “the kidnapping of about 250 of them”. In 2024 a later sentence in the text we hold (not in our translated set)."),
           "pt": ("fact", "absent", ("October 7 attacks", "s1"), "2024: hostages named later in the text we hold (that sentence is not in our translated set). Not in the 2026 text we hold; it may appear later in the opening section, beyond the text we hold."),
           "nl": ("fact", "fact", ("October 7 attacks", "k_hostages"), "“An estimated 250–255 people were taken prisoner and transferred to Gaza as hostages”. The 2024 copy says the same with 200–250."),
           "ru": ("fact", "fact", ("October 7 attacks", "k_hostages"), "“another 251 were taken hostage” (2024: 242).")}
    ICJ = {"ar": ("fact", "fact", ("Gaza genocide", "k_icj"), "The ICJ “found that Israel was acting under a reasonable [or: plausible] intent to commit acts of genocide”. The January 2024 order made no finding on intent."),
           "it": ("legal", "fact", ("Gaza genocide", "k_icj"), "2025: the court asked Israel to «prevent possible genocidal acts». 2026: the court “deemed Israel's actions in Gaza «plausibly genocidal»”, a phrase the court did not use."),
           "ru": ("absent", "fact", ("Israeli apartheid", "k_icj"), "The ICJ “found Israel guilty”: verdict wording for a non-binding advisory opinion."),
           "fr": ("absent", "fact", ("Israeli apartheid", "k_icj"), "“The Court recognises that Israel” is “conducting a policy of apartheid”. The 2024 opinion found a breach of CERD Article 3 without saying whether it was segregation or apartheid."),
           "es": ("absent", "legal", ("Israeli apartheid", "k_icj"), "Reports the 2024 opinion under article 3. Not one of the four overstatements we found."),
           "he": ("absent", "legal", ("Gaza war", "k_genocide"), "“South Africa filed a suit against Israel at the International Court of Justice (ICJ) for genocide”: the case, reported as a case."),
           "pl": ("absent", "disputed", ("Gaza genocide", "k_courts"), "Stresses that only courts can rule on genocide.")}
    NOTE = {("ter", "en"): "Beyond the 1,200 characters we hold. The designation now sits at the end of the opening section, attributed (see the Hamas timeline above).",
            ("ter", "ar"): "No terror word in the text we hold; Hamas is “a Palestinian, resistance, popular, Islamic, national movement”.",
            ("gen", "he"): "No article linked to English Gaza genocide, so this square reads the Gaza war article: the court-case clause is its only genocide mention. The Hebrew October 7 article has one more genocide mention, beyond the text we hold.",
            ("gen", "de"): "No article linked to English Gaza genocide. The Gaza war article has 3 genocide mentions, all beyond the text we hold.",
            ("gen", "ru"): "No article linked to English Gaza genocide. The Gaza war article mentions genocide only beyond the text we hold.",
            ("occ", "he"): "“belligerent occupation”, the Israeli legal term, and now “a territory in the Land of Israel”.",
            ("apa", "ar"): "“an accusation directed against” Israeli policy became “a confirmed fact in” it."}

    cells, need = {}, set()
    for k, lab, arts in COLS:
        for l in ORDER:
            c = None
            if k in ("o7", "hos", "icj"):
                src = {"o7": O7, "hos": HOS, "icj": ICJ}[k]
                if k != "icj" and not ARTS["October 7 attacks"].get(l, {}).get("slots"):
                    c = {"f": "na", "n": "na", "a": "October 7 attacks", "s": None, "x": "No article in this language is linked to the English article on the October 7 attacks."}
                elif l in src:
                    f, n, tgt, note = src[l]
                    a, s = (arts[0], tgt) if isinstance(tgt, str) else tgt
                    c = {"f": f, "n": n, "a": a, "s": s, "x": note}
                elif k == "icj":
                    a = "Gaza genocide" if ARTS["Gaza genocide"].get(l, {}).get("slots") else "Gaza war"
                    c = {"f": "none", "n": "none", "a": a, "s": "s1", "x": "None of the four overstatements we found (Arabic, Italian, Russian, French)."}
            else:
                for a in arts:
                    X = ARTS[a].get(l) or {}
                    hc = X.get("headline_claim")
                    if hc and X.get("slots"):
                        c = {"f": hc.get("first") or "na", "n": hc.get("latest") or "na", "a": a, "s": hc.get("evidence_slot"), "x": NOTE.get((k, l))}
                        break
                if c is None:
                    X = ARTS[arts[0]].get(l) or {}
                    c = {"f": "na", "n": "na", "a": arts[0], "s": None,
                         "x": "No article in this language." if not X.get("slots") else "Not coded: no sentence held for this claim."}
            if c["s"] and not ((ARTS[c["a"]].get(l) or {}).get("slots") or {}).get(c["s"]):
                raise SystemExit(f"langs: matrix cell {k}/{l} points at missing slot {c['a']}/{c['s']}")
            if c["s"]:
                need.add((c["a"], l, c["s"]))
            cells.setdefault(k, {})[l] = c

    MOM = [("Gaza genocide", "ar", "s1", "Arabic: from accusation to definition", "In 2024 the Arabic article said Israel “has been accused of committing crimes of genocide”. Now it opens: “The genocide of Gaza is the systematic, deliberate and ongoing destruction”."),
           ("Gaza war", "he", "k_genocide", "Hebrew: genocide only as a court case", "Hebrew has no article linked to English Gaza genocide. Its Gaza-war article mentions genocide once, as South Africa’s suit at the ICJ."),
           ("Gaza war", "es", "s1", "Spanish: “a genocide in Gaza by Israel”", "The first sentence of the Spanish Gaza-war article now says the war “has unleashed a genocide in Gaza by Israel”, and calls 7 October “a retaliatory attack”."),
           ("Gaza genocide", "es", "s1", "Spanish: the same move in the genocide article", "From “have accused Israel of carrying out a «genocide against the Palestinian people»” to “The Palestinian genocide in Gaza is the systematic and continuing destruction”."),
           ("Gaza genocide", "pt", "s1", "Portuguese: from “accused” to “is”", "From “has been accused of genocide” to “is the intentional and systematic destruction, ongoing”."),
           ("Gaza genocide", "nl", "s1", "Dutch moved the other way", "From “Israel is committing genocide”, attributed to organisations and experts, to a genocide “that Israel may or may not have committed”."),
           ("Zionism", "ar", "s1", "Arabic: Zionism “by colonizing a land outside Europe”", "Colonialism moved from the critics’ sentence into the definition, with “the war of ethnic cleansing of Palestine” and “a Jewish ethnocracy” in the same sentence."),
           ("Zionism", "he", "s1", "Hebrew: the Balfour wording", "Hebrew kept colonization out and moved the other way: “a Jewish state” became “a national home for the Jewish people”."),
           ("Zionism", "nl", "k_colonial", "Dutch: colonisation in place of Zionism", "Herzl “gave the impetus to organised Zionism” became “gave the impetus to the organised colonisation of Palestine”."),
           ("Israeli apartheid", "ar", "s1", "Arabic: “an accusation” became “a confirmed fact”", "Apartheid is no longer “an accusation directed against Israeli policy” but “a confirmed fact in Israeli policy”."),
           ("Israeli apartheid", "he", "k_dispute", "Hebrew: the claims are “in dispute”", "Hebrew keeps apartheid attributed: “The degree of correctness of these claims is in dispute among scholars, jurists and statesmen.”"),
           ("Israeli apartheid", "pt", "s1", "Portuguese: apartheid “and in Israel”", "Portuguese states apartheid as fact and extends it from “the Palestinian territories occupied by Israel” to Israel itself."),
           ("October 7 attacks", "he", "s1", "Hebrew: from “surprise attack” to “massacre”", "Hebrew retitled the article: “The surprise attack on Israel” is now “The Seventh of October massacre”."),
           ("October 7 attacks", "de", "s1", "German: “since the Holocaust”", "German says in its own voice that it was “the largest massacre and crime against humanity against Jews since the Holocaust”."),
           ("October 7 attacks", "es", "k_genocide", "Spanish: the attack as the start of a genocide", "From “marked the start of the 2023 war between Israel and Hamas” to “marked the start of the Gaza war and of the Palestinian genocide in Gaza”."),
           ("October 7 attacks", "ar", "s1", "Arabic: aimed “against the Israeli occupation”", "The operation of “the Palestinian resistance factions” is now aimed “against the Israeli occupation”."),
           ("Hamas", "he", "s1", "Hebrew: “terror organisation”, in its own voice", "Terror stays first: Hamas “is a Palestinian Sunni-Islamist terror organisation that also operates as a political movement”."),
           ("Hamas", "ar", "s1", "Arabic: “resistance”", "Arabic calls Hamas “a Palestinian, resistance, popular, Islamic, national movement”. The text we hold has no terror word."),
           ("Hamas", "ru", "s1", "Russian: “terrorist” enters the definition", "The only edition where “terrorist” entered the definition in its own voice: “a Palestinian Islamist Sunni terrorist political and military resistance organisation”."),
           ("Hamas", "de", "s1", "German: from its own voice to “41 states”", "From “a Sunni-Islamist Palestinian terrorist organisation” to an organisation “classified internationally by 41 states as a terrorist association”."),
           ("Gaza genocide", "ar", "k_icj", "Arabic: a finding the court did not make", "The Arabic article says the ICJ “found that Israel was acting under a reasonable [or: plausible] intent to commit acts of genocide”. The order found only that some of South Africa’s claimed rights were plausible."),
           ("Israeli apartheid", "ru", "k_icj", "Russian: “found Israel guilty”", "Verdict wording for a non-binding advisory opinion."),
           ("West Bank", "fr", "s1", "French: “illegally occupied by Israel since 1967”", "French now puts the illegal occupation in the first sentence, as fact."),
           ("West Bank", "he", "s1", "Hebrew: “a territory in the Land of Israel”", "Hebrew keeps “belligerent occupation” and now calls the area “a territory in the Land of Israel”. English now places the same land in Palestine."),
           ("Nakba", "pl", "s1", "Polish: “carried out by Israelis”", "Polish states 1948 as ethnic cleansing and names “Israelis” as the perpetrators: “the ethnic cleansings carried out by Israelis on Palestinian Arabs”."),
           ("Nakba", "he", "k_ec", "Hebrew: one school’s view", "Hebrew gives ethnic cleansing as the view of “Palestinian historiography and scholars of the critical approach”, and labels the Israeli view “the Zionist-establishment narrative”.")]

    # every “…” inside our notes and captions must be our exact translation of that article × language
    def tr_pool(a, l):
        X = ARTS.get(a, {}).get(l) or {}
        return " ".join(v["tr"] for S in (X.get("slots") or {}).values() for v in (S.get("first"), S.get("latest")) if v)
    # English text beyond the 1,200 characters held is checked against the dated October 7 study (patterns/angle/OCT7.md)
    _o7p = os.path.join(HERE, "patterns", "angle", "OCT7.md")
    EXT = open(_o7p).read() if os.path.exists(_o7p) else ""
    def check_quotes(text, pools, where):
        for q in re.findall(r"“([^”]+)”", text or ""):
            for piece in q.rstrip(".").split(" … "):
                if not any(piece in p for p in pools) and not (where.endswith("/en") and EXT and f'"{piece}' in EXT):
                    raise SystemExit(f"langs: quote not in our translations ({where}): {piece!r}")
    for k, row in cells.items():
        for l, c in row.items():
            pools = [tr_pool(a, l) for a in ARTS]
            check_quotes(c.get("x"), pools, f"{k}/{l}")
    moms = []
    for a, l, s, h, cap in MOM:
        if not ((ARTS[a].get(l) or {}).get("slots") or {}).get(s):
            raise SystemExit(f"langs: moment slot missing {a}/{l}/{s}")
        check_quotes(h + " " + cap, [tr_pool(a, l)], f"moment {a}/{l}/{s}")
        need.add((a, l, s)); moms.append([a, l, s, h, cap])

    # key emphasis words: one fixed gloss per word, so a non-reader sees the charge in any sentence (our glosses)
    KEY = {"he": [("רצח עם", "genocide (lit. people-murder)", "gen"), ("טיהור אתני", "ethnic cleansing", "ec"), ("אפרטהייד", "apartheid", "apa"),
                  ("תפיסה לוחמתית", "belligerent occupation", "occ"), ("כיבוש", "occupation", "occ"), ("ארגון טרור", "terror organisation", "ter"),
                  ("ארגוני הטרור", "the terror organisations", "ter"), ("ארגוני טרור", "terror organisations", "ter"), ("טבח", "massacre", "ter"), ("חטיפת", "abduction", "hos")],
           "ar": [("الإبادة الجماعية", "the genocide", "gen"), ("إبادة جماعية", "genocide", "gen"), ("التطهير العرقي", "ethnic cleansing", "ec"),
                  ("الفصل العنصري", "apartheid (lit. racial separation)", "apa"), ("استعمار", "colonial / colonization", "col"), ("الاحتلال", "the occupation", "occ"),
                  ("احتلال", "occupation", "occ"), ("المقاومة", "the resistance", "res"), ("مقاومة", "resistance", "res"), ("إرهابية", "terrorist", "ter"),
                  ("مجزرة", "massacre", "ter"), ("أسروا", "took captive", "hos"), ("أسَرُوا", "took captive", "hos")],
           "ru": [("геноцид", "genocide", "gen"), ("апартеид", "apartheid", "apa"), ("террористическая", "terrorist", "ter"), ("терроризма", "terrorism", "ter"),
                  ("заложник", "hostage(s)", "hos"), ("сопротивления", "resistance", "res"), ("оккупац", "occupation", "occ")]}
    def cat(g):
        g = g.lower()
        for c, p in (("gen", r"genocid|exterminat"), ("ec", r"ethnic cleansing"), ("col", r"coloni"), ("apa", r"apartheid|racial separation|segregation"),
                     ("occ", r"occup"), ("hos", r"hostage|abduct|captiv|took captive|captur|kidnap"), ("ter", r"terror|massacre|slaughter"),
                     ("res", r"resist")):
            if re.search(p, g):
                return c
        return "oth"
    # an organisation's own name is not the encyclopedia's framing: "Islamic Resistance Movement" (the source of the
    # acronym Hamas) gets no gloss or underline; the chip stays on the descriptor ("a Palestinian, resistance, ... movement")
    NAMES = {"ar": (["حركة المقاومة الإسلامية"], ["Islamic Resistance Movement"])}
    def name_spans(s, names):
        return [(m.start(), m.end()) for nm in names for m in re.finditer(re.escape(nm), s, flags=re.I)]
    def find_tr(tr, gloss, skip=()):
        cands = [gloss, re.sub(r"\s*\(.*?\)", "", gloss), gloss.strip("'\"“”")]
        cands += [re.sub(r"^(the|a|an) ", "", c, flags=re.I) for c in list(cands)]
        cands += [x for c in list(cands) if " / " in c for x in c.split(" / ")]
        for c in cands:
            c = c.strip().strip("'\"“”").strip()
            if len(c) < 3:
                continue
            for mm in re.finditer(re.escape(c), tr, flags=re.I):
                i = mm.start()
                if not any(a <= i < b for a, b in skip):
                    return [i, i + len(c)]
        return None
    def toks(s, spans, flag):
        cuts = sorted({0, len(s)} | {p for sp in spans for p in (sp["start"], sp["end"])})
        out = []
        for x, y in zip(cuts, cuts[1:]):
            ch = any(sp["start"] <= x and y <= sp["end"] for sp in spans)
            for m in re.finditer(r"\S+\s*|\s+", s[x:y]):
                out.append([flag if ch else 0, m.group()])
        return out
    def merge(a, b, rem, add):
        A, B = toks(a, rem, 1), toks(b, add, 2)
        ka = [i for i, t in enumerate(A) if t[0] == 0]; kb = [j for j, t in enumerate(B) if t[0] == 0]
        nz = lambda t: re.sub(r"[\W_]+", "", t).lower() or t.strip()
        sm = difflib.SequenceMatcher(None, [nz(A[i][1]) for i in ka], [nz(B[j][1]) for j in kb], autojunk=False)
        pairs = [(ka[m.a + q], kb[m.b + q]) for m in sm.get_matching_blocks() for q in range(m.size)]
        out, ia, ib, odd = [], 0, 0, 0
        for pa, pb in pairs + [(len(A), len(B))]:
            # unmarked text that only one version has (spacing, punctuation, a reordered word) swaps without a mark:
            # kinds 4 / 5, so the page never marks a word the checked diff did not mark
            for t in A[ia:pa]:
                odd += t[0] == 0 and bool(nz(t[1]).strip()) and bool(re.search(r"\w", t[1])); out.append([1 if t[0] else 4, t[1]])
            for t in B[ib:pb]:
                odd += t[0] == 0 and bool(re.search(r"\w", t[1])); out.append([2 if t[0] else 5, t[1]])
            if pa < len(A):
                out.append([0, A[pa][1]] if A[pa][1] == B[pb][1] else [3, A[pa][1], B[pb][1]])
            ia, ib = pa + 1, pb + 1
        assert "".join(t[1] for t in out if t[0] in (0, 1, 3, 4)) == a
        assert "".join((t[2] if t[0] == 3 else t[1]) for t in out if t[0] in (0, 2, 3, 5)) == b
        return out, odd
    for X in (v for AA in ARTS.values() for v in AA.values()):
        for S in (X.get("slots") or {}).values():
            for v in (S.get("first"), S.get("latest")):
                if v:
                    assert all(ord(ch) < 0x10000 for ch in v["orig"] + v["tr"]), "non-BMP character: JS offsets would shift"

    out, odd_total = {}, 0
    for a, AA in ARTS.items():
        for l, X in AA.items():
            if not X.get("slots"):
                continue
            hc = X.get("headline_claim") or {}
            keep = {"s1", hc.get("evidence_slot")} | {s for (aa, ll, s) in need if aa == a and ll == l}
            kc = (X.get("key_changes") or [])[:3]
            sl = {}
            for s, S in X["slots"].items():
                if s not in keep:
                    continue
                f, n, d = S.get("first"), S.get("latest"), S.get("diff") or {}
                rec = {}
                for side in ("o", "t"):
                    key = "orig" if side == "o" else "tr"
                    if f and n:
                        dd = d.get(key) or {}
                        m, odd = merge(f[key], n[key], dd.get("removed", []), dd.get("added", []))
                        odd_total += odd
                    else:
                        m = [[0, t[1]] for t in toks((f or n)[key], [], 0)]
                    rec[side] = m
                links = {"f": [], "n": []}
                lid = 0
                for w, v in (("f", f), ("n", n)):
                    if not v:
                        continue
                    nmo, nmt = NAMES.get(l, ([], []))
                    so, st = name_spans(v["orig"], nmo), name_spans(v["tr"], nmt)
                    inname = lambda i: any(a <= i < b for a, b in so)
                    for t in v.get("terms") or []:
                        i = next((mm.start() for mm in re.finditer(re.escape(t["orig"]), v["orig"]) if not inname(mm.start())), -1)
                        if i < 0:
                            continue
                        lid += 1
                        cn = t.get("connotation") or ""
                        if so and cat(t["gloss"]) == "res" and cn:
                            cn = cn.rstrip() + " Also part of the group’s official name (Islamic Resistance Movement); here it is used as a description."
                        links[w].append([i, i + len(t["orig"]), find_tr(v["tr"], t["gloss"], st), t["gloss"], cat(t["gloss"] + " " + (t.get("connotation") or "")[:0]), "t%d" % lid, cn])
                    for j, c in enumerate(kc):
                        o_, g_ = (c["from_orig"], c["from_gloss"]) if w == "f" else (c["to_orig"], c["to_gloss"])
                        i = v["orig"].find(o_) if o_ and "(" not in o_[:1] else -1
                        if i < 0 or any(x[0] <= i < x[1] for x in links[w]):
                            continue
                        lid += 1
                        links[w].append([i, i + len(o_), find_tr(v["tr"], g_), g_, "kc", "k%d" % lid, c.get("note") or ""])
                    for o_, g_, c_ in KEY.get(l, []):
                        for mm in re.finditer(re.escape(o_), v["orig"], flags=re.I):
                            i, j = mm.start(), mm.end()
                            if any(x[0] < j and i < x[1] for x in links[w]) or inname(i):
                                continue
                            lid += 1
                            links[w].append([i, j, find_tr(v["tr"], g_, st), g_, c_, "d%d" % lid, ""])
                meta = {w: {"d": v["date"], "r": v["revid"], "v": v["voice"], "tr": 1 if v.get("truncated") else 0, "nt": v.get("note")}
                        for w, v in (("f", f), ("n", n)) if v}
                sl[s] = {"m": meta, "o": rec["o"], "t": rec["t"], "L": links, "u": 1 if d.get("unchanged") else 0}
            out.setdefault(a, {})[l] = {"ti": X.get("title"), "d": [(X.get("first") or {}).get("date"), (X.get("latest") or {}).get("date")], "hc": [hc.get("claim"), hc.get("first"), hc.get("latest"), hc.get("evidence_slot")] if hc else None,
                                        "kc": [[c.get("from_orig"), c.get("from_gloss"), c.get("to_orig"), c.get("to_gloss"), c.get("note")] for c in kc], "sl": sl}
    if odd_total:
        print(f"langs: {odd_total} unmarked words differ in position between versions; they swap without a mark")
    return {"order": ORDER, "voice": L["meta"]["voice_codes"], "missing": L["meta"]["missing_articles"],
            "cols": [[k, lab] for k, lab, _ in COLS], "cells": cells, "moments": moms, "arts": out}

res["langs"] = langs_data()


# Cross-wiki aggregates (analyze_crosswiki.py -> patterns/crosswiki/chart_data). Only dates and counts are inlined:
# no revision ids, account ids or hashes. The prose numbers in #crosslang and #organised are checked against these.
def crosswiki_data():
    D = os.path.join(PAT, "crosswiki", "chart_data")
    if not os.path.exists(os.path.join(D, "creation.json")):
        return None
    J = lambda n: json.load(open(os.path.join(D, n + ".json")))
    gg = J("creation").get("Gaza genocide") or {}
    created = sorted(([l, v["created"], v.get("days_after_english") or 0] for l, v in gg.items()), key=lambda r: r[1])
    E = J("exposure")
    expo = {l: round(100 * ((v.get("after_war") or {}).get("genocide") or {}).get("own_voice", 0)) for l, v in E.items()}
    A, S, Y, SR, RF = J("crosswiki_accounts"), J("sync"), J("diffusion"), J("sources"), J("rfc")
    # the static prose quotes these numbers: fail the build if the data moved under it
    chk = [(A["insert"]["accounts"], 281), (A["insert"]["same_family_2plus_languages"]["observed"], 0), (A["remove"]["accounts"], 284),
           (A["remove"]["same_family_2plus_languages"]["observed"], 0), (A["same_article_2plus_languages"]["observed"], 153),
           (round(A["same_article_2plus_languages"]["expected_by_chance"]), 106),
           (S["windows"]["1d"]["cross_account_cross_language_pairs"]["observed"], 135), (S["windows"]["1w"]["cross_account_cross_language_pairs"]["observed"], 925),
           (round(S["windows"]["1w"]["cross_account_cross_language_pairs"]["expected_by_chance"]), 579),
           (round(100 * SR["stuck_vs_reverted"]["share_new_source_stuck"]), 50), (round(100 * SR["stuck_vs_reverted"]["share_new_source_reverted"]), 28),
           (RF["sticks"], 26), (RF["settled_within_30d_after_close"]["observed"], 6), (round(100 * Y["english_first_share"]["observed"]), 69),
           (J("blocs")["edges"], 0), (expo.get("en"), 11), (expo.get("he"), 4)]
    bad = [(i, a, b) for i, (a, b) in enumerate(chk) if a != b]
    assert not bad, f"cross-wiki prose numbers out of date: {bad}"
    return {"gg": created, "expo": expo}

res["xw"] = crosswiki_data()

tk_p = os.path.join(HERE, "notes", "takeaways.json")
if os.path.exists(tk_p):
    res["takeaways"] = json.load(open(tk_p))

# Quotes are shown as exact text: decode HTML entities copied from wikitext (&nbsp;, &ndash;, &#702;) so the
# page's esc() renders them as characters, not as "&nbsp;". langs is skipped: its character spans index the raw text.
import html as _html
def _unent(o):
    if isinstance(o, str):
        return _html.unescape(o) if "&" in o else o
    if isinstance(o, list):
        return [_unent(x) for x in o]
    if isinstance(o, dict):
        return {k: _unent(v) for k, v in o.items()}
    return o
for _k in list(res):
    if _k != "langs":
        res[_k] = _unent(res[_k])
_ent = re.compile(r"&[a-z]+;|&#\d+;")
_left = [k for k in res if k != "langs" and _ent.search(json.dumps(res[k], ensure_ascii=False))]
assert not _left, f"HTML entities left in quote data: {_left}"

findings_path = os.path.join(HERE, "findings.html")
findings = open(findings_path).read() if os.path.exists(findings_path) else ""
tpl = open(os.path.join(HERE, "page_template.html")).read()
labdir = os.path.join(HERE, "lab")
lab_html = open(os.path.join(labdir, "lab.html")).read() if os.path.exists(os.path.join(labdir, "lab.html")) else ""
lab_css = open(os.path.join(labdir, "lab.css")).read() if os.path.exists(os.path.join(labdir, "lab.css")) else ""
lab_js = open(os.path.join(labdir, "lab.js")).read() if os.path.exists(os.path.join(labdir, "lab.js")) else ""
tpl = (tpl.replace("<!--LAB-->", lab_html).replace("/*LABCSS*/", lab_css).replace("/*LABJS*/", lab_js))
html = (tpl.replace("<!--FINDINGS-->", findings)
           .replace("/*DATA*/null", json.dumps(res, separators=(",", ":")).replace("</", "<\\/")
                        # 9 stored Hamas revisions lost the Arabic name in "(an Arabic acronym from ...)": never show an empty parenthesis
                        .replace("acronym from )", "acronym from [Arabic name not in this revision\\u2019s text])")))
assert "acronym from )" not in html, "empty Arabic parenthesis in a rendered quote"
open(sys.argv[1], "w").write(html)
print(f"wrote {sys.argv[1]} ({len(html)/1e6:.1f} MB)")
