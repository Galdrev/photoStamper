"""Guard collector: full revision histories, talk-page !votes and lead critical-term counts for the scoped articles, plus
the redacted ArbCom extract. Runs inside ONE workflow job, next to coord.py, under the same in-job salt.

  python guard.py plan        -> data/guard/plan.json (offline: topic scope + comparison pool from manifest and mass3 frame)
  python guard.py collect     -> data/guard/raw.json.gz, data/guard/arbcom.json (network; time-budgeted)
  GUARD_LIMIT=6 ...           -> test mode (first 6 topic + 6 comparison articles)

Scope (plan). Topic = the curated core of the manifest (treatment groups israel, zionism, conflict, antisemitism) plus
every mass3 frame article of the Israel, Palestine and Israel Palestine Collaboration projects rated Top or High
importance. Comparison pool = the manifest's comparison articles plus every mass3 frame comparison article rated Top or
High. In the job the pool is matched 1:1 to the topic articles (tier: core/Top -> core/Top, High -> High) on nearest log
page length (prop=info), greedy in a seeded random order, without replacement.

Collection (collect), in this order, each phase with its own share of GUARD_BUDGET_MIN:
  arbcom    action=raw of the four ArbCom pages; names redacted and findings extracted in memory
            (analyze_guard.arbcom_extract); only the redacted extract is written
  resolve   prop=info (50 titles per call) -> canonical title, length; matching
  history   prop=revisions rvlimit=max rvdir=newer, rvprop ids|timestamp|user|sha1|comment|size|tags; usernames hashed at
            once (coord.h, the run-wide salt); comments reduced to flags and the revision ids they undo / restore,
            converted to positions in the history (the raw comment is never kept). Until 55% of the budget.
  talk      Talk:<title> + its subpages named *archive* / *rfc* / *move* (list=allpages), content in batches of 8,
            parsed for RfC / requested-move sections and linked AfD pages; one stance per signed account per discussion,
            signature names hashed at once. Until 75% of the budget.
  leads     section-0 wikitext (rvsection=0, 50 revids per call) of the before / after states of reverts since 2021,
            in a seeded random order (so a truncated sample is a random sample); critical-term count only. Until the end.
Privacy: as coord.py. Usernames exist only in memory; raw outputs stay on the runner and are deleted by the workflow.
Nothing here prints a name, a hash or a revision id.
"""
import argparse, gzip, json, math, os, random, re, sys, threading, time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wt_net                   # noqa: E402
import analyze as A             # noqa: E402
import coord as CO              # noqa: E402
import analyze_guard as AG      # noqa: E402

OUT = os.path.join(HERE, "data", "guard")
EN = "https://en.wikipedia.org/w/api.php"
RAW_URL = "https://en.wikipedia.org/w/index.php"
SEED = 20261108
THREADS = int(os.environ.get("GUARD_THREADS", "3"))
BUDGET_MIN = float(os.environ.get("GUARD_BUDGET_MIN", "250"))
MAX_REVS = int(os.environ.get("GUARD_MAX_REVS", "150000"))
MAX_TALK_PAGES = int(os.environ.get("GUARD_MAX_TALK", "250"))
PHASE_END = {"history": 0.55, "talk": 0.75, "leads": 1.0}
CORE_GROUPS = {"israel", "zionism", "conflict", "antisemitism"}
M3_TOPIC_PROJECTS = {"Israel", "Palestine", "Israel Palestine Collaboration"}
TIERS = ("Top", "High")
ARBCOM = {"PIA5 case": "Wikipedia:Arbitration/Requests/Case/Palestine-Israel_articles_5",
          "PIA5 proposed decision": "Wikipedia:Arbitration/Requests/Case/Palestine-Israel_articles_5/Proposed_decision",
          "PIA4 case": "Wikipedia:Arbitration/Requests/Case/Palestine-Israel_articles_4",
          "PIA5 evidence": "Wikipedia:Arbitration/Requests/Case/Palestine-Israel_articles_5/Evidence"}
