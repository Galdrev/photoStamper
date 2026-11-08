# Zionism first sentence: what each edit did (change codes)

Data: `data/ratchet.json`, `articles["Zionism"]`, `fs_variants` and `fs_timeline`. The page counts 292 changes: change k goes from wording `tl[k-1][1]` to wording `tl[k][1]`. These 292 changes are 238 distinct (from, to) transitions. Each transition was coded once and the codes were then mapped onto every change. Machine-readable output: `change_codes.json`. The October 7 stepper tabs (October 7 attacks, Hamas, Gaza genocide) use the same `fs_*` structure, so they were coded in the same run. Their results are under `other_articles` in the JSON and summarised briefly at the end of this file.

## Method

- **Unit.** One distinct (from wording, to wording) transition. 205 of the 238 Zionism transitions have stored text on both sides. The other 33 (37 changes) are **uncodable**: in 31 the wording on one or both sides was never stored, and in 2 one side is a blank first sentence (the sentence was emptied).
- **Masking.** Each coder got only the pairs: the two texts as A and B, in a random order drawn separately for each coder, plus a flag saying which came first. Coders saw no wording ids, dates, counts, revert flags or editor information. The items from all four articles were shuffled together into batches of 40.
- **Two blind coders.** Each pass ran as its own headless Claude process (`claude -p`) with every tool switched off, so it could not read the repository or the other pass. Both got the identical codebook (in `change_codes.json` → `axes`). A coder sometimes dropped items from a batch; those items went back to the same coder in small batches until every item had a code.
- **Agreement.** Cohen's κ per axis, computed on the raw codes before any adjudication.
- **Adjudication.** A third pass (the agent running this task, which read the before and after texts and the wording ids but no dates or counts) resolved only the axes where the two coders disagreed. Agreed axes stand as coded. Every adjudicated transition carries both coders' codes and a note (`coders`, `adjudication_note`).
- **Mirror check.** Where both A→B and B→A were coded, their directions should be opposites. Four adjudicated codes were changed to mirror a code both coders had agreed on. Three mismatches between two *agreed* codes were left as coded and are listed in `method.mirror_check`.
- **Rules for removals.** Voice describes the after text. If a claim is removed and nothing replaces it, voice is `na`.
- **Time measures.** Timeline dates are whole days. `days_live` is the number of days from a change to the next change (0 for same-day edits). The last change runs to the end of the data, 2026-11-04, derived from the final wording's `live_days`. `regime_days` is given only for non-neutral and uncodable changes. It counts days until the next change that is not neutral: how long the stance set by that edit lasted, through any wording-only edits in between.

## Inter-coder agreement (before adjudication)

| axis | Zionism n=205: agreement | Zionism κ | all four articles n=627: agreement | all four κ |
|---|---|---|---|---|
| direction | 94.1% | **0.914** | 93.9% | 0.907 |
| voice | 90.7% | **0.818** | 90.8% | 0.844 |
| claim_type | 93.2% | **0.866** | 92.7% | 0.876 |

26 of the 205 coded Zionism transitions had at least one disagreement and were adjudicated. In 3 of the 94 adjudicated pairs (across all four articles), one coder read the order backwards (see the notes).

## Summary: Zionism, all 292 changes

| | changes | share of changes | days live | share of days | stance-regime days | share |
|---|---|---|---|---|---|---|
| more_critical | 88 | 30.1% | 386 | 18.6% | 700 | 33.8% |
| less_critical | 77 | 26.4% | 96 | 4.6% | 885 | 42.7% |
| neutral | 83 | 28.4% | 1,444 | 69.7% | — | — |
| mixed | 7 | 2.4% | 30 | 1.5% | 33 | 1.6% |
| uncodable | 37 | 12.7% | 117 | 5.6% | 455 | 21.9% |
| **voice:** own_voice | 158 | 54.1% | 420 | 20.3% | | |
| attributed | 5 | 1.7% | 181 | 8.7% | | |
| na | 92 | 31.5% | 1,355 | 65.4% | | |
| **claim:** contested_characterisation | 170 | 58.2% | 511 | 24.6% | | |
| verifiable_fact | 5 | 1.7% | 120 | 5.8% | | |
| na | 80 | 27.4% | 1,325 | 63.9% | | |

Total days: 2,073. Reverts: 108 changes are flagged as reverts. Of these, 51 are less_critical, 31 more_critical, 11 neutral, 4 mixed and 11 uncodable. So most less_critical changes (51 of 77) undo an edit, while most more_critical changes (57 of 88) are not reverts.

