"""Mass v3: a stratified random sample with known inclusion probabilities (fixes the mass2 frame, see
patterns/sampling/AUDIT.md).

  python mass3.py population                 -> data/mass3/population.json   (every main-namespace article each project
                                                assesses, via PageAssessments; redirects resolved, deduped, assigned)
  python mass3.py sample                     -> data/mass3/frame.json        (stratified SRS, fixed seed, pi per row,
                                                rows already measured in mass2 marked `reused`)
  python mass3.py estimate [--of N] [--check] -> requests / runtime per shard (--check: exit non-zero over the budget)
  python mass3.py shard --shard I --of N     -> data/mass3/m3_I.json.gz      (non-reused rows only; checkpointed via
                                                mass._run; exits non-zero if >5% of rows error)
  python mass3.py merge                      -> data/mass3.json, data/mass3_leads.json.gz (fetched + reused records with
                                                design weights; exits non-zero if <95% of fetch rows arrived)
  python mass3.py analyze                    -> patterns/sampling/mass3_results.md, chart_data/07_*.json, 08_*.json
  MASS_LIMIT=40 ...                          -> test mode (first 40 rows of the shard)

Populations (exact PageAssessments project names; never a prefix or keyword search, so "India" cannot match Indiana):
  TOPIC       Israel, Palestine, Judaism, Jewish history (required), then the Israel Palestine Collaboration, Arab-Israeli
              conflict and Zionism projects/task forces if PageAssessments lists them.
  COMPARISON  Kurdistan, Ukraine, Turkey, Serbia, Armenia, Azerbaijan (required), Russo-Ukrainian war, Kosovo, Cyprus,
              Kashmir (only a Kashmir project or a Kashmir task force of India/Pakistan - India/Pakistan as a whole are
              never used), Northern Ireland and The Troubles (optional: used if found, otherwise recorded as skipped).
  Project names are discovered with list=projects&pjsubprojects=1 (task forces are "Parent/Task force"). Required names
  must match a project exactly; optional ones match the whole name or the task-force part, case and dash insensitive.

Population. list=projectpages&wppprojects=<one project>&wppassessments=1&wpplimit=max, following `continue` until done
(the API's flag is wppassessments; it returns class and importance per page). Only namespace 0 is kept. Every page id
is resolved in batches of 50 (prop=info|pageprops, redirects=1): redirects are replaced by their target (dropped if the
target is not an article), missing and disambiguation pages are dropped, and pages are deduped by resolved page id
(a project's assessment of the target beats its assessment of a redirect). An article assessed by any topic project is
TOPIC and belongs to its first topic project in the order above; otherwise it is COMPARISON and belongs to its first
comparison project. Every project and importance it has is kept (`assess`), plus `also_comparison` for topic articles
that a comparison project also tags (mass2 silently dropped these 572 overlap pages). Importance is that of the
assigned project: Top, High, Mid, Low (Bottom counted as Low), NA, Unknown, and Unrated (empty).

Sample. Strata = side x project x importance. Per side, n_h is proportional to N_h with a floor of 40 for strata with
N_h >= 40; strata with N_h < 40 are taken whole (census, pi = 1), so no article has pi = 0. Floors and censuses are
fixed first and the rest of the target is spread proportionally (largest remainder), repeated until stable. Within a
stratum the rows (sorted by page id) are drawn with random.Random(SEED).sample, so pi = n_h / N_h exactly and the base
weight is 1 / pi. Rows already in mass2 (matched by resolved page id, then title) stay eligible and are drawn like any
other; they are marked `reused` and their mass2 measurements are used instead of a fetch.

Per fetched row (shard): random_baseline.collect - mass_narr features (critical counts, event-filter residuals, lead
prose) at mass.DATES (2021-01-01, 2023-07-01, now = the population run's date) with strict lead fetches, a creation
check when the 2021 lead is missing, and pageviews for the last 12 complete months.

Analysis (design-based). Hajek (ratio) estimators with weights N_h / r_h (r_h = rows of the stratum that arrived; a
non-response adjustment within stratum, equal to 1 / pi when everything arrived). Sum of weights = N. CIs: stratified
bootstrap (rows resampled with replacement within each stratum, census strata held fixed, B = WT_BOOT), percentile 95%.
(a) post-war mean change in lead critical hits per 10k words, topic minus comparison (leads >= 20 words at all three
dates); (b) share of leads whose critical-term count rose Jul 2023 -> now; (c) the narrative-residual DiD and its share
of (a); (d) share of 12-month views on leads that gained; (e) Israel+Palestine minus Judaism gain share (and Judaism
minus comparison). Overall, by importance, and against data/random_baseline.json (equal weights) when it exists.
"""
import argparse, glob, gzip, json, math, os, random, sys, time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wt_net                   # noqa: E402
import analyze as A             # noqa: E402
import mass as M                # noqa: E402
import random_baseline as RB    # noqa: E402

API = "https://en.wikipedia.org/w/api.php"
DATA = A.DATA
MDIR = os.path.join(DATA, "mass3")
OUT_MD = os.path.join(HERE, "patterns", "sampling", "mass3_results.md")
CHART = os.path.join(HERE, "patterns", "sampling", "chart_data")
KIND = "m3"
SEED = 20261107
TARGET = {"topic": int(os.environ.get("WT_M3_TOPIC", "3000")), "comparison": int(os.environ.get("WT_M3_COMPARISON", "3000"))}
FLOOR = 40
NB = int(os.environ.get("WT_BOOT", "1000"))
MIN_WORDS = RB.MIN_WORDS
CRIT = list(A.CRITICAL)
SIDES = ("topic", "comparison")
LEVELS = ["Top", "High", "Mid", "Low", "NA", "Unknown", "Unrated"]
REQ_PER_ARTICLE = 4.15            # 3 leads + 1 pageviews + creation check for ~15% without a 2021 lead (random baseline)
CALIBRATION = 1.15                # retries/continuations, as calibrated in the mass2 pilot
BUDGET_H = 4.0                    # per shard, at the effective rate below
EFF_RPS = 1.0                     # effective req/s per shard seen with 4 jobs at WT_RPS 2

