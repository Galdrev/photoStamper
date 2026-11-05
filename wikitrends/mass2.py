"""Mass v2 collector: the pilot's best signals (patterns/pilot_eval/EVAL.md section 4, mass_scope.json) for the whole mass frame.

  python mass2.py resolve                     -> data/mass/frame2.json   (one job: resolve + dedupe titles, page info and
                                                                          Wikidata "now" batched, concept alias table)
  python mass2.py shard --shard I --of N      -> data/mass/m2_I.json.gz  (checkpointed via mass._run; fails loudly >5% errors)
  python mass2.py merge                       -> data/mass2.json (compact, per article), data/mass2_leads.json.gz,
                                                 data/mass2_events.json.gz (per-event lists), data/mass2_editors.json.gz,
                                                 data/mass2_summary.json
  python mass2.py estimate                    -> request / wall-time estimate from the mass edit distribution (offline)
  MASS_LIMIT=40 ...                           -> test mode (first 40 rows)

Per article (one fetch of each snapshot serves every snapshot signal):
  free   history rvprop ids|timestamp|user|size|comment|tags|flags|sha1 -> edit sizes, tags, summary classes, moves (RM flag
         tightened, vandal move/revert pairs flagged), titles at dates (None before creation); 3 snapshots (2021-01-01,
         2023-07-01, now) -> short description, infobox, lead image, categories, See also, navboxes, maintenance/pp tags,
         alias-resolved concept links, lead citation classes + domains (named refs resolved), P/J displacement split,
         and the mass_narr narrative features (event filter applied, lead prose stored separately)
  scale  page info + Wikidata now (batched in `resolve`), account facts (aggregated; salted hashes only), talk now, talk
         history, RfC/RM scan with per-discussion dates, pageviews summed over former titles (partial month excluded),
         Wikidata 2023-07-01, protection log (old-format entries parsed, former titles followed, "now" anchored on page
         info), lead term events (one continuous sequence 2021 -> now, seeded from the 2021 snapshot; full for pages up to
         WT_LEAD_GRID x 50 revisions, otherwise a time-stratified grid refined around every term flip: coverage always
         reaches "now"; restorations tagged; per-event hashed account flags)
  opt.   LiftWing revert risk on up to 6 event revisions per article, only with WT_LIFTWING=1
Lead events run on every page (the 300k-request budget allows it: ~3.1 requests/article with the grid). WT_LEAD_SCOPE=cheap
falls back to the evaluator's cheaper variant: topic and atrocity pages plus comparison pages whose lead contains a tracked
term at any snapshot (~1.4 requests/article).
Privacy: no username, raw edit summary, block reason or closer text is written. Editors are salted hashes (WT_SALT).
"""
import argparse, glob, gzip, hashlib, json, math, os, re, sys, time
from collections import Counter
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wt_net                   # noqa: E402
import analyze as A             # noqa: E402
import explore as E             # noqa: E402
import pilot as P               # noqa: E402
import mass as M                # noqa: E402
import mass_narr as MN          # noqa: E402
from corpus import ATROCITY_CASES   # noqa: E402

KIND = "m2"
LEAD_GRID = int(os.environ.get("WT_LEAD_GRID", "8"))        # grid requests per article (x50 revisions); full below that
LEAD_REFINE = int(os.environ.get("WT_LEAD_REFINE", "40"))   # refinement requests per article around flips
LEAD_ALL = os.environ.get("WT_LEAD_SCOPE", "all") != "cheap"     # budget allows all pages (see estimate)
LW_MAX = 6
P.LW_ON[0] = os.environ.get("WT_LIFTWING") == "1"          # LiftWing off unless asked for
MAX_FORMER = 5                                              # former titles followed for pageviews / protection log
MAX_EVENTS = 3000
ALIAS, GROUP_OF = {}, {}                                    # concept alias table (lower-case link target -> concept)

# evaluator's concept groups (EVAL 3.3); keys are WATCH_LINKS names, resolved to current titles in `resolve`
CONCEPT_GROUPS = {"Nakba": "nakba_1948", "1948 Palestinian expulsion and flight": "nakba_1948",
                  "Israeli apartheid": "apartheid_il", "Settler colonialism": "settler_colonialism",
                  "Zionism as settler colonialism": "settler_colonialism", "Gaza genocide": "gaza_genocide",
                  "Israeli occupation of the West Bank": "occupation_il", "Israeli-occupied territories": "occupation_il",
                  "Occupied Palestinian territories": "occupation_il", "Genocide": "genocide_generic",
                  "Ethnic cleansing": "genocide_generic", "Land of Israel": "jewish_history", "Israelites": "jewish_history",
                  "Jewish history": "jewish_history", "Jewish exodus from the Muslim world": "jewish_exodus",
                  "Antisemitism": "antisemitism", "New antisemitism": "antisemitism"}
INFOBOX_KEYS = {"type", "result", "status", "location", "date", "target", "targets", "perpetrator", "perpetrators", "victims",
                "deaths", "fatalities", "casualties", "motive", "partof", "territory", "conventional_long_name", "common_name",
                "native_name", "name", "ideology", "purpose", "founded", "established", "government_type", "sovereignty_type",
                "methods", "accused", "charges", "outcome", "cause", "attack_type", "weapons", "region"}


# ------------------------------------------------------------------ dates
def _midnight(s=None):
    if s:
        d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        d = d.astimezone(timezone.utc) if d.tzinfo else d
    else:
        d = datetime.now(timezone.utc)
    return d.strftime("%Y-%m-%dT00:00:00Z")


def set_now(now):
    """One fixed "now" for the whole run (shards may run on different days): rewrites the pilot's dates/windows in place."""
    P.NOW = now
    P.DATES.update({"2021-01-01": "2021-01-01T00:00:00Z", "2023-07-01": "2023-07-01T00:00:00Z", "now": now})
    P.WINDOWS.update({"w1": ("2021-01-01T00:00:00Z", "2023-07-01T00:00:00Z"), "w2": ("2023-07-01T00:00:00Z", now),
                      "war": (P.WAR, now)})


set_now(_midnight(os.environ.get("WT_NOW")))


def frame2_path():
    return os.path.join(M.OUT, "frame2.json")


# ------------------------------------------------------------------ resolve (one job before the shards)
INFO = {"prop": "info|pageprops|description|pageassessments|redirects", "inprop": "protection|watchers|visitingwatchers|talkid",
        "ppprop": "wikibase_item|disambiguation", "palimit": "max", "rdlimit": "max", "rdnamespace": 0, "rdprop": "title"}


