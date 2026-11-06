# Sampling audit: was the mass tier chosen correctly, and do the statistics account for how it was chosen?

Auditor's note, 2026-11-06. Scope: the mass2 tier (10,320 articles), with a check on mass v1 and the deep panel. Everything here is reproducible:

- `build_df.py`: one row per mass2 article, built through `analyze_mass2.build`, so the outcomes are exactly the card outcomes.
- `audit.py`: design reconstruction, weights, bootstraps, balance, matching and comparison subsets.
- `extras.py`: population-weighted matching, the outlier check and the imputation bound.

Chart data is in `chart_data/`:

- `01_population_vs_sample.json`
- `02_balance_smd.json` (Love plot)
- `03_weighted_vs_unweighted.json` (dot-and-whisker)
- `04_comparison_projects.json`
- `05_selection_effects.json`
- `06_extras.json`

CIs are 95%. Square brackets are a stratified bootstrap (1,000 replicates, articles resampled within project × importance stratum). Curly brackets are a project-cluster bootstrap. All unweighted figures reproduce the published cards exactly:

- (a) +2.22
- residual +1.98 (89%)
- 3.9% vs 1.5%
- 15.0% vs 5.0%
- views DiD +7.5 pp
- mass v1 holdout A1 +3.6 pp [1.6, 5.5], A5 +5.6 pp, A5b −0.1 pp

## Verdict in one paragraph

The sample is a sound, documented frame, but it is **not a random sample of "the topic"**, and the published statistics treat it as if it were. Every number is unweighted, so it implicitly over-weights:

- **Palestine** (85% of its Mid pages sampled) and topic High-importance pages;
- and under-weights **Israel's Mid-importance pages** (12% sampled), which barely changed.

On the comparison side, a cap of 260 per project means 85% of the comparison population had **zero** chance of selection. The comparison group is mostly Top- and High-importance pages: 42% Top in the sample, against 4% of the topic population.

Weighting the topic side to its real population roughly **halves** the article-share results: (a), (b) and (e). It **leaves reader exposure (d) intact** and leaves the narrative residual "most of the change". Matching on importance, activity, length and age makes the topic-vs-comparison gap **larger**, not smaller, because the busier comparison pages over-state the comparison baseline.

The direction of every headline holds, but several sizes in SYNTHESIS must change. The exposure gap is not robust against *other live conflicts*.

---

## 1. Population vs sample

### How rows were selected (mass.py `frame()`)

1. **Frame.** Talk pages in `Category:{Top,High,Mid}-importance <suffix>`. The suffix is found by `allcategories` prefix search on a keyword, keeping names at most 20 characters longer than the keyword. **Low-, NA- and Unknown-importance articles are never in the frame.**
2. **Projects.**
   - Topic (in order): Israel, Judaism, Jewish history, Palestine. *Zionism, Jewish culture and Arab–Israeli conflict were listed but have no importance categories, so they contribute nothing.*
   - Comparison: 23 projects. Cyprus and Armenian history found nothing, and Sikhism has only 8 articles.
3. **Assignment.** An article goes to the first project in list order that lists it. Its importance is the highest level across the group's projects. An article listed by both a topic and a comparison project is dropped; 572 were dropped this way, and their titles were not kept. So "Palestine" means *Palestine-project pages that the Israel and Judaism projects do not also list*.
4. **Draw.** Within each project, the pages are shuffled (seed 42), sorted Top > High > Mid, and the first 1,400 (topic) or 260 (comparison) are kept. Within each project × importance cell this is a simple random sample, so the inclusion probability is π = n/N.
5. **mass2 resolve.** Redirects were resolved: 126 duplicate rows merged, 8 missing pages and 3 disambiguation pages dropped. This is treated as ignorable non-response within the stratum.

**Bug.** The keyword "India" also matched `Indiana articles` and `Indianapolis articles`. Eight US-state pages are in the India comparison sample: Marion County, Indiana; Indiana Supreme Court; Seal of Indiana; and others. The effect is negligible, but it should be fixed by matching whole suffixes.

### Population sizes