REVERT_TAGS = {"mw-undo", "mw-rollback", "mw-manual-revert"}
RV_RX = re.compile(r"\b(?:rv|rvv|revert\w*|undid|undo\w*|rollback|rolled back|restor\w*)\b", re.I)
UNDO_RX = re.compile(r"\b(?:Undid|Undo|Undoing|Undone) (?:revision|edit) (\d+)", re.I)
RESTORE_RX = re.compile(r"\bRestored (?:revision|version) (\d+)", re.I)


# ------------------------------------------------------------------ plan (offline)
def plan():
    man = json.load(open(os.path.join(A.DATA, "manifest.json")))
    fr = json.load(open(os.path.join(A.DATA, "mass3", "frame.json")))["rows"]
    topic, pool = {}, {}
    for t, (g, sub) in man.items():
        if g == "treatment" and sub in CORE_GROUPS:
            topic[t] = {"title": t, "tier": "core", "src": "manifest"}
        elif g == "control":
            pool[t] = {"title": t, "tier": "core", "src": "manifest"}
    for r in fr:
        if r["importance"] not in TIERS:
            continue
        if r["group"] == "topic" and r["project"] in M3_TOPIC_PROJECTS:
            topic.setdefault(r["title"], {"title": r["title"], "tier": r["importance"], "src": "mass3"})
        elif r["group"] == "comparison":
            pool.setdefault(r["title"], {"title": r["title"], "tier": r["importance"], "src": "mass3"})
    for t in list(pool):
        if t in topic:
            del pool[t]
    os.makedirs(OUT, exist_ok=True)
    out = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "topic": sorted(topic.values(), key=lambda x: x["title"]),
           "pool": sorted(pool.values(), key=lambda x: x["title"]),
           "counts": {"topic": dict(Counter(x["tier"] for x in topic.values())), "pool": dict(Counter(x["tier"] for x in pool.values()))}}
    json.dump(out, open(os.path.join(OUT, "plan.json"), "w"), indent=1)
    print(f"guard plan: topic {out['counts']['topic']}, comparison pool {out['counts']['pool']}")
    return out


# ------------------------------------------------------------------ network helpers
def q(params):
    p = {"format": "json", "formatversion": 2, **params}
    j = wt_net.get_json(EN, p)
    if j is None:
        raise RuntimeError("API request failed after retries")
    return j


def raw_page(title):
    """index.php?action=raw -> wikitext or None (missing). Same rate limit / counters as wt_net.get_json."""
    for i in range(6):
        wt_net._wait_slot()
        try:
            r = wt_net._S.get(RAW_URL, params={"title": title, "action": "raw"}, timeout=90)
            wt_net.C["requests"] += 1
            if r.status_code == 200:
                wt_net.C["ok"] += 1
                return r.text
            if r.status_code == 404:
                return None
            if r.status_code == 429:
                wt_net.C["http_429"] += 1; time.sleep(int(r.headers.get("retry-after", 20) or 20)); continue
        except Exception:
            pass
        wt_net.C["retries"] += 1; time.sleep(min(60, 2 ** i))
    # fall back to the API (same wikitext)
    j = wt_net.get_json(EN, {"action": "query", "prop": "revisions", "titles": title, "rvprop": "content", "rvslots": "main",
                             "format": "json", "formatversion": 2})
    try:
        return j["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"]
    except Exception:
        return None


def resolve(titles):
    """-> {original title: {"title": canonical, "length": int} or None}."""
    out = {}
    for i in range(0, len(titles), 50):
        chunk = titles[i:i + 50]
        j = q({"action": "query", "prop": "info", "titles": "|".join(chunk), "redirects": 1})
        qy = j.get("query") or {}
        m = {t: t for t in chunk}
        for n in qy.get("normalized") or []:
            for k, v in m.items():
                if v == n["from"]:
                    m[k] = n["to"]
        for rd in qy.get("redirects") or []:
            for k, v in m.items():
                if v == rd["from"]:
                    m[k] = rd["to"]
        pages = {p["title"]: p for p in qy.get("pages") or []}
        for t in chunk:
            p = pages.get(m[t])
            out[t] = None if (p is None or p.get("missing") or p.get("invalid")) else {"title": p["title"], "length": p.get("length") or 0}
    return out