def resolve_batch(titles, max_pages=20):
    """Page info for up to 50 titles in one call (+ continuation for redirects/assessments). -> {input title: page or None}."""
    pages, mapping, cont, n, trunc = {}, {}, {}, 0, False
    while True:
        j = P.q({"action": "query", "titles": "|".join(titles), "redirects": 1, **INFO, **cont})
        qy = j.get("query") or {}
        for x in (qy.get("normalized") or []) + (qy.get("redirects") or []):
            mapping[x["from"]] = x["to"]
        for p in qy.get("pages") or []:
            d = pages.setdefault(p.get("title"), {"title": p.get("title"), "redirects": []})
            for k in ("pageid", "length", "watchers", "visitingwatchers", "description", "descriptionsource", "talkid",
                      "missing", "invalid", "protection"):
                if k in p:
                    d[k] = p[k]
            d.setdefault("pageprops", {}).update(p.get("pageprops") or {})
            d.setdefault("pa", {}).update(p.get("pageassessments") or {})
            d["redirects"] += [r["title"] for r in p.get("redirects") or []]
        n += 1
        if "continue" not in j:
            break
        if n >= max_pages:
            trunc = True; break
        cont = j["continue"]

    def canon(t):
        for _ in range(6):
            if t not in mapping:
                break
            t = mapping[t]
        return t
    out = {}
    for t in titles:
        d = pages.get(canon(t))
        if d is not None:
            d["redirects_truncated"] = trunc
        out[t] = d
    return out


def pinfo(d):
    pp = d.get("pageprops") or {}
    return {"pageid": d.get("pageid"), "length": d.get("length"), "watchers": d.get("watchers"),
            "visitingwatchers": d.get("visitingwatchers"),
            "protection": [{"type": x.get("type"), "level": x.get("level"), "expiry": x.get("expiry")} for x in d.get("protection") or []],
            "description": d.get("description"), "description_source": d.get("descriptionsource"),
            "assessments": d.get("pa") or {}, "qid": pp.get("wikibase_item"), "disambiguation": "disambiguation" in pp,
            "talk_exists": bool(d.get("talkid")), "n_redirects": len(set(d.get("redirects") or [])),
            "redirects_truncated": d.get("redirects_truncated", False)}


def wd_now_batch(qids):
    j = P.q({"action": "wbgetentities", "ids": "|".join(qids), "props": "labels|descriptions|aliases|sitelinks",
             "languages": "|".join(P.WD_LANGS)}, url=P.WD, core=False)
    out = {}
    for q, e in ((j or {}).get("entities") or {}).items():
        if e and "missing" not in e:
            w = P.parse_wikidata(json.dumps(e))
            if w:
                w.pop("n_claims", None); w.pop("p31", None)      # claims not fetched in the batch (see the 2023 snapshot)
            out[q] = w
    return out


def concept_table():
    """Alias table for the watch-list concepts: every redirect to each concept's current page -> that page."""
    info = {}
    for i in range(0, len(P.WATCH_LINKS), 50):
        info.update(resolve_batch(P.WATCH_LINKS[i:i + 50]))
    alias, groups = {}, {}
    for w in P.WATCH_LINKS:
        d = info.get(w)
        if not d or d.get("missing") or d.get("invalid"):
            print(f"WARNING: watch concept {w!r} did not resolve", file=sys.stderr); continue
        c = d["title"]
        groups[c] = CONCEPT_GROUPS.get(w, groups.get(c) or c)
        for a in [w, c] + (d.get("redirects") or []):
            alias.setdefault(a.lower(), c)
    inbound = {c: P.linksto(c) for c in sorted(set(alias.values()))}
    return alias, groups, inbound


def resolve():
    fr = json.load(open(os.path.join(M.OUT, "frame.json")))
    rows = [{"title": r["title"], "group": r["group"], "project": r.get("project"), "importance": r.get("importance"),
             "stratum": r["group"]} for r in fr["rows"]]
    lim = int(os.environ.get("MASS_LIMIT", "0"))
    if lim:
        rows = rows[:lim]
    for case, ts in ATROCITY_CASES.items():
        rows += [{"title": t, "group": "comparison", "project": None, "importance": None, "stratum": "atrocity", "case": case}
                 for t in ts]
    titles = list(dict.fromkeys(r["title"] for r in rows))
    info = {}
    wt_net.heartbeat("resolve", 0, len(titles), force=True)
    for i in range(0, len(titles), 50):
        info.update(resolve_batch(titles[i:i + 50]))
        wt_net.heartbeat("resolve", min(len(titles), i + 50), len(titles))
    out, by_c = [], {}
    dropped = {"missing": [], "disambiguation": [], "duplicate": []}
    for r in rows:
        d = info.get(r["title"])
        if d is None or d.get("missing") or d.get("invalid"):
            dropped["missing"].append(r["title"]); continue
        pi = pinfo(d)
        if pi["disambiguation"]:
            dropped["disambiguation"].append(r["title"]); continue
        c = d["title"]
        if c in by_c:                                          # redirect (or atrocity candidate) resolving to a kept page
            k = by_c[c]
            if r["title"] not in k["frame_titles"]:
                k["frame_titles"].append(r["title"])
            if r["stratum"] == "atrocity":
                k["atrocity_case"] = r["case"]
            elif r["group"] != k["group"]:
                k["group_conflict"] = True
            dropped["duplicate"].append({"title": r["title"], "canonical": c}); continue
        rec = {**r, "title": c, "frame_titles": [r["title"]], "pi": pi}
        if r["stratum"] == "atrocity":
            rec["atrocity_case"] = r["case"]
        by_c[c] = rec; out.append(rec)
    qids = sorted({r["pi"]["qid"] for r in out if r["pi"].get("qid")})
    wd = {}
    for i in range(0, len(qids), 50):
        wd.update(wd_now_batch(qids[i:i + 50]))
        wt_net.heartbeat("resolve-wikidata", min(len(qids), i + 50), len(qids))
    for r in out:
        r["wd_now"] = wd.get(r["pi"].get("qid"))
    alias, groups, inbound = concept_table()
    cases = {case: sorted({r["title"] for r in out if r.get("atrocity_case") == case}) for case in ATROCITY_CASES}
    for case, got in cases.items():
        print(f"atrocity {case}: {got or 'NONE RESOLVED'}", flush=True)
    res = {"now": P.NOW, "rows": out, "dropped": dropped, "atrocity_resolved": cases, "aliases": alias, "concept_groups": groups,
           "concept_inbound_now": inbound, "n_frame_rows": len(fr["rows"]),
           "requests": {k: v for k, v in wt_net.C.items() if k not in ("latency_sum", "started")}}
    os.makedirs(M.OUT, exist_ok=True)
    json.dump(res, open(frame2_path(), "w"))
    wt_net.heartbeat("resolve-done", len(out), len(titles), force=True)
    print(f"resolve: {len(rows)} rows -> {len(out)} unique pages; dropped {len(dropped['missing'])} missing, "
          f"{len(dropped['disambiguation'])} disambiguation, {len(dropped['duplicate'])} duplicates; "
          f"{wt_net.C['requests']} requests", flush=True)
    n_frame = sum(1 for r in rows if r["stratum"] != "atrocity")
    if sum(1 for r in out if r["stratum"] != "atrocity") < 0.8 * n_frame:
        sys.exit("resolve: fewer than 80% of frame rows resolved to unique pages - refusing to start shards")
    if not all(cases.values()):
        print("::warning::an atrocity case resolved to no page: " + ", ".join(c for c, v in cases.items() if not v), flush=True)
    return res


