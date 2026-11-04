"""Inline results.json + findings.html into the report page.

Usage: python build_page.py OUT.html
"""
import json, os, sys

HERE = os.path.dirname(__file__)
res = json.load(open(os.path.join(HERE, "data", "results.json")))

for a in res["articles"]:
    fs, out = a["first_sentences"], []
    for x in fs:
        if not out or out[-1]["s"] != x["s"]:
            out.append(x)
    a["first_sentences"] = out
    # keep diffs compact: drop long unchanged runs
    d = a["lead_diff"]
    a["lead_changed"] = sum(x["t"] != "=" for x in d)
    a["lead_truncated"] = len(d) > 60
    if len(d) > 60:
        a["lead_diff"] = [x for x in d if x["t"] != "="][:60]
    for k in ("top10", "crit0", "crit1", "conn0", "conn1", "lcrit0", "lcrit1"):
        if a.get(k) is not None:
            a[k] = round(a[k], 3)

for name, key in (("bisect.json", "trace"), ("crosslang.json", "crosslang"), ("ratchet.json", "ratchet")):
    p = os.path.join(HERE, "data", name)
    res[key] = json.load(open(p)) if os.path.exists(p) else None
if res.get("crosslang"):
    for langs in res["crosslang"]["articles"].values():
        for v in langs.values():
            s = v["series"]
            v["series"] = [s[0], s[-1]] if len(s) > 1 else s
mp = os.path.join(HERE, "data", "mass_results.json")
if os.path.exists(mp) and "mass" not in res:
    res["mass"] = json.load(open(mp)).get("mass")
qa_p = os.path.join(HERE, "data", "qa.json")
if os.path.exists(qa_p):
    qa = json.load(open(qa_p)); qa.pop("per_article", None); res["qa"] = qa

# Reader exposure: monthly pageviews x which first-sentence variant was live (from the ratchet timeline)
def exposure(res):
    if not res.get("ratchet"):
        return None
    pv = {a["title"]: a.get("pv_monthly") for a in res["articles"] if a.get("pv_monthly")}
    out = {}
    for t, a in res["ratchet"]["articles"].items():
        if t not in pv or not a.get("fs_timeline"):
            continue
        tl = a["fs_timeline"]; var = {v["id"]: v["s"] for v in a["fs_variants"]}
        views = Counter()
        for ym, n in pv[t].items():              # 'YYYYMM'
            day = f"{ym[:4]}-{ym[4:6]}-15"
            live = None
            for d, vid, _ in tl:
                if d <= day:
                    live = vid
                else:
                    break
            if live is not None:
                views[live] += n
        tot = sum(views.values())
        out[t] = {"total_views": tot, "variants": [{"s": var.get(v, "")[:300], "views": n, "share": n / tot if tot else 0}
                                                   for v, n in views.most_common(6)]}
    return out


from collections import Counter
res["exposure"] = exposure(res)

findings_path = os.path.join(HERE, "findings.html")
findings = open(findings_path).read() if os.path.exists(findings_path) else ""
tpl = open(os.path.join(HERE, "page_template.html")).read()
html = (tpl.replace("<!--FINDINGS-->", findings)
           .replace("/*DATA*/null", json.dumps(res, separators=(",", ":")).replace("</", "<\\/")))
open(sys.argv[1], "w").write(html)
print(f"wrote {sys.argv[1]} ({len(html)/1e6:.1f} MB)")
