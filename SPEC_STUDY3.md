# Study 3: sharper questions, from the data, tested on data nobody mined (frozen 2026-11-05)

**Why:** study 1's pre-registered average test was null. Most articles do not change, and a minority change a lot. The owner asked for better questions, without dressing the answer up. So:
1. We split all articles 50/50 by `sha1("study3|"+title)` (commit c3a07bf, before any hypothesis existed).
2. Agents mined only the **discovery** half (scripts committed as delivered: `wikitrends/study3/hyp_where.py`, `hyp_how.py`, `hyp_narr.py`, plus the discovery output `run1000.txt`).
3. The hypotheses below are frozen here. They are then run **once, unchanged**, on the **holdout** half.
4. Known limit: the aggregate study-1 results were already known, so this guards against article-level overfitting, not against knowing the headline.

## Part A. Quantitative hypotheses (holdout: mass tier 5,146 articles, deep tier 253)

Each one uses the named function, unchanged, on holdout articles. "Replicates" means the estimate has the predicted sign AND the script's 95% bootstrap CI excludes the null. Benjamini–Hochberg at q = 0.10 runs across the primary family, A1–A10. For this correction we convert each CI to an approximate two-sided p, assuming normality from the CI width. The `hyp_where` functions also use their permutation p.

| # | Question | Function | Prediction (discovery estimate) |
|---|---|---|---|
| A1 | After Oct 2023, did a larger share of topic articles gain critical vocabulary than comparison articles? | where.h1b_any_gain_did | > 0 (+7.2 pp) |
| A2 | Same question, for a substantial gain of more than 0.5 per 1k words | where.h1_tail_share_did | > 0 (+3.7 pp) |
| A3 | Is the gain carried by occupation and expulsion/Nakba words more than by genocide? | where.h2_occnakba_minus_genocide | > 0 (+3.9 pp) |
| A4 | Did the opening paragraph gain too? | where.h3_lead_any_gain_did | > 0 (+2.6 pp) |
| A5 | Is the change in the Israel and Palestine projects rather than Judaism? | where.h4_ip_minus_judaism | > 0 (+9.9 pp) |
| A6 | Did high-importance topic articles change more than high-importance comparison articles? | where.h5_mass_importance_TH_did | > 0 (+9.4 pp) |
| A7 | Is the excess concentrated in the most-edited articles (top quintile of edits, cut recomputed on the holdout)? | how.h1_surge_concentration (triple difference) | > 0 (+15.9 pp) |
| A8 | Ratchet: among articles whose count moved, did "up" become more dominant post-war in topic articles? | how.h3_direction_ratchet_mass | > 0 (+0.125) |
| A9 | A sustained rise, not a one-off jump: the share of quarters that add critical terms, topic articles post vs pre | where.h6b_deep_addition_hazard_topic_only | > 0 (+0.041) |
| A10 | Within topic articles, does the post-war surge in editing predict gain while baseline churn does not (vs a placebo frame)? | how.h2_surge_not_baseline (difference) | < 0 (−0.98) |

**Equivalence and secondary checks.** None of these enter the BH family. All are reported.
- **A5b:** Judaism vs comparison, `where.h4b_judaism_vs_comparison`. Prediction: within ±3 pp.
- **Placebo:** `where.h1_placebo_did` (placebo geography words). Expected to be well below A1.
- **Net version:** `where.h1c_net_gain_did`.
- **Deep ratchet:** `how.h3b_ratchet_deep`.
- **Timing:** `how.h5_timing_lag`.
- **Growth:** `how.h4_growth_vs_rewrite`, reported at thresholds 1.00, 1.05 and 1.10.
- **Salience interaction:** `where.h7_deep_salience_interaction`.
- **Rejected in discovery, re-reported:** `where.r1_*`, `where.r2_*`, `how.r1_*`, `how.r2_*`.

## Part B. Narrative hypotheses (deep holdout, lead text)

These run `hyp_narr.py` unchanged on the holdout. Each function's own pre-stated `pass` flag is the replication criterion. We report the numbers, not just the flag.

- **B1. Additive layering, not substitution.** In the deep tier, an article gaining critical lead framing does not lose continuity or Jewish-history framing: Spearman ρ > −0.15 (`h1_additive_layering_deep`). Mass leads: the share with any critical frame rises in Israel and Palestine by at least 1.5 pp more than in control, and changes by less than 1.5 pp in Judaism and Jewish history (`h1_domain_split_mass`).
- **B2. The war triggered it; history is the content.** Among added critical lead sentences, historical anchors outnumber 2023-or-later references, and the up-step rate per article-quarter rises post-war in topic more than in control (`h2_timing_vs_content`).
- **B3. Palestine becomes the modern land name.** Palestine-type land names in leads rise, judged by sign test across articles (`h3_modern_land_naming`).
- **B4. Wikipedia's own voice.** The share of critical lead sentences with no attribution rises in topic and not in control (`h4_wikivoice`).
- **B5. Two displacements.** Palestinian displacement mentions rise and Jewish displacement mentions do not fall (`h5_displacement_and_violence`).

**Predictions for study 2.** Its measures and analysis were fixed earlier, in SPEC_NARRATIVE.md. These predictions were written before any study-2 result was seen.
- **C1 coherence.** N4 share, N5 and N7 co-move positively. N1, N2 and N8 changes are near zero and uncorrelated with that cluster. So H2-coherence, a single shared component, is predicted to FAIL, with no more variance on that component than in the comparison disputes.
- **N2 (before 135 CE).** No significant rise in the Palestine share. The naming change is modern (B3), not ancient.
- **N6.** The share of violence labels attributed to Israeli actors does not rise. Discovery showed a fall from 0.71 to 0.64.
- **N4.** The P share rises because the P rate rises, while the J rate stays flat.

## Part C. Qualitative content KPIs

Frozen separately, after the close-reading codebook is merged; see the Part C section, appended below when frozen. Coding there is masked and done twice per item, with agreement reported.
