# Synthesis: how English Wikipedia's coverage of Israel, Palestine, Zionism and Judaism changed, 2021 to 2026

Editor's synthesis of 38 pattern cards from three analysts (when_where_what = WWW, how_who = HW, story_sources_langs = SSL), plus 12 full-scale cards (mass2 = M1 to M12), 8 event-timing cards on the deep panel (EV1 to EV8), the mass2 event-timing run (`data/event_timing_mass2.json`, cited as EVM), the pilot evaluation (`pilot_eval/EVAL.md`, cited as PILOT) and the study 2 precision check. Checked against notes/FINDINGS.md, study3/holdout_results/SUMMARY.md, study3/holdout_results/event_mass_leads.txt and TALKING_POINTS.md. Chart files are given relative to `wikitrends/patterns/`.

**Tiers, named every time.** *Mass2* is the full crawl: 10,320 articles (4,642 topic, 5,678 comparison), duplicate redirects removed, former titles followed. *Mass v1* is the earlier 3-snapshot run used by WWW and the sealed holdout. *Deep panel* is 513 curated articles, quarterly (407 topic leads in the exposure work). *Key articles* are the 25 to 40 battleground leads with every revision. *Pilot* is 166 hand-picked articles.

**Two kinds of interval in mass2.** Square brackets are article-level bootstrap CIs. Curly brackets are project CIs, which resample whole WikiProjects. The topic side has only 4 projects, so the project CI is coarse and wide. Where the two disagree (article CI excludes zero, project CI does not), this document gives both and treats the claim as one step weaker.

---

## What changed in this update (probability sample, random baseline, network)

Sources: `sampling/mass3_results.md` (cited as M3; chart data `sampling/chart_data/08_mass3_estimates.json`), `sampling/random_baseline.md` (RB), `coord/cards.md` and `coord/chart_data/network.json`, `blocs.json` (NET). *Mass v3* is a stratified probability sample of the full populations: every article PageAssessments lists for WikiProjects Israel, Palestine, Judaism and Jewish history (48,974 topic articles, all importance grades) and for nine conflict-region projects (Ukraine, Turkey, Serbia, Kosovo, Armenia, Azerbaijan, Kurdistan, Cyprus, Northern Ireland; 141,356 articles). 3,000 + 3,000 drawn within side x project x importance; design weights N_h / arrived_h; 95% stratified bootstrap CIs. Note the M3 comparison group is conflict regions only, unlike mass2's 23 projects (countries, conflicts, religions).

**New headline.** The core, most-read Israel articles shifted; the long tail did not; across the full population of 49,000 articles, the average change was no larger than in other conflicts' articles.

- **Core vs long tail (M3, share of leads gaining critical terms, Jul 2023 to now, topic vs comparison).** Top 10.3% vs 4.4% (+5.9 pp [0.9, 11.2]; N 333 vs 482). High 6.0% vs 3.6% (+2.4 pp [−2.5, +7.6], not significant; N 1,699 vs 2,475). Mid 1.5% vs 0.0% (+1.5 pp [0.5, 2.8]; N 7,519 vs 9,662). Low 0.5% vs 0.4% (+0.1 [−0.4, +0.7]; N 25,885); Unknown 0.3% vs 0.6% (−0.3 [−1.1, +0.5]; N 13,319). Low plus Unknown are about 80% of the topic population. Top-grade view share on gaining leads 30.5% vs 19.1% (difference not significant).
- **Population level, not significant.** (a) lead critical DiD −0.37 per 10k [−1.55, +0.83]; (b) share gaining 0.9% vs 0.5%, +0.4 pp [−0.0, +0.9]; (c) residual DiD +0.11 [−1.04, +1.23] (residual share undefined in practice: −30% [−964%, 985%]); (d) view share on gaining leads 4.8% vs 4.6%, +0.2 pp [−5.9, +5.2].
- **Holds at every level.** Israel+Palestine minus Judaism gain share +0.9 pp [0.2, 1.5] (1.2% vs 0.3%). Judaism minus comparison −0.2 pp [−0.7, +0.3]. About 446 [277, 616] topic articles gained critical terms in their lead.
- **Random baseline (RB, 2,466 random articles).** Site-wide drift is about zero: −0.06 per 10k [−0.18, +0.00], post-war share gaining 0.0%. Topic minus random on the mass2 frame +2.60 per 10k [1.75, 3.51] (residual +2.25 [1.43, 3.13]); share gaining +4.1 pp. On the M3 population: topic minus random share gaining +0.9 pp [0.5, 1.2], comparison minus random +0.5 pp [0.2, 0.8]. Contested subjects moved; Wikipedia at large did not.
- **Network (NET).** Topic: 14 significant account pairs vs 2.15 expected by chance (95th 5), all on shared articles (no timing edge); 2 communities of 3+ vs 0.34 by chance. Bloc A (4 accounts, medium): 23 articles, 45 insertions / 23 removals, 0 of 200 null worlds as large and dense. Bloc B (4 accounts, medium): found in the insertions-only test, 114 insertions across 53 articles, null-world share 0.005; being an insertions-only test, it cannot see the same accounts' removals, so "insert-only" describes the test, not proof they never removed. No synchrony (no member event within 10 min of another; median same-article gaps 14 and 66 days), no copy-paste sweeps (topic, comparison, Nakba village wording: 25 sentences, 17 pages, 15 accounts, 0 sweeps), no remove-direction bloc. Both blocs: no account under 500 edits; median age about 3 and 6 years. Comparison: 3 pairs vs 0.28, no bloc. Window alignment, LOW confidence: Bloc A 41% of events in the pro-Israel email-canvassing window vs 18% for matched sets (p 0.02 to 0.04); Discord window 21% vs 23%. Bloc B 34% vs 15% (p 0.05) and 29% vs 24%. Nothing passes p<0.01; no post-sanction drop beyond matched sets.

**Strengthened**
- **Concentration in the core (P2, P3).** Now shown on a probability sample with known inclusion probabilities, by importance grade, against conflict-region comparisons: the Top grade gap (+5.9 pp) excludes zero, and so does Mid (+1.5 pp).
- **Not site-wide drift.** The random baseline rules drift out on every measure (RB card 5: STRONG).
- **Judaism did not move** (P2): −0.2 pp [−0.7, +0.3] against the comparison at population level; Israel+Palestine minus Judaism +0.9 pp [0.2, 1.5].
- **No synchronized tag-teaming, no sweeps** (D7, P8): confirmed by the full coordination tier with calibrated nulls.

**Weakened**
- **"More topic articles than comparison articles gained" as a topic-wide claim.** The sealed-half replication (+3.6 pp [1.7, 5.6], mass v1) stays valid for its frame: Top, High and Mid articles of the original crawl against the original 23-project comparison. It does not generalise to the full population: across all 48,974 articles the M3 gap is +0.4 pp [−0.0, +0.9]. Say "in the core", never "the topic".
- **Reader exposure as a topic-wide figure (P3, D9).** 3.9% of articles / 15% of views describes the core crawl. Across the population, 4.8% vs 4.6% of views: no difference. Top grade 30.5% vs 19.1% (not significant).
- **Narrative residual 89% (P4).** Valid in the core crawl; at population level there is no DiD to decompose.
- **"Tight community of regulars" vs "campaign" (D7).** Now partly quantified: two small blocs beyond chance. They are consistent with regulars sharing watchlists and with off-wiki coordination alike; the data cannot tell these apart.

