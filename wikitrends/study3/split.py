"""Study 3 split (written before any study-3 hypothesis): deterministic 50/50 article split by sha1(title).

  python study3_split.py -> data/study3/split.json, discovery_deep.json, discovery_mass.json
Discovery half: hypotheses may be generated from it freely. Holdout half: untouched until SPEC_STUDY3.md is frozen.
"""
import hashlib, json, os
import os; D = os.path.join(os.path.dirname(__file__), "..", "data")
half = lambda t: "discovery" if int(hashlib.sha1(("study3|" + t).encode()).hexdigest(), 16) % 2 == 0 else "holdout"

res = json.load(open(f"{D}/results.json")); mass = json.load(open(f"{D}/mass_results.json"))["mass"]
split = {"deep": {a["title"]: half(a["title"]) for a in res["articles"]},
         "mass": {a["t"]: half(a["t"]) for a in mass["lab_articles"]}}
json.dump(split, open(f"{D}/study3/split.json", "w"), indent=0)
keep = {k: res[k] for k in ("dates", "lexicon", "frames", "pre_war", "first_post_war", "week0", "n_weeks") if k in res}
keep["articles"] = [a for a in res["articles"] if split["deep"][a["title"]] == "discovery"]
json.dump(keep, open(f"{D}/study3/discovery_deep.json", "w"))
json.dump({"dates": mass["dates"], "lab_frames": mass["lab_frames"],
           "articles": [a for a in mass["lab_articles"] if split["mass"][a["t"]] == "discovery"]},
          open(f"{D}/study3/discovery_mass.json", "w"))
for tier in ("deep", "mass"):
    v = list(split[tier].values()); print(tier, "discovery", v.count("discovery"), "holdout", v.count("holdout"))
