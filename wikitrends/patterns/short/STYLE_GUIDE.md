# Style guide for the summary section

Register: popular data science for a critical general reader. The reader can follow an argument, distrusts being sold to, and wants to see the evidence before the conclusion.

**How these were sourced.** This session's network blocked direct page fetches for every candidate site (OWID, Datawrapper, Pew, Gelman, Data Colada, Gwern, ACX/SSC, FT, NYT and others). Quotations below come from search-indexed text of the cited pages or close secondary write-ups. Each one is marked **[verbatim]** where the search index returned the wording itself, and **[paraphrase]** where it returned a summary. Check any [paraphrase] against the page before quoting it in public.

Pieces used (10): Roser, "The world is awful. The world is much better. The world can be much better." (OWID); Simonsohn, "[47] Evaluating Replications: 40% Full ≠ 60% Empty" (Data Colada); Silver, "When We Say 70 Percent, It Really Means 70 Percent" (FiveThirtyEight); Alexander, "Beware the Man of One Study" (Slate Star Codex); Gelman, "Stories and Stats" (Boston Review) and "The garden of forking paths" (with Loken); Muth, "What to consider when choosing colors for data visualization" and "Emphasize what you want readers to see with color" (Datawrapper); Cairo, "This Hurricane Map Doesn't Mean What You Think It Means" (NYT, 2019); Burn-Murdoch on titles and annotation (GIJN); Gwern, "About This Website", confidence tags; Pew methodology pages. Also: Harford's rules, Healy's *Data Visualization*, the Economist style guide, Ritchie interviews.

---

## 1. The headline states the finding at its true strength. No puns, no reversals.

Roser's best-known OWID essay has a plain, three-clause title: *"The world is awful. The world is much better. The world can be much better."* It packs the whole mixed result into the headline and does not turn it into a twist. [verbatim title] https://ourworldindata.org/much-better-awful-can-be-better

Burn-Murdoch cites a study in which the best-performing chart had "a strong narrative title" plus explanatory annotations, while minimalist versions ranked lowest. [paraphrase] https://gijn.org/stories/data-visualization-storytelling-tips-john-burn-murdoch/ So the title should be **informative**, meaning it says what was found, without being **clever**. The European data-vis guide (drawing on ONS practice) asks writers to state a chart's main message "in 10 words or less". [paraphrase] https://data.europa.eu/apps/data-visualisation-guide/guidelines-for-visualisation-titles

*Applied:* "The average didn't move. The window display did." is a setup and punchline. A descriptive headline says which articles changed, where in the article, and roughly how much.

## 2. Mixed results are stated as mixed, side by side, not resolved into a slogan.

Roser: "All three statements are true at the same time." [verbatim] https://ourworldindata.org/much-better-awful-can-be-better. He gives no aphorism to settle the tension; the reader holds all three statements at once.

*Applied:* "Lopsided, not one-sided" is a verdict about the evidence, and reader 2 flagged it as "an editorial judgment". Give the two directions with their numbers and let the reader weigh them.

## 3. Treat a null result as information and an inconclusive one as inconclusive.

Data Colada [47]: "inconclusive replications are not failed replications". Results should be allowed to come out inconclusive, not only as success or failure. [paraphrase of section header] https://datacolada.org/47. The title itself, *"40% Full ≠ 60% Empty"*, is the one kind of wit that works: it makes a statistical point precisely.

*Applied:* the Judaism result is a formal equivalence test, so say "equivalent to zero". The exposure gap is suggestive, so say "suggestive" and give the reason (the project-level interval crosses zero). The pre-registered average test was null and underpowered. Say so, and say why it does not contradict the concentrated result.

## 4. Give the number, its interval, and what the interval means in words.

Pew's methodology notes give the margin of error with the conditions attached: plus or minus 1.8 points "for full-sample estimates at 50%", larger for subgroups, and "random sampling error is only one possible source of error". [paraphrase] https://www.pewresearch.org/internet/2024/11/13/2024-national-public-opinion-reference-survey-methodology/

Silver, defending calibrated forecasts, makes the claim checkable: of 5,589 events his models called at 70%, 71% occurred. [verbatim figures] https://fivethirtyeight.com/features/when-we-say-70-percent-it-really-means-70-percent/

*Applied:* "15% of topic reading (95% interval about 10% to 21%)" is better than "among the most read".

## 5. Readers anchor on the central estimate, so put the uncertainty in the sentence, not in a footnote.

Cairo on the hurricane cone: people misread it, and people at the cone's edge prepare less. His diagnosis is that "it's a complex chart that requires some explaining". [paraphrase] https://ccs.miami.edu/this-hurricane-map-doesnt-mean-what-you-think-it-means-by-alberto-cairo/. Northwestern's Matthew Kay on the NYT needle: it "was supposed to communicate uncertainty, but people didn't make that connection". [verbatim, as quoted] https://news.northwestern.edu/stories/2020/10/presidential-plinko-visualizes-data-uncertainty

*Applied:* "as of late 2026 the wave has passed" should become "by 2026 the rate was back at the pre-war level; this describes data to late 2026, not a forecast."

## 6. Label confidence explicitly, using a small fixed scale.

Gwern tags each essay with a certainty level from a fixed scale ("certain", "highly likely", "likely", "possible", "unlikely", "highly unlikely"), adapted from Kesselman's list of estimative words. [verbatim scale terms] https://gwern.net/about

