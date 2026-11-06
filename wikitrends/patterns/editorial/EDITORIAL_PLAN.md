# Editorial plan: the report page, rebuilt around the Zionism timeline

Date: 2026-11-06. Inputs: `page_template.html` (section ids as of today), `findings.html`, `notes/takeaways.json`, `patterns/SYNTHESIS.md` (numbers), `patterns/story_sources_langs/cards.md` (exact quotes), `patterns/when_where_what/cards.md` (place articles), `patterns/editorial/sec_*.png` (what the page looks like now).

Rules applied throughout: every number is from SYNTHESIS.md; every quote is verbatim from a data file; no em dashes in new copy (em dashes inside quoted Wikipedia text stay, because the quote is exact); the design, the CSS classes and the chart code are untouched. Section ids are kept so that anchors, `takeaways.json` links and the lab intents keep working.

---

## A. Diagnosis: what does not work now

1. **The page opens with a conclusion, not a scene** (`sec_short.png`). The first screen is a 110-word paragraph of findings plus five cards of statistics ("−0.1 percentage points, with a range of −2.3 to +2.3"). A reader has been told the answer, with intervals, before being shown a single sentence of Wikipedia. Nothing on the first screen is concrete.
2. **The best material is buried in third position** (`sec_zionism.png`). The Zionism timeline, the chip row ("re-establishment REMOVED", "colonization ADDED", "as few Palestinian Arabs as possible ADDED") and the before/after paragraph are the strongest ten seconds on the page. They sit under the summary, under a jump link, with a flat lede ("Zionism is one of the most-read topic pages").
3. **The page title appears after the first section.** In the template the `header.hero` with the H1 ("Did Wikipedia's articles on Jews, Israel and Zionism drift toward an anti-colonial framing?") and the edit-stream canvas comes after `#zionism` (template lines 104 to 118). A visitor scrolling from the top meets the summary, then Zionism, then the title of the report.
4. **Four summaries before the first question.** `#short` (summary paragraph plus "Key findings" cards), `#sixty` ("What we found, in short", six cards; `sec_sixty.png`), `#findings-sec` ("What we found" prose, five numbered items; `sec_findings-sec.png`) and the `canbox` / layer legend all restate the same five results. The 15%, the 89% and the 9.1% each appear three times before any chart beyond Zionism.
5. **"Changes in both directions" is ambiguous** (`sec_short.png`, lower third). It reads as "the two sides" or "the Palestinian articles", and it leads with the Nakba quote, which is the single most charged example on the page, so the block looks like a rebuttal of the Nakba edit. It was meant as "edits that went against the main trend". The Nakba quote belongs in a Palestinian-history story, not in a counter-trend box.
6. **The first analytical section is a null result labelled "the most important chart"** (`sec_key.png`). The scrolly builds for five steps toward "−0.3, the range crosses zero, could be chance". It is followed by `#chance` ("none of the three stands out from chance"), the 27-tile robustness scoreboard (`sec_board.png`) and, later, the full forest plot (`sec_test.png`, hollow dots all the way down). That is three screens of "nothing happened" in the main line, before the reader reaches the twist.
7. **Three more sections are nulls or self-refuting in their own lede.** `#vocab` ends "The other articles moved more" (`sec_vocab.png`); `#heatmap` says "The rise is more widespread among the other articles" (`sec_heatmap.png`); `#ratchet` opens by saying "the ratchet does not describe the topic as a whole" (`sec_ratchet.png`). The charts are good. The placement makes the page argue against itself.
8. **The "What this means" paragraphs hedge faster than they explain.** `#reach` (`sec_reach.png`) spends nine sentences on 15% vs 5%, of which five are caveats. `#spread` repeats "it says nothing about intent" twice within the section. The caveats are right; they need one home (the trust section) rather than a copy under every chart.
9. **The exact-edits section opens on Zionism again and offers 40 picks including Catholic Church, Tibet and Taiwan** (`sec_exact.png`). It should open on the Nakba, which is where the Palestinian-history story is told edit by edit, and the comparison picks should stay but not lead.
10. **"Organic or organised?" is a full screen of 0.000s** (`sec_organic.png`). The one usable sentence ("the same pairs of editors edited one after the other 0.72 times per 10,000 edits on topic articles, 0.35 on comparison") is a signal worth one line in "Who did it?". The rest is appendix.
11. **The reader is asked to learn a taxonomy** (CONTENT / PROCESS / SOURCES chips, the "Three ways to read the record" legend, "Exploratory · not pre-registered" badges) before being told a story. Keep the chips (design), drop the explanatory legend from the main line.
12. **The register wobbles.** "The window display" metaphor (FINAL.md), "gold", "Swipe for more →", "Shuffle it yourself →" sit next to "q = 0.338" and "R8 cluster bootstrap by subgroup". The main line should be calm and plain; p-values and tile codes live in the trust section and the appendix.

---

## B. New running order

Legend: KEEP = section and chart as they are, new title and lede only. REWRITE = same chart, new text and role. MOVE TO APPENDIX = intact, below the fold. CUT = removed from the report view (content folded elsewhere where noted).

