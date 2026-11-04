---
name: blind-stance-coder
description: Blind-code pairs of masked encyclopedia opening sections (version A vs B) for change in how favourably the main subject is framed. Use only when given a wikitrends blind shard file.
---

# Blind stance coder (rubric v2)

You compare two versions, **A** and **B**, of the opening section of an encyclopedia article.
Names of countries, peoples, religions, places and organisations are masked as `[ENTITY-n]`.
You do not know which version is older, which article it is, or why it is being coded. Do not try to work out any of these.
Judge each item **on its own**. Do not compare it with other items in the file.

## Question: does B present the main subject (usually [ENTITY-1], or the article's subject) more or less favourably than A?

- `B_less_favourable`: B makes the subject look worse. Examples:
  - adds or strengthens negative descriptions;
  - states as fact something A attributed or hedged;
  - removes positive or neutral context;
  - moves criticism into the first sentence or the definition.
- `B_more_favourable`: B makes the subject look better. Examples:
  - adds positive descriptions or legitimising context;
  - attributes or hedges something A stated as fact;
  - removes or softens criticism.
- `no_stance_change`: the differences are wording, structure, dates or neutral facts, with no net change in evaluation.
- `unclear`: the changes point both ways about equally, or you cannot tell. Use this whenever you are not confident.

Also give:
- `kind`: one of `framing` (same facts, different characterisation), `factual_update` (events or facts added or removed), `both` or `none`.
- `confidence`: one of `low`, `med` or `high`.

## Rules
1. **Quote first.** Copy the shortest exact phrase (at most 30 words) from A or B that most justifies your label, prefixed `A:` or `B:`. It must appear verbatim in that version; it is checked by code. If no quote supports a directional label, use `no_stance_change` or `unclear`.
2. **Judge only the text.** Use no outside knowledge, and form no view on which version is true. You are measuring presentation, not accuracy.
3. **Attribution counts.** "Critics describe X as …" vs "X is …" is a stance change, in either direction.
4. **Length is not a signal.**
5. **Identical versions** are `no_stance_change`, `none`.

## Calibration examples (deliberately on unrelated subjects, mirrored in both directions)
| A | B | label | kind |
|---|---|---|---|
| "[ENTITY-1] is a football club founded in 1902." | "[ENTITY-1] is a football club founded in 1902, notorious for match-fixing scandals." | `B_less_favourable` | `framing` |
| "[ENTITY-1] is a football club founded in 1902, notorious for match-fixing scandals." | "[ENTITY-1] is a football club founded in 1902." | `B_more_favourable` | `framing` |
| "The company has been accused of exploiting workers." | "The company exploited workers." | `B_less_favourable` | `framing` (hedge removed) |
| "The company exploited workers." | "The company has been accused of exploiting workers." | `B_more_favourable` | `framing` (hedge added) |
| "…a chemical firm." | "…a chemical firm; in 2019 a court fined it for pollution." | `B_less_favourable` | `factual_update` |
| "…a chemical firm." | "…a chemical firm; in 2019 it won an award for clean production." | `B_more_favourable` | `factual_update` |
| "…has 9 million members (2020)." | "…has 9.8 million members (2024)." | `no_stance_change` | `factual_update` |
| "…is a religious order." | "…is a Catholic religious order founded in Spain." | `no_stance_change` | `framing` |
| Changes of equal weight in both directions | | `unclear` | `both` |

## Output
Return a JSON array, one object per item, in input order:
`{"id": "...", "quote": "...", "label": "...", "kind": "...", "confidence": "..."}`
Return valid JSON only. Label every item.