def match(topic, pool, info, seed=SEED):
    rnd = random.Random(seed)
    tt = [x for x in topic if info.get(x["title"])]
    rnd.shuffle(tt)
    used, pairs = set(), []
    cls = lambda tier: "TopCore" if tier in ("core", "Top") else "High"
    for x in tt:
        lt = math.log(max(1, info[x["title"]]["length"]))
        cands = [c for c in pool if c["title"] not in used and info.get(c["title"]) and cls(c["tier"]) == cls(x["tier"])]
        if not cands:
            cands = [c for c in pool if c["title"] not in used and info.get(c["title"])]
        if not cands:
            break
        best = min(cands, key=lambda c: (abs(math.log(max(1, info[c["title"]]["length"])) - lt), c["title"]))
        used.add(best["title"]); pairs.append((x, best))
    return pairs


# ------------------------------------------------------------------ histories
def history(title, deadline):
    """-> (revs list of [revid, ts, u, flags, sha_id, size, undo_idx, restore_idx], truncated)."""
    revs, shas, undo_ref, rest_ref = [], {}, [], []
    cont = {}
    truncated = False
    while True:
        j = q({"action": "query", "prop": "revisions", "titles": title, "rvprop": "ids|timestamp|user|sha1|comment|size|tags",
               "rvlimit": "max", "rvdir": "newer", **cont})
        if j.get("error"):
            raise RuntimeError(f"history API error {j['error'].get('code')}")
        pages = (j.get("query") or {}).get("pages") or []
        for p in pages:
            for r in p.get("revisions") or []:
                u = r.get("user")
                hidden = bool(r.get("userhidden")) or not u
                fl = 0
                if hidden:
                    fl |= AG.F_HIDDEN
                else:
                    if A.ANON.match(u):
                        fl |= AG.F_ANON
                    if A.BOT.search(u):
                        fl |= AG.F_BOT
                c = r.get("comment") or ""
                if RV_RX.search(c):
                    fl |= AG.F_RVSUM
                if set(r.get("tags") or []) & REVERT_TAGS:
                    fl |= AG.F_RVTAG
                m1, m2 = UNDO_RX.search(c), RESTORE_RX.search(c)
                undo_ref.append(int(m1.group(1)) if m1 else None)
                rest_ref.append(int(m2.group(1)) if m2 else None)
                s = r.get("sha1") if not r.get("sha1hidden") else None
                sid = shas.setdefault(s, len(shas)) if s else -1
                revs.append([int(r["revid"]), AG.ep(r["timestamp"]), CO.h(u) if not hidden else None, fl, sid,
                             r.get("size"), -1, -1])
        if "continue" in j and len(revs) < MAX_REVS and time.time() < deadline:
            cont = {k: v for k, v in j["continue"].items()}
            continue
        truncated = "continue" in j
        break
    pos = {r[0]: k for k, r in enumerate(revs)}
    for k, (a, b) in enumerate(zip(undo_ref, rest_ref)):
        revs[k][6] = pos.get(a, -1) if a else -1
        revs[k][7] = pos.get(b, -1) if b else -1
    return revs, truncated


# ------------------------------------------------------------------ talk pages and !votes
H2 = re.compile(r"^==(?!=)\s*(.*?)\s*==\s*$", re.M)
VOTE = re.compile(r"^[*#]{1,2}\s*(?:<[^>]{0,40}>\s*)*(?:\{\{[^{}]{0,30}\}\}\s*)?'''\s*(?:\[\[[^\]|]*\|)?\s*"
                  r"(?:(?:strong(?:ly)?|weak|tentative|conditional|procedural|speedy|snow)\s+)?"
                  r"(support|oppose|include|exclude|keep|delete|merge|redirect|don'?t move|do not move|not moved|move|"
                  r"yes|no|agree|disagree|retain|remove|option\s*[a-z0-9]{1,3}|[a-d]|[1-4])\b", re.I)
