# When, where, what words: pattern cards

Ranked by how interesting and solid each pattern is. Chart data is in `chart_data/`.

## 1. One surge in the first half of 2024, then a plateau, now slower than before the war  
*WHEN · STRONG*

**What we see.** In the 332 topic articles that have existed since 2021, the net number of critical terms added was about 7 per 100 articles per quarter before the war. It jumped to 40 (2024-Q1, the quarter of the ICJ order) and 46 (2024-Q2), stayed near 22 for the rest of 2024, then fell back to an average of about 4 in 2025-26. That is below the pre-war pace. The pooled rate climbed from 13.3 to 16.0 hits per 10k words by January 2025 and has stayed flat since (16.1 in Oct 2026). The 84 quiet comparison articles show no surge (rate 12.8 to 12.9).

**Chart.** bars: net critical terms added per 100 articles per quarter (topic vs quiet comparison), with a line for the pooled rate per 10k words; mark Oct 2023 and the ICJ order (26 Jan 2024) (`chart_data/01_timeline_quarterly.json`)

**So what.** This was a time-limited wave, not an ongoing slide. If someone says 'Wikipedia keeps getting more critical', the data says no: the step happened in 2024 and has since stalled. A journalist can date it, and a researcher can treat 2024 as the event window.

**Caveat.** Quarterly snapshots of counts; a single large article can move a quarter (the comparison group swings because one article was blanked and restored).

**Examples.**
- Israeli–Palestinian conflict: 33 to 62 critical hits between Jul 2023 and Nov 2026 (mass tier).
- List of genocides: 55 to 154 hits between the Apr and Jul 2024 snapshots (the Gaza entry).

## 2. A hot core and a quiet periphery: 85% of topic articles did not change at all  
*WHERE · STRONG*

**What we see.** Across 4,009 unique topic articles (mass tier), 11.4% gained critical terms after July 2023 and 85% had exactly the same count. The top 1% of articles (40) supplied 38% of all added terms, the top 5% supplied 78% and the top 10% supplied 96%. Israel and Palestine WikiProject articles are 61% of the sample but supplied 84% of the additions. Judaism articles are 28% of the sample and supplied 7%. Top-importance articles are 8% of the sample and supplied 23%. Even so, the change spread more widely than before the war: the number of gaining articles went from 215 to 456, and the top-1% share fell from 50% to 38%. In the comparison group the number of gainers barely moved (302 to 341) and the top 1% still holds 49%.

**Chart.** Lorenz curve: cumulative share of added critical terms (y) against the share of articles ranked by additions (x), four lines: topic pre/post and comparison pre/post (`chart_data/03_concentration.json`)

**So what.** The 'Wikipedia shifted' story is really about a few hundred pages. Readers of most topic pages (religion, people, organisations) see no change. Monitoring can focus on about 400 hot articles. The broadening from 215 to 456 gainers is the part worth watching.

**Caveat.** Counts terms, not meaning; 125 redirect-duplicate rows (for example Palestine / Palestinian state / Palestinian homeland) were removed before computing.

**Examples.**
- Gaza Strip +25, Benjamin Netanyahu +22, Criticism of Israel +21, West Bank +18, Deir Yassin massacre +16 (critical hits added, Jul 2023 to Nov 2026).

## 3. Genocide, Nakba/expulsion and ethnic cleansing rose after the war; apartheid and colonial had already risen before it  
*WHAT WORDS · STRONG*

**What we see.** After July 2023, topic-article rates rose for genocide (+46% deep panel, +23% mass tier), ethnic cleansing (+37% / +29%), Nakba/expulsion (+22% / +17%), war crimes (+18% / +11%) and occupation (+14% / +9%). The comparison groups were flat (genocide −1% / +1%). Apartheid had already risen +39% between 2021 and 2023 (the years of the Amnesty and HRW reports) and moved only +7% after. In the word race, 'displacement' rose +87%, 'ICJ' +143%, 'famine' +42% and 'two-state' +37%.

