# Design council, round 2: editor-publisher memo

Date: 2026-11-06. Scope: the live page (`page_template.html`, my round-1 running order, now built), plus five new inputs: `angle/ANGLE.md` (audience and rules), `angle/PERP.md`, `angle/OCT7.md`, `orgs/ORGS.md` + `orgs/tests.md`, `who/WHO.md`, `sampling/AUDIT.md`. Three things are still coming: the coordination network graph, the random-Wikipedia baseline, and mass3 (the stratified probability sample that will give the final headline numbers). Every number below is from those files or from SYNTHESIS.md; every quote is verbatim. Placeholders for mass3 are written `[MASS3: …]`. Claims that ORGS.md marks as read from search snippets only carry `[VERIFY]`, because ORGS says every line needs checking against the primary page before publication.

Three corrections the page must absorb before anything else:
- **Hamas.** ANGLE.md says "terrorist" moved out of Hamas's definition. OCT7.md shows that is wrong: from January 2021 on, "terrorist" never held in the first sentence for more than about 2.4 hours (under six hours in three years). What left the definition was "militant", on 12 October 2023. What moved was the designation sentence, from sentence 5 of 20 to sentence 22 of 23. The page must use OCT7's wording, not the brief's.
- **The Israel denial sentence.** The page's #news card quotes "Israel and its allies, including the United States, deny that Israel's actions constitute genocide." That was the 1 October 2026 text. Since 4 November 2026 it reads "Israel has denied that its actions constitute genocide." Date every quote; use the 4 Nov text as "now".
- **Gaza genocide own-voice date.** SYNTHESIS P7 and the SSL card say 2025-10-05 ("per talk"). OCT7 dates the first own-voice version to 21 Sep 2025 and the current sentence to 26 Sep 2025. The coordinator's brief says 26 Sep 2025. Use 26 Sep 2025 and have the builder reconcile the ratchet record before publishing; the "8 one-way steps" count is unaffected.

---

## 1. Where each new finding goes

The round-1 spine stays: Zionism opener, Key findings box, widening, question sections, trust, appendix. Four things change: two new question sections go in early (the charge against Israel; October 7, Hamas and the hostages), "Who wrote it?" becomes "Organised or organic?", and the sampling audit gets a visible home in the trust section plus a numbers convention everywhere.

| New finding | Goes | Replaces or compresses |
|---|---|---|
| **PERP** (who is named as doing harm; 1,731 lead sentences in the 150 most-read articles) | New section `#charge`, directly after the widening (`#andyet` + `#reach`). Title: *What is Israel charged with now, and in whose voice?* Charts: PERP cards 2 and 3 (grave charges stacked by voice; occupation own-voice share, Israel vs Russia/Turkey). | Absorbs the attribution line from `#sourcing` ("most new terms arrived attributed, a few flagship leads later dropped it") and the Gaza genocide staircase. `#sourcing` itself goes to the appendix (its source-class and ADL charts stay there intact). |
| **OCT7** (Hamas definition, designation position, October 7 first sentence and title, hostages, genocide voice, 26 May 2025) | New section `#oct7`, after `#charge`. Title: *October 7, Hamas and the hostages: what the first sentence says now.* Charts: `oct7_01` (Hamas first-sentence step timeline with the five "terrorist" ticks), `oct7_08` (designation position bar), `oct7_03` (October 7 title and first-sentence swimlane), `oct7_04` (hostages small multiples). The `#exact` trace already has a Hamas pick (12 changes); link to it. | Nothing on the page covers this. It compresses the "terrorism thinned out" line in `#against` (which moves here as one sentence with the comparison table from OCT7 card 3). |
| **PERP card 4** (1948 gets an agent: Palestinian-victim sentences with no named perpetrator 62% → 51% → 38%; "Hundreds of thousands of Jews fled or were expelled from Arab states" still agentless) | Into `#palestine` as its second paragraph and a third quote pair (1948 Arab–Israeli War, 2021 vs now). | Replaces the "term or two" sentence about Palestinians / History of Palestine (weak, raw counts) with a coded result. |
| **ORGS + tests + WHO + network graph** | `#spread` is rebuilt as `#organised`: *Organised or organic?* (see section 3). Position unchanged (after `#when`). The appendix `#organic` is folded into it (the co-editing bars and the 30-minute null come up; the hour-of-day polar charts and the 0.000 rows stay in the appendix). | Replaces "Who wrote it?" and the appendix "Signals of coordination". `#spread`'s six panels are kept as the section's first figure. |
| **WHO cards 1 to 4** (14 accounts for 16 traced Zionism changes; 44 insertions / 41 removals of "coloni-", 37 of 41 removals reverted; one account 38.8% of war-window Nakba edits; median top-account flip share 32% topic vs 20% comparison) | Zionism numbers into the opener's `#ziMeans`; the rest into `#organised` as the "concentration" panel. | Replaces the opener's current "at least fourteen editors" sentence with exact figures. |
| **AUDIT** | (a) A "How we chose the articles" box in the trust section (`#limits`), using the AUDIT text verbatim. (b) A new figure in `#board`: `sampling/chart_data/03_weighted_vs_unweighted.json` as a dot-and-whisker, "Same data, three honest ways to count". (c) The numbers convention in section 4, applied to the Key findings box, `#andyet`, `#reach`, `#news`, `#palestine`. (d) `#reach` gains one sentence: against live wars the reading share is about the same. | Replaces every "whole topic", "all 4,642 topic articles" and "three times the comparison" on the page. Comparison count 5,678 becomes 5,670. |
| **Random-Wikipedia baseline** (coming) | One row in the `#board` dot chart and one sentence in `#andyet`: "against a random draw of Wikipedia, [BASELINE: …]". | Nothing yet. Reserve the slot. |
| **mass3** (coming) | The headline numbers in the Key findings box, `#andyet`, `#reach`, `#news`. Until it lands, every size shows sample and weighted figures side by side (section 4). | The unweighted mass2 sizes as headline figures. |

