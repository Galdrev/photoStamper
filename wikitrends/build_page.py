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
    if len(d) > 60:
        a["lead_diff"] = [x for x in d if x["t"] != "="][:60]
    for k in ("top10", "crit0", "crit1", "conn0", "conn1", "lcrit0", "lcrit1", "critpre"):
        if a.get(k) is not None:
            a[k] = round(a[k], 3)

findings_path = os.path.join(HERE, "findings.html")
findings = open(findings_path).read() if os.path.exists(findings_path) else ""
tpl = open(os.path.join(HERE, "page_template.html")).read()
html = (tpl.replace("<!--FINDINGS-->", findings)
           .replace("/*DATA*/null", json.dumps(res, separators=(",", ":"))))
open(sys.argv[1], "w").write(html)
print(f"wrote {sys.argv[1]} ({len(html)/1e6:.1f} MB)")
