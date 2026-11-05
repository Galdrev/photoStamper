"""Build masked, order-randomised coding batches for study 3 Part C (frozen 2026-11-05).

Selection (frozen): every topic pair (group == "treatment") with change > 0.05 and every
comparison pair (group in {control, control_contaminated}), minus pairs that auto_kpis flags
as parse artefacts (template/navbox residue). Excluded pairs are listed in the key.

Masking: the coder sees only the cleaned texts of the two leads, called Version A and
Version B, plus (where the input has first_sentence_edits) an unordered list of other
first-sentence variants with no timestamps, edit summaries, reverted flags or sizes.
No title, no group, no dates. Pair ids are salted hashes.
Each coder gets the same batch composition but an independent A/B orientation and item
order (seeded per coder), so position effects do not line up across coders.

Outputs in OUT_DIR:
  coder1/batch_01.json ...   coder2/batch_01.json ...   (give these to the coders)
  KEY_DO_NOT_SHARE.json      (title, group, change, d0, length tercile, orientation per coder)

Usage: python make_batches.py IN.json OUT_DIR [--seed S] [--coders 2] [--batch-size 20] [--max-variants 8]
"""
import argparse
import hashlib
import json
import math
import os
import random
import re

from auto_kpis import clean_lead, first_sentence, is_parse_artefact, in_analysis_set, tercile, words, group_of

CODEBOOK_VERSION = "study3-partC-v1.0-frozen-2026-11-05"


def _norm(s):
    return re.sub(r"\s+", " ", (s or "").replace("&nbsp;", " ")).strip()


def pair_id(salt, title):
    return "P" + hashlib.sha1(f"{salt}|{title}".encode()).hexdigest()[:8]


def variants(x, a_text, b_text, rng, max_n):
    """Distinct first-sentence texts seen in the traced edits, excluding any that already
    appear in Version A or B; shuffled; capped."""
    seen, out = set(), []
    a_n, b_n = _norm(a_text), _norm(b_text)
    for e in x.get("first_sentence_edits") or []:
        for s in (e.get("before"), e.get("after")):
            s = _norm(clean_lead(s))
            if len(s) < 20 or s in seen:
                continue
            seen.add(s)
            if s in a_n or s in b_n:
                continue
            out.append(s)
    rng.shuffle(out)
    return out[:max_n]


def build(path_in, out_dir, seed="study3-partC", n_coders=2, batch_size=20, max_variants=8):
    data = json.load(open(path_in))
    salt = hashlib.sha1(f"salt|{seed}".encode()).hexdigest()[:16]
    selected, excluded = [], []
    for x in data:
        if not in_analysis_set(x):
            continue
        if is_parse_artefact(x.get("lead0")) or is_parse_artefact(x.get("lead1")):
            excluded.append({"title": x["title"], "group": x["group"], "reason": "parse_artefact"})
            continue
        selected.append(x)
    ids = {x["title"]: pair_id(salt, x["title"]) for x in selected}
    assert len(set(ids.values())) == len(ids), "pair id collision"

    rng = random.Random(f"{seed}|pairs")
    order = sorted(selected, key=lambda x: ids[x["title"]])
    rng.shuffle(order)
    n_batches = max(1, math.ceil(len(order) / batch_size))
    batches = [order[i::n_batches] for i in range(n_batches)]   # even sizes, groups mixed

    key = {"codebook_version": CODEBOOK_VERSION, "seed": seed, "salt": salt, "source": os.path.abspath(path_in),
           "selection": "topic change > 0.05 + all comparison, minus parse artefacts",
           "pairs": {}, "orientation": {}, "excluded": excluded}
    for b, xs in enumerate(batches, 1):
        for x in xs:
            key["pairs"][ids[x["title"]]] = {
                "title": x["title"], "group": x["group"], "grp": group_of(x["group"]), "change": x.get("change"),
                "d0": x.get("d0"), "d1": x.get("d1"), "lead0_words": words(x.get("lead0")),
                "tercile": tercile(words(x.get("lead0"))), "batch": b,
                "has_variants": int(bool(x.get("first_sentence_edits")))}

    for c in range(1, n_coders + 1):
        cdir = os.path.join(out_dir, f"coder{c}")
        os.makedirs(cdir, exist_ok=True)
        key["orientation"][f"coder{c}"] = {}
        for b, xs in enumerate(batches, 1):
            crng = random.Random(f"{seed}|coder{c}|batch{b}")
            items = []
            for x in sorted(xs, key=lambda x: ids[x["title"]]):
                pid = ids[x["title"]]
                old, new = clean_lead(x.get("lead0")), clean_lead(x.get("lead1"))
                a_is_old = crng.random() < 0.5
                a, bb = (old, new) if a_is_old else (new, old)
                key["orientation"][f"coder{c}"][pid] = "A=old" if a_is_old else "A=new"
                vrng = random.Random(f"{seed}|coder{c}|{pid}|variants")
                items.append({"id": pid, "version_A": a, "version_B": bb,
                              "other_first_sentence_variants": variants(x, a, bb, vrng, max_variants)})
            crng.shuffle(items)
            batch = {"batch_id": f"b{b:02d}", "coder": f"coder{c}", "codebook_version": CODEBOOK_VERSION,
                     "n_items": len(items), "items": items}
            json.dump(batch, open(os.path.join(cdir, f"batch_{b:02d}.json"), "w"), ensure_ascii=False, indent=1)
    json.dump(key, open(os.path.join(out_dir, "KEY_DO_NOT_SHARE.json"), "w"), ensure_ascii=False, indent=1)
    return key, batches


def leak_check(out_dir, key):
    """Batch files may hold only the masked fields: no title, group, dates or edit metadata."""
    bad = []
    for c in key["orientation"]:
        cdir = os.path.join(out_dir, c)
        for f in sorted(os.listdir(cdir)):
            b = json.load(open(os.path.join(cdir, f)))
            if set(b) != {"batch_id", "coder", "codebook_version", "n_items", "items"}:
                bad.append((f, "unexpected batch fields"))
            for it in b["items"]:
                if set(it) != {"id", "version_A", "version_B", "other_first_sentence_variants"}:
                    bad.append((f, it["id"], "unexpected item fields"))
                if not all(isinstance(v, str) for v in it["other_first_sentence_variants"]):
                    bad.append((f, it["id"], "variant metadata"))
    return bad


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("path_in")
    ap.add_argument("out_dir")
    ap.add_argument("--seed", default="study3-partC")
    ap.add_argument("--coders", type=int, default=2)
    ap.add_argument("--batch-size", type=int, default=20)
    ap.add_argument("--max-variants", type=int, default=8)
    a = ap.parse_args()
    key, batches = build(a.path_in, a.out_dir, a.seed, a.coders, a.batch_size, a.max_variants)
    P = key["pairs"].values()
    print(f"pairs: {len(key['pairs'])} (topic {sum(p['grp'] == 'topic' for p in P)}, "
          f"comparison {sum(p['grp'] == 'comparison' for p in P)}); excluded: {len(key['excluded'])}; "
          f"batches: {len(batches)} of sizes {[len(b) for b in batches]}")
    for c, o in key["orientation"].items():
        print(c, "A=old share:", round(sum(v == "A=old" for v in o.values()) / len(o), 3))
    print("leak check:", leak_check(a.out_dir, key) or "clean")