# (family, side, required, exact full names, optional normalized names matched against the whole name or the task-force part)
SPEC = [
    ("Israel", "topic", True, ["Israel"], None),
    ("Palestine", "topic", True, ["Palestine"], None),
    ("Judaism", "topic", True, ["Judaism"], None),
    ("Jewish history", "topic", True, ["Jewish history"], None),
    ("Israel Palestine Collaboration", "topic", False, [], {"israel palestine collaboration", "israel-palestine collaboration",
                                                              "israel-palestine conflict collaboration"}),
    ("Arab-Israeli conflict", "topic", False, [], {"arab-israeli conflict", "israeli-palestinian conflict"}),
    ("Zionism", "topic", False, [], {"zionism"}),
    ("Kurdistan", "comparison", True, ["Kurdistan"], None),
    ("Ukraine", "comparison", True, ["Ukraine"], None),
    ("Russo-Ukrainian war", "comparison", False, [], {"russo-ukrainian war", "russia-ukraine war", "russian invasion of ukraine",
                                                      "war in ukraine"}),
    ("Turkey", "comparison", True, ["Turkey"], None),
    ("Serbia", "comparison", True, ["Serbia"], None),
    ("Kosovo", "comparison", False, [], {"kosovo"}),
    ("Armenia", "comparison", True, ["Armenia"], None),
    ("Azerbaijan", "comparison", True, ["Azerbaijan"], None),
    ("Cyprus", "comparison", False, [], {"cyprus"}),
    ("Kashmir", "comparison", False, [], {"kashmir", "jammu and kashmir", "jammu & kashmir", "azad kashmir", "kashmir conflict",
                                          }),
    ("Northern Ireland", "comparison", False, [], {"northern ireland"}),
    ("The Troubles", "comparison", False, [], {"the troubles", "troubles"}),
]


def _now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _api(params):
    return RB._api(params)          # wt_net.get_json + fail loudly on a failed or error response


def _norm(s):
    return " ".join(str(s).replace("–", "-").replace("—", "-").replace("_", " ").lower().split())


def _tf(s):
    """Normalized name without a trailing "task force" / "work group" (exact comparison, never a prefix match)."""
    n = _norm(s)
    for suf in (" task force", " work group", " workgroup"):
        if n.endswith(suf):
            n = n[:-len(suf)]
    return n


def norm_imp(x):
    x = (x or "").strip()
    if not x:
        return "Unrated"
    k = x.capitalize() if x.upper() != "NA" else "NA"
    return {"Bottom": "Low", "Na": "NA", "None": "Unrated", "Unassessed": "Unrated"}.get(k, k if k in LEVELS else "Unknown")


