"""Cross-wiki analysis on data/crosswiki.json.gz (crosswiki.py): how the key narrative terms travelled between language
editions, whether the same accounts carried them, and what the other traces (talk, logs, views, sources, Wikidata) show.

  python analyze_crosswiki.py [--data data/crosswiki.json.gz] [--null 1000] [--calib 200]
  python analyze_crosswiki.py --scan patterns/crosswiki       (publication privacy gate only)
  -> patterns/crosswiki/cards.md, cards.json, chart_data/*.json (network_crosswiki.json: coord's network.json schema + languages)

Cards (each: confidence, null model, expected-by-chance numbers; no usernames or hashes):
  T1 diffusion       first entry of each term family per article and language; lag vs English; who moved first. Null: each
                     language's entry dates permuted across the cells (article x family) where it has one
  T2 voice           attributed -> own-voice paths and timing per language. Null: transitions spread evenly over the
                     language's editing activity (share of its revisions after 7 Oct 2023)
  T3 trend           per language, cells present on 6 Oct 2023 vs now; insertion share after the war vs editing activity
                     (null: the page's events moved to random revisions of the same page)
  C1 accounts        accounts on the same article in 2+ languages; inserters (removers) of the same family in 2+ languages.
                     Null: accounts shuffled within language among accounts with the same activity (same number of articles /
                     families in that language)
  C2 synchrony       same-account and cross-account same-direction changes of a family in different languages within 1 h,
                     1 d, 1 w; campaign clusters (one article + family + direction in 3+ languages within 48 h). Null: every account-language timeline shifted by
                     a random offset (1-7 d / 3-21 d / 14-90 d / 7-60 d for the clusters); clusters are selection-calibrated
                     against the best cluster of each null world
  C3 blocs           analyze_coord.Engine / network / blocs on units "article [language]" (term events), with the
                     rewiring null run inside each language (stratified_curveball), plus talk-page co-activity as a second
                     edge type (accounts active in 2+ languages)
  C4 windows         analyze_coord.window_alignment for cross-wiki accounts and every community / flagged cluster
  N1-N4 narrative    Hamas terror-sentence position, hostage mentions, October 7 naming, court-ruling overstatement flags
  S1 sources         reference domains that arrive with a term insertion; sticking vs reverted insertions (permutation null)
  R1 RfC             English wordings settling after an RfC / RM close vs by attrition (null: uniform stick dates), and other
                     languages' moves after English closes
  K1 / L1 / V1 / W1  creation dates, renames + protection, pageview exposure to each framing, Wikidata descriptions
"""
import argparse, gzip, json, math, os, re, sys, time, zlib
from collections import Counter, defaultdict
from datetime import datetime, timezone

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze_coord as AC      # noqa: E402  (Engine, network, blocs, window_alignment, privacy_scan, card)
import explore as EX            # noqa: E402  (source classes)

OUT = os.path.join(HERE, "patterns", "crosswiki")
DATA = os.path.join(HERE, "data", "crosswiki.json.gz")
FAMILIES = ["colonial", "genocide", "apartheid", "occupation", "ethnic_cleansing"]
T0 = AC.ep("2021-01-01T00:00:00Z")
WAR = AC.ep("2023-10-07T00:00:00Z")
DAY, HOUR = 86400.0, 3600.0
SYNC_W = {"1h": (HOUR, (1, 7)), "1d": (DAY, (3, 21)), "1w": (7 * DAY, (14, 90))}
CAMPAIGN_W, CAMPAIGN_SHIFT, CAMPAIGN_MIN_LANGS = 2 * DAY, (7, 60), 3
STICK_D, SETTLE_D = 90, 30
COURT_SAID = {
    "icj_found_plausible_intent": "ICJ order of 26 Jan 2024: found some of the rights South Africa claimed plausible; it made no "
                                  "finding of intent",
    "icj_plausibly_genocidal": "No ICJ ruling uses the phrase 'plausibly genocidal'",
    "court_found_israel_guilty": "ICJ advisory opinion of 19 Jul 2024 is non-binding and gives no verdict of guilt",
    "icj_recognised_apartheid": "ICJ advisory opinion of 19 Jul 2024 found a breach of CERD Article 3 without saying whether it "
                                "was segregation or apartheid",
    "icj_ruled_genocide": "No ICJ judgment has found that Israel is committing genocide (merits pending)",
}


def iso(t):
    return AC.iso(t)


def ep(ts):
    return AC.ep(ts)


def pct(x):
    return f"{100 * x:.0f}%" if x is not None else "n/a"


def p_hi(null, obs):
    null = np.asarray(null, float)
    return round((int((null >= obs - 1e-12).sum()) + 1) / (len(null) + 1), 4)


def p_lo(null, obs):
    null = np.asarray(null, float)
    return round((int((null <= obs + 1e-12).sum()) + 1) / (len(null) + 1), 4)


def nstat(null, obs):
    null = np.asarray(null, float)
    return {"observed": obs, "expected_by_chance": round(float(null.mean()), 3) if len(null) else None,
            "null_p95": round(float(np.percentile(null, 95)), 3) if len(null) else None, "p": p_hi(null, obs)}


def conf_p(p, n, n_min=10):
    if n < n_min or p is None:
        return "low"
    return "high" if p <= 0.002 else "medium" if p <= 0.01 else "low"


def card(cid, title, what, conf, null, so_what, caveat, numbers=None, chart=None):
    return AC.card(cid, title, what, conf, null, so_what, caveat, numbers, chart)


# ------------------------------------------------------------------ page model
class Page:
    def __init__(self, r):
        self.r = r
        self.lang, self.concepts, self.concept = r["lang"], r["concepts"], r["concepts"][0]
        self.title = r.get("resolved_title") or r["title"]
        self.revs = r.get("revs") or []
        self.events = r.get("events") or []
        self.voice = r.get("voice") or []
        seed = r.get("seed") or {}
        self.created = r.get("created")
        self.tl = []                                        # (t, code) of known states, seed at T0
        if seed.get("state") and seed["state"] not in ("h", "r"):
            self.tl.append((T0, seed["state"]))
        for x in self.revs:
            s = x.get("s")
            if s and s not in ("h", "r"):
                self.tl.append((ep(x["t"]), s))
        self.ft = []                                        # (t, features)
        if seed.get("f"):
            self.ft.append((T0, seed["f"]))
        for x in self.revs:
            if x.get("f"):
                self.ft.append((ep(x["t"]), x["f"]))
        self.tt = np.array([t for t, _ in self.tl]) if self.tl else np.zeros(0)
        self.rev_t = np.array([ep(x["t"]) for x in self.revs]) if self.revs else np.zeros(0)
        self.baseline = self.tl[0][1] if self.tl and (seed.get("state") or not self.created or self.created < "2021") else None

    def state_at(self, t):
        if not len(self.tt):
            return None
        k = int(np.searchsorted(self.tt, t, side="right")) - 1
        return self.tl[k][1] if k >= 0 else None

    def feat_at(self, t):
        f = None
        for tt, x in self.ft:
            if tt > t:
                break
            f = x
        return f

    def end_state(self):
        return self.tl[-1][1] if self.tl else None


def load_pages(D):
    return [Page(r) for r in D["pages"] if not r.get("missing")]


def reg(e):
    return bool(e.get("u")) and not e.get("anon") and not e.get("bot")


def t_end(pages):
    ts = [p.rev_t.max() for p in pages if len(p.rev_t)]
    return float(max(ts)) if ts else time.time()


# ------------------------------------------------------------------ T1 diffusion
def entry_table(pages, langs, concepts):
    """{(concept, family): {lang: ("pre", None) | ("in", t) | ("never", None)}}"""
    by = defaultdict(list)
    for p in pages:
        for c in p.concepts:
            by[(c, p.lang)].append(p)
    tab = {}
    for c in concepts:
        for k, f in enumerate(FAMILIES):
            row = {}
            for l in langs:
                ps = by.get((c, l))
                if not ps:
                    continue
                if any(p.baseline and p.baseline[k] != "0" for p in ps):
                    row[l] = ("pre", None); continue
                ins = [ep(e["t"]) for p in ps for e in p.events if e["family"] == f and e["kind"] == "insert"]
                row[l] = ("in", min(ins)) if ins else ("never", None)
            tab[(c, f)] = row
    return tab


