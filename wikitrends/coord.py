"""Coordination collector: one run-wide pseudonymous ID per account for the edits that matter (critical-term lead events).

  python coord.py plan                       -> data/coord/plan.json  (offline: event revisions from mass2_events + ratchet)
  python coord.py shard --shard I --of N     -> data/coord/coord_I.json.gz (checkpointed via mass._run; fails loudly >5% errors)
  python coord.py merge                      -> data/coord.json.gz, data/coord_summary.json
  python coord.py estimate                   -> request count / wall time (offline, from plan.json)
  COORD_LIMIT=20 ...                         -> test mode (first 20 articles of the shard)

Input: every exact critical-term insertion/removal (analyze.CRITICAL) in mass2_events (topic AND comparison articles), plus
the key-article events of data/ratchet.json that carry a revid. Unit of work = article (all its event revisions).
Per event revision:
  metadata  prop=revisions&revids=<=50 per call: user (hashed at once), timestamp, comment (class labels only), size, tags,
            sha1, parentid, minor; deleted / suppressed revisions and hidden users are recorded as states, not errors
  diff      action=compare fromrev=parentid torev=revid: only the added / removed sentences that contain the event's term
            (prose-cleaned, <=600 chars each, <=8 per side) + normalised 5-word shingles of each inserted sentence
  accounts  list=users (pilot.user_facts, 50 per call): registration month, rounded edit count, groups (allow-list), block
            status, block reason class; kept per salted hash
Privacy: usernames live only in memory. Hash = HMAC-SHA256(WT_SALT, username)[:16]; WT_SALT is one run-wide value passed to the
shards as a masked job output and never written to disk. Raw edit summaries are reduced to class labels (they can name
accounts). Note: revids are public, so a hash can be re-linked to an account by anyone with API access; the hash keeps names
out of files and cards, it is not anonymisation. Cards (analyze_coord.py) are aggregate only.
"""
import argparse, glob, gzip, hashlib, hmac, html, json, os, re, sys, time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wt_net                   # noqa: E402
import analyze as A             # noqa: E402
import pilot as P               # noqa: E402
import mass as M                # noqa: E402

KIND = "coord"
OUT = os.path.join(HERE, "data", "coord")
EN = "https://en.wikipedia.org/w/api.php"
MAX_SENT, SENT_CAP, SHINGLE = 8, 600, 5
VILLAGE = re.compile(r"^(?:village|place|town|locality|municipality[^,]*|former village|depopulated village|hamlet)\b.*"
                     r"(?:mandatory palestine|state of palestine|palestine|west bank|gaza)", re.I)
GROUPS_KEEP = {"autoconfirmed", "extendedconfirmed", "sysop", "rollbacker", "reviewer", "patroller", "bot", "checkuser",
               "oversight", "bureaucrat", "extendedmover", "templateeditor"}
TAGS_KEEP = {"mw-reverted", "mw-undo", "mw-rollback", "mw-manual-revert", "mw-blank", "mw-replace", "mobile edit",
             "mobile web edit", "visualeditor", "wikieditor", "possible vandalism", "discussiontools", "mw-new-redirect",
             "large unwikified new article", "references removed", "section blanking", "advanced mobile edit"}
COMMENT_CLASSES = [("revert", r"\b(?:rv|rvv|revert\w*|undid|undo\w*|rollback|restor\w*)\b"),
                   ("sock", r"\bsock\w*|block evasion|\bLTA\b|checkuser"),
                   ("ecr", r"\bARBPIA|\bARBECR|\bECR\b|extended[- ]confirmed|\b500/30\b|\bAE\b|contentious topic"),
                   ("consensus", r"consensus|\btalk\b|\bRfC\b|\bRM\b|discuss"),
                   ("pov", r"\bN?POV\b|neutral|bias|weasel|\bWP:LABEL|\bloaded\b"),
                   ("source", r"\bsourc\w*|\bcit\w*|\bref\w*|\bRS\b|unsourced|\bOR\b|synth"),
                   ("lead", r"\blead\b|\blede\b|first sentence|opening"),
                   ("copyedit", r"\bc/?e\b|copy ?edit|typo|grammar|wording|tweak|clarif")]
COMMENT_RX = [(k, re.compile(p, re.I)) for k, p in COMMENT_CLASSES]
_SALT = [None]


# ------------------------------------------------------------------ pseudonyms
def salt():
    if _SALT[0] is None:
        s = os.environ.get("WT_SALT")
        if not s:
            sys.exit("coord: WT_SALT is required (one run-wide salt, from the workflow's salt job); refusing to run with a "
                     "random salt, which would make hashes unlinkable across shards")
        _SALT[0] = s
    return _SALT[0]


