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

## Part C: content KPIs, coded by two independent LLM coders on 205 masked pairs (150 topic, 55 comparison)
**Coding quality:**
- 0 invalid codes; 0 quotes voided as non-verbatim.
- Reliable (κ ≥ 0.6): K01 0.69, K03 0.74, K04 0.86, K08 0.89, K10 0.66, K11 0.74, K12 0.78.
- Unreliable: K02 0.59, K07 0.51.
- No variance: K05. No coder found any "Zionist militants"-type relabel in the holdout.

**Primary family: none supported.** The topic share of pairs showing each move is not higher than the comparison share. The comparison leads were rewritten at similar or higher rates.

| KPI | Topic | Comparison | Δ [95% CI] | q | Verdict |
|---|---|---|---|---|---|
| K01 voice upgrade | 6.7% | 10.0% | −3.3 [−11.9, 4.4] | 0.55 | not supported |
| K02 story onset | 6.3% | 14.5% | −8.2 | 0.08 | unreliable (κ 0.59) |
| K03 name primacy | 21.7% | 35.5% | −13.8 [−27.3, −0.9] | 0.08 | reverse, but the length-adjusted MH is n.s. (−7.8, p 0.30) |
| K04 definitional class | 2.3% | 0% | +2.3 [0.3, 5.0] | 0.55 | not supported (too rare) |
| K05 actor relabel | 0% | 0% | — | — | no variance |
| K09 camp label (auto) | 2.0% | 9.1% | −7.1 | 0.08 | reverse of discovery (6% vs 0%) |

Every secondary KPI was also not supported.

**Direction within topic pairs (exploratory, was not tested, small counts averaged over coders).** When a move happens in a topic article, its direction is lopsided:
- **K01 voice:** claims about the Jewish/Israeli party move into narrator voice in about 6 pairs, against 1 the other way.
- **K07 harm agent made explicit:** Israeli actor about 5, Palestinian 0. K07 is unreliable (κ 0.51).
- **K03 names:** balanced. Jewish/Israeli names were demoted in 9 pairs and promoted in 6; Palestinian/Arab names were demoted in 6 and promoted in 8.
- **K11 Jewish belonging claims:** strengthened in 11 pairs, weakened in 6. Not a cut.

**Reading.** The rhetorical *moves* the close readers saw are ordinary Wikipedia editing, about as frequent in comparison articles. What looks topic-specific is not *how often* a move happens but *which way* it points and *what content* it carries. The counts are too small to confirm that here.

**Deviation.** The coders shared one scratchpad. Two coder-2 sessions saw the first lines of a coder-1 helper script, a file path only, no codes. The risk to independence is low, and it is recorded here.
