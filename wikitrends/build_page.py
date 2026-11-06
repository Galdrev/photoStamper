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
    def tags(s):
        if not s:
            return None
        t = [k for k in crit if has(k, s)]
        if re.search(r"\bre-?establish", s, re.I):
            t.append("re_establish")
        return t
    V = {v["id"]: v.get("s") for v in ra["fs_variants"]}
    tl = ra["fs_timeline"]
    state = [tags(V.get(i)) for _, i, _ in tl]
    blank = [d for d, i, _ in tl if V.get(i) == ""]
    # key moves: a term appears/disappears between consecutive kept wordings
    changes, last, last_k = [], None, None
    flips = {}
    for k, ((d, i, rv), st) in enumerate(zip(tl, state)):
        mv = []
        if st is not None:
            if last is not None:
                for term in set(last) | set(st):
                    if (term in st) != (term in last):
                        mv.append(term + ("+" if term in st else "-"))
                        flips.setdefault(term, []).append([d, "+" if term in st else "-"])
            last, last_k = st, k
        if k:
            changes.append([d, tl[k - 1][1], i, int(rv), sorted(mv)])
    def stat(term):
        f = flips.get(term, [])
        return {"in": sum(x[1] == "+" for x in f), "out": sum(x[1] == "-" for x in f),
                "first_in": next((x[0] for x in f if x[1] == "+"), None), "last": f[-1] if f else None,
                "start": term in (state[0] or []), "end": term in (last or [])}
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
            "n_wordings": ra.get("fs_n_variants") or len(set(i for _, i, _ in tl)),
            "n_kept": sum(1 for s in V.values() if s), "n_undone": sum(int(x[2]) for x in tl), "blank": blank,
            "first_ts": tl[0][0], "col": stat("settler_colonial"), "re": stat("re_establish"),
            "other_terms": sorted(t for t in flips if t not in ("settler_colonial", "re_establish"))}


res["zionism"] = zionism_data()

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