### New running order

0. Page title and dek (hero H1).
1. `#zionism` One sentence, 292 edits (KEEP, dek rewritten for the audience; WHO figures in `#ziMeans`).
2. `#breathe` The same sentence, any day you choose (KEEP).
3. `#sixty` Key findings (REWRITE, six cards, section 2).
4. `#andyet` + `#reach` Zionism is not alone (REWRITE numbers, section 4).
5. `#charge` NEW. What is Israel charged with now, and in whose voice? (PERP)
6. `#oct7` NEW. October 7, Hamas and the hostages: what the first sentence says now. (OCT7)
7. `#news` Is it just the war? (KEEP; numbers per section 4; replace the Israel denial quote with the 4 Nov 2026 text)
8. `#when` When did it happen, and what set it off? (KEEP; add one sentence: the surge came before the documented campaigns)
9. `#palestine` Did the Palestinian-history articles change too, and how? (KEEP; add PERP card 4)
10. `#organised` NEW, from `#spread` + `#organic` + WHO + ORGS + tests + the network graph. Organised or organic? (section 3)
11. `#crosslang` Did other languages follow? (KEEP, compress the dek to three sentences)
12. `#against` Not every edit went the same way (KEEP, cut to four bullets; the terrorism line moves to `#oct7`)
13. `#board` How far to trust this (KEEP; add the weighted-vs-unweighted figure; `#key` scrolly moves in here as the pre-registered test)
14. `#checks` Does the counter see edits we know happened? (KEEP)
15. `#limits` What this can and cannot tell you (KEEP; add the "How we chose the articles" box and the "not detected is not did not happen" paragraph)
16. `#method` For researchers (KEEP)
Appendix: `#test`, `#sourcing`, `#vocab`, `#ratchet`, `#organic` remainder, `#ledger`. (`#heatmap` and `#editing` cut from the page; both stay in the data lab.)

---

## 2. The Israeli-media framing

The lens is "how the world's reference tells Israel's story". The register is Israeli newsroom: short sentences, the fact first, the exact words of the encyclopedia, no adjectives on the quotes. The accuracy rules are what let the piece survive: every claim at the strength the data give, "documented" / "alleged" / "not detected" said as such, no editor named.

### Page title and dek (hero)

**H1.** How the world's reference now tells Israel's story: English Wikipedia, 2021 to 2026