def _dump(path, obj, gz=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with (gzip.open(tmp, "wt") if gz else open(tmp, "w")) as f:
        json.dump(obj, f)
    os.replace(tmp, path)


# ================================================================== 1. population
def list_projects():
    j = _api({"action": "query", "list": "projects", "pjsubprojects": 1})
    pr = j["query"].get("projects")
    if isinstance(pr, dict):
        names = list(pr)
    else:
        names = [x if isinstance(x, str) else (x.get("name") or x.get("*") or x.get("title")) for x in (pr or [])]
    names = [n for n in names if n]
    if not names:
        raise RuntimeError("list=projects returned no projects")
    return names


def resolve_projects(names):
    """Exact names per SPEC -> (ordered [{name, family, side, required}], skipped [...]); exits if a required one is missing."""
    have = set(names)
    out, skipped, missing, used = [], [], [], set()
    for fam, side, req, exact, opt in SPEC:
        hit = [n for n in exact if n in have]
        if opt:
            hit += sorted(n for n in names if n not in hit and (_tf(n) in opt or ("/" in n and _tf(n.split("/", 1)[1]) in opt)))
        hit = [n for n in hit if n not in used]
        if not hit:
            (missing if req else skipped).append({"family": fam, "side": side, "looked_for": exact or sorted(opt)})
            continue
        for n in hit:
            used.add(n); out.append({"name": n, "family": fam, "side": side, "required": req})
    if missing:
        sys.exit(f"population: required projects not found in PageAssessments: {[m['family'] for m in missing]}")
    return out, skipped


def project_pages(name):
    """Every page `name` assesses: [{pageid, ns, title, class, importance}], following continuation to the end."""
    out, cont, req = [], {}, 0
    while True:
        j = _api({"action": "query", "list": "projectpages", "wppprojects": name, "wppassessments": 1, "wpplimit": "max", **cont})
        req += 1
        pr = j["query"].get("projects") or {}
        if isinstance(pr, list):
            pr = {(x.get("name") or x.get("project") or name): (x.get("pages") or []) for x in pr}
        for p in (pr.get(name) or []) if isinstance(pr, dict) else []:
            a = p.get("assessment") or {}
            out.append({"pageid": p.get("pageid"), "ns": p.get("ns", 0), "title": p.get("title"),
                        "class": a.get("class") or "", "importance": a.get("importance") or ""})
        if "continue" not in j:
            break
        cont = {k: v for k, v in j["continue"].items()}
        wt_net.heartbeat(f"projectpages {name}", len(out), 0)
    return out, req


def resolve_ids(titles, workers=4):
    """{pageid: {"pageid": target id, "title": target title, "redirect_from": title or None} | {"drop": reason}} for the
    assessed page ids in `titles` ({pageid: title as PageAssessments gave it}), 50 ids per request."""
    ids = sorted(titles)
    batches = [ids[k:k + 50] for k in range(0, len(ids), 50)]

    def one(part):
        j = _api({"action": "query", "pageids": "|".join(map(str, part)), "prop": "info|pageprops", "ppprop": "disambiguation",
                  "redirects": 1})
        q = j["query"]
        pages = q.get("pages") or []
        if isinstance(pages, dict):
            pages = list(pages.values())
        ctx = {"redir": {r["from"]: r["to"] for r in q.get("redirects") or []},
               "by_title": {p.get("title"): p for p in pages}, "by_id": {p.get("pageid"): p for p in pages if p.get("pageid")}}
        return {i: _classify(i, titles[i], ctx) for i in part}

    res = {}
    with ThreadPoolExecutor(workers) as ex:
        for k, part in enumerate(ex.map(one, batches), 1):
            res.update(part)
            wt_net.heartbeat("resolve", k, len(batches))
    return res


def _classify(pid, title, ctx):
    """Resolved target of one assessed page id."""
    redir, by_title, by_id = ctx["redir"], ctx["by_title"], ctx["by_id"]
    p = by_id.get(pid)
    src = None
    if p is None or p.get("redirect"):              # a redirect's id comes back as its target, listed under redirects
        if title in redir:
            src = title
            p = by_title.get(redir[title])
            if p is None:                           # target outside the batch's pages: a section/interwiki/special target
                return {"drop": "redirect_out_of_namespace"}
        if p is None:
            return {"drop": "unresolved"}
    if p.get("missing") or p.get("invalid"):
        return {"drop": "missing"}
    if p.get("ns", 0) != 0:
        return {"drop": "redirect_out_of_namespace" if src else "namespace"}
    if p.get("redirect"):                           # still a redirect (double or broken redirect)
        return {"drop": "redirect_unresolved"}
    if "disambiguation" in (p.get("pageprops") or {}):
        return {"drop": "disambiguation"}
    return {"pageid": p["pageid"], "title": p["title"], "redirect_from": src}


def build_population(projects, pages_by_project, resolved):
    """Dedupe by resolved page id and assign each article to its side / first project. Pure function (tested)."""
    order = {s: [p["name"] for p in projects if p["side"] == s] for s in SIDES}
    side_of = {p["name"]: p["side"] for p in projects}
    arts, drops, raw = {}, Counter(), {s: defaultdict(Counter) for s in SIDES}
    for name in [p["name"] for p in projects]:
        for pg in pages_by_project.get(name) or []:
            if pg.get("ns", 0) != 0:
                drops["namespace"] += 1; continue
            r = resolved.get(pg["pageid"]) or {"drop": "unresolved"}
            if "drop" in r:
                drops[r["drop"]] += 1; continue
            a = arts.setdefault(r["pageid"], {"pageid": r["pageid"], "title": r["title"], "assess": {}, "redirects_merged": []})
            if r["redirect_from"]:
                if r["redirect_from"] not in a["redirects_merged"]:
                    a["redirects_merged"].append(r["redirect_from"])
            cur = a["assess"].get(name)
            new = {"class": pg["class"], "importance": norm_imp(pg["importance"]), "via_redirect": bool(r["redirect_from"])}
            if cur is None or (cur["via_redirect"] and not new["via_redirect"]):
                a["assess"][name] = new
    rows = []
    for a in arts.values():
        ps = set(a["assess"])
        side = "topic" if any(side_of[p] == "topic" for p in ps) else "comparison"
        proj = next(p for p in order[side] if p in ps)
        x = a["assess"][proj]
        rows.append({"pageid": a["pageid"], "title": a["title"], "side": side, "project": proj, "importance": x["importance"],
                     "class": x["class"], "assess": a["assess"], "redirects_merged": a["redirects_merged"],
                     "also_comparison": side == "topic" and any(side_of[p] == "comparison" for p in ps)})
        for p, v in a["assess"].items():
            raw[side_of[p]][p][v["importance"]] += 1
    rows.sort(key=lambda r: r["pageid"])
    return rows, drops, raw


def stratum(r):
    return f"{r['side']}|{r['project']}|{r['importance']}"


def population(path=None):
    path = path or os.path.join(MDIR, "population.json")
    names = list_projects()
    projects, skipped = resolve_projects(names)
    print("population: projects", [(p["side"], p["name"]) for p in projects], "skipped", [s["family"] for s in skipped], flush=True)
    pages, req = {}, {"list_projects": 1, "projectpages": 0, "resolve": 0}
    for p in projects:
        pages[p["name"]], n = project_pages(p["name"])
        req["projectpages"] += n
        print(f"  {p['name']}: {len(pages[p['name']])} assessed pages ({n} requests)", flush=True)
    titles = {pg["pageid"]: pg["title"] for v in pages.values() for pg in v if pg.get("ns", 0) == 0 and pg.get("pageid")}
    ids = sorted(titles)
    resolved = resolve_ids(titles)
    req["resolve"] = math.ceil(len(ids) / 50)
    rows, drops, raw = build_population(projects, pages, resolved)
    if drops["unresolved"] > 0.01 * max(1, len(ids)):
        sys.exit(f"population: {drops['unresolved']}/{len(ids)} page ids could not be resolved (>1%)")
    N = Counter(stratum(r) for r in rows)
    side_tot = {s: sum(1 for r in rows if r["side"] == s) for s in SIDES}
    by_imp = {s: dict(Counter(r["importance"] for r in rows if r["side"] == s)) for s in SIDES}
    pop = {"generated": _now(), "now": time.strftime("%Y-%m-%dT00:00:00Z", time.gmtime()), "source": "PageAssessments list=projectpages",
           "projects": projects, "skipped_projects": skipped, "requests": req,
           "assessed_pages_raw": {p: len(v) for p, v in pages.items()}, "dropped": dict(drops),
           "counts_by_project_importance": {s: {p: dict(c) for p, c in raw[s].items()} for s in SIDES},
           "strata": dict(sorted(N.items())), "side_totals": side_tot, "side_by_importance": by_imp,
           "also_comparison": sum(r["also_comparison"] for r in rows),
           "notes": {"counts_by_project_importance": "every article each project assesses (after redirect resolution; an article "
                                                     "counts once per project, so projects overlap)",
                     "strata": "after assignment to the first project of its side: disjoint, sums to the side totals"},
           "articles": rows}
    _dump(path, pop)
    print(f"population: topic {side_tot['topic']:,}, comparison {side_tot['comparison']:,} articles; dropped {dict(drops)}", flush=True)
    return pop


# ================================================================== 2. sample
def allocate(N, target, floor=FLOOR):
    """{stratum: n_h}: proportional to N_h, n_h >= floor where N_h >= floor, census where N_h < floor, n_h <= N_h."""
    fixed, free = {}, {h: v for h, v in N.items() if v > 0}
    for h, v in list(free.items()):
        if v < floor:
            fixed[h] = v; del free[h]
    while free:
        rem = target - sum(fixed.values())
        Nf = sum(free.values())
        prop = {h: rem * v / Nf for h, v in free.items()}
        lo = {h for h in free if prop[h] < floor}
        hi = {h for h in free if prop[h] > free[h]}
        if not lo and not hi:
            break
        for h in lo:
            fixed[h] = floor; del free[h]
        for h in hi - lo:
            fixed[h] = free.pop(h)
    out = dict(fixed)
    if free:
        rem = target - sum(fixed.values())
        Nf = sum(free.values())
        prop = {h: rem * v / Nf for h, v in free.items()}
        base = {h: int(math.floor(p)) for h, p in prop.items()}
        left = rem - sum(base.values())
        for h in sorted(free, key=lambda h: (-(prop[h] - base[h]), h))[:max(0, left)]:
            base[h] += 1
        out.update(base)
    return {h: min(out[h], N[h]) for h in N if N[h] > 0}


def mass2_index(path=None):
    """{pageid: title}, {title: title} of mass2 articles (resolved title, former frame titles)."""
    path = path or os.path.join(DATA, "mass2.json.gz")
    if not os.path.exists(path):
        alt = path[:-3] if path.endswith(".gz") else path + ".gz"
        if not os.path.exists(alt):
            sys.exit(f"sample: {path} not found (mass2 reuse needs it)")
        path = alt
    m = json.load(gzip.open(path, "rt") if path.endswith(".gz") else open(path))
    by_id, by_t = {}, {}
    for r in m.get("articles") or []:
        if (r.get("stratum") or r.get("group")) == "atrocity" or not isinstance(r.get("title"), str):
            continue
        pid = (r.get("now") or {}).get("pageid")
        if pid:
            by_id[pid] = r["title"]
        by_t[r["title"]] = r["title"]
        for t in r.get("frame_titles") or []:
            by_t.setdefault(t, r["title"])
    return by_id, by_t, m.get("now")


def sample(pop_path=None, path=None, mass2_path=None):
    pop = json.load(open(pop_path or os.path.join(MDIR, "population.json")))
    path = path or os.path.join(MDIR, "frame.json")
    by_id, by_t, m2now = mass2_index(mass2_path)
    rng = random.Random(SEED)
    rows_by = defaultdict(list)
    for r in pop["articles"]:
        rows_by[stratum(r)].append(r)
    alloc, out = [], []
    for side in SIDES:
        Ns = {h: len(v) for h, v in rows_by.items() if h.startswith(side + "|")}
        n = allocate(Ns, TARGET[side])
        for h in sorted(Ns):
            pool = sorted(rows_by[h], key=lambda r: r["pageid"])
            drawn = rng.sample(pool, n[h])
            pi = n[h] / Ns[h]
            k_re = 0
            for r in sorted(drawn, key=lambda r: r["pageid"]):
                m2 = by_id.get(r["pageid"]) or by_t.get(r["title"])
                k_re += bool(m2)
                out.append({"title": r["title"], "pageid": r["pageid"], "group": side, "project": r["project"],
                            "importance": r["importance"], "class": r["class"], "stratum": h, "pi": pi, "w": 1 / pi,
                            "projects": sorted(r["assess"]), "also_comparison": r["also_comparison"],
                            "reused": bool(m2), "mass2_title": m2})
            prop = Ns[h] * TARGET[side] / sum(Ns.values())
            alloc.append({"stratum": h, "side": side, "N": Ns[h], "n": n[h], "pi": round(pi, 6), "reused": k_re,
                          "rule": "census" if n[h] == Ns[h] else "floor" if prop < FLOOR else "proportional"})
    fr = {"generated": _now(), "now": pop["now"], "population_generated": pop["generated"], "seed": SEED, "targets": TARGET,
          "floor": FLOOR, "mass2_now": m2now, "dates": [M.DATES[0], M.DATES[1]],
          "side_totals": {s: {"N": sum(a["N"] for a in alloc if a["side"] == s), "n": sum(a["n"] for a in alloc if a["side"] == s),
                              "reused": sum(a["reused"] for a in alloc if a["side"] == s)} for s in SIDES},
          "allocation": alloc, "rows": out}
    _dump(path, fr)
    for s in SIDES:
        t = fr["side_totals"][s]
        print(f"sample {s}: N {t['N']:,}, n {t['n']:,} ({t['reused']:,} reused from mass2, {t['n'] - t['reused']:,} to fetch)", flush=True)
    return fr


# ================================================================== estimate
def estimate(fr=None, of=4, check=False):
    fr = fr or json.load(open(os.path.join(MDIR, "frame.json")))
    todo = [r for r in fr["rows"] if not r["reused"]]
    per = [len(M.shard(todo, i, of)) for i in range(of)]
    req = [math.ceil(n * REQ_PER_ARTICLE * CALIBRATION) for n in per]
    hrs = [q / EFF_RPS / 3600 for q in req]
    waves = math.ceil(of / 4)
    est = {"rows": len(fr["rows"]), "reused": len(fr["rows"]) - len(todo), "to_fetch": len(todo),
           "requests_total": sum(req), "requests_per_shard": req, "hours_per_shard_at_1rps": [round(h, 2) for h in hrs],
           "waves_at_max_parallel_4": waves, "wall_hours": round(max(hrs) * waves, 2) if hrs else 0}
    print("estimate:", json.dumps(est), flush=True)
    if check and hrs and max(hrs) > BUDGET_H * 0.9:
        sys.exit(f"estimate: a shard needs {max(hrs):.1f} h at {EFF_RPS} req/s (> 90% of the {BUDGET_H} h budget): raise --of")
    return est


# ================================================================== 3. shard / merge
def collect(row):
    return RB.collect(row)


def load_frame(path=None):
    return json.load(open(path or os.path.join(MDIR, "frame.json")))


def run_shard(i, n):
    fr = load_frame()
    RB.set_now(fr["now"])
    rows = M.shard([r for r in fr["rows"] if not r["reused"]], i, n)
    lim = int(os.environ.get("MASS_LIMIT", "0"))
    M._run(KIND, collect, rows[:lim] if lim else rows, i, out_dir=MDIR)


def views12(pv):
    """Last 12 monthly values of a mass2 (compact {start, views}) or shard ({YYYYMM: views}) pageview series."""
    mon = (pv or {}).get("monthly")
    if isinstance(mon, dict) and isinstance(mon.get("views"), list):
        vals = mon["views"]
    elif isinstance(mon, dict):
        vals = [mon[k] for k in sorted(mon)]
    else:
        return None
    have = [v for v in vals if isinstance(v, (int, float))]
    return sum(v for v in vals[-12:] if isinstance(v, (int, float))) if have else None


def _compact(sn):
    return [None if not isinstance(x, dict) else {k: x.get(k) for k in ("date", "words", "crit", "counts", "ev")} for x in sn]


def merge(mass2_path=None):
    fr = load_frame()
    fetched = {}
    for f in sorted(glob.glob(os.path.join(MDIR, f"{KIND}_*.json.gz"))):
        for r in json.load(gzip.open(f, "rt")):
            fetched.setdefault(r["title"], r)
    need_m2 = any(r["reused"] for r in fr["rows"])
    m2 = {}
    if need_m2:
        p = mass2_path or os.path.join(DATA, "mass2.json.gz")
        p = p if os.path.exists(p) else (p[:-3] if p.endswith(".gz") else p + ".gz")
        m = json.load(gzip.open(p, "rt") if p.endswith(".gz") else open(p))
        m2 = {r["title"]: r for r in m.get("articles") or [] if isinstance(r.get("title"), str)}
    arts, leads, miss = [], {}, Counter()
    for row in fr["rows"]:
        base = {k: row.get(k) for k in ("title", "pageid", "group", "project", "importance", "class", "stratum", "pi", "w",
                                        "projects", "also_comparison", "reused", "mass2_title")}
        if row["reused"]:
            r = m2.get(row["mass2_title"])
            if r is None:
                miss["reused_not_in_mass2"] += 1; continue
            sn = RB.mass2_snaps(r)
            arts.append({**base, "source": "mass2", "existed_2021": sn[0] is not None or not r.get("created_in_window"),
                         "created_later": bool(r.get("created_in_window")), "views_12m": views12(r.get("pageviews")),
                         "snaps": _compact(sn)})
        else:
            r = fetched.get(row["title"])
            if r is None:
                miss["not_fetched"] += 1; continue
            sn = r.get("snaps") or []
            arts.append({**base, "source": "mass3", "existed_2021": r.get("existed_2021"), "created_later": r.get("created_later"),
                         "deleted": r.get("deleted"), "created": r.get("created"),
                         "views_12m": (r.get("pageviews") or {}).get("views_12m"), "snaps": _compact(sn)})
            leads[row["title"]] = [None if not isinstance(x, dict) else x.get("lead_prose") for x in sn]
    n_fetch = sum(1 for r in fr["rows"] if not r["reused"])
    res = {"generated": _now(), "now": fr["now"], "mass2_now": fr.get("mass2_now"), "seed": fr["seed"], "targets": fr["targets"],
           "side_totals": fr["side_totals"], "allocation": fr["allocation"], "missing": dict(miss),
           "arrived": {"fetched": n_fetch - miss["not_fetched"], "of_fetch": n_fetch,
                       "reused": sum(1 for a in arts if a["source"] == "mass2")},
           "weight_note": "w = 1/pi (base design weight); analyze adjusts to N_h / arrived_h within stratum", "articles": arts}
    _dump(os.path.join(DATA, "mass3.json"), res)
    _dump(os.path.join(DATA, "mass3_leads.json.gz"), {"dates": [d[:10] for d in M.DATES[:2]] + [fr["now"][:10]], "leads": leads}, gz=True)
    print(f"mass3 merged: {len(arts)}/{len(fr['rows'])} rows ({res['arrived']['reused']} reused from mass2, "
          f"{res['arrived']['fetched']}/{n_fetch} fetched); missing {dict(miss)}", flush=True)
    if miss["reused_not_in_mass2"]:
        sys.exit(f"mass3 merge: {miss['reused_not_in_mass2']} reused rows not found in mass2")
    if n_fetch and res["arrived"]["fetched"] < 0.95 * n_fetch:
        sys.exit(f"mass3 merge: only {res['arrived']['fetched']}/{n_fetch} fetch rows arrived (<95%)")
    return res


# ================================================================== 4. analyze
def outcomes(a):
    """Per-article outcome dict from compact snaps (same measures as random_baseline / the audit)."""
    sn = a.get("snaps") or [None, None, None]
    x = [RB.lm(s) for s in (sn + [None] * 3)[:3]]
    o = {"okL": False, "okG": False, "post_unf": np.nan, "post_res": np.nan, "post_ev": np.nan, "pre_unf": np.nan,
         "pre_res": np.nan, "gain": np.nan, "v12": np.nan}
    if all(v is not None and v[0] >= MIN_WORDS for v in x) and a.get("existed_2021", True) is not False:
        (w0, c0, r0), (w1, c1, r1), (w2, c2, r2) = x
        o.update(okL=True, post_unf=(c2 / w2 - c1 / w1) * 1e4, post_res=(r2 / w2 - r1 / w1) * 1e4,
                 post_ev=((c2 - r2) / w2 - (c1 - r1) / w1) * 1e4, pre_unf=(c1 / w1 - c0 / w0) * 1e4, pre_res=(r1 / w1 - r0 / w0) * 1e4)
    v = a.get("views_12m")
    if x[1] is not None and x[2] is not None and isinstance(v, (int, float)):
        o.update(okG=True, gain=float(x[2][1] > x[1][1]), v12=float(v))
    return o


KEYS = ["okL", "okG", "post_unf", "post_res", "post_ev", "pre_unf", "pre_res", "gain", "v12"]


def arrays(arts, weights=None):
    O = [outcomes(a) for a in arts]
    D = {k: np.array([o[k] for o in O], dtype=bool if k in ("okL", "okG") else float) for k in KEYS}
    D["is_t"] = np.array([a["group"] == "topic" for a in arts], bool)
    D["ip"] = np.array([a["group"] == "topic" and a.get("project") in ("Israel", "Palestine") for a in arts], bool)
    D["ju"] = np.array([a["group"] == "topic" and a.get("project") == "Judaism" for a in arts], bool)
    D["imp"] = np.array([a.get("importance") or "Unrated" for a in arts], object)
    D["w"] = np.array(weights if weights is not None else [a.get("w", 1.0) for a in arts], float)
    return D


def wm(x, w, m):
    m = m & np.isfinite(x)
    sw = w[m].sum()
    return float((x[m] * w[m]).sum() / sw) if sw > 0 else np.nan


def stats(D, idx=None, sub=None):
    """Headline statistics (audit (a)-(e)) on rows idx (default all), optionally restricted to boolean mask `sub`."""
    if idx is not None:
        D = {k: v[idx] for k, v in D.items()}
    w = D["w"]
    base = np.ones(len(w), bool) if sub is None else (sub if idx is None else sub[idx])
    t, c, L, G = D["is_t"] & base, ~D["is_t"] & base, D["okL"], D["okG"]
    o = {}
    for lab in ("unf", "res", "ev"):
        o[f"a_{lab}_t"] = wm(D[f"post_{lab}"], w, t & L); o[f"a_{lab}_c"] = wm(D[f"post_{lab}"], w, c & L)
        o[f"a_{lab}"] = o[f"a_{lab}_t"] - o[f"a_{lab}_c"]
    o["a_pre_t"] = wm(D["pre_unf"], w, t & L); o["a_pre_c"] = wm(D["pre_unf"], w, c & L)
    o["c_share"] = o["a_res"] / o["a_unf"] if o["a_unf"] and np.isfinite(o["a_unf"]) and abs(o["a_unf"]) > 1e-9 else np.nan
    o["b_t"] = wm(D["gain"], w, t & G); o["b_c"] = wm(D["gain"], w, c & G); o["b"] = o["b_t"] - o["b_c"]
    o["gainers_t_total"] = float((w * np.nan_to_num(D["gain"]))[t & G].sum() / max(1e-12, w[t & G].sum()) * w[t].sum())
    v = D["v12"]
    for nm, m in (("t", t), ("c", c)):
        mm = m & G & np.isfinite(v)
        den = (w[mm] * v[mm]).sum()
        o[f"d_{nm}"] = float((w[mm] * v[mm] * D["gain"][mm]).sum() / den) if den > 0 else np.nan
    o["d"] = o["d_t"] - o["d_c"]
    o["d_did"] = (o["d_t"] - o["b_t"]) - (o["d_c"] - o["b_c"])
    o["e_ip"] = wm(D["gain"], w, t & G & D["ip"]); o["e_ju"] = wm(D["gain"], w, t & G & D["ju"]); o["e"] = o["e_ip"] - o["e_ju"]
    o["e_ju_vs_c"] = o["e_ju"] - o["b_c"]
    o["N_t"] = float(w[t].sum()); o["N_c"] = float(w[c].sum())
    o["n_t"] = int(t.sum()); o["n_c"] = int(c.sum()); o["nL_t"] = int((t & L).sum()); o["nL_c"] = int((c & L).sum())
    return o


def strata_index(arts):
    by = defaultdict(list)
    for k, a in enumerate(arts):
        by[a["stratum"]].append(k)
    return {h: np.array(v) for h, v in by.items()}


def boot(D, S, census, fn, B=None, seed=SEED, extra=None):
    """Stratified bootstrap: resample rows within each stratum (census strata fixed). fn(idx) -> dict of floats.
    extra: optional (n_rows, fn_extra) for an independent SRS sample (random baseline) resampled in the same replicate."""
    B = B or NB
    rng = np.random.default_rng(seed)
    draws = {h: (np.tile(ix, (B, 1)) if census.get(h) or len(ix) < 2 else ix[rng.integers(0, len(ix), size=(B, len(ix)))])
             for h, ix in S.items()}
    reps = []
    for b in range(B):
        idx = np.concatenate([draws[h][b] for h in S]) if S else np.array([], int)
        ridx = rng.integers(0, extra[0], size=extra[0]) if extra else None
        reps.append(fn(idx, ridx))
    keys = reps[0].keys() if reps else []
    out = {}
    for k in keys:
        v = np.array([r[k] for r in reps], float)
        v = v[np.isfinite(v)]
        out[k] = [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))] if len(v) >= 0.9 * B else None
    return out