**Replaced**
- **Exploratory weighted figures** (AUDIT: +1.8 per 10k, +1.9 pp, 2.5% of articles, 13.7% of views, Judaism −0.3) are replaced on the page by M3 population estimates. The AUDIT combined estimate stays as the best estimate for the Top/High/Mid population only.
- **"No sign of synchronized tag-teaming" (picture sentence 5)** is replaced by the fuller network result above.
- **Picture sentences 1 and 3** should now read: (1) "...Israel and Palestine articles at the core of the subject took on more of the vocabulary of legal accusation and of 1948, while Judaism articles did not move; across all 49,000 articles in the four projects, the average change was no larger than in articles on other conflict regions." (3) "It is concentrated by importance: 10.3% of Top-importance topic articles gained critical terms in their lead against 4.4% for other conflict regions, Mid 1.5% vs 0.0%, while the Low-importance and ungraded long tail (80% of articles) did not differ."

---

## What changed in the previous update (mass2)

**Strengthened**
- **Established editors.** At full scale, topic pages are edited by more established accounts than comparison pages: 9.1% vs 17.2% of war-window edits came from accounts with under 500 edits (−8.2 pp [−9.4, −7.1] {−11.3, −1.6}). Both CIs agree. P8 moves from SUGGESTIVE to STRONG for this part.
- **Formal process grew on the core.** RfCs per article-year nearly tripled on topic pages while they fell on comparison pages, and they sit on a few pages (new P11).
- **Structural reframing is real at scale.** Framing categories were added to 7.2% of topic articles vs 2.2% of comparison articles (new P12). The pilot had found no category reframing; it was too small.
- **Vocabulary travels along links.** Linking to a core concept comes before the concept's vocabulary reaching the lead, +5.6 pp at the same edit volume (new P12). The pilot had called link diffusion modest.
- **The narrative residual replicated at full scale.** 89% of the post-war topic-vs-comparison lead change is in sentences that are not about recent events (P4).
- **Change came as added text,** now with mass2 edit sizes (P4, P7).
- **Battles, not courts, move the editing**, now with event timing at full scale. Legal and institutional events show no effect on term insertions in any window (new P10).

**Weakened**
- **Reader exposure.** The headline is now the mass2 figure: **3.9% of topic articles gained lead critical terms and they carry 15% of topic views** (comparison 1.5% and 5%). The deep-panel "15% of articles carry 46% of views" was a hand-picked-sample figure and is no longer a headline (P3, D9). The topic level is three times the comparison level, but the comparison group shows a similar tilt toward its most-read pages, and the project CI on the difference crosses zero.
- **Survival and the ratchet.** At scale, topic insertions do not survive worse than comparison insertions (30-day 47.3% vs 42.9%). The 36% vs 56% result holds only for the key battleground leads (D5, P7).
- **Concentration of the fighting.** "Four pages hold 68% of lead flips" is true inside the 25 key articles only. Across all 4,642 topic articles the top 4 pages hold 9% of flips (D6, P7).
- **"The first rush bounced, what stuck came in 2024."** Sharp on the deep panel (23% vs 54% kept for a week), much milder at scale (46% in 2023-H2 vs 53% in 2024-H1) (P1, P10).
- **Fewer newcomers than before the war.** The drop in accounts under a year old is small at scale (DiD −2.2 pp [−4.3, −0.3] {−4.8, +0.9}) and the project CI crosses zero (P8).
- **Timing of the wave.** At scale the insertion rate stayed high through all of 2024, not only the first half (P1).

**Withdrawn**
- **Study 2's N5 "1948 forced vs fled" result is withdrawn.** The measure scored 53% on a hand-coded precision check, under the 60% gate. Nothing in this synthesis or the storyline uses it. Study 2's N1 (indigeneity, 40%) and N6 (terror or massacre by perpetrator, 53%) are dropped for the same reason. N2 (ancient-land naming) passed at exactly 60% and is fragile; it is not used here either.
- **Blocked accounts over-represented in critical-term flips** (PILOT finding 2). At full scale there is no excess over the base rate: 13.7% of war-window topic insertions came from now-indef-blocked accounts against a base of 12.3% on the same pages (+1.4 pp [−2.8, +6.5] {−4.6, +5.4}); removals 11.3% vs 11.0%.
- **"Categories show no reframing"** (PILOT finding 10). Overturned at scale (P12).
- **"Protection does not predict change"** (PILOT finding 8), as worded. At scale protected topic pages did change more often at the same edit volume, but so did protected comparison pages. The ruling is now "protection marks the core; it is not shown to cause change" (P11).

---

## The picture in 5 sentences

1. Between 2021 and 2026, the Israel and Palestine articles at the core of English Wikipedia's coverage took on more of the vocabulary of legal accusation and of 1948 (genocide, ethnic cleansing, expulsion, occupation), while Judaism articles did not move; across all 48,974 articles in the four projects, the average change was no larger than in articles on other conflict regions (M3), and Wikipedia as a whole did not drift (RB).
2. The change came as one wave: critical-term insertions per 1,000 topic edits went from about 7 before the war to about 16 through 2024 and back to 5 or 6 in 2026, and military escalations brought editors in while court rulings and reports did not.
3. It is concentrated by importance: 10.3% of Top-importance topic articles gained critical terms in their lead against 4.4% for other conflict regions (+5.9 pp [0.9, 11.2]), Mid 1.5% vs 0.0%, while the Low-importance and ungraded long tail, 80% of articles, did not differ; in the core crawl the 3.9% of topic articles that gained carry 15% of topic reading (comparison: 1.5% and 5%).
4. It came as added text about older history and the land, 89% of it not about recent events, written by established editors on pages that also gained protection, RfCs, framing categories and links to core concepts such as the Nakba; a few high-traffic leads (Gaza genocide, Israel, Israeli apartheid, Nakba, Zionism) now state contested labels in Wikipedia's own voice.
5. Jewish history content was kept, lead sources shifted only slightly, other language editions mostly did not follow, two small blocs of long-standing accounts returned to the same articles more often than chance (14 linked pairs vs about 2 expected), but with no synchrony, no pasted wording and no clear alignment with either documented canvassing window, and blocked accounts did no more than their share; the data cannot tell us whether the new wording is accurate, what editors intended, or whether anyone coordinated off-wiki.

---

## Where the analysts overlap or disagree

Overlaps were merged into the patterns below. These are the real disagreements, with a ruling on each. D5, D6 and D9 were revised in this update; D13 and D14 are new.