SIG = re.compile(r"\[\[\s*:?\s*User(?: talk)?\s*:\s*([^\]|#/\n]+)", re.I)
UNSIGNED = re.compile(r"\{\{\s*unsigned2?\s*\|([^|}]+)", re.I)
TS_RX = re.compile(r"\d{1,2}:\d{2}, (\d{1,2}) (" + AG.MONTHS + r") (\d{4}) \(UTC\)")
POS = {"support", "include", "keep", "yes", "agree", "retain", "move"}
NEG = {"oppose", "exclude", "delete", "no", "disagree", "remove", "don't move", "dont move", "do not move", "not moved"}
AFD_TPL = re.compile(r"\{\{\s*(?:Old ?AfD multi|Old ?AfD full|Oldafdfull|Old ?AfD|Afd ?old)\b([^{}]*)\}\}", re.I)


def stance(s):
    s = re.sub(r"\s+", " ", s.lower().strip())
    if s in POS:
        return "pos"
    if s in NEG:
        return "neg"
    if s in ("merge", "redirect"):
        return "merge"
    m = re.match(r"(?:option ?)?([a-z0-9]{1,3})$", s)
    return f"opt:{m.group(1)}" if m else None


def norm_user(n):
    n = re.sub(r"[_\s]+", " ", n).strip()
    return n[:1].upper() + n[1:] if n else n


def parse_votes(text):
    """-> list of (hashed account, stance), first !vote per account; unsigned lines are skipped."""
    out, seen = [], set()
    for ln in text.splitlines():
        m = VOTE.match(ln)
        if not m:
            continue
        st = stance(m.group(1))
        if not st:
            continue
        sigs = SIG.findall(ln) or UNSIGNED.findall(ln)
        if not sigs:
            continue
        u = norm_user(sigs[-1])
        if not u or A.ANON.match(u) or A.BOT.search(u):
            continue
        hu = CO.h(u)
        if hu in seen:
            continue
        seen.add(hu); out.append([hu, st])
    return out


def first_month(text):
    best = None
    for d, mo, y in TS_RX.findall(text):
        k = (int(y), AG.MONTHS.split("|").index(mo) + 1)
        best = k if best is None or k < best else best
    return f"{best[0]}-{best[1]:02d}" if best else None


def talk_discussions(text, kind_hint=None):
    """Split a talk page (or an AfD page) into RfC / RM discussions -> list of {kind, ym, key, votes}."""
    out = []
    if kind_hint == "afd":
        v = parse_votes(text)
        if v:
            out.append({"kind": "afd", "ym": first_month(text), "key": (first_month(text) or "") + "|afd", "votes": v})
        return out
    hs = list(H2.finditer(text))
    for k, m in enumerate(hs):
        body = text[m.end(): hs[k + 1].start() if k + 1 < len(hs) else len(text)]
        head = m.group(1)
        if re.search(r"\{\{\s*rfc\b|\{\{\s*(?:closed )?rfc ?top|\{\{\s*rfc ?bottom", body, re.I) or \
                re.search(r"\bRfC\b|request for comment", head, re.I):
            kind = "rfc"
        elif re.search(r"\{\{\s*requested move|\{\{\s*rm ?top", body, re.I) or re.search(r"requested move|move request|^move\b", head, re.I):
            kind = "rm"
        else:
            continue
        v = parse_votes(body)
        if v:
            out.append({"kind": kind, "ym": first_month(body), "key": f"{head[:80]}|{first_month(body)}", "votes": v})
    return out


def afd_pages(text, title):
    res = []
    for m in AFD_TPL.finditer(text):
        params = m.group(1)
        pg = re.findall(r"\|\s*page\d*\s*=\s*([^|}\n]+)", params, re.I)
        res += [p.strip() for p in pg] or [title]
    return sorted({"Wikipedia:Articles for deletion/" + p for p in res})


def page_contents(titles):
    """-> {title: wikitext}; batches of 8 titles, following continuation."""
    out = {}
    for i in range(0, len(titles), 8):
        chunk = titles[i:i + 8]
        cont = {}
        for _ in range(20):
            j = q({"action": "query", "prop": "revisions", "titles": "|".join(chunk), "rvprop": "content", "rvslots": "main", **cont})
            for p in (j.get("query") or {}).get("pages") or []:
                for r in p.get("revisions") or []:
                    c = ((r.get("slots") or {}).get("main") or {}).get("content")
                    if c:
                        out[p["title"]] = c
            if "continue" in j:
                cont = dict(j["continue"]); continue
            break
    return out