**Chart.** dumbbell or slope chart per word family: % change 2021→2023 vs 2023→2026, topic vs comparison, deep and mass panels side by side (`chart_data/07_vocabulary_families.json`)

**So what.** The post-war vocabulary is the vocabulary of legal accusation and of 1948 (genocide, expulsion, ethnic cleansing). Apartheid is an older, pre-war layer. Arguments about 'apartheid entering Wikipedia' after 7 October are aimed at the wrong period.

**Caveat.** The Nakba/expulsion lexicon also catches Jewish expulsions: 76 of the 410 net added hits are in Judaism and Jewish-history articles (for example Edict of Expulsion +20).

**Examples.**
- Deir Yassin massacre lead (2026): 'It occurred during the 1947–1948 civil war and was a central component of the Nakba and the 1948 Palestinian expulsion and flight.' (absent in 2021)
- Israel lead (2026): 'After the Hamas-led October 7 attacks, Israel began committing genocide against Palestinians in Gaza.'

## 4. The wave reached places and people, not just war pages; religion stayed still  
*WHERE · SUGGESTIVE*

**What we see.** Comparing the share of topic articles that gained critical terms per year before and after the war: place articles went from 1.6% to 4.6% a year, people from 1.3% to 2.4%, politics, relations and rights from 5.2% to 9.6%, and conflict from 4.9% to 7.8%. Religion and texts stayed under 1% a year, and Holocaust and persecution articles moved little (6.1% to 6.9%). Of the 60 place articles that gained, 35 gained Nakba/expulsion wording, many of them Palestinian village pages. In the comparison group no article type sped up; most slowed.

**Chart.** paired horizontal bars by article type: % gaining per year, pre vs post, topic and comparison panels (`chart_data/05_geography_type_importance.json`)

**So what.** The change is a re-telling of the land and its people (villages, camps, leaders), in line with the 'older-history residual' finding. It is not a spill-over of war news. Editors of geography and biography pages are part of the story.

**Caveat.** Article type comes from a title-keyword classifier, about 70% correct on a spot-check; untyped titles (mostly places) are a large residual.

**Examples.**
- Gaza Strip lead (2026) now says it 'became a refuge for Palestinians who fled or were expelled by Zionist forces in the Nakba'.
- Yarmouk Camp 0→8, Gaza City +6, Al-Khisas +4, Mustafa Barghouti +10, Yahya Sinwar +10.

## 5. First the edit storm, then the words  
*WHEN · SUGGESTIVE*

**What we see.** Edits to topic articles more than doubled in the war quarter (2023-Q4: 24 per article, against about 10.5 before). That quarter added only 0.9 critical terms per 100 edits, which is below the pre-war 1.0. The words came in 2024-Q1 and Q2 (2.5 and 3.0 terms per 100 edits), while edit volume was already falling. By 2025-Q2 edits were back to baseline. Article by article, the biggest vocabulary jump usually falls in the same quarter as that article's own edit peak (median lag 0). So the aggregate lag comes from different articles having their storms at different times.

**Chart.** dual line by quarter: edits per article and critical terms added per 100 edits (topic), with the comparison as a faint line (`chart_data/01_timeline_quarterly.json`)

**So what.** The first weeks after the attack were about news coverage. The reframing came months later, article by article, as editors worked through older pages. Anyone watching for 'framing shifts' should look one to two quarters after an event, not at the event itself.

**Caveat.** Quarterly resolution; the per-article lag has a wide spread (−7 to +10 quarters).

**Examples.**
- The Zionism group's big vocabulary quarters were 2024-Q3 and Q4, nine to twelve months after October 2023.

## 6. Lead amplifies: lead text moved about 2.6 times more than body text  
*WHAT WORDS · STRONG*

