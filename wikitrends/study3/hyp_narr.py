"""Study 3 narrative-lens hypotheses (discovery-derived). Each hNN_* function takes a list of articles in the
discovery/holdout schema and returns a dict of statistics plus a 'pass' flag for the pre-stated prediction.
Deep-schema functions use: group, created_in_window, subgroup, lead_diff, lead_frame_series, first_sentences.
Mass-schema functions use: g, p, l (lead frame counts [words, 12 frames] at 3 dates).
Regexes for N4/N6 are copied verbatim from wikitrends/narrative.py so results are comparable with study 2.
"""
import re
from collections import Counter

LEXICON = {
"settler_colonial": {
"include": [
"settler[- ]colonial\\w*",
"\\bcoloni[sz](?:ation|ations|e|es|ed|ing|er|ers)\\b",
"colonial (?:project|enterprise|state|regime|venture)",
"\\bcolonialis[mt]s?\\b"
],
"exclude": [
"(?:greek|phoenician|roman|spanish|portuguese|space|mars) coloni[sz]"
]
},
"apartheid": {
"include": [
"\\bapartheid\\b"
],
"exclude": []
},
"genocide": {
"include": [
"\\bgenocid\\w*"
],
"exclude": []
},
"ethnic_cleansing": {
"include": [
"ethnic(?:ally)? cleans\\w*"
],
"exclude": []
},
"occupation": {
"include": [
"occupied territor\\w*",
"(?:military|belligerent|illegal|foreign|israeli|russian|turkish|moroccan|indian|pakistani|chinese|armenian|azerbaijani) occupation",
"occupying (?:power|forces?|army)",
"under occupation",
"occupation of (?:the )?(?:west bank|gaza|palestin\\w*|golan|east jerusalem|crimea|northern cyprus|kashmir|tibet|western sahara|donbas|nagorno)",
"occupied (?:west bank|gaza|palestin\\w*|golan|east jerusalem|crimea|northern cyprus|kashmir|tibet|western sahara|ukrain\\w*)"
],
"exclude": [
"(?:german|nazi|axis|japanese|ottoman|british|roman|allied|soviet) (?:military )?occupation"
]
},
"nakba_expulsion": {
"include": [
"\\bnakba\\b",
"\\bdispossess\\w*",
"\\bexpul\\w*",
"\\bexpell\\w*"
],
"exclude": [
"expul\\w* of (?:the )?jews",
"expell\\w* (?:the )?jews",
"jews (?:were|was) expell\\w*",
"jewish expul\\w*",
"expul\\w* of jews",
"alhambra",
"edict of expulsion"
]
},
"war_crimes": {
"include": [
"war crimes?",
"crimes? against humanity",
"collective punishment"
],
"exclude": []
},
"indigenous_homeland": {
"include": [
"\\bindigenous\\b",
"ancestral homeland",
"\\bhomeland\\b",
"self-determination",
"land of israel",
"\\beretz\\b",
"jewish (?:connection|continuity|presence) (?:to|in|with)"
],
"exclude": [
"palestinian (?:homeland|self-determination)",
"indigenous palestin\\w*",
"palestinians? (?:as|are) (?:the )?indigenous",
"kurdish (?:homeland|self-determination)"
]
},
"persecution_antisemitism": {
"include": [
"\\bantisemit\\w*",
"\\banti-semit\\w*",
"\\bpersecut\\w*",
"\\bpogroms?\\b"
],
"exclude": []
},
"terrorism": {
"include": [
"\\bterroris[mt]\\w*"
],
"exclude": []
},
"militant": {
"include": [
"\\bmilitants?\\b",
"\\bmilitancy\\b"
],
"exclude": []
},
"placebo_geography": {
"include": [
"\\brivers?\\b",
"\\bmountains?\\b",
"\\bdeserts?\\b",
"\\bclimate\\b",
"\\brainfall\\b",
"\\bcoast(?:al|line)?\\b",
"\\bvalleys?\\b"
],
"exclude": []
}
}
FRAMES = list(LEXICON)
CRIT = ["settler_colonial", "apartheid", "genocide", "ethnic_cleansing", "occupation", "nakba_expulsion", "war_crimes"]
_LX = {k: (re.compile("|".join(v["include"]), re.I), re.compile("|".join(v["exclude"]), re.I) if v["exclude"] else None)
       for k, v in LEXICON.items()}
R = lambda p: re.compile(p, re.I)
# --- verbatim from wikitrends/narrative.py ---
DISP_P = R(r"\b(?:nakba|palestinian (?:refugees?|exodus|expulsions?|displacement|flight)|1948 palestinian expulsion)\b")
DISP_J = R(r"\b(?:jewish exodus|jewish refugees|expulsions? of (?:the )?jews from (?:arab|muslim)\w*|jews (?:from|of) arab (?:countries|lands|states)|"
           r"farhud|mizrahi refugees|exodus of jews from)\b")
