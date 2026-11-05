"""Automatable content KPIs for study 3, Part C (frozen with CODEBOOK.md, 2026-11-05).

Every function takes the two lead texts of one pair: lead0 (OLD, Jan 2021 or earliest)
and lead1 (NEW, Oct 2026). Nothing here looks at the title or the group.

Frozen KPIs computed here (see CODEBOOK.md for definitions):
  K04a colonial_fs (auto sub-indicator of PRIMARY K04): colonial wording enters the first sentence in narrator voice
  K06 presupposed_eval_np     PRIMARY   evaluative/legal category packed into a noun phrase is added
  K09 camp_label              SECONDARY partisan-alignment label for an actor is added
Support proxies (reported, never tested): zionist_actor_label, majority_anchor.
Style controls (measured in both groups, never tested as topic findings):
  len_ratio, fs_change, rest_change, protected_opening, fs_tense_flip,
  attribution_density_change, terror_fs_removed, alt_names_fs_change.
Length stratum: lead0 word count (cleaned text) -> tercile with cut points fixed on discovery.

Usage:  python auto_kpis.py IN.json OUT.json      (IN = a qual_*.json list of pairs)
"""
import json
import re
import sys
import difflib
import statistics as st

# ---------------------------------------------------------------- frozen constants
# Tercile cut points of lead0 word count (clean_lead + whitespace split), computed on the
# discovery analysis set (topic pairs with change > 0.05 plus all comparison pairs, n = 213).
# T1: words <= TERCILE_CUTS[0]; T2: TERCILE_CUTS[0] < words <= TERCILE_CUTS[1]; T3: above.
TERCILE_CUTS = (158, 340)

# ---------------------------------------------------------------- text handling
_TEMPLATE_LINE = re.compile(r"^\s*(\*|#|\||\{\{|\}\}|[\w-]+\s*=)")
_ABBREV = ["c.", "ca.", "e.g.", "i.e.", "U.S.", "U.N.", "U.K.", "St.", "Mt.", "Dr.", "Jr.", "Sr.",
           "No.", "vs.", "cf.", "approx.", "Gen.", "Lt.", "Col.", "Mr.", "Mrs.", "Ms.", "Prof.", "al."]


def clean_lead(t):
    """Normalise a stored lead: entities to spaces, drop template/list lines and short label
    lines without sentence punctuation (map legends, navbox residue)."""
    t = (t or "").replace("&nbsp;", " ").replace("\u00a0", " ")
    keep = []
    for line in t.split("\n"):
        s = line.strip()
        if not s:
            keep.append("")
            continue
        if _TEMPLATE_LINE.match(s):
            continue
        if not re.search(r"[.!?;:]", s) and len(s.split()) < 15:
            continue
        keep.append(s)
    out = "\n".join(keep)
    out = re.sub(r"\n{3,}", "\n\n", out).strip()
    return out


def is_parse_artefact(raw):
    """True if the stored lead is mostly template/list residue (e.g. Islam lead1 in discovery)."""
    raw = raw or ""
    lines = [l for l in raw.split("\n") if l.strip()]
    if not lines:
        return True
    tmpl = sum(bool(_TEMPLATE_LINE.match(l.strip())) for l in lines)
    words = len(clean_lead(raw).split())
    return (tmpl >= 10 and tmpl / len(lines) > 0.3) or words == 0


def words(t):
    return len(clean_lead(t).split())


def tercile(n_words):
    if n_words <= TERCILE_CUTS[0]:
        return "T1"
    if n_words <= TERCILE_CUTS[1]:
        return "T2"
    return "T3"


def sentences(t):
    t = re.sub(r"\s+", " ", clean_lead(t)).strip()
    if not t:
        return []
    for i, a in enumerate(_ABBREV):
        t = t.replace(a, a.replace(".", f"\u2063{i}\u2063"))
    t = re.sub(r"\b([A-Z])\.(?=\s?[A-Z]\.)", "\\1\u2064", t)   # initials like "A. B."
    parts = re.split(r"(?<=[.!?])[\"')\]]*\s+(?=[A-Z\"'(\u0590-\u06FF])", t)
    out = []
    for p in parts:
        for i, a in enumerate(_ABBREV):
            p = p.replace(a.replace(".", f"\u2063{i}\u2063"), a)
        out.append(p.replace("\u2064", ".").strip())
    return [s for s in out if s]


def first_sentence(t):
    s = sentences(t)
    return s[0] if s else ""


