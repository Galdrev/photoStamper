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