VIOL = R(r"\b(?:terroris[mt]s?|terror attacks?|massacres?)\b")
ACT_P = R(r"\b(?:palestinians?|hamas|plo|fatah|islamic jihad|pflp|fedayeen|arab (?:gunmen|militants|rioters|forces)|hezbollah)\b")
ACT_I = R(r"\b(?:israel(?:i|is)?|idf|israel defense forces|irgun|lehi|haganah|settlers?|jewish (?:militants|underground|terrorists)|kach|kahane)\b")
JEWISH_HIST = R(r"\b(?:jewish|jews|israelites?|hebrews?|judaism|temple|kingdom of (?:israel|judah)|judean)\b")
# --- study-3 narrative-lens definitions (fixed from discovery; do not tune on holdout) ---
IPCTX = R(r"\b(?:israel\w*|zionis\w+|palestin\w+|gaza\w*|west bank|idf|haganah|irgun|lehi|nakba|settle(?:r|ment)s?|occupied territor\w+|arabs?)\b")
JEWVICT = R(r"\bholocaust|shoah|nazi|1492|spain|iberia|jews (?:were|was) (?:expelled|deported)|expulsion of (?:the |many )?jews|sephard")
ATTR = R(r"\b(?:critics?|accus\w+|alleg\w+|described as|characteri[sz]\w+|according to|consider(?:ed|s)?|view(?:ed|s)? (?:it|as|this)|"
         r"argu\w+|claim\w*|deni\w+|deny|disput\w+|some (?:scholars|historians|observers)|have called|has called|labell?ed|controvers\w+|"
         r"opponents?|critici[sz]\w+|regarded as|reject\w+|describ\w+|accord\w*|scholars|historians|experts|organi[sz]ations|groups have|"
         r"has been (?:called|termed)|referred to (?:by|as)|known (?:by|to) palestinians|says?|said|stated?)\b")
CONT = R(r"\b(?:re-?establish\w*|return(?:ed|ing)? to|restor\w*|ancestral|homeland|reviv\w*|ingathering|repatriat\w*|re-?constitut\w*|"
         r"historic(?:al)? (?:land|homeland|connection)|continuous|continuity|persisted)\b")
EVENT = R(r"\b(?:october 7|7 october|2023|2024|2025|2026|gaza war|israel[–-]hamas war|gaza genocide|ongoing)\b")
HIST = R(r"\b(?:1947|1948|1949|1967|nakba|mandat\w+|ottoman|zionis\w+|19th|20th|partition|six-day)\b")
LANDNAME_P = R(r"mandatory palestine|region of palestine|palestine region|19(?:47|48)(?:[–-](?:19)?(?:48|49))? palestine war")
LANDNAME_J = R(r"\bland of israel|eretz israel|\bjudea\b|\bjudaea\b")


def crit_hits(s):
    n = 0
    for f in CRIT:
        inc, exc = _LX[f]
        for m in inc.finditer(s):
            if exc and exc.search(s[max(0, m.start() - 40):m.end() + 40]):
                continue
            n += 1
    return n


def ip_crit(s):
    """Critical-frame sentence about Israel/Palestine (not about Jews as victims of Nazis/Spain)."""
    return crit_hits(s) > 0 and bool(IPCTX.search(s)) and not JEWVICT.search(s)


def lead(a, side):
    """Lead sentences at the first (side=0) or last (side=1) snapshot, rebuilt from lead_diff."""
    want = "-" if side == 0 else "+"
    return [x["s"] for x in (a.get("lead_diff") or []) if x["t"] in ("=", want)]


def _topic(arts, existing=True):
    return [a for a in arts if a.get("group") == "treatment" and not (existing and a.get("created_in_window"))]


def _control(arts, existing=True):
    return [a for a in arts if a.get("group") != "treatment" and not (existing and a.get("created_in_window"))]


def _spearman(x, y):
    from scipy.stats import spearmanr
    r = spearmanr(x, y)
    return float(r.statistic), float(r.pvalue)


def _sign(up, down):
    from scipy.stats import binomtest
    return float(binomtest(up, up + down).pvalue) if up + down else None