def h(user):
    return hmac.new(salt().encode(), user.encode(), hashlib.sha256).hexdigest()[:16]


def comment_classes(c):
    if not c:
        return ["empty"]
    return [k for k, rx in COMMENT_RX if rx.search(c)] or ["other"]


# ------------------------------------------------------------------ text helpers
def norm_words(s):
    return re.findall(r"[a-z0-9]+", s.lower().replace("–", " ").replace("—", " "))


def shingles(s, k=SHINGLE):
    w = norm_words(s)
    if len(w) < k:
        return [" ".join(w)] if w else []
    return list(dict.fromkeys(" ".join(w[i:i + k]) for i in range(len(w) - k + 1)))


def sh_hash(x):
    return hashlib.blake2b(x.encode(), digest_size=5).hexdigest()


ROW = re.compile(r'<td[^>]*class="[^"]*diff-(addedline|deletedline)[^"]*"[^>]*>(.*?)</td>', re.S)


def diff_lines(body):
    """MediaWiki table diff -> (added lines, deleted lines) as plain wikitext."""
    add, rem = [], []
    for kind, cell in ROW.findall(body or ""):
        t = html.unescape(re.sub(r"<[^>]+>", "", cell)).strip()
        if t:
            (add if kind == "addedline" else rem).append(t)
    return add, rem


def line_sentences(lines):
    out = []
    for ln in lines:
        p = A.prose(ln)
        out += [re.sub(r"\s+", " ", s).strip() for s in A.sentences(p)]
    return [s for s in out if len(s) > 3]


def term_sentences(add_lines, rem_lines, terms):
    """Sentences added / removed by the edit that contain one of the event terms (sentence-level set difference)."""
    sa, sr = line_sentences(add_lines), line_sentences(rem_lines)
    na, nr = {" ".join(norm_words(s)) for s in sa}, {" ".join(norm_words(s)) for s in sr}
    def pick(ss, other):
        res, seen = [], set()
        for s in ss:
            n = " ".join(norm_words(s))
            if n in other or n in seen:
                continue
            ts = [t for t in terms if A.count(t, s) > 0]
            if ts:
                seen.add(n); res.append({"s": s[:SENT_CAP], "terms": ts})
        return res[:MAX_SENT]
    added, removed = pick(sa, nr), pick(sr, na)
    for x in added:
        x["sh"] = [sh_hash(z) for z in shingles(x["s"])]
    return added, removed


# ------------------------------------------------------------------ plan (offline)
def _load_gz_or_json(base):
    if os.path.exists(base):
        return json.load(open(base))
    return json.load(gzip.open(base + ".gz", "rt"))


def plan():
    from corpus import KEY_ARTICLES, KEY_ARTICLES_CONTROL
    meta = {}
    m2 = _load_gz_or_json(os.path.join(A.DATA, "mass2.json"))
    for r in m2["articles"]:
        d = (r.get("now") or {}).get("description") or ""
        meta[r["title"]] = {"group": r["group"], "stratum": r.get("stratum"), "project": r.get("project"),
                            "village": bool(r.get("project") == "Palestine" and VILLAGE.search(d))}
    del m2
    ev = json.load(gzip.open(os.path.join(A.DATA, "mass2_events.json.gz"), "rt"))["articles"]
    arts, n_src = {}, Counter()
    def add(title, revid, ts, term, kind, src, grp=None):
        if term not in A.CRITICAL or not revid:
            return
        a = arts.setdefault(title, {"title": title, **(meta.get(title) or {"group": grp, "stratum": None, "project": None,
                                                                            "village": False}), "revs": {}})
        r = a["revs"].setdefault(str(revid), {"revid": int(revid), "ts": ts, "events": []})
        if not any(e["term"] == term and e["kind"] == kind for e in r["events"]):
            r["events"].append({"term": term, "kind": kind, "src": src}); n_src[src] += 1
    for t, v in ev.items():
        for e in v.get("lead_events") or []:
            if e.get("exact"):
                add(t, e.get("revid"), e.get("ts"), e["term"], e["kind"], "mass2")
    rp = os.path.join(A.DATA, "ratchet.json")
    if os.path.exists(rp):
        rj = json.load(open(rp))
        for t, terms in (rj.get("events") or {}).items():
            grp = "topic" if t in KEY_ARTICLES else "comparison" if t in KEY_ARTICLES_CONTROL else None
            for term, lst in terms.items():
                for e in lst:
                    if e.get("revid"):
                        ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(e["t"])) if e.get("t") else None
                        add(t, e["revid"], ts, term, e["kind"], "ratchet", grp)
    rows = []
    for a in arts.values():
        a["revs"] = sorted(a["revs"].values(), key=lambda r: r["revid"])
        if a.get("group") in ("topic", "comparison"):
            rows.append(a)
    rows.sort(key=lambda a: a["title"])
    os.makedirs(OUT, exist_ok=True)
    out = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "rows": rows,
           "n_events": dict(n_src), "n_revisions": sum(len(a["revs"]) for a in rows),
           "by_group": dict(Counter(a["group"] for a in rows))}
    json.dump(out, open(os.path.join(OUT, "plan.json"), "w"))
    print(f"coord plan: {len(rows)} articles, {out['n_revisions']} revisions, events {dict(n_src)}, {out['by_group']}")
    return out


