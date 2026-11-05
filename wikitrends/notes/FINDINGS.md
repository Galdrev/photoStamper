# Findings (final; verified by an adversarial review; every number traceable to a data file)

## Headline
In the pre-registered test, critical terms ("genocide", "apartheid", "occupation", "colonial"…) did **not** rise significantly more in 422 English Wikipedia articles on Israel, Jews and Zionism than in comparison articles between Jan 2021 and Oct 2026. **Verdict: NOT SUPPORTED.** The test cannot rule out a moderate change in article openings.

In a much larger exploratory sample (10,433 articles), these terms became modestly more frequent **after October 2023**. The rise is concentrated in Palestine- and Israel-tagged articles and is similar in size to other war-affected topics (Armenia, Russia, Ukraine). Judaism articles did not move.

Word counts do not show who a term is aimed at. They measure the **vocabulary of conflict**, not an editorial stance.

## 1. Pre-registered test (deep panel)
Source: data/results.json (run 41978060043). The panel is 332 topic and 90 comparison articles that existed in Jan 2021. 85 manifest articles were excluded because they never reached 300 words of prose: stubs, lists and redirects, listed in data/excluded_articles.json.

| id | outcome | extra change (per 10k words) | 95% CI | p | q (BH) |
|---|---|---|---|---|---|
| P1 | critical terms, opening paragraph (n 289/88) | +6.36 | [−2.50, +15.77] | 0.199 | 0.338 |
| P2 | critical terms, full text | −0.30 | [−2.70, +1.68] | 0.846 | 0.846 |
| P3 | connection terms, full text | −1.64 | [−4.05, +0.26] | 0.225 | 0.338 |

**Verdict: NOT SUPPORTED.** This is absence of evidence, not evidence of absence. P1's interval allows a meaningful rise.

**Robustness** (data/results.json `robustness`):
- **P1 under specific checks:**
  - hand-picked articles only (R1): **+13.0 [2.0, 25.8], p = 0.046**;
  - comparison reweighted to topic article lengths (R4): **+23.1 [12.2, 33.6]**;
  - without "genocide" terms (R2): **+0.4 [−5.6, 6.1]**, so the opening-paragraph signal is mostly genocide vocabulary;
  - medians (R5): 0.0;
  - cluster bootstrap by subgroup (R8, added later): [−9.6, 23.2];
  - log scale (R7): n.s.
- **P2:**
  - R4: +4.1 [1.3, 6.8], in the opposite direction from the point estimate;
  - all other checks: n.s.
- **P3:** all checks n.s.
- **Placebo vocabulary (R6):** no group difference in any test, so the instrument is not biased.

**Multiplicity.** About 470 tests were run across the study. Of the 81 secondary deep-panel tests, one survives BH q < 0.10: "militant", full text, pre-war (+0.73, q = 0.049).