`frame.json → category_counts` stores the talk-page count of all 186 categories. These are the population counts. They overlap across a project's own sub-categories and across projects. The pool for a cell is therefore:

- exact where the whole level was taken (N = n_frame);
- estimated as `category count × the project's own pool/category ratio on its whole levels` where the cap bites;
- the same estimate for levels the cap never reached (π = 0).

These figures are as of the frame run (Nov 2026).

| Topic project | Top N / n / π | High N / n / π | Mid N / n / π |
|---|---|---|---|
| Israel | 167 / 161 / 0.96 | 807 / 796 / 0.99 | 3,580 / 424 / **0.12** |
| Judaism | 149 / 147 / 0.99 | 655 / 645 / 0.98 | ~1,749 / 586 / **0.34** |
| Jewish history | 11 / 11 / 1 | 88 / 88 / 1 | 406 / 403 / 0.99 |
| Palestine | 33 / 31 / 0.94 | 276 / 267 / 0.97 | ~1,278 / 1,083 / **0.85** |
| **Topic total** | 360 / 350 / 0.97 | 1,826 / 1,796 / 0.98 | 7,013 / 2,496 / **0.36** |

Topic: 12,292 category talk pages, about 9,199 unique pages in the frame, 4,642 sampled (π = 0.50). **Population mix:** Top 3.9%, High 19.8%, Mid 76.2%. **Sample mix:** 7.5%, 38.7%, 53.8%. **Project shares:**

| Project | Population | Sample |
|---|---|---|
| Israel | 49.5% | 29.7% |
| Judaism | 27.8% | 29.7% |
| Jewish history | 5.5% | 10.8% |
| Palestine | 17.3% | 29.7% |

| Comparison | Top | High | Mid |
|---|---|---|---|
| Category talk pages | 4,478 | 19,025 | 73,784 |
| Estimated pool | 4,176 | 17,447 | 68,374 |
| Sampled (mass2) | 2,368 | 3,111 | 191 |
| π | 0.57 | 0.18 | **0.003** |
| Pool with π = 0 | 0 | 9,957 | 66,713 |

Comparison: about 90,000 unique pages, 5,670 sampled (π = 0.063). **85% of the comparison pool had zero probability of selection.**

- India, Russia and Sri Lanka are sampled from Top only, with π between 0.23 and 0.59.
- The 191 Mid articles come from Kurdistan (106), Tibet (58), Azerbaijan (21), Sikhism (5) and Bosnia (1).
- Every cell is listed in `chart_data/01_population_vs_sample.json`.

**What was not stored, and the exact calls that would give it** (the sandbox cannot reach Wikipedia):

- **Low, NA and Unknown sizes, per project:**
  `action=query&prop=categoryinfo&titles=Category:Low-importance_Israel-related_articles|Category:NA-importance_Israel-related_articles|Category:Unknown-importance_Israel-related_articles|Category:Israel-related_articles_by_quality`
  Repeat for Palestine-related, Judaism, Jewish history-related and each comparison suffix. Use `categoryinfo.pages`; it also counts template and category talk pages.
- **Article-level frame with class and importance, one call family per project** (PageAssessments; this is the recommended source):
  `action=query&list=projectpages&wppprojects=Israel|Palestine|Judaism|Jewish history&wppassessments=1&wpplimit=max` (continue until done).
- **Exact pools and the 572 "both" titles:** rerun `mass.cat_talk_titles` over the 186 categories (about 300 requests) and store `seen` before the cap.

## 2. Selection effects

| | Topic sample | Comparison sample | Comment |
|---|---|---|---|
| Importance (sample) | Top 7.5% / High 38.7% / Mid 53.8% | 41.8% / 54.9% / 3.4% | Importance SMD −1.43. The groups differ most here. |
| Importance (population) | 3.9 / 19.8 / 76.2 | 4.6 / 19.4 / 76.0 | The two *populations* are alike; the *samples* are not. |
| Median edits Jan 2021 to Jul 2023 | 18 | 45 | SMD −0.56 (log) |
| Median views per month before the war | 613 | 2,704 | SMD −0.52 |
| Median lead words, Jul 2023 | 94 | 134 | 2021 lead SMD −0.31 |
| Created after 2021-01-01 | 8.1% | 4.3% | SMD +0.16. Page id SMD +0.29, so topic pages are newer. |
| Stub or Start class | 40% (weighted 46%) | 38% | |
| Contentious-topic notice | 33.6% | 7.9% | This is the treatment-adjacent difference. |
| Redirect rows merged | 55 | 55 | 126 duplicates in all. Mass v1 and holdout figures predate the merge. |