**What we see.** In the mass tier, critical terms per 10k words rose 13.5% in topic article bodies after July 2023 (5.37 to 6.10) and 35% in leads (8.18 to 11.03). Comparison articles rose 1.1% in bodies and 5.4% in leads. The share of first sentences that contain a critical term went from 1.48% to 2.08% for topic articles, and from 0.63% to 0.66% for comparison articles.

**Chart.** grouped bars: % change 2023→2026 in critical rate, lead vs body, topic vs comparison (`chart_data/09_lead_vs_body.json`)

**So what.** What most readers actually see (the lead, and the snippet in search results and AI answers) changed more than the article underneath. Platform and search teams should audit leads first.

**Caveat.** Leads are short, so a single sentence moves the rate a lot.

**Examples.**
- West Bank lead (2026) now cites the ICJ finding that the occupation 'violates the international prohibition on racial segregation and apartheid'.

## 7. Some words fell: 'terrorism' and 'militant' thinned out in topic articles  
*WHAT WORDS · SUGGESTIVE*

**What we see.** After July 2023, terrorism vocabulary per 10k words fell 12% in deep-panel topic articles and 9% in the mass tier; in leads it fell 24% / 19%. 'Terrorist' fell 15%, 'militant' 7%, 'peace' 8% and 'homeland' 8%. In the comparison group terrorism was flat (0% / +4%). The fall is concentrated in a few articles: Hamas lost 47 terrorism mentions and Netanyahu 24. Meanwhile more articles contain the word at all (10.9% to 11.6%), so the word is spreading thinly while being cut where it was dense.

**Chart.** diverging bars: % change per word 2023→2026, topic vs comparison (word race) (`chart_data/08_word_race.json`)

**So what.** The shift is not only additions. In flagship articles the security framing was cut back while the legal and historical framing grew. Anyone claiming one-sided change should count losses too.

**Caveat.** Driven by a handful of articles; some of the drop is restructuring (lists split, sections moved).

**Examples.**
- Hamas lead 2021: 'a Palestinian Sunni-Islamic fundamentalist but pragmatic, militant, and nationalist organization'. 2026: 'a Sunni Islamist Palestinian nationalist political organisation with a military wing … It has governed the Israeli-occupied Gaza Strip since 2007.'

## 8. Core first, periphery a year later  
*WHERE · SUGGESTIVE*

**What we see.** The hand-picked core of the deep panel (conflict, Israel, Zionism, antisemitism subgroups) had made half of its post-war vocabulary additions by 2024-Q2 or Q3. The randomly sampled category articles and the Judaism subgroup reached the same point only in 2025-Q2. That is three to four quarters later.

**Chart.** cumulative-share lines from 2023-Q4, one per subgroup, with a 50% reference line (`chart_data/06_diffusion_core_periphery.json`)

**So what.** The framing spreads outward from flagship pages to the long tail, like a diffusion process. Changes made to the core today predict what the periphery will say in about a year.

**Caveat.** Periphery totals are small (Judaism: 38 added terms) and subgroup labels come from the sampling design.

## 9. Flagship leads are still settling: lasting gains locked in throughout 2024–2026  
*WHEN · ANECDOTE*

**What we see.** In the leads of 25 topic key articles, 25 (article, term) pairs were gained and 6 lost between 2021 and 2026. The final, lasting change happened in 2024 for 10 of the gains, in 2025 for 7 and in 2026 for 7. Comparison key articles had 4 gains and 5 losses. Counting only articles that existed in 2021, critical (article, term) pairs present in leads went from 15 (2021) to 18 (Sep 2023), 23 (mid-2024) and a peak of 29 (mid-2025), then eased to 26 by Oct 2026.

**Chart.** step line by month: (article, term) pairs present in topic vs comparison key leads; dots for each final lock-in (`chart_data/02_key_leads_monthly.json`)

**So what.** Unlike the article mass, which plateaued in 2025, flagship leads are still being fought over. The Israel lead's genocide and apartheid wording last flipped in September 2026, after 19 and 39 flips. These are the places to watch next.