# H1 Additive layering: critical gain is uncorrelated with loss of Jewish continuity / Jewish-history lead content.
def h1_additive_layering_deep(arts):
    rows = []
    for a in _topic(arts):
        L0, L1 = lead(a, 0), lead(a, 1)
        if not L0 or not L1:
            continue
        w0 = sum(len(s.split()) for s in L0) or 1; w1 = sum(len(s.split()) for s in L1) or 1
        d_ip = sum(map(ip_crit, L1)) - sum(map(ip_crit, L0))
        d_cont = sum(len(CONT.findall(s)) for s in L1) - sum(len(CONT.findall(s)) for s in L0)
        d_jh = 100 * (sum(len(JEWISH_HIST.findall(s)) for s in L1) / w1 - sum(len(JEWISH_HIST.findall(s)) for s in L0) / w0)
        rows.append((d_ip, d_cont, d_jh))
    x = [r[0] for r in rows]
    rc = _spearman(x, [r[1] for r in rows]); rj = _spearman(x, [r[2] for r in rows])
    g = [r for r in rows if r[0] > 0]; ng = [r for r in rows if r[0] <= 0]
    out = dict(n=len(rows), rho_crit_cont=rc, rho_crit_jhdensity=rj,
               gainers=len(g), frac_cont_loss_gainers=sum(r[1] < 0 for r in g) / max(1, len(g)),
               frac_cont_loss_others=sum(r[1] < 0 for r in ng) / max(1, len(ng)))
    # prediction: no negative association (substitution would give rho < -0.15)
    out["pass"] = rc[0] > -0.15 and rj[0] > -0.15
    return out


def h1_domain_split_mass(arts, frames=None):
    """Mass schema. Share of articles with >=1 critical lead-frame hit, 2021-01 vs latest, by project.
    Prediction: Israel and Palestine projects rise >= 1.5 pp more than control; Judaism and Jewish history projects
    change < 1.5 pp (independence of the Jewish-history domain)."""
    frames = frames or FRAMES
    ci = [1 + frames.index(f) for f in CRIT]; ji = 1 + frames.index("indigenous_homeland")
    def stat(sel):
        A_ = [a for a in arts if sel(a) and a["l"][0] is not None and a["l"][-1] is not None and a["l"][0][0] > 0]
        c0 = sum(sum(a["l"][0][i] for i in ci) > 0 for a in A_) / max(1, len(A_))
        c1 = sum(sum(a["l"][-1][i] for i in ci) > 0 for a in A_) / max(1, len(A_))
        j0 = sum(a["l"][0][ji] > 0 for a in A_) / max(1, len(A_)); j1 = sum(a["l"][-1][ji] > 0 for a in A_) / max(1, len(A_))
        return dict(n=len(A_), crit0=c0, crit1=c1, dcrit=c1 - c0, indig0=j0, indig1=j1, dindig=j1 - j0)
    out = {p: stat(lambda a, p=p: a["g"] == "t" and a["p"] == p) for p in ("Judaism", "Jewish history", "Israel", "Palestine")}
    out["control"] = stat(lambda a: a["g"] == "c")
    dc = out["control"]["dcrit"]
    out["pass"] = (out["Israel"]["dcrit"] - dc >= 0.015 and out["Palestine"]["dcrit"] - dc >= 0.015
                   and abs(out["Judaism"]["dcrit"]) < 0.015 and abs(out["Jewish history"]["dcrit"]) < 0.015)
    return out


# H2 Post-2023 timing, pre-2023 content.
def h2_timing_vs_content(arts, war_q="2023-10"):
    T = _topic(arts)
    added = [x["s"] for a in T for x in (a.get("lead_diff") or []) if x["t"] == "+" and crit_hits(x["s"])]
    ev = sum(bool(EVENT.search(s)) for s in added); hi = sum(bool(HIST.search(s)) for s in added)
    def steps(group):
        pre = post = 0; npre = npost = 0
        for a in group:
            s = a.get("lead_frame_series"); dts = a.get("crit_series_dates")
            if not s or not dts or war_q not in dts:
                continue
            iw = dts.index(war_q)
            tot = [None if any(s[f][k] is None for f in CRIT) else sum(s[f][k] for f in CRIT) for k in range(len(dts))]
            for k in range(1, len(dts)):
                if tot[k] is None or tot[k - 1] is None:
                    continue
                if k < iw: npre += 1; pre += tot[k] > tot[k - 1]
                else: npost += 1; post += tot[k] > tot[k - 1]
        return dict(up_rate_pre=pre / max(1, npre), up_rate_post=post / max(1, npost))
    t, c = steps(T), steps(_control(arts))
    out = dict(added_crit_sents=len(added), event_anchored=ev, history_anchored=hi, topic=t, control=c)
    out["pass"] = (ev < hi and ev / max(1, len(added)) < 0.2
                   and t["up_rate_post"] / max(1e-9, t["up_rate_pre"]) > 1.5 * c["up_rate_post"] / max(1e-9, c["up_rate_pre"]))
    return out


