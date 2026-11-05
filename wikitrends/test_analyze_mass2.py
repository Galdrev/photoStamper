"""Offline end-to-end test for analyze_mass2.py (no network).

  python test_analyze_mass2.py [--n 10000] [--keep DIR]   -> exits non-zero on any failed check

1. mocked pipeline: test_mass2's fake Wikipedia -> mass2.py resolve / shard / merge -> analyze_mass2.py; every card present,
   no error cards, no username or editor hash in any output.
2. scaled fixture: ~10k articles cloned from the mocked records with every field randomised, the real mass-tier lead texts
   (data/mass_leads.json.gz, when present) and groups/relevance from data/mass_narr.json -> runtime under 10 minutes, and the
   narrative-residual card reproduces study3/holdout_results/event_mass_leads.txt.
3. missing fields: the fixture with keys deleted at random at every level, and with optional files removed -> still runs.
"""
import argparse, copy, gzip, json, os, random, shutil, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("WT_SALT", "test-salt")
os.environ["WT_NOW"] = "2026-11-05"

OK = [True]


def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg, flush=True)
    OK[0] &= bool(cond)


def run_mock_pipeline(tmp):
    import test_mass2 as T
    mass, mass2 = T.setup(tmp)
    mass2.resolve(); mass2.run_shard(0, 1); mass2.merge()
    return os.path.join(tmp, "data"), T.REAL_USERS


def run_analysis(data, out, boot=200, extra=()):
    import analyze_mass2 as AM
    t = time.time()
    res = AM.main(["--data", data, "--out", out, "--boot", str(boot), *extra])
    return res, time.time() - t


def outputs_text(out):
    blobs = []
    for root, _, fs in os.walk(out):
        for f in fs:
            blobs.append(open(os.path.join(root, f), encoding="utf-8").read())
    return "\n".join(blobs)


# ------------------------------------------------------------------ scaled fixture
DOMAINS = ["hrw.org", "amnesty.org", "aljazeera.com", "timesofisrael.com", "haaretz.com", "nytimes.com", "bbc.co.uk", "adl.org",
           "jstor.org", "books.google.com", "un.org", "972mag.com", "reuters.com", "example.org"]
CLASSES = ["Israeli press", "Arab & Palestinian press, pro-Palestinian outlets", "Rights orgs & UN", "Pro-Israel advocacy",
           "Western wire & papers", "Scholarly (books, journals)", "Other"]
CATS = ["History of Palestine", "Genocides in Asia", "Israeli apartheid", "Massacres of Jews", "Terrorism in Israel", "Villages",
        "Zionism", "21st-century genocides", "Occupied territories", "Populated places"]
SDS = ["Village in Palestine", "Palestinian village depopulated in the 1948 Nakba", "Ethnic cleansing of Palestinians", "City in Israel",
       "Ongoing genocide in the Gaza Strip", "Jewish religious text", "Region in West Asia", "Accusation of apartheid against Israel"]
CONCEPTS = ["nakba_1948", "apartheid_il", "settler_colonialism", "gaza_genocide", "occupation_il", "genocide_generic", "jewish_history",
            "antisemitism"]
TERMS = ["settler_colonial", "apartheid", "genocide", "ethnic_cleansing", "occupation", "nakba_expulsion", "war_crimes"]


def h12(rng):
    return "%012x" % rng.getrandbits(48)