def diffusion(pages, langs, concepts, rng, n=1000):
    tab = entry_table(pages, langs, concepts)
    cells = [k for k, row in tab.items() if sum(1 for v in row.values() if v[0] == "in") >= 2]
    dated = {l: [(k, tab[k][l][1]) for k in tab if tab[k].get(l, ("",))[0] == "in"] for l in langs}

    def stats(T):
        lead, en_first, en_pairs, f90, lags = Counter(), 0, 0, 0, defaultdict(list)
        n_cells = 0
        for k in cells:
            ds = {l: T[l][k] for l in langs if k in T[l]}
            if len(ds) < 2:
                continue
            n_cells += 1
            lead[min(ds, key=ds.get)] += 1
            if "en" in ds:
                for l, t in ds.items():
                    if l == "en":
                        continue
                    lag = (t - ds["en"]) / DAY
                    lags[l].append(lag); en_pairs += 1
                    en_first += lag > 0; f90 += 0 < lag <= 90
        return {"lead": lead, "n_cells": n_cells, "en_first_share": en_first / en_pairs if en_pairs else None,
                "follow90_share": f90 / en_pairs if en_pairs else None, "pairs": en_pairs, "lags": lags}
    obs = stats({l: dict(v) for l, v in dated.items()})
    nulls = []
    for _ in range(n):
        T = {}
        for l, v in dated.items():
            ks = [k for k, _ in v]; ts = np.array([t for _, t in v]); rng.shuffle(ts)
            T[l] = dict(zip(ks, ts))
        nulls.append(stats(T))
    lead_tab = {l: {"first_in_cells": obs["lead"].get(l, 0),
                    "expected_by_chance": round(float(np.mean([s["lead"].get(l, 0) for s in nulls])), 2),
                    "p_high": p_hi([s["lead"].get(l, 0) for s in nulls], obs["lead"].get(l, 0))} for l in langs}
    ef = [s["en_first_share"] for s in nulls if s["en_first_share"] is not None]
    fl = [s["follow90_share"] for s in nulls if s["follow90_share"] is not None]
    lag_sum = {l: {"n": len(v), "median_days": round(float(np.median(v)), 1), "q25": round(float(np.percentile(v, 25)), 1),
                   "q75": round(float(np.percentile(v, 75)), 1), "share_after_english": round(float(np.mean(np.array(v) > 0)), 3)}
               for l, v in obs["lags"].items() if v}
    pre_en_later = sum(1 for k, row in tab.items() if row.get("en", ("",))[0] == "pre" for l, v in row.items() if l != "en" and v[0] == "in")
    cells_out = []
    for (c, f), row in sorted(tab.items()):
        en = row.get("en")
        cells_out.append({"article": c, "family": f, "languages": {
            l: {"status": v[0], "date": iso(v[1])[:10] if v[1] else None,
                "lag_vs_english_days": round((v[1] - en[1]) / DAY, 1) if (v[1] and en and en[0] == "in" and l != "en") else None}
            for l, v in sorted(row.items())}})
    return {"cells_with_2plus_dated": obs["n_cells"], "pairs_with_english": obs["pairs"], "leader": lead_tab,
            "english_first_share": {"observed": round(obs["en_first_share"], 3) if obs["en_first_share"] is not None else None,
                                    "expected_by_chance": round(float(np.mean(ef)), 3) if ef else None,
                                    "p_high": p_hi(ef, obs["en_first_share"]) if ef and obs["en_first_share"] is not None else None},
            "follow_within_90d_share": {"observed": round(obs["follow90_share"], 3) if obs["follow90_share"] is not None else None,
                                        "expected_by_chance": round(float(np.mean(fl)), 3) if fl else None,
                                        "p_high": p_hi(fl, obs["follow90_share"]) if fl and obs["follow90_share"] is not None else None},
            "lags_vs_english": lag_sum, "english_had_it_before_2021_other_entered_later": pre_en_later, "cells": cells_out}


# ------------------------------------------------------------------ T2 voice
def binom_hi(k, n, p):
    if n == 0:
        return 1.0
    return float(sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1)))


def voice_paths(pages, langs):
    out = {}
    for l in langs:
        ps = [p for p in pages if p.lang == l]
        paths, lagd, trans = Counter(), [], []
        for p in ps:
            for k, f in enumerate(FAMILIES):
                fa = next((t for t, s in p.tl if s[k] == "1"), None)
                fs = next((t for t, s in p.tl if s[k] == "2"), None)
                if fa is None and fs is None:
                    continue
                endv = p.end_state()[k]
                if fa is not None and fs is not None and fa < fs:
                    paths["attributed_then_own_voice"] += 1; lagd.append((fs - fa) / DAY)
                elif fs is not None:
                    paths["own_voice_from_entry" if endv != "1" else "own_voice_then_attributed"] += 1
                else:
                    paths["attributed_only"] += 1
            trans += [ep(v["t"]) for v in p.voice if v["kind"] == "to_stated"]
        rv = np.concatenate([p.rev_t for p in ps]) if ps else np.zeros(0)
        share_post = float((rv >= WAR).mean()) if len(rv) else 0.0
        k_post = sum(t >= WAR for t in trans)
        ratchet_mode = any((p.r.get("coverage") or {}).get("mode") == "ratchet" for p in ps)
        out[l] = {"paths": dict(paths), "attributed_to_own_voice_median_days": round(float(np.median(lagd)), 1) if lagd else None,
                  "to_own_voice_transitions": len(trans), "after_war": k_post,
                  "expected_after_war_by_activity": round(len(trans) * share_post, 2), "share_revisions_after_war": round(share_post, 3),
                  "p_high": round(binom_hi(k_post, len(trans), share_post), 4) if trans else None,
                  "voice_coverage": "event revisions only (ratchet reuse)" if ratchet_mode else "every read revision"}
    return out


# ------------------------------------------------------------------ T3 trend
def trend(pages, langs, concepts, rng, n=1000):
    tend = t_end(pages)
    months = []
    y, m = 2021, 1
    while AC.ep(f"{y}-{m:02d}-01T00:00:00Z") < tend:
        months.append(f"{y}-{m:02d}"); y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    def cells_at(l, t, stated=False):
        cs = set()
        for p in pages:
            if p.lang != l:
                continue
            s = p.state_at(t)
            if not s:
                continue
            for k, f in enumerate(FAMILIES):
                if (s[k] == "2") if stated else (s[k] != "0"):
                    cs.add((p.concept, f))
        return cs
    series = {l: [{"month": mo, "cells_present": len(cells_at(l, ep(mo + "-01T00:00:00Z") + 27 * DAY)),
                   "cells_own_voice": len(cells_at(l, ep(mo + "-01T00:00:00Z") + 27 * DAY, True))} for mo in months] for l in langs}
    out = {}
    pre = WAR - DAY
    for l in langs:
        ps = [p for p in pages if p.lang == l]
        if not ps:
            continue
        a, b = cells_at(l, pre), cells_at(l, tend)
        ins = [(p, e) for p in ps for e in p.events if e["kind"] == "insert" and not e.get("creation")]
        obs = sum(ep(e["t"]) >= WAR for _, e in ins)
        nulls = []
        byp = defaultdict(int)
        for p, _ in ins:
            byp[id(p)] += 1
        pm = {id(p): p for p in ps}
        for _ in range(n):
            c = 0
            for pid, k in byp.items():
                rt = pm[pid].rev_t
                if len(rt):
                    c += int((rng.choice(rt, size=k) >= WAR).sum())
            nulls.append(c)
        out[l] = {"cells_present_6oct2023": len(a), "cells_present_now": len(b), "gained": len(b - a), "lost": len(a - b),
                  "gained_cells": sorted(f"{c}: {f}" for c, f in b - a)[:30], "lost_cells": sorted(f"{c}: {f}" for c, f in a - b)[:30],
                  "insertions": len(ins), "insertions_after_war": nstat(nulls, obs) if ins else None}
    en = out.get("en", {})
    for l, v in out.items():
        v["net_gain_vs_english"] = (v["gained"] - v["lost"]) - (en.get("gained", 0) - en.get("lost", 0))
    return out, series


# ------------------------------------------------------------------ C1 cross-wiki accounts
def _popcount(x):
    x = x.astype(np.int64)
    c = np.zeros(x.shape, np.int64)
    while x.any():
        c += x & 1; x = x >> 1
    return c


def _multi_bits(M, nbits):
    """M: accounts x langs bitmasks -> per account: any bit set in >= 2 languages."""
    cnt = np.zeros((M.shape[0], nbits), np.int16)
    for b in range(nbits):
        cnt[:, b] = ((M >> b) & 1).sum(axis=1)
    return (cnt >= 2).any(axis=1)


def _strata_perm(M, rng):
    M2 = M.copy()
    for l in range(M.shape[1]):
        col = M[:, l]
        deg = _popcount(col)
        for d in np.unique(deg[col != 0]):
            idx = np.where((col != 0) & (deg == d))[0]
            if len(idx) > 1:
                M2[idx, l] = col[rng.permutation(idx)]
    return M2