**Dek.** English Wikipedia is the text millions of people, and the AI assistants they ask, read first. We followed every edit to 4,642 of its articles on Israel, Palestine, Zionism and Judaism for almost six years, and to 5,670 articles on other countries, conflicts and religions, measured the same way. This is what the encyclopedia now says, when it changed, how, and how organised it was.

### Opener dek (`#zionism`)

**Headline (keep).** A Jewish state became "a Jewish homeland through colonization". It took 292 edits.

**Dek.** In January 2021 English Wikipedia defined Zionism as a movement for "the re-establishment of and support for a Jewish state in the territory defined as the historic Land of Israel". Today it is "an ethnic nationalist movement that emerged in late 19th-century Europe to establish and support a Jewish homeland through colonization in the region of Palestine". The word "re-establishment", the claim of return, left the first sentence for the last time on 9 July 2024. "Colonization" was written into the sentence 44 times and taken out 41 times; 37 of those 41 removals were undone. It has stood since 27 August 2026. Between the two definitions lie 292 changes to one sentence, 108 of them reverted, by 455 accounts over the whole article. This is what the fight over the encyclopedia's one-line answer to "what is Zionism?" looks like. It is not the only sentence that changed.

**`#ziMeans` (replace the prose after the generated numbers).** The 16 traced changes that carried each quarter's wording came from 14 different accounts; no account made more than two. In the war period 366 accounts edited the article; the busiest made 17.4% of its 3,279 edits. These were veterans: a median account age of 9.4 years, and no edits from accounts with under 500 edits. A petition against the "colonization" wording drew more than 10,000 signatures in autumn 2024 `[VERIFY]`; a January 2025 discussion kept the sentence, and a one-year moratorium on reopening it followed `[VERIFY]`. The month with the most removals of the word was June 2024, before the petition. Zionism is one article. The rest of this report asks what else the encyclopedia now says about Israel, and who wrote it.

### Key findings box (`#sixty`, six cards; big number, one line, link down)

1. **"Israel began committing genocide."** The encyclopedia states this as fact, in its own voice, in the opening section of the article on Israel (42.9 million views since 2021) and on Benjamin Netanyahu ("Netanyahu's government has been orchestrating the Gaza genocide", 26.2 million). In the 150 most-read articles on the subject, sentences charging Israel with genocide went from 0 in 2021 and 0 in July 2023 to 8 now; two are in Wikipedia's voice, five are attributed to scholars and organisations, one is Israel's denial. No sentence charges Hamas or Palestinians with genocide. → `#charge`

2. **0 → 8 → 2.** The same count, as the card's number. (Merge with card 1 if the design needs five cards; keep the number.) Alternative card: **46% → 80%**: the share of "occupation" sentences stated as fact rather than attributed. The same move happened to Russia in Crimea (25% → 74%), so this one is not unique to Israel. → `#charge`

3. **Five days.** "Militant" left Hamas's definition on 12 October 2023, in the month its article was read 8,236,474 times. Hamas is now "a Sunni Islamist Palestinian nationalist political organisation with a military wing". "Terrorist" was written into the definition five times and never held longer than about 2.4 hours. The sentence listing the countries that designate Hamas moved from sentence 5 of 20 to sentence 22 of 23; since 31 October 2026 it names no country: "Several countries have designated Hamas as a terrorist organisation." The Hamas and Israel opening sections do not mention the hostages. → `#oct7`

4. **"By Zionists."** The Nakba is now "the ethnic cleansing of Palestinian Arabs by Zionists", in Wikipedia's voice, present tense. Across the most-read articles, sentences about Palestinian victims that name no perpetrator fell from 62% to 38%; the exodus of Jews from Arab states is still written with no agent: "Hundreds of thousands of Jews fled or were expelled from Arab states". → `#palestine`

5. **Most articles did not change.** Of 4,642 sampled articles, 3.9% gained critical vocabulary in their opening paragraph; weighted to the four subject groups' real size, about 2.5% [2.0, 3.0] `[MASS3: final share]`. Those pages carry 15% of the reading (weighted about 14% [8, 20]) `[MASS3: final share]`. Articles on Judaism did not move. The wave ran through 2024 (about 16 new critical terms per 1,000 edits, against about 7 before the war) and was back to 5 to 6 by 2026. → `#reach`, `#when`

