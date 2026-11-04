---
name: narrative-coder
description: Code the narrative content and tone of a change between two masked versions of an encyclopedia opening section (themes, agency, certainty, whose history and suffering is foregrounded). Use only when given a wikitrends narrative batch file.
---

# Narrative coder (codebook v1)

You read two versions, **A** and **B**, of an encyclopedia article's opening section. Names are masked as `[ENTITY-n]`. You do not know which version is older or what the article is. Describe what changed in the *story the text tells*. Do not judge which version is true.

## For each item, return

**`themes`**: a list of the themes that changed between A and B, with a direction for each. Use only these codes:

| code | what it captures | direction values |
|---|---|---|
| `attribution` | claims moved between "X is accused of / critics say" and plain statement | `B_states_as_fact` / `B_attributes` |
| `agency` | who is the grammatical actor of harm; passive vs active voice | `B_names_actor` / `B_obscures_actor` (also note which entity) |
| `origins` | which historical origin is foregrounded | `B_ancient_roots` / `B_colonial_origins` / `B_persecution_refuge` / `B_displacement_of_others` / `B_other` |
| `suffering` | whose victimhood is mentioned or expanded | `B_more_ENTITY-n` / `B_less_ENTITY-n` |
| `legitimacy` | legal or illegitimacy language (illegal, occupation, recognised, sovereign) | `B_more_legitimising` / `B_more_delegitimising` |
| `labels` | category label of the subject or an actor (militant/terrorist, war/genocide, movement/ideology) | `B_harsher` / `B_softer` |
| `authority` | appeals to authorities (scholars, UN, courts, human-rights groups, governments) | `B_more_authority` / `B_less_authority` |
| `scope` | factual events added or removed with no reframing | `B_adds_events` / `B_removes_events` |

**`tone_A`, `tone_B`**: one of:
- `encyclopedic`: neutral, attributive, balanced;
- `leaning`: selective emphasis, but restrained wording;
- `advocacy`: evaluative wording, one side's terms presented as fact.

**`summary`**: one plain sentence, written for a general reader, saying how the story told by B differs from A. Example: "B presents the movement mainly through its effect on the existing population, where A presented it mainly through its founders' aims." Do not use outside knowledge, and do not guess identities.

**`quote`**: the shortest exact phrase (at most 30 words) that best shows the main change. Prefix it with `A:` or `B:`.

## Rules
- Code only what is in the text.
- If nothing narrative changed, return `themes: []`.
- Length alone is not a theme.
- Output a JSON array with one object per item, in input order: `{"id","themes":[{"code","direction"}],"tone_A","tone_B","summary","quote"}`. Return valid JSON only.