# ------------------------------------------------------------------ collect
RVPROP = "ids|timestamp|user|comment|size|tags|sha1|flags"


def rev_meta(revids):
    """-> {revid: meta dict or {'state': 'missing'}}. Network failure raises (article error, retried on resume)."""
    out = {}
    for i in range(0, len(revids), 50):
        chunk = revids[i:i + 50]
        j = wt_net.get_json(EN, {"action": "query", "prop": "revisions", "revids": "|".join(map(str, chunk)),
                                 "rvprop": RVPROP, "rvslots": "main", "format": "json", "formatversion": 2})
        if j is None:
            raise RuntimeError(f"revision metadata failed after retries ({len(chunk)} revids)")
        if j.get("error"):
            raise RuntimeError(f"revision metadata API error {j['error'].get('code')}")
        qy = j.get("query") or {}
        bad = qy.get("badrevids") or {}
        for k in (bad.values() if isinstance(bad, dict) else bad):
            out[int(k.get("revid"))] = {"state": "missing"}
        for p in qy.get("pages") or []:
            for r in p.get("revisions") or []:
                out[int(r["revid"])] = {"state": "ok", **r}
    for r in revids:
        out.setdefault(int(r), {"state": "missing"})
    return out


def fetch_diff(parentid, revid):
    """-> (status, body, size_delta). status: ok | empty | creation | deleted | hidden | failed."""
    if not parentid:
        return "creation", None, None
    j = wt_net.get_json(EN, {"action": "compare", "fromrev": parentid, "torev": revid, "prop": "diff|size",
                             "difftype": "table", "format": "json", "formatversion": 2})
    if j is None:
        return "failed", None, None
    if j.get("error"):
        code = str(j["error"].get("code"))
        if code in ("nosuchrevid", "missingcontent", "nosuchpageid", "missingtitle"):
            return "deleted", None, None
        if code in ("permissiondenied", "revdeleted", "suppressed") or "hidden" in code or "deleted" in code:
            return "hidden", None, None
        return "failed", None, None
    c = j.get("compare") or {}
    body = c.get("body")
    delta = (c["tosize"] - c["fromsize"]) if isinstance(c.get("tosize"), int) and isinstance(c.get("fromsize"), int) else None
    if not body or not body.strip():
        return "empty", "", delta
    return "ok", body, delta


def acct_record(f):
    if f is None:
        return {"missing": True}
    ec = f.get("ec")
    ec_r = int(float(f"{ec:.2g}")) if ec else (0 if ec == 0 else None)
    return {"reg": (f.get("reg") or "")[:7] or None, "ec": ec_r, "ext": f.get("ext"), "groups": sorted(set(f.get("groups") or []) & GROUPS_KEEP),
            "blocked": f.get("blocked"), "indef": f.get("indef"), "partial": f.get("partial"), "breason": f.get("breason")}