| # | Disagreement | Ruling |
|---|---|---|
| D1 | **Attribution.** WWW12: more loaded words now come with attribution (mass, 21.3% to 25.0%). SSL2/SSL9: labels moved into Wikipedia's own voice. FINDINGS: "the tiers disagree, so there is no clear direction". | Both are true at different levels, and the mass result is better supported. Across 10k articles, with a comparison group, the hedged share rose in topic articles (0.213 to 0.250) and stayed flat in comparison (0.167 to 0.172). In the 332 deep-panel leads the hedged share rose to 0.43 by Jan 2024 and then fell to 0.26 by 2026, below its 2021 level of 0.31, while comparison leads rose from 0.10 to 0.20. But that lead series has only 61 to 93 mentions per quarter. The two system-level tests of "voice upgrades" both failed (holdout B4: DiD −0.04; coded K01: topic 6.7% vs comparison 10.0%). Say: "most new words came in attributed; in a few flagship leads the attribution was later removed." Do not say Wikipedia as a whole moved into its own voice. |
| D2 | **Timing.** WWW5: "first the edit storm, then the words". WWW5 itself and Q6: per article, median lag 0. HW2: readers came for a month, editors stayed 18 months. Holdout: timing lag n.s. | Per article, words and edits arrive together (median lag 0, n=66; holdout lag n.s.). Weekly series agree on both tiers: edits and insertions correlate most at lag 0 (deep r=0.517; mass2 leads r=0.569; differenced 0.214 and 0.202), with no lead or lag. The aggregate delay is a composition effect. Present this as "news first, reframing second, settling third", and say clearly that each article changed during its own busy period. Do not imply editors waited for readers to leave. |
| D3 | **Still moving or settled?** WWW1: plateau since Jan 2025. WWW9: flagship leads still being fought over. HW6: the fight is cooling. | Compatible, and mass2 confirms the ebb. Insertions per 1,000 topic edits fell from 16.0 (2024-H1) to 10.8, 8.2, then 5.1 and 5.9 in 2026, at or below the pre-war 5 to 8. Flips in 25 key leads fell from 129 in 2023-Q4 to 7 to 13 per quarter in 2026, but 7 final lock-ins still happened in 2026 (Israel's on 2026-09-04, Zionism's on 2026-08-27). "Cooling, with a few last decisions" covers both. |
| D4 | **How different is the topic from other conflicts?** HW1 (STRONG): at the same edit level, topic articles change 2 to 4x as often. FINDINGS: "similar in size to other war-affected topics". | Both hold, measured differently. Against the pooled comparison group the ratio is 2 to 4x. Against other live conflicts it is smaller: in the busiest fifth of each project, Palestine 57% and Israel 44%, against Ukraine 30%, Armenia 30% and Bosnia 27%. Israel/Palestine leads the league, but other live conflicts are in the same league, and Judaism (15%) sits with Greece and India. What is distinctive is less the size than where the change went (WWW10). |
| D5 | **Persistence.** HW5: "contested words get in by persistence". FINDINGS and TALKING_POINTS: "edit wars, not a ratchet". Holdout A8 did not replicate. | **Revised.** Two results, two scopes. In the key battleground leads, topic insertions survive less well than comparison insertions (36% vs 56% at 30 days), with 3.3 vs 1.4 failed tries before a term sticks. At full scale (M9, 4,226 exact events) the gap disappears: topic insertions survive 30 days 47.3% vs 42.9% in comparison (+4.5 pp [−2.5, +11.1] {−7.6, +20.7}); Kaplan-Meier 47.6% vs 43.0%; stuck terms needed 0.39 failed tries on average in topic vs 0.75 in comparison. So the ratchet picture belongs to the battlegrounds, not to the topic. Present persistence as a description of a few leads, never as the mechanism. |
| D6 | **Where the change lives: hot core or quiet pages?** WWW2: a hot core of a few hundred pages. SSL1: the most-read pages. HW7/HW8: the battlegrounds are 4 or 5 pages, and the change landed on low-revert pages. | **Revised.** Additions are concentrated in a few hundred articles, including high-traffic pages. Within the 25 key articles, Israel, Gaza war, Gaza genocide and Hamas hold 68% of lead flips; across all 4,642 topic articles the top 4 pages hold only 9% (M9), so flipping is common well beyond the famous four. Among busy articles, low-revert topic pages gained most often (28.5% vs 13%). A7 ("concentrated in the most-edited") did not replicate, so do not say "the busiest pages changed most". |
| D7 | **Sweeps.** HW10: multi-article sweeps are rarer on topic pages. Mass data: sweeps per 1,000 editors are 120 (topic) vs 70 (comparison). | The mass tier is better supported. Drop "sweeps are rarer on topic pages". Supportable: more recurring co-editing per edit (1.6 vs 0.56 pre-war; 0.72 vs 0.35 post-war), overlap among the top 150 editors rose (1.11 to 1.61x null), no sign of tight time-synchronized pairs. That describes a tight community of regulars, not evidence for or against a campaign. |
| D8 | **Jewish ties to the land.** SSL11: 'homeland' in first sentences 5 to 1. Holdout K11 (κ 0.74): Jewish belonging claims strengthened in 11 pairs, weakened in 6. B3: Jewish land names also rose (11 to 19). | K11 and B3 are better supported. Keep SSL11 as an ANECDOTE about a few flagship first sentences, some of them MOS:FIRST clean-ups. |
| D9 | **Gain rates and reader exposure differ by tier.** WWW2: 11.4% of mass topic articles gained (full text). HW3: 31 to 52% of deep-panel articles gained. SSL1: 15% of deep topic leads gained and carry 46% of topic views. M10: 3.9% of mass2 topic leads gained and carry 15% of views. | **Revised.** Use M10 as the headline. The deep panel was chosen to be long, curated, prominent articles, so it holds nearly all the giant pages (Israel, Benjamin Netanyahu, Palestine, Zionism) while leaving out the long tail of stubs, lists, villages and biographies that make up most of the 4,642 mass2 topic articles and much of their reading. Its denominator is small and top-heavy, so "share of views" inflates to 46%. Mass2 also counts 12 months of views summed over former titles, where the deep figure used views since 2021 on current titles. The deep figure still describes those 407 pages; it is not the topic. Always name the tier. |
| D10 | **Languages.** SSL4: English moved and others barely did. FINDINGS: English is within the range of the other 10 languages. | In full text, English is not an outlier. In leads, English is clearly positive (+0.24 per 1,000 words, p<0.001), but Portuguese is just as large (+0.27, p=0.004). Say "English and Portuguese leads moved; most others did not detectably". |
| D11 | **Colonial.** WWW3: colonial rose before the war. WWW11: colonial rises Wikipedia-wide, more in comparison leads. SSL6: Zionism now says "colonization". | Mixed. Deep topic leads +47% before, −20% after; mass topic leads −3% before, +54% after; quiet comparison leads +56% and +42%. Do not present "colonial" as the topic's signature word. Zionism's definition is an ANECDOTE. |
| D12 | **Small factual mismatches.** Zionism "colonization" first entry; 35 vs 25 stuck terms; Zionism 44 vs 105 flips. | Use 2024-06-05 for the first entry. 35 counts every final "stick" event; 25 is net new against 2021; use 25 in / 6 out for the key articles. Quote 44 in/out cycles and name the pattern. |
| D13 | **Pilot vs mass2.** The pilot (166 hand-picked articles) found blocked accounts over-represented in flips, no category reframing, modest link diffusion, and protection "not predicting" change. | **Mass2 wins on all four**, because it covers the whole topic with a comparison group. Blocked accounts: no excess (M1). Categories: real but small reframing (M6). Links: clear diffusion signal (M7). Protection: marks the core in both groups (M2). The pilot remains useful for its hand checks (EVAL 1.2) and the LiftWing result. |
| D14 | **Deep-panel events vs mass2 events.** EV2: legal events not followed by more lead insertions (60 leads). EV3: first rush bounced, 2024 stuck. EVM: same analysis on 4,642 topic leads. | Legal null confirmed at scale. Military escalations show a clearer insertion effect at scale (short window 1.34x, p=0.001; long window 1.17x, p=0.054) than on the deep panel (1.19x, p=0.086). The bounce-then-stick contrast is mostly a deep-panel feature (see P1, P10). |

---

## Headline patterns

### P1. The change came as one wave through 2024, and it is back to the pre-war rate in 2026
*Merges WWW1, WWW5, WWW8, HW2, HW12, HW6, EV3, EVM half-years. Holdout A9 and A10 replicate.*