def sim(a, b):
    return difflib.SequenceMatcher(None, a.split(), b.split(), autojunk=False).ratio()


# ---------------------------------------------------------------- lexicons (frozen)
COLONIAL = re.compile(r"\bcoloni[sz]\w*|\bcolonies\b|\bcolonial\w*|\bcolonists?\b|\bsettler[- ]colonial\w*", re.I)
# attribution / report cues; if one occurs earlier in the same sentence the term counts as attributed
ATTR_CUE = re.compile(
    r"\b(according to|described|describes?|characteri[sz]e[sd]?|considered|considers?|regarded|"
    r"viewed|views?|called|termed|label+ed|critics?|opponents?|proponents?|supporters?|"
    r"scholars?|historians?|analysts?|argue[sd]?|arguing|claim(s|ed)?|alleg\w+|accus\w+|"
    r"some|many|several|seen as|refer(s|red)? to)\b", re.I)

PRESUP = [
    ("X-occupied", re.compile(r"\b[A-Z][\w]+-(?:occupied|annexed|controlled|blockaded)\b")),
    ("occupied+Name", re.compile(r"(?:\b(?:the|in|of|from|into|on|across|throughout)\s+)occupied\s+(?=[A-Z])\w+")),
    ("occupied+territory", re.compile(r"\boccupied\s+(?:territor\w+|lands?|areas?|zones?|regions?|homeland)\b", re.I)),
    ("illegal+N", re.compile(r"\b(?:illegal|unlawful)(?:ly)?\s+(?:[\w-]+\s+)?(?:settlements?|occupation|annexation|outposts?|"
                             r"wall|barrier|blockade|siege|detentions?|invasion|regime|colon\w+|expulsions?|transfer|annexed|occupied)\b", re.I)),
    ("blockaded/besieged", re.compile(r"\b(?:the|a|an|from|in|into|of)\s+(?:blockaded|besieged)\b", re.I)),
    ("forced+N", re.compile(r"\bforced\s+(?:evacuations?|displacements?|deportations?|expulsions?|transfers?|removals?|"
                            r"relocations?|assimilation|conversions?|islami[sz]ation|sinici[sz]ation|labou?r|starvation)\b", re.I)),
    # contested category used as an event/system name in passing ("the Gaza genocide", "Israeli apartheid");
    # uncontested historical names (the Holocaust) and "<Place> massacre" event names are not counted
    ("named-atrocity NP", re.compile(r"\b(?:the\s+)?(?!(?:The|This|That|These|A|An|Its|Their|Such)\b)[A-Z][\w'’-]+\s+(?:genocide|ethnic cleansing|apartheid)\b")),
]
_QUOTED = re.compile(r"\"[^\"]{0,300}\"|“[^”]{0,300}”")

CAMP = re.compile(
    r"\b[Pp]ro-(?:[A-Z][\w-]*|government|independence|regime|democracy)\b"
    r"|\b[Aa]nti-(?:[A-Z][\w-]*|government)\s+(?:groups?|activists?|organi[sz]ations?|lobby|lobbies|forces|militias?|"
    r"campaigners?|movements?|advocacy|advocates?|bias|commentators?|media|parties|party|factions?)\b"
    r"|\b(?:and|or)\s+(?:its|their|his|her)\s+(?:supporters|allies|backers|defenders)\b"
    r"|\b[Ss]upporters\s+of\s+(?:the\s+)?[A-Z][\w-]+")

ZIONIST_ACTOR = re.compile(r"\bZionists\b|\bZionist\s+(?:militias?|militants?|paramilitar\w+|forces|settlers?|leaders?|"
                           r"groups?|fighters|troops|underground|authorities|leadership|immigrants|colonists)\b")
MAJORITY = re.compile(r"\b(?:overwhelming|large|vast|clear|small|tiny)?\s*(?:Arab|Muslim|Jewish|Christian|Druze|Palestinian|"
                      r"[A-Z][a-z]+)\s+(?:majority|minority)\b|\bpredominantly\s+(?:[A-Z][a-z]+\s*)+(?:population|people|inhabitants)?"
                      r"|\b\d{1,2}(?:\.\d)?\s?%\s+(?:\w+\s+){0,2}(?:Arab|Muslim|Jewish|Christian|Jews|Arabs|Muslims|Christians)\b")
