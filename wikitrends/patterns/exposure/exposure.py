"""View-weighted exposure: of all the times readers opened the six flash hero articles, what share met each wording?

Inputs (data only; nothing in the page templates or build scripts is touched):
  views_daily.json.gz  wikitrends-data:views/<run>/views/  daily agent=user pageviews (current title, former titles from page
                       moves, current redirects) + every revision's section 0 since 2021 (timestamp, first sentence, lead hash)
  lead_<Title>.json.gz same run: lead prose by hash (used for the Israel opening-section row)
  ../../data/leads.json the Jan 2021 lead (rev0), used only to fill the days between 1 Jan 2021 and the first 2021 edit

Matching follows the flash edition: whitespace-normalised, curly apostrophes folded (build_flash.norm), substring tests on
the first sentence as ratchet.py splits it (analyze.sentences on analyze.prose of section 0), Israel on the whole section 0.

  python exposure.py <dir with views_daily.json.gz> [<dir of a later run> ...] -> exposure.json
  (run 42651558741: the six hero articles; run 42704500939: Benjamin Netanyahu and Palestine, the other two reach bars)
"""
import bisect, gzip, json, os, re, sys
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
WT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, WT)
import analyze as A  # noqa: E402

norm = lambda t: re.sub(r"\s+", " ", (t or "").replace("’", "'").replace(" ", " "))
low = lambda t: norm(t).lower()
UTC = timezone.utc
WAR = datetime(2023, 10, 7, tzinfo=UTC)


def has(*pats):
    return lambda s: all(re.search(p, s) for p in pats)


ATTR = r"accus|according to|\bstates? that|\bsays? that|have stated|has been described|characteri[sz]|considered"
# per article: text field ("fs" first sentence, "lead" section 0), ordered (key, label, predicate) on lowercased text; first
# match wins; the remainder is "other". "crit" and "soft" name the hero's then/now categories.
RULES = {
    "Israel": {"text": "lead", "crit": ["committing", "accusation"], "soft": "no_genocide", "cats": [
        ("committing", "own voice: “began committing genocide” in the opening section", has(r"committing genocide")),
        ("accusation", "“genocide” in the opening section as an accusation (“accusations that it has committed … genocide”)", has(r"genocid")),
        ("no_genocide", "no “genocide” in the opening section", lambda s: True)]},
    "Zionism": {"text": "fs", "crit": "colonization", "soft": "re_establishment", "cats": [
        ("colonization", "“colonization” / “colonial” in the first sentence", has(r"coloni[sz]|colonial")),
        ("re_establishment", "“re-establishment” (no colonization)", has(r"re-?establish")),
        ("establishment", "“establishment of … homeland/state”, neither colonization nor re-establishment", has(r"establish"))]},
    "Nakba": {"text": "fs", "crit": "ec_by_zionists", "soft": "destruction", "cats": [
        ("ec_by_zionists", "“ethnic cleansing … by Zionists”", has(r"ethnic cleansing", r"by zionists")),
        ("ec_other", "“ethnic cleansing” with another or no agent (by Israel, Israeli, none)", has(r"ethnic cleansing")),
        ("destruction", "“the destruction of Palestinian society” (no ethnic cleansing)", has(r"destruction of palestinian society"))]},
    "October 7 attacks": {"text": "fs", "crit": "armed_incursions", "soft": "coordinated_attacks", "cats": [
        ("armed_incursions", "“armed incursions”", has(r"armed incursion")),
        ("coordinated_attacks", "“coordinated attacks” (or other “attack(s)” wording, no incursions)", has(r"attack"))]},
    "Hamas": {"text": "fs", "crit": "political_org", "soft": "militant", "cats": [
        ("political_org", "“political organisation with a military wing”", has(r"political organi[sz]ation with a military wing")),
        ("militant", "“militant” in the first sentence", has(r"\bmilitant")),
    ]},
    # run 2 (the two other flash reach bars): the opening section, as for Israel; the charge in any voice (the treemap's test)
    "Benjamin Netanyahu": {"text": "lead", "crit": "genocide", "soft": "no_genocide", "cats": [
        ("genocide", "“genocide” in the opening section", has(r"genocid")),
        ("no_genocide", "no “genocide” in the opening section", lambda s: True)]},
    "Palestine": {"text": "lead", "crit": "genocide", "soft": "no_genocide", "cats": [
        ("genocide", "“genocide” in the opening section", has(r"genocid")),
        ("no_genocide", "no “genocide” in the opening section", lambda s: True)]},
    "Gaza genocide": {"text": "fs", "crit": "own_voice", "soft": "allegations", "cats": [
        ("allegations", "“Allegations have been made” / alleged", has(r"\ballegation|\balleged")),
        ("attributed", "attributed: “accused of”, “according to …”", has(ATTR)),
        ("own_voice", "own voice: genocide stated as fact (“carried out by Israel”)", has(r"genocid"))]},
}