def talk(title):
    pages = ["Talk:" + title]
    cont = {}
    for _ in range(10):
        j = q({"action": "query", "list": "allpages", "apnamespace": 1, "apprefix": title + "/", "aplimit": "max", **cont})
        for p in (j.get("query") or {}).get("allpages") or []:
            sub = p["title"].split("/", 1)[-1].lower()
            if re.search(r"archive|rfc|move|request", sub):
                pages.append(p["title"])
        if "continue" in j:
            cont = dict(j["continue"]); continue
        break
    pages = pages[:MAX_TALK_PAGES]
    texts = page_contents(pages)
    discs = []
    afd = set()
    for t, txt in texts.items():
        discs += talk_discussions(txt)
        afd.update(afd_pages(txt, title))
    if afd:
        for t, txt in page_contents(sorted(afd)[:10]).items():
            discs += talk_discussions(txt, "afd")
    seen, uniq = set(), []
    for d in discs:
        if d["key"] not in seen:
            seen.add(d["key"]); d.pop("key"); uniq.append(d)
    return uniq, len(texts)


# ------------------------------------------------------------------ leads
def lead_counts(revids):
    """-> {str(revid): lead critical-term count or None (hidden / missing)}; 50 per call, rvsection=0."""
    out = {}
    def parse(j):
        for p in (j.get("query") or {}).get("pages") or []:
            for r in p.get("revisions") or []:
                c = ((r.get("slots") or {}).get("main") or {}).get("content")
                if c is None:
                    out[str(r["revid"])] = None; continue
                pr = A.prose(A.split_lead(c))
                out[str(r["revid"])] = sum(A.count(k, pr) for k in A.CRITICAL)
    for i in range(0, len(revids), 50):
        chunk = revids[i:i + 50]
        j = q({"action": "query", "prop": "revisions", "revids": "|".join(map(str, chunk)), "rvprop": "ids|content",
               "rvslots": "main", "rvsection": 0})
        if j.get("error"):
            for r in chunk:                                     # fallback: one revision per call
                j1 = q({"action": "query", "prop": "revisions", "revids": str(r), "rvprop": "ids|content", "rvslots": "main",
                        "rvsection": 0})
                if not j1.get("error"):
                    parse(j1)
            continue
        parse(j)
    return out


# ------------------------------------------------------------------ collect
def _pool(fn, items, deadline, label, threads=THREADS):
    """Run fn over items with a thread pool until the deadline; -> (results by item index, errors, skipped)."""
    res, errs, skipped = {}, 0, 0
    lock = threading.Lock()
    def wrap(k, it):
        if time.time() > deadline:
            return k, "skip", None
        try:
            return k, "ok", fn(it)
        except Exception as e:
            print("ERR", label, type(e).__name__, str(e)[:120], file=sys.stderr, flush=True)
            return k, "err", None
    with ThreadPoolExecutor(threads) as ex:
        futs = [ex.submit(wrap, k, it) for k, it in enumerate(items)]
        for n, f in enumerate(as_completed(futs), 1):
            k, st, v = f.result()
            with lock:
                if st == "ok":
                    res[k] = v
                elif st == "err":
                    errs += 1
                else:
                    skipped += 1
            wt_net.heartbeat(f"guard-{label}", n, len(items), errors=errs, skipped=skipped)
    return res, errs, skipped