- **Numbers.** Mass2 leads, critical-term insertions per 1,000 topic edits by half-year: about **7** (2021 to 2023-H1, range 5.3 to 7.7), **13.5** (2023-H2), **16.0** (2024-H1), **15.9** (2024-H2), 10.8 (2025-H1), 8.2 (2025-H2), **5.1 and 5.9** (2026). Insertions that lasted a week peaked in 2024-H2 (115, against 24 to 32 per half-year before the war). Comparison-article insertions fell over the same period (about 107 to 187 per half-year before the war, 71 to 101 after). Deep panel: net critical terms per 100 topic articles per quarter about 7 before the war, 40 (2024-Q1) and 46 (2024-Q2), about 4 in 2025-26. Mass v1 pooled rate 13.3 to 16.0 per 10k words by Jan 2025, 16.1 in Oct 2026. Pageviews of key articles were 22x normal in Oct 2023 and back to 2 to 3x within three months; edits stayed at 1.7 to 2.5x for 15 months.
- **Confidence.** STRONG for the wave and the return to baseline (two tiers agree). SUGGESTIVE for "core first, periphery a year later" (WWW8; the Judaism periphery has only 38 added terms). SUGGESTIVE for "the first rush bounced": on the deep panel only 23% of 2023-H2 insertions lasted a week against 54% in 2024-H1 (p=0.0007), but at scale the shares are 46% and 53%.
- **Best chart.** Bars of insertions per 1,000 edits by half-year, topic vs comparison, with the week-durable share as a line; mark 7 Oct 2023. `events/chart_data/mass2_01_weekly_timeline_events.json` (aggregate to half-years) with `data/event_timing_mass2.json` → `half_years`. Deep-panel back-up: `when_where_what/chart_data/01_timeline_quarterly.json`.
- **Example.** List of genocides went from 55 to 154 critical hits between the Apr and Jul 2024 snapshots, when the Gaza entry was written. Zionism's editing: 10.9 edits per 100k views before the war, 4.0 in the first six months, 42.8 after.
- **So what.** This was a time-limited reframing, not a continuing slide. "Wikipedia keeps getting more critical" is not supported: by 2026 the rate of new insertions is at or below the pre-war rate. The size of the news spike does not predict the direction of change (Spearman 0.01 across 22 articles). Attention brought editors; it did not set the direction.

### P2. A few hundred pages carry the change; most topic articles did not change, and Judaism did not move
*Merges WWW2, HW7 (in part), holdout A1, A5, A5b, B1, M9 entries and exits.*

- **Numbers.** Mass v1: of 4,009 unique topic articles, **85.1% had exactly the same count**, and 456 gained. The top **40 articles (1%) supplied 38%** of added terms. Israel and Palestine projects are 61% of articles and supplied 84% of additions; Judaism is 28% of articles and supplied 7%. Replicated DiD: **+3.6 pp** [1.7, 5.6]; Israel+Palestine minus Judaism +5.6 pp; Judaism vs comparison −0.1 pp [−2.3, 2.3], formally equivalent to zero. Mass2 leads, 2021 to now: 223 article-terms entered topic leads and 61 left; comparison 125 in, 73 out.
- **Confidence.** STRONG (10k articles, comparison group, sealed-half replication, mass2 consistent).
- **Best chart.** Lorenz curve, four lines (topic pre/post, comparison pre/post). `when_where_what/chart_data/03_concentration.json`. Label the 1% and 5% points.
- **Example.** Biggest gainers, Jul 2023 to Nov 2026: Gaza Strip +25, Benjamin Netanyahu +22, Criticism of Israel +21, West Bank +18, Deir Yassin massacre +16.
- **So what.** "Wikipedia shifted on Israel" is really "a few hundred Israel and Palestine pages shifted". Articles on Jews, Judaism and religion are where they were. Monitoring can be small and targeted.

### P3. The change sits where readers look: leads, first sentences, and the most-read pages
*Merges WWW6, SSL1, SSL7, SSL3, M10. Holdout A4 and A6 replicate.*

- **Numbers.** Mass v1: critical rate in leads **+35%** (8.18 to 11.03 per 10k words) against **+13.5%** in bodies; comparison leads +5.4%. First sentences with a critical term: 1.48% to **2.08%** (comparison 0.63% to 0.66%). Mass2 exposure, last 12 months, former titles included: **3.9% of topic articles gained lead critical terms and carry 15.0% [9.5, 21.3] {2.7, 25.2} of topic views** (279 million views); comparison **1.5% of articles, 5.0%** [2.9, 7.5] {2.4, 8.4}. Views meeting any changed lead: topic 17.2%, comparison 8.2%. Relevant subset: topic 8.3% of articles, 27.6% of views; comparison 3.8% and 8.6%. Views-share minus article-share, DiD +7.5 pp [+1.6, +14.3] {−2.9, +16.8}.
- **Confidence.** STRONG for lead amplification and first sentences. SUGGESTIVE for the exposure gap: the topic level (15%) is three times the comparison level (5%) on both CIs, but the extra tilt toward read pages is not established, because the article CI on the DiD excludes zero and the project CI does not. A handful of very large pages drive the views share. SUGGESTIVE for SSL3 ("87% of views came before the wording settled").
- **Best chart.** Paired bars, share of articles vs share of views, topic and comparison, all and relevant subsets. `mass2/chart_data/10_pageviews_exposure.json`. Back-up: `when_where_what/chart_data/09_lead_vs_body.json`.
- **Example.** Benjamin Netanyahu, 7.0M views in the last 12 months, lead critical terms 1 to 4. 2026: "Netanyahu's government has been orchestrating the Gaza genocide, culminating in the South Africa v. Israel case before the International Court of Justice (ICJ) in December 2023." Israel (4.6M views) 5 to 8; Palestine (2.4M) 2 to 5; Zionism (1.8M) 1 to 5; Hamas (1.3M) 0 to 3.
- **So what.** This is the twist, at its honest size. Count articles and the change is small (4%), and the pre-registered average test was null. Count readers and it is three times bigger (15%), and three times the comparison group's. It is not "most topic reading": 83% of topic views land on leads that did not change. Changed pages being read pages is partly how Wikipedia works everywhere (comparison gainers also punch above their article share). Search snippets and AI answers draw on exactly these lead sentences. The earlier deep-panel figure (15% of articles, 46% of views) describes a hand-picked set of prominent pages and should not be quoted as the topic figure (D9).

### P4. The story moved back to 1948 and to the land, as added text, not as war news
*Merges WWW4, SSL6, SSL10, SSL11 (as anecdote), event filter, M12, M8, holdout B2, B3.*

- **Numbers.** Mass2 narrative residual (9,177 leads, all three snapshots): post-war DiD in lead critical hits per 10k words, unfiltered **+2.22** [+1.37, +3.12] {−0.47, +4.78}, residual after removing sentences about 2022+ events **+1.98** [+1.10, +2.82] {−0.40, +4.29}, event sentences +0.24. **The residual is 89% of the change.** Relevant subset residual +4.35 [+2.20, +6.69] {+0.15, +5.98}. Pre-war residual DiD +0.14, null. The frozen holdout script on the earlier crawl gave +2.06 of +2.34 (88%), and 11 of 12 rows match. Deep panel: +8.4 of +9.3 per 10k words in older-history sentences. History-anchored vs event-anchored added sentences 18 vs 5 (B2, replicates). Added text (M8): topic leads that gained critical terms grew in 78.2% of cases (median +33.5 words) vs 55.8% of other topic leads; the removed/added byte ratio did not change (0.627 to 0.626; DiD −0.014, n.s.); new war-window lead events in topic were 665 insertions vs 392 removals. Place articles gaining per year 1.6% to 4.6% (deep); 35 of 60 gaining place articles gained Nakba/expulsion wording.
- **Confidence.** STRONG for the history-anchored residual (replicated on two tiers and the holdout), with one caution: on the full set the project CI crosses zero, while on the relevant subset both CIs exclude zero. STRONG for "added text". SUGGESTIVE for the article-type breakdown (classifier about 70% accurate) and for naming.
- **Best chart.** Stacked bar, residual plus event part, per group and window. `mass2/chart_data/12_narrative_residual.json`. Pair with a then/now card (`then_vs_now` in `story_sources_langs/cards.json`) and the article-type bars `when_where_what/chart_data/05_geography_type_importance.json`.
- **Example.** Nakba, 2021: "The Nakba, also known as the Palestinian Catastrophe, was the destruction of Palestinian society and homeland in 1948, and the permanent displacement of a majority of the Palestinian Arabs." 2026: "The Nakba ... is the ethnic cleansing of Palestinian Arabs by Zionists through their violent displacement and dispossession of land, property, and belongings ..."
- **So what.** The war did not mainly produce war coverage. It sent editors back to retell 1897 to 1948 and to rename the land, and they did it by adding sentences, not by deleting others. Jewish history content was kept (B1: ρ = −0.03). No claim here rests on study 2's "forced vs fled" measure, which was withdrawn.