How to read the time columns: the long stable stretches were mostly reached through wording-only edits, so "days live" is dominated by neutral changes. "Stance-regime days" credits each stretch to the last edit that changed the stance. The 753-day stretch from 12 June 2021 is credited to one less_critical edit: the Hebrew name "Eretz Israel" was added.

## Key cross-tab: direction × voice × claim_type (Zionism)

| cell | transitions | changes | share of 255 coded changes | days live | regime days |
|---|---|---|---|---|---|
| **more_critical · own_voice · contested_characterisation (headline)** | **54** | **78** | **30.6%** (26.7% of all 292) | **336** (16.2%) | **650** |
| less_critical · own_voice · contested_characterisation (mirror) | 47 | 70 | 27.5% | 38 (1.8%) | 74 |
| neutral · na · na | — | 79 | 31.0% | 1,146 | — |
| more_critical · na · contested (removals) | — | 7 | 2.7% | 50 | 50 |
| less_critical · na · contested (removals) | — | 4 | 1.6% | 55 | 56 |
| mixed · own_voice · contested | — | 7 | 2.7% | 30 | 33 |
| more_critical · attributed · contested | — | 3 | 1.2% | 0 | 0 |
| less_critical · attributed · contested | — | 1 | 0.4% | 2 | 2 |
| less_critical · own_voice · verifiable_fact | — | 2 | 0.8% | 1 | 753 |
| other neutral cells | — | 4 | 1.6% | 298 | — |

Reading: in the Zionism first sentence, the edits that changed stance almost always did it with a contested characterisation stated in the encyclopedia's own voice, never with attribution. 3 more_critical changes were attributed, against 78 in own voice. The more critical and less critical edits are close in number (78 against 70), but the text produced by the more critical edits stayed up much longer: 336 days against 38. Of the 70 less critical changes in own voice, 48 are reverts and 64 were themselves undone within a day. For the 78 more critical changes the figures are 27 and 47.

## The 10 most consequential transitions

Ranked by `regime_days`, the number of days the stance set by the edit lasted before the next non-neutral change. The texts are the stored first sentences, exactly as held. Some stored texts are cut off.

### 1. Hebrew name "Eretz Israel" in as name for the region

- Change k=21, 2021-06-12, wording 16 → 17; the stance it set lasted **753 days** (to the next non-neutral change)
- Codes: **less_critical**, own_voice, verifiable_fact
- Before: “Zionism ( Tsiyyonut after Zion) is both an ideology and nationalist movement that espouses the establishment of, and support for a Jewish state centered in the area roughly corresponding to Canaan, the Holy Land, or the region of Palestine on the basis of a long Jewish connection and attachment to that land.”
- After: “Zionism ( Tsiyyonut after Zion) is both an ideology and nationalist movement that espouses the establishment of, and support for a Jewish state centered in the area roughly corresponding to Canaan, the Holy Land, or the region of Palestine or Eretz Israel on the basis of a long Jewish connection and attachment to that land.”

### 2. "in historic Palestine" out, "pursued through the colonization of Palestine" in

- Change k=212, 2025-04-06, wording 120 → 119; the stance it set lasted **75 days** (to the next non-neutral change)
- Codes: **more_critical**, own_voice, contested_characterisation
- Before: “Zionism is an ethnocultural nationalist movement that emerged in Europe in the late 19th century that aimed to establish and support a national home for the Jewish people in historic Palestine, a region roughly corresponding to the Land of Israel in Judaism, with central importance in Jewish history.”
- After: “Zionism is an ethnocultural nationalist movement that emerged in Europe in the late 19th century that aimed to establish a national home for the Jewish people, pursued through the colonization of Palestine, a region roughly corresponding to the Land of Israel in Judaism, with central importance in Jewish history.”

### 3. "through the colonization of Palestine" in, stated as fact

- Change k=229, 2025-07-22, wording 131 → 130; the stance it set lasted **74 days** (to the next non-neutral change)
- Codes: **more_critical**, own_voice, contested_characterisation
- Before: “Zionism is an ethnocultural nationalist movement that emerged in late 19th-century Europe to establish and support a Jewish homeland in the Land of Israel in Judaism and central to Jewish history.”
- After: “Zionism is an ethnocultural nationalist movement that emerged in late 19th-century Europe to establish and support a Jewish homeland through the colonization of Palestine, a region corresponding to the Land of Israel in Judaism and central to Jewish history.”

