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

## Part C. Qualitative content KPIs (frozen)

**Frozen 2026-11-05**, before any holdout coding. Everything is in `wikitrends/study3/codebook_final/`: `CODEBOOK.md` (human-readable), `codebook.json` (machine-readable, read by the scripts), `coder_instructions.md` (the exact LLM coder prompt), `auto_kpis.py`, `make_batches.py`, `analyze_codes.py`. This merges three discovery-only close readings (`qual_voice/`, `qual_history/`, `qual_process/`). Moves found by two or three readers come first. Moves every reader called general Wikipedia style are kept only as style controls.

**Coding set and unit.** Holdout lead pairs from `data/study3/qual_holdout.json`: every topic pair with change > 0.05, plus every comparison pair (control and control_contaminated). Pairs that `auto_kpis` flags as template artefacts are excluded. The unit is the lead pair (K04: the first sentence). The run happens once.

**Primary KPIs (BH family, q = 0.10).** Each is the share of pairs showing the move, old to new:
- K01 voice_upgrade: a contested characterisation that appears in both versions climbs the attribution ladder toward narrator voice.
- K02 story_onset: the causal story starts earlier, or gains a prior cause.
- K03 name_primacy: the primary name, or the co-name order, changes for a place, polity or subject. Macro-region labels are excluded.
- K04 definitional_class: the first-sentence definition gains a colonial, atrocity, legal-violation or apartheid category in narrator voice.
- K05 actor_relabel: a collective actor's label moves to an ideological category ("Jewish militias" to "Zionist militants").
- K09 camp_label: a partisan-alignment label is added (automatic regex).

K01–K05 are LLM-coded; K09 is automatic.

**Secondary KPIs** (BH separately, exploratory): K06 presupposed evaluative noun phrase (automatic; demoted because the discovery contrast was +2.7 pp under a group-neutral lexicon), K07 harm-agent explicitness, K08 party denial appended, K10 refusal recontextualised, K11 belonging claims (continuity, demography, indigeneity), K12 suffering as motive.

**Style controls** (both groups, never tested): SC1 genus change, plus the automatic length, first-sentence and attribution-density measures and the terror* label in sentence 1.

**Direction** is coded per claim and per party: JEWISH_ISRAELI, PALESTINIAN_ARAB, OTHER_STATE, OTHER_GROUP. It is never coded per article. Labels are descriptive, e.g. "moves a characterisation of [party]'s conduct from attributed to narrator voice". Party breakdowns are descriptive only.

**Decision rule.**
- Pair score: the mean of the two coders' binary indicators, or the automatic 0/1.
- Estimate: Δ = topic share minus comparison share.
- CI: 95% bootstrap over pairs within group (10,000 resamples, seed 20261105).
- p: two-sided permutation p (10,000). This replaces a CI-derived p because comparison cells of 0 make the bootstrap degenerate.
- Multiplicity: BH at q = 0.10 across the six primaries.
- Length: lead0 word terciles with cut points fixed from discovery (T1 ≤ 158, T2 159–340, T3 ≥ 341). Every KPI is reported per pair and per tercile. A Mantel–Haenszel risk difference across terciles gets a stratified bootstrap CI and a within-tercile permutation p.
- A primary KPI is **supported** if all of these hold: it is reliable, BH q ≤ 0.10, Δ > 0, the MH risk difference is > 0, and the stratified p ≤ 0.10. It is **length-sensitive** if BH-significant but the MH condition fails, **reverse** if BH-significant with Δ < 0, and **not supported** otherwise.
- Pre-specified sensitivity analyses (they do not change verdicts): both-coders and either-coder combinations; without control_contaminated; comparison also filtered to change > 0.05; lead0 dated 2021 only; excluding pairs marked unusable.

**Reliability.** Two independent LLM coding sessions with the same prompt, each with its own randomised A/B orientation and item order. Cohen's κ is computed per KPI on the binary indicator; raw agreement, PABAK and the full categorical κ are also reported. **A KPI with κ < 0.6 is reported as unreliable and not interpreted.** The BH family stays fixed. Every positive code needs a verbatim evidence quote, and non-verbatim quotes void the code. A coder with more than 15% voided codes is re-run once, and both runs are reported. The automatic KPIs are deterministic. Validity checks: the K04a regex is compared with the LLM's K04 colonial codes, and K09 spans get a precision audit.

**Masking.** The coder sees only the two cleaned leads, labelled Version A and Version B in random order, plus unordered first-sentence variants (text only) where traced edits exist. The coder does not see the title, group, dates, edit summaries or the order key, which stays in `KEY_DO_NOT_SHARE.json`. The content usually reveals the subject, and the party codes reveal what the study is about. Masking guards against knowing the group label and the before/after direction, not the subject.

**Not applied:** the Amendment D event filter. Coders see the full leads, and update-only changes are excluded inside the KPI definitions (K01 and K02 exclude new facts and chronology).

**Discovery calibration (not results).** The frozen regexes give, topic vs comparison over 166 and 46 pairs:
- K09: 6.0% vs 0.0%.
- K06: 11.4% vs 8.7%.
- K04a (colonial term enters sentence 1): 1.8% vs 2.2%.

The scripts were tested on discovery only: 212 pairs in 11 batches, leak check clean. The analysis ran end to end on fake codes and recovered a planted effect with correct orientation.

## Amendment D: separating narrative change from event updates (frozen 2026-11-05, before any filtered number was computed)

**Problem the owner raised:** when October 7 and the war happened, articles were *expected* to gain sentences about them. The Israel article adding the war is a factual update, not a narrative change. We want the narrative change only.

**Rule** (`wikitrends/event_filter.py`, symmetric for topic and comparison, fixed in advance). A sentence counts as an **event sentence** if it does any of the following:
- (a) names a year from 2022 onward;
- (b) mentions a recent event from a fixed list that covers both the topic (Oct 7, Israel–Hamas/Gaza war, hostages, ICJ case, Iran–Israel war, Gaza famine/genocide, 2024 Lebanon) and comparison conflicts of the same era (Russian invasion of Ukraine, Sudan war, the 2023 Karabakh offensive and exodus, Tigray, Myanmar, Wagner);
- (c) uses recency wording ("the ongoing war", "as of", "since the start of the war").

Everything else is the **narrative residual**.
- **Primary:** drop event sentences only.
- **Sensitivity:** drop every paragraph that contains an event sentence.

**Outcomes:** each analysis below is reported three ways:
- unfiltered;
- residual (narrative);
- event part (updates), with the event share of critical terms.

Analyses covered:
1. Study 1 critical-rate change, lead and full text, topic vs comparison DiD (deep tier, every quarterly snapshot; computed in CI by `event_clean.py`).
2. Study 3 A1–A6 on mass-tier leads (mass_narr now stores the lead text, so the residual can be computed).
3. Study 2 N-measures on the residual.

**Interpretation rule:** if a topic effect survives in the residual, it is narrative change in older material, not event coverage. If it lives only in the event part, it is the war being covered.

**Known bias, accepted in advance:** rule (a) also drops sentences that cite recent scholarship ("in 2024 scholars described the Nakba as…"). That removes some real narrative change, so the filter is conservative against finding narrative change.