6. **Veterans, and documented canvassing on both sides.** Since the war began, 9.1% of edits to these articles came from accounts with under 500 edits, against 17.2% on comparison articles. Wikipedia's arbitration committee has found off-wiki canvassing promoting a pro-Israel view (email, January 2024) and a pro-Palestinian view (a Discord channel, sanctions December 2024 and April 2025) `[VERIFY]`. Our own tests could not tell any campaign's footprint from chance, and the surge in critical wording came before the Discord channel existed: topic insertions ran at 3.4 times the comparison rate in the 16 weeks after 7 October 2023, and 2.0 times while the channel was active. → `#organised`

The box keeps one line under the cards: *The numbers in cards 5 and 6 are counts across thousands of articles; weighting and sampling can move them (see "How far to trust this"). The sentences in cards 1 to 4 are the encyclopedia's exact text on the dates given; no weighting changes them.*

### Section ledes for the two new sections

**`#charge`. What is Israel charged with now, and in whose voice?**
First sentence: The encyclopedia did not start blaming Israel more often; it changed what it blames Israel for, and in two of its most-read articles it dropped the attribution. Support: In the 150 most-read articles, the share of harm sentences naming Israel, Israelis, Jews or Zionists as the one doing the harm was 23.6% in 2021, 24.1% in July 2023 and 26.4% now, a change inside the margin of error. The charge changed: genocide, 0 sentences in 2021 and July 2023, 8 now, 2 in Wikipedia's own voice; apartheid 0 → 1 → 4, one in own voice; occupation stated as fact rather than attributed 46% → 51% → 80%. The 50 most-read articles on other disputes (Ukraine, Karabakh, Northern Ireland, Kosovo, Cyprus, Kashmir) gained no new genocide charge against any state; their occupation sentences also moved into Wikipedia's voice (25% → 74%, Crimea and northern Cyprus). Caveat line: coded by one reader with a 100-row self-check (98% and 99% precision), not an independent second coder; the 150 articles are the most-read, not a sample.

**`#oct7`. October 7, Hamas and the hostages: what the first sentence says now.**
First sentence: The encyclopedia's one-line answer to "what was October 7?" is "a series of coordinated armed incursions from the blockaded Gaza Strip into the Gaza envelope of southern Israel were carried out by Hamas and several other Palestinian militant groups"; the first sentence has never kept "massacre", "terror", the death toll or the hostages. Support: "massacre" held for about an hour in total, "terror" for 0.2 days, the toll for 1.2 days, the hostages never. The killing is described plainly in paragraph 2 ("massacring civilians in 21 communities") and the lead gives the toll (at least 1,195), the hostages (251) and that 44 governments called it terrorism; since October 2026 the Hannibal Directive is also in the opening section, and a clause calling Israel's response genocide was removed. The Gaza war's first sentence has not named Hamas since 26 May 2025, the day the October 7 article lost "Hamas-led" from its title. Then the Hamas material (five days, designation position, "Several countries") and the comparison table: ISIS and al-Shabaab also lost "terrorist" from their first sentences, so that word is Wikipedia-wide style; what sets Hamas, Hezbollah and PIJ apart is that they are introduced as political or paramilitary bodies while ISIS and al-Qaeda are still "militant organisations", and their designations sit in the last fifth of the lead.

---

## 3. "Organised or organic?": one investigative section

**Yes, merge.** "Who wrote it?" (`#spread`), the appendix "Signals of coordination" (`#organic`), WHO.md, ORGS.md, tests.md and the coming network graph are one question for this audience, and the audience will ask it first: was this done to us, and by whom? Answered in pieces across three sections it reads as evasive. Answered in one section, with the graph in the middle, the documented record on one side and the tests on the other, it reads as an investigation that knows its limits.

