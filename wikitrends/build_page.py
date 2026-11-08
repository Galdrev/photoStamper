"""Inline results.json + findings.html into the report page.

Usage: python build_page.py OUT.html
"""
import json, os, sys

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

tk_p = os.path.join(HERE, "notes", "takeaways.json")
if os.path.exists(tk_p):
    res["takeaways"] = json.load(open(tk_p))

findings_path = os.path.join(HERE, "findings.html")
findings = open(findings_path).read() if os.path.exists(findings_path) else ""
tpl = open(os.path.join(HERE, "page_template.html")).read()
labdir = os.path.join(HERE, "lab")
lab_html = open(os.path.join(labdir, "lab.html")).read() if os.path.exists(os.path.join(labdir, "lab.html")) else ""
lab_css = open(os.path.join(labdir, "lab.css")).read() if os.path.exists(os.path.join(labdir, "lab.css")) else ""
lab_js = open(os.path.join(labdir, "lab.js")).read() if os.path.exists(os.path.join(labdir, "lab.js")) else ""
tpl = (tpl.replace("<!--LAB-->", lab_html).replace("/*LABCSS*/", lab_css).replace("/*LABJS*/", lab_js))
html = (tpl.replace("<!--FINDINGS-->", findings)
           .replace("/*DATA*/null", json.dumps(res, separators=(",", ":")).replace("</", "<\\/")))
open(sys.argv[1], "w").write(html)
print(f"wrote {sys.argv[1]} ({len(html)/1e6:.1f} MB)")