def ts_between(rng, a="2021-01-02", b="2026-11-01"):
    import datetime as dt
    t0 = dt.datetime.fromisoformat(a + "T00:00:00+00:00").timestamp(); t1 = dt.datetime.fromisoformat(b + "T00:00:00+00:00").timestamp()
    return dt.datetime.fromtimestamp(rng.uniform(t0, t1), dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def synth(tpl, title, grp, project, rng, base_c, lead_crit, pool):
    r = copy.deepcopy(tpl)
    r.update({"title": title, "frame_titles": [title], "group": grp, "project": project, "stratum": grp})
    r.pop("atrocity_case", None)
    busy = rng.lognormvariate(3.5, 1.4)
    for k, a in r["at"].items():
        if not isinstance(a, dict):
            continue
        art = a.get("article")
        if isinstance(art, dict) and "same_as" not in art:
            art["short_desc"] = rng.choice(SDS) if rng.random() < 0.9 else None
            art["categories"] = sorted(rng.sample(CATS, rng.randint(0, 4)))
            tot = rng.randint(0, 12)
            cl = {}
            for _ in range(tot):
                c = rng.choice(CLASSES); cl[c] = cl.get(c, 0) + 1
            cl["_total"] = tot
            art["lead_refs_resolved"] = cl
            art["lead_domains"] = {d: rng.randint(1, 3) for d in rng.sample(DOMAINS, rng.randint(0, 5))}
            art["concept_groups"] = sorted(rng.sample(CONCEPTS, rng.randint(0, 3)))
            art["see_also"] = rng.sample(["Nakba", "Zionism", "Israeli apartheid", "Gaza genocide", "Foo", "Bar"], rng.randint(0, 3))
            if art.get("infobox"):
                art["infobox"]["fields"] = {"type": rng.choice(["Genocide, ethnic cleansing", "War", "Village", "Massacre"])}
            art["lead_words"] = rng.randint(20, 400)
        narr = a.get("narr")
        if isinstance(narr, dict) and "same_as" not in narr:
            narr["c"] = dict(base_c)
        a["protection"] = rng.choice([{}, {"edit": "extendedconfirmed"}, {"edit": "autoconfirmed"}, {}, {"edit": "extendedconfirmed", "move": "sysop"}])
        if a.get("title"):
            a["title"] = title
    for w, x in (r.get("win") or {}).items():
        e = int(busy * (1.5 if w == "w2" else 1.0))
        x["edits"] = e; x["anon"] = int(e * rng.uniform(0, 0.3)); x["bytes_added"] = int(e * rng.uniform(20, 300))
        x["bytes_removed"] = int(x["bytes_added"] * rng.uniform(0.3, 1.1)); x["big_add"] = rng.randint(0, 3); x["big_remove"] = rng.randint(0, 2)
        acc = x.get("accounts") or {}
        acc["n_edits"] = int(e * 0.8)
        for f in ("share_age_lt30", "share_age_lt365", "share_editcount_lt500", "share_ec_now", "share_indef_now"):
            acc[f] = round(rng.uniform(0, 0.5 if f != "share_ec_now" else 1), 3)
        acc["median_age_days"] = rng.uniform(100, 5000)
        x["accounts"] = acc
    pv = r.get("pageviews") or {}
    lvl = rng.lognormvariate(7, 2)
    pv["monthly"] = {"start": "202101", "views": [int(lvl * rng.uniform(0.5, 1.5)) if rng.random() > 0.02 else None for _ in range(70)]}
    pv["titles"] = [title] + (["Old " + title] if rng.random() < 0.1 else [])
    pv["total_by_title"] = {t: int(lvl * 70 * (1 if i == 0 else 0.2)) for i, t in enumerate(pv["titles"])}
    r["pageviews"] = pv
    for k in ("2023", "now"):
        src = r.get("wikidata_2023") if k == "2023" else (r.get("now") or {}).get("wikidata")
        if isinstance(src, dict):
            src["descriptions"] = {"en": rng.choice(SDS).lower(), "he": rng.choice(["x", "y"])}
    r["created_in_window"] = None
    r["moves"] = [{"ts": ts_between(rng), "from": "Old " + title, "to": title, "rm": rng.random() < 0.5}] if rng.random() < 0.05 else []
    # per-event detail
    evs = []
    n_ev = int(rng.expovariate(1 / (0.2 + lead_crit))) if rng.random() < 0.4 else 0
    for _ in range(min(n_ev, 60)):
        u = rng.choice(pool)
        evs.append({"ts": ts_between(rng), "term": rng.choice(TERMS), "kind": rng.choice(["insert", "remove"]), "revid": rng.randint(1, 10 ** 9),
                    "exact": rng.random() < 0.95, "after_ts": None, "restore": rng.random() < 0.3, "reverted": rng.random() < 0.3,
                    "u": u, "anon": False,
                    "acct": {"age_d": rng.randint(1, 6000), "lt500": rng.random() < 0.1, "ext": rng.random() < 0.9, "indef": rng.random() < 0.15,
                             "partial": rng.random() < 0.2, "breason": rng.choice(["sock", "arb_enforcement", "other", None])} if rng.random() < 0.8 else None,
                    "lw": None})
    evs.sort(key=lambda e: e["ts"])
    disc = [{"kind": rng.choice(["rfc", "rm"]), "ts": ts_between(rng), "closed": rng.random() < 0.6, "formal": True,
             "result": rng.choice(["moved", "not moved", "no consensus", "other", None])} for _ in range(int(rng.expovariate(1 / (busy / 200 + 0.01))))][:40]
    plog = [{"ts": ts_between(rng, "2015-01-01"), "action": "protect", "details": [{"type": "edit", "level": "extendedconfirmed", "expiry": "infinite"}],
             "src": "details"}] if rng.random() < 0.3 else []
    return r, {"lead_events": evs, "discussions": disc, "protection_log": plog}


def scaled_fixture(src_data, dst, n, seed=7):
    rng = random.Random(seed)
    m = json.load(open(os.path.join(src_data, "mass2.json")))
    tpls = [a for a in m["articles"] if a["title"] in ("Zionism", "Israel", "Nakba", "Kosovo", "Kashmir", "Hebron")]
    atro = [a for a in m["articles"] if a.get("stratum") == "atrocity" or a["title"] == "Gaza genocide"]
    old_ev = json.load(gzip.open(os.path.join(src_data, "mass2_events.json.gz"), "rt"))["articles"]
    real_leads, mn = None, {}
    rl = os.path.join(HERE, "data", "mass_leads.json.gz"); mp = os.path.join(HERE, "data", "mass_narr.json")
    if os.path.exists(rl) and os.path.exists(mp):
        real_leads = json.load(gzip.open(rl, "rt"))["leads"]
        mn = json.load(open(mp))["articles"]
    titles = [t for t in (real_leads or {}) if t in mn][:n] if real_leads else []
    if len(titles) < n:
        titles += [f"Synthetic {i}" for i in range(n - len(titles))]
    pool = [h12(rng) for _ in range(3000)]
    arts, det, leads, eds = [], {}, {}, {}
    for t in titles:
        info = mn.get(t, {})
        grp = info.get("group") or rng.choice(["topic", "comparison"])
        proj = info.get("project") or rng.choice(["Israel", "Palestine", "Judaism", "Ukraine", "India", "Armenia"])
        both = bool(info.get("baseline_both_groups")); land = info.get("baseline_landconf_per_1000") or 0.0
        wds = max(1, (info.get("snaps") or [{}])[0].get("words") or info.get("lead_words_first") or 100) if info else 100
        base_c = {"_words": wds, "LANDCONF": land * wds / 1000}
        if both:
            from mass_narr import groups_for
            for gk in groups_for({"group": grp, "project": proj})[0]:
                base_c["G_" + gk] = 1
        ls = real_leads.get(t) if real_leads else None
        crit_now = 0
        if ls is None and real_leads is None:
            ls = [f"{t} is a place. It was described as genocide in {2020 + i}. More text about the land and the war." * 3 for i in range(3)]
        elif ls is None:
            ls = [None, None, None]          # padding rows: no lead text (kept out of the reference comparison)
        r, d = synth(rng.choice(tpls), t, grp, proj, rng, base_c, crit_now, pool)
        arts.append(r); det[t] = d; leads[t] = ls
        eds[t] = {"w1": sorted(rng.sample(pool, 3)), "w2": sorted(rng.sample(pool, 3))}
    for a in atro:
        arts.append(copy.deepcopy(a)); det[a["title"]] = old_ev.get(a["title"], {})
        leads[a["title"]] = [f"The {a['title']} was a genocide. Scholars describe it as genocide.", None,
                             f"The {a['title']} is a genocide against a people. Some have alleged genocide."]
    m["articles"] = arts
    os.makedirs(dst, exist_ok=True)
    json.dump(m, open(os.path.join(dst, "mass2.json"), "w"))
    json.dump({"note": "fixture", "articles": det}, gzip.open(os.path.join(dst, "mass2_events.json.gz"), "wt"))
    json.dump({"dates": ["2021-01-01", "2023-07-01", "now"], "leads": leads}, gzip.open(os.path.join(dst, "mass2_leads.json.gz"), "wt"))
    json.dump({"windows": ["w1", "w2"], "editors": eds}, gzip.open(os.path.join(dst, "mass2_editors.json.gz"), "wt"))
    shutil.copy(os.path.join(src_data, "mass2_summary.json"), dst)
    return len(arts), bool(real_leads), pool


def damage(x, rng, p):
    """Delete keys at random at every level (and null some values)."""
    if isinstance(x, dict):
        for k in list(x):
            if k == "title":
                continue
            u = rng.random()
            if u < p:
                del x[k]
            elif u < 1.5 * p:
                x[k] = None
            else:
                damage(x[k], rng, p)
    elif isinstance(x, list):
        for v in x:
            damage(v, rng, p)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, default=10000); ap.add_argument("--keep")
    a = ap.parse_args()
    tmp = a.keep or tempfile.mkdtemp()
    os.makedirs(tmp, exist_ok=True)
    try:
        # ---------------- 1. mocked pipeline
        data, real_users = run_mock_pipeline(os.path.join(tmp, "mock"))
        out = os.path.join(tmp, "out_mock")
        res, sec = run_analysis(data, out)
        cards = res["cards"]
        check(len(cards) == 12 and [c["rank"] for c in cards] == list(range(1, 13)), f"12 cards in order ({len(cards)})")
        check(not [c["id"] for c in cards if c.get("error")], f"no error cards on mocked output: {[c['id'] for c in cards if c.get('error')]}")
        need = {"title", "what_we_see", "chart", "confidence", "so_what", "caveat", "examples"}
        check(all(need <= set(c) and c["confidence"] in ("STRONG", "SUGGESTIVE", "ANECDOTE") for c in cards), "card format and confidence labels")
        files = os.listdir(os.path.join(out, "chart_data"))
        check(len(files) >= 12 and os.path.exists(os.path.join(out, "cards.md")), f"chart_data ({len(files)} files) and cards.md written")
        check(all(os.path.exists(os.path.join(out, p.strip())) for c in cards for p in str((c.get("chart") or {}).get("data", "")).split(",") if p.strip()),
              "every chart data path in the cards exists")
        txt = outputs_text(out)
        leaked = [u for u in real_users if f'"{u}"' in txt or f" {u} " in txt or f"*{u}*" in txt]
        check(not leaked, f"no usernames in analysis outputs ({leaked})")
        ev = json.load(gzip.open(os.path.join(data, "mass2_events.json.gz"), "rt"))["articles"]
        hs = {e["u"] for x in ev.values() for e in x.get("lead_events") or [] if e.get("u")}
        check(hs and not [h for h in hs if h in txt], f"no editor hashes in outputs ({len(hs)} hashes checked)")
        atro = next(c for c in cards if c["id"] == "atrocity_voice")
        check("Masalit genocide" in json.dumps(atro) or "El Fasher" in json.dumps(atro), "atrocity card covers the atrocity stratum")
        # ---------------- 2. scaled fixture
        big = os.path.join(tmp, "big")
        n, real, pool = scaled_fixture(data, big, a.n)
        print(f"fixture: {n} articles (real lead texts: {real})", flush=True)
        res, sec = run_analysis(big, os.path.join(tmp, "out_big"), boot=1000)
        cards = res["cards"]
        check(sec < 600, f"{n} articles analysed in {sec:.0f}s (< 600s)")
        check(not [c["id"] for c in cards if c.get("error")], f"no error cards at scale: {[(c['id'], c.get('error')) for c in cards if c.get('error')]}")
        txt = outputs_text(os.path.join(tmp, "out_big"))
        check(not [h for h in pool if h in txt], "no fixture editor hashes in outputs")
        nr = next(c for c in cards if c["id"] == "narrative_residual")
        vr = nr["numbers"].get("vs_reference") or []
        if real:
            check(len(vr) == 12 and all(r["match"] for r in vr), f"narrative residual reproduces event_mass_leads.txt: "
                  f"{sum(r['match'] for r in vr)}/{len(vr)} rows; " + "; ".join(f"{r['subset']} {r['window']} {r['outcome']} {r['did']} vs {r['ref_did']} n={r['n']} vs {r['ref_n']}" for r in vr))
            close = [r for r in vr if all(abs(x - y) <= 0.01 * y for x, y in zip(r["n"], r["ref_n"]))]
            check(len(close) == len(vr), f"article counts within 1% of the reference ({len(close)}/{len(vr)})")
        # ---------------- 3. missing fields
        rng = random.Random(3)
        dmg = os.path.join(tmp, "damaged")
        shutil.copytree(big, dmg)
        m = json.load(open(os.path.join(dmg, "mass2.json")))
        m["articles"] = m["articles"][:1500] + [{"title": "Bare record"}, {"title": "Odd", "at": [], "win": "x", "pageviews": 3}]
        damage(m["articles"], rng, 0.08)
        json.dump(m, open(os.path.join(dmg, "mass2.json"), "w"))
        evd = json.load(gzip.open(os.path.join(dmg, "mass2_events.json.gz"), "rt"))
        damage(evd, rng, 0.05)
        json.dump(evd, gzip.open(os.path.join(dmg, "mass2_events.json.gz"), "wt"))
        res, _ = run_analysis(dmg, os.path.join(tmp, "out_dmg"), boot=100)
        errs = [(c["id"], c.get("error")) for c in res["cards"] if c.get("error")]
        check(not errs, f"randomly deleted fields: no crash, no error cards ({errs})")
        for f in ("mass2_events.json.gz", "mass2_leads.json.gz", "mass2_editors.json.gz", "mass2_summary.json"):
            os.remove(os.path.join(dmg, f))
        res, _ = run_analysis(dmg, os.path.join(tmp, "out_min"), boot=50)
        errs = [(c["id"], c.get("error")) for c in res["cards"] if c.get("error")]
        check(len(res["cards"]) == 12 and not errs, f"only mass2.json present: all 12 cards, no error cards ({errs})")
    finally:
        if not a.keep:
            shutil.rmtree(tmp, ignore_errors=True)
    print("ALL PASS" if OK[0] else "SOME CHECKS FAILED")
    sys.exit(0 if OK[0] else 1)


if __name__ == "__main__":
    main()