**Over-represented in the topic sample:**
- Palestine-only pages: 30% of the sample, 17% of the population, and the project that changed most (6.7% of leads gained critical terms).
- High and Top pages.
- Jewish history pages.

**Under-represented:**
- Israel Mid pages: 9% of the sample, 39% of the population; 0.9% gained.
- Judaism Mid pages.

**Missing entirely:**
- Low-importance and unassessed pages: villages, minor biographies, stubs. 234 of the 264 surviving deep-panel category-crawl pages (89%) are not in the mass2 sample. Only part of that is the Mid draw, so much of the topic likely lives outside the Top-to-Mid frame.
- Overlap pages tagged by both groups (572). These are probably the most entangled pages, such as Iran–Israel and Lebanon topics.

**Cross-tagging now.** 28 comparison articles carry a topic-project tag today (for example Assassination of Ali Khamenei and Joseph Stalin). Dropping them changes nothing: (a) stays +2.22 and (b) +2.5 pp.

**Deep panel (corpus.py).** The manifest has 598 rows:
- treatment: 148 hand-picked seeds and 347 pages from a depth-1 crawl of 6 categories (shuffled, capped);
- control: 103 rows, all hand-picked.

After the 300-word rule, 513 remain. 84 of the 85 exclusions were treatment rows, mostly category-crawl stubs, so the filter is asymmetric.

The hand-picked seeds are the famous, contested pages, including every press-documented VALIDATION target and pages created inside the window (Gaza genocide, October 7 attacks). That is **selection on the outcome**. In mass2 the hand-picked topic seeds are 56 Top, 40 High and 9 Mid, with a median of 316k views a year, against 7.2k for a mass2 topic page. Hand-picked controls have a median of 1.1M views. Two control seeds, Arab nationalism and Palestinian nationalism, are topic pages in mass2; they are on the contaminated list.

Implication: deep-panel shares, such as "15% of articles carry 46% of views" and the 31 to 52% gain rates, describe a purposive set of battleground pages. They are case-study evidence, not estimates for the topic. SYNTHESIS D9 already demotes the exposure figure, which is correct.

## 3. Design-weighted results (mass2)

The weight is N_pool / n_mass2 within project × importance. Cells with fewer than 30 articles are pooled within group × importance; without this, the single Bosnia Mid article would get a weight of 514. After pooling:

- topic: weights 1.0 to 8.4 (Israel Mid), Kish design effect 2.2, effective n 2,137;
- comparison: weights 1.0 to 37, design effect 2.5, effective n 2,265.

The weighted comparison side can only stand for the 15% of its pool that had π > 0. Its weighted Mid estimate is dominated by one Nagorno-Karabakh village: "Martuni, Nagorno-Karabakh" gained 1 term in a 68-word lead, +147 per 10k words, at weight 37. So for (a) three robust variants are reported:

- comparison not weighted, topic weighted;
- Martuni removed;
- comparison Mid imputed from comparison High.