ATTR_DENSITY = re.compile(
    r"\b(according to|described (as|by)|accused|alleg\w+|critics?|some (scholars|historians|academics)|"
    r"has been (called|termed|characteri[sz]ed|described)|considers?|regarded as|viewed as|claim(s|ed)?)\b", re.I)
TERROR = re.compile(r"\bterror\w*", re.I)
ALT_NAME = re.compile(r"\b(also (known|called|referred to) as|or the|officially( known as)?|abbreviated|known (to|in) \w+ as)\b", re.I)


# ---------------------------------------------------------------- KPI functions
_NAMING = re.compile(r"\b(also|or)\s+(called|known as|referred to as|termed)\b", re.I)


def colonial_narrator_fs(text):
    """1 if the first sentence contains colonial wording with no attribution cue before it in
    the same sentence (narrator voice); naming formulas ('also called') are not cues.
    Also returns the matched token or ''."""
    fs = first_sentence(text)
    fs_noq = _NAMING.sub(" ", _QUOTED.sub(" ", fs))
    for m in COLONIAL.finditer(fs_noq):
        if not ATTR_CUE.search(fs_noq[: m.start()]):
            return 1, m.group(0)
    return 0, ""


def k04a_colonial_fs(lead0, lead1):
    o, ot = colonial_narrator_fs(lead0)
    n, nt = colonial_narrator_fs(lead1)
    return {"K04a_old": o, "K04a_new": n, "K04a_gain": int(n == 1 and o == 0), "K04a_loss": int(o == 1 and n == 0),
            "K04a_new_token": nt}


def presupposed_hits(text):
    """List of (pattern, span) evaluative NPs outside quotations; named-atrocity NPs that already
    occur in the version's own first sentence (the article's own subject) are excluded."""
    t = re.sub(r"\s+", " ", clean_lead(text))
    tq = _QUOTED.sub(lambda m: " " * len(m.group(0)), t)
    fs = first_sentence(text)
    own = {m.group(0).lower().replace("the ", "", 1).strip() for _, p in PRESUP[-1:] for m in p.finditer(fs)}
    hits = []
    for name, p in PRESUP:
        for m in p.finditer(tq):
            span = m.group(0)
            if name == "named-atrocity NP":
                key = span.lower().replace("the ", "", 1).strip()
                if key in own:
                    continue
            hits.append((name, span.strip()))
    return hits


def k06_presupposed_eval_np(lead0, lead1):
    h0, h1 = presupposed_hits(lead0), presupposed_hits(lead1)
    w0, w1 = max(words(lead0), 1), max(words(lead1), 1)
    r0, r1 = 100 * len(h0) / w0, 100 * len(h1) / w1
    return {"K06_old_n": len(h0), "K06_new_n": len(h1), "K06_old_per100w": round(r0, 3), "K06_new_per100w": round(r1, 3),
            "K06_gain": int(len(h1) > len(h0) and r1 > r0), "K06_loss": int(len(h1) < len(h0) and r1 < r0),
            "K06_new_spans": sorted({s for _, s in h1} - {s for _, s in h0})[:8]}


def camp_hits(text):
    t = _QUOTED.sub(" ", re.sub(r"\s+", " ", clean_lead(text)))
    return [m.group(0) for m in CAMP.finditer(t)]


def k09_camp_label(lead0, lead1):
    c0, c1 = camp_hits(lead0), camp_hits(lead1)
    return {"K09_old_n": len(c0), "K09_new_n": len(c1), "K09_gain": int(len(c1) > len(c0)),
            "K09_loss": int(len(c1) < len(c0)), "K09_new_spans": sorted(set(c1) - set(c0))[:8]}


def support_proxies(lead0, lead1):
    z0 = len(ZIONIST_ACTOR.findall(clean_lead(lead0)))
    z1 = len(ZIONIST_ACTOR.findall(clean_lead(lead1)))
    m0 = len(MAJORITY.findall(clean_lead(lead0)))
    m1 = len(MAJORITY.findall(clean_lead(lead1)))
    return {"SUP_zionist_actor_old": z0, "SUP_zionist_actor_new": z1, "SUP_zionist_actor_gain": int(z1 > z0),
            "SUP_majority_old": m0, "SUP_majority_new": m1, "SUP_majority_gain": int(m1 > m0)}