**Structure (top to bottom).**
1. Lede: what we can say, in one paragraph, at the strength we can say it.
2. The six panels from `#spread` (established editors, protection, RfCs, categories, links, added text). Kept as they are.
3. **The network graph** (centrepiece). See the spec below.
4. The concentration panel (WHO cards 3 and 4): per key article, flips with hash, distinct accounts, top-1 and top-3 share; one account made 38.8% of war-window Nakba edits; median top-account flip share 32% on topic pages against 20% on comparison pages; insertions and removals done by largely separate accounts (318 only inserted, 296 only removed, 59 both), and the comparison group shows the same split.
5. **The public record, documented and alleged**: the ORGS table reduced to the rows that matter, each tagged Documented / Alleged / Not shown, both sides, dated. `[VERIFY]` on every row until the primary pages are read.
6. **The footprint tests** (tests.md): the period table (0.51 / 3.44 / 2.01 / 1.84 / 0.82), the joint test (mean ratio 1.01, p = 0.53), and the power line.
7. Closing paragraph: "not detected" is not "did not happen", and why.

**Lede text.** The edits were made by long-standing accounts, in small groups per page, with insertions and removals done by different hands, and a pool of regulars moving across the hot pages: nine accounts changed the first sentence of three or more key articles, against none on comparison articles. Wikipedia's arbitration committee has documented off-wiki canvassing on both sides of this subject `[VERIFY]`. Our data cannot see off-wiki channels. What it can see is timing and footprint, and there the record is clear in one direction only: the wave of critical wording began in the 16 weeks after 7 October 2023, before the documented pro-Palestinian channel existed, and no campaign, exposure or sanction date leaves a mark we can tell from chance. That is a low-power test; it would need the rate to fall to a fifth or rise fourfold to show.

**The network graph: what it must do.**
- Nodes are anonymous account hashes; edges connect accounts that edited different articles in sync beyond a chance baseline (the baseline must be stated on the figure: shuffled timing, same accounts and articles). Edge colour: insert / remove direction. Node colour: community (algorithmic). A time control with the Discord window (reported active Feb to Sep 2024) marked so the reader can see whether community density changes inside it.
- It must show the comparison group in the same way, side by side or toggled, or it says nothing.
- It must print its own null if that is the result: "no community beyond chance" is a finding, and it agrees with the 30-minute test (zero recurring pairs within 30 minutes on five or more articles).
- It must reconcile its edge definition with that null in one sentence on the figure, because readers will ask why the earlier test found nothing and the graph shows lines.