**Caveat.** Only 21–25 articles; one edit war can add or remove several pairs.

**Examples.**
- Israel: genocide (19 flips) and apartheid (39 flips) both final on 2026-09-04.
- Israeli–Palestinian conflict: colonial, apartheid, genocide and Nakba all locked in during 2024.

## 10. Other wars have their own waves, but they stay inside the war articles  
*COMPARISON · SUGGESTIVE*

**What we see.** Comparison conflicts show event-tied steps. Tigray war went from 0 to 21 critical hits in its first year and then stayed flat. Nagorno-Karabakh conflict went 5→8→13 around the 2023 offensive, then up to 19 in 2026. The Sudanese civil war reached 40 hits within 18 months. Ukraine had 636 edits in 2022-Q1, yet its critical count fell (6 to 3). Among comparison projects only Ukraine sped up afterwards (gainers 3.9% to 5.1% a year). In the comparison group as a whole, war-type articles did not speed up (5.3% to 5.5% a year) and other types slowed.

**Chart.** small multiples: critical count by quarter for Tigray, Nagorno-Karabakh, Sudan, Ukraine, Armenia, with their event dates (`chart_data/10_other_conflicts_waves.json`)

**So what.** 'Vocabulary follows events' is normal Wikipedia behaviour. What sets the Israel–Palestine topic apart is that the wave left the war articles and reached history, place and biography pages.

**Caveat.** Few comparison conflict articles in the deep panel (6 shocked); mass-tier comparison has only three snapshots.

**Examples.**
- Tigray war: 0, 1, 8, 12, 19, 21 critical hits over its first six quarters, then flat for four years.

## 11. Wikipedia-wide drift is small, and 'colonial' is the one word that rises everywhere  
*COMPARISON · SUGGESTIVE*

**What we see.** Across the comparison group, critical vocabulary drifted up 2.6% from 2021 to 2023 and 1.1% from 2023 to 2026 (mass tier). It is slowing, not accelerating. 'Colonial' is the exception: in the leads of the quiet comparison articles it rose from 2.4 to 5.2 per 10k words over the window, more than in the topic leads (1.1 to 1.3). The apparent +28% rise in 'indigenous' in comparison articles is almost all one page (Taiwanese indigenous peoples, +294 hits). Scholarly citations rose everywhere (comparison 47% to 61%, topic 37% to 47%).

**Chart.** line: comparison-group critical rate and colonial-lead rate over time, with topic as reference (`chart_data/11_wikipedia_wide_drift.json`)

**So what.** A decolonial vocabulary is spreading across Wikipedia in general. Topic-specific claims should be measured against it. The topic's distinctive vocabulary is genocide and Nakba/expulsion, not colonial.

**Caveat.** Comparison sets were chosen for structural similarity, not at random; the scholarly-citation classifier may also drift.

**Examples.**
- Taiwanese indigenous peoples alone accounts for about half of the comparison group's indigenous/homeland increase.

## 12. More of the loaded words now come with attribution  
*WHAT WORDS (surprise) · SUGGESTIVE*

**What we see.** The share of loaded-term mentions in topic articles with a hedge or attribution nearby ('accused', 'described as', 'according to'…) rose from 21.3% (2023) to 25.0% (2026). In the comparison group it went from 16.7% to 17.2%. This sits alongside the known move of a few flagship leads to Wikipedia's own voice.

**Chart.** slope chart: hedged share 2021/2023/2026, topic vs comparison (`chart_data/09_lead_vs_body.json`)

**So what.** Most of the new vocabulary came in as reported claims, not as statements in Wikipedia's own voice. The voice upgrades (Gaza genocide, Israel lead) are the exception, not the norm, which matters for fairness debates.

**Caveat.** Window-based hedge detection; pooled only, no per-article test.