| Statistic | Unweighted | Design-weighted | Robust weighted variants |
|---|---|---|---|
| **(a)** post-war lead critical DiD, hits per 10k words | **+2.22** [1.30, 3.17] {−0.44, 4.79} | **+0.87** [−0.38, 1.80] {−0.97, 4.32} | topic-only weighted +1.14 [0.46, 1.77]; without Martuni +1.32 [0.67, 1.97]; Mid imputed +1.17 [0.47, 1.82] |
| **(b)** share of leads gaining critical terms, topic vs comparison | 3.9% vs 1.5%, **+2.4 pp** [1.8, 3.1] {−0.4, 4.8} | 2.5% vs 1.3%, **+1.1 pp** [0.3, 1.9] {−0.6, 4.7} | Mid imputed 2.5% vs 1.2%, +1.3 pp [0.7, 2.0] |
| (b′) full-text gain share, post minus pre DiD (A1 on mass2) | +5.1 pp [3.7, 6.4] | +3.2 pp [1.6, 4.6] | |
| (b″) **A1 on the sealed mass v1 holdout** | **+3.6 pp** [1.6, 5.5] | **+2.6 pp** [0.5, 4.9] | all of mass v1: +5.4 → +3.4 pp |
| **(c)** narrative-residual DiD / share of (a) | **+1.98** [1.05, 2.88] / **89%** [76, 98] | **+1.07** [0.44, 1.66] / ratio unstable, 123% [−470, 787] | without Martuni 81% [57, 94]; Mid imputed 81% [54, 94]; topic-only 84% [57, 99] |
| **(d)** view share on gaining leads, topic vs comparison | **15.0% vs 5.0%** (+10.0 pp [4.2, 17.1]) | **13.7% vs 3.4%** (+10.3 pp [4.6, 16.9] {−0.6, 22.9}) | Mid imputed 13.7% vs 2.7% |
| (d′) views share minus article share, DiD | +7.5 pp [1.9, 14.6] {−2.1, 17.0} | +9.2 pp [3.6, 15.6] {−0.4, 19.2} | |
| **(e)** Israel+Palestine minus Judaism, lead gain share | **+5.2 pp** [4.3, 6.2] (5.8% vs 0.5%) | **+2.7 pp** [2.0, 3.6] (3.3% vs 0.5%) | A5 mass v1 holdout +5.6 → +4.2 pp [1.4, 7.1] |
| (e″) Judaism minus comparison | −0.9 pp [−1.4, −0.4] | −0.8 pp [−1.6, −0.1] | A5b holdout −0.1 → −0.3 [−2.8, 2.1]: still inside ±3 pp |

**Relevant subset** (Wikidata type and baseline relevance), unweighted → weighted:

| Statistic | Unweighted | Weighted |
|---|---|---|
| (a) | +4.53 [2.44, 6.80] | +4.00 [2.24, 5.86] {0.18, 6.17} |
| residual | +4.35 | +3.85 |
| residual share | 96% | 96% |
| (b) | 8.3% vs 3.8%, +4.5 pp | 6.4% vs 2.7%, +3.6 pp [2.0, 5.2] |
| (d) | 27.6% vs 8.6% | 22.9% vs 6.4% |

The relevant subset is much less sensitive to weighting.

**By importance, design-weighted** (the comparison levels that both groups really sample):

| Level | (a) | (b) | (d) |
|---|---|---|---|
| Top | +2.42 [0.49, 4.37] | +8.2 pp | 29% vs 4% |
| High | +2.92 [1.45, 4.58] | +3.3 pp | 8% vs 3% |
| Top+High | +2.89 [1.64, 4.21] | +4.1 pp [3.1, 5.1] | |

For Mid, (a) cannot be estimated: there are 191 comparison articles, almost all from Kurdistan, Tibet and Karabakh. Topic Mid moved little: +0.95 per 10k words and 1.6% gained.

**Reading.** The headline sizes in SYNTHESIS are sizes for the *sample*. The population of the four projects is three-quarters Mid pages, and Israel's Mid pages barely changed. So the average article-level effect is about half of what was published. It remains clearly positive except when the comparison side leans on one village.

Exposure (d) does not shrink, because views are concentrated on the Top and High pages, which were sampled almost completely. The "Judaism did not move" result is untouched.

## 4. Comparison balance and matching

Standardised mean differences, topic minus comparison. The denominator is the pooled SD; the bar for balance is |SMD| < 0.1. Plot data: `chart_data/02_balance_smd.json`.