**Validation.** 2 of 4 pre-specified known changes were detected (Israel's genocide wording, Dec 2025; the Gaza entry in List of genocides). The Zionism "colonization" target failed on timing: the wording entered between Apr and Jul 2024, not Jul–Oct as press reports said. A post-hoc check finds it there, but that check does not count. The Gaza genocide target used a weak pattern. Occupied Palestinian territories resolved to a different title and was not in the fetched data.

## 2. Exploratory: mass tier (10,433 articles by WikiProject importance; 3 snapshots)
Source: data/mass_results.json (run 41918142246).

- **Critical terms, full text:**
  - whole window +0.50 [0.28, 0.74];
  - pre-war +0.04 (n.s.);
  - **post-war +0.47 [0.27, 0.68], p < 0.001**.
- **Critical terms, opening paragraph:** pre-war +0.14 (n.s.), **post-war +2.51 [1.60, 3.39]**.
- **Connection terms, opening paragraph:** post-war −0.58 [−1.12, −0.03].
- **Size:** about 1 extra critical term per 20,000 words of article text.
- **By project (mean change, critical, full text):**
  - topic: Palestine +1.28, Israel +0.71, Jewish history +0.34, **Judaism +0.002**;
  - comparison: Armenia +1.08, Russia +0.69, Bosnia +0.55, Ukraine +0.54; others −0.39 … +0.30.
- **Caveat:** the importance strata are unbalanced (Mid: 2,160 topic vs 154 comparison). The effect holds within Top (+0.78) and High (+0.67).
- **Other Wikipedias** (per 1,000 words, topic minus comparison change): English (+0.05) lies within the range of 10 other languages (−0.06 … +0.14). But on the 16 key articles, English opening paragraphs gained critical terms more often than other languages (63% vs 40%). The result depends on scale. The multilingual lexicon is smaller.

## 3. Exploratory: process (organic or organised?)
- **Ratchet** (lead of every revision, 25 topic and 15 comparison key articles; data/ratchet.json; CIs from an article-level bootstrap, script in notes):
  - **Survival:** critical-term insertions survive 30 days 36% (topic) vs 56% (comparison). Asymmetry (insertion minus removal survival): topic +0.07 [−0.02, +0.18]; comparison +0.28 [+0.08, +0.41].
  - **Group difference:** about −0.22, not significant. The "push until it sticks" pattern is not stronger for the topic.
  - **Without the Israel article** (34% of topic events): +0.06 [−0.04, +0.24].
  - **Churn:** more insertion/removal events per article in the topic (10.7 vs 5.0). Yet lead revert rate is *lower* in the topic (8.5% vs 16.8%).
  - **Militant:** topic −0.10 vs comparison +0.47.
- **Co-editing** (not proof of coordination):
  - recurring editor pairs per 10k edits: topic 1.6 / 0.7 (pre/post war; the rate fell after the war in both groups) vs comparison 0.6 / 0.35;
  - sweeps per 1,000 editors: 102 / 120 vs 73 / 70;
  - deep panel editor-overlap ratio: topic 1.11 → 1.61, comparison 1.17 → 1.08.
  - **Topic articles show 2–3× more recurring co-editing per edit, and overlap rose after the war.** The null model produced no baseline pairs. Shared watchlists and breaking news produce the same pattern.

## 4. Exploratory: content and epistemics
- **Hedging:**
  - mass tier: topic share of loaded-term mentions with attribution 0.22 → 0.25; comparison flat at 0.17;
  - deep panel: topic 0.26 → 0.25 while comparison rose 0.16 → 0.18;
  - unhedged topic mentions grew by about 59%.
  - The tiers disagree, so there is no clear direction.
- **Sourcing:** the scholarly-citation share rose in both groups (topic 0.37 → 0.54, comparison 0.48 → 0.63).
- **Masked stance coding** (260 changed leads; data/blind/blind_summary.json):
  - newer version harsher on its subject: topic 12.4% vs comparison 5.6%; net difference +0.075, **p = 0.22 (n.s.)**;
  - the "subject" is not always Israel or Jews (it includes Breivik, Qutbism and the ADL);
  - quality: calibration 98%, anchors 100%, swap consistency 70%, smaller-model agreement 0.67.
- **Blinding failed:** a model named the exact article for 25 of 30 masked leads.
- **Narrative coding** (the 45 directional items):
  - recurring moves in topic changes: events added, appeals to courts/UN/rights groups, harsher labels, attributed claims turned into stated fact;
  - tone moved toward "leaning/advocacy" in 36% of topic vs 33% of comparison changes, so **no difference in tone**;
  - examples were chosen as the first listed by item id, not hand-picked.
- **Lexicon precision:** 0.90–1.00 for critical terms, but "intended sense" does not mean "directed at Israel". Indigenous/homeland precision is 0.725. The connection lexicon excludes Palestinian homeland terms by design.

## What this study can and cannot say
- **Can say:**
  - the pre-registered test did not find a topic-specific framing shift;
  - after Oct 2023, conflict vocabulary rose modestly in Palestine/Israel articles, as it did in other war-affected topics;
  - English Wikipedia is not an outlier among 11 languages;
  - topic articles show more co-editing per edit.
- **Cannot say:**
  - whether any change is accurate;
  - whether terms are aimed at Israel or others;
  - whether co-editing reflects coordination;
  - that "nothing changed" (the lead test is underpowered).