HERO = {"Israel": ("began committing genocide", None), "Zionism": ("a Jewish homeland through colonization", "re-establishment"),
        "Nakba": ("the ethnic cleansing of Palestinian Arabs by Zionists", "the destruction of Palestinian society"),
        "October 7 attacks": ("coordinated armed incursions", "coordinated attacks"),
        "Hamas": ("political organisation with a military wing", "militant"),
        "Gaza genocide": ("carried out by Israel", "Allegations have been made"),
        "Benjamin Netanyahu": ("orchestrating the Gaza genocide", None), "Palestine": ("recognised as constituting genocide", None)}


def hero(title, text):
    now, then = HERO[title]
    t = norm(text)
    if now in t:
        return "now"
    if (then is None and "genocid" not in t.lower()) or (then and then in t):
        return "then"
    return "neither"


def classify(rule, text):
    s = low(text)
    for k, _, p in rule["cats"]:
        if p(s):
            return k
    return "other"


def ep(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC).timestamp()


def day0(d):
    return datetime.strptime(d, "%Y%m%d").replace(tzinfo=UTC)


def main(*srcs):
    V, SRC = {}, {}
    for d in srcs:
        for t, a in json.load(gzip.open(os.path.join(d, "views_daily.json.gz")))["articles"].items():
            V[t], SRC[t] = a, d
    src = " + ".join(srcs)
    L0 = {v["title"]: v for v in json.load(open(os.path.join(WT, "data", "leads.json")))}
    out = {"generated": datetime.now(UTC).strftime("%Y-%m-%d"), "source": src, "articles": {}}
    for title, rule in RULES.items():
        a = V[title]
        texts = json.load(gzip.open(os.path.join(SRC[title], f"lead_{title.replace(' ', '_')}.json.gz"))) if rule["text"] == "lead" else {}
        notes = []
        # state change points (t, cat): carry the last known state through hidden revisions
        pts, last = [], None
        for r in a["revisions"]:
            if r.get("hidden"):
                continue
            txt = texts[r["h"]] if rule["text"] == "lead" else r.get("fs", "")
            c = classify(rule, txt) + "|" + hero(title, txt)
            if not norm(txt).strip() or re.match(r"#redirect", low(txt)):
                c = "not_article"
            if c != last:
                pts.append((ep(r["ts"]), c)); last = c
        first_t = ep(a["revisions"][0]["ts"])
        # the days from 1 Jan 2021 to the first 2021 edit: the Jan 2021 lead (leads.json rev0) if we have it
        lo = L0.get(title)
        if lo and lo["d0"] == "2021-01" and first_t > ep("2021-01-01T00:00:00Z"):
            txt = lo["lead0"] if rule["text"] == "lead" else (A.sentences(lo["lead0"]) or [""])[0]
            pts.insert(0, (ep("2021-01-01T00:00:00Z"), classify(rule, txt) + "|" + hero(title, txt)))
            notes.append(f"1 Jan 2021 to first 2021 edit ({a['revisions'][0]['ts'][:10]}): state from the Jan 2021 lead (leads.json rev0 {lo['rev0']})")
        elif first_t > ep("2021-01-02T00:00:00Z"):
            notes.append(f"no stored state before {a['revisions'][0]['ts'][:10]} (first revision since 2021 in the history as it stands now): those days are excluded")
        T = [p[0] for p in pts]

        def state_seconds(t0, t1):
            """{cat: seconds} live in [t0, t1)."""
            res = {}
            i = bisect.bisect_right(T, t0) - 1
            t = t0
            while t < t1:
                c = pts[i][1] if i >= 0 else "unknown"
                nxt = T[i + 1] if i + 1 < len(T) else float("inf")
                e = min(nxt, t1)
                res[c] = res.get(c, 0) + (e - t)
                t = e; i += 1
            return res

        # daily views: main = current title + former titles (moves); all = + every current redirect
        # a title counts from the moment it became the article's title (its first move-in; the first title from the start),
        # so views of the current title while it was still a redirect to something else are not counted
        mv = [(ep(r["ts"]), r["move"][0], r["move"][1]) for r in a["revisions"] if "move" in r]
        since = {(mv[0][1] if mv else title): 0.0}
        for t_, src_, dst_ in mv:
            since.setdefault(dst_, t_)
        main_titles = [x for x in since if x in a["views"]]
        days = sorted({d for x in a["views"].values() for d in x})

        def w_title(x, d):
            t0 = day0(d).timestamp()
            return min(1.0, max(0.0, (t0 + 86400 - since[x]) / 86400))
        vm = {d: sum(a["views"][x].get(d, 0) * w_title(x, d) for x in main_titles) for d in days}
        va = {d: sum(x.get(d, 0) for x in a["views"].values()) for d in days}
        per_day = []
        for d in days:
            t0 = day0(d).timestamp()
            ss = state_seconds(t0, t0 + 86400)
            per_day.append((d, ss, vm[d], va[d]))
        end = days[-1]
        W = {"all_2021_now": "20210101", "since_7_oct_2023": "20231007",
             "last_12_months": (day0(end) - timedelta(days=364)).strftime("%Y%m%d"),
             "surge_7_oct_to_31_dec_2023": "20231007"}
        W_END = {"surge_7_oct_to_31_dec_2023": "20231231"}
        keys = [k for k, _, _ in rule["cats"]] + ["other"]
        states = sorted({c for _, c in pts if c != "not_article"})
        crit = rule["crit"] if isinstance(rule["crit"], list) else [rule["crit"]]
        art = {"rule_text": "first sentence" if rule["text"] == "fs" else "opening section (section 0)",
               "categories": {k: l for k, l, _ in rule["cats"]} | {"other": "none of the above (incl. parse artefacts)"},
               "critical": crit, "softer": rule["soft"], "titles_views_main": {x: datetime.fromtimestamp(since[x], UTC).strftime("%Y-%m-%d %H:%M") if since[x] else "start" for x in main_titles},
               "hero_phrases": {"now": HERO[title][0], "then": HERO[title][1] or "no “genocide” anywhere in the opening section"},
               "n_redirect_titles_with_views": len(a["views"]) - len(main_titles), "last_day": end, "windows": {}}
        for wn, ws in W.items():
            sv = {k: 0.0 for k in states}; sa = {k: 0.0 for k in states}; st = {k: 0.0 for k in states}
            excl_v = excl_t = 0.0
            for d, ss, nm, na in per_day:
                if d < ws or d > W_END.get(wn, end):
                    continue
                known = {c: s for c, s in ss.items() if c in sv}
                ks = sum(known.values())
                excl_t += 86400 - ks
                if ks == 0:
                    excl_v += nm; continue
                excl_v += nm * (1 - ks / 86400)
                for c, s in known.items():
                    sv[c] += nm * s / 86400; sa[c] += na * s / 86400; st[c] += s
            marg = lambda D, j, ks: {k: sum(x for c, x in D.items() if c.split("|")[j] == k) for k in ks}
            vv, va_, tt = (marg(D, 0, keys) for D in (sv, sa, st))
            hk = ["now", "then", "neither"]
            hv, ht = marg(sv, 1, hk), marg(st, 1, hk)
            V_ = sum(vv.values()); VA = sum(va_.values()); TT = sum(tt.values())
            sh = lambda x, n: round(x / n, 4) if n else None
            w = {"from": ws, "to": W_END.get(wn, end), "views_total": round(V_), "views_total_incl_redirects": round(VA),
                 "days_covered": round(TT / 86400, 1), "views_excluded_no_state": round(excl_v),
                 "view_share": {k: sh(vv[k], V_) for k in keys}, "time_share": {k: sh(tt[k], TT) for k in keys},
                 "view_share_incl_redirects": {k: sh(va_[k], VA) for k in keys},
                 "views": {k: round(vv[k]) for k in keys}}
            s = rule["soft"]
            cv, ct = sum(vv[k] for k in crit), sum(tt[k] for k in crit)
            w["critical"] = {"view_share": sh(cv, V_), "time_share": sh(ct, TT), "views": round(cv)}
            w["softer"] = {"view_share": w["view_share"][s], "time_share": w["time_share"][s], "views": w["views"][s]}
            w["hero_exact_phrase"] = {k: {"view_share": sh(hv[k], V_), "time_share": sh(ht[k], TT), "views": round(hv[k])} for k in hk}
            oth = [k for k in keys if k not in crit and k != s]
            w["other_or_neither"] = {"view_share": sh(sum(vv[k] for k in oth), V_), "time_share": sh(sum(tt[k] for k in oth), TT),
                                     "views": round(sum(vv[k] for k in oth))}
            w["gap_points_critical"] = round(100 * (w["critical"]["view_share"] - w["critical"]["time_share"]), 1) if V_ and TT else None
            art["windows"][wn] = w
            for k in keys + ["critical", "softer", "other_or_neither"]:
                a_, b_ = (w["view_share"][k], w["time_share"][k]) if k in keys else (w[k]["view_share"], w[k]["time_share"])
                if a_ is not None and b_ is not None and abs(a_ - b_) > 0.10 and not (k in keys and k in crit + [s] and len(crit) == 1):
                    out.setdefault("flags_view_vs_time_over_10_points", []).append(
                        {"article": title, "window": wn, "category": k, "view_share": a_, "time_share": b_, "gap_points": round(100 * (a_ - b_), 1)})
        # episodes: each stretch of the critical wording, its days and views (finds brief wordings during spikes)
        eps = []
        for i, (t, c) in enumerate(pts):
            t1 = pts[i + 1][0] if i + 1 < len(pts) else day0(end).timestamp() + 86400
            if t1 <= ep("2021-01-01T00:00:00Z"):
                continue
            v = 0.0
            for d, ss, nm, na in per_day:
                t0 = day0(d).timestamp()
                ov = max(0, min(t1, t0 + 86400) - max(t, t0))
                if ov:
                    v += nm * ov / 86400
            eps.append({"cat": c.split("|")[0], "hero": c.split("|")[-1], "from": datetime.fromtimestamp(t, UTC).strftime("%Y-%m-%d %H:%M"),
                        "to": datetime.fromtimestamp(t1, UTC).strftime("%Y-%m-%d %H:%M"), "days": round((t1 - t) / 86400, 2), "views": round(v)})
        art["episodes_top_views_per_day"] = sorted([e for e in eps if e["days"] > 0 and e["views"]],
                                                    key=lambda e: -e["views"] / max(e["days"], 1 / 24))[:12]
        art["n_state_changes"] = len(pts)
        art["moves"] = [[r["ts"]] + r["move"] for r in a["revisions"] if "move" in r]
        art["notes"] = notes
        out["articles"][title] = art
    json.dump(out, open(os.path.join(HERE, "exposure.json"), "w"), indent=1, ensure_ascii=False)
    return out


if __name__ == "__main__":
    main(*sys.argv[1:])