| # | Section id | New working title | Purpose (one line) | Action |
|---|---|---|---|---|
| 0 | `header.hero` (H1 + deck only) | *What changed in English Wikipedia's articles on Israel, Palestine, Zionism and Judaism, 2021 to 2026* | Page title and one-sentence dek at the very top; the stream canvas moves to #when. | REWRITE (split: H1 to top, canvas to #when) |
| 1 | `#zionism` | **One sentence, 292 edits: how Wikipedia redefined Zionism** | The opening scene: the before/after paragraph, the chip row, the improved timeline. | REWRITE (opener) |
| 2 | `#breathe` | **The same sentence, any day you choose** | Companion to the scene: drag the strip, read the sentence as it stood. One line of text. | KEEP (moved up, directly after #zionism) |
| 3 | `#sixty` | **Key findings** | The compact box of five numbered findings (big number, one line, link down). Replaces the old summary. | REWRITE (retitle, re-order cards, drop the Zionism card) |
| 4 | `#andyet` band + `#reach` | **Zionism is not alone: 3.9% of 4,642 articles, 15% of the reading** | Widen out: a few hundred pages, most-read among them, Judaism flat, comparison group three times lower. | REWRITE (band text; reach chart kept) |
| 5 | `#key` | **Q1. Is the whole topic drifting, or a few pages?** | The honest null as contrast: the average article did not move; that is why a reader-weighted view was needed. Scrolly kept. | REWRITE |
| 6 | `#news` | **Q2. Is it just the war?** | 89% of the extra change is in sentences about older history and the land; other wars kept their vocabulary inside the war articles. | REWRITE (swap the Nakba quote for West Bank) |
| 7 | `#when` (+ hero canvas) | **Q3. When did it happen, and what set it off?** | One wave through 2024, back to baseline in 2026; battles brought editors, courts did not. | REWRITE (canvas added above the weekly chart) |
| 8 | `#spread` | **Q4. Who wrote it?** | Established accounts, formal discussion, categories and links; no newcomer flood, no blocked-account excess, no sign of scheduling. | REWRITE |
| 9 | NEW `#palestine` (built from `#exact` + quote cards) | **Q5. Did the Palestinian-history articles change too, and how?** | Yes: 1948 retold as ethnic cleansing in Wikipedia's voice, the land renamed, by edits on a few flagship pages and on village pages; some moves pulled back. `#exact` becomes this section's chart, defaulting to Nakba. | REWRITE (`#exact` moved here and retitled; quote cards added using the existing `.news-q` markup) |
| 10 | `#crosslang` | **Q6. Did other languages follow?** | Mostly not: English and Portuguese moved; 'genocide' for Gaza crossed languages, the re-telling of 1948 did not. | KEEP (new lede) |
| 11 | `#sourcing` | **Q7. Did new sources drive it?** | No: the source mix moved by fractions of a point; most new terms arrived attributed; a few flagship leads later dropped the attribution. | REWRITE (lede; charts kept) |
| 12 | `#short` → only its second `.short-b` block, re-homed as `#against` | **Not every edit went the same way** | The counter-trend ledger: antisemitism 37 to 54 leads, 61 terms out against 223 in, attribution up, settlements hedge, settler-colonialism pulled back. No Nakba here. | REWRITE (rename, move, re-fill; see D) |
| 13 | `#board` (+ `#chance` folded in as its first line) | **How far to trust this: the rule we wrote down first, and what survived** | Pre-registration, sealed half, the scoreboard, the shuffle result, what we dropped (`#dropped` aside moves here). | REWRITE (lede), `#chance` CUT as a section, its sentence moved into the board lede |
| 14 | `#checks` | **Does the counter see edits we know happened?** | Validation against dated, reported edits and the masked reading. | KEEP (out of the `howchecked` details, into the trust section) |
| 15 | `#short` details (methods, limits, what would change this, glossary) | **What this can and cannot tell you** | The four `details` blocks and the `canbox`, in one place. | MOVE (into trust section, after #checks) |
| 16 | `#method` | **For researchers: how this was measured** | Unchanged. | KEEP |
| 17 | `#test` | Appendix A. Every word group, compared with similar articles | Forest plot. | MOVE TO APPENDIX |
| 18 | `#vocab` | Appendix B. Each group of words on its own | Small multiples. | MOVE TO APPENDIX |
| 19 | `#heatmap` | Appendix C. Every article as a strip of quarters | Heatmap. | MOVE TO APPENDIX |
| 20 | `#ratchet` | Appendix D. Do added words stay? The battleground pages | Survival curves, key articles only. | MOVE TO APPENDIX |
| 21 | `#editing` | Appendix E. Edits, talk pages, reverts, logged-out users | Four panels plus the cross-article editor bars. | MOVE TO APPENDIX |
| 22 | `#organic` | Appendix F. Signals of coordination, against chance | Whole section, intact, with its "Read this first" box. | MOVE TO APPENDIX |
| 23 | `#ledger` | Appendix G. Every article in the sample | Table. | MOVE TO APPENDIX |
| - | `#findings-sec` | | Prose duplicate of the summary. The "What this cannot tell you" paragraph moves to item 15. | CUT |
| - | `#short` (summary H2, paragraph, "Key findings" cards, definition line) | | Replaced by the opener plus the Key findings box. The definition line moves into the #andyet band. | CUT |
| - | `canbox` + `.layers` legend + `.ledeband` | | Taxonomy and loading-state band. `canbox` content goes to item 15. | CUT from the main line |
| - | `#beyond` band ("Beyond the main test") | | Its warning ("exploratory, not pre-registered") becomes one sentence in the trust lede; the chips on each section stay. | CUT |

Reading time for the main line (items 0 to 13): about 12 minutes, matching STORYLINE.md. Everything a sceptic needs is still on the page, below.

---

## C. New texts

### Page title (header.hero H1 + deck, now at the top)

**H1.** What changed in English Wikipedia's articles on Israel, Palestine, Zionism and Judaism, 2021 to 2026

**Deck.** We followed every edit to 10,320 articles for almost six years: 4,642 about Israel, Palestine, Zionism and Judaism, and 5,678 about other countries, conflicts and religions, measured the same way. This is what moved, where, when, and by whose hand, starting with one sentence.

### Opener: `#zionism`

**Eyebrow.** One sentence, every edit

**Headline.** A Jewish state became "a Jewish homeland through colonization". It took 292 edits.

**Dek.** In January 2021 English Wikipedia defined Zionism as a movement for "the re-establishment of and support for a Jewish state in the territory defined as the historic Land of Israel". Today it is "an ethnic nationalist movement that emerged in late 19th-century Europe to establish and support a Jewish homeland through colonization in the region of Palestine". Between those two sentences lie 292 changes to the first sentence, 108 of them later undone. "Colonial" or "colonization" went in and came out 44 times before it stayed, on 27 August 2026.

**Intro (above the chip row).** Read the two paragraphs first, then the chips: they are the article's own words, removed or added. Then step through the timeline. Every mark is an edit to the first sentence; the grey bars behind are all edits to the article, week by week. Watch what happens after October 2023, and notice that the sentence was not settled until almost three years later.

**`#ziMeans` (keep the generated numbers; replace the sentence that follows them with):** The definition did not change in one stroke. It was written, reverted and rewritten by at least fourteen editors, most of them long-standing accounts, and the version that stuck came after a talk-page discussion, not during the war's busiest week. Zionism is one article. The rest of this report asks whether it is typical.

### Companion: `#breathe`

**Headline.** The same sentence, any day you choose

**One line.** Drag along the strip to read the first sentence as it stood on that day. Amber, struck through, is what 2021 had and today does not; blue is what is new.

### Key findings box: `#sixty` (retitled)

**Eyebrow.** Key findings
**Headline.** Five things the data show, and one it does not

Cards, in this order (card markup unchanged; numbers from SYNTHESIS):

1. **15% of topic reading** lands on pages whose opening paragraph gained critical vocabulary since the war began. Those pages are 3.9% of topic articles. In comparison articles: 1.5% of articles, 5% of reading. → #reach
2. **7 → 16 → 5–6** new critical terms per 1,000 topic edits: before the war, through 2024, in 2026. One wave, now past. Battles brought editors in; court rulings did not. → #when
3. **89%** of the extra change in opening paragraphs is in sentences that are not about recent events. The story moved back to 1948 and to the land. → #news
4. **9.1%** of topic edits since the war began came from accounts with under 500 edits, against 17.2% in comparison articles. Long-standing editors, not a wave of new accounts. → #spread
5. **−0.1 points**: Judaism articles changed exactly as much as comparison articles. The change is in the Israel and Palestine articles. → #key
6. (the "does not" card) **Not supported**: the one test we fixed in advance, an average over articles, found no extra rise (−0.30 per 10,000 words, range −2.7 to +1.7). Counting articles hides what counting readers shows. → #key

Drop the current sixth card (the Zionism quote pair): it now opens the page.

### Widening: `#andyet` band + `#reach`

**Eyebrow.** The pattern · Full crawl, 10,320 articles

**Headline.** Zionism is not alone: a few hundred pages, and the ones people read

**Band text.** We collected every English Wikipedia article in the topic, 4,642 of them, and 5,678 comparison articles on other countries, conflicts and religions. Most topic articles did not change: 85.1% ended the period with exactly the same count of critical vocabulary as they started. Articles on Judaism moved no more than comparison articles (the difference is −0.1 percentage points, a range of −2.3 to +2.3). The change sits in the Israel and Palestine articles, which are 61% of the topic and supplied 84% of the added terms, and inside them it is steep: the top 40 articles, 1% of the topic, supplied 38% of all new terms. More topic articles than comparison articles gained critical vocabulary after October 2023, by 3.6 percentage points, and that held on the half of the data we had sealed until the end.

*Critical vocabulary:* words from the legal and historical charges made against Israel, such as genocide, apartheid, ethnic cleansing, occupation, colonial, Nakba/expulsion. We counted Jewish-history vocabulary (homeland, indigenous, antisemitism) the same way.

**`#reach` headline.** The changed pages are 3.9% of topic articles and 15% of topic reading

**`#reach` lede.** The opening paragraph is what readers, search snippets and AI assistants see first. Each pair of bars is one group: first all its articles, then all its reading over the last 12 months. The dark part is the pages whose opening paragraph gained critical vocabulary since July 2023. Topic: 3.9% of articles, 15% of reading. Comparison: 1.5% and 5%. The five most-read gainers are Benjamin Netanyahu (7.0M views), Israel (4.6M), Palestine (2.4M), Zionism (1.8M) and Hamas (1.3M).

**`#mReach` (replace).** Three times the comparison level, on both of our ranges. It is not most topic reading: 83% of topic views land on opening paragraphs that did not change. Whether topic pages tilt more steeply toward well-read pages than comparison pages do is suggestive, not established.

### Q1: `#key`

**Headline.** Is the whole topic drifting, or a few pages?

**First sentence.** A few pages: the average article did not move, and the test we wrote down before collecting data says so.

**Support.** Across 332 topic and 90 comparison articles followed every quarter, critical vocabulary in the full text rose by 1.3 per 10,000 words in the topic articles and 1.6 in the comparison articles; the extra change is −0.30, with a range of −2.7 to +1.7. Scroll to build that chart layer by layer. It is the reason this report counts readers and pages, not averages: a change in a few hundred opening paragraphs is invisible to an average over thousands of articles.

### Q2: `#news`

**Headline.** Is it just the war?

**First sentence.** No: set aside every opening-paragraph sentence about events since 2022 and 89% of the extra change is still there.

**Support.** After July 2023 the extra change in critical vocabulary in opening paragraphs, topic minus comparison, was +2.22 per 10,000 words; without the sentences about recent events it was +1.98. Before the war the same comparison showed no difference. Other wars get their own vocabulary waves, but theirs stayed inside the war articles: Tigray's critical hits went 0, 1, 8, 12, 19, 21 over six quarters and then flat, and did not spread to Ethiopian history or place pages. Here the change left the war articles for history, places and people: place articles gaining critical terms went from 1.6% a year before the war to 4.6% after.

**Quote cards (replace the Nakba card; keep Israel):**
- *Older history and the land · West Bank.* 2021-04-02: "The West Bank (... HaGadah HaMa'aravit or Yehuda VeShomron) is a landlocked territory near the Mediterranean coast of Western Asia, bordered by Jordan ... and by Israel to the south, west and north." 2026-04-03: "... is the larger of the two Palestinian territories (the other being the Gaza Strip) that make up Palestine."
- *Recent events · Israel, 2026, one of the few opening paragraphs that states the label in Wikipedia's own voice; the next sentence gives the denial.* "After the Hamas-led October 7 attacks, Israel began committing genocide against Palestinians in Gaza. Israel and its allies, including the United States, deny that Israel's actions constitute genocide."

### Q3: `#when`

**Headline.** When did it happen, and what set it off?

**First sentence.** One wave: new critical terms per 1,000 topic edits ran at about 7 before the war, 13.5 in late 2023, 16.0 and 15.9 through 2024, then 10.8, 8.2, and 5.1 and 5.9 in 2026, at or below the pre-war rate.

**Support.** Military escalations brought the editors: in the three weeks after each of 24 escalations, topic edits rose 17% against the six weeks before, far more than after 2,000 random dates. After the 25 legal and institutional events (ICJ orders, ICC, UN votes, rights reports, recognitions) editing was 0.94 times usual and new critical vocabulary showed no rise at all; after the ICJ provisional measures order of 26 January 2024, topic edits went from 482 to 466 a week. The fight cooled, with a few last decisions: Zionism's first sentence settled on 27 August 2026 and Israel's on 4 September 2026.

(The hero stream canvas sits above the weekly chart with its existing caption: each row an article, each mark an edit, the red line 7 October 2023.)

### Q4: `#spread`

**Headline.** Who wrote it?

**First sentence.** Long-standing accounts: since the war began, 9.1% of topic edits came from accounts with under 500 edits, against 17.2% on comparison pages, and accounts later blocked made 13.7% of the critical-term insertions against a 12.3% share of all editing on the same pages, which is no excess.

**Support.** The same pages gained formal process and structure: extended-confirmed protection went from 10.9% of topic pages in 2021 to 31.1% now (comparison 0.7% to 5.0%); formal discussions rose from 0.29 to 0.79 per 100 articles a year and sit on 51 pages, with Gaza genocide (21), October 7 attacks (13), Zionism (13) and Hamas (8) holding nearly half; framing categories were added to 7.2% of topic articles against 2.2% of comparison articles; and pages already linking to a core concept such as the Nakba picked up its vocabulary 5.6 points more often at the same editing volume. Most of the uncontested change landed on quiet pages: among busy topic articles, those with few reverts gained critical terms 28.5% of the time, against 13% for contested ones. We found no editor pairs editing the same page within 30 minutes on five or more articles. None of this can see intent or coordination off Wikipedia.

### Q5: NEW `#palestine` (chart: `#exact` moved here, default pick Nakba)

**Headline.** Did the Palestinian-history articles change too, and how?

**First sentence.** Yes, and this is where the biggest change in the story is: 1948 is now told as ethnic cleansing in Wikipedia's own voice, the land is named Palestine, and the change reached village pages, but it did not run through every Palestinian article and some of it was pulled back.

**Support (three short paragraphs).**

The Nakba article defined its subject in 2021 as "the destruction of Palestinian society and homeland in 1948, and the permanent displacement of a majority of the Palestinian Arabs". By 2026 it reads: "The Nakba (النَّكْبَة) is the ethnic cleansing of Palestinian Arabs by Zionists through their violent displacement and dispossession of land, property, and belongings, along with the destruction of their society and the suppression of their culture, identity, political rights, and national aspirations." "Ethnic cleansing" entered Wikipedia's voice on 24 April 2024; the perpetrator was named in December 2025 ("by Israel"), then changed to "by Zionists" in July 2026; "was" became "is". The 2021 version also took a position. The article gained an infobox whose type field begins "Genocide, ethnic cleansing, forced displacement, dispossession, mass killing, settler colonialism".

The re-telling spread along links and categories. Topic articles linking to Nakba/1948 went from 114 to 127 to 223 across the three snapshots. The categories most often added to topic pages since July 2023 were "1948 Palestinian expulsion and flight" (16), "Zionist political violence" (11) and "Israeli massacres of Palestinians" (10). Of 390 topic place articles, 35 gained Nakba/expulsion wording after July 2023, many of them village pages; the Gaza Strip's opening paragraph now says it "became a refuge for Palestinians who fled or were expelled by Zionist forces in the Nakba", and the West Bank is "the larger of the two Palestinian territories (the other being the Gaza Strip) that make up Palestine".

It was not a sweep. The opening paragraphs of Palestinians, History of Palestine and Palestinian refugees moved by a counted term or two each, and the 1948 expulsion article went the other way: in 2023 its first sentence said Palestinian Arabs "were expelled or fled from their homes by Zionist militias"; since May 2025 it says they "were expelled or fled from their homes", with the paramilitaries named in the next sentence. One thing the data cannot say is how 1948 departures are described, forced or fled: our measure for that failed its precision check and was withdrawn.

**Chart.** `#exact` trace, default pick **Nakba 12**, then **1948 Palestinian expulsion and flight 9**, **West Bank 14**, **Gaza Strip** (if present) and **Mandatory Palestine 10** first in the pick row; the remaining topic and comparison picks follow. The existing "What this means" line (`#mTrace`) is generated and stays.

**Quote cards (`.news-q` markup, two cards):** Nakba 2021 / 2026 (exact text above) and 1948 Palestinian expulsion and flight 2023-07-07 / 2025-05-30 (exact text above). Caption under the pair: "Both articles describe the same year. One moved toward a stated charge; the other removed the agent from its first sentence."

### Q6: `#crosslang`

**Headline.** Did other languages follow?

**First sentence.** Mostly not: in opening paragraphs, English moved by +0.24 critical terms per 1,000 words against its comparison articles and Portuguese by +0.27; the other nine languages averaged +0.06.

**Support.** What crossed languages was the label for the current war: "genocide" entered the Gaza war opening paragraph in 9 of 11 Wikipedias, stated as fact in Spanish, attributed to scholars in English, French and Dutch, framed as accusations in Russian. The re-telling of 1897 to 1948 mostly did not cross: colonial framing was added in English, French, Italian, Dutch and Arabic, and not at all in German, Russian, Hebrew, Spanish or Polish. For Zionism itself, English went from 28.4 to 76.3 critical terms per 10,000 opening-paragraph words; German, French, Spanish, Russian, Hebrew and Polish stayed at zero; Arabic fell from 53.8 to 42.8. This is a story about the English-language community as much as about events.

### Q7: `#sourcing`

**Headline.** Did new sources drive it?

**First sentence.** No: the words changed far more than the sources did.

**Support.** In opening-paragraph citations, scholarly sources went from 43.3% to 48.0% in topic articles and from 49.5% to 55.2% in comparison articles, a Wikipedia-wide trend; Arab and Palestinian press went from 0.7% to 1.1%, pro-Israel advocacy from 1.0% to 0.8%, Israeli press from 6.4% to 5.8%. Most new critical terms arrived attributed: the share with a source named rose from 21% to 25% in topic articles while comparison articles stayed flat at 17%. The exception is a few flagship pages where the attribution was later removed: the Gaza genocide first sentence went from "Allegations have been made that the 2023 Israel–Hamas war constituted a genocide against the Palestinians" to "The Gaza genocide is the ongoing, intentional, and systematic destruction of the Palestinian people in the Gaza Strip carried out by Israel during the Gaza war" in eight one-way steps over 21 months. That is not unique to Gaza: 9 of 11 atrocity articles we checked now state "genocide" in Wikipedia's voice, up from 4 in 2023. Wikipedia's June 2024 ruling on the ADL left no visible step in citations.

### Trust section lede: `#board` (with `#chance` folded in)

**Eyebrow.** How far to trust this

**Headline.** The rule we wrote down first, the half we sealed, and what we dropped

**Lede.** Before seeing the data we wrote down three main tests, six other ways to run each, and a rule for what would count as support. By that rule the hypothesis is not supported: none of the three average tests stands out from chance (an extra change at least as large as the real one turned up in 4,228 of 5,000 label shuffles for the full-text test). Everything above this line comes from a second stage, on the full crawl, which was not pre-registered; its one main result, that more topic articles than comparison articles gained critical vocabulary after October 2023, replicated on the half of the articles we had set aside and only checked at the end (+3.6 percentage points, range 1.7 to 5.6). Where our two kinds of range disagree, we have called the result suggestive. Below are the scoreboard, the checks against edits reported in the news, the earlier results we withdrew, and what this study cannot tell you.

---

## D. Renaming "Changes in both directions"

**New title:** **Not every edit went the same way** (eyebrow: *Against the trend*). The alternative "Edits against the trend" is accurate but reads as a category label; the sentence form answers the question a reader is actually asking at that point, "was it all one way?". The id becomes `#against`.

**Where:** after Q7, immediately before the trust section. It is the hinge between "what we found" and "how far to trust it".

**What goes in it (and nothing else):**

Intro line: *Lopsided, not one-sided. These are the moves that ran against the main trend, counted on the same pages.*

- Antisemitism is mentioned in 54 topic opening paragraphs, up from 37 (18 gained, 1 lost), including the Israel article.
- 61 critical terms left topic opening paragraphs against 223 that entered (comparison: 73 out, 125 in).
- The share of critical terms attributed to a source rose from 21% to 25% in topic articles; comparison stayed at 17%.
- *Israeli settlement*, 2021: "... built in violation of international law on lands occupied by Israel ..." 2026: "... The international community considers Israeli settlements to be illegal under international law, but Israel disputes this."
- *Zionism as settler colonialism* was pulled back from "its founders and early leaders, as well as several scholars" to "some scholars", with the edit summary "more NPOV".
- Terrorism vocabulary fell in topic opening paragraphs by 24% (Hamas: "militant" and "fundamentalist" gone from its first sentence; the terrorist designations stay in the opening paragraph, lower down).

**What moves out of it:** the Nakba quote pair and the line "The 2021 version also took a position" (both to Q5); the "1948 expulsion article dropped 'by Zionist militias'" example (to Q5, where it sits next to the Nakba as the pull-back). The block must not contain a Palestinian-history quote, because that is exactly what made it read as "the other side".

---

## E. The summary at the top: my call

**Become a compact "Key findings" box directly after the Zionism opener, built from the existing `#sixty` cards.** Not at the top, and not the current `#short`.

Reasons:
1. The owner's own reading of the page shows the top summary did not land: it was read as a set of claims, one of them misread. A scene first, then the box, gives the reader a concrete anchor (one sentence, 292 edits) before any abstraction.
2. The `#sixty` cards already have the right shape for a findings box: one big number, one line, one link down. The `#short` cards are paragraphs with ranges; they belong in the trust section and in the deep sections.
3. A box after the opener still serves the skimmer: it is within the first two screens on desktop, and every card links to its chart. Nothing a hurried reader needs is lost.
4. The six-card set makes the null visible without leading with it: card 6 ("Not supported") sits next to card 1 (15%), which is the contrast the whole piece turns on.
5. It removes three of the four duplicate summaries (`#short` text, `#findings-sec`, the summary H2). The page stops repeating itself.

The old summary H2 ("Most articles did not change. The opening paragraphs of a few hundred widely read Israel and Palestine articles did.") is a good sentence. It becomes the first line of the `#andyet` band, where it introduces the widening.

---

## F. Ten publisher's tips

1. **Open every presentation with the chip row, not a chart.** "re-establishment REMOVED, colonization ADDED, as few Palestinian Arabs as possible ADDED" needs no explanation. Give the audience five seconds of silence on it before you speak.
2. **Headline on the sentence, not on the topic.** "One sentence, 292 edits" travels; "Wikipedia framing drift" does not. Avoid "bias", "woke", "anti-colonial" in any headline: the data measure emphasis, not bias, and the first critic will quote the headline back at you.
3. **Say the null yourself, early and plainly.** "Our own first test found nothing on average" is your best credibility line. Critics from the left will say you went fishing after a null; the pre-registered rule, the sealed half and the +3.6 points answer that, so keep them within one scroll of the twist.
4. **Expect the attack "15% is just the big pages".** Pre-empt it: comparison articles show the same tilt (1.5% to 5%), the topic level is three times higher on both ranges, and the extra tilt is called suggestive on the page. Never quote the old 46% figure.
5. **Expect "so it is just the war".** Answer with 89% and with Tigray: other wars' vocabulary stayed inside the war articles; this one moved to 1948, villages and definitions.
6. **Expect "who are these editors" and refuse to go there.** The page says established accounts, no newcomer flood, no blocked-account excess, no sign of scheduling, and that it cannot see intent or off-wiki coordination. Do not speculate beyond that in any Q&A; one speculative sentence will become the story.
7. **Expect "you call the Nakba edit wrong".** The page does not. Say, every time: the 2021 version also took a position; we report what the encyclopedia states as its baseline, not whether it is true. The withdrawn "forced vs fled" measure is your proof you do not push a measure that fails.
8. **Expect "Wikipedia says genocide everywhere now".** Yes: 9 of 11 atrocity leads. Gaza differs in speed and reach, not in the label. Have that number ready; it disarms the "singling out" charge from both directions.
9. **Cut from the main line anything whose lede argues against itself.** The ratchet, the heatmap, the per-word forest plot and the coordination screen are all honest nulls; they are appendix material. A reader who sees "the other articles moved more" three times stops trusting the 15%.
10. **Keep the register flat where the evidence is hot.** The Nakba, Gaza genocide and Israel quotes do the work. Add no adjectives to them, no "shocking", no "quietly". The calm is the authority.

---

## G. Edit list for the builder

Order of operations matters only for items 1 to 4; after that, each item is independent. "Lede" means the `p.deck` under the H2 unless stated. Chart code, CSS and ids are not changed unless the item says so.

1. **`header.hero`**: move the H1 and `p.deck#deck` to the top of `#view-report`, directly after `.mast`. New H1 and deck as in C ("What changed in English Wikipedia's articles ... 2021 to 2026"). Move the `figure.stream` (canvas `#hero`, `#heroLabs`, `figcaption`) into `#when`, above the existing weekly `figure.fig`. Keep `drawHero()` as is.
2. **`#zionism`**: now first section. Eyebrow "One sentence, every edit". H2: "A Jewish state became “a Jewish homeland through colonization”. It took 292 edits." Deck: as in C. Insert the intro paragraph (C) as a `p.deck` between the header and `#ziSum`. In the JS that fills `#ziMeans`, keep the generated numbers and replace the trailing prose with the sentence in C. Remove the `.zi-jump` link (it lived in `#short`). Reconcile the in/out count: SYNTHESIS (D12) says quote 44 in/out cycles; the page currently prints 43 in, 42 out; use whichever the data file supports after the check in SYNTHESIS data note 12, and use the same number in the deck.
3. **`#breathe`**: place directly after `#zionism`. H2 "The same sentence, any day you choose". Replace `.br-hint` with the one line in C. Keep the slider, keys and lab button.
4. **`#sixty`**: place after `#breathe`. Eyebrow "Key findings"; H2 "Five things the data show, and one it does not". Edit `notes/takeaways.json`: reorder to 15% / 7→16→5–6 / 89% / 9.1% / −0.1 / Not supported; delete the Zionism quote card; add the Judaism card (`number` "−0.1 points", `unit` "Judaism articles changed exactly as much as comparison articles", `link_anchor` "key"); set the "Not supported" card's `unit` to "the one test we fixed in advance, an average over articles, found no extra rise" and keep its mini bar. Remove "Swipe for more →" on desktop widths if it is a text node (keep on mobile).
5. **`#andyet` band**: eyebrow "The pattern · Full crawl, 10,320 articles". H2 "Zionism is not alone: a few hundred pages, and the ones people read". Deck: the band text in C, preceded by the sentence "Most articles did not change. The opening paragraphs of a few hundred widely read Israel and Palestine articles did." Move the `p.cap.short-def` (critical vocabulary definition) from `#short` to the end of this band, with the added clause on Jewish-history vocabulary. Remove `.xchip` "The twist".
6. **`#reach`**: directly after the band (keep `margin-top:56px`). Eyebrow "Few pages, many readers". H2 and deck as in C. Replace the `#mReach` string in `drawReach()` with the three sentences in C. Chart and the most-read list unchanged.
7. **`#key`**: eyebrow "Q1". H2 "Is the whole topic drifting, or a few pages?". Deck: first sentence plus support from C, then the existing "Scroll to build the chart ..." instruction. Scrolly step cards and `drawKey()` unchanged. `#mKey` unchanged.
8. **`#chance`**: remove the section from the main line. Its sentence (4,228 of 5,000 shuffles for P2) is now in the `#board` lede. Keep the "Shuffle it yourself" `.inlab` button by moving it into `#board` after `#boardWrap`.
9. **`#news`**: eyebrow "Q2". H2 "Is it just the war?". Deck as in C (first sentence, support). In `drawNews()`, replace the Nakba quote card with the West Bank card (label "Older history and the land · West Bank, 2021 and 2026"; exact text in C). Keep the Israel card and its label. Keep the 89/11 bar and the caption. Replace `#mNews` with: "The war did not mainly produce war coverage. It sent editors back to retell 1897 to 1948 and to rename the land, by adding sentences rather than deleting others. On the articles most relevant to the topic this holds on both of our ranges; on the full set the coarser range crosses zero."
10. **`#when`**: eyebrow "Q3". H2 "When did it happen, and what set it off?". Deck: first sentence and support from C, then the existing "Every week from 2021 to 2026 ..." instruction. Hero canvas figure inserted above the weekly chart (item 1). `#mWhen` unchanged (it already says battles vs courts).
11. **`#spread`**: eyebrow "Q4". H2 "Who wrote it?". Deck as in C. Replace `#mSpread` with: "Each of these is established on its own; we have not separated them as causes. Protection marks the core pages; it is not shown to cause change. None of this can see intent or coordination off Wikipedia." Six panels unchanged.
12. **NEW `#palestine`** (a `section.sec` using the `#exact` markup): move `#exact` here, change its id to `palestine` and add `aria-labelledby="palH"`. Eyebrow "Q5" (keep the CONTENT and PROCESS chips, drop the "Exploratory" xchip). H2 "Did the Palestinian-history articles change too, and how?". Deck: first sentence and the three support paragraphs from C. Insert a `div.news-q` with the two quote cards (Nakba 2021/2026; 1948 Palestinian expulsion and flight 2023/2025) and the caption, between the header and `#trPicks`. In the picks renderer, set the default pick to Nakba and order the first five picks Nakba, 1948 Palestinian expulsion and flight, West Bank, Mandatory Palestine, Gaza Strip (skip any not present); the rest follow in their current order. Add a `p.cap` after `#mTrace`: "How 1948 departures are described, forced or fled, is not measured here; that measure failed its precision check and was withdrawn." Verify the "term or two" sentence against `data/mass_results.json` lead vectors (`l` column sums: Palestinians 0, 1, 2; Palestinian refugees 2, 3, 3; History of Palestine 3, 2, 5) before publishing; if the builder cannot confirm, drop that sentence and keep the 1948 pull-back.
13. **`#crosslang`**: eyebrow "Q6". H2 "Did other languages follow?". Deck as in C, then the existing "Each stripe is one language ..." instruction. Default article stays Zionism. `xlWrap` unchanged.
14. **`#sourcing`**: eyebrow "Q7". H2 "Did new sources drive it?". Deck as in C. Charts unchanged. Remove the "Exploratory" xchip from the eyebrow (the trust lede covers it).
15. **`#against`** (the second `.short-b` block from `#short`, re-homed as its own `section.sec` with `id="against"`): H2 "Not every edit went the same way"; eyebrow "Against the trend"; contents exactly as in D (intro line, six bullets, using the existing `ul.short-row` and `.news-q` markup for the Israeli settlement quote). Remove the Nakba quote pair, the "Neither is 'neutral'" line and the 1948 expulsion example from this block.
16. **`#board`**: eyebrow "How far to trust this". H2 and lede as in C. Move the `aside#dropped` ("What we checked and dropped") to directly after `#boardWrap`. Then the Shuffle button (item 8).
17. **`#checks`**: take it out of `details#howchecked` and place it after `#board`. H2 "Does the counter see edits we know happened?" (unchanged). Deck unchanged.
18. **Limits block**: after `#checks`, a `section.sec` with eyebrow "What this can and cannot tell you", holding, in order: the `canbox` (unchanged text), then the four `details.stats` from `#short` (Methods in one paragraph, Limitations, What would change these conclusions, Glossary), then the "What this cannot tell you" paragraph from `findings.html` as a `p.means`.
19. **`#method`**: unchanged, after item 18.
20. **Appendix band**: replace the `#beyond` band with a band whose eyebrow is "Appendix" and H2 "The rest of the evidence: every word, every article, every check". Deck: "These sections hold the parts of the record that did not change, or that changed the same way in comparison articles. They are here so the main line can be checked."
21. **Appendix sections, in this order, intact, with the "Exploratory" xchips kept:** `#test` (H2 "Every word group, compared with similar articles"), `#vocab` ("Each group of words on its own"), `#heatmap` ("Every article as a strip of quarters"), `#ratchet` ("Do added words stay? The battleground pages only"), `#editing` ("Edits, talk pages, reverts and logged-out users"), `#organic` ("Signals of coordination, measured against chance"), `#ledger` ("Every article in the sample"). Keep `details#howchecked` as the wrapper for `#ledger` only, retitled "The ledger".
22. **CUT**: `#short` (everything not moved in items 4, 5, 15, 18), `#findings-sec` and `#findingsMore`, the `.layers` legend, the `.ledeband`, the `canbox` at its old position (it moves, item 18). Update `findings.html` to contain only the "What this cannot tell you" paragraph and the statistics `details`, since the rest is now on the page.
23. **Nav anchors**: any link to `#short` or `#findings-sec` (including `takeaways.json` `link_anchor` values and the `.more` links) must point to the new ids: `#reach`, `#key`, `#when`, `#news`, `#spread`, `#palestine`, `#against`, `#board`. Search the JS for `"#short"` and `"findings-sec"` before removing.
24. **Global copy check**: search the report view for "loaded word" (replace with "critical vocabulary" except inside chart SVG text), for "lead" used as a noun in reader-facing prose (replace with "opening paragraph"), for em dashes outside quoted Wikipedia text, and for "window display", "gold", "twist" (remove).

---

## Final check for the writer of the next draft

- Numbers that must match SYNTHESIS exactly: 10,320 / 4,642 / 5,678; 85.1%; 3.9% / 15% / 1.5% / 5%; 83%; +3.6 pp [1.7, 5.6]; −0.1 pp [−2.3, +2.3]; 61% / 84%; 40 articles / 1% / 38%; 7 / 13.5 / 16.0 / 15.9 / 10.8 / 8.2 / 5.1 / 5.9; 17% / 0.94x; 482 to 466; 89% / +2.22 / +1.98; 1.6% to 4.6%; 9.1% / 17.2%; 13.7% / 12.3%; 10.9% / 11.5% / 31.1% / 0.7% / 5.0%; 0.29 / 0.79; 51 pages; 21 / 13 / 13 / 8; 7.2% / 2.2%; +5.6 pp; 28.5% / 13%; 114 / 127 / 223; 16 / 11 / 10; 35 of 390; +0.24 / +0.27 / +0.06; 9 of 11; 43.3 / 48.0 / 49.5 / 55.2; 0.7 / 1.1; 1.0 / 0.8; 6.4 / 5.8; 21% / 25% / 17%; 54 / 37; 61 / 223 / 73 / 125; 24%; 4 of 11 / 9 of 11; 292 / 108 / 44; 27 August 2026 / 4 September 2026.
- Quotes that must be verbatim: Zionism 2021 and 2026 first sentences; Nakba 2021 and 2026; 1948 Palestinian expulsion and flight 2023 and 2025; West Bank 2021 and 2026; Gaza Strip "became a refuge ..."; Israel 2026 genocide sentence; Gaza genocide 2024 and 2025; Israeli settlement 2021 and 2026; Zionism as settler colonialism "more NPOV"; the Nakba infobox type field.
- Do not use: the deep-panel 46% figure; "4.4 million views" for the Nakba (not in SYNTHESIS); any "forced vs fled" claim; "most readers"; "colonial" as the topic's signature word (D11: it rises in comparison leads too).