# ------------------------------------------------------------------ snapshot parsing
SEC0 = re.compile(r"^=+[^=\n].*?=+[ \t]*$", re.M)
REF_DEF = re.compile(r"<ref\s+name\s*=\s*[\"']?([^\"'>/]+?)[\"']?\s*>(.*?)</ref\s*>", re.S | re.I)
REF_USE = re.compile(r"<ref\s+name\s*=\s*[\"']?([^\"'>/]+?)[\"']?\s*/\s*>", re.I)
REF_BODY = re.compile(r"<ref(?:\s[^>]*)?(?<!/)>(.*?)</ref\s*>", re.S | re.I)
SCHOLARLY = re.compile(r"\{\{\s*cite (?:book|journal|thesis)|\bdoi\s*=|\bisbn\s*=|\{\{\s*(?:sfn|harvnb)", re.I)


def section0(wt):
    """MediaWiki section 0 (text before the first heading of any level), as rvsection=0 returns it."""
    m = SEC0.search(wt)
    return wt[:m.start()] if m else wt


def lead_citations(wt, lead):
    """Lead citations with named-ref reuse resolved: per-domain counts and source classes."""
    defs = {n.strip(): b for n, b in REF_DEF.findall(wt)}
    bodies = REF_BODY.findall(lead) + [defs[n.strip()] for n in REF_USE.findall(lead) if n.strip() in defs]
    doms, cls = Counter(), Counter()
    for b in bodies:
        ds = [d.lower() for d in E.URL.findall(b)]
        for d in set(ds):
            doms[d] += 1
        c = next((E.classify(d) for d in ds if E.classify(d)), None)
        if not c and SCHOLARLY.search(b):
            c = "Scholarly (books, journals)"
        cls[c or "Other"] += 1
    cls["Scholarly (books, journals)"] += len(re.findall(r"\{\{\s*(?:sfn|sfnp|harvnb)\s*\|", lead, re.I))
    cls["_total"] = sum(v for k, v in cls.items() if not k.startswith("_"))
    return dict(doms.most_common(60)), {k: v for k, v in cls.items() if v}


def concepts(links):
    return sorted({ALIAS[l.lower()] for l in links if l.lower() in ALIAS})


def compact_article(wt):
    """pilot.parse_article + alias-resolved concept links + lead domains; full link lists and headings reduced."""
    p = P.parse_article(wt)
    if p is None or p.get("redirect"):
        return p
    lead = A.split_lead(wt)
    links = p.pop("links")
    p["concepts"] = concepts(links)
    p["concepts_lead"] = concepts(P.wikilinks(lead))
    p["concept_groups"] = sorted({GROUP_OF.get(c, c) for c in p["concepts"]})
    p.pop("lead_templates", None)
    p["heading_h"] = sorted({hashlib.md5(x.lower().encode()).hexdigest()[:6] for x in p.pop("headings")})
    ib = p.get("infobox")
    if ib:
        crit = lambda v: any(A.count(k, v) for k in A.CRITICAL)
        ib["fields"] = dict(list({k: v for k, v in ib["fields"].items() if k in INFOBOX_KEYS or crit(v)}.items())[:30])
    p["lead_domains"], p["lead_refs_resolved"] = lead_citations(wt, lead)
    return p


# ------------------------------------------------------------------ moves, titles
RM_TIGHT = re.compile(r"requested move|\bWP:RM\b|\bper RM\b|\bRM (?:clos\w*|discussion|result)|closed RM|move request|"
                      r"#Requested move|WP:RMNAC|WP:RMTR|technical request", re.I)


def clean_moves(revs, moves):
    """Tighten the RM flag on the pilot's move list and flag move/revert pairs (A->B then B->A within 90 days)."""
    reasons = {}
    for r in revs:
        mv = P.MOVE.search(r.get("comment") or "")
        if mv:
            reasons[r["timestamp"]] = mv.group(3) or ""
    out = [{**m, "rm": bool(RM_TIGHT.search(reasons.get(m["ts"], "")))} for m in moves]
    for i, a in enumerate(out):
        for b in out[i + 1:]:
            if b["from"] == a["to"] and b["to"] == a["from"] and P.ep(b["ts"]) - P.ep(a["ts"]) < 90 * 86400:
                a["reverted"] = True; b["revert_of_move"] = True
                if not RM_TIGHT.search(reasons.get(b["ts"], "")):
                    a["rm"] = False
                break
    return out


def title_at(current, moves, date, created, snap_meta):
    if (created and date < created) or not snap_meta:
        return None                                            # page did not exist yet
    return P.title_at(current, [m for m in moves if not (m.get("reverted") or m.get("revert_of_move"))], date)


def former_titles(current, moves):
    seen = []
    for m in moves:
        if m.get("reverted") or m.get("revert_of_move"):
            continue
        if m["from"] != current and m["from"] not in seen and not P.NS_PREFIX.match(m["from"]):
            seen.append(m["from"])
    return seen[:MAX_FORMER]


# ------------------------------------------------------------------ pageviews
def pageviews(titles):
    """Monthly user views (all-access) summed over the current and former titles; the partial current month is excluded."""
    y, m = int(P.NOW[:4]), int(P.NOW[5:7])
    py, pm = (y, m - 1) if m > 1 else (y - 1, 12)
    end, cur = f"{py}{pm:02d}0100", f"{y}{m:02d}"
    tot, per, any_ = Counter(), {}, False
    for t in titles:
        q = P.requests.utils.quote(t.replace(" ", "_"), safe="")
        j = wt_net.get_json(P.PV.format(acc="all-access", t=q, end=end), {}, tries=4, ok404=True)
        series = {i["timestamp"][:6]: i["views"] for i in j["items"] if i["timestamp"][:6] < cur} if j and "items" in j else None
        per[t] = sum(series.values()) if series else None
        for k, v in (series or {}).items():
            tot[k] += v; any_ = True
    return {"titles": titles, "total_by_title": per, "monthly": dict(sorted(tot.items())) if any_ else None}


def views_in(pv, w):
    a, b = P.WINDOWS[w]
    mon = [k for k in (pv.get("monthly") or {}) if a[:4] + a[5:7] <= k < b[:4] + b[5:7]]
    return {"per_month": (sum(pv["monthly"][k] for k in mon) / len(mon)) if mon else None, "months": len(mon)}