def cross_accounts(pages, langs, concepts, D, rng, n=1000):
    L = {l: i for i, l in enumerate(langs)}; Cn = {c: i for i, c in enumerate(concepts)}
    accs = {}
    def ai(u):
        if u not in accs:
            accs[u] = len(accs)
        return accs[u]
    edits = []
    for p in pages:
        for x in p.revs:
            if reg(x):
                for c in p.concepts:
                    edits.append((ai(x["u"]), L[p.lang], Cn[c]))
    ev = defaultdict(list)
    for p in pages:
        for e in p.events:
            if e["exact"] and reg(e):
                ev[e["kind"]].append((ai(e["u"]), L[p.lang], FAMILIES.index(e["family"]), Cn[p.concept]))
    NA, NL = len(accs), len(langs)
    res = {}
    if NA:
        M = np.zeros((NA, NL), np.int64)
        for a, l, c in edits:
            M[a, l] |= 1 << c
        active_langs = (M != 0).sum(axis=1)
        obs = int(_multi_bits(M, len(concepts)).sum())
        nulls = [int(_multi_bits(_strata_perm(M, rng), len(concepts)).sum()) for _ in range(n)]
        res["same_article_2plus_languages"] = {
            "accounts": int((active_langs >= 1).sum()), "accounts_in_2plus_languages": int((active_langs >= 2).sum()),
            "share_of_all": round(obs / max(1, int((active_langs >= 1).sum())), 4),
            "share_of_multilingual": round(obs / max(1, int((active_langs >= 2).sum())), 4), **nstat(nulls, obs)}
    for kind in ("insert", "remove"):
        rows = ev.get(kind) or []
        if not rows:
            res[kind] = None; continue
        F = np.zeros((NA, NL), np.int64); FC = np.zeros((NA, NL), np.int64)
        for a, l, f, c in rows:
            F[a, l] |= 1 << f; FC[a, l] |= 1 << (c * len(FAMILIES) + f)
        act = (F != 0).any(axis=1); nact = int(act.sum())
        multi = int(((F != 0).sum(axis=1) >= 2).sum())
        o_f = int(_multi_bits(F, len(FAMILIES)).sum()); o_fc = int(_multi_bits(FC, len(FAMILIES) * len(concepts)).sum())
        nf, nfc = [], []
        for _ in range(n):
            nf.append(int(_multi_bits(_strata_perm(F, rng), len(FAMILIES)).sum()))
            nfc.append(int(_multi_bits(_strata_perm(FC, rng), len(FAMILIES) * len(concepts)).sum()))
        res[kind] = {"accounts": nact, "accounts_in_2plus_languages": multi,
                     "same_family_2plus_languages": {"share_of_all": round(o_f / max(1, nact), 4), **nstat(nf, o_f)},
                     "same_family_same_article_2plus_languages": {"share_of_all": round(o_fc / max(1, nact), 4), **nstat(nfc, o_fc)}}
    # aggregate account facts: cross-wiki term accounts vs single-language term accounts
    inv = {v: k for k, v in accs.items()}
    langs_of = defaultdict(set)
    for kind in ("insert", "remove"):
        for a, l, f, c in ev.get(kind) or []:
            langs_of[a].add(l)
    def facts(group):
        ages, ecs, home_en, home_lang, local, nw = [], [], 0, 0, 0, []
        first_t = {}
        for p in pages:
            for e in p.events:
                if e["exact"] and reg(e):
                    first_t[e["u"]] = min(first_t.get(e["u"], 9e18), ep(e["t"]))
        for a in group:
            f = (D.get("accounts") or {}).get(inv[a]) or {}
            if f.get("reg") and inv[a] in first_t:
                ages.append((first_t[inv[a]] - ep(f["reg"] + "-01T00:00:00Z")) / (365.25 * DAY))
            if f.get("ec") is not None:
                ecs.append(f["ec"])
            home_en += f.get("home") == "enwiki"
            home_lang += bool(f.get("home")) and f.get("home") != "enwiki" and f.get("home")[:-4] in langs
            local += f.get("looked_up") is True and not f.get("global")
            if f.get("n_wikis"):
                nw.append(f["n_wikis"])
        k = max(1, len(group))
        return {"accounts": len(group), "median_global_age_years_at_first_event": round(float(np.median(ages)), 1) if ages else None,
                "median_global_edit_count": float(np.median(ecs)) if ecs else None,
                "share_home_english": round(home_en / k, 3), "share_home_other_studied_language": round(home_lang / k, 3),
                "share_local_unattached": round(local / k, 3), "median_attached_wikis": float(np.median(nw)) if nw else None}
    res["profiles"] = {"cross_wiki_term_accounts": facts([a for a, s in langs_of.items() if len(s) >= 2]),
                       "single_language_term_accounts": facts([a for a, s in langs_of.items() if len(s) == 1])}
    return res


# ------------------------------------------------------------------ C2 synchrony
def event_table(pages, langs, concepts):
    rows = []
    for p in pages:
        for e in p.events:
            if e["exact"] and reg(e):
                rows.append({"u": e["u"], "lang": p.lang, "concept": p.concept, "family": e["family"], "kind": e["kind"],
                             "t": ep(e["t"]), "creation": bool(e.get("creation"))})
    return rows


class Sync:
    def __init__(self, rows, langs, concepts, tend):
        self.rows = rows
        self.t = np.array([r["t"] for r in rows], float)
        us = sorted({r["u"] for r in rows}); ui = {u: i for i, u in enumerate(us)}
        self.acc = np.array([ui[r["u"]] for r in rows], np.int64)
        self.lang = np.array([langs.index(r["lang"]) for r in rows], np.int64)
        self.con = np.array([concepts.index(r["concept"]) for r in rows], np.int64)
        self.grp = np.array([FAMILIES.index(r["family"]) * 2 + (r["kind"] == "insert") for r in rows], np.int64)
        self.cgrp = self.con * 100 + self.grp                    # campaign clusters: same article, family and direction
        self.tl = self.acc * len(langs) + self.lang              # account-language timeline id
        self.span = (T0, max(tend, float(self.t.max()) if len(self.t) else tend))
        self.langs = langs

    def shifted(self, rng, lo, hi):
        k = rng.uniform(lo, hi, size=int(self.tl.max()) + 1 if len(self.tl) else 1) * rng.choice([-1, 1], size=int(self.tl.max()) + 1 if len(self.tl) else 1)
        a, b = self.span
        return a + np.mod(self.t + DAY * k[self.tl] - a, b - a)

    def pairs(self, t, W):
        n = len(t)
        if n < 2:
            return 0, 0, 0
        key = self.grp * 1e10 + t
        o = np.argsort(key, kind="stable"); ks = key[o]
        je = np.searchsorted(ks, ks + W, side="right")
        cnt = je - np.arange(n) - 1
        tot = int(cnt.sum())
        if tot == 0:
            return 0, 0, 0
        I = np.repeat(np.arange(n), cnt)
        J = np.arange(tot) - np.repeat(np.cumsum(cnt) - cnt, cnt) + I + 1
        I, J = o[I], o[J]
        dl = self.lang[I] != self.lang[J]
        sa = self.acc[I] == self.acc[J]
        return int((dl & sa).sum()), int((dl & ~sa).sum()), int((dl & ~sa & (self.con[I] == self.con[J])).sum())

    def clusters(self, t, best_only=False):
        """Windows of CAMPAIGN_W holding events of one article + family + direction in >= CAMPAIGN_MIN_LANGS languages."""
        out, best = [], None
        for g in np.unique(self.cgrp):
            idx = np.where(self.cgrp == g)[0]
            idx = idx[np.argsort(t[idx])]
            ts = t[idx]
            je = np.searchsorted(ts, ts + CAMPAIGN_W, side="right")
            for i in range(len(idx)):
                if je[i] - i < CAMPAIGN_MIN_LANGS:
                    continue
                mem = idx[i:je[i]]
                nl = len(set(self.lang[mem].tolist()))
                if nl < CAMPAIGN_MIN_LANGS:
                    continue
                sc = (nl, len(set(self.acc[mem].tolist())), -(ts[je[i] - 1] - ts[i]))
                if best is None or sc > best:
                    best = sc
                if not best_only:
                    out.append((sc, frozenset(mem.tolist())))
        if best_only:
            return best
        keep = []
        for sc, m in sorted(out, key=lambda x: (-len(x[1]), x[0])):
            if not any(m <= k for _, k in keep):
                keep.append((sc, m))
        return keep


def synchrony(rows, langs, concepts, tend, rng, n=1000):
    S = Sync(rows, langs, concepts, tend)
    res = {"events": len(rows), "accounts": len(set(S.acc.tolist())), "windows": {}}
    for w, (sec, (lo, hi)) in SYNC_W.items():
        o = S.pairs(S.t, sec)
        nl = [S.pairs(S.shifted(rng, lo, hi), sec) for _ in range(n)]
        res["windows"][w] = {"same_account_cross_language_pairs": nstat([x[0] for x in nl], o[0]),
                             "cross_account_cross_language_pairs": nstat([x[1] for x in nl], o[1]),
                             "cross_account_same_article_pairs": nstat([x[2] for x in nl], o[2]),
                             "null": f"each account-language timeline shifted by a random {lo}-{hi} days (either sign, wrapped)"}
    obs = S.clusters(S.t)
    null_best = [S.clusters(S.shifted(rng, *CAMPAIGN_SHIFT), best_only=True) for _ in range(n)]
    null_counts = []
    for _ in range(min(n, 200)):
        null_counts.append(len(S.clusters(S.shifted(rng, *CAMPAIGN_SHIFT))))
    cl = []
    for sc, m in sorted(obs, key=lambda x: x[0], reverse=True):
        m = sorted(m)
        p = (sum(1 for b in null_best if b is not None and b >= sc) + 1) / (n + 1)
        nacc = sc[1]
        conf = "high" if p <= 0.002 and nacc >= 2 else "medium" if p <= 0.01 and nacc >= 2 else "low"
        r0 = rows[m[0]]
        cl.append({"family": r0["family"], "direction": r0["kind"], "languages": sorted({rows[i]["lang"] for i in m}),
                   "n_languages": sc[0], "n_accounts": nacc, "events": len(m), "span_hours": round(-sc[2] / HOUR, 1),
                   "articles": sorted({rows[i]["concept"] for i in m}), "first": iso(min(rows[i]["t"] for i in m))[:10],
                   "creations": sum(rows[i]["creation"] for i in m),
                   "p_selection_calibrated": round(p, 4), "confidence": conf, "_m": sorted({int(S.acc[i]) for i in m}),
                   "_u": sorted({rows[i]["u"] for i in m})})
    res["campaigns"] = {"clusters": cl[:40], "n_clusters": len(cl),
                        "expected_clusters_by_chance": round(float(np.mean(null_counts)), 2) if null_counts else None,
                        "null_p95_clusters": float(np.percentile(null_counts, 95)) if null_counts else None,
                        "p_count": p_hi(null_counts, len(cl)) if null_counts else None,
                        "flagged": sum(1 for c in cl if c["confidence"] in ("high", "medium")),
                        "null": f"timelines shifted {CAMPAIGN_SHIFT[0]}-{CAMPAIGN_SHIFT[1]} days; each cluster's score (languages, "
                                "accounts, tightness) against the best cluster of every null world"}
    return res


# ------------------------------------------------------------------ C3 network (article + talk co-activity)
def engine_events(rows):
    return [{"u": r["u"], "title": f"{r['concept']} [{r['lang']}]", "group": "crosswiki", "t": r["t"], "kind": r["kind"],
             "revid": i, "terms": [r["family"]], "age_d": r.get("age_d"), "village": False, "lang": r["lang"]}
            for i, r in enumerate(rows)]


