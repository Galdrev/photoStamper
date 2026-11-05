"""Event-update filter (SPEC_STUDY3 amendment D, frozen before any filtered result was computed).

Goal: separate *narrative* change from *factual updates about recent events*. When a war breaks out, the Israel article is
expected to gain sentences about it; that is news coverage, not a re-telling of history. We drop sentences that are about
recent events and measure framing only in what remains (the "narrative residual").

The rule is symmetric (the same for topic and comparison articles) and outcome-blind:
  an EVENT sentence is one that
    (a) names a year from 2022 on, or
    (b) mentions a recent event from a fixed list covering BOTH the topic and the comparison disputes, or
    (c) uses generic recency wording ("the ongoing war", "as of", "since the start of the war").
Two variants:
  sentence-level (primary): drop only event sentences;
  paragraph-level (sensitivity): drop every paragraph that contains an event sentence.
"""
import re

YEAR = re.compile(r"\b20(?:2[2-9])\b")
RECENT = re.compile("|".join([
    # Israel / Palestine 2023-
    r"\bOctober 7\b", r"\b7 October\b", r"\bOct(?:ober)?\.? 7(?:th)?\b", r"Hamas-led (?:attack|incursion|assault)",
    r"Israel[–-]Hamas war", r"\bGaza war\b", r"\bwar in Gaza\b", r"Swords of Iron", r"\bhostages?\b",
    r"South Africa v\.? Israel", r"Iran[–-]Israel war", r"Twelve-Day War", r"Gaza genocide", r"Gaza (?:Strip )?famine",
    r"\bIsrael[–-]Hezbollah (?:war|conflict) \(20", r"Israeli invasion of (?:southern )?Lebanon \(20",
    # comparison disputes and other comparison conflicts, same era
    r"Russian invasion of Ukraine", r"full-scale invasion", r"\bSudanese civil war\b", r"\bwar in Sudan\b",
    r"Azerbaijani offensive", r"flight of Nagorno-Karabakh Armenians", r"dissolution of (?:the )?(?:Republic of )?Artsakh",
    r"Tigray war", r"Myanmar civil war", r"\bWagner (?:Group )?(?:rebellion|mutiny)\b",
]), re.I)
RECENCY = re.compile(r"\b(?:the ongoing (?:war|conflict|invasion)|as of\b|since the (?:start|outbreak) of the (?:war|conflict|invasion)|"
                     r"(?:in|since) (?:the )?(?:current|ongoing) war)", re.I)

ABBR = re.compile(r"\b(?:c|ca|U\.S|U\.K|St|Mr|Dr|e\.g|i\.e|vs|v|BCE|CE|BC|AD|Oct|No)\.$")


def sentences(p):
    p = re.sub(r"\s+", " ", p).strip()
    parts, buf = [], ""
    for chunk in re.split(r"(?<=[.!?])\s+", p):
        buf = f"{buf} {chunk}".strip() if buf else chunk
        if not ABBR.search(buf):
            parts.append(buf); buf = ""
    if buf:
        parts.append(buf)
    return [s for s in parts if s]


def is_event(s):
    return bool(YEAR.search(s) or RECENT.search(s) or RECENCY.search(s))


def split(prose_text, level="sentence"):
    """-> (residual_text, event_text, stats). prose_text: output of analyze.prose(); paragraphs separated by blank lines."""
    paras = [p for p in re.split(r"\n\s*\n", prose_text) if p.strip()]
    keep, drop, n_s, n_ev = [], [], 0, 0
    for p in paras:
        ss = sentences(p)
        flags = [is_event(s) for s in ss]
        n_s += len(ss); n_ev += sum(flags)
        if level == "paragraph":
            (drop if any(flags) else keep).append(" ".join(ss))
        else:
            keep.append(" ".join(s for s, f in zip(ss, flags) if not f))
            drop.append(" ".join(s for s, f in zip(ss, flags) if f))
    return ("\n\n".join(x for x in keep if x), "\n\n".join(x for x in drop if x),
            {"sentences": n_s, "event_sentences": n_ev, "event_share": n_ev / n_s if n_s else None})


def residual_measures(prose_text, measure, min_words=0):
    """Critical-frame measures on the residual and on the event part, both variants. `measure` = analyze.measure."""
    out = {}
    for level in ("sentence", "paragraph"):
        res, ev, st = split(prose_text, level)
        safe = lambda t, mw: measure(t, max(1, mw)) if t and t.strip() else None   # empty part -> None, never divide by 0
        out[level] = {"residual": safe(res, min_words), "event": safe(ev, 1), **st}
    return out