# ------------------------------------------------------------------ protection (EVAL 1.3 problem 3)
PROT_OLD = re.compile(r"\[(edit|move|create|upload)=(\w+)\]\s*\((?:expires ([^()]*?)\s*(?:\(UTC\))?|indefinite|infinite|infinity)\)", re.I)
PROT_OLDEST = re.compile(r"\[edit=(\w+):move=(\w+)\]", re.I)


def _expiry(s):
    for fmt in ("%H:%M, %d %B %Y", "%H:%M, %B %d, %Y", "%d %B %Y"):
        try:
            return datetime.strptime(s.strip().rstrip(","), fmt).strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            pass
    return None


def log_entries(title, until=None):
    """Protection log of one title. Old entries without `details` are parsed from params.description or the comment
    (in memory only). Returns (entries, move_prot sources) or (None, []) on failure."""
    out, srcs = [], []
    for j in P.paged({"action": "query", "list": "logevents", "letype": "protect", "letitle": title, "ledir": "newer",
                      "lelimit": "max", "leprop": "timestamp|details|type|comment"}, core=False, max_pages=5):
        if "_failed" in j:
            return None, []
        if "_truncated" in j:
            break
        for e in j.get("query", {}).get("logevents", []):
            ts, act, pr = e.get("timestamp"), e.get("action"), e.get("params") or {}
            if until and ts and ts >= until:
                continue
            det = [{"type": d.get("type"), "level": d.get("level"), "expiry": d.get("expiry")} for d in pr.get("details") or []]
            src = "details"
            if not det and act in ("protect", "modify"):
                txt = " ".join(str(x) for x in (pr.get("description"), e.get("comment")) if x)
                det = [{"type": t.lower(), "level": lv, "expiry": (_expiry(ex) if ex else "infinity")} for t, lv, ex in PROT_OLD.findall(txt)]
                if not det:
                    m = PROT_OLDEST.search(txt)
                    det = [{"type": "edit", "level": m.group(1), "expiry": "infinity"},
                           {"type": "move", "level": m.group(2), "expiry": "infinity"}] if m else []
                src = "old_format" if det else "unparsed"
            if act == "move_prot":
                src = "move_prot"
                old = pr.get("oldtitle_title") or pr.get("oldtitle")
                if old:
                    srcs.append((old, ts))
            out.append({"ts": ts, "action": act, "details": det, "src": src, "title": title})
    return out, srcs


def protect_log(title, moves):
    entries, srcs = log_entries(title)
    if entries is None:
        return None
    todo = [(m["from"], m["ts"]) for m in moves if m["from"] != title and not (m.get("reverted") or m.get("revert_of_move"))] + srcs
    followed = [title]
    while todo and len(followed) <= MAX_FORMER:
        t, until = todo.pop(0)
        if t in followed or P.NS_PREFIX.match(t):
            continue
        e2, s2 = log_entries(t, until)
        followed.append(t)
        if e2 is None:
            continue
        entries += e2
        todo += [(x, ts) for x, ts in s2 if x not in followed]
    return {"entries": sorted(entries, key=lambda e: e["ts"] or ""), "titles": followed}


def protection_at(entries, date):
    usable = [e for e in entries if e["src"] != "unparsed"]       # an unparsed protect must not wipe the known state
    st = P.protection_at(usable, date)
    unknown = any(e["src"] == "unparsed" and (e["ts"] or "") <= date for e in entries)
    return st, unknown


def now_protection(pi):
    return {x["type"]: x["level"] for x in pi.get("protection") or []
            if not (x.get("expiry") and x["expiry"] not in ("infinite", "infinity") and x["expiry"] < P.NOW)}


# ------------------------------------------------------------------ talk: RfC / RM with per-discussion dates
RFC_TPL = re.compile(r"\{\{\s*rfc\s*[|}]|rfcid\s*=|\{\{\s*(?:closed )?rfc top", re.I)
RM_TPL = re.compile(r"\{\{\s*requested move/dated|result of the move request was|\{\{\s*rm top", re.I)
CLOSE_RESULT = re.compile(r"\{\{\s*(?:closed rfc top|rfc top|archive top|atop|discussion top|rm top|closed top)\s*\|[^{}]*?result\s*=\s*([^|{}]{0,200})", re.I)
RESULT_CLASS = [("moved", re.compile(r"^\W*(?:page )?moved|^\W*move(?:d)? to\b", re.I)),
                ("not moved", re.compile(r"not moved|do not move|not done", re.I)),
                ("no consensus", re.compile(r"no consensus|no clear consensus", re.I)),
                ("withdrawn", re.compile(r"withdrawn|procedural close|speedy close", re.I)),
                ("consensus", re.compile(r"\bconsensus (?:for|to|in favou?r|that|is)|\bsupport(?:ed)?\b|option \w+", re.I)),
                ("against", re.compile(r"consensus against|\boppose", re.I))]


def result_class(txt):
    if not txt:
        return None
    t = P.clean(txt, 200)
    return next((k for k, rx in RESULT_CLASS if rx.search(t)), "other")


def discussions(wt):
    """RfC / RM sections of one talk page: [{kind, ts, closed, formal, result}] (class labels only; no text or names)."""
    out = []
    parts = re.split(r"^==\s*([^=].*?)\s*==\s*$", wt, flags=re.M)
    for i in range(1, len(parts) - 1, 2):
        head, body = parts[i], parts[i + 1]
        rfc_h = bool(re.search(r"\brfc\b|request for comments?", head, re.I)); rfc_t = bool(RFC_TPL.search(body[:5000]))
        rm_h = bool(re.search(r"requested move|move request", head, re.I)); rm_t = bool(RM_TPL.search(body))
        if not (rfc_h or rfc_t or rm_h or rm_t):
            continue
        kind = "rfc" if (rfc_t or (rfc_h and not rm_t)) else "rm"
        res = P.RM_RESULT.search(body) if kind == "rm" else None
        cr = CLOSE_RESULT.search(body)
        rtxt = res.group(1) if res else (cr.group(1) if cr else None)
        out.append({"kind": kind, "ts": P.sig_ts(body), "closed": bool(P.CLOSED.search(body)) or bool(res),
                    "formal": rfc_t if kind == "rfc" else rm_t, "result": result_class(rtxt)})
    return out


