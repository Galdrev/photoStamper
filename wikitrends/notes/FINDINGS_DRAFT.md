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