### 4. "through colonization" in, stated as fact

- Change k=292, 2026-08-27, wording 168 → 167; the stance it set has lasted **69 days** so far (it is the current wording, to the end of the data)
- Codes: **more_critical**, own_voice, contested_characterisation
- Before: “Zionism is an ethnic nationalist movement that emerged in late 19th-century Europe to establish and support a Jewish homeland in the region of Palestine, which roughly corresponds to the Land of Israel in Judaism—itself central to Jewish history.”
- After: “Zionism is an ethnic nationalist movement that emerged in late 19th-century Europe to establish and support a Jewish homeland through colonization in the region of Palestine, which roughly corresponds to the Land of Israel in Judaism—itself central to Jewish history.”

### 5. 'aliyah' out, leaving colonization as sole stated means

- Change k=208, 2025-02-01, wording 117 → 116; the stance it set lasted **64 days** (to the next non-neutral change)
- Codes: **more_critical**, own_voice, contested_characterisation
- Before: “Zionism is an ethnocultural nationalist movement that emerged in Europe in the late 19th century aimed to establish a national home for the Jewish people, pursued through aliyah and the colonization of Palestine, a region roughly corresponding to the Land of Israel in Judaism, with central importance in Jewish history.”
- After: “Zionism is an ethnocultural nationalist movement that emerged in Europe in the late 19th century aimed to establish a national home for the Jewish people, pursued through the colonization of Palestine, a region roughly corresponding to the Land of Israel in Judaism, with central importance in Jewish history.”

### 6. "settlement" out, "colonization" in; "cultural" to "ethnocultural", stated as fact

- Change k=238, 2025-11-25, wording 138 → 137; the stance it set lasted **64 days** (to the next non-neutral change)
- Codes: **more_critical**, own_voice, contested_characterisation
- Before: “Zionism is an cultural nationalist movement that emerged in late 19th-century Europe; it primarily seeks to establish and support a Jewish homeland through the settlement of the Palestine region, which corresponds to the Land of Israel in Judaism and is central to Jewish history.”
- After: “Zionism is an ethnocultural nationalist movement that emerged in late 19th-century Europe; it primarily seeks to establish and support a Jewish homeland through the colonization of the Palestine region, which corresponds to the Land of Israel in Judaism and is central to Jewish history.”

### 7. Clause about much larger Land of Israel borders out

- Change k=3, 2021-04-02, wording 2 → 3; the stance it set lasted **52 days** (to the next non-neutral change)
- Codes: **less_critical**, na, contested_characterisation. Adjudicated: Removes the 'much larger area' borders clause; the insertion of the same clause (variant 1 to 2) was coded more_critical by both coders, so this removal is coded as its mirror
- Before: “Zionism ( Tsiyyonut after Zion) is both an ideology and nationalist movement among the Jewish people that espouses the re-establishment of and support for a Jewish state centered in the area roughly corresponding to Canaan, the Holy Land, or the region of Palestine, but whose borders as the Land of Israel would encompass a much larger area.”
- After: “Zionism ( Tsiyyonut after Zion) is both an ideology and nationalist movement among the Jewish people that espouses the re-establishment of and support for a Jewish state centered in the area roughly corresponding to Canaan, the Holy Land, or the region of Palestine.”

### 8. Land of Israel and Jewish history framing out

- Change k=232, 2025-10-04, wording 130 → 133; the stance it set lasted **47 days** (to the next non-neutral change)
- Codes: **more_critical**, na, contested_characterisation. Adjudicated: Jewish-history framing removed; removal so voice na
- Before: “Zionism is an ethnocultural nationalist movement that emerged in late 19th-century Europe to establish and support a Jewish homeland through the colonization of Palestine, a region corresponding to the Land of Israel in Judaism and central to Jewish history.”
- After: “Zionism is an ethnocultural nationalist movement that emerged in late 19th-century Europe, seeking to establish and support a Jewish homeland through the colonization of Palestine.”

### 9. "settlement" out, "colonization" in, stated as fact

- Change k=285, 2026-07-11, wording 166 → 149; the stance it set lasted **40 days** (to the next non-neutral change)
- Codes: **more_critical**, own_voice, contested_characterisation
- Before: “Zionism is an ethnocultural nationalist movement that emerged in late 19th-century Europe to establish and support a Jewish homeland through settlement in the region of Palestine, which roughly corresponds to the Land of Israel in Judaism, itself central to Jewish history.”
- After: “Zionism is an ethnocultural nationalist movement that emerged in late 19th-century Europe to establish and support a Jewish homeland through colonization in the region of Palestine, which roughly corresponds to the Land of Israel in Judaism—itself central to Jewish history.”