def rfc_scan(now_talk_wt, arch_pages, max_archives=60):
    found = discussions(now_talk_wt or "")
    recent = sorted((t for t, ts in arch_pages if ts and ts >= P.WINDOWS["w1"][0]), reverse=True)
    trunc = len(recent) > max_archives
    recent = recent[:max_archives]
    for i in range(0, len(recent), 10):
        for j in P.paged({"action": "query", "prop": "revisions", "titles": "|".join(recent[i:i + 10]), "rvprop": "content",
                          "rvslots": "main"}, core=False, max_pages=5):
            if "_failed" in j:
                return None
            if "_truncated" in j:
                break
            for p in j.get("query", {}).get("pages", []) or []:
                for r in p.get("revisions") or []:
                    c = (r.get("slots") or {}).get("main", {}).get("content")
                    if c:
                        found += discussions(c)
    seen, uniq = set(), []
    for d in found:                                   # the same section can sit on two pages mid-archiving
        k = (d["kind"], d["ts"])
        if d["ts"] and k in seen:
            continue
        seen.add(k); uniq.append(d)
    uniq.sort(key=lambda d: d["ts"] or "9")
    out = {"archives_scanned": len(recent), "archives_truncated": trunc, "undated": sum(1 for d in uniq if not d["ts"]),
           "items": uniq[:500]}
    for w in P.WINDOWS:
        dw = [d for d in uniq if d["ts"] and P.in_win(d["ts"], w)]
        rf = [d for d in dw if d["kind"] == "rfc"]; rm = [d for d in dw if d["kind"] == "rm"]
        out[w] = {"rfc": len(rf), "rfc_formal": sum(d["formal"] for d in rf), "rfc_closed": sum(d["closed"] for d in rf),
                  "rm": len(rm), "rm_moved": sum(d["result"] == "moved" for d in rm),
                  "rm_not_moved": sum(d["result"] in ("not moved", "no consensus") for d in rm),
                  "rm_result_known": sum(bool(d["result"]) for d in rm)}
    return out


# ------------------------------------------------------------------ lead term events (EVAL 1.3 problem 4)
UNK, HID = "unk", "hid"


def fetch_leads(revids, budget):
    """Section-0 term state of given revisions, 50 per request (revids mode). budget = [requests left]."""
    got = {}
    for i in range(0, len(revids), 50):
        if budget[0] <= 0:
            break
        chunk = revids[i:i + 50]
        cont, pages = {}, 0
        while True:
            j = P.q({"action": "query", "prop": "revisions", "revids": "|".join(map(str, chunk)), "rvprop": "ids|content",
                     "rvslots": "main", "rvsection": 0, **cont}, core=False)
            budget[0] -= 1; budget[1] += 1
            if j is None:
                return None
            for p in (j.get("query") or {}).get("pages") or []:
                for r in p.get("revisions") or []:
                    c = (r.get("slots") or {}).get("main", {})
                    got[r["revid"]] = HID if (c.get("texthidden") or "content" not in c) else P.lead_terms(A.prose(c["content"]))
            pages += 1
            if "continue" not in j or pages >= 5:
                break
            cont = j["continue"]
        for rid in chunk:
            got.setdefault(rid, HID)
    return got


def spread(m):
    """0..m-1 in an order that interleaves early and late items (refinement budget is spent evenly over time)."""
    if m <= 1:
        return list(range(m))
    bits = max(1, (m - 1).bit_length())
    key = lambda i: int(format(i, f"0{bits}b")[::-1], 2)
    return sorted(range(m), key=key)


def lead_events(revs, seed, grid_req=None, refine_req=None):
    """Term flips in the lead over one continuous revision sequence (2021 -> now), seeded with the 2021 snapshot state.
    n <= grid_req*50 revisions: every revision is read (exact). Otherwise a time-stratified grid (stride <= 50) is read over
    the WHOLE sequence, so coverage always reaches the last revision, and every grid interval whose end states differ is
    read in full (up to refine_req requests, intervals in time-interleaved order). Revisions with a known sha1 are never
    re-read. An event is exact when the previous revision's state is known; otherwise it is attributed to the interval."""
    grid_req = LEAD_GRID if grid_req is None else grid_req
    refine_req = LEAD_REFINE if refine_req is None else refine_req
    seq = [r for r in revs if r.get("revid")]
    n = len(seq)
    cov = {"n_revs": n, "seeded": seed is not None}
    if not n:
        return [], {**cov, "stride": None, "requests": 0}
    k = min(50, max(1, math.ceil(n / (grid_req * 50))))
    grid = sorted(set(range(0, n, k)) | {n - 1})
    st, by_sha = [UNK] * n, {}
    budget = [math.ceil(len(grid) / 50) + 3, 0]          # the grid is always read in full: coverage reaches the end

    def fill_sha():
        for i, r in enumerate(seq):
            if st[i] == UNK and r.get("sha1") in by_sha:
                st[i] = by_sha[r["sha1"]]

    def load(idx):
        fill_sha()
        need = [i for i in idx if st[i] == UNK]
        got = fetch_leads([seq[i]["revid"] for i in need], budget)
        if got is None:
            return False
        for i in need:
            if seq[i]["revid"] in got:
                st[i] = got[seq[i]["revid"]]
                if st[i] != HID and seq[i].get("sha1"):
                    by_sha[seq[i]["sha1"]] = st[i]
        fill_sha()
        return True

    if not load(grid):
        return None, cov
    known = lambda i: st[i] not in (UNK, HID)
    diff, last = [], (seed, -1)
    for a, b in zip(grid, grid[1:]):
        if known(a):
            last = (st[a], a)
        if b - a > 1 and known(b) and last[0] is not None and st[b] != last[0]:
            diff.append((last[1], b))
    refined, take = 0, []
    for idx in spread(len(diff)):
        a, b = diff[idx]
        need = [i for i in range(a + 1, b) if st[i] == UNK and seq[i].get("sha1") not in by_sha]
        if math.ceil((len(take) + len(need)) / 50) > refine_req:
            continue
        take += need; refined += 1
    budget[0] = refine_req
    if take and not load(sorted(take)):
        return None, cov
    events, prev, prev_i, seen_sha = [], seed, -1, set()
    for i, r in enumerate(seq):
        s, sha = st[i], r.get("sha1")
        if known(i):
            if prev is not None:
                tg = set(r.get("tags") or [])
                for term in P.TERMS:
                    if s[term] != prev[term]:
                        exact = prev_i == i - 1
                        events.append({"ts": r["timestamp"], "term": term, "kind": "insert" if s[term] else "remove",
                                       "revid": r["revid"], "user": (r.get("user") or "") if exact else "", "exact": exact,
                                       "after_ts": None if exact or prev_i < 0 else seq[prev_i]["timestamp"],
                                       "reverted": "mw-reverted" in tg,
                                       "restore": bool(tg & A.REVERTING) or bool(sha and sha in seen_sha)})
            prev, prev_i = s, i
        if sha:
            seen_sha.add(sha)
    kn = [i for i in range(n) if known(i)]
    cov.update({"stride": k, "grid": len(grid), "requests": budget[1], "known": len(kn), "differing_intervals": len(diff),
                "refined_intervals": refined, "unrefined_intervals": len(diff) - refined,
                "first_ts": seq[0]["timestamp"], "last_ts": seq[-1]["timestamp"],
                "last_known_ts": seq[kn[-1]]["timestamp"] if kn else None,
                "exact_share": (sum(e["exact"] for e in events) / len(events)) if events else None,
                "created_terms": sorted(t for t, v in st[kn[0]].items() if v) if (kn and seed is None) else None})
    return events, cov