def design_weights(fr_alloc, arts):
    """N_h / r_h per row (r_h = rows of stratum h that arrived)."""
    N = {a["stratum"]: a["N"] for a in fr_alloc}
    r = Counter(a["stratum"] for a in arts)
    return [N[a["stratum"]] / r[a["stratum"]] for a in arts]


def kish(w):
    w = np.asarray(w, float)
    return (len(w) * (w ** 2).sum() / w.sum() ** 2, w.sum() ** 2 / (w ** 2).sum()) if len(w) else (np.nan, 0)


def random_arrays(rb):
    arts = [{"group": "random", "snaps": a.get("snaps"), "views_12m": a.get("views_12m"), "existed_2021": a.get("existed_2021"),
             "stratum": "random", "w": 1.0} for a in (rb.get("articles") or {}).values() if a.get("existed_2021")]
    return arrays(arts) if arts else None


def rstats(R, ridx=None):
    if ridx is not None:
        R = {k: v[ridx] for k, v in R.items()}
    w, L, G = R["w"], R["okL"], R["okG"]
    v = R["v12"]; mm = G & np.isfinite(v); den = (w[mm] * v[mm]).sum()
    return {"a_unf": wm(R["post_unf"], w, L), "a_res": wm(R["post_res"], w, L), "a_pre": wm(R["pre_unf"], w, L),
            "b": wm(R["gain"], w, G), "d": float((w[mm] * v[mm] * R["gain"][mm]).sum() / den) if den > 0 else np.nan,
            "n": int(L.sum())}