# H3 Palestine as the default land-name for the Ottoman/Mandate era (not antiquity).
def h3_modern_land_naming(arts):
    def tally(group):
        r = dict(P0=0, P1=0, J0=0, J1=0, up=0, down=0)
        for a in group:
            p0 = sum(len(LANDNAME_P.findall(s)) for s in lead(a, 0)); p1 = sum(len(LANDNAME_P.findall(s)) for s in lead(a, 1))
            r["P0"] += p0; r["P1"] += p1; r["up"] += p1 > p0; r["down"] += p1 < p0
            r["J0"] += sum(len(LANDNAME_J.findall(s)) for s in lead(a, 0)); r["J1"] += sum(len(LANDNAME_J.findall(s)) for s in lead(a, 1))
        r["sign_p"] = _sign(r["up"], r["down"])
        return r
    t, c = tally(_topic(arts)), tally(_control(arts))
    out = dict(topic=t, control=c)
    out["pass"] = t["up"] > 2 * t["down"] and (t["sign_p"] or 1) < 0.05 and t["J1"] >= 0.7 * t["J0"]
    return out


# H4 Wikivoice migration + Israel as agent in critical sentences.
def h4_wikivoice(arts):
    def tally(group, topic):
        tot = [0, 0]; un = [0, 0]; up = down = 0; isr = [0, 0]
        for a in group:
            u = []
            for side in (0, 1):
                ss = [s for s in lead(a, side) if (ip_crit(s) if topic else crit_hits(s) > 0)]
                tot[side] += len(ss); n_un = sum(not ATTR.search(s) for s in ss); un[side] += n_un; u.append(n_un)
                isr[side] += sum(bool(ACT_I.search(s)) for s in ss)
            up += u[1] > u[0]; down += u[1] < u[0]
        return dict(sents=tot, unattributed=un, share_unattr=[un[k] / max(1, tot[k]) for k in (0, 1)],
                    art_up=up, art_down=down, sign_p=_sign(up, down), israeli_actor=isr)
    t, c = tally(_topic(arts), True), tally(_control(arts), False)
    did = (t["share_unattr"][1] - t["share_unattr"][0]) - (c["share_unattr"][1] - c["share_unattr"][0])
    out = dict(topic=t, control=c, did_share_unattr=did)
    out["pass"] = t["art_up"] > 2 * t["art_down"] and (t["sign_p"] or 1) < 0.05 and did > 0
    return out


# H5 Two displacements: Palestinian displacement added, Jewish displacement not removed; violence labels sticky.
def h5_displacement_and_violence(arts):
    r = dict(P0=0, P1=0, J0=0, J1=0, P_up=0, P_down=0, J_up=0, J_down=0, viol_I0=0, viol_I1=0, viol_P0=0, viol_P1=0)
    def nearest(s, pos):
        best, bd = None, 10 ** 9
        for g, rx in (("P", ACT_P), ("I", ACT_I)):
            for m in rx.finditer(s):
                if abs(m.start() - pos) < bd: best, bd = g, abs(m.start() - pos)
        return best
    for a in _topic(arts):
        L = [lead(a, 0), lead(a, 1)]
        p = [sum(len(DISP_P.findall(s)) for s in l) for l in L]; j = [sum(len(DISP_J.findall(s)) for s in l) for l in L]
        r["P0"] += p[0]; r["P1"] += p[1]; r["J0"] += j[0]; r["J1"] += j[1]
        r["P_up"] += p[1] > p[0]; r["P_down"] += p[1] < p[0]; r["J_up"] += j[1] > j[0]; r["J_down"] += j[1] < j[0]
        for side, l in enumerate(L):
            for s in l:
                for m in VIOL.finditer(s):
                    g = nearest(s, m.start())
                    if g: r[f"viol_{g}{side}"] += 1
    sh = lambda i, p: i / max(1, i + p)
    r["viol_share_I"] = [sh(r["viol_I0"], r["viol_P0"]), sh(r["viol_I1"], r["viol_P1"])]
    r["pass"] = (r["P_up"] > 3 * max(1, r["P_down"]) and r["J_down"] <= r["J_up"] + 1
                 and abs(r["viol_share_I"][1] - r["viol_share_I"][0]) < 0.10)
    return r


ALL = [h1_additive_layering_deep, h2_timing_vs_content, h3_modern_land_naming, h4_wikivoice, h5_displacement_and_violence]

if __name__ == "__main__":
    import json, sys
    deep = sys.argv[1] if len(sys.argv) > 1 else "/home/user/photoStamper/wikitrends/data/study3/discovery_deep.json"
    mass = sys.argv[2] if len(sys.argv) > 2 else "/home/user/photoStamper/wikitrends/data/study3/discovery_mass.json"
    D = json.load(open(deep)); arts = D["articles"]
    for f in ALL:
        print(f.__name__, json.dumps(f(arts), default=str))
    M = json.load(open(mass))
    print("h1_domain_split_mass", json.dumps(h1_domain_split_mass(M["articles"], M.get("lab_frames")), default=str))