def lead_include(row, terms_at):
    if LEAD_ALL:
        return "all"
    if row["group"] == "topic" or row.get("atrocity_case"):
        return "topic_or_atrocity"
    if any(s and any(s.values()) for s in terms_at.values()):
        return "term_at_snapshot"
    return None


def acct_flags(user, ts):
    if not user or A.ANON.match(user) or A.BOT.search(user):
        return None
    f = P._ucache.get(user)
    if not f:
        return None
    age = int((P.ep(ts) - P.ep(f["reg"])) / 86400) if f.get("reg") else None
    return {"age_d": age, "lt500": (f.get("ec") or 0) < 500, "ext": f["ext"], "indef": f["indef"], "partial": f.get("partial"),
            "breason": f.get("breason")}


def term_events(row, revs, seed):
    ev, cov = lead_events(revs, seed)
    if ev is None:
        return None
    if P.LW_ON[0]:
        rids = list(dict.fromkeys(e["revid"] for e in ev if e["exact"]))
        pick = rids if len(rids) <= LW_MAX else [rids[int(i * len(rids) / LW_MAX)] for i in range(LW_MAX)]
        scores = {rid: P.liftwing(rid) for rid in pick}
    else:
        scores = {}
    for e in ev:
        e["lw"] = scores.get(e["revid"])
    agg = P.event_aggregates(ev)                                 # also fills the account cache for the flags below
    agg_new = P.event_aggregates([e for e in ev if not e["restore"]])
    restores = {w: Counter(f"{'critical' if e['term'] in A.CRITICAL else e['term']}_{e['kind']}" for e in ev
                           if e["restore"] and P.in_win(e["ts"], w)) for w in P.WINDOWS}
    out = [{"ts": e["ts"], "term": e["term"], "kind": e["kind"], "revid": e["revid"], "exact": e["exact"],
            "after_ts": e["after_ts"], "restore": e["restore"], "reverted": e["reverted"],
            "u": P.h(e["user"]) if e["user"] else None, "anon": bool(A.ANON.match(e["user"])) if e["user"] else None,
            "acct": acct_flags(e["user"], e["ts"]), "lw": e["lw"]} for e in ev]
    return {"coverage": cov, "by_window": agg, "by_window_new_only": agg_new, "restores": {w: dict(c) for w, c in restores.items()},
            "events": out[-MAX_EVENTS:], "events_truncated": len(out) > MAX_EVENTS}


# ------------------------------------------------------------------ per-article collector
def collect(row):
    t, pi = row["title"], row["pi"]
    failed = []
    rec = {k: row[k] for k in ("title", "frame_titles", "group", "project", "importance", "stratum", "atrocity_case", "group_conflict")
           if row.get(k) is not None}
    rec["now"] = {**pi, "wikidata": row.get("wd_now")}
    rec["at"], leads, terms_at, prev = {}, {}, {}, None
    for k, d in P.DATES.items():
        meta, wt = P.wikitext_at(t, d)
        if meta and prev and meta.get("revid") == prev[0]:
            art, narr, lp, terms = prev[1:]
            narr = {**narr, "date": d[:10]} if narr else None
        elif wt is None or re.match(r"\s*#redirect", wt, re.I):
            art, narr, lp, terms = ({"redirect": True} if wt else None), None, None, None
        else:
            art = compact_article(wt)
            s0 = section0(wt)
            narr = MN.snap_features(row, s0, d)
            lp = narr.pop("lead_prose") if narr else None
            terms = P.lead_terms(A.prose(s0))
        if meta:
            prev = (meta.get("revid"), art, narr, lp, terms)
        rec["at"][k] = {"rev": meta, "article": art, "narr": narr}
        leads[k], terms_at[k] = lp, terms
    # revisions since 2021 (free signals); usernames stay in memory
    revs, trunc = P.history(t, "ids|timestamp|user|size|comment|tags|flags|sha1")
    if revs is None:
        raise RuntimeError(f"revisions failed: {t}")
    revs = [r for r in revs if r["timestamp"] <= P.NOW]
    a0 = rec["at"]["2021-01-01"]
    prev_size = (a0["article"] or {}).get("bytes") if a0["rev"] and revs and a0["rev"].get("revid") != revs[0].get("revid") else None
    agg, moves, eds, created = P.rev_aggregates(revs, prev_size)
    moves = clean_moves(revs, moves)
    rec.update({"created_in_window": created, "revisions_truncated": trunc, "moves": moves})
    for k, d in P.DATES.items():
        rec["at"][k]["title"] = title_at(t, moves, d, created, rec["at"][k]["rev"])
    # talk now, talk history, overlap
    talk, twt, trevs, ttrunc = f"Talk:{t}", None, [], False
    if pi.get("talk_exists"):
        _, twt = P.wikitext_at(talk, P.NOW)
        trevs, ttrunc = P.history(talk, "timestamp|user|size")
        if trevs is None:
            failed.append("talk_revisions"); trevs = []
        trevs = [r for r in trevs if r["timestamp"] <= P.NOW]
    rec["talk_now"] = P.parse_talk(twt) if twt is not None else None
    tagg, _, teds, _ = P.rev_aggregates(trevs)
    for w in P.WINDOWS:
        a_eds, t_eds = eds[w], set(teds[w]); n = sum(a_eds.values())
        agg[w]["talk"] = {"edits": tagg[w].get("edits", 0), "editors": tagg[w]["editors"], "bytes_added": tagg[w].get("bytes_added", 0),
                          "edits_per_month": tagg[w]["edits_per_month"],
                          "talk_to_article_edits": (tagg[w].get("edits", 0) / agg[w]["edits"]) if agg[w].get("edits") else None,
                          "article_edits_by_talk_participants": (sum(c for u, c in a_eds.items() if u in t_eds) / n) if n else None,
                          "article_editors_on_talk": (sum(1 for u in a_eds if u in t_eds) / len(a_eds)) if a_eds else None}
    rec["talk_revisions_truncated"] = ttrunc
    rec["_editors"] = {w: sorted(P.h(u) for u in eds[w]) for w in ("w1", "w2")}
    # account facts (aggregate)
    ua = P.user_aggregates(revs)
    for w in P.WINDOWS:
        agg[w]["accounts"] = ua[w]
    # pageviews over current + former titles
    pv = pageviews([t] + former_titles(t, moves))
    rec["pageviews"] = pv
    for w in P.WINDOWS:
        agg[w]["views"] = views_in(pv, w)
    rec["win"] = agg
    # protection: log incl. former titles and old formats; "now" anchored on page info
    pl = protect_log(t, moves)
    if pl is None:
        failed.append("protect_log")
    now_pi = now_protection(pi)
    for k, d in P.DATES.items():
        if pl is None:
            rec["at"][k]["protection"] = now_pi if k == "now" else None; continue
        st, unk = protection_at(pl["entries"], d)
        rec["at"][k]["protection"] = st
        rec["at"][k]["protection_uncertain"] = unk
    recon_now = rec["at"]["now"]["protection"] if pl else None
    rec["at"]["now"]["protection"] = now_pi
    rec["protection"] = {"source_now": "page_info", "recon_now": recon_now, "recon_matches_now": recon_now == now_pi if pl else None,
                         "titles_followed": pl["titles"] if pl else None,
                         "entries": [{k: e[k] for k in ("ts", "action", "details", "src")} for e in pl["entries"]][-60:] if pl else None,
                         "n_entries": len(pl["entries"]) if pl else None,
                         "n_old_format": sum(e["src"] == "old_format" for e in pl["entries"]) if pl else None,
                         "n_unparsed": sum(e["src"] == "unparsed" for e in pl["entries"]) if pl else None}
    # archives + RfC/RM scan
    if pi.get("talk_exists"):
        ta = P.talk_archives(t)
        if ta is None:
            failed.append("talk_archives"); ta = {"_pages": []}
        arch = ta.pop("_pages", [])
        rec["talk_archives"] = ta
        rec["discussions"] = rfc_scan(twt, arch)
        if rec["discussions"] is None:
            failed.append("discussions")
    else:
        rec["talk_archives"], rec["discussions"] = {"n": 0, "bytes": 0, "n_subpages": 0}, None
    # Wikidata at 2023-07-01 ("now" came batched from resolve)
    rec["wikidata_2023"] = None
    if pi.get("qid"):
        meta, content = P.wikitext_at(pi["qid"], P.DATES["2023-07-01"], url=P.WD, core=False)
        if content is not None:
            rec["wikidata_2023"] = {**(P.parse_wikidata(content) or {}), "revid": meta["revid"], "ts": meta["ts"]}
    # lead term events
    why = lead_include(row, terms_at)
    rec["lead_events_scope"] = why
    if why:
        te = term_events(row, revs, terms_at["2021-01-01"])
        if te is None:
            failed.append("lead_events")
        rec["term_events"] = te
    else:
        rec["term_events"] = None
    rec["_leads"] = [leads[k] for k in P.DATES]
    rec["failed_signals"] = failed
    return rec