## 13. The body and the lead can move in opposite directions: Zionism  
*WHERE (surprise) · ANECDOTE*

**What we see.** In the Zionism article, settler-colonial mentions in the body fell from 52 to 9 between the Apr and Jul 2026 snapshots (the body shrank from 15.3k to 12.6k words). Over the same months the lead kept and settled 'colonization'. Overall the article's critical count went 34 → 103 (Jan 2025) → 27.

**Chart.** two lines: Zionism body vs lead settler-colonial count by quarter

**So what.** Counting the whole article can hide a change in the lead, and the other way round. Coders should look at lead and body separately.

**Caveat.** One article; the reason for the body cut (a split or trim) was not traced.

**Examples.**
- Zionism lead (2026): 'an ethnocultural nationalist movement that emerged in late 19th-century Europe to establish and support a Jewish homeland through colonization in the region of Palestine'.

# New questions

### Q1. Does the vocabulary diffuse along links: do articles linked from a hot-core article gain the same terms later than the core did?
- **Data:** Not with existing data (no link graph). Need prop=links (or pagelinks via action=query&generator=links) for the ~400 hot-core articles, then the revision text of linked pages at quarterly snapshots (prop=revisions&rvstart=…&rvprop=content).
- **Feasibility:** 1–3 requests per core article for links; about 24 per linked article for quarterly snapshots (or 3 at mass-tier dates). Roughly 400 + 3×5,000 requests.
- **Why:** It would show whether the core-then-periphery pattern (card WWW8) is editors following links, or independent editing.
- **Quick check:** Partial: the deep-panel core subgroups reached half their additions by 2024-Q2/Q3, the periphery by 2025-Q2 (card WWW8).

### Q2. Is the 2024 surge the work of a few editors who sweep many articles, or many editors each touching one?
- **Data:** Partly: ratchet.json has salted editor hashes for lead inserts in 40 key articles; mass/deep only have counts. For the mass tier we would need prop=revisions&rvprop=user|timestamp|size|tags for the 2023-07..2025-01 window, plus diffs (action=compare) for revisions that change critical counts.
- **Feasibility:** About 2–10 revision-list requests per article; for diffs, 1 compare per candidate revision (about 5–20 per hot article). Feasible for the ~450 gainers.
- **Why:** It separates organic consensus from campaign editing, which is the most-asked question from non-specialists.
- **Quick check:** Existing ratchet summary: the terms that stuck took on average 3.4 distinct editors and 3.3 failed attempts before sticking.

### Q3. Did the vocabulary arrive with a particular source type (rights orgs, Arab/Palestinian press, scholarly)?
- **Data:** Partly answered: mass citations by source class at 3 dates. To tie sources to the added sentences, we need the reference attached to each added sentence: parse <ref> in the diff (action=compare) of revisions that add critical terms.
- **Feasibility:** 1 compare per adding revision; about 3,000 revisions for the mass tier.
- **Why:** It tests whether the change tracks the academic literature or advocacy sourcing.
- **Quick check:** Topic citations: Arab & Palestinian press 0.6% → 1.7%, pro-Israel advocacy 1.0% → 0.6%, rights orgs/UN flat at about 1.5%, scholarly 37% → 47% (but comparison scholarly also 47% → 61%, so that part is Wikipedia-wide).

### Q4. Does page protection (extended-confirmed / ARBPIA) slow or freeze the change?
- **Data:** Not in existing data. Need prop=info&inprop=protection (current), plus list=logevents&letype=protect&letitle=… for the protection history.
- **Feasibility:** 1 batched request per 50 articles for current protection; 1 per article for the log. About 10k requests in total.
- **Why:** ArbCom put the whole topic under extended-confirmed restrictions in 2020 and tightened them later. If protection bounds the change, platform rules matter more than editor views.
- **Quick check:** Proxy check with mass data: among high-edit topic articles (top quartile), 45% of low-revert articles gained critical terms against 20% of high-revert ones, so contested pages change less.

