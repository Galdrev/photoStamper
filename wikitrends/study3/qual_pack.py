"""Study 3 qualitative packs: lead pairs (2021-01 vs latest) + exact first-sentence edit traces, split by the frozen study-3 halves.

  python study3_qual_pack.py -> data/study3/qual_discovery.json, data/study3/qual_holdout.json (holdout not opened until codebook frozen)
"""
import difflib, json
import os; D = os.path.join(os.path.dirname(__file__), "..", "data")
split = json.load(open(f"{D}/study3/split.json"))["deep"]
leads = json.load(open(f"{D}/leads.json")); traces = json.load(open(f"{D}/bisect.json"))
for half in ("discovery", "holdout"):
    out = []
    for a in leads:
        if split.get(a["title"]) != half or not a.get("lead0") or not a.get("lead1"):
            continue
        sim = difflib.SequenceMatcher(None, a["lead0"], a["lead1"], autojunk=False).ratio()
        out.append({"title": a["title"], "group": a["group"], "d0": a["d0"], "d1": a["d1"], "change": round(1 - sim, 3),
                    "lead0": a["lead0"], "lead1": a["lead1"],
                    "first_sentence_edits": [{k: e.get(k) for k in ("timestamp", "comment", "reverted", "size_delta", "before", "after")}
                                             for e in traces.get(a["title"], [])]})
    out.sort(key=lambda r: -r["change"])
    json.dump(out, open(f"{D}/study3/qual_{half}.json", "w"), ensure_ascii=False)
    print(half, len(out), "articles;", sum(r["change"] > 0.05 for r in out), "changed >5%;", sum(bool(r["first_sentence_edits"]) for r in out), "with traces")
