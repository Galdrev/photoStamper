"""Merge coder outputs with the order key and the auto KPIs; compute reliability, topic-minus-
comparison estimates, length strata, bootstrap CIs, permutation p, Mantel-Haenszel and BH.
Study 3 Part C, frozen 2026-11-05. All rules come from codebook.json; nothing is tuned here.

Usage:
  python analyze_codes.py --key BATCHES/KEY_DO_NOT_SHARE.json --batches BATCHES \
      --codes coder1=CODES_DIR_1 --codes coder2=CODES_DIR_2 \
      --auto AUTO.json --codebook codebook.json --out RESULTS.json [--reps 10000]

CODES_DIR_k holds the coder's JSON outputs (one file per batch, each a JSON array of pair
objects as specified in coder_instructions.md). BATCHES is the make_batches.py output dir
(used to verify that evidence quotes are verbatim in the version the coder saw).
"""
import argparse
import glob
import json
import os
import re
from collections import defaultdict

import numpy as np

SEED = 20261105
STRATA = ("T1", "T2", "T3")


# ---------------------------------------------------------------- loading
def load_codes(d):
    out = {}
    for f in sorted(glob.glob(os.path.join(d, "*.json"))):
        x = json.load(open(f))
        if isinstance(x, dict) and "items" in x:
            x = x["items"]
        for item in x:
            out[item["id"]] = item
    return out


def load_texts(batch_dir, coder):
    texts = {}
    for f in sorted(glob.glob(os.path.join(batch_dir, coder, "*.json"))):
        for it in json.load(open(f))["items"]:
            texts[it["id"]] = {"A": it["version_A"], "B": it["version_B"]}
    return texts


def _norm(s):
    s = (s or "").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip()


def evidence_ok(ev, text_ab):
    if not isinstance(ev, str):
        return False
    m = re.match(r"^\s*([AB])\s*:\s*(.+)$", ev, re.S)
    if not m:
        return False
    q = _norm(m.group(2)).strip('"').strip()
    if len(q) < 3 or "..." in q or "…" in q:
        return False
    return q in _norm(text_ab[m.group(1)])


# ---------------------------------------------------------------- orientation
def normalise(kpi, ans, a_is_old):
    """Return (code, instances) in OLD->NEW orientation: 'B' now means the NEW version."""
    code = ans.get("code", "none") if isinstance(ans, dict) else "none"
    if code not in kpi["values"]:
        code = "INVALID"
    insts = [dict(i) for i in (ans.get("parties") or [])] if isinstance(ans, dict) else []
    if not a_is_old:
        code = kpi["flip"].get(code, code)
        fl = kpi.get("instance_flip", {})
        for i in insts:
            if "dir" in i:
                i["dir"] = fl.get("dir", {}).get(i["dir"], i["dir"])
            for x, y in fl.get("swap", []):
                i[x], i[y] = i.get(y), i.get(x)
    return code, insts


# ---------------------------------------------------------------- statistics
def cohen_kappa(a, b):
    a, b = list(a), list(b)
    n = len(a)
    if n == 0:
        return None
    cats = sorted(set(a) | set(b))
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    if pe >= 1.0:
        return None
    return (po - pe) / (1 - pe)


