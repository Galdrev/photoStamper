"""Elsewhere on Wikipedia: build patterns/trail/verified.json from the verification fetch (wikitrends-verify workflow).

Usage: python verify_extract.py <wikitrends-data checkout>/verify/42847367759 <...>/verify/42848274633
Each run directory holds, per article, the section-0 wikitext of the revision live on 1 Jan 2021 (or of the first revision
when the article is younger), of the latest revision, and the first-sentence history since 2021 (no usernames, no
comments other than page moves). Opening section = analyze.prose(analyze.split_lead(section 0)), first sentence =
analyze.sentences(...)[0], as everywhere in the project. The decisions are VERIFIED.md's, by hand; this script only
writes the texts, the revision references and the dates of each key phrase, so the flash build can check its quotes.
"""
import gzip, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
import analyze as A, analyze_trail as AT

DECISIONS = {
    "Criticism of Israel": ("KEEP", "real rewrite: the 2021 second sentence became the first (1 Jul 2025) and gained the Nakba, the Israeli occupation and Zionist political violence"),
    "Palestinian political violence": ("KEEP", "real change: “or terror(ism)” left the first sentence (10 Dec 2025), which now explains the violence as insurgency by a people without a state"),
    "Plan Dalet": ("KEEP", "real change: from “a plan worked out by the Haganah” to “a Zionist military plan … for the conquest of territory” (4 Jun 2023), and the Nakba in sentence 2 (14 Aug 2024)"),
    "Causes of the 1948 Palestinian expulsion and flight": ("KEEP", "real change in sentence 2: from “great controversy” to “most scholars consider that the majority … were directly expelled” (15 Aug 2024)"),
    "Comparisons between Israel and Nazi Germany": ("DROP", "rename and rewrite: the 2021 article was “Holocaust inversion” (moved 7 Apr 2022); antisemitism and the Holocaust are in sentence 2 now, and the 2021 “antisemitic” was itself in sentence 2 (a sentence-split artefact)"),
    "Genocide": ("DROP", "word-list artefact: the count is the article's own subject word; a general scholarly rewrite with no mention of Israel or Palestine in the opening"),
    "Settler colonialism": ("DROP", "word-list artefact: “indigenous” is a general term here, not the Jewish-indigeneity frame; critical terms fell 20 -> 11; no Israel or Palestine in the opening"),
    "Sheikh Jarrah controversy": ("DROP", "created 15 May 2021 (no 2021 version), wording settled since Sep 2021; both framings are attributed; a legal property dispute (court-centric)"),
    "Gaza genocide recognition": ("DROP", "created 21 Aug 2025 as a split, renamed twice; the opening is attributed (“has been accused … by several states”) and centred on the ICJ case (court-centric)"),
    "Samaritans": ("DROP", "no critical change; the first sentence gained “Israelite Samaritans”, a Jewish-history term, i.e. the other direction"),
    "East Jerusalem": ("DROP", "legal-status wording (“under illegal occupation … according to international law”), close to the court framing the owner excluded; the Jordan clause moved to paragraph 2"),
    "Bar Kokhba Revolt": ("DROP", "a move: “Judea” left the first sentence but is in sentence 2 (“depopulation of Judea proper”)"),
    "Ancient Israel and Judah": ("DROP", "rename artefact: the article was “History of ancient Israel and Judah” until 20 Jan 2026 and its first sentence now names the title (“Ancient Israel and Judah were two Israelite kingdoms …”); both kingdoms are named in sentence 4"),
    "Majdal Shams": ("DROP", "a village (the owner's scope rule: the long tail of places is not the story), though the change is real (“governed by Israel” -> “Under Israeli occupation since 1967”; “Quneitra Governorate, Syria”)"),
}
# key phrases dated from the first-sentence (fs) or opening-section (lead) history: (phrase, where, expected state now)
KEYS = {
    "Criticism of Israel": [("human rights violations", "fs", True), ("Nakba", "fs", True), ("Zionist political violence", "fs", True)],
    "Palestinian political violence": [("terror", "fs", False), ("insurgency", "fs", True)],
    "Plan Dalet": [("worked out by the Haganah", "fs", False), ("Zionist military plan", "fs", True), ("known as the Nakba", "lead", True)],
    "Causes of the 1948 Palestinian expulsion and flight": [("by Israeli forces", "fs", False), ("most scholars consider", "lead", True), ("great controversy", "lead", False)],
}
ws = lambda t: re.sub(r"\s+", " ", t or "").strip()


def runs(hist, texts, phrase, where):
    out, prev = [], None
    for r in hist:
        if r.get("hidden"):
            continue
        s = (r["fs"] if where == "fs" else texts[r["h"]]).lower()
        f = phrase.lower() in s
        if f != prev:
            out.append({"ts": r["ts"], "revid": r["revid"], "in": f})
            prev = f
    return out


def one(rec):
    if not rec:
        return None
    p = A.prose(A.split_lead(rec["section0"]))
    ss = A.sentences(p)
    crit, conn = AT.lead_counts_text(rec["section0"])
    return {"revid": rec["revid"], "ts": rec["ts"], "first_sentence": ss[0] if ss else "", "sentences": [ws(s) for s in ss[:6]],
            "opening": ws(p), "critical": crit, "connection": conn}


def main(dirs):
    out = {"note": "Elsewhere on Wikipedia, hand verification (VERIFIED.md). Section 0 of the revision live on 1 Jan 2021 "
                   "(or the first revision) and of the latest revision; texts are analyze.prose() of section 0, whitespace-normalised.",
           "runs": [os.path.basename(d.rstrip("/")) for d in dirs], "articles": {}}
    for d in dirs:
        vd = os.path.join(d, "verify")
        for f in sorted(os.listdir(vd)):
            if f.startswith("leads_") or not f.endswith(".json.gz"):
                continue
            rec = json.load(gzip.open(os.path.join(vd, f)))
            texts = json.load(gzip.open(os.path.join(vd, "leads_" + f)))
            t = rec["title"]
            hist = rec["history"]
            dec, why = DECISIONS[t]
            a = {"run": os.path.basename(d.rstrip("/")), "decision": dec, "reason": why,
                 "then": one(rec["then_2021"]) if rec["then_2021"] else None,
                 "created": None if rec["then_2021"] else one(rec["first_rev"]),
                 "now": one(rec["now"]), "moves": [{"ts": r["ts"], "from": r["move"][0], "to": r["move"][1]} for r in hist if "move" in r],
                 "revisions_since_2021": len(hist), "keys": {}}
            for phrase, where, now_in in KEYS.get(t, []):
                R = runs(hist, texts, phrase, where)
                assert R and R[-1]["in"] == now_in, f"{t}: {phrase} state now"
                a["keys"][phrase] = {"where": where, "changes": R}
            out["articles"][t] = a
    assert set(out["articles"]) == set(DECISIONS), sorted(set(DECISIONS) ^ set(out["articles"]))
    json.dump(out, open(os.path.join(HERE, "verified.json"), "w"), ensure_ascii=False, indent=1)
    print("wrote verified.json:", {k: v["decision"] for k, v in out["articles"].items()})


if __name__ == "__main__":
    main(sys.argv[1:])