def style_controls(lead0, lead1):
    S0, S1 = sentences(lead0), sentences(lead1)
    f0, f1 = (S0[0] if S0 else ""), (S1[0] if S1 else "")
    fs_chg = 1 - sim(f0, f1)
    rest_chg = (1 - sim(" ".join(S0[1:]), " ".join(S1[1:]))) if len(S0) > 1 and len(S1) > 1 else None
    n0, n1 = max(len(S0), 1), max(len(S1), 1)
    was0 = bool(re.search(r"\b(was|were)\b", f0[:200]))
    was1 = bool(re.search(r"\b(was|were)\b", f1[:200]))
    a0 = len(ATTR_DENSITY.findall(" ".join(S0))) / n0
    a1 = len(ATTR_DENSITY.findall(" ".join(S1))) / n1
    return {
        "SC_len_ratio": round((words(lead1) + 1) / (words(lead0) + 1), 3),
        "SC_fs_change": round(fs_chg, 3),
        "SC_rest_change": None if rest_chg is None else round(rest_chg, 3),
        "SC_protected_opening": None if rest_chg is None else int(fs_chg < rest_chg - 0.2),
        "SC_fs_tense_flip": int(was0 != was1),
        "SC_attr_density_up": int(a1 > a0), "SC_attr_density_down": int(a1 < a0),
        "SC_terror_fs_removed": int(bool(TERROR.search(f0)) and not TERROR.search(f1)),
        "SC_terror_fs_added": int(bool(TERROR.search(f1)) and not TERROR.search(f0)),
        "SC_alt_names_fs_up": int(len(ALT_NAME.findall(f1)) > len(ALT_NAME.findall(f0))),
        "SC_alt_names_fs_down": int(len(ALT_NAME.findall(f1)) < len(ALT_NAME.findall(f0))),
    }


def all_kpis(lead0, lead1):
    w0 = words(lead0)
    out = {"lead0_words": w0, "lead1_words": words(lead1), "tercile": tercile(w0),
           "parse_artefact": int(is_parse_artefact(lead0) or is_parse_artefact(lead1))}
    for f in (k04a_colonial_fs, k06_presupposed_eval_np, k09_camp_label, support_proxies, style_controls):
        out.update(f(lead0, lead1))
    return out


# ---------------------------------------------------------------- runner
def group_of(g):
    return "topic" if g == "treatment" else "comparison"


def in_analysis_set(x):
    """Coding/analysis set: topic pairs with change > 0.05, all comparison pairs."""
    return x["group"] != "treatment" or (x.get("change") or 0) > 0.05


def summarise(rows):
    keys = ["K04a_gain", "K04a_loss", "K06_gain", "K06_loss", "K09_gain", "K09_loss", "SUP_zionist_actor_gain",
            "SUP_majority_gain", "SC_protected_opening", "SC_fs_tense_flip", "SC_attr_density_up", "SC_attr_density_down",
            "SC_terror_fs_removed", "SC_terror_fs_added", "SC_alt_names_fs_up", "SC_alt_names_fs_down"]
    R = [r for r in rows if r["in_analysis_set"] and not r["parse_artefact"]]
    summ = {"n": {g: sum(r["grp"] == g for r in R) for g in ("topic", "comparison")}}
    for k in keys:
        row = {}
        for g in ("topic", "comparison"):
            v = [r[k] for r in R if r["grp"] == g and r[k] is not None]
            row[g] = round(sum(v) / len(v), 3) if v else None
            for t in ("T1", "T2", "T3"):
                vt = [r[k] for r in R if r["grp"] == g and r["tercile"] == t and r[k] is not None]
                row[f"{g}_{t}"] = f"{sum(vt)}/{len(vt)}"
        row["diff"] = None if None in (row["topic"], row["comparison"]) else round(row["topic"] - row["comparison"], 3)
        summ[k] = row
    summ["median_len_ratio"] = {g: st.median([r["SC_len_ratio"] for r in R if r["grp"] == g]) for g in ("topic", "comparison")}
    return summ


def main(path_in, path_out):
    data = json.load(open(path_in))
    rows = []
    for x in data:
        r = {"title": x["title"], "group": x["group"], "grp": group_of(x["group"]), "change": x.get("change"),
             "in_analysis_set": int(in_analysis_set(x))}
        r.update(all_kpis(x.get("lead0") or "", x.get("lead1") or ""))
        rows.append(r)
    out = {"source": path_in, "tercile_cuts": TERCILE_CUTS, "pairs": rows, "summary": summarise(rows)}
    json.dump(out, open(path_out, "w"), ensure_ascii=False, indent=1)
    return out


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    res = main(sys.argv[1], sys.argv[2])
    print(json.dumps(res["summary"], indent=1))
