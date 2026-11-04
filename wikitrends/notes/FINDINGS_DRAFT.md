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