def collect():
    CO.salt()
    t0 = time.time()
    dl = lambda ph: t0 + PHASE_END[ph] * BUDGET_MIN * 60
    pl = json.load(open(os.path.join(OUT, "plan.json")))
    summ = {"budget_min": BUDGET_MIN}
    # arbcom
    pages = {}
    for label, title in ARBCOM.items():
        try:
            pages[label] = raw_page(title)
        except Exception:
            pages[label] = None
    ab = AG.arbcom_extract(pages)
    del pages
    json.dump(ab, open(os.path.join(OUT, "arbcom.json"), "w"), indent=1, ensure_ascii=False)
    print(f"guard arbcom: {sum(1 for v in ab['pages'].values() if v['found'])} pages, {len(ab['items'])} items, "
          f"leak check {ab['redaction_leak_check']}", flush=True)
    # resolve + match
    topic, pool = pl["topic"], pl["pool"]
    info = resolve([x["title"] for x in topic + pool])
    pairs = match(topic, pool, info)
    lim = int(os.environ.get("GUARD_LIMIT", "0"))
    if lim:
        pairs = pairs[:lim]
    arts = []
    for x, c in pairs:
        arts.append({"title": info[x["title"]]["title"], "group": "topic", "tier": x["tier"]})
        arts.append({"title": info[c["title"]]["title"], "group": "comparison", "tier": c["tier"]})
    seen = set(); arts = [a for a in arts if not (a["title"] in seen or seen.add(a["title"]))]
    summ.update({"topic_in_plan": len(topic), "topic_resolved": sum(1 for x in topic if info.get(x["title"])),
                 "matched_pairs": len(pairs), "articles": dict(Counter(a["group"] for a in arts))})
    print(f"guard scope: {summ['articles']} ({summ['topic_resolved']}/{len(topic)} topic resolved)", flush=True)
    # histories (seeded random order so a budget cut is not biased toward one group)
    order = list(range(len(arts))); random.Random(SEED).shuffle(order)
    H, err, skip = _pool(lambda k: history(arts[k]["title"], dl("history")), order, dl("history"), "history")
    for k, (revs, tr) in H.items():
        arts[order[k]]["revs"], arts[order[k]]["truncated"] = revs, tr
    summ["history"] = {"done": len(H), "errors": err, "skipped_budget": skip,
                       "truncated": sum(1 for a in arts if a.get("truncated"))}
    arts = [a for a in arts if "revs" in a]
    print(f"guard history: {summ['history']}, revisions {sum(len(a['revs']) for a in arts)}", flush=True)
    # talk pages
    T, err, skip = _pool(lambda a: talk(a["title"]), arts, dl("talk"), "talk")
    discs = []
    for k, (ds, npg) in T.items():
        arts[k]["talk_pages"] = npg
        for d in ds:
            discs.append({"a": arts[k]["title"], "group": arts[k]["group"], **d})
    summ["talk"] = {"articles_done": len(T), "errors": err, "skipped_budget": skip, "discussions": len(discs),
                    "talk_pages": sum(a.get("talk_pages", 0) for a in arts), "kinds": dict(Counter(d["kind"] for d in discs))}
    print(f"guard talk: {summ['talk']}", flush=True)
    # leads for reverts since 2021
    need = set()
    t_from = AG.ep(AG.LEAD_FROM)
    for a in arts:
        for rv in AG.find_reverts(a["revs"]):
            if rv["t"] >= t_from and rv["before"]:
                need.add((rv["before"], rv["after"]))
    pairs_l = sorted(need); random.Random(SEED + 1).shuffle(pairs_l)
    revids = list(dict.fromkeys(x for p in pairs_l for x in p))
    batches = [revids[i:i + 50] for i in range(0, len(revids), 50)]
    Lr, err, skip = _pool(lead_counts, batches, dl("leads"), "leads")
    leads = {}
    for v in Lr.values():
        leads.update(v)
    summ["leads"] = {"reverts_needing_direction": len(pairs_l), "revisions_needed": len(revids),
                     "revisions_measured": len(leads), "batches_done": len(Lr), "errors": err, "skipped_budget": skip}
    print(f"guard leads: {summ['leads']}", flush=True)
    summ["requests"] = wt_net.C["requests"]; summ["failures"] = wt_net.C["failures"]
    summ["elapsed_min"] = round((time.time() - t0) / 60, 1)
    out = {"summary": summ, "articles": arts, "discussions": discs, "leads": leads, "arbcom": ab}
    with gzip.open(os.path.join(OUT, "raw.json.gz"), "wt") as f:
        json.dump(out, f, separators=(",", ":"))
    print(f"guard collect done in {summ['elapsed_min']} min, {summ['requests']} requests", flush=True)
    if not arts or summ["history"]["errors"] > 0.05 * max(1, len(order)):
        sys.exit("guard collect: too many history errors (>5%) or no articles")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["plan", "collect"])
    a = ap.parse_args()
    if a.cmd == "plan":
        plan()
    else:
        collect()


if __name__ == "__main__":
    main()