| Covariate | Unweighted | Design-weighted | CEM | Propensity 1:1 |
|---|---|---|---|---|
| Lead words 2021 (log) | −0.31 | −0.35 | 0.00 | 0.00 |
| No 2021 lead | +0.16 | +0.09 | 0.00 | −0.02 |
| Page id (log, age proxy) | +0.29 | +0.36 | −0.02 | 0.00 |
| Created after 2021 | +0.16 | +0.11 | 0.00 | −0.01 |
| Edits before the war (log) | −0.56 | −0.56 | −0.01 | −0.05 |
| Views per month before the war (log) | −0.52 | −0.57 | +0.03 | −0.04 |
| Importance | **−1.43** | −1.54 | 0.00 | 0.00 |
| Lead had a critical term in Jul 2023 (not matched on) | +0.10 | +0.05 | +0.15 | +0.13 |

How the matching was done:

- **CEM:** exact on importance; quartiles of lead length, page id, edits and views; plus flags for no 2021 lead and creation after 2021. ATT weights. 3,985 of 4,642 topic articles kept.
- **Propensity:** logit on the same covariates, 1:1 nearest neighbour with replacement, caliper 0.2 SD. 4,640 topic articles kept, 1,686 comparison articles used.
- **CIs:** the matching is redone in every one of 200 bootstrap replicates.

| | (a) DiD | (b) gain share |
|---|---|---|
| Unmatched, sample | +2.22 | 3.9% vs 1.5%, +2.4 pp |
| **CEM (sample ATT)** | **+2.76** [1.68, 3.94] | 3.8% vs 0.6%, **+3.2 pp** [2.5, 3.9] |
| **Propensity NN** | **+2.75** [1.23, 3.56] | 3.9% vs 0.4%, **+3.5 pp** [2.4, 3.9] |
| **CEM, topic at design weights (population ATT)** | **+1.84** [1.11, 2.99] | 2.3% vs 0.4%, **+1.9 pp** [1.7, 2.6] |
| Relevant, CEM / PS | +3.72 [0.53, 6.89] / +5.29 [2.26, 9.63] | +8.0 pp [5.9, 11.1] / +7.0 pp [5.3, 8.7] |
| Relevant, CEM at design weights | +4.46 [1.67, 7.79] | +7.1 pp [5.4, 10.7] |

**The result holds and grows under matching.** The comparison sample is busier, longer and more prominent than the topic sample, and busy pages change more everywhere. Matched comparison pages gain far less often (0.4 to 0.6% instead of 1.5%).

The two corrections pull in opposite directions:

- Weighting to the topic population shrinks the estimates.
- Matching on prominence enlarges them.

Combined, the best single estimate for the four projects' population is **(a) +1.8 per 10k words and (b) +1.9 pp**: smaller than published, clearly non-zero. Matching does not balance the baseline critical-term rate (SMD +0.13 to +0.15). Matching on it would be matching on an outcome-adjacent variable, so it was left as a reported imbalance.

## 5. Are the comparison projects the right comparison?

Comparison projects were ranked by distance to Israel+Palestine on pre-war features only: contentious-topic share, relevance share, Jul 2023 lead critical rate, pre-war change and pre-war edits (`04_comparison_projects.json`).

- **Most similar:** Kurdistan, Ukraine, Turkey, Serbia, India, Armenia, Bangladesh, Bosnia and Herzegovina.
- **Least similar:** Catholicism, Buddhism, Islam, Sri Lanka, Tibet, Sikhism, Russia, Hinduism.

Religions have almost no contentious-topic tags and no baseline critical vocabulary. They are a weak counterfactual for Israel and Palestine, but they are the natural one for Judaism.