# ------------------------------------------------------------------ shard / merge
def load_frame2():
    f2 = json.load(open(frame2_path()))
    set_now(f2["now"])
    ALIAS.clear(); ALIAS.update(f2.get("aliases") or {})
    GROUP_OF.clear(); GROUP_OF.update(f2.get("concept_groups") or {})
    return f2


def run_shard(i, n):
    f2 = load_frame2()
    if not os.environ.get("WT_SALT"):
        print("WARNING: WT_SALT not set; random per-process salt (hashes not linkable across shards)", file=sys.stderr)
    rows = M.shard(f2["rows"], i, n)
    lim = int(os.environ.get("MASS_LIMIT", "0"))
    print(f"mass2 shard {i}/{n}: {len(rows)} articles, now={P.NOW}, liftwing={P.LW_ON[0]}, lead grid={LEAD_GRID} refine={LEAD_REFINE}",
          flush=True)
    M._run(KIND, collect, rows[:lim] if lim else rows, i)


SPARSE = {"c", "counts", "res_counts", "ev_counts", "lex_lead", "lex_full", "maint", "refs", "lead_refs", "lead_refs_resolved", "restores"}


def _round(x):
    if isinstance(x, float):
        return float(f"{x:.4g}")
    if isinstance(x, dict):
        return {k: _round(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_round(v) for v in x]
    return x


def _sparse(x, key=None):
    if isinstance(x, dict):
        if key in SPARSE:
            return {k: _sparse(v, k) for k, v in x.items() if v not in (0, None, False)}
        return {k: _sparse(v, k) for k, v in x.items()}
    if isinstance(x, list):
        return [_sparse(v, key) for v in x]
    return x


def split_detail(r):
    """Per-event lists go to mass2_events.json.gz; mass2.json keeps per-article signals."""
    det = {}
    te = r.get("term_events")
    if te and "events" in te:
        det["lead_events"] = te.pop("events")
    if r.get("discussions") and "items" in r["discussions"]:
        det["discussions"] = r["discussions"].pop("items")
    if r.get("protection") and "entries" in r["protection"]:
        det["protection_log"] = r["protection"].pop("entries")
    return det


def compact(r):
    """Merged-file form: event aggregates only for (term, kind) cells with events, sparse counters (absent key = 0),
    floats to 4 significant digits, monthly views as a list from 2021-01, a snapshot identical to the previous date
    stored as {"same_as": date}. Shard files keep the full form."""
    te = r.get("term_events")
    if te:
        for k in ("by_window", "by_window_new_only"):
            te[k] = {w: {c: v for c, v in cells.items() if v.get("n")} for w, cells in (te.get(k) or {}).items()}
    pv = r.get("pageviews") or {}
    if pv.get("monthly"):
        ms = sorted(pv["monthly"])
        y, m, seq = 2021, 1, []
        while f"{y}{m:02d}" <= ms[-1]:
            seq.append(pv["monthly"].get(f"{y}{m:02d}")); y, m = (y, m + 1) if m < 12 else (y + 1, 1)
        pv["monthly"] = {"start": "202101", "views": seq}
    for w in (r.get("win") or {}).values():
        w["tags"] = dict(list((w.get("tags") or {}).items())[:12])
    prev = None
    for k, a in (r.get("at") or {}).items():
        rid = (a.get("rev") or {}).get("revid")
        if prev and rid and rid == prev[1]:
            for f in ("article", "narr"):
                if a.get(f) is not None:
                    a[f] = {"same_as": prev[0]}
        elif rid:
            prev = (k, rid)
        if a.get("article") and isinstance(a["article"], dict):
            a["article"].pop("watch_links_lead", None)
    return _round(_sparse(r))


def _dump_gz(path, obj):
    with gzip.open(path, "wt") as f:
        json.dump(obj, f, separators=(",", ":"))


def merge():
    f2 = load_frame2()
    recs, seen = [], set()
    for f in sorted(glob.glob(os.path.join(M.OUT, f"{KIND}_*.json.gz"))):
        for r in json.load(gzip.open(f, "rt")):
            if r["title"] not in seen:
                seen.add(r["title"]); recs.append(r)
    order = {r["title"]: k for k, r in enumerate(f2["rows"])}
    recs.sort(key=lambda r: order.get(r["title"], 10 ** 9))
    leads = {r["title"]: r.pop("_leads", None) for r in recs}
    editors = {r["title"]: r.pop("_editors", None) for r in recs}
    keys = list(P.DATES)
    meta = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "now": P.NOW, "dates": P.DATES, "windows": P.WINDOWS,
            "note": "Mass v2. Editors are salted hashes (per-run salt, never stored); account facts are per-article shares; edit "
                    "summaries, block reasons and close results are class labels only. Compact form: counters are sparse "
                    "(absent key = 0), event aggregates only for cells with events, floats to 4 significant digits.",
            "concept_groups": f2.get("concept_groups"), "concept_inbound_now": f2.get("concept_inbound_now"),
            "atrocity_resolved": f2.get("atrocity_resolved")}
    details = {r["title"]: split_detail(r) for r in recs}
    out_p = os.path.join(A.DATA, "mass2.json")
    json.dump({**meta, "articles": [compact(r) for r in recs]}, open(out_p, "w"), separators=(",", ":"))
    _dump_gz(os.path.join(A.DATA, "mass2_events.json.gz"), {"note": "per-article lead events (hashed accounts), RfC/RM "
             "discussions (dates, class labels) and protection log entries", "articles": details})
    mb = os.path.getsize(out_p) / 1e6
    if mb > 90:                                   # git hosts refuse files over 100 MB: ship a gzip copy instead
        _dump_gz(out_p + ".gz", json.load(open(out_p)))
        print(f"WARNING: mass2.json is {mb:.0f} MB; wrote mass2.json.gz for the data branch", flush=True)
    _dump_gz(os.path.join(A.DATA, "mass2_leads.json.gz"), {"dates": keys, "leads": leads})
    _dump_gz(os.path.join(A.DATA, "mass2_editors.json.gz"), {"windows": ["w1", "w2"], "editors": editors})
    te = [r["term_events"] for r in recs if r.get("term_events")]
    cov = [x["coverage"] for x in te if x["coverage"].get("n_revs")]
    summ = {"n_expected": len(f2["rows"]), "n_records": len(recs), "by_stratum": dict(Counter(r["stratum"] for r in recs)),
            "dropped_in_resolve": {k: len(v) for k, v in f2["dropped"].items()},
            "failed_signals": dict(Counter(s for r in recs for s in r.get("failed_signals") or [])),
            "lead_events": {"articles": len(te), "scope": dict(Counter(r.get("lead_events_scope") for r in recs)),
                            "full_read": sum(c["stride"] == 1 for c in cov),
                            "covered_to_last_revision": sum(c.get("last_known_ts") == c.get("last_ts") for c in cov),
                            "unrefined_intervals": sum(c.get("unrefined_intervals", 0) for c in cov),
                            "requests": sum(c.get("requests", 0) for c in cov)},
            "coverage": {f"article@{k}": sum(1 for r in recs if (r["at"][k] or {}).get("article")) for k in keys} |
                        {"talk_now": sum(1 for r in recs if r.get("talk_now")), "pageviews": sum(1 for r in recs if (r.get("pageviews") or {}).get("monthly")),
                         "wikidata_now": sum(1 for r in recs if r["now"].get("wikidata")), "wikidata_2023": sum(1 for r in recs if r.get("wikidata_2023")),
                         "protection_recon_matches_now": sum(1 for r in recs if (r.get("protection") or {}).get("recon_matches_now"))}}
    json.dump(summ, open(os.path.join(A.DATA, "mass2_summary.json"), "w"), indent=1)
    print("mass2 merged:", json.dumps(summ, indent=1), flush=True)
    if len(recs) < 0.95 * len(f2["rows"]):
        sys.exit(f"mass2 merge: only {len(recs)}/{len(f2['rows'])} articles (<95%) - some shards incomplete")


