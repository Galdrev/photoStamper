# Text-only edits for the report page (page_template.html)

Scope: headings, ledes (decks), captions and "What this means" lines. No design, layout or chart changes. Every new text uses the FINAL.md terms: **critical vocabulary**, **Jewish-history vocabulary**, **opening paragraph** (never "lead"), **comparison articles**, **Wikipedia's own voice / attributed**, **sealed half**. No "loaded", no em dashes, no p-values, intervals or "per 10,000 words" in reader-facing prose.

Line numbers refer to page_template.html as of 2026-11-05. Ordered by priority.

---

## Priority 1: words that carry a slant or confuse the main result

**1. Scrolly heading (line 750, `#keyH`)**
- Old: `Did loaded words rise faster in the topic articles?`
- New: `On average, did critical vocabulary rise faster than in comparison articles?`

**2. Scrolly deck (line 751)**
- Old: `Scroll to build the chart one layer at a time. Every line counts words like “colonial”, “apartheid”, “genocide” and “occupation” per 10,000 words of text, in one copy of each article every three months.`
- New: `Scroll to build the chart one layer at a time. Each line shows how often critical vocabulary (genocide, apartheid, ethnic cleansing, occupation, colonial, Nakba/expulsion) appears, checked every three months. Higher means the words appear more often in the same amount of text.`

**3. "The twist" deck (line 782)**
- Old: `The average article did not move. So we crawled the whole topic, 4,642 topic articles and 5,678 comparison articles, and asked a different question: not how much the average page changed, but which pages changed, when, and how.`
- New: `The average article barely moved, and the test we fixed in advance found no clear rise. So we collected every article in the topic, 4,642 topic articles and 5,678 comparison articles, and asked a different question: not how much the average page changed, but which pages changed, when, and how. The finding that more topic articles than comparison articles gained critical vocabulary held up on the sealed half of the data: half the articles we had set aside and only checked at the end.`

**4. "The twist" heading (line 781)**
- Old: `And yet: a narrow, heavily read core changed`
- New: `And yet: a small set of heavily read pages changed`

**5. Reach deck (line 789)**
- Old: `Each bar is all of one group: first its articles, then its last 12 months of reading. The dark part is the articles whose opening paragraph gained critical terms (genocide, apartheid, occupation, ethnic cleansing…) between July 2023 and now.`
- New: `The opening paragraph is what readers, search engines and AI assistants see first. Each bar is all of one group: first its articles, then its last 12 months of reading. The dark part is the articles whose opening paragraph gained critical vocabulary between July 2023 and now.`

**6. Reach "What this means" (`#mReach`, in `drawReach()`)**
- Old: `... It is not most topic reading: 83% of topic views land on leads that did not change. Changed pages being read pages is partly how Wikipedia works everywhere, and the extra tilt toward read pages does not survive resampling whole WikiProjects, so treat it as suggestive. An earlier hand-picked sample showed a much larger share because it held nearly all the giant pages and left out the long tail of stubs, villages and biographies that make up most topic articles.`
- New: `... It is not most topic reading: 83% of topic views land on opening paragraphs that did not change. Changed pages being read pages is partly how Wikipedia works everywhere. When we repeat the test treating each Wikipedia subject group as one unit, the extra tilt toward read pages is no longer clear, so treat that part as suggestive. An earlier hand-picked sample showed a much larger share because it held nearly all the giant pages and left out the many very short articles, villages and biographies that make up most topic articles.`

**7. Israel quote label in "News or narrative?" (`#newsQ`, in `drawNews()`)**
- Old: `Recent events · Israel, 2026`
- New: `Recent events · Israel, 2026 · one of the few opening paragraphs that states the label in Wikipedia's own voice; the next sentence gives the denial`

**8. Nakba quote label in "News or narrative?" (`#newsQ`)**
- Old: `Older history · Nakba`
- New: `Older history · Nakba · what the encyclopedia states as its baseline, then and now (the 2021 version also took a position)`

**9. Layer chip and description "EPISTEMICS" (line 733 and every eyebrow chip with class `layer epistemics`)**
- Old: `EPISTEMICS` / `How claims are backed up. Which sources are cited, and whether loaded words are presented as fact or as someone’s claim.`
- New: `SOURCES` / `How claims are backed up. Which sources are cited, and whether critical vocabulary is stated in Wikipedia's own voice or attributed to someone.`

**10. "What this study can tell you", first item (line 722)**
- Old: `Whether words like “colonial”, “apartheid” and “genocide” became more common in these articles.`
- New: `Whether critical vocabulary (genocide, apartheid, colonial…) became more common in these articles, and whether Jewish-history vocabulary (homeland, indigenous, antisemitism…) did too.`

## Priority 2: plain words for the timeline, filter and editors

**11. "When it happened" heading (line 798, `#whenH`)**
- Old: `One wave, and it followed the battles`
- New: `One wave that followed the battles and, as of late 2026, has passed`

**12. "When it happened" deck (line 799)**
- Old: `... the bottom panel is new critical terms going into topic leads. ...`
- New: `... the bottom panel is new critical vocabulary going into topic opening paragraphs. ...`