| Comparison set | (a) unweighted / weighted | (b) unweighted / weighted | (d) topic 15.0% vs comparison (unweighted) |
|---|---|---|---|
| All 23 projects | +2.22 / +0.87 | +2.4 / +1.1 pp | 5.0% (+10.0 pp) |
| **Conflict projects a priori** (Kurdistan, Armenia, Azerbaijan, Ukraine, Russia, Taiwan, Tibet, Sri Lanka, Bosnia, Serbia) | **+1.79** [0.70, 2.87] / +0.14 [−2.10, 1.61] (Martuni) | **+1.7 pp** [0.9, 2.5] / +0.3 pp [−1.3, 1.4] | **10.5% (+4.5 pp [−4.8, 12.7])** |
| Conflict projects, CEM | +2.77 [1.34, 3.98] | +2.7 pp [2.1, 3.6] | |
| Live wars since 2022 (Ukraine, Russia, Armenia, Azerbaijan) | +2.13 [0.93, 3.27] / −0.46 | +1.2 pp [0.1, 2.2] / −0.5 pp | **14.1% (+0.9 pp [−10.3, 13.6])** |
| 8 most similar, data-driven | +1.93 [0.80, 3.07] / +1.09 [0.31, 1.92] | +1.5 pp [0.5, 2.3] / +0.5 pp [−0.4, 1.3] | 8.3% |
| Countries | +2.61 / +1.54 | +2.8 / +1.8 pp | 2.9% |
| Religions | +2.48 / +1.44 | +3.5 / +2.2 pp | 2.1% |
| Relevant subset, conflict projects | +3.24 [0.35, 6.06] / +3.07 [1.22, 5.19] | +2.6 pp [0.4, 5.1] / +2.1 pp [−0.2, 4.5] | 19.4% vs 27.6% |

**Reading:**

- Against other contested conflicts the lead-vocabulary DiD survives at about 80% of its size, unweighted. It survives matching at full size.
- Weighted, it is fragile, because the conflict comparison's Mid tier is a handful of Karabakh and Kurdish pages.
- The share-gaining gap halves (+1.7 pp).
- **The reader-exposure gap disappears against conflicts:** 15% vs 10.5%, and vs 14.1% for the live wars.
- The pooled comparison flatters the topic mainly because it contains religions and quiet countries.

This agrees with SYNTHESIS D4 ("other live conflicts are in the same league") and contradicts P3's "three times the comparison group's" when the comparison is other conflicts.

## 6. Recommendations

### Population definition to state on the page

> "Articles that Wikipedia's own WikiProjects Israel, Palestine, Judaism and Jewish history rate as Top-, High- or Mid-importance (about 9,200 articles in November 2026), of which we analysed 4,642: all Top and High articles and a random draw of Mid articles, weighted back to the true size of each project and level. Low-importance and unrated pages are not covered. The comparison is 5,670 mostly Top- and High-importance articles from 23 WikiProjects on other countries, conflicts and religions."

Do not call mass2 "the whole topic" (SYNTHESIS D13) or "all topic articles" (D6 and P7). Say "the 4,642 sampled articles of the four projects".

### Data that would close the gaps

1. **Population counts and full pools.** Use `list=projectpages` (PageAssessments) for all 27 projects. Store per-article class and importance, including Low and NA, plus the 572 "both" titles and the pre-cap pools. With these, π is exact rather than estimated where the cap bites.
2. **Comparison Mid and High.** Draw a supplementary random sample of comparison Mid (for example 40 per project, about 900 articles), and High for India, Russia and Sri Lanka. Without it, nothing design-based can be said about three-quarters of the comparison population.
3. **A Low-importance stratum.** A random 1,000 Low-importance topic pages and 1,000 comparison pages. This is where villages and biographies live, and where the deep-panel crawl suggests a large part of the topic sits.
4. **Random-Wikipedia baseline** (being built). Make it a `list=random` namespace-0 draw of 5,000 or more pages with the same three snapshots and lexicon. Add a second, stratified draw from all WikiProject-tagged pages by importance, so it can be weighted like the main tiers. Report the topic against the random baseline *and* against conflict projects.
5. **Fix the frame code.** Match whole suffixes (the Indiana bug). Record the source category per row. Fix project assignment by overlap rather than list order, or at least record every project and importance an article has. Add `weight` and `pi` columns to `frame.json` and mass2, and make `analyze_mass2.py` report weighted alongside unweighted.
6. **Pre-specify the weighted estimand** in a SPEC amendment before re-running. The current runs are post hoc, so label every weighted figure as exploratory until then.

### "How we chose the articles" box (Israeli-media audience)