# ------------------------------------------------------------------ cost / time estimate (offline)
def estimate(shards=None, eff_rps=1.0, parallel=4, budget_h=5.0):
    """Requests per article from the mass edit distribution (data/mass_results.json lab_articles: edits since 2021).
    Fixed parts follow the evaluator's measured costs (mass_scope.json); lead events follow the grid model above."""
    la = json.load(open(os.path.join(A.DATA, "mass_results.json")))["mass"]["lab_articles"]
    lim = LEAD_GRID * 50
    fr = json.load(open(os.path.join(A.DATA, "mass_results.json")))["mass"]["lab_frames"]
    crit_i = [fr.index(k) for k in A.CRITICAL if k in fr]     # comparison pages run lead events if a term is in a lead
    flip_rate = 0.01               # share of revisions that flip a tracked lead term (pilot: ~0.5-2% on topic pages)
    tot, lead_tot = 0.0, 0.0
    for a in la:
        e = a.get("e") or 0
        # 3 snapshots, talk now, archive list, RfC archive content, Wikidata 2023, pageviews (+former titles),
        # protection log (+former titles), account lookups (50 per call, cached), resolve job (batched)
        fixed = 3 + 1.0 + 1.0 + 0.3 + 1.0 + 1.15 + 1.15 + 0.5 + 0.07
        hist = max(1, math.ceil(e / 500)) + max(1, math.ceil(0.5 * e / 500))  # article + talk history (talk ~ half the edits)
        if e <= lim:
            lead = math.ceil(e / 50) if e else 0
        else:
            k = min(50, math.ceil(e / lim)); pts = math.ceil(e / k) + 1
            lead = math.ceil(pts / 50) + min(LEAD_REFINE, math.ceil(min(pts, flip_rate * e) * (k - 1) / 50))
        share = 1.0 if (LEAD_ALL or a["g"] == "t") else float(any(x and any(x[1 + ci] for ci in crit_i) for x in a["l"]))
        tot += fixed + hist + share * lead; lead_tot += share * lead
    n = 0.988 * len(la)                                                      # after redirect dedupe (125 duplicates)
    per = tot / len(la) * 1.06                                               # 6% retries (pilot)
    total = per * n
    need = math.ceil(total / (eff_rps * 3600 * budget_h))
    shards = shards or max(6, need)
    per_shard_h = total / shards / eff_rps / 3600
    waves = math.ceil(shards / parallel)
    res = {"articles": round(n), "requests_per_article": round(per, 2), "lead_requests_per_article": round(lead_tot / len(la) * 1.06, 2),
           "total_requests": round(total), "shards": shards, "requests_per_shard": round(total / shards),
           "hours_per_shard_at_%.1f_rps" % eff_rps: round(per_shard_h, 2), "waves": waves,
           "wall_hours": round(waves * per_shard_h + 0.3, 1), "min_shards_for_%gh" % budget_h: need}
    print(json.dumps(res, indent=1))
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["resolve", "shard", "merge", "estimate"])
    ap.add_argument("--shard", type=int, default=0); ap.add_argument("--of", type=int, default=1)
    ap.add_argument("--rps", type=float, default=1.0)
    a = ap.parse_args()
    if a.cmd == "resolve":
        resolve()
    elif a.cmd == "shard":
        run_shard(a.shard, a.of)
    elif a.cmd == "merge":
        merge()
    else:
        estimate(eff_rps=a.rps)