def collect(row):
    revids = [r["revid"] for r in row["revs"]]
    meta = rev_meta(revids)
    users = {m.get("user") for m in meta.values() if m.get("user")}
    reg = {u for u in users if not A.ANON.match(u) and not A.BOT.search(u)}
    facts = user_facts(reg) if reg else {}
    out_revs, accounts = [], {}
    for pr in row["revs"]:
        m = meta.get(pr["revid"]) or {"state": "missing"}
        terms = sorted({e["term"] for e in pr["events"]})
        rec = {"revid": pr["revid"], "events": pr["events"], "ts": m.get("timestamp") or pr.get("ts"), "state": m["state"]}
        if m["state"] == "ok":
            u = m.get("user")
            hidden = bool(m.get("userhidden")) or not u
            anon = bool(u and A.ANON.match(u)); bot = bool(u and A.BOT.search(u))
            rec.update({"parentid": m.get("parentid"), "u": h(u) if u and not hidden else None, "user_hidden": hidden,
                        "anon": anon if not hidden else None, "bot": bot if not hidden else None,
                        "comment_hidden": bool(m.get("commenthidden")), "comment_class": comment_classes(m.get("comment")),
                        "size": m.get("size"), "sha1": m.get("sha1") if not m.get("sha1hidden") else None,
                        "tags": sorted(set(m.get("tags") or []) & TAGS_KEEP), "minor": bool(m.get("minor")),
                        "suppressed": bool(m.get("suppressed")), "text_hidden": bool(m.get("texthidden"))})
            if u and not hidden and not anon and not bot:
                f = facts.get(u)
                accounts[rec["u"]] = acct_record(f)
                if f and f.get("reg") and rec["ts"]:
                    rec["age_d"] = int((P.ep(rec["ts"]) - P.ep(f["reg"])) / 86400)
            if m.get("texthidden"):
                st, body, delta = "hidden", None, None
            else:
                st, body, delta = fetch_diff(m.get("parentid"), pr["revid"])
            rec["diff_status"], rec["delta"] = st, delta
            if st == "ok":
                ad, rm = diff_lines(body)
                rec["added"], rec["removed"] = term_sentences(ad, rm, terms)
            if st == "failed":
                rec["error"] = "diff_failed"
        else:
            rec["diff_status"] = "missing"
        out_revs.append(rec)
    return {"title": row["title"], "group": row["group"], "stratum": row.get("stratum"), "village": row.get("village", False),
            "revs": out_revs, "accounts": accounts}


def user_facts(names):
    """pilot.user_facts (as used by mass2) plus the group list; cached per username in memory only, never written."""
    with P._ulock:
        todo = sorted(n for n in names if n not in P._ucache)
    for i in range(0, len(todo), 50):
        chunk = todo[i:i + 50]
        j = P.q({"action": "query", "list": "users", "ususers": "|".join(chunk),
                 "usprop": "editcount|registration|groups|blockinfo"}, core=False)
        got = {}
        for u in (j or {}).get("query", {}).get("users", []):
            if u.get("missing") or u.get("invalid"):
                got[u.get("name")] = None; continue
            got[u["name"]] = {"reg": u.get("registration"), "ec": u.get("editcount"), "groups": u.get("groups") or [],
                              "ext": bool({"extendedconfirmed", "sysop"} & set(u.get("groups") or [])),
                              "blocked": "blockid" in u,
                              "indef": "blockid" in u and str(u.get("blockexpiry")) in ("infinite", "infinity"),
                              "partial": bool(u.get("blockpartial")),
                              "breason": P.block_reason(u.get("blockreason")) if "blockid" in u else None}
        with P._ulock:
            for n in chunk:
                P._ucache[n] = got.get(n)
    with P._ulock:
        return {n: P._ucache.get(n) for n in names}


# ------------------------------------------------------------------ shard / merge
def load_plan():
    return json.load(open(os.path.join(OUT, "plan.json")))


def rev_error_share(recs):
    revs = [r for a in recs for r in a["revs"]]
    return (sum(1 for r in revs if r.get("error")) / len(revs)) if revs else 0.0, len(revs)


def run_shard(i, n):
    salt()
    pl = load_plan()
    rows = M.shard(pl["rows"], i, n)
    lim = int(os.environ.get("COORD_LIMIT", "0"))
    rows = rows[:lim] if lim else rows
    print(f"coord shard {i}/{n}: {len(rows)} articles, {sum(len(r['revs']) for r in rows)} revisions", flush=True)
    M.OUT = OUT
    os.makedirs(OUT, exist_ok=True)
    M._run(KIND, collect, rows, i)          # exits non-zero if >5% of articles raised
    recs = json.load(gzip.open(os.path.join(OUT, f"{KIND}_{i}.json.gz"), "rt"))
    share, nrev = rev_error_share(recs)
    print(f"coord shard {i}: {nrev} revisions, revision-level error share {share:.3%}", flush=True)
    if share > 0.05:
        # drop failed revisions' articles from the checkpoint so a re-run retries them, then fail loudly
        keep = [a for a in recs if not any(r.get("error") for r in a["revs"])]
        p = os.path.join(OUT, f"{KIND}_{i}.json.gz")
        json.dump(keep, gzip.open(p + ".tmp", "wt")); os.replace(p + ".tmp", p)
        sys.exit(f"coord shard {i}: {share:.1%} of revisions failed (>5%) - re-run to resume")


