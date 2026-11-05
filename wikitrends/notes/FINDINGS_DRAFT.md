# Findings draft (internal; written as results arrive; every line traceable to a data file)

## Ratchet (exploratory; 25 topic vs 15 comparison key articles; lead of every revision since 2021)
Source: data/ratchet.json (run 41932638279). CIs: 2,000-sample article-level bootstrap.

| family | group | insertion survives 30d | removal survives 30d | asymmetry | n ins / rem |
|---|---|---|---|---|---|
| critical | topic | 0.36 [0.29, 0.51] | 0.30 [0.24, 0.41] | +0.07 [-0.02, +0.19] | 267 / 249 |
| critical | comparison | 0.56 [0.41, 0.67] | 0.28 [0.21, 0.41] | +0.28 [+0.06, +0.41] | 75 / 76 |
| connection | topic | 0.42 [0.35, 0.55] | 0.21 [0.15, 0.32] | +0.21 [+0.09, +0.35] | 92 / 86 |
| connection | comparison | 0.70 [0.48, 0.88] | 0.35 [0.18, 0.58] | +0.35 [-0.03, +0.61] | 23 / 20 |
| terrorism | topic | 0.22 [0.05, 0.64] | 0.17 [0.06, 0.35] | +0.05 [-0.15, +0.48] | 50 / 48 |
| terrorism | comparison | 0.29 [0.00, 0.58] | 0.67 [0.28, 1.00] | -0.37 [-0.92, +0.27] | 17 / 15 |

Reading:
- Insertions outlast removals in both groups. This is a general Wikipedia pattern.
- The "push until it sticks" asymmetry is not larger for the topic articles. It is smaller for critical terms.
- The topic articles are far more contested: about 3.5× the insertion and removal events per group, with lower survival for both.
- Mean failed attempts before a critical term stuck: topic 3.3 vs comparison 1.4. Retries are more common, which is consistent with contestation in both directions.

## Mass tier (exploratory; 10,433 articles sampled by WikiProject importance; Jan 2021 → Nov 2026)
Source: data/mass_results.json (run 41918142246). Permutation p-values, bootstrap CIs.

- **Critical frames, full text:** DiD +0.50 per 10k words [+0.28, +0.74], p < 0.001 (n 4,078 topic / 5,111 comparison).
- **Critical frames, lead:** DiD +2.38 [+1.43, +3.41], p < 0.001. **Connection frames, lead:** −1.00 [−1.74, −0.29], p = 0.009. **Connection frames, full text:** −0.03 (n.s.).
- **By importance:** Top +0.78 [0.17, 1.53]; High +0.67 [0.35, 0.98]; Mid +0.45 (n.s.).
- **By project (mean change, critical, full text):** topic Palestine +1.28, Israel +0.71, Jewish history +0.34. Comparison Armenia +1.08, Russia +0.69, Bosnia +0.55, Ukraine +0.54. The signal concentrates in conflict articles, at a size similar to other war-hit topics.
- **Hedging (share of loaded-term mentions with attribution):** topic 0.22 → 0.21 → 0.25; comparison 0.17 → 0.17 → 0.17. More attribution over time, not less.
- **First sentence contains a critical term:** topic 1.3% → 1.5% → 2.1%; comparison 0.6% → 0.6% → 0.7%.
- **Cross-language (per 1,000 words; topic minus comparison change, per language):** English full-text equivalent +0.05 sits inside the range of the other 10 languages (−0.06 … +0.14). Only Portuguese lead is significant (+0.27). English is not an outlier. Caveat: the multilingual lexicon is smaller.
- **Coordination (tailgating pairs, ≥5 shared articles):** topic 29 / 20 (pre/post war), comparison 31 / 19. Not higher for topic. The circular-shift null produced 0 pairs, so the ratio is undefined; report counts only.

## Pre-registered primary tests (deep panel; run 41978060043; analysis log tail)
Panel: 332 topic / 90 comparison articles existing in Jan 2021. 513 articles loaded (85 manifest articles were dropped; reason still to verify). 260,831 revisions.

| id | outcome | DiD | 95% CI | p (perm) | q (BH) |
|---|---|---|---|---|---|
| P1 | critical, lead | +6.36 | [−2.50, +15.77] | 0.199 | 0.338 |
| P2 | critical, full text | −0.30 | [−2.70, +1.68] | 0.846 | 0.846 |
| P3 | connection, full text | −1.64 | [−4.05, +0.26] | 0.225 | 0.338 |

**Pre-registered verdict: NOT SUPPORTED.** None of P1–P3 is significant after BH.

Validation targets: Israel PASS; List of genocides PASS; Zionism (press timing) FAIL, while its post-hoc window PASSES; Gaza genocide FAIL (a weak "allegations" pattern written by me); Occupied Palestinian territories not in data.

Deep-panel exploratory: hedged share topic 0.26 → 0.25, comparison 0.16 → 0.18. Scholarly citation share rose in both groups (topic 0.37 → 0.54; comparison 0.48 → 0.63). First sentence contains a critical term: topic 4.2% → 6.0%, comparison 10.0% → 8.9%.

## Masked stance coding (exploratory; rubric v2; 260 changed leads, 170 topic / 90 comparison; both A/B orders)
Source: data/blind/blind_summary.json
- Quality gate PASSED: calibration 98.3% (known-answer synthetic edits), anchors 100%, swap consistency 70%, 0 unsupported quotes.
- Newer version harsher on its subject: topic 12.4% vs comparison 5.6%. Newer version gentler: topic 7.1% vs comparison 7.8%.
- Net (harsher minus gentler) difference topic − comparison: +0.075, permutation p = 0.22. **Not significant.** Direction is consistent with the mass tier.
- **Blinding check: an AI named the exact article for 25/30 masked leads (83%).** Masking does not blind models to Wikipedia. Coding is "masked, not blind", and coder priors cannot be ruled out.

## Lexicon precision (480 hits hand-coded by agent; data/kwic_coded.json)
Precision: apartheid, ethnic cleansing, occupation, antisemitism/persecution 1.00; settler-colonial 0.975; war crimes 0.95; militant 0.95; genocide 0.925; terrorism 0.925; Nakba/expulsion 0.90; placebo geography 0.825; indigenous/homeland 0.725 ("Land of Israel" used as a place name inflates the topic-side connection count). The connection lexicon excludes Palestinian homeland/indigeneity terms by design, so it measures one narrative. 2 of 40 "colonial" hits are historical Zionist self-descriptions.