### P5. The new words are genocide and expulsion; apartheid is an older layer; colonial is rising everywhere; terrorism thinned out
*Merges WWW3, WWW7, WWW11, SSL12.*

- **Numbers.** After July 2023, topic rates (deep / mass v1): **genocide +46% / +23%** (comparison −1% / +1%), ethnic cleansing +37% / +29%, Nakba/expulsion +22% / +17%. Apartheid rose **+39%** in 2021 to 2023 and only +7% after. Terrorism vocabulary **−12% / −9%** in topic text and −24% / −19% in leads (comparison flat); Hamas alone lost 47 mentions.
- **Confidence.** STRONG for genocide against comparison. SUGGESTIVE for the rest; the Nakba lexicon is contaminated (data note 2), the terrorism fall is a few articles, and colonial is mixed (D11).
- **Best chart.** Dumbbell per word family. `when_where_what/chart_data/07_vocabulary_families.json`.
- **Example.** Hamas, 2021: "a Palestinian Sunni-Islamic fundamentalist but pragmatic, militant, and nationalist organization." 2026: "a Sunni Islamist Palestinian nationalist political organisation with a military wing known as the al-Qassam Brigades." The terrorist designations are still in the lead, lower down.
- **So what.** The post-war vocabulary is the vocabulary of courts and of 1948. Arguments that "apartheid entered Wikipedia after 7 October" are aimed at the wrong period. Changes also ran the other way: 'by Zionist militias' was cut from the 1948 expulsion first sentence, Israeli settlements now adds "but Israel disputes this", antisemitism appears in 54 topic leads instead of 37. The picture is lopsided, not one-sided.

### P6. Other conflicts and other Wikipedias did not do this in the same way
*Merges HW1, HW3, WWW10, WWW11, SSL4, SSL5, EV4.*

- **Numbers.** At equal edit activity, topic articles gained **2 to 4x** as often as the pooled comparison (busiest tenth: 41% vs 19%). In the busiest fifth: Palestine 57%, Israel 44%, against **Ukraine 30%, Armenia 30%**, Bosnia 27%; Judaism 15%. English leads +0.24 per 1,000 words (p<0.001), Portuguese +0.27, the other 9 languages near zero (mean +0.06). Other wars move their own pages: comparison events were followed by 1.36x edits on the shocked comparison pages (p=0.005) and not on topic pages (0.90x).
- **Confidence.** STRONG for topic vs pooled comparison. SUGGESTIVE for topic vs other live conflicts (D4) and for languages (D10).
- **Best chart.** Dot plot, share gaining by edit-activity decile. `how_who/chart_data/activity_decile_gain.json`; then `how_who/chart_data/busiest_by_project.json` and `story_sources_langs/chart_data/languages_lead_did.json`.
- **Example.** Tigray war went 0, 1, 8, 12, 19, 21 critical hits over its first six quarters and then stayed flat, and the vocabulary did not spread to Ethiopian history or place pages.
- **So what.** "Vocabulary follows wars" is normal Wikipedia behaviour. Two things set this topic apart: a given amount of editing turned into change more often, and the change left the war articles for history, places and people.

### P7. Quiet pages absorbed the change; the famous edit wars are a few pages and are cooling
*Merges HW4 to HW8, WWW9, WWW13, M9. Holdout revert moderation −3.9 [−6.8, −0.5] (exploratory). A8 did not replicate.*

- **Numbers.** Among busy mass-tier articles, **low-revert topic pages gained 28.5%** of the time, mid and high 13.9% and 13.1% (comparison 10.5%, 10.3%, 6.5%). High-talk topic pages gained 60%, low-talk 22%. Inside the 25 key articles, **Israel, Gaza war, Gaza genocide and Hamas hold 68%** of lead flips; across all topic articles the top 4 hold **9%**. Key-lead flips per quarter: 129 in 2023-Q4, 7 to 13 in 2026. Survival at scale: topic insertions 47.3% at 30 days vs comparison 42.9% (n.s.); in the key leads 36% vs 56%. Topic archetypes at scale: single step 243 article-term pairs, tried and reverted 224, back-and-forth 133, tug-of-war 71.
- **Confidence.** STRONG for "low-revert pages changed more". SUGGESTIVE for talk-page deliberation and for cooling. The battleground survival gap is SUGGESTIVE and limited to the key leads. ANECDOTE for single-article histories.
- **Best chart.** Grouped bars by revert tercile. `how_who/chart_data/revert_tercile_gain.json`. For survival at both scales: `mass2/chart_data/09_lead_term_events.json` (it carries the ratchet reference).
- **Example.** Gaza genocide lead, eight one-way steps in 21 months, from "Allegations have been made that the 2023 Israel–Hamas war constituted a genocide against the Palestinians" (2024-01-01) to "The Gaza genocide is the ongoing, intentional, and systematic destruction of the Palestinian people in the Gaza Strip carried out by Israel during the Gaza war" (2025-10-05, "per talk"). Against that, Israel's lead: 'apartheid' entered and left 39 times, each state lasting a median of about 12 hours.
- **So what.** The edit wars in the news are real, but they are a few pages, and their rules (low survival, many failed tries) do not describe the topic as a whole. Most topic-specific change landed where nobody reverted it, often after discussion. Anyone who monitors only edit wars misses most of it.

### P8. It was written by established editors, not a flood of newcomers or blocked accounts, and the timing does not look scheduled
*Merges HW9, HW10, HW11, FINDINGS co-editing, M1, PILOT 3.1.*

- **Numbers.** Mass2, war window: edits by accounts with under 500 edits **9.1% topic vs 17.2% comparison** (−8.2 pp [−9.4, −7.1] {−11.3, −1.6}); relevant subset −11.3 pp [−13.0, −9.5] {−13.7, +0.5}. Anonymous edits 10.6% vs 16.1%. Accounts under a year old: topic 19.0% (pre-war) to 15.9%, comparison 23.9% to 23.0% (DiD −2.2 pp [−4.3, −0.3] {−4.8, +0.9}). Now-indef-blocked accounts: 13.7% of war-window topic insertions and 11.3% of removals, against a base of 12.3% and 11.0% on the same pages; excess +1.4 pp [−2.8, +6.5] and +0.2 pp [−4.1, +4.4]. Deep panel: edits by accounts new that quarter 41% in 2023-Q4, then 12 to 17% from late 2024. Eight editors changed first sentences on 3 or more key articles. Overlap among the 150 most active topic editors rose from 1.11x to 1.61x a popularity null. Zero editor pairs edited within 30 minutes of each other on 5 or more articles.
- **Confidence.** STRONG for "more established accounts than comparison" (both CIs agree on the full set). SUGGESTIVE for "fewer newcomers than before the war" (project CI crosses zero). STRONG for "no blocked-account excess at scale" as a null; it overturns the pilot. SUGGESTIVE for the co-editing signals.
- **Best chart.** Grouped bars by window, low-edit-count share, topic vs comparison, with the adders/removers blocked table. `mass2/chart_data/01_who_edits.json`, `mass2/chart_data/01_adders_removers_blocked.json`.
- **Example.** Israeli apartheid, 2024-08-05, a topic regular's edit summary: "taking the first step in summarizing the body in the lede to reflect the article's new scope".
- **So what.** "Brigading by new accounts" is not what the data show, and neither is "blocked sockpuppets wrote it": flips by now-blocked accounts match their share of all editing on the same pages, in both directions. Before the war, a few blocked accounts were busy on both sides (top 3 made 13 of 36 blocked insertions; removals by blocked accounts 27.2% vs 20.2% base). The text was written by an experienced, overlapping community, which fits the topic's extended-confirmed rules. These signals cannot detect off-wiki coordination or sockpuppets that were never caught, and block status is as of collection, not at the time of the edit.