def merge():
    pl = load_plan()
    recs, seen = [], set()
    for f in sorted(glob.glob(os.path.join(OUT, f"{KIND}_*.json.gz"))):
        for r in json.load(gzip.open(f, "rt")):
            if r["title"] not in seen:
                seen.add(r["title"]); recs.append(r)
    recs.sort(key=lambda r: r["title"])
    accounts, revisions, arts = {}, [], {}
    for a in recs:
        arts[a["title"]] = {"group": a["group"], "stratum": a.get("stratum"), "village": a.get("village", False)}
        for k, v in a["accounts"].items():
            accounts.setdefault(k, v)
        for r in a["revs"]:
            revisions.append({"title": a["title"], **r})
    co = {}
    for r in revisions:
        if not r.get("u") or r.get("anon") or r.get("bot"):
            continue
        c = co.setdefault(r["u"], {"articles": set(), "groups": Counter(), "events": []})
        c["articles"].add(r["title"]); c["groups"][arts[r["title"]]["group"]] += 1
        for e in r["events"]:
            c["events"].append([r["title"], r["ts"], e["term"], e["kind"]])
    co = {k: {"articles": sorted(v["articles"]), "groups": dict(v["groups"]), "events": sorted(v["events"], key=lambda x: x[1] or "")}
          for k, v in co.items()}
    st = Counter(r.get("diff_status") for r in revisions)
    share, nrev = rev_error_share(recs)
    summ = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n_articles_expected": len(pl["rows"]),
            "n_articles": len(recs), "n_revisions": nrev, "revision_error_share": share, "diff_status": dict(st),
            "rev_state": dict(Counter(r.get("state") for r in revisions)),
            "user_hidden": sum(1 for r in revisions if r.get("user_hidden")), "anon": sum(1 for r in revisions if r.get("anon")),
            "accounts": len(accounts), "accounts_missing": sum(1 for v in accounts.values() if v.get("missing")),
            "inserted_sentences": sum(len(r.get("added") or []) for r in revisions),
            "removed_sentences": sum(len(r.get("removed") or []) for r in revisions),
            "by_group": dict(Counter(a["group"] for a in recs))}
    out = {"note": "Coordination data: critical-term event revisions. Accounts are HMAC-SHA256(run salt, username)[:16]; the "
                   "salt is never stored. Edit summaries are class labels. Sentences are term-bearing added/removed prose.",
           "summary": summ, "articles": arts, "revisions": revisions, "accounts": accounts, "coactivity": co}
    with gzip.open(os.path.join(A.DATA, "coord.json.gz"), "wt") as f:
        json.dump(out, f, separators=(",", ":"))
    json.dump(summ, open(os.path.join(A.DATA, "coord_summary.json"), "w"), indent=1)
    print("coord merged:", json.dumps(summ, indent=1), flush=True)
    if len(recs) < 0.95 * len(pl["rows"]) or share > 0.05:
        sys.exit(f"coord merge: {len(recs)}/{len(pl['rows'])} articles, revision error share {share:.1%} - incomplete")


def estimate(n_shards=4, eff_rps=1.0, retry_factor=1.15, acct_per_rev=0.55):
    """Requests: ceil(revs/50) metadata calls per article + 1 compare per revision (minus creations) + users/50."""
    pl = load_plan()
    meta = sum(-(-len(a["revs"]) // 50) for a in pl["rows"])
    diffs = pl["n_revisions"]
    users = int(pl["n_revisions"] * acct_per_rev / 50) + len(pl["rows"])    # chunks are per article (cache is per process)
    users = min(users, int(pl["n_revisions"] * acct_per_rev))
    tot = meta + diffs + users
    per = tot / n_shards * retry_factor
    res = {"articles": len(pl["rows"]), "revisions": pl["n_revisions"], "metadata_requests": meta, "compare_requests": diffs,
           "users_requests_upper": users, "total": tot, "total_with_retries": int(tot * retry_factor), "shards": n_shards,
           "per_shard": int(per), "hours_per_shard_at_eff_rps": round(per / eff_rps / 3600, 2)}
    print(json.dumps(res, indent=1))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["plan", "shard", "merge", "estimate"])
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--of", type=int, default=4)
    a = ap.parse_args()
    if a.cmd == "plan":
        plan()
    elif a.cmd == "shard":
        run_shard(a.shard, a.of)
    elif a.cmd == "merge":
        merge()
    else:
        estimate(a.of)


if __name__ == "__main__":
    main()