### Q5. Is there a Wikipedia-wide decolonial drift ('colonial', 'indigenous') outside our hand-picked comparison sets?
- **Data:** Not with existing data; the comparison groups are purposive. Need a random article baseline: list=random&rnnamespace=0 (5,000 articles) and prop=revisions at 2021-01, 2023-07 and 2026-11.
- **Feasibility:** About 4 requests per article (1 random batch call per 500, then 3 snapshot fetches); about 15k requests.
- **Why:** Without a random baseline we cannot tell topic change from encyclopedia-wide style change. 'Colonial' rose in comparison leads (card WWW11).
- **Quick check:** Comparison-group leads: colonial 2.4 → 5.2 per 10k; indigenous rise is one article (Taiwanese indigenous peoples).

### Q6. Do readers drive it: did page-view spikes precede vocabulary changes?
- **Data:** Mostly missing: pv_monthly exists for only 37 deep articles. Need the Wikimedia REST pageviews API /metrics/pageviews/per-article/en.wikipedia/all-access/user/{title}/monthly/2021010100/2026110100.
- **Feasibility:** 1 request per article; 10k requests, cheap.
- **Why:** Attention → edits → words is the simplest causal story; testing it per article would replace the calendar narrative.
- **Quick check:** Per-article: the vocabulary jump usually coincides with the article's own edit peak (median lag 0 quarters, n=66), so edits and words move together and attention is the next link to test.

### Q7. Did the Nakba wording enter Palestinian village articles in a coordinated sweep (same phrasing across many villages)?
- **Data:** Partially: mass tier gives counts only. Need the lead text of the ~400 Palestine-project place articles at 2023-07 and 2026-11 (prop=revisions&rvprop=content&rvsection=0), then near-duplicate phrase detection.
- **Feasibility:** 2 requests per article, about 800 requests.
- **Why:** 35 of 60 gaining place articles gained Nakba/expulsion wording. Template-like phrasing would point to a project drive (WikiProject Palestine), not diffuse editing.
- **Quick check:** Counts only: 35 of 390 topic place articles gained Nakba/expulsion terms after Jul 2023.

### Q8. Is the flagship-lead ebb in 2026 (29 → 26 pairs) the start of a counter-wave?
- **Data:** Yes, existing ratchet.json covers it; refreshing it monthly needs prop=revisions&rvsection=0 for 40 key articles since the last revid.
- **Feasibility:** 1–5 requests per article per month.
- **Why:** It tells whether the plateau is a stable consensus or a pendulum.
- **Quick check:** In 2026 only 1 topic (article, term) loss became final (Hezbollah, settler-colonial, Aug 2026) against 7 final gains; the ebb is mostly pairs still in flux.

### Q9. Do other language editions follow English with a lag?
- **Data:** Partly: crosslang.json (20 key articles × 11 languages) and the mass languages tests exist. A lag test needs quarterly snapshots in each language (prop=revisions per language wiki).
- **Feasibility:** About 24 requests per article-language; 20×10×24 ≈ 5k.
- **Why:** If English leads and others follow, English Wikipedia sets the global framing.
- **Quick check:** Mass-tier language tests (2023→2026, topic minus comparison): no language has a significant body change; only Portuguese leads (+0.27 per 1,000 words, p=0.004). So other wikis mostly did not follow.

# Data notes

- mass_results.json lab_articles contains 125 duplicate rows (redirects resolving to the same page, for example 'Palestine' / 'Palestinian state' / 'Palestinian homeland', and 'West Bank' / 'Economy of the West Bank'). All mass figures here are deduplicated (9,062 unique articles with three snapshots). Earlier mass results may be slightly inflated by these duplicates.
- The deep panel has scattered missing snapshots (about 100 articles miss 1–3 quarters); they were forward-filled.
- The mass-tier pre window is 30 months and the post window 40 months; 'per year' figures annualise the share of articles gaining.