**13. Half-year bars title and note (lines 804 to 805)**
- Old: `New critical terms per 1,000 topic edits, by half-year` / `all 4,642 topic leads`
- New: `How often an edit added critical vocabulary, by half-year` / `all 4,642 topic opening paragraphs; new terms for every 1,000 edits`

**14. "When it happened" "What this means" (line 810, `#mWhen`)**
- Old: `... topic edits rose 17% against the six weeks before (p=0.001, against 2,000 random dates). After the 25 legal and institutional events (ICJ orders, ICC, UN votes, rights reports, recognitions) they were 0.94× usual, and term insertions showed no effect at all.`
- New: `... topic edits rose 17% against the six weeks before, far more than on 2,000 random dates. After the 25 legal and institutional events (ICJ orders, ICC, UN votes, rights reports, recognitions) editing was slightly below usual, and new critical vocabulary showed no rise at all.`

**15. "News or narrative?" deck (line 817)**
- Old: `A war produces new sentences about the war. So we set aside every lead sentence that names a year from 2022 on, a recent event or recency wording, and measured the extra change again. Most of it was still there.`
- New: `A war produces new sentences about the war. So we set aside every sentence in the opening paragraph that names a year from 2022 on, a recent event or words that mark recent time, and measured the extra change again. Most of it was still there.`

**16. "News or narrative?" chart labels (`#newsFig`, in `drawNews()`)**
- Old: `Where the extra lead change sits, topic minus comparison, after July 2023` / `9,177 leads with all three snapshots` / `+1.98 terms per 10,000 lead words` / `11% · +0.24`
- New: `Where the extra change in opening paragraphs sits, compared with similar articles, after July 2023` / `9,177 opening paragraphs seen at all three dates` / `89% of the extra change` / `11% of the extra change`

**17. "News or narrative?" caption (same function)**
- Old: `Total extra change: +2.22 critical terms per 10,000 words of lead text. Before the war the same filtered difference was +0.14, which is zero within its range.`
- New: `Before the war, the same comparison showed no difference.`

**18. "News or narrative?" "What this means" caution (`#mNews`)**
- Old: `One caution: on the full set the interval that resamples whole WikiProjects crosses zero; on the articles most relevant to the topic, both intervals stay clear of it.`
- New: `One caution: when we treat each Wikipedia subject group as one unit, the result on all articles is no longer clear; on the articles most relevant to the topic it holds either way.`

**19. "How it spread" heading (line 827, `#spreadH`)**
- Old: `Experienced hands, formal process, and the structure of the encyclopedia`
- New: `Long-standing editors, more formal discussion, and new categories and links`

**20. "Established editors" panel text (`drawSpread()`)**
- Old: `Share of war-window edits made by accounts with under 500 edits. Flips by now-blocked accounts matched their share of all editing on the same pages.`
- New: `Share of edits since the war began made by accounts with under 500 edits. Accounts later blocked made no more of these changes than their usual share on the same pages.`

**21. "Links come before words" panel (`drawSpread()`)**
- Old: `+5.6 pp` / `at the same edit volume`; heading `RfCs nearly tripled, on a few pages`
- New: `+5.6 points` / `with the same amount of editing`; heading `Formal discussions (RfCs) nearly tripled, on a few pages`

**22. "How it spread" "What this means" (line 831, `#mSpread`)**
- Old: `<b>What this means:</b> this was not a flood of new accounts. Established editors added text, ...`
- New: `<b>What this means:</b> long-standing accounts made the edits, not a wave of new accounts, and accounts later blocked did no more than usual. That rules out a newcomer flood; it says nothing about intent or off-wiki coordination. Established editors added text, ...` (rest unchanged)

**23. "What we checked and dropped", newcomer item (line 843)**
- Old: `“Fewer newcomers than before the war.” The drop is small and not robust (−2.2 points; the project interval crosses zero).`
- New: `“Fewer newcomers than before the war.” The drop is small (2.2 points) and disappears when we treat each Wikipedia subject group as one unit.`

## Priority 3: consistent terms in lower sections

**24. Ratchet heading and vocabulary deck (lines 931 and 851)**
- Old: `Once a loaded word goes in, does it stay?` / `The scroll chart in the main test adds up seven groups of loaded words.`
- New: `Once critical vocabulary goes in, does it stay?` / `The scroll chart in the main test adds up seven groups of critical vocabulary.`

**25. Article table caption (line 1017) and sourcing deck (line 974)**
- Old: `“Loaded words” means words like colonial, apartheid and genocide. “History words” means words like homeland, indigenous and antisemitism.` / `A loaded word can be stated as fact (“the genocide”) or attributed to someone (“accused of genocide”).`
- New: `“Critical vocabulary” means words like genocide, apartheid, ethnic cleansing, occupation and colonial. “Jewish-history vocabulary” means words like homeland, indigenous and antisemitism.` / `A critical term can be stated in Wikipedia's own voice (“the genocide”) or attributed to someone (“accused of genocide”).`

---

25 edits. Left as is on purpose: the Zionism tug-of-war section (`#breathe`) and the cross-language section (`#crosslang`), whose headings and decks are already plain; the researcher-only captions (robustness rule, method section), which keep their technical terms for specialists.