### 10. Land of Israel borders "would encompass a much larger area" in

- Change k=2, 2021-03-02, wording 1 → 2; the stance it set lasted **31 days** (to the next non-neutral change)
- Codes: **more_critical**, own_voice, contested_characterisation
- Before: “Zionism ( Tsiyyonut after Zion) is both an ideology and nationalist movement among the Jewish people that espouses the re-establishment of and support for a Jewish state in the territory defined as the Land of Israel (roughly corresponding to Canaan, the Holy Land, or the region of Palestine).”
- After: “Zionism ( Tsiyyonut after Zion) is both an ideology and nationalist movement among the Jewish people that espouses the re-establishment of and support for a Jewish state centered in the area roughly corresponding to Canaan, the Holy Land, or the region of Palestine, but whose borders as the Land of Israel would encompass a much larger area.”

For context: "colonial" or "colonization" first entered the sentence on 2024-06-05 (k=56, "as a colonial project", reverted the next day). The current wording dates from 2026-08-27 (k=292, "through colonization" restored, stated as fact; live 69 days to the end of the data): “Zionism is an ethnic nationalist movement that emerged in late 19th-century Europe to establish and support a Jewish homeland through colonization in the region of Palestine, which roughly corresponds to the Land of Israel in Judaism—itself central to Jewish history.”

## October 7 stepper articles (same method, same run)

| article | changes | uncodable | more / less / neutral / mixed | κ direction / voice / claim | headline cell: changes (share of coded) | mirror cell | adjudicated |
|---|---|---|---|---|---|---|---|
| October 7 attacks | 131 | 10 | 21 / 20 / 76 / 4 | 0.923 / 0.718 / 0.790 | 9 (7.4%) | 8 | 29 |
| Hamas | 120 | 2 | 31 / 27 / 56 / 4 | 0.901 / 0.788 / 0.869 | 29 (24.6%) | 20 | 15 |
| Gaza genocide | 247 | 45 | 64 / 46 / 88 / 4 | 0.889 / 0.910 / 0.920 | 29 (14.4%) | 8 | 24 |

For these articles, direction is read from Israel's standpoint in the conflict. "more_critical" also covers removing or softening a charge or negative description of Israel's adversaries, for example "terrorist", "militant" to "military", "attacks" to "incursions", or dropping hostage-taking. The same applies to adding the self-description "nationalist" for Hamas, which mirrors the Zionism rule on self-description. This extension is a judgement call and is stated in `axes.direction._extension_for_oct7_articles`.

## Reader-facing labels

The internal codes stay as they are. `change_codes.json` → `label_options` gives 2 or 3 candidate newsroom labels for each axis value, with a one-line note on the trade-offs. An editorial pass will choose the final wording. Avoid "hostile". Use "attributed", not "alleged".

## Caveats

1. **The coders are not independent humans.** Both blind passes and the adjudicator are Claude. The passes were blind to each other and ran as separate processes, but they share training and therefore biases. κ measures consistency under the codebook, not validity. A human check would answer a hostile reader best: an Israeli and a non-Israeli coder on the 26 adjudicated transitions plus a random 30.
2. **Order errors.** In 3 adjudicated pairs a coder read the before and after texts backwards. An agreed code could be wrong in the same way only if both coders, with independent A/B orders, made the error on the same pair. That is unlikely, but not checked beyond the mirror test.
3. **Marginal calls.** "homeland" to "state", "homeland" to "home", "Modern Zionism", "in Judaism" and "roughly" are close calls. Each one is noted in the transition record.
4. **The codebook decides direction.** Removing Jewish-history or self-description framing counts as more critical by definition. A reader who rejects that rule will reject the direction codes for roughly 50 transitions whose gloss turns only on that framing. The claim_type and voice codes do not depend on it.
5. **Stored text is sometimes cut off** at a fixed length (for example "an area of central importa"). In those cases the coders judged the fragment they had.
6. **Uncodable changes:** 37 of 292 (12.7%). In those changes the before or the after wording was never stored, or is blank. The page should show them as "not coded", not as neutral.
7. **Time is in whole days.** Same-day edits get 0 days. The end date (2026-11-04) is derived from `live_days`.
8. **Only the first sentence is coded.** Changes elsewhere in the opening paragraph are not covered here.
9. No editor names or ids appear in these files.