def agreement_stats(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n if n else None
    k = cohen_kappa(a, b)
    cats = max(len(set(a) | set(b)), 2)
    pabak = None if po is None else (cats * po - 1) / (cats - 1)
    return {"n": n, "kappa": None if k is None else round(k, 3), "raw_agreement": None if po is None else round(po, 3),
            "pabak": None if pabak is None else round(pabak, 3)}


def diff(y, g, s=None):
    t, c = y[g == 1], y[g == 0]
    if len(t) == 0 or len(c) == 0:
        return np.nan
    return t.mean() - c.mean()


def mh_rd(y, g, s):
    num = den = 0.0
    for k in np.unique(s):
        m = s == k
        t, c = y[m & (g == 1)], y[m & (g == 0)]
        if len(t) == 0 or len(c) == 0:
            continue
        w = len(t) * len(c) / (len(t) + len(c))
        num += w * (t.mean() - c.mean())
        den += w
    return num / den if den else np.nan


def boot_ci(stat, y, g, s, reps, rng, within_strata=False):
    idx_groups = []
    if within_strata:
        for k in np.unique(s):
            for gg in (0, 1):
                idx_groups.append(np.where((s == k) & (g == gg))[0])
    else:
        for gg in (0, 1):
            idx_groups.append(np.where(g == gg)[0])
    vals = np.empty(reps)
    for r in range(reps):
        ix = np.concatenate([rng.choice(ig, len(ig), replace=True) for ig in idx_groups if len(ig)])
        vals[r] = stat(y[ix], g[ix], s[ix])
    vals = vals[~np.isnan(vals)]
    if len(vals) == 0:
        return [None, None]
    return [round(float(np.percentile(vals, 2.5)), 4), round(float(np.percentile(vals, 97.5)), 4)]


def perm_p(stat, y, g, s, reps, rng, within_strata=False):
    obs = stat(y, g, s)
    if np.isnan(obs):
        return None
    gp = g.copy()
    hits = 0
    for r in range(reps):
        if within_strata:
            for k in np.unique(s):
                m = np.where(s == k)[0]
                gp[m] = rng.permutation(g[m])
        else:
            gp = rng.permutation(g)
        hits += abs(stat(y, gp, s)) >= abs(obs) - 1e-12
    return (hits + 1) / (reps + 1)


def bh(pvals):
    """Benjamini-Hochberg adjusted q-values (None passes through)."""
    items = [(i, p) for i, p in enumerate(pvals) if p is not None]
    m = len(items)
    q = [None] * len(pvals)
    prev = 1.0
    for rank, (i, p) in sorted(enumerate(sorted(items, key=lambda t: t[1]), 1), key=lambda t: -t[0]):
        prev = min(prev, p * m / rank)
        q[i] = round(prev, 4)
    return q


def estimate(pairs, field, reps, seed):
    P = [p for p in pairs if p.get(field) is not None]
    if not P:
        return None
    y = np.array([p[field] for p in P], float)
    g = np.array([1 if p["grp"] == "topic" else 0 for p in P])
    s = np.array([STRATA.index(p["tercile"]) for p in P])
    rng = np.random.default_rng(seed)
    out = {"n_topic": int(g.sum()), "n_comparison": int((1 - g).sum()),
           "share_topic": round(float(y[g == 1].mean()), 4) if g.sum() else None,
           "share_comparison": round(float(y[g == 0].mean()), 4) if (1 - g).sum() else None}
    d = diff(y, g)
    out["delta"] = None if np.isnan(d) else round(float(d), 4)
    out["delta_ci95"] = boot_ci(diff, y, g, s, reps, rng)
    out["p_perm"] = perm_p(diff, y, g, s, reps, rng)
    by = {}
    for k, name in enumerate(STRATA):
        m = s == k
        yt, yc = y[m & (g == 1)], y[m & (g == 0)]
        by[name] = {"topic": f"{yt.sum():g}/{len(yt)}", "comparison": f"{yc.sum():g}/{len(yc)}",
                    "delta": None if not len(yt) or not len(yc) else round(float(yt.mean() - yc.mean()), 4)}
    out["by_tercile"] = by
    rd = mh_rd(y, g, s)
    out["mh_rd"] = None if np.isnan(rd) else round(float(rd), 4)
    out["mh_rd_ci95"] = boot_ci(mh_rd, y, g, s, reps, rng, within_strata=True)
    out["mh_p_perm_stratified"] = perm_p(mh_rd, y, g, s, reps, rng, within_strata=True)
    return out


# ---------------------------------------------------------------- main pipeline
def coder_pass(key, allk, llm_ids, coder, codes, texts):
    """Normalise one coder's answers. Returns ({pid: {kid: (code, insts)}}, {pid: usable}, stats)."""
    norm, usable = {}, {}
    ev_pos = ev_bad = inval = 0
    for pid in key["pairs"]:
        item = codes.get(pid)
        if item is None:
            continue
        a_is_old = key["orientation"][coder][pid] == "A=old"
        usable[pid] = bool(item.get("usable", True))
        norm[pid] = {}
        for kid in llm_ids:
            ans = item.get(kid) or {"code": "none"}
            code, insts = normalise(allk[kid], ans, a_is_old)
            if code == "INVALID":
                inval += 1
                code, insts = "none", []
            if code != "none":
                ev_pos += 1
                if not evidence_ok(ans.get("evidence"), texts[pid]):
                    ev_bad += 1
                    code, insts = "none", []
            norm[pid][kid] = (code, insts)
    stats = {"pairs_coded": len(norm), "missing": sorted(set(key["pairs"]) - set(norm)),
             "invalid_codes": inval, "positive_codes": ev_pos, "voided_non_verbatim": ev_bad,
             "void_rate": round(ev_bad / ev_pos, 3) if ev_pos else None,
             "rerun_required_over_15pct": bool(ev_pos and ev_bad / ev_pos > 0.15)}
    return norm, usable, stats


def analyse(key_path, batch_dir, code_dirs, auto_path, codebook_path, out_path, reps=10000):
    key = json.load(open(key_path))
    cb = json.load(open(codebook_path))
    auto = {r["title"]: r for r in json.load(open(auto_path))["pairs"]}
    kpis = {k["id"]: k for k in cb["kpis"]}
    sc1 = next(x for x in cb["style_controls"] if x["id"] == "SC1")
    allk = dict(kpis, SC1=sc1)
    llm_ids = [k for k, v in kpis.items() if v["coder"] == "llm"] + ["SC1"]
    auto_ids = [k for k, v in kpis.items() if v["coder"] == "auto"]
    coders = sorted(code_dirs)

    N, U, res = {}, {}, {"codebook_version": cb["version"], "coders": coders, "coder_checks": {}}
    for c in coders:
        N[c], U[c], res["coder_checks"][c] = coder_pass(key, allk, llm_ids, c, load_codes(code_dirs[c]), load_texts(batch_dir, c))

    # ---- reliability
    rel = {}
    common = [pid for pid in key["pairs"] if all(pid in N[c] for c in coders)]
    for kid in llm_ids:
        pos = set(allk[kid]["primary_positive"])
        if len(coders) < 2:
            rel[kid] = {"note": "one coder only"}
            continue
        c1, c2 = coders[:2]
        cat1 = [N[c1][p][kid][0] for p in common]
        cat2 = [N[c2][p][kid][0] for p in common]
        b1 = [int(x in pos) for x in cat1]
        b2 = [int(x in pos) for x in cat2]
        r = {"binary": agreement_stats(b1, b2), "categorical": agreement_stats(cat1, cat2),
             "prevalence": round((sum(b1) + sum(b2)) / (2 * len(common)), 3) if common else None}
        k = r["binary"]["kappa"]
        r["status"] = "no_variance" if k is None else ("unreliable" if k < 0.6 else "reliable")
        rel[kid] = r
    res["reliability"] = rel

    # ---- pair table
    rows = []
    for pid, meta in key["pairs"].items():
        a = auto.get(meta["title"], {})
        row = {"id": pid, "title": meta["title"], "group": meta["group"], "grp": meta["grp"], "change": meta["change"],
               "d0": meta.get("d0"), "tercile": meta["tercile"], "lead0_words": meta["lead0_words"]}
        row["unusable_votes"] = sum(1 for c in coders if pid in U[c] and not U[c][pid])
        for kid in llm_ids:
            pos = set(allk[kid]["primary_positive"])
            got = [int(N[c][pid][kid][0] in pos) for c in coders if pid in N[c]]
            row[f"{kid}_mean"] = sum(got) / len(got) if got else None
            row[f"{kid}_and"] = int(all(got)) if got else None
            row[f"{kid}_or"] = int(any(got)) if got else None
            row[f"{kid}_codes"] = {c: N[c][pid][kid][0] for c in coders if pid in N[c]}
            row[f"{kid}_instances"] = {c: N[c][pid][kid][1] for c in coders if pid in N[c]}
        for kid in auto_ids:
            f = kpis[kid]["auto_field"]
            v = a.get(f)
            row[f"{kid}_mean"] = row[f"{kid}_and"] = row[f"{kid}_or"] = v
        row["K04a_gain"] = a.get("K04a_gain")
        for f in ("SC_len_ratio", "SC_protected_opening", "SC_fs_tense_flip", "SC_terror_fs_removed", "SC_alt_names_fs_up",
                  "SC_attr_density_down", "SUP_zionist_actor_gain", "SUP_majority_gain"):
            row[f] = a.get(f)
        rows.append(row)
    rows = [r for r in rows if r["unusable_votes"] < max(len(coders), 1) or not coders]

    # ---- validity of K04a vs LLM K04 colonial subset
    if coders:
        v1, v2 = [], []
        for r in rows:
            if r["K04a_gain"] is None:
                continue
            col = 0
            for c, insts in r["K04_instances"].items():
                col = max(col, int(any(i.get("class") == "colonial" and i.get("dir") == "B_gains" for i in insts)))
            v1.append(int(r["K04a_gain"]))
            v2.append(col)
        res["validity_K04a_vs_llm_colonial"] = agreement_stats(v1, v2) if v1 else None

    # ---- estimates
    fam = cb["families"]
    est = {}
    order = fam["primary"] + fam["secondary"] + ["SC1"]
    for i, kid in enumerate(order):
        est[kid] = {"family": "primary" if kid in fam["primary"] else "secondary" if kid in fam["secondary"] else "style_control",
                    "main": estimate(rows, f"{kid}_mean", reps, SEED + i)}
    for fname in ("primary", "secondary"):
        ids = fam[fname]
        qs = bh([est[k]["main"]["p_perm"] if est[k]["main"] else None for k in ids])
        for k, q in zip(ids, qs):
            est[k]["q_bh"] = q
    for kid in order:
        e = est[kid]
        m = e["main"]
        st = rel.get(kid, {}).get("status", "auto") if kid not in auto_ids else "auto"
        e["reliability_status"] = st
        if kid == "SC1" or m is None:
            e["verdict"] = "style_control" if kid == "SC1" else "no_data"
            continue
        q = e.get("q_bh")
        if st in ("unreliable", "no_variance"):
            v = "unreliable"
        elif q is not None and q <= 0.10 and m["delta"] is not None and m["delta"] < 0:
            v = "reverse"
        elif q is not None and q <= 0.10 and m["delta"] > 0:
            ok = m["mh_rd"] is not None and m["mh_rd"] > 0 and (m["mh_p_perm_stratified"] or 1) <= 0.10
            v = "supported" if ok else "length_sensitive"
        else:
            v = "not_supported"
        e["verdict"] = v if e["family"] == "primary" else v + " (exploratory)"
    # ---- sensitivity (estimates only; verdicts unchanged)
    sens_sets = {
        "coders_AND": (rows, "and"), "coders_OR": (rows, "or"),
        "no_control_contaminated": ([r for r in rows if r["group"] != "control_contaminated"], "mean"),
        "comparison_change_gt_0.05": ([r for r in rows if r["grp"] == "topic" or (r["change"] or 0) > 0.05], "mean"),
        "lead0_from_2021": ([r for r in rows if str(r.get("d0") or "").startswith("2021")], "mean"),
        "no_unusable_votes": ([r for r in rows if r["unusable_votes"] == 0], "mean"),
    }
    for kid in fam["primary"] + fam["secondary"]:
        est[kid]["sensitivity"] = {}
        for name, (rs, comb) in sens_sets.items():
            m = estimate(rs, f"{kid}_{comb}", max(reps // 5, 200), SEED + 99)
            est[kid]["sensitivity"][name] = None if m is None else {k: m[k] for k in ("share_topic", "share_comparison", "delta", "delta_ci95", "mh_rd")}
    res["estimates"] = est

    # ---- direction breakdown (descriptive): share of pairs with each (party, dir), coder-mean
    brk = {}
    for kid in [k for k in llm_ids if k != "SC1"]:
        cnt = defaultdict(lambda: {"topic": 0.0, "comparison": 0.0})
        for r in rows:
            for c, insts in r[f"{kid}_instances"].items():
                seen = {(i.get("party", "UNCLEAR"), i.get("dir", "")) for i in insts}
                for pd in seen:
                    cnt[f"{pd[0]}|{pd[1]}"][r["grp"]] += 1 / len(r[f"{kid}_instances"])
        nT = sum(r["grp"] == "topic" for r in rows) or 1
        nC = sum(r["grp"] == "comparison" for r in rows) or 1
        brk[kid] = {k: {"topic_share": round(v["topic"] / nT, 4), "comparison_share": round(v["comparison"] / nC, 4)}
                    for k, v in sorted(cnt.items())}
    res["direction_breakdown"] = brk

    # ---- style controls (auto), both groups
    scs = {}
    for f in ("SC_protected_opening", "SC_fs_tense_flip", "SC_terror_fs_removed", "SC_alt_names_fs_up", "SC_attr_density_down",
              "SUP_zionist_actor_gain", "SUP_majority_gain", "K04a_gain"):
        vals = {g: [r[f] for r in rows if r["grp"] == g and r[f] is not None] for g in ("topic", "comparison")}
        scs[f] = {g: (round(sum(v) / len(v), 4) if v else None) for g, v in vals.items()}
    res["style_controls_and_support"] = scs
    res["n_pairs_analysed"] = {"topic": sum(r["grp"] == "topic" for r in rows), "comparison": sum(r["grp"] == "comparison" for r in rows)}
    res["pairs"] = rows
    json.dump(res, open(out_path, "w"), ensure_ascii=False, indent=1, default=str)
    return res


def print_summary(res):
    print("pairs analysed:", res["n_pairs_analysed"])
    for c, s in res["coder_checks"].items():
        print(c, {k: v for k, v in s.items() if k != "missing"}, "missing:", len(s["missing"]))
    print(f"{'KPI':5} {'fam':9} {'kappa':>6} {'topic':>6} {'comp':>6} {'delta':>7} {'CI95':>17} {'p':>7} {'q':>7} {'MH-RD':>7} {'p_MH':>7}  verdict")
    for kid, e in res["estimates"].items():
        m = e["main"] or {}
        k = res["reliability"].get(kid, {}).get("binary", {}).get("kappa", "auto")
        ci = m.get("delta_ci95") or [None, None]
        print(f"{kid:5} {e['family'][:9]:9} {str(k):>6} {str(m.get('share_topic')):>6} {str(m.get('share_comparison')):>6} "
              f"{str(m.get('delta')):>7} {str(ci):>17} {str(round(m['p_perm'], 4) if m.get('p_perm') else None):>7} "
              f"{str(e.get('q_bh')):>7} {str(m.get('mh_rd')):>7} {str(round(m['mh_p_perm_stratified'], 4) if m.get('mh_p_perm_stratified') else None):>7}  {e['verdict']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True)
    ap.add_argument("--batches", required=True)
    ap.add_argument("--codes", action="append", required=True, help="coderN=DIR")
    ap.add_argument("--auto", required=True)
    ap.add_argument("--codebook", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--reps", type=int, default=10000)
    a = ap.parse_args()
    code_dirs = dict(x.split("=", 1) for x in a.codes)
    res = analyse(a.key, a.batches, code_dirs, a.auto, a.codebook, a.out, a.reps)
    print_summary(res)


if __name__ == "__main__":
    main()