**What it must not do.**
- No node labels, no "ringleader" callouts, no sizing that invites unmasking, no overlay of accounts named by press reports or by the ADL. ORGS and WHO are explicit: hashes are never linked to names, and the public record "does not map onto our measured edits".
- No caption that equates a community with an organisation, a side, or the Discord channel. A community is accounts that edit together; shared watchlists and subject expertise produce the same pattern (WHO card 8).
- No arrow from the graph to the content: "this community wrote the genocide sentence" is not something the data can say, and must not be implied by placing the graph next to the quotes.
- Not "coordinated editing fell 95%" (ADL, alleged; our data cannot attribute the 2024 → 2025 fall, which is consistent with sanctions, saturation and the war's tempo alike).
- Not the "8,000 articles" figure (likely the Discord's 8,000 members; ORGS lists it under likely errors), and nothing on Israeli government "Wikipedia operations" (no documented Wikipedia editing; the 2025 contracts concern web and AI content).

**What the section must claim, in these words.** Documented: ArbCom's January 2024 finding of pro-Israel email canvassing and proxying; ArbCom's December 2024 and April 2025 sanctions for editing after off-wiki canvassing on the Tech for Palestine Discord channel and for further off-wiki coordination; PIA5's roughly eight topic bans on both camps, on conduct grounds, not a coordination finding; the 2008 CAMERA list and the 2010 Yesha / My Israel course `[VERIFY all]`. Alleged: that about 40 (Pirate Wires) or about 30 (ADL) editors acted as one group and reshaped coverage; the WMF called the ADL's conclusions flawed. Not detected: a footprint from any initiative, with the power line. Firm: the surge came first.

---

## 4. Showing the sampling correction without killing the story

The audit says two things: weighting the sample to the real size of the four subject groups roughly halves the article-share results, and matching on prominence grows them; the best combined estimate is +1.8 per 10,000 words and +1.9 points, smaller than published and clearly non-zero. Reader exposure barely moves (15% → 13.7%), Judaism ≈ 0 is untouched, the wave and the editor composition are untouched. Against other live wars the exposure gap disappears (15% vs 14.1%).

The story survives because the story is not "more than Ukraine". It is what the encyclopedia now says about Israel, in which voice, when it was written, and by whom. Weighting cannot change a sentence. So:

**Rule 1: quantities carry two numbers; quotes carry a date.** Every article-share or rate from mass2 appears as "sample X; weighted to the population about Y [CI]" until mass3 replaces both with one figure. Every quote appears with its revision date. The Key findings box says this in one line under the cards (section 2).

**Rule 2: the headline sizes change now, not later.** On the page today:
- "3.9% of articles, 15% of reading" → "3.9% of the 4,642 sampled articles (about 2.5% [2.0, 3.0] weighted to the four groups' population) carry 15% of topic reading (weighted about 14% [8, 20])". Comparison: 1.5% and 5% (weighted 1.3% and 3.4%).
- "three times the comparison level" → "about four times the pooled comparison, and about the same as other live wars: against Ukraine, Russia, Armenia and Azerbaijan the share of reading on changed opening paragraphs is 14.1%".
- "89%" → "about 80 to 90%" (weighted variants 81% to 84%; the unstable 123% ratio is not shown, the figure's note says why).
- "+3.6 points on the sealed half" → "+3.6 points on the sealed half (+2.6 [0.5, 4.9] weighted)".
- "Israel and Palestine projects are 61% of articles" → "67% of the population, 60% of the sample".
- "all 4,642 topic articles", "the whole topic" → "the 4,642 sampled Top-, High- and Mid-importance articles of four WikiProjects". Comparison 5,670.

**Rule 3: one figure shows the correction, in the trust section.** `03_weighted_vs_unweighted.json` as a dot-and-whisker: five rows (a, b, c, d, e), three dots each (unweighted, design-weighted, matched), with the population-weighted-and-matched combined estimate marked. Title: "Same data, three honest ways to count". Caption: "Weighting to the real size of the subject groups shrinks the article-level sizes by about half. Matching articles of similar prominence grows them. The direction never changes. Reader exposure and the Judaism result do not move." Add the random-Wikipedia row when it lands.

**Rule 4: the "How we chose the articles" box** (AUDIT section 6, verbatim) sits in `#limits`, with its two limits kept: against other active conflicts the gap is smaller and the reading share about the same; the 25 to 40 traced articles were chosen because they are contested and show how change happened, not how much.

**Rule 5: `#reach` says the live-wars comparison in its own voice**, not in a footnote: "Other live wars show the same tilt toward their most-read pages. What is specific to this subject is not the share of reading. It is what the opening paragraphs now say."

**Rule 6: mass3 is the last word.** Mark every `[MASS3]` placeholder and a single build switch that swaps sample/weighted pairs for the final figure. Do not publish "final" numbers twice.

---

## 5. What to cut

- **`#key` scrolly from the main line.** It is the pre-registered null and belongs in the trust section, as the first figure under "The rule we wrote down first". The widening band keeps one sentence on it.
- **`#heatmap` and `#editing` from the page.** Both are in the data lab; both say "the other articles moved more", which is now said once, properly, in the trust figure.
- **`#sourcing` to the appendix**, with its attribution finding moved into `#charge` as one sentence (attributed share 21% → 25% in topic articles, comparison flat at 17%; a few flagship leads later dropped the attribution).
- **`#against` to four bullets**: antisemitism 37 → 54 opening paragraphs; 61 terms out against 223 in; the Israeli settlement hedge ("but Israel disputes this"); "Zionism as settler colonialism" pulled back to "some scholars". The terrorism line goes to `#oct7`, where it is told properly with the comparison table.
- **`#crosslang` dek to three sentences**; the chart stays.
- **The current `#organic` section**: only the co-editing bars and the 30-minute null come up into `#organised`; the hour-of-day polar charts and the deep-panel 0.000 rows stay in the appendix.
- **Any sentence that implies motive**: "quietly", "slipped in", "hijacked". The ORGS and WHO files are careful; the page must be as careful.
- **The brief's own phrasing** "terrorist moved out of the definition" (wrong) and the 1 Oct 2026 Israel denial quote (superseded).

Target length of the main line: about 14 minutes, two more than round 1, because two sections of exact quotes were added and three sections of nulls were removed.
