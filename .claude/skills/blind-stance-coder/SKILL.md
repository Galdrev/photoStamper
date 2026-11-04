---
name: blind-stance-coder
description: Blind-code pairs of masked encyclopedia lead sections (version A vs B) for change in how favourably the subject is framed. Use only when given a wikitrends blind batch file.
---

# Blind stance coder (rubric v1)

You compare two versions, **A** and **B**, of the opening section of an encyclopedia article.
Names of countries, peoples, religions, places and organisations are masked as `[ENTITY-n]`.
You do not know which version is older, which article it is, or why it is being coded. Do not guess any of these.

## For each item, answer two questions

**1. label: does B frame the article's main subject (usually [ENTITY-1]) more or less favourably than A?**
- `B_less_favourable`: B adds or strengthens negative characterisations of the subject, or removes or weakens positive or neutral ones. Examples:
  - wrongdoing stated as fact rather than as an allegation;
  - loaded terms added (e.g. "colonial", "apartheid", "genocide", "terrorist", "extremist");
  - legitimising context removed;
  - critics' views moved into the first sentence or definition.
- `B_more_favourable`: the reverse.
- `no_stance_change`: B differs only in facts, dates, wording or structure, with no net shift in evaluation.
- `unclear`: the changes point both ways about equally, or the masking makes it impossible to tell. Use it whenever you are not confident. It is a legitimate answer.

**2. kind: what kind of change is it?**
- `framing`: the same facts are characterised differently (word choice, attribution, emphasis, ordering).
- `factual_update`: new events or facts are added or removed.
- `both`
- `none`

## Rules
- **Quote first.** Before labelling, copy the shortest exact phrase (at most 30 words) from A or B that most justifies your label. Prefix it with `A:` or `B:`. If you cannot quote a phrase that supports a directional label, the label must be `no_stance_change` or `unclear`.
- **Judge only the text.** Use no outside knowledge of real conflicts, and no view on which characterisation is true. A favourable shift can be accurate, and so can an unfavourable one. You are measuring framing, not truth.
- **Hedging matters.** Changes in attribution and hedging ("critics describe X as …" → "X is …") count as stance changes.
- **Length is not a signal.** A longer version is not more or less favourable because it is longer.

## Illustrative examples (invented, not from the data)
1. **A:** "[ENTITY-1] is a movement that seeks independence for [ENTITY-2]." **B:** "[ENTITY-1] is a movement that seeks independence for [ENTITY-2], described by critics as separatist." → `B_less_favourable`, `framing`, quote: "B: described by critics as separatist"
2. **A:** "…has been accused of ethnic cleansing." **B:** "…carried out ethnic cleansing." → `B_less_favourable`, `framing`
3. **A:** "…an armed group." **B:** "…a resistance movement that defends [ENTITY-2]." → `B_more_favourable`, `framing`
4. **A:** "…population of 9 million (2020)." **B:** "…population of 9.8 million (2024)." → `no_stance_change`, `factual_update`
5. **A:** "…signed a peace treaty in 1994." **B:** "…signed a peace treaty in 1994; in 2024 it was accused of war crimes by a UN commission." → `B_less_favourable`, `factual_update` (a new event that is negative for the subject)
6. **A:** "…is a religion." **B:** "…is an Abrahamic religion with roots in the ancient Near East." → `no_stance_change`, `framing`
7. **A:** "…was founded as a homeland for [ENTITY-2]." **B:** "…was founded through the displacement of [ENTITY-3]; supporters describe it as a homeland for [ENTITY-2]." → `B_less_favourable`, `framing`
8. Mixed changes of equal weight in both directions → `unclear`

## Output
Write a JSON array, one object per item, in input order. Each object has these fields:
`{"id": "...", "quote": "...", "label": "...", "kind": "..."}`
Return valid JSON only, with no commentary. Label every item. Use `unclear` rather than skipping one.