def _r(x, k=4):
    return None if x is None or not np.isfinite(x) else round(float(x), k)


def _fmt(est, ci, k=2, pct=False):
    if est is None or not np.isfinite(est):
        return "n/a"
    m, u = (100, " pp") if pct else (1, "")
    s = f"{est * m:+.{k}f}{u}"
    return s + (f" [{ci[0] * m:+.{k}f}, {ci[1] * m:+.{k}f}]" if ci else "")


def _p(x, k=1):
    return "n/a" if x is None or not np.isfinite(x) else f"{x * 100:.{k}f}%"


def analyze(data_dir=None, out_md=None, chart_dir=None):
    data_dir, out_md, chart_dir = data_dir or DATA, out_md or OUT_MD, chart_dir or CHART
    m3 = json.load(open(os.path.join(data_dir, "mass3.json")))
    arts = m3["articles"]
    if not arts:
        sys.exit("analyze: mass3.json has no articles")
    alloc = m3["allocation"]
    Nh = {a["stratum"]: a["N"] for a in alloc}
    census = {a["stratum"]: a["n"] == a["N"] for a in alloc}
    wts = design_weights(alloc, arts)
    D = arrays(arts, wts)
    D_unw = dict(D); D_unw["w"] = np.ones(len(arts))
    S = strata_index(arts)
    rbp = os.path.join(data_dir, "random_baseline.json")
    R = random_arrays(json.load(open(rbp))) if os.path.exists(rbp) else None

    est = stats(D)
    ci = boot(D, S, census, lambda idx, _: stats(D, idx))
    unw = stats(D_unw)
    levels = [l for l in LEVELS if any(a.get("importance") == l for a in arts)]
    by_imp = {}
    for l in levels:
        sub = D["imp"] == l
        by_imp[l] = {"est": stats(D, sub=sub), "ci": boot(D, S, census, lambda idx, _, s=sub: stats(D, idx, s), B=max(200, NB // 2))}
    rnd = None
    if R is not None:
        def fr(idx, ridx):
            s, q = stats(D, idx), rstats(R, ridx)
            return {"t_a": s["a_unf_t"] - q["a_unf"], "c_a": s["a_unf_c"] - q["a_unf"], "t_res": s["a_res_t"] - q["a_res"],
                    "c_res": s["a_res_c"] - q["a_res"], "t_b": s["b_t"] - q["b"], "c_b": s["b_c"] - q["b"],
                    "t_d": s["d_t"] - q["d"], "c_d": s["d_c"] - q["d"],
                    "t_acc": (s["a_unf_t"] - s["a_pre_t"]) - (q["a_unf"] - q["a_pre"]),
                    "c_acc": (s["a_unf_c"] - s["a_pre_c"]) - (q["a_unf"] - q["a_pre"])}
        rnd = {"random": rstats(R), "est": fr(np.arange(len(arts)), np.arange(len(R["w"]))),
               "ci": boot(D, S, census, fr, extra=(len(R["w"]), None))}

    # ---------------------------------------------------------------- write
    side_N = {s: sum(a["N"] for a in alloc if a["side"] == s) for s in SIDES}
    side_n = {s: sum(1 for a in arts if a["group"] == s) for s in SIDES}
    k = {s: kish([w for w, a in zip(wts, arts) if a["group"] == s]) for s in SIDES}
    imp_tab = {s: {l: (sum(a["N"] for a in alloc if a["side"] == s and a["stratum"].endswith("|" + l)),
                       sum(1 for a in arts if a["group"] == s and a.get("importance") == l)) for l in LEVELS} for s in SIDES}
    L = []
    L.append("# Mass v3: design-based estimates for a defined population\n")
    L.append(f"Generated by `wikitrends/mass3.py analyze` on {_now()[:10]}. Frame drawn {m3.get('now', '')[:10]} (seed {m3.get('seed')}); "
             f"reused mass2 records measured {str(m3.get('mass2_now') or '')[:10]}. Population, sampling and estimators are "
             f"described in the `mass3.py` docstring. CIs are 95% stratified bootstraps (B={NB}, rows resampled within "
             f"side x project x importance; census strata fixed; no finite-population correction elsewhere, so CIs are "
             f"conservative). Weights are N_h / arrived_h.\n")
    L.append("## Population and sample\n")
    L.append("| Side | Importance | Population N | Sample n | Share of population |\n|---|---|---|---|---|")
    for s in SIDES:
        for l in LEVELS:
            Nn, nn = imp_tab[s][l]
            if Nn:
                L.append(f"| {s} | {l} | {Nn:,} | {nn:,} | {Nn / side_N[s] * 100:.1f}% |")
        L.append(f"| **{s}** | all | **{side_N[s]:,}** | **{side_n[s]:,}** | 100% |")
    L.append(f"\nSum of weights: topic {est['N_t']:,.0f} (N = {side_N['topic']:,}), comparison {est['N_c']:,.0f} "
             f"(N = {side_N['comparison']:,}). Kish design effect topic {k['topic'][0]:.2f} (effective n {k['topic'][1]:,.0f}), "
             f"comparison {k['comparison'][0]:.2f} (effective n {k['comparison'][1]:,.0f}). Rows reused from mass2: "
             f"{sum(a['source'] == 'mass2' for a in arts):,}; fetched: {sum(a['source'] == 'mass3' for a in arts):,}; "
             f"missing: {m3.get('missing')}. Lead panel (three leads >= {MIN_WORDS} words): topic {est['nL_t']:,}, "
             f"comparison {est['nL_c']:,}.\n")
    L.append("## Headline results (audit (a)-(e)), design-weighted vs unweighted\n")
    L.append("| Statistic | Design-weighted [95% CI] | Unweighted sample |\n|---|---|---|")
    rows = [("(a) post-war lead critical DiD, hits per 10k words (topic - comparison)", "a_unf", 2, False),
            ("    topic mean change", "a_unf_t", 2, False), ("    comparison mean change", "a_unf_c", 2, False),
            ("(b) share of leads gaining critical terms, topic - comparison", "b", 1, True),
            ("    topic share gaining", "b_t", 1, True), ("    comparison share gaining", "b_c", 1, True),
            ("(c) narrative-residual DiD, hits per 10k", "a_res", 2, False),
            ("(c) residual share of (a)", "c_share", 0, True),
            ("(d) view share on gaining leads, topic - comparison", "d", 1, True),
            ("    topic view share on gaining leads", "d_t", 1, True), ("    comparison view share", "d_c", 1, True),
            ("(d') view share minus article share, DiD", "d_did", 1, True),
            ("(e) Israel+Palestine minus Judaism, gain share", "e", 1, True),
            ("    Israel+Palestine gain share", "e_ip", 1, True), ("    Judaism gain share", "e_ju", 1, True),
            ("(e'') Judaism minus comparison", "e_ju_vs_c", 1, True)]
    for lab, key, kk, pct in rows:
        L.append(f"| {lab} | {_fmt(est[key], ci.get(key), kk, pct)} | {_fmt(unw[key], None, kk, pct)} |")
    L.append(f"\nEstimated number of topic articles whose lead gained critical terms post-war (HT total): "
             f"{est['gainers_t_total']:,.0f} [{(ci.get('gainers_t_total') or [np.nan])[0]:,.0f}, "
             f"{(ci.get('gainers_t_total') or [np.nan, np.nan])[1]:,.0f}] of {side_N['topic']:,}.\n")
    L.append("## By importance (design-weighted)\n")
    L.append("| Importance | n topic / comparison | (a) DiD per 10k | (b) gain share t vs c | (b) diff | (d) view share t vs c |\n|---|---|---|---|---|---|")
    for l in levels:
        e, c_ = by_imp[l]["est"], by_imp[l]["ci"]
        L.append(f"| {l} | {e['n_t']:,} / {e['n_c']:,} | {_fmt(e['a_unf'], c_.get('a_unf'))} | {_p(e['b_t'])} vs {_p(e['b_c'])} | "
                 f"{_fmt(e['b'], c_.get('b'), 1, True)} | {_p(e['d_t'])} vs {_p(e['d_c'])} |")
    if rnd:
        q, e, c_ = rnd["random"], rnd["est"], rnd["ci"]
        L.append("\n## Against the random-Wikipedia baseline\n")
        L.append(f"Random baseline (data/random_baseline.json, equal weights, panel n {q['n']:,}): post-war mean change "
                 f"{_fmt(q['a_unf'], None)} per 10k, residual {_fmt(q['a_res'], None)}, share gaining {_p(q['b'])}, view share on "
                 f"gaining leads {_p(q['d'])}.\n")
        L.append("| Statistic | Topic - random | Comparison - random |\n|---|---|---|")
        for lab, kt, kc, kk, pct in (("post-war mean change per 10k", "t_a", "c_a", 2, False),
                                     ("narrative residual per 10k", "t_res", "c_res", 2, False),
                                     ("share gaining", "t_b", "c_b", 1, True), ("view share on gaining leads", "t_d", "c_d", 1, True),
                                     ("post-war acceleration (post - pre) beyond random", "t_acc", "c_acc", 2, False)):
            L.append(f"| {lab} | {_fmt(e[kt], c_.get(kt), kk, pct)} | {_fmt(e[kc], c_.get(kc), kk, pct)} |")
    else:
        L.append("\n## Against the random-Wikipedia baseline\n\nNot run: data/random_baseline.json was not present.\n")
    L.append("\n## Caveats\n")
    L.append("- The population is what the named WikiProjects assess on PageAssessments at the population run; articles no "
             "project tags are outside it. Task forces and optional projects that were not found are listed in "
             "data/mass3/population.json (`skipped_projects`).\n- Reused mass2 rows were measured on mass2's date; fetched rows "
             "on this run's date, so their post-war windows differ by the gap between the two runs.\n- Leads come from the "
             "mass_narr lead measure for both sources (mass2's `narr` snapshots), not the text re-measurement used by "
             "analyze_mass2, so unweighted figures here need not equal the mass2 cards.\n- Full-text measures (b') are not "
             "collected in mass3.\n- Pre-specify these estimands before treating them as confirmatory (AUDIT section 6).\n")
    os.makedirs(os.path.dirname(out_md), exist_ok=True)
    open(out_md, "w", encoding="utf-8").write("\n".join(L))
    clean = lambda d: {kk: (_r(v) if isinstance(v, float) else v) for kk, v in d.items()}
    os.makedirs(chart_dir, exist_ok=True)
    json.dump({"side_totals": side_N, "by_importance": {s: {l: {"N": v[0], "n": v[1]} for l, v in imp_tab[s].items() if v[0]} for s in SIDES},
               "strata": [{"stratum": a["stratum"], "N": a["N"], "n": a["n"], "pi": a["pi"], "reused": a["reused"], "rule": a.get("rule")} for a in alloc]},
              open(os.path.join(chart_dir, "07_mass3_population.json"), "w"), indent=1)
    out = {"overall": {"weighted": clean(est), "ci": ci, "unweighted": clean(unw)},
           "by_importance": {l: {"weighted": clean(v["est"]), "ci": v["ci"]} for l, v in by_imp.items()},
           "random": None if not rnd else {"random": clean(rnd["random"]), "diff": clean(rnd["est"]), "ci": rnd["ci"]},
           "kish": {s: {"deff": _r(k[s][0], 3), "n_eff": _r(k[s][1], 1)} for s in SIDES}}
    json.dump(out, open(os.path.join(chart_dir, "08_mass3_estimates.json"), "w"), indent=1)
    print("analyze: wrote", out_md, flush=True)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["population", "sample", "estimate", "shard", "merge", "analyze"])
    ap.add_argument("--shard", type=int, default=0); ap.add_argument("--of", type=int, default=4)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.cmd == "population":
        population()
    elif a.cmd == "sample":
        sample()
    elif a.cmd == "estimate":
        estimate(of=a.of, check=a.check)
    elif a.cmd == "shard":
        run_shard(a.shard, a.of)
    elif a.cmd == "merge":
        merge()
    else:
        analyze()
