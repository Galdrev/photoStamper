# Study 3 holdout results (frozen scripts, run once, unchanged)

## Part A: primary family (BH q = 0.10). 7 of 10 replicate.
| # | Holdout estimate [95% CI] | q | Verdict | Discovery |
|---|---|---|---|---|
| A1 share gaining critical terms, post-war DiD (mass) | +3.6 pp [1.7, 5.6] | 0.002 | ✅ replicates | +7.2 pp |
| A2 substantial gain (>0.5 per 1k) | +3.5 pp [2.2, 4.9] | 0.002 | ✅ | +3.7 pp |
| A3 occupation/Nakba minus genocide | +1.8 pp [−0.1, 3.6] | 0.074 | ❌ CI touches 0 | +3.9 pp |
| A4 opening paragraph gains | +2.5 pp [1.3, 3.7] | 0.002 | ✅ | +2.6 pp |
| A5 Israel+Palestine minus Judaism | +5.6 pp [2.6, 8.4] | <0.001 | ✅ | +9.9 pp |
| A6 Top/High-importance articles | +3.7 pp [0.9, 6.5] | 0.008 | ✅ | +9.4 pp |
| A7 concentrated in most-edited articles | +1.8 pp [−6.2, 9.7] | 0.66 | ❌ | +15.9 pp |
| A8 ratchet (moves go up) | +0.07 [−0.05, 0.20] | 0.26 | ❌ same sign | +0.125 |
| A9 sustained addition rate, topic | +0.017 [0.003, 0.031] | 0.029 | ✅ | +0.041 |
| A10 post-war surge predicts gain, baseline churn doesn't | −2.26 [−3.58, −1.21] | <0.001 | ✅ | −0.98 |

**Secondary checks:**
- **A5b (Judaism vs comparison):** −0.1 pp [−2.3, 2.3]. Within ±3, so equivalent: no change.
- **Placebo words:** +1.8 pp [−0.4, 4.1], n.s. A1 is twice the placebo, but the gap is not large.
- **Net gain DiD:** +3.5 pp [0.9, 6.2].
- **Occupation/Nakba alone:** +3.0 pp [1.5, 4.6]. **Genocide alone:** +1.2 pp [0.2, 2.3].
- **Deep full-text tail:** null again.
- **Growth, not rewriting:** +0.18 [0.03, 0.33]; replicates.
- **Timing lag:** n.s.

**New in the holdout, not predicted; exploratory, needs a third sample:**
- **Salience interaction (deep):** +0.38 [0.09, 0.71].
- **Revert moderation:** T×revert −3.9 [−6.8, −0.5]. Contested topic articles changed *less*.
- **Editor concentration:** top10 coef +4.0 [1.5, 8.0]. In discovery it was null, with the opposite sign.

**Effect size shrinkage:** holdout effects are about half the discovery size. This is the expected winner's-curse shrinkage, and the halved size is the honest one.

## Part B: narrative (deep leads)
| # | Holdout result | Verdict |
|---|---|---|
| B1 additive, not substitution | ρ(critical, continuity) = −0.03; ρ(critical, Jewish-history density) = −0.04 | ✅ pass |
| B1 mass domain split | Israel +3.2 pp, Palestine +4.6 pp, control +0.4, Judaism −0.4, Jewish history +0.4 | ✅ pass |
| B2 war-triggered, history-anchored | 18 history-anchored vs 5 event-anchored added sentences; topic up-step rate 0.9%→1.6%, control flat | ✅ pass |
| B3 Palestine as modern land name | 10 articles up, 2 down; sign p = 0.039. Jewish names also rose (11→19) | ✅ pass (both grew) |
| B4 claims move into Wikipedia's voice (regex) | Unattributed share 0.63→0.55; DiD −0.04 | ❌ fail |
| B5 Palestinian displacement up, Jewish not down | P 14→13, J 12→8 | ❌ fail |