### P9. The words changed more than the sources and the reuse surfaces did, and most new words arrived attributed
*Merges SSL8, SSL13, SSL2, SSL9, WWW12, holdout B4 and K01, M4, M5, M11, PILOT 3.4 and 3.10.*

- **Numbers.** Mass2 lead citations (4,468 topic and 5,510 comparison leads): scholarly 43.3% to 48.0% in topic and 49.5% to 55.2% in comparison (DiD −1.0 pp, n.s.); Arab and Palestinian press 0.7% to 1.1% (DiD +0.28 pp [+0.09, +0.46] {−0.13, +0.74}); pro-Israel advocacy 1.0% to 0.8% (DiD −0.20 pp, both CIs exclude zero); Israeli press 6.4% to 5.8% (DiD −0.57 pp [−0.89, −0.23]); rights groups and UN flat at 1.8%. Mass v1 all citations: Arab and pro-Palestinian outlets 0.63% to 1.68%. Short descriptions changed in 55.7% of topic articles whose lead count changed vs 32.5% of the rest; in comparison 63.2% vs 43.8%; DiD +3.8 pp [−6.5, +15.0], n.s. Topic short descriptions containing a critical term: 26 then, 24 now. Attribution share of loaded terms, mass v1: topic 21% to 25%, comparison 17% flat. Atrocity set (M11): 'genocide' stated in Wikipedia's voice in 4 of 11 leads in 2023 and 9 of 11 now, including new pages (Tigray genocide, Masalit genocide, Darfur 2023).
- **Confidence.** STRONG for "sources barely moved" and "descriptions co-move everywhere". SUGGESTIVE for the small press shifts (the Arab-press DiD loses its project CI). SUGGESTIVE for attribution (D1). ANECDOTE for voice upgrades and the atrocity set.
- **Best chart.** Small multiples, lead citation share by class. `mass2/chart_data/05_lead_citation_classes.json`. Second: `mass2/chart_data/04_sd_wikidata.json` (paired bars plus a quote table).
- **Example.** Second Intifada short description: "2000–2005 Palestinian uprising against Israel" to "2000–2005 Palestinian uprising against Israeli occupation" (348k views). Hebron, Wikidata: "city in the West Bank" to "Palestian city in the occupied West Bank". Israel lead, 2026: "After the Hamas-led October 7 attacks, Israel began committing genocide against Palestinians in Gaza. Israel and its allies, including the United States, deny that Israel's actions constitute genocide."
- **So what.** The reframing did not come from a flood of partisan sources; lead sources moved by fractions of a point. Short descriptions moving with the lead is ordinary maintenance in both groups; what matters are the few high-traffic descriptions that now carry a framing term. Stating 'genocide' in Wikipedia's voice is common in the atrocity set, so Gaza differs in speed and reach (title, short description, infobox, categories), not in the label itself.

### P10. Battles bring editors; courts and reports do not; no single event explains the wave
*New. Merges EV1 to EV8 and EVM.*

- **Numbers.** Deep panel, 3 weeks after vs 6 weeks before, against 2,000 random dates: after the 24 military escalations topic edits rose 17% (p=0.001) and pageviews 28% (p=0.007); after the 25 legal and institutional events (ICJ, ICC, UN votes, rights reports, recognitions) edits were 0.94x and pageviews 0.73x; ceasefires 0.97x. Mass2 leads (4,642 topic articles): after military escalations, critical-term insertions 1.34x (p=0.001) in the short window and **1.17x (p=0.054)** over 13 weeks; legal and institutional events **no effect** (1.01x short, 0.96x long). Events that left the clearest mark on insertions that lasted a week, each weak on its own: Shireen Abu Akleh killing (May 2022) 3.2x, October 7 2.6x, **the Nagorno-Karabakh offensive 2.6x (a placebo)**, US strikes on Iran (Jun 2025) 2.3x, Rafah offensive 2.2x. Each new war moved editing less: 3.0x after October 7, 2.0x after Nasrallah's killing, 1.06x after the June 2025 Iran strikes.
- **Confidence.** STRONG for "military escalations bring more edits; legal events do not" (deep panel, survives isolation and placebo checks). STRONG as a null for "legal rulings triggered the vocabulary" (two tiers). SUGGESTIVE for the military effect on insertions (42 tests per table; the long window misses 0.05). ANECDOTE for single events: a placebo ranks third, so the top list is mostly noise.
- **Best chart.** Heatmap, event type by outcome, cell = excess, shaded by p. `events/chart_data/mass2_02_type_by_outcome.json`. Second: ranked bars of events that left a mark, placebo highlighted, `events/chart_data/mass2_04_left_a_mark.json`.
- **Example.** After the ICJ provisional measures order (26 Jan 2024), topic edits were flat (482 to 466 a week) and deep-panel lead insertions fell from 2.8 to 1.0 a week. Where institutions do leave a mark is narrow and fast: the Gaza genocide first sentence named Amnesty, HRW, B'Tselem, the genocide scholars' association and the UN Commission of Inquiry within days of each finding, then dropped the attribution list for Wikipedia's own voice on 5 Oct 2025 (EV6, ANECDOTE).
- **So what.** Do not write "after the ICJ ruling, Wikipedia changed". The shooting war supplies editors and attention; once there, they work on old contested wording. Institutional findings enter as sources in a few articles, not as triggers of a wave.

### P11. Process grew on the core: protection tripled and RfCs nearly tripled, on a few pages
*New. Merges M2, M3, PILOT 3.2 and 3.7.*

- **Numbers.** EC edit protection, topic: **10.9% (2021), 11.5% (Jul 2023), 31.1% (now)**; comparison 0.7%, 1.5%, 5.0%. Contentious-topic notice on the talk page now: topic 33.6%, comparison 7.9%. At the same post-2023 edit volume, topic pages EC-protected in Jul 2023 gained lead critical terms +8.6 pp [+6.2, +11.3] {+3.6, +9.9} more often than unprotected ones; comparison +4.5 pp [+1.6, +9.3] {−0.1, +9.5}; the difference between the two, +4.2 pp [−1.0, +8.1], is not distinguishable from zero. RfCs: topic **0.29 to 0.79 per 100 articles a year** (33 in the pre-war window, 122 after), comparison 0.76 to 0.59 (DiD per article-year +0.007 [+0.002, +0.012] {+0.002, +0.013}). Requested moves: topic 97 to 208, comparison 256 to 239. Post-war topic RfCs sit on 51 of 4,642 pages, and the top 5 hold 48%: Gaza genocide 21, October 7 attacks 13, Zionism 13, Hamas 8.
- **Confidence.** STRONG for the rise in protection and RfCs (both CIs agree on RfCs). STRONG for "protection marks the core". Protection as a cause of change: not shown. RfC and RM outcomes: ANECDOTE (51 of 122 RfCs closed; RM results known for 50 of 208).
- **Best chart.** Line of EC share by date, topic vs comparison, plus a Pareto of RfCs by page. `mass2/chart_data/02_protection_ct.json`, `mass2/chart_data/03_rfc_rm.json`.
- **Example.** Gaza genocide: 21 RfCs and 11 requested moves after the war, including the 2024-07-03 move from "Allegations of genocide in the 2023 Israeli attack on Gaza". For scale, Russo-Ukrainian war (2022–present): 13 RfCs and 6 moves.
- **So what.** Before the war, topic pages used RfCs less often per article than comparison pages; after it, they used them nearly three times as often as before, and more often than comparison pages. That fits the battlegrounds being settled by formal process rather than by attrition, but we have not yet aligned RfC closes with lock-in dates. Protection goes where the core pages are, in both groups; it does not by itself explain who wrote what.