> **How we chose the articles**
>
> Wikipedia's volunteer editors sort articles into subject groups called WikiProjects. Each group grades how central an article is to its subject: Top, High, Mid or Low importance.
>
> We took the four groups that cover this story: **Israel, Palestine, Judaism and Jewish history**. Together they grade about 9,200 articles as Top, High or Mid. We analysed 4,642 of them: every Top and High article, and a random draw of the Mid ones. Because we drew more from some groups than others (most Palestine pages, one in eight Israel Mid pages), every percentage is weighted back to each group's true size.
>
> **Not included:** pages graded Low importance or not graded at all, mostly short pages on villages, minor figures and stubs. Our numbers describe the articles Wikipedia's own editors consider central to the subject, not every page that mentions Israel.
>
> **The yardstick.** To tell whether this is special to Israel, we ran the same tests on 5,670 articles from 23 other groups: conflicts (Ukraine, Russia, Armenia, Azerbaijan, the Kurds, Bosnia, Serbia, Taiwan, Tibet, Sri Lanka), countries (India, Pakistan, Turkey, Iran, Ireland, Greece, Poland, Bangladesh) and religions (Islam, Hinduism, Catholicism, Buddhism, Sikhism). These are mostly their most important articles. We also matched articles of similar length, age, traffic and importance; the gap stayed.
>
> **Two limits.**
> - Against other active conflicts, such as Ukraine or Armenia–Azerbaijan, the gap is smaller. The share of reading that lands on changed opening paragraphs is about the same as there.
> - The 25 to 40 famous articles we trace edit by edit, such as Zionism, Israel and Gaza genocide, were chosen by us because they are contested. They show *how* change happened. They are not a sample of Wikipedia.

### Headline numbers in SYNTHESIS that must change

| Where | Now | Change to |
|---|---|---|
| Top box, P3, D9, "What we can conclude" | "3.9% of topic articles gained lead critical terms and they carry 15% of topic views (comparison 1.5% and 5%)" | "In the sampled 4,642, 3.9% gained. Weighted to the four projects' population, **about 2.5% of articles [2.0, 3.0], carrying about 14% of views [8, 20]**. Comparison 1.3% and 3.4%, or 10.5% against other conflicts." Keep "15%" only with "sample". |
| P3 "so what"; summary sentence 3 | "three times the comparison group's" | "about four times the pooled comparison, but **similar to other live conflicts** (Ukraine, Russia, Armenia, Azerbaijan: 14%)". Exposure-gap confidence stays SUGGESTIVE, now also because of the comparison choice. |
| P4 | "post-war DiD +2.22 … residual +1.98 … 89%" | Add: "weighted to population +1.1 to +1.3 (residual about +1.0, 80 to 85%). Matched +2.8. Population-weighted and matched +1.8." **"Most of the change is not about recent events" stands; "89%" should read "about 80 to 90%".** |
| P2 and "We can say", A1 | "+3.6 pp, replicated" | Keep, and add "weighted +2.6 pp [0.5, 4.9]". |
| P2 | "Israel+Palestine minus Judaism +5.6 pp"; "Israel and Palestine projects are 61% of articles" | Weighted +4.2 pp (mass v1 holdout), or +2.7 pp on mass2 lead gains. IP is **67% of the population** but 60% of the sample. Judaism ≈ 0 is unchanged. |
| D13, D6, P7, Tiers line | "covers the whole topic", "all 4,642 topic articles" | "the sampled 4,642 Top-to-Mid articles of four WikiProjects". Mass2 comparison n is 5,670 (+8 atrocity), not 5,678. |
| P6 / D4 | "2 to 4x the pooled comparison" | Not re-estimated here. The pooled comparison is 42% Top-importance against 4% in the topic population, so every "at equal activity" ratio should be re-run within importance level. |
| Data-quality notes | (missing) | Add "unweighted sample statistics; the frame caps under-sample Israel Mid pages (π = 0.12) and give 85% of comparison pages no chance of selection" and the Indiana bug. |

What does **not** need to change: the direction of every mass result, Judaism ≈ comparison, the wave timing (P1), the editor composition (P8) and the process results (P11 and P12). The last four were not re-weighted here, and their samples carry the same Mid under-weighting, so add the weighting caveat.
