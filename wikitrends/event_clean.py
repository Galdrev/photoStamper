"""Amendment D (SPEC_STUDY3): study 1's critical-rate DiD, split into narrative residual vs event updates.

  python event_clean.py -> data/event_clean.json
For every quarterly snapshot of every deep-tier article, sentences about recent events (event_filter.py) are separated from
the rest. Outcomes per part (full text, lead):
  unfiltered     critical hits per 10k words (as in study 1)
  residual       critical hits per 10k words of the residual text           (narrative, primary)
  resid_share    residual critical hits per 10k words of ALL text           (additive decomposition:
  event_share    event critical hits per 10k words of ALL text               unfiltered = resid_share + event_share)
Both filter levels (sentence = primary, paragraph = sensitivity). Windows: whole, pre-war, post-war.
"""
import glob, gzip, json, os

import analyze as A
import event_filter as EF

OUTCOMES = ("unfiltered", "residual", "resid_share", "event_share")


def part_rates(text, min_words, level):
    m = A.measure(text, min_words)
    if m is None:
        return None
    res, ev, st = EF.split(text, level)
    cr = lambda t: sum(A.count(k, t) for k in A.CRITICAL) if t else 0
    rw = len(A.re.findall(r"\w+", res)); c_res, c_ev = cr(res), cr(ev)
    return {"rate": {"unfiltered": m["rate"]["critical_rate"],
                     "residual": c_res * 1e4 / rw if rw >= min_words / 2 else None,
                     "resid_share": c_res * 1e4 / m["words"], "event_share": c_ev * 1e4 / m["words"]},
            "event_sent_share": st["event_share"]}


def main():
    manifest = json.load(open(os.path.join(A.DATA, "manifest.json")))
    arts = []
    for fn in sorted(glob.glob(os.path.join(A.ART, "*.json.gz"))):
        rec = json.load(gzip.open(fn, "rt", encoding="utf-8"))
        if rec["title"] not in manifest:
            continue
        rec["group"], rec["subgroup"] = manifest[rec["title"]]
        a = A.analyze_article(rec)
        if not a["series"]:
            continue
        a["ev_series"] = {lv: [{"date": s["date"],
                                "full": part_rates(s["_fp"], A.MIN_WORDS_FULL, lv),
                                "lead": part_rates(s["lead_text"], A.MIN_WORDS_LEAD, lv)} for s in a["series"]]
                          for lv in ("sentence", "paragraph")}
        arts.append(a)
    dates = sorted({s["date"] for a in arts for s in a["series"]}); first, last = dates[0], dates[-1]
    for a in arts:
        a["primary"] = A.exact(a["series"], first) is not None and a["group"] in ("treatment", "control") \
            and a["title"] not in A.CONTROL_CONTAMINATED
    T = [a for a in arts if a["primary"] and a["group"] == "treatment"]; C = [a for a in arts if a["primary"] and a["group"] == "control"]

    def ch(G, lv, part, k, d0, d1):
        out = []
        for a in G:
            s0, s1 = A.exact(a["ev_series"][lv], d0), A.at(a["ev_series"][lv], d1)
            v0 = s0 and s0[part] and s0[part]["rate"][k]; v1 = s1 and s1[part] and s1[part]["rate"][k]
            if v0 is not None and v1 is not None and s0[part] and s1[part]:
                out.append(v1 - v0)
        return A.np.array(out)

    tests = []
    for lv in ("sentence", "paragraph"):
        for part in ("lead", "full"):
            for wname, d0, d1 in (("whole", first, last), ("pre-war", first, A.PRE_WAR), ("post-war", A.PRE_WAR, last)):
                for k in OUTCOMES:
                    r = A.did_test(ch(T, lv, part, k, d0, d1), ch(C, lv, part, k, d0, d1))
                    if r:
                        for kk in ("_perm", "_t", "_c"):
                            r.pop(kk, None)
                        tests.append({"level": lv, "part": part, "window": wname, "outcome": k, **r})
    share = {g: {d: A.mean([s["full"]["event_sent_share"] for a in G for s in a["ev_series"]["sentence"] if s["date"] == d and s["full"]])
                 for d in dates} for g, G in (("treatment", T), ("control", C))}
    per_article = {a["title"]: {"group": a["group"], "ev_series": a["ev_series"]["sentence"]} for a in arts}
    json.dump({"dates": dates, "n_t": len(T), "n_c": len(C), "tests": tests, "event_sentence_share": share, "articles": per_article},
              open(os.path.join(A.DATA, "event_clean.json"), "w"))
    for t in tests:
        if t["level"] == "sentence" and t["window"] in ("whole", "post-war"):
            print(f"{t['part']:4} {t['window']:8} {t['outcome']:12} DiD {t['did']:+.2f} [{t['lo']:+.2f},{t['hi']:+.2f}] p={t['p_perm']:.3f}")


if __name__ == "__main__":
    main()