### P12. The reframing reached the structure: categories and links, and links come first
*New. Merges M6, M7, PILOT 3.3 and 3.6.*

- **Numbers.** Framing categories (genocide, colonial, apartheid, occupation, massacre, terror, Zionism, antisemitism), Jul 2023 to now: added to **7.2% of topic articles vs 2.2% of comparison** (+4.95 pp [+4.17, +5.80] {+1.18, +8.55}); per 100 articles 10.8 added and 5.6 removed in topic, 4.2 and 2.7 in comparison. Most added topic categories: **1948 Palestinian expulsion and flight** (16), **Zionist political violence** (11), **Israeli massacres of Palestinians** (10), **Israeli apartheid** (8), Zionists from Ottoman Palestine (7), Nakba (6). Infobox fields gaining a critical term: 0.7% vs 0.3% (+0.40 pp [+0.12, +0.69] {−0.27, +0.93}). Concept links: topic articles linking to Gaza genocide 0, 0, 69; to Nakba/1948 114, 127, 223; to Israeli apartheid 18, 29, 52. Where a concept's term was absent from the lead in Jul 2023, articles already linking to it picked up the term in 7.9% of 784 pairs vs 0.5% of 25,672 unlinked pairs; within edit-volume quartiles **+5.6 pp [+4.1, +7.2] {+1.6, +9.2}**; comparison +1.65 pp; DiD +3.95 pp [+1.44, +6.15]. Where the link was added after Jul 2023, 22.5% now have the term (n=311).
- **Confidence.** STRONG for the category rise and for link-then-term (both CIs agree on the full set). SUGGESTIVE for infobox changes (project CI crosses zero) and for the relevant-subset link result ({−0.48, +11.09}). Direction of categories: the regex is direction-blind, and terrorist-designation and massacres-of-Jews categories count too, but the most-added list leans one way.
- **Best chart.** Dot plot per 100 articles with a top-categories table, `mass2/chart_data/06_categories_infobox_seealso.json`; bars of term pick-up, linked vs not, `mass2/chart_data/07_concept_links.json`.
- **Example.** Gaza genocide now sits in "21st-century genocides", "Genocide of indigenous peoples in Asia" and "Incitement to genocide of Palestinians" (PILOT). The Nakba gained an infobox whose type field begins "Genocide, ethnic cleansing, forced displacement, dispossession, mass killing, settler colonialism".
- **So what.** The new framing is not only in sentences. It is in the category tree and the link graph, which drive navigation, related-article lists and machine reuse. Links to a core article tend to come before its vocabulary reaches a lead, so new links to Nakba, Gaza genocide or Israeli apartheid are an early signal for monitoring. The category "1948 Palestinian expulsion and flight" names both expulsion and flight; it says nothing about which one, and should not be read as support for the withdrawn N5 result.

---

## What we can conclude

Said at the right strength.

**We can say (strong):**
- After October 2023, more English Wikipedia articles on Israel and Palestine gained critical vocabulary than comparison articles did. It replicated on a sealed half of the data (+3.6 pp).
- The change is concentrated in Israel and Palestine projects, in leads and first sentences, and in a few hundred pages, including some of the most-read.
- Articles on Judaism did not change (formally equivalent to zero).
- It came as a wave through 2024, and by 2026 the rate of new insertions is back at or below the pre-war rate.
- It came as added text, about 89% of it not about recent events. Jewish history content was kept.
- Military escalations brought more editing; legal and institutional events did not, and they did not trigger the vocabulary change.
- Topic pages are edited by more established accounts than comparison pages, and now-blocked accounts did not make more than their share of critical-term flips.
- Protection, contentious-topic notices and RfCs all grew on topic pages, and RfCs sit on a few pages.
- Framing categories were added three times as often as in comparison articles, and linking to a core concept tends to precede its vocabulary reaching the lead.
- Lead sources and short descriptions behaved much like comparison articles.
- Pages with few reverts changed more than contested pages.

**We can say (suggestive):**
- Topic pages that gained lead terms carry 15% of topic reading, three times the comparison share, but the extra tilt toward read pages is not robust to resampling projects.
- Editing turned into change more often here than in other live conflicts, and the change spread beyond war articles.
- English (and Portuguese) leads moved; most other language editions did not detectably.
- Fewer newcomers than before the war (a small drop; project CI crosses zero).
- On the battleground leads, insertions survive less well and need more tries than in comparison leads; across the topic as a whole they do not.
- New labels mostly came in attributed. A few flagship leads later dropped the attribution.
- Military escalations may also bring more term insertions (long-window p=0.054).

**We cannot conclude:**
- **Truth or accuracy.** Counting words measures emphasis. "Genocide" can appear more because a court case exists.
- **Intent.** We cannot see why editors wrote what they wrote.
- **Coordination.** We found no synchronized tag-teaming and no blocked-account excess, but we cannot detect or rule out off-wiki coordination or undetected sockpuppets.
- **That nothing happened.** The pre-registered deep-panel average test was null and underpowered for leads.
- **Who a word is aimed at.** A 'genocide' or 'expulsion' hit can be about Jews, Palestinians or others (data note 2).
- **How 1948 departures are described (forced vs fled).** The measure failed its precision check and the result is withdrawn.
- **Causes.** Protection, RfCs, links and editor composition all fit the pattern. We have not separated them, and protection is shown only to mark the core.
- **Effect on readers.** We know what text was live when people visited, not what they took from it.

---

## What someone could do with this

**Readers**
- Read the lead of a contested article as the current state of a negotiation. Open "View history" and the talk page before quoting a first sentence.
- Check whether a loaded label is attributed ("according to", "X state that") or in Wikipedia's voice. The difference is often a single recent edit.
- For contested history, read the body. The body keeps the competing views even when the first sentence does not.

**Wikipedia editors and the community**
- Audit the low-revert pages in the Israel and Palestine projects (villages, places, biographies), not only the battlegrounds. That is where most of the uncontested change landed.
- Review framing categories as carefully as lead wording. They are added three times as often here as elsewhere and are watched less.
- Make voice changes visible. A move from attributed claim to Wikipedia's voice on a high-traffic lead could get a talk-page note or an RfC by default, as page moves already do.
- Compare like with like. Apply the same voice standard to Gaza, Uyghur, Rohingya, Tigray and Sudan articles, and document where they differ and why.

**Journalists and researchers**
- Date claims properly. The vocabulary wave was in 2024, apartheid language came before the war, and no court ruling or report lines up with a jump.
- Weight by pageviews, and say which sample you weighted. At full scale it is 4% of articles and 15% of reading; a hand-picked sample of prominent pages will give much larger shares.
- Report a comparison group, and if you cluster by WikiProject, report how few clusters there are.
- Do not cite study 2's "forced vs fled", indigeneity or perpetrator-of-terror measures.
- Go to talk archives and RfC closes. Edit summaries rarely say why (7% cite talk or consensus).

