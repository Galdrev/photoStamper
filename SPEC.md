# Pre-registered analysis spec

Written 2026-11-04, before any real data was seen. The CI run that collects the data was still in progress when this was committed; the git timestamp is the proof.
Any deviation from this spec must be listed in the report under "Deviations".

## Unit and sample
- Unit: an article. Snapshots are quarterly, from 2021-01 to 2026-10.
- **Primary panel:** articles that already existed on 2021-01-01 (a balanced panel).
- Articles created later (e.g. "Gaza genocide", "October 7 attacks") are reported descriptively and kept out of the tests.
- Groups: topic (hand-picked + category sample) and comparison (hand-picked).

## Primary outcomes (3; BH correction across these at q = 0.05)
- **P1.** Change in the *critical-frame rate in the lead section* (hits per 10k words), from 2021-01 to the latest snapshot. Difference-in-differences (topic minus comparison).
- **P2.** The same for the *full article*.
- **P3.** Change in the *connection-frame rate in the full article*, DiD.

Inference uses a label-permutation p-value (5,000 shuffles of the group labels across articles) and an article-level bootstrap 95% CI.

## Secondary outcomes (exploratory, BH across all of them at q = 0.10)
- Each individual frame, in the full article and in the lead.
- Pre-war (2021-01 → 2023-07) and post-war (2023-07 → latest) windows.
- Edit, talk, revert and anonymous-edit dynamics.
- Editor concentration.

## Robustness (each primary result is reported with a pass/fail count)
- **R1.** Hand-picked articles only (drop the category sample).
- **R2.** Leave-one-term-out: no single regex may account for more than 50% of the effect.
- **R3.** Placebo break dates: does a fake break at 2022-01 show a similar change? Report where the real estimate falls in the distribution of placebo estimates.
- **R4.** Length-matched comparison: reweight comparison articles to the topic group's baseline word count.
- **R5.** Median instead of mean (robust to outlier articles).
- **R6.** Placebo lexicon: geography and climate terms should show a DiD of about 0.

## Blind stance coding (second, independent instrument)
- **Items.** For each article in both groups with a changed lead section: the lead in 2021-01 and the latest lead.
- **Blinding.** The article title and the main entity names are masked. The two versions are shown in random order as A and B.
- **The question.** Does version B, compared with A, frame its subject more favourably, less favourably, the same, or is it unclear?
- **Change type.** Is the change a factual update or a framing change?
- **Reliability.** Each item is coded 3 times: two prompt wordings and two Claude model sizes. The report gives the agreement between codings.
- **Validation.** Before scaled coding, the coder must recover the expected direction on the known documented changes. If it gets fewer than 70% right, the instrument is reported as failed and not used for conclusions.
- **Name-swap placebo.** 30 comparison-article items with Israel/Jewish entity names swapped in. A coding shift on these means the coder is reacting to names.
- **Outcome S1.** The share of topic leads coded "less favourable", minus the same share for comparison leads. Permutation p-value.

## Decision rule for the headline
- **H1 supported:** at least 2 of P1–P3 are significant after BH, in the predicted direction, and pass at least 4 of 6 robustness checks. S1 must not contradict this.
- **Partial:** at least 1 primary outcome is significant, or the results are mixed.
- **Not supported:** none of P1–P3 is significant.
- The headline sentence on the page must use exactly one of these three labels.

## Amendment 1 (2026-11-04, still before any real data was seen)
These changes come from the independent code review.
- **Snapshots excluded:** redirect snapshots, snapshots under 300 words, and snapshots landing on a later-reverted revision. The lead needs at least 40 words to be measured.
- **Text excluded:** back-matter sections (See also, References, Further reading, External links) are stripped before counting.
- **Lexicon v2:** occupation terms need a territorial anchor ("occupied West Bank", "Russian occupation"; the job sense is gone). "Colonial" is limited to the colonization, colonialism and settler-colonial forms. Jewish expulsions such as the Alhambra Decree no longer count as Nakba/expulsion. Palestinian and Kurdish "homeland/self-determination" no longer count as connection frames. A placebo geography lexicon is added.
- **Comparison set:** 10 contaminated articles (Lebanon, Iran, Palestinian nationalism and others) move out of the primary comparison group. "Shocked" comparison articles (Ukraine, Darfur, Karabakh and others) form a subgroup, and a settler-colonial comparison set is added.
- **Trends:** trend lines use the balanced panel. Articles created during the window are shown separately.
- **War marker:** the first post-war snapshot is 2024-01. The 2023-10-01 snapshot predates 7 October.
- **Primary scale:** stays absolute change in hits per 10k words. On synthetic data, log1p(rate) blew up for articles starting from zero. A log scale with an offset equal to the median baseline rate is added as R7.
- **Edit dynamics:** bots are excluded, temporary accounts (~2025-…) count as logged out, revert rates are per-article means, and the partial final quarter is dropped.
- **Editor breadth:** compared on equal-size random subsamples.
- **Validation:** five dated press-documented changes are added as known-answer tests (corpus.py VALIDATION).

## Amendment 2 (2026-11-04, before real data)
- The name-swap placebo is replaced with an unmasked repeat: 15 topic and 15 comparison items are coded again with names visible, and flip rates are reported by group. Reason: masking would erase any swapped-in names, so the planned placebo could not work.
- Coders: rubric v1 (.claude/skills/blind-stance-coder). Three codings per item: wording A on a large model, wording B on a large model, and wording A on a small model. The final label is the majority; ties count as "unclear".