*Applied:* SYNTHESIS.md already uses STRONG / SUGGESTIVE / ANECDOTE. Use two plain-English levels in the summary: "clear" (both intervals agree) and "suggestive" (they disagree).

## 7. Resist the crisp story; that is where overclaiming enters.

Gelman, on election punditry: commentators fixate on one piece of data and exaggerate its significance "to produce a crisp and usable story". [paraphrase] https://www.bostonreview.net/forum/gelman-sides-stories-and-stats/. On analytic flexibility, Gelman and Loken's "garden of forking paths": choices that depend on the data can produce false positives with no deliberate p-hacking. [paraphrase] https://sites.stat.columbia.edu/gelman/research/unpublished/p_hacking.pdf

*Applied:* name what was fixed in advance (the sealed half) and what was exploratory. Withdrawn results go in the methods, stated plainly. They are not a trust badge ("We dropped our own failed results").

## 8. On a contested topic, show the whole distribution of evidence, not the most quotable piece.

Alexander's "Beware the Man of One Study" uses the minimum-wage debate to show how each side cites the single study it likes. He observes that "only one side has presented a funnel plot" and argues for looking at the whole body of evidence. [paraphrase, partial verbatim] https://slatestarcodex.com/2014/12/12/beware-the-man-of-one-study/

*Applied:* the Nakba before/after pair is one example. Present it as an example, state that the 2021 text also took a position, and set the counter-direction numbers next to it, not below it.

## 9. Check your own reaction to the number before you phrase it.

Harford's first rule, "Search your feelings": notice how a statistic makes you feel, because wishful thinking can turn a dubious number into solid evidence, or solid evidence into fake news. [paraphrase] https://www.goodreads.com/en/book/show/201280067-how-to-make-the-world-add-up

*Applied:* words like "front door", "redressed" and "wave" carry feeling, either alarm or reassurance, that the counts do not. Reader 1 heard intent in "redressed". Use words that describe what was measured.

## 10. Use neutral, defined terms. Define once, then use the same term every time.

The Economist style guide opens with Orwell's rules, including: never use a figure of speech "you are used to seeing in print", and prefer the plain word. [paraphrase] https://cdn.static-economist.com/sites/default/files/pdfs/style_guide_12.pdf

*Applied:* keep the existing definition of *critical vocabulary* word for word, and do not alternate it with "loaded words", "words of accusation" or "charges". Define "comparison articles" and "opening paragraph" once.

## 11. A metaphor must carry structure the reader needs. Otherwise cut it.

The same guide notes that a fresh metaphor used in moderation can enliven writing, while stale metaphors disguise an absence of thought. [paraphrase] https://cdn.static-economist.com/sites/default/files/pdfs/style_guide_12.pdf. Gelman and Loken's "garden of forking paths" earns its place because it names a mechanism that has no other short name.

*Applied:* "the shop window" adds no mechanism, since "the opening paragraph is what readers, search engines and AI assistants see first" is already literal and clear. It also implies a dresser, and therefore intent. Use no metaphor.

## 12. Say what would change your mind, concretely.

Ritchie on microplastics: her view could change "a lot" if the evidence changed, and she names what she would need to see, namely real detrimental health effects. On food carbon footprints she says the research is "just very mixed, with no clear winner". [paraphrase, partial verbatim] https://80000hours.org/podcast/episodes/hannah-ritchie-environmental-optimism/ and https://businessforgoodpodcast.com/episodes/ep190-hannah-ritchie-has-some-uncomfortable-truths-about-helping-the-planet

*Applied:* name observable things: a renewed rise in the quarterly rate, a site-wide baseline showing the same rise, word-list errors, an exposure figure driven by a few giant pages.

## 13. Disclose methods briefly, in one place, next to the findings.

Pew pairs each short report with a compact methods statement (sample, dates, margin of error) and links to the full methodology. [paraphrase] https://www.pewresearch.org/our-methods/. Healy's *Data Visualization* gives a full section of its first chapter to "Problems of Honesty and Good Judgment". [verbatim section title] https://socviz.co/lookatdata.html

*Applied:* one paragraph covering what was counted, in how many articles, against what, which intervals, and what was held out and withdrawn.

## 14. Colour is for data. Emphasis in text should be typographic and sparing.

Muth: grey suits less important elements, which "makes the highlight colors stand out more", and grey should not be used as just another category colour. [paraphrase] https://www.datawrapper.de/blog/colors and https://www.datawrapper.de/blog/emphasize-with-color-in-data-visualizations. Burn-Murdoch: "a line of red in a sea of grey lines will immediately stand out". [verbatim, as reported] https://gijn.org/stories/data-visualization-storytelling-tips-john-burn-murdoch/

*Applied:* on this page teal means "topic articles". Using teal italics for a slogan line in the headline spends a data colour on rhetoric. Keep colour for the charts and the quote-pair keys.

---

## Quick checklist for any summary text on this page

- Headline: what changed, where, how much. No setup and punchline.
- Every number has its comparison figure; every suggestive result says "suggestive" and why.
- Both directions sit side by side, with numbers.
- No pull-quotes of our own aphorisms, no bolded one-liners.
- No metaphor unless it names a mechanism.
- One methods paragraph; limitations next to it; "what would change this" in concrete, observable terms.
- No em dashes. One term per concept.