**Platforms that reuse Wikipedia (search, AI assistants, knowledge panels)**
- Treat the first sentence of a contested-topic article as volatile. Israel's lead wording settled only on 2026-09-04.
- Carry attribution through. If the source sentence says "X state that", the snippet or answer should too.
- Snapshot carefully and record the revision ID used.
- Monitor the reuse surfaces: short description, Wikidata description, first sentence, categories.

**The owner's own monitoring**
- **"Watch the hot core."** About 50 articles chosen by pageviews × lead changes, drawn from the roughly 175 topic articles whose lead gained terms (together 15% of topic views). Start from Israel, Benjamin Netanyahu, Gaza Strip, Israeli–Palestinian conflict, Zionism, Jerusalem, Jews, Gaza war, Palestine, Israel Defense Forces, Hamas, Nakba, Gaza genocide, Israeli apartheid, West Bank.
- Weekly: diff the first sentence and lead; record term presence, voice level, short description and Wikidata description. Alert on a voice-level change, a new term that survives 7 days, or a short-description change.
- Monthly: new links to the core concepts (Nakba/1948, Gaza genocide, Israeli apartheid, settler colonialism) and new framing categories across the topic. Links come before lead vocabulary.
- Quarterly: rerun the mass2 insertion rate per 1,000 edits with the comparison group and the Judaism equivalence test, so "back to baseline" stays current.
- Keep a matched comparison watchlist (Ukraine, Armenia, Uyghur, Sudan, Tigray) so every alert has a baseline.

---

## Open questions, ranked

Updated with mass2, the pilot and event timing. Answered questions are listed under the table.

| Rank | Question | Value | Feasibility | Status |
|---|---|---|---|---|
| 1 | **Do formal processes settle the battlegrounds?** Align RfC closes and RM outcomes with lock-in dates on the key leads; do title moves come before de-hedging? | High: tells "governed decision" from "persistence wins" | Medium: better close parsing; dates are now kept | Counts done (P11); outcomes parsed for under half; alignment not done |
| 2 | **Is the Gaza voice upgrade special?** Timing and reach of the stated label across the atrocity set, and across languages | Very high | High | Partly answered: 9 of 11 atrocity leads now stated (P9). Open: speed, reach and language voice |
| 3 | **Who adds and who removes, by home topic area?** Do the same established editors work across the topic and across languages? | Very high | Medium; cross-wiki needs an ethics decision | Account age and block status answered (P8). Contribution-topic part open. Needs one fixed salt |
| 4 | **Does the link signal hold as a cause?** Full link-graph history and clickstream: do reader paths now route into the reframed articles? | High | Medium-low: pagelinks dumps, clickstream | Link-then-term shown (P12). Outlinks of core articles and reader paths open |
| 5 | **Is there a Wikipedia-wide drift?** A random-article baseline for 'colonial', 'indigenous' and the critical lexicon | High | Medium: about 15k requests | Open. Comparison insertions fell after 2023, which makes this more pressing |
| 6 | **Which sources sit behind the new lead sentences?** Refs attached to added sentences; per-outlet check (ADL, Al Jazeera) | Medium-high | Medium | Domains now stored; class shifts small (P9). Sentence-level refs open |
| 7 | **Was there a village sweep?** Template-like Nakba wording in Palestinian village articles | Medium | High: about 800 requests | Open |
| 8 | **Do other languages follow English with a lag?** | Medium | Low: about 5k requests | Open |
| 9 | **Why are pre-war blocked accounts busier in removals?** 27.2% of pre-war topic removals vs a 20.2% base | Low-medium | Medium: needs block reasons | Open; time at risk explains much of the pre-war base |

Answered and not ranked: protection (P11: marks the core, not shown to cause change); reuse surfaces (P9: co-movement is ordinary maintenance); revert-risk fairness (PILOT 3.9: no asymmetry between insertions and removals, AUC 0.75); readers driving it (P10 and HW12: attention brings editors, not direction); legal triggers (P10: no); talk volume (P7); position in the lead (P3).

---

## Data-quality notes to fix

1. **Duplicate redirect rows.** Fixed in mass2 (deduplicated by resolved page). Mass v1, FINDINGS and holdout figures predate the fix and may be slightly inflated; mass2 results agree with them in sign and rough size.
2. **The Nakba/expulsion lexicon catches Jewish expulsions.** 76 of 410 net added hits are in Judaism and Jewish-history articles (Edict of Expulsion +20). In mass2 event windows, "History of the Jews in England" counts as a Nakba/expulsion insertion. Fix: split the lexicon, or require a 1948/Palestinian co-term.
3. **Pageviews by current title.** Fixed in mass2: former titles hold 4.7% of topic views, and counting them moves the gainers' all-period view share only from 16.5% to 17.0%. The deep-panel exposure figures still use current titles.
4. **Project CI is coarse.** The topic side has 4 WikiProjects, so the project bootstrap resamples among very few clusters. Its intervals are wide and unstable at the edges. Report both CIs; do not treat a project CI that crosses zero as a refutation, nor an article CI alone as settled.
5. **Mass2 card wording.** M10's "so what" says "most topic reading now lands on leads that changed". The data say 15% (17.2% for any change). Fix the card before sharing.
6. **Study 2 lexicon precision.** N1 (40%), N5 (53%) and N6 (53%) failed the 60% gate and are dropped; N5's "1948 forced vs fled" result is withdrawn. N2 passed at exactly 60% and should be re-checked on untruncated sentences before any use. N5's errors were mostly mixed sentences ("fled or were expelled") and title matches ("1948 Palestinian expulsion and flight").
7. **Title-keyword article-type classifier at about 70% accuracy.** Fix with Wikidata P31 and hand-check 200.
8. **Top-decile concentration is partly mechanical.** Lead with the 1% (38%) and 5% (78%) figures.
9. **Per-article mean vs pooled rate.** Always say which.
10. **Event-study power and multiplicity.** 6 types × 7 to 13 outcomes per table; about 2 cells per table reach p<0.05 by chance. Event windows overlap (they cover 41% of weeks and hold 63% of mass2 topic insertions), and a placebo ranks third among events that left a mark. Quote type-level results, not single events.
11. **Hedge regex.** Counts denials and quotations as hedges. Validate on 100 hand-coded mentions. The M11 voice classifier has the same weakness.
12. **Ratchet counts.** Reconcile "35 stuck" with "25 gained, 6 lost" and Zionism's 44 cycles vs 105 flips. Always say whether a survival figure is key-article or mass2.
13. **Censoring in survival.** Mass2 gives Kaplan-Meier; use it for any figure by year. HW6's 77% (n=13) stays a hint.
14. **Editor hashes salted per run.** Mass2 distinct-account counts still rely on one salt per run. Use one fixed secret salt across runs, then discard it.
15. **Block status is as of collection.** Older windows have had more time at risk. Block reasons and partial-vs-sitewide flags are not stored.
16. **Language comparisons.** English uses a 7-term lexicon on all articles; other languages 5 translated stems on about 550 top articles. Compare signs and rough sizes only.
17. **Source classes.** 'Arab & pro-Palestinian' mixes Al Jazeera, +972 (Israeli) and Anadolu (Turkish); 25 to 50% of citations are 'Other'. Mass2 now stores domains, so refine the classes.
18. **Categories are explicit links only.** Template-added categories are missed in both pilot and mass2; the framing regex is direction-blind.
19. **Cross-references in how_who/cards.md are off by one.** Fix before sharing.
20. **Deep-panel gaps.** About 100 articles miss 1 to 3 quarters and were forward-filled.