def label_map(E, net):
    """Reproduce analyze_coord.network's A1.. labels: node order = (community, -events), ties in graph insertion order."""
    order_nodes = []
    seen = set()
    for _, pid, _ in E.edges("network"):
        for a in (pid // E.NA, pid % E.NA):
            if a not in seen:
                seen.add(a); order_nodes.append(int(a))
    cid = {a: c["id"] for c in net["communities"] for a in c["_m"]}
    ev_n = Counter(int(a) for a in E.acc)
    order = sorted(order_nodes, key=lambda a: (cid[a], -ev_n[a]))
    lab = {a: f"A{k + 1}" for k, a in enumerate(order)}
    for nd, a in zip(net["nodes"], order):
        assert nd["id"] == lab[a] and nd["events"] == ev_n[a], "label reconstruction mismatch"
    return lab


def unit_lang(u):
    return u.rsplit("[", 1)[1].rstrip("]")


def edge_languages(E, a, b, window=1800):
    ia, ib = np.where(E.acc == a)[0], np.where(E.acc == b)[0]
    langs, cross = set(), False
    for x in ia:
        dt = np.abs(E.t[ib] - E.t[x])
        for y in ib[(dt <= window) & (E.art[ib] != E.art[x])]:
            la, lb = unit_lang(E.arts[E.art[x]]), unit_lang(E.arts[E.art[y]])
            langs |= {la, lb}; cross = cross or la != lb
    shared = E.rows[a] & E.rows[b]
    sl = {unit_lang(E.arts[m]) for m in shared}
    langs |= sl
    cross = cross or len(sl) >= 2
    return sorted(langs), cross


def talk_rows(pages, multi_accounts):
    rows, seen = [], set()
    for p in pages:
        for x in p.r.get("talk") or []:
            if not reg(x) or x["u"] not in multi_accounts:
                continue
            t = ep(x["t"])
            k = (x["u"], p.lang, p.concept, int(t // HOUR))
            if k in seen:
                continue
            seen.add(k)
            rows.append({"u": x["u"], "concept": "Talk: " + p.concept, "lang": p.lang, "t": t, "kind": "talk", "family": "talk"})
    return rows


_CURVEBALL = AC.curveball


def stratified_curveball(strata):
    """analyze_coord.curveball run inside each language: an account keeps its number of units per language and every unit its
    number of accounts, so the null never moves an editor into an edition they do not edit (language locality is not
    mistaken for a bloc). Same output format (flat arrays in row order) as analyze_coord.curveball."""
    def cb(rows, n, rng, thin=None, burn=None):
        rows = [set(r) for r in rows]
        groups = sorted(set(strata.values()))
        gens, subs = [], []
        for g in groups:
            sub = [{x for x in r if strata[x] == g} for r in rows]
            subs.append([len(x) for x in sub])
            gens.append(_CURVEBALL(sub, n, rng, thin, burn))
        for _ in range(n):
            parts = [[] for _ in rows]
            for gen, deg in zip(gens, subs):
                flat = next(gen); off = 0
                for i, d in enumerate(deg):
                    parts[i] += flat[off:off + d].tolist(); off += d
            yield np.fromiter((x for r in parts for x in sorted(r)), dtype=np.int32, count=sum(len(r) for r in parts))
    return cb


def run_engine(ev, name, n_null, n_calib, seed, log):
    E = AC.Engine(ev, name, n_null, n_calib, seed=seed)
    strata = {i: unit_lang(a) for i, a in enumerate(E.arts)}
    AC.curveball = stratified_curveball(strata)
    try:
        return E.run(log)
    finally:
        AC.curveball = _CURVEBALL


def networks(rows, pages, langs, n_null, n_calib, seed, log=print):
    D0 = {"revisions": []}
    out = {}
    ev = engine_events(rows)
    if len({e["u"] for e in ev}) < 3:
        return {"nodes": [], "edges": [], "communities": [], "counts": {}}, None, None, {}
    E = run_engine(ev, "crosswiki/terms", n_null, n_calib, seed, log)
    eba = defaultdict(list)
    for e in ev:
        eba[E.ai[e["u"]]].append(e)
    net = AC.network(E, D0, eba, log)
    bl = AC.blocs(E, D0, eba)
    lab = label_map(E, net) if net["nodes"] else {}
    all_langs = defaultdict(set)
    for p in pages:
        for x in list(p.revs) + list(p.r.get("talk") or []):
            if reg(x):
                all_langs[x["u"]].add(p.lang)
    inv = {v: k for k, v in lab.items()}
    for nd in net["nodes"]:
        a = inv[nd["id"]]
        nd["languages"] = sorted(all_langs.get(E.accs[a], set()))
        nd["term_languages"] = sorted({e["lang"] for e in eba[a]})
    edges = E.edges("network")
    for ed, (i, pid, sig) in zip(net["edges"], edges):
        ls, cross = edge_languages(E, pid // E.NA, pid % E.NA)
        ed.update({"edge_type": "terms", "languages": ls, "cross_language": cross})
    for c in net["communities"]:
        c["languages"] = sorted({l for a in c["_m"] for l in {e["lang"] for e in eba[a]}})
    # talk co-activity (second edge type): accounts active in 2+ languages
    multi = {u for u, s in all_langs.items() if len(s) >= 2}
    tr = talk_rows(pages, multi)
    talk_edges, talk_counts = [], {"accounts": len({r["u"] for r in tr}), "events": len(tr)}
    if len({r["u"] for r in tr}) >= 3:
        E2 = run_engine(engine_events(tr), "crosswiki/talk", n_null, min(n_calib, 50), seed + 1, log)
        nxt = len(lab)
        h2l = {E.accs[a]: l for a, l in lab.items()}
        for i, pid, sig in E2.edges("network"):
            ps = E2.pair_stats(i)
            main = AC.DEFAULT_W if AC.DEFAULT_W in sig else "shared"
            m = ps[main]
            ends = []
            for a in (pid // E2.NA, pid % E2.NA):
                h = E2.accs[a]
                if h not in h2l:
                    nxt += 1; h2l[h] = f"A{nxt}"
                    net["nodes"].append({"id": h2l[h], "events": 0, "articles": 0, "insert_share": None, "community": None,
                                         "age_bucket": "unknown", "languages": sorted(all_langs.get(h, set())), "term_languages": [],
                                         "talk_only": True})
                ends.append(h2l[h])
            ls, cross = edge_languages(E2, pid // E2.NA, pid % E2.NA)
            talk_edges.append({"source": ends[0], "target": ends[1], "edge_type": "talk",
                               "weight": round(math.log2((m["observed"] + 1) / (m["null_mean"] + 1)), 3), "basis": main,
                               "significant_on": sig, "observed": m["observed"], "null_mean": m["null_mean"], "null_p95": m["null_p95"],
                               "p": m["p"], "windows": {k: ps[k] for k in AC.WINDOWS}, "shared_articles": ps["shared"],
                               "languages": ls, "cross_language": cross})
        talk_counts.update({"edges": len(talk_edges), "expected_by_chance": E2.calib_counts("network")})
        term_pairs = {tuple(sorted((e["source"], e["target"]))) for e in net["edges"]}
        talk_counts["also_term_edge"] = sum(1 for e in talk_edges if tuple(sorted((e["source"], e["target"]))) in term_pairs)
    net["edges"] += talk_edges
    net["counts"]["talk"] = talk_counts
    net["counts"]["cross_language_term_edges"] = sum(1 for e in net["edges"] if e["edge_type"] == "terms" and e["cross_language"])
    net["counts"]["cross_language_talk_edges"] = sum(1 for e in talk_edges if e["cross_language"])
    return net, bl, E, eba


# ------------------------------------------------------------------ narrative traces (N1-N4)
def at_dates(p, dates):
    return {d: p.feat_at(ep(d + "T00:00:00Z")) for d in dates}


def narrative(pages, langs, tend):
    now = iso(tend)[:10]
    dates = ["2021-01-01", "2023-10-06", "2024-10-07", now]
    hamas, hostages, o7, court = {}, {}, {}, {}
    for p in pages:
        if p.concept == "Hamas":
            snap = {}
            for d, f in at_dates(p, dates).items():
                snap[d] = None if not f else {"terror_sentence": (f["tr"] + 1) if "tr" in f else None, "sentences": f["n"]}
            moves = []
            prev = None
            for t, f in p.ft:
                v = (f["tr"] + 1) if "tr" in f else None
                if v != prev:
                    moves.append({"date": iso(t)[:10], "terror_sentence": v, "sentences": f["n"]}); prev = v
            hamas[p.lang] = {"at": snap, "changes": len(moves) - 1 if moves else 0, "timeline": moves[-12:]}
        if p.concept in ("October 7 attacks", "Gaza war", "Hamas", "Israel"):
            snap = {}
            for d, f in at_dates(p, dates).items():
                snap[d] = None if not f else {"mentions": (f.get("hg") or [0])[0],
                                               "first_sentence": (f["hg"][1] + 1) if f.get("hg") else None, "sentences": f["n"]}
            hostages.setdefault(p.lang, {})[p.concept] = snap
        if p.concept == "October 7 attacks":
            tl, prev = [], None
            for t, f in p.ft:
                v = f.get("o7") or []
                if v != prev:
                    tl.append({"date": iso(t)[:10], "first_sentence_names": v}); prev = v
            o7[p.lang] = {"now": (p.ft[-1][1].get("o7") if p.ft else None), "timeline": tl[-12:],
                          "renames": [{"date": (m["ts"] or "")[:10], "from": m["from"], "to": m["to"]} for m in p.r.get("moves") or []]}
        for t, f in p.ft:
            for flag in f.get("ct") or []:
                c = court.setdefault(p.lang, {}).setdefault(flag, {"articles": set(), "first": t, "last": t, "now": False})
                c["articles"].add(p.concept); c["first"] = min(c["first"], t); c["last"] = max(c["last"], t)
        if p.ft:
            for flag in p.ft[-1][1].get("ct") or []:
                court[p.lang][flag]["now"] = True
    court_out = {l: {k: {"articles": sorted(v["articles"]), "first_seen": iso(v["first"])[:10], "last_seen": iso(v["last"])[:10],
                         "in_lead_now": v["now"], "what_the_court_said": COURT_SAID[k]} for k, v in d.items()} for l, d in court.items()}
    return {"hamas_terror_sentence": hamas, "hostages": hostages, "october7_naming": o7, "court_overstatement": court_out}


# ------------------------------------------------------------------ S1 sources at insertion
def sources(pages, tend, rng, n=2000):
    items = []
    for p in pages:
        rem = defaultdict(list)
        for e in p.events:
            if e["kind"] == "remove":
                rem[e["family"]].append(ep(e["t"]))
        for e in p.events:
            if e["kind"] != "insert" or not e.get("refs"):
                continue
            t = ep(e["t"])
            nxt = min([x for x in rem[e["family"]] if x > t], default=None)
            if (nxt is not None and nxt - t < 30 * DAY) or e.get("reverted"):
                fate = "reverted"
            elif (nxt or tend) - t >= 30 * DAY:
                fate = "stuck"
            else:
                fate = "censored"
            items.append({"lang": p.lang, "fate": fate, "new": e["refs"]["n_new"], "doms": e["refs"]["new_domains"],
                          "before": e["refs"].get("classes_before") or {}})
    arrive, stock = Counter(), Counter()
    for it in items:
        for d in it["doms"]:
            arrive[EX.classify(d) or "Other"] += 1
        for k, v in it["before"].items():
            stock[k] += v
    lab = [it for it in items if it["fate"] in ("stuck", "reverted")]
    y = np.array([it["new"] > 0 for it in lab], bool); g = np.array([it["fate"] == "stuck" for it in lab], bool)
    res = {"insertions_with_source_data": len(items), "share_with_new_source": round(float(np.mean([it["new"] > 0 for it in items])), 3) if items else None,
           "arriving_classes": dict(arrive.most_common()), "classes_already_in_lead": dict(stock.most_common()),
           "by_language": {l: {"insertions": sum(1 for it in items if it["lang"] == l),
                               "share_with_new_source": round(float(np.mean([it["new"] > 0 for it in items if it["lang"] == l])), 3)}
                           for l in sorted({it["lang"] for it in items})}}
    if g.any() and (~g).any():
        diff = float(y[g].mean() - y[~g].mean())
        nd = []
        for _ in range(n):
            gg = rng.permutation(g)
            nd.append(float(y[gg].mean() - y[~gg].mean()))
        res["stuck_vs_reverted"] = {"stuck": int(g.sum()), "reverted": int((~g).sum()),
                                    "share_new_source_stuck": round(float(y[g].mean()), 3),
                                    "share_new_source_reverted": round(float(y[~g].mean()), 3),
                                    "difference": round(diff, 3), "expected_difference_by_chance": round(float(np.mean(nd)), 3),
                                    "null_p95": round(float(np.percentile(nd, 95)), 3), "p": p_hi(nd, diff),
                                    "expected_stuck_with_new_source_by_chance": round(float(y.mean() * g.sum()), 1)}
    return res


# ------------------------------------------------------------------ R1 RfC settle vs attrition
def rfc_settle(pages, tend, rng, n=10000):
    en = [p for p in pages if p.lang == "en" and p.r.get("rfc")]
    sticks, closes_by_concept = [], defaultdict(list)
    n_items = Counter()
    for p in en:
        items = p.r["rfc"]["items"]
        for d in items:
            n_items[(d["kind"], bool(d.get("closed_at")))] += 1
        closes = sorted(ep(d["closed_at"]) for d in items if d.get("closed_at"))
        closes_by_concept[p.concept] += closes
        span = (T0, tend - STICK_D * DAY)
        for f in FAMILIES:
            ev = sorted((e for e in p.events if e["family"] == f), key=lambda e: e["t"])
            if not ev:
                continue
            last = ev[-1]; t = ep(last["t"])
            if t > span[1]:
                continue
            failed = sum(1 for a, b in zip(ev, ev[1:]) if a["kind"] == last["kind"] and b["kind"] != a["kind"]
                         and ep(b["t"]) - ep(a["t"]) < 30 * DAY and ep(a["t"]) > t - 365 * DAY)
            after = any(0 <= t - c <= SETTLE_D * DAY for c in closes)
            # chance that a random date in the span falls within SETTLE_D days after one of this page's closes
            cov = 0.0
            if closes:
                iv = sorted((max(span[0], c), min(span[1], c + SETTLE_D * DAY)) for c in closes)
                cur = None
                for a, b in iv:
                    if b <= a:
                        continue
                    if cur and a <= cur[1]:
                        cur[1] = max(cur[1], b)
                    else:
                        if cur:
                            cov += cur[1] - cur[0]
                        cur = [a, b]
                if cur:
                    cov += cur[1] - cur[0]
            sticks.append({"article": p.concept, "family": f, "kind": last["kind"], "date": iso(t)[:10], "after_close": after,
                           "failed_attempts_before": failed, "p_window": cov / (span[1] - span[0])})
    k = sum(s["after_close"] for s in sticks)
    pw = np.array([s["p_window"] for s in sticks])
    sim = (rng.random((n, len(pw))) < pw).sum(axis=1) if len(pw) else np.zeros(n)
    # other languages: same article + family moves within SETTLE_D days after an English close
    oth, exp = 0, 0.0
    for p in pages:
        if p.lang == "en":
            continue
        closes = closes_by_concept.get(p.concept) or []
        span_p = (max(T0, ep(p.created) if p.created else T0), tend)
        frac = min(1.0, sum(min(span_p[1], c + SETTLE_D * DAY) - max(span_p[0], c) for c in closes
                            if min(span_p[1], c + SETTLE_D * DAY) > max(span_p[0], c)) / max(1.0, span_p[1] - span_p[0]))
        for e in p.events:
            if e["exact"]:
                t = ep(e["t"]); oth += any(0 <= t - c <= SETTLE_D * DAY for c in closes); exp += frac
    return {"rfc_rm_items": {f"{a}_{'closed_dated' if b else 'open_or_undated'}": v for (a, b), v in n_items.items()},
            "sticks": len(sticks), "settled_within_30d_after_close": nstat(sim, k),
            "by_attrition": sum(1 for s in sticks if not s["after_close"] and s["failed_attempts_before"] > 0),
            "no_close_no_failed_attempts": sum(1 for s in sticks if not s["after_close"] and s["failed_attempts_before"] == 0),
            "stick_list": sticks,
            "other_language_moves_within_30d_after_english_close": {"observed": oth, "expected_by_chance": round(exp, 2)}}


# ------------------------------------------------------------------ K1 / L1 / V1 / W1
def creation(pages, langs, concepts):
    out = {}
    for c in concepts:
        row = {}
        for p in pages:
            if c in p.concepts and p.created:
                if p.lang not in row or p.created < row[p.lang]:
                    row[p.lang] = p.created
        en = row.get("en")
        out[c] = {l: {"created": v[:10], "days_after_english": round((ep(v) - ep(en)) / DAY) if en and l != "en" else None}
                  for l, v in sorted(row.items(), key=lambda x: x[1])}
    return out


def logs(pages):
    out = {}
    for p in pages:
        prot = p.r.get("protection") or []
        since = [e for e in prot if (e["ts"] or "") >= "2021"]
        last = next((e for e in reversed(prot) if e["action"] in ("protect", "modify", "unprotect")), None)
        out.setdefault(p.lang, {})[p.title] = {
            "article": p.concept, "renames": [{"date": (m["ts"] or "")[:10], "from": m["from"], "to": m["to"]} for m in p.r.get("moves") or []],
            "protection_actions_since_2021": len(since),
            "protection_dates": [{"date": (e["ts"] or "")[:10], "action": e["action"],
                                  "levels": sorted({f"{d['type']}={d['level']}" for d in e["details"]})} for e in since][-15:],
            "last_protection": None if not last else {"date": (last["ts"] or "")[:10], "action": last["action"],
                                                       "levels": sorted({f"{d['type']}={d['level']}" for d in last["details"]})}}
    return out


def exposure(pages, langs):
    """Views (monthly, user agent) that met each family in the lead, by voice, per language; before and after 7 Oct 2023."""
    out = {}
    for l in langs:
        acc = {per: {f: Counter() for f in FAMILIES} for per in ("before_war", "after_war")}
        tot = Counter()
        for p in pages:
            if p.lang != l:
                continue
            for mo, v in ((p.r.get("views") or {}).get("monthly") or {}).items():
                t = ep(f"{mo[:4]}-{mo[4:6]}-15T00:00:00Z")
                per = "after_war" if t >= WAR else "before_war"
                tot[per] += v
                s = p.state_at(t)
                for k, f in enumerate(FAMILIES):
                    acc[per][f]["own_voice" if s and s[k] == "2" else "attributed" if s and s[k] == "1" else "absent_or_unknown"] += v
        out[l] = {per: {"views_m": round(tot[per] / 1e6, 2), **{f: {k: round(v / tot[per], 4) if tot[per] else None for k, v in acc[per][f].items()}
                                               for f in FAMILIES}} for per in acc}
    return out


def wikidata_traces(D, langs):
    wd = D.get("wikidata") or {}
    qinv = {q: c for c, q in (D.get("qids") or {}).items()}
    out = {}
    for q, ch in (wd.get("changes") or {}).items():
        c = qinv.get(q, "?")
        per = {}
        for l in langs:
            x = [e for e in ch if e["lang"] == l]
            d = [e for e in x if e["field"] == "description"]
            per[l] = {"description_changes": len(d), "label_changes": sum(1 for e in x if e["field"] == "label"),
                      "bulk_changes_value_not_shown": sum(1 for e in x if e["action"] == "bulk"),
                      "description_changes_after_war": sum(1 for e in d if e["ts"] >= "2023-10-07"),
                      "description_history": [{"date": e["ts"][:10], "value": e["value"]} for e in d][-8:],
                      "description_now": ((wd.get("current") or {}).get(q) or {}).get("descriptions", {}).get(l),
                      "label_now": ((wd.get("current") or {}).get(q) or {}).get("labels", {}).get(l)}
        out[c] = per
    return out


# ------------------------------------------------------------------ main analysis
def analyze_data(D, n_null=1000, n_calib=200, seed=7, log=print):
    rng = np.random.default_rng(seed)
    langs, concepts = D["langs"], D["concepts"]
    pages = load_pages(D)
    tend = t_end(pages)
    acc = D.get("accounts") or {}
    R = {"meta": {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "null_draws": n_null, "calibration_worlds": n_calib,
                  "collection": D.get("summary"), "pages": len(pages), "end": iso(tend)[:10]}}
    log("T1 diffusion"); R["diffusion"] = diffusion(pages, langs, concepts, rng, n_null)
    log("T2 voice"); R["voice"] = voice_paths(pages, langs)
    log("T3 trend"); R["trend"], R["trend_series"] = trend(pages, langs, concepts, rng, n_null)
    log("C1 accounts"); R["accounts"] = cross_accounts(pages, langs, concepts, D, rng, n_null)
    rows = event_table(pages, langs, concepts)
    for r in rows:
        f = acc.get(r["u"]) or {}
        r["age_d"] = int((r["t"] - ep(f["reg"] + "-01T00:00:00Z")) / DAY) if f.get("reg") else None
    log("C2 synchrony"); R["sync"] = synchrony(rows, langs, concepts, tend, rng, n_null)
    log("C3 network")
    net, bl, E, eba = networks(rows, pages, langs, n_null, n_calib, seed, log)
    R["network"], R["blocs"] = net, bl
    log("C4 windows")
    win = {}
    if E is not None:
        tl = defaultdict(set)
        for e in E.ev:
            tl[E.ai[e["u"]]].add(e["lang"])
        cw = [a for a, s in tl.items() if len(s) >= 2]
        if len(cw) >= 3 and len(cw) < E.NA:
            win["cross_wiki_term_accounts"] = {"size": len(cw), **AC.window_alignment(E, cw, rng)}
        for c in net["communities"]:
            if c["size"] >= AC.MIN_BLOC:
                win[f"community {c['id']}"] = {"size": c["size"], "confidence": c["confidence"], **AC.window_alignment(E, c["_m"], rng)}
        for k, c in enumerate(R["sync"]["campaigns"]["clusters"]):
            if c["confidence"] in ("high", "medium"):
                m = [E.ai[u] for u in c["_u"] if u in E.ai]
                if m and len(m) < E.NA:
                    win[f"campaign cluster {k + 1}"] = {"size": len(m), **AC.window_alignment(E, m, rng)}
    R["windows"] = win
    log("narrative / sources / RfC / logs / views / wikidata")
    R["narrative"] = narrative(pages, langs, tend)
    R["sources"] = sources(pages, tend, rng)
    R["rfc"] = rfc_settle(pages, tend, rng)
    R["creation"] = creation(pages, langs, concepts)
    R["logs"] = logs(pages)
    R["exposure"] = exposure(pages, langs)
    R["wikidata"] = wikidata_traces(D, langs)
    return R


# ------------------------------------------------------------------ cards
LANG_NAME = {"en": "English", "he": "Hebrew", "ar": "Arabic", "es": "Spanish", "fr": "French", "de": "German", "ru": "Russian",
             "it": "Italian", "pt": "Portuguese", "nl": "Dutch", "pl": "Polish"}
NOT_DETECTED = ("'Not detected' means our tests found nothing beyond chance; with few events the tests have little power, "
                "so it is not proof that it did not happen.")


def build_cards(R):
    cards = []
    m = R["meta"]; col = m.get("collection") or {}
    cards.append(card("cw_data", "What the cross-wiki tier covers",
                      f"{col.get('pages', m['pages'])} language editions of the key articles ({col.get('by_lang')}), "
                      f"{col.get('revisions')} article revisions and {col.get('talk_revisions')} talk revisions since 2021; "
                      f"{col.get('events')} term events ({col.get('exact_events')} pinned to an exact revision). One run-wide "
                      "pseudonymous ID per account across all wikis.", "descriptive",
                      {"draws": m["null_draws"], "calibration_worlds": m["calibration_worlds"], "expected_by_chance": "n/a"},
                      "Everything below is measured on the opening sections of these pages.",
                      "Term detection is a word list per language (attribution by marker words); it misses paraphrase.",
                      numbers={"collection": col}))
    # T1
    d = R["diffusion"]
    ld = sorted(d["leader"].items(), key=lambda x: -x[1]["first_in_cells"])
    top = ld[0] if ld else None
    ef = d["english_first_share"]; fw = d["follow_within_90d_share"]
    cards.append(card("T1", f"Who said it first: {LANG_NAME.get(top[0], top[0]) if top else 'n/a'} led most often" if top else "Diffusion",
                      f"In {d['cells_with_2plus_dated']} article-term cells where 2+ editions added the term after 2021, the first mover "
                      f"was {', '.join(f'{LANG_NAME.get(l, l)} {v['first_in_cells']} (chance {v['expected_by_chance']})' for l, v in ld[:5])}. "
                      f"English moved before the other edition in {pct(ef['observed'])} of {d['pairs_with_english']} pairs "
                      f"(chance {pct(ef['expected_by_chance'])}, p={ef['p_high']}); {pct(fw['observed'])} followed English within 90 days "
                      f"(chance {pct(fw['expected_by_chance'])}, p={fw['p_high']}). In {d['english_had_it_before_2021_other_entered_later']} "
                      "more cases English already had the term before 2021 and the other edition added it later.",
                      conf_p(min(x for x in (ef["p_high"], fw["p_high"]) if x is not None) if (ef["p_high"] or fw["p_high"]) else None,
                             d["pairs_with_english"]),
                      {"null": "each language's entry dates permuted across the cells where it has one (keeps each edition's "
                               "general timing; breaks the link to the specific article and term)",
                       "expected_english_first_share": ef["expected_by_chance"], "expected_follow90_share": fw["expected_by_chance"]},
                      "A systematic leader is the edition the others follow; a short follow lag is consistent with copying or translation.",
                      "First entry only; a term can enter and leave many times. Pages created after 2021 count their creation as entry.",
                      numbers={k: v for k, v in d.items() if k != "cells"}, chart="chart_data/diffusion.json"))
    # T2
    v = R["voice"]
    a2s = {l: x["paths"].get("attributed_then_own_voice", 0) for l, x in v.items()}
    cards.append(card("T2", "From 'accused of' to fact: where the encyclopedia's own voice took over",
                      "Article-term paths from attributed to own voice: " + ", ".join(
                          f"{LANG_NAME.get(l, l)} {n} (median {v[l]['attributed_to_own_voice_median_days']} d)" for l, n in
                          sorted(a2s.items(), key=lambda x: -x[1]) if n) + ". Own-voice transitions after 7 Oct 2023 vs expected from "
                      "editing activity: " + ", ".join(f"{LANG_NAME.get(l, l)} {x['after_war']}/{x['to_own_voice_transitions']} "
                                                       f"(chance {x['expected_after_war_by_activity']}, p={x['p_high']})"
                                                       for l, x in v.items() if x["to_own_voice_transitions"]),
                      conf_p(min([x["p_high"] for x in v.values() if x["p_high"] is not None] or [1]),
                             sum(x["to_own_voice_transitions"] for x in v.values())),
                      {"null": "transitions spread like the language's revisions (binomial on the after-war share of revisions)",
                       "expected_after_war": {l: x["expected_after_war_by_activity"] for l, x in v.items()}},
                      "Moving a charge from someone's mouth into the encyclopedia's voice is the strongest framing change.",
                      "Voice = a term sentence without an attribution word of that language (a marker heuristic, not a coded reading). "
                      "English key articles from ratchet carry voice only at event revisions.",
                      numbers=v, chart="chart_data/voice.json"))
    # T3
    t = R["trend"]; en = t.get("en", {})
    cards.append(card("T3", "After 7 October: which editions moved with English",
                      "Article-term cells present on 6 Oct 2023 -> now: " + ", ".join(
                          f"{LANG_NAME.get(l, l)} {x['cells_present_6oct2023']}->{x['cells_present_now']}" for l, x in t.items()) +
                      ". Insertions after the war vs expected from editing activity: " + ", ".join(
                          f"{LANG_NAME.get(l, l)} {x['insertions_after_war']['observed']} (chance {x['insertions_after_war']['expected_by_chance']})"
                          for l, x in t.items() if x.get("insertions_after_war")),
                      conf_p(min([x["insertions_after_war"]["p"] for x in t.values() if x.get("insertions_after_war")] or [1]),
                             sum(x["insertions"] for x in t.values())),
                      {"null": "each page's insertion events moved to random revisions of the same page (keeps its activity curve)",
                       "expected_after_war": {l: (x["insertions_after_war"] or {}).get("expected_by_chance") for l, x in t.items()}},
                      f"English gained {en.get('gained', 0)} and lost {en.get('lost', 0)} cells; 'net_gain_vs_english' compares each edition.",
                      "Cells are article x term family; presence anywhere in the opening section.",
                      numbers=t, chart="chart_data/trend_by_lang.json"))
    # C1
    a = R["accounts"]; s = a.get("same_article_2plus_languages") or {}
    ins, rem = a.get("insert") or {}, a.get("remove") or {}
    def fam(x):
        y = (x or {}).get("same_family_2plus_languages") or {}
        return f"{y.get('observed')} (chance {y.get('expected_by_chance')}, p={y.get('p')})"
    cards.append(card("C1", "The same accounts across editions",
                      f"{s.get('observed')} of {s.get('accounts')} accounts ({pct(s.get('share_of_all'))}) edited the same key article in "
                      f"2+ languages; chance {s.get('expected_by_chance')} (p={s.get('p')}). Accounts that inserted a term family in 2+ "
                      f"languages: {fam(ins)} of {ins.get('accounts')} inserters; removed in 2+ languages: {fam(rem)} of {rem.get('accounts')} removers.",
                      conf_p(min([x for x in (s.get("p"), (ins.get("same_family_2plus_languages") or {}).get("p"),
                                              (rem.get("same_family_2plus_languages") or {}).get("p")) if x is not None] or [1]),
                             ins.get("accounts", 0) + rem.get("accounts", 0)),
                      {"null": "within each language, accounts shuffled among accounts with the same activity (number of articles, "
                               "or families, in that language); multilingual accounts stay multilingual",
                       "expected_same_article": s.get("expected_by_chance"),
                       "expected_insert_same_family": (ins.get("same_family_2plus_languages") or {}).get("expected_by_chance"),
                       "expected_remove_same_family": (rem.get("same_family_2plus_languages") or {}).get("expected_by_chance")},
                      "Above chance means multilingual editors carry the same term across editions, not just edit in several.",
                      "Same username = same global (SUL) account; local accounts checked for every term-event account. " + NOT_DETECTED,
                      numbers=a, chart="chart_data/crosswiki_accounts.json"))
    # C2
    sy = R["sync"]; w = sy["windows"]; cp = sy["campaigns"]
    cards.append(card("C2", "Same-day moves in different editions",
                      "; ".join(f"within {k}: same account {x['same_account_cross_language_pairs']['observed']} pairs (chance "
                                f"{x['same_account_cross_language_pairs']['expected_by_chance']}, p={x['same_account_cross_language_pairs']['p']}), "
                                f"different accounts {x['cross_account_cross_language_pairs']['observed']} (chance "
                                f"{x['cross_account_cross_language_pairs']['expected_by_chance']}, p={x['cross_account_cross_language_pairs']['p']})"
                                for k, x in w.items()) +
                      f". Clusters of one term moving in {CAMPAIGN_MIN_LANGS}+ editions of the same article within 48 h: {cp['n_clusters']} (chance "
                      f"{cp['expected_clusters_by_chance']}); flagged beyond the selection-calibrated null: {cp['flagged']}.",
                      "high" if any(c["confidence"] == "high" for c in cp["clusters"]) else
                      "medium" if cp["flagged"] else conf_p(min(x["cross_account_cross_language_pairs"]["p"] for x in w.values()), sy["events"]),
                      {"null": "account-language timelines shifted at random (1-7 d for 1 h, 3-21 d for 1 d, 14-90 d for 1 w); "
                               "clusters against the best cluster of each null world",
                       "expected": {k: x["cross_account_cross_language_pairs"]["expected_by_chance"] for k, x in w.items()},
                       "expected_clusters": cp["expected_clusters_by_chance"]},
                      "Synchrony across editions beyond chance is what coordination would look like.",
                      "News also synchronises editions (an ICJ ruling, a UN report): the time-shift null removes news timing too, so "
                      "a flagged cluster is a lead to read, not proof of coordination. " + NOT_DETECTED,
                      numbers=sy, chart="chart_data/sync.json"))
    # C3
    nc = (R["network"] or {}).get("counts") or {}
    sig = [c for c in (R["network"] or {}).get("communities") or [] if c.get("confidence") in ("high", "medium")]
    cards.append(card("C3", "Cross-wiki blocs",
                      f"{nc.get('accounts_tested')} accounts with term events; {nc.get('edges')} significant term co-activity edges "
                      f"(chance {((nc.get('expected_by_chance') or {}).get('edges_mean'))}), {nc.get('cross_language_term_edges')} of them "
                      f"across languages; talk co-activity edges {(nc.get('talk') or {}).get('edges')} (cross-language "
                      f"{nc.get('cross_language_talk_edges')}). Communities of 3+: {nc.get('communities_3plus')}, beyond chance: {len(sig)}.",
                      "high" if any(c["confidence"] == "high" for c in sig) else "medium" if sig else "low",
                      {"null": "analyze_coord engine with degree-preserving rewiring inside each language (shared article-language "
                               "units) and 1-7 d timeline shifts, "
                               "whole pipeline re-run on null worlds", "expected_by_chance": nc.get("expected_by_chance"),
                       "talk_expected_by_chance": (nc.get("talk") or {}).get("expected_by_chance")},
                      "A bloc that spans editions is the cross-wiki form of a canvassed group.",
                      "Nodes are A1, A2...; units are 'article [language]'. " + NOT_DETECTED,
                      numbers={"counts": nc, "communities": [{k: v for k, v in c.items() if k not in ("members",)} for c in (R["network"] or {}).get("communities") or []][:20]},
                      chart="chart_data/network_crosswiki.json"))
    # C4
    wn = R["windows"]
    best = None
    for k, x in wn.items():
        for wk, y in x["windows"].items():
            if best is None or y["p_high"] < best[2]["p_high"]:
                best = (k, wk, y)
    cards.append(card("C4", "Cross-wiki activity and the documented canvassing windows",
                      "; ".join(f"{k} ({x['size']} accounts): " + ", ".join(
                          f"{wk} {pct(y['window_share'])} of events (matched sets {pct(y['expected_window_share'])}, p={y['p_high']})"
                          for wk, y in x["windows"].items()) for k, x in wn.items()) or "No account set large enough to test.",
                      conf_p(best[2]["p_high"], 10) if best else "low",
                      {"null": "matched random account sets (same event counts), analyze_coord.window_alignment",
                       "expected": {k: {wk: y["expected_window_share"] for wk, y in x["windows"].items()} for k, x in wn.items()}},
                      "The windows are English-Wikipedia findings (ArbCom); here we ask whether cross-wiki activity clusters in them.",
                      "Windows overlap the war's busiest news months; matched sets share that background. " + NOT_DETECTED,
                      numbers=wn, chart="chart_data/windows.json"))
    # N1-N4
    nr = R["narrative"]
    hm = nr["hamas_terror_sentence"]; now = m["end"]
    def hpos(l):
        at = hm[l]["at"]; ks = sorted(at)
        a0, a1 = at.get(ks[0]), at.get(ks[-1])
        f = lambda x: "n/a" if not x else ("none" if x["terror_sentence"] is None else f"{x['terror_sentence']}/{x['sentences']}")
        return f"{LANG_NAME.get(l, l)} {f(a0)} -> {f(a1)}"
    cards.append(card("N1", "Hamas and 'terror': where the designation sits in each edition's opening",
                      "First sentence with a terror word, as sentence k of n (2021 -> now): " + "; ".join(hpos(l) for l in sorted(hm)) + ".",
                      "descriptive", {"null": "none (measurement)", "expected_by_chance": "n/a"},
                      "Moving the designation to the end of the opening changes what a skimming reader takes away.",
                      "Sentence split on . ! ? ؟; template text removed. Terror word list: terror/terreur/террор/טרור/ارهاب.",
                      numbers=hm, chart="chart_data/narrative.json"))
    hg = nr["hostages"]
    cards.append(card("N2", "The hostages in the opening sections",
                      "Hostage mentions now (count, first sentence) by edition: " + "; ".join(
                          f"{LANG_NAME.get(l, l)}: " + ", ".join(f"{c} {((x.get(now) or {}).get('mentions'))}"
                                                                for c, x in sorted(d.items())) for l, d in sorted(hg.items())) + ".",
                      "descriptive", {"null": "none (measurement)", "expected_by_chance": "n/a"},
                      "Whether the hostages appear at all, and how early, is a direct measure of whose suffering the opening foregrounds.",
                      "Word list per language (hostage / Geisel / otage / rehén / חטופים / رهائن / أسرى ...); «أسرى» also means prisoners.",
                      numbers=hg, chart="chart_data/narrative.json"))
    o7 = nr["october7_naming"]
    cards.append(card("N3", "How each edition names 7 October",
                      "First-sentence naming now: " + "; ".join(f"{LANG_NAME.get(l, l)} {', '.join(x['now'] or ['none'])}" for l, x in sorted(o7.items())) +
                      ". Renames: " + ("; ".join(f"{LANG_NAME.get(l, l)} {r['date']} '{r['from']}' -> '{r['to']}'" for l, x in sorted(o7.items())
                                                for r in x["renames"]) or "none since 2021") + ".",
                      "descriptive", {"null": "none (measurement)", "expected_by_chance": "n/a"},
                      "'Massacre', 'attack' and 'operation' tell three different stories of the same day.",
                      "Classes from a multilingual word list on the first sentence; the title comes from the move log.",
                      numbers=o7, chart="chart_data/narrative.json"))
    ct = nr["court_overstatement"]
    cards.append(card("N4", "Court rulings said more than the courts did",
                      ("; ".join(f"{LANG_NAME.get(l, l)}: " + ", ".join(f"{k} ({', '.join(v['articles'])}; {v['first_seen']} -> "
                                                                       f"{v['last_seen']}{', still in the lead' if v['in_lead_now'] else ''})"
                                                                       for k, v in d.items()) for l, d in sorted(ct.items()))
                       or "No overstatement pattern found in the opening sections.") + " What the courts said: " +
                      " | ".join(f"{k}: {v}" for k, v in COURT_SAID.items()),
                      "descriptive", {"null": "none (pattern flags)", "expected_by_chance": "n/a"},
                      "Turning a provisional order or a non-binding opinion into a finding is a factual error, not a framing choice.",
                      "Flags are the patterns in LANGS.md finding 7 plus an English equivalent; each hit needs a human read.",
                      numbers=ct, chart="chart_data/narrative.json"))
    # S1
    so = R["sources"]; sv = so.get("stuck_vs_reverted") or {}
    cards.append(card("S1", "What sources came in with the term",
                      f"{so['insertions_with_source_data']} insertions with section-0 references at both revisions; "
                      f"{pct(so['share_with_new_source'])} brought a new domain. Arriving classes: {so['arriving_classes']}. "
                      + (f"Insertions that stuck brought a new source {pct(sv['share_new_source_stuck'])} of the time vs "
                         f"{pct(sv['share_new_source_reverted'])} for reverted ones (difference {sv['difference']}, chance "
                         f"{sv['expected_difference_by_chance']}, p={sv['p']})." if sv else ""),
                      conf_p(sv.get("p"), sv.get("stuck", 0) + sv.get("reverted", 0), 20) if sv else "low",
                      {"null": "stuck / reverted labels permuted across insertions", "expected_difference": sv.get("expected_difference_by_chance"),
                       "expected_stuck_with_new_source": sv.get("expected_stuck_with_new_source_by_chance")},
                      "Whether a framing sticks because it is sourced, or because it is pushed, is the core fairness question.",
                      "Domains only (explore.SOURCE_CLASSES); citation templates without URLs count as no domain.",
                      numbers=so, chart="chart_data/sources.json"))
    # R1
    rf = R["rfc"]; st = rf["settled_within_30d_after_close"]
    cards.append(card("R1", "Settled by a formal discussion, or by attrition?",
                      f"Of {rf['sticks']} English wordings that stuck (term entered or left and stayed {STICK_D}+ days), {st['observed']} "
                      f"settled within {SETTLE_D} days after an RfC / move-request close (chance {st['expected_by_chance']}, p={st['p']}); "
                      f"{rf['by_attrition']} stuck after failed attempts with no close nearby. Other editions changed the same term within "
                      f"{SETTLE_D} days after an English close {rf['other_language_moves_within_30d_after_english_close']['observed']} times "
                      f"(chance {rf['other_language_moves_within_30d_after_english_close']['expected_by_chance']}).",
                      conf_p(st["p"], rf["sticks"], 8),
                      {"null": "stick dates uniform over 2021 -> now-90 d; each page's own close dates",
                       "expected_by_chance": st["expected_by_chance"]},
                      "A wording that settles right after a close was decided by the community's formal process.",
                      "Close date = first signature after the close template; undated or unclosed items are counted but not aligned.",
                      numbers={k: v for k, v in rf.items() if k != "stick_list"}, chart="chart_data/rfc.json"))
    # K1 / L1 / V1 / W1
    cr = R["creation"]
    gg = cr.get("Gaza genocide") or {}
    cards.append(card("K1", "When each edition opened a 'Gaza genocide' article",
                      "Gaza genocide: " + ", ".join(f"{LANG_NAME.get(l, l)} {x['created']}" + (f" (+{x['days_after_english']} d)" if x["days_after_english"] is not None else "")
                                                   for l, x in gg.items()) + ". Editions without one have no page in the data.",
                      "descriptive", {"null": "none (dates)", "expected_by_chance": "n/a"},
                      "Opening a dedicated article is itself a framing decision.",
                      "Creation = first revision of the current page (its history follows renames).",
                      numbers=cr, chart="chart_data/creation.json"))
    lg = R["logs"]
    cards.append(card("L1", "Renames and protection",
                      "Renames since 2021: " + ("; ".join(f"{LANG_NAME.get(l, l)} {r['date']} '{r['from']}' -> '{r['to']}'"
                                                          for l, d in sorted(lg.items()) for x in d.values() for r in x["renames"]) or "none") +
                      ". Protection actions since 2021 per edition: " + ", ".join(
                          f"{LANG_NAME.get(l, l)} {sum(x['protection_actions_since_2021'] for x in d.values())}" for l, d in sorted(lg.items())) + ".",
                      "descriptive", {"null": "none (log records)", "expected_by_chance": "n/a"},
                      "A title is the first framing a reader sees; protection decides who may change the text.",
                      "Renames are moves confirmed in the move log; protection levels are each wiki's own names.",
                      numbers=lg, chart="chart_data/logs.json"))
    ex = R["exposure"]
    def gv(l):
        x = (ex.get(l) or {}).get("after_war") or {}
        g = x.get("genocide") or {}
        return f"{LANG_NAME.get(l, l)} {pct(g.get('own_voice'))}"
    cards.append(card("V1", "How many readers met each framing",
                      "Share of key-article views after 7 Oct 2023 whose opening stated 'genocide' in the encyclopedia's own voice: " +
                      ", ".join(gv(l) for l in ex if ((ex[l].get("after_war") or {}).get("views_m"))) + ".",
                      "descriptive", {"null": "none (exposure measurement)", "expected_by_chance": "n/a"},
                      "Exposure turns a wording into an audience: what millions actually read.",
                      "Monthly user views (all access) summed over current and former titles; framing at mid-month.",
                      numbers=ex, chart="chart_data/exposure.json"))
    wd = R["wikidata"]
    cards.append(card("W1", "The one-line descriptions search engines show",
                      "Wikidata description changes since 2021 (after the war): " + "; ".join(
                          f"{c}: " + ", ".join(f"{l} {x['description_changes']} ({x['description_changes_after_war']})" for l, x in d.items()
                                               if x["description_changes"]) for c, d in wd.items()) + ".",
                      "descriptive", {"null": "none (change records)", "expected_by_chance": "n/a"},
                      "These short lines appear under search results and in AI answers.",
                      "Values come from edit summaries; bulk edits are counted without values.",
                      numbers=wd, chart="chart_data/wikidata.json"))
    return cards


def render_md(cards, R):
    out = ["# Cross-wiki: how the narrative travelled between language editions", "",
           f"Generated {R['meta']['generated']}. Data to {R['meta']['end']}. Nulls: {R['meta']['null_draws']} draws. "
           "No usernames or account hashes appear here; accounts in the network are A1, A2...", ""]
    for c in cards:
        out += [f"## {c['title']}", "", f"**Confidence:** {c['confidence']}", "", c["what_we_see"], "",
                f"**Null model:** {json.dumps(c['null_model'], ensure_ascii=False)}", "", f"**So what:** {c['so_what']}", "",
                f"**Caveat:** {c['caveat']}", ""]
    return "\n".join(out)


_BIGOK = ("view", "byte", "total", "count", "sum")


def _clean(x, key=""):
    # large aggregate counts (views, bytes) are written in millions so the privacy gate's revid rule cannot misfire on them
    if isinstance(x, (int, np.integer)) and not isinstance(x, bool) and abs(int(x)) >= 1_000_000 and any(b in str(key).lower() for b in _BIGOK):
        return round(int(x) / 1e6, 3)
    if isinstance(x, dict):
        return {k: _clean(v, k) for k, v in x.items() if not str(k).startswith("_")}
    if isinstance(x, list):
        return [_clean(v, key) for v in x]
    if isinstance(x, set):
        return sorted(x)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        return float(x)
    return x


def write_outputs(R, out_dir=OUT):
    cd = os.path.join(out_dir, "chart_data")
    os.makedirs(cd, exist_ok=True)
    cards = build_cards(R)
    dump = lambda name, obj: json.dump(_clean(obj), open(os.path.join(cd, name), "w"), indent=1, ensure_ascii=False)
    net = {"generated": R["meta"]["generated"],
           "method": {"edge": f"analyze_coord edges (p<{AC.P_EDGE}, observed>={AC.MIN_OBS}) on units 'article [language]'; edge_type "
                              "'terms' = term-event co-activity (shared units or events on different units within 10/30/60 min), "
                              "'talk' = talk-page co-activity of accounts active in 2+ languages",
                      "communities": "Louvain on term edges (analyze_coord.network)",
                      "languages": "node: languages the account edited on these pages; edge: languages of the co-activity",
                      "labels": "A1, A2...; no hashes or usernames"},
           "crosswiki": R["network"]}
    dump("network_crosswiki.json", net)
    dump("diffusion.json", R["diffusion"]); dump("voice.json", R["voice"])
    dump("trend_by_lang.json", {"per_language": R["trend"], "monthly": R["trend_series"]})
    dump("crosswiki_accounts.json", R["accounts"]); dump("sync.json", R["sync"]); dump("blocs.json", R["blocs"] or {})
    dump("windows.json", R["windows"]); dump("narrative.json", R["narrative"]); dump("sources.json", R["sources"])
    dump("rfc.json", R["rfc"]); dump("creation.json", R["creation"]); dump("logs.json", R["logs"])
    dump("exposure.json", R["exposure"]); dump("wikidata.json", R["wikidata"])
    json.dump(_clean({"meta": R["meta"], "cards": cards}), open(os.path.join(out_dir, "cards.json"), "w"), indent=1, ensure_ascii=False)
    open(os.path.join(out_dir, "cards.md"), "w").write(render_md(_clean(cards), R))
    return cards


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", help="only run the publication privacy gate on this file or directory")
    ap.add_argument("--data", default=DATA)
    ap.add_argument("--null", type=int, default=int(os.environ.get("CW_NULL", "1000")))
    ap.add_argument("--calib", type=int, default=int(os.environ.get("CW_CALIB", "200")))
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    salt = os.environ.get("WT_SALT", "")
    if a.scan:
        bad = AC.privacy_scan(a.scan, [salt])
        for b in bad[:50]:
            print("PRIVACY:", b)
        sys.exit(f"privacy gate: {len(bad)} problem(s) - nothing may be published" if bad else 0)
    D = json.load(gzip.open(a.data, "rt"))
    R = analyze_data(D, a.null, a.calib)
    cards = write_outputs(R, a.out)
    for c in cards:
        print(f"[{c['confidence']}] {c['title']}")
    bad = AC.privacy_scan(a.out, [salt])
    if bad:
        for b in bad[:50]:
            print("PRIVACY:", b)
        sys.exit(f"privacy gate: {len(bad)} problem(s) in {a.out}")


if __name__ == "__main__":
    main()
