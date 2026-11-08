# Editor-in-chief structural cut (2026-11-08)

## Phone screens (Playwright, 390×844, document scroll height ÷ 844, viewport-wrapped build)

| | before | after |
|---|---|---|
| Whole document (story view) | **74.3** | **19.5** |
| Report view only | 73.9 (67.6 before the appendix) | 19.1 |
| Evidence room (separate tab) | n/a | 52 at 390px, 49 at 1280px |

My "before" figure is lower than the brief's estimate of about 90 because I measured with every disclosure closed. The "after" figure uses the same method.

## New story order (screens at 390px)

1. Hero, with a plain scope line (core articles that carry the narrative; the long tail is not the story): 1.1
2. **Zionism**, the step-through timeline as the opener, with the word chips (re-establishment → colonization): 3.6
3. **After the battles**, the re-pointed scrolly (sticky chart plus 5 step cards; details below): 3.8
4. **The charge**: Israel and Netanyahu genocide sentences, quoted: 1.2
5. **October 7 and Hamas**: "armed incursions"; terror designation moved from sentence 5 to 22 of 23 (chart): 1.8
6. **1948 and the Nakba**: 2021 and 2026 first sentences: 1.1
7. **Other languages**: the voice grid (Hebrew and Arabic first; a square opens its sentence in the evidence-room reader): 2.1
8. **Some edits went the other way, far fewer** (61 out against 223 in, plus four real opposite-direction edits): 0.8
9. **Organised or organic?**, with the network graph (anonymous A1…, opens in Network view): 1.9
10. **How far to trust this**: one honesty line plus the can and can't box: 1.2

Mast, tabs and footer take about 0.8. Every story section has a headline, a one-line bottom line, one chart, interactive or quote, and at most about 120 words of prose; Organised is the exception at about 130.

## Owner must-fix 4

- **Court contrast removed** from the story: the #when headline and bottom line, #mWhen, card 4 in takeaways.json, and the #charge text that said "legal events did not raise…". Nothing in the page says "battles, not the court rulings". There was no separate FAQ block in this template.
- **Scrolly re-pointed.** The scrolly now shows weekly new critical terms in the opening paragraphs of the 4,642 core articles (`mass2_01_weekly_timeline_events.json`). Pale bars are terms written in; solid bars are the part still there a week later (`ins7`, now in `R.v3`). Red lines mark battles and escalations; dotted lines mark ceasefires. The ICJ line is gone.
  - The chart animates its time window per card.
  - Each card covers one battle and the dated wording or order change after it. The cards are: Hamas "militant" → "military" (12 Oct 2023); October 7 "attacks" → "incursions" → "armed incursions"; the Hamas opening section tripling in length while its terror mentions fell from 4 to 1; the Nakba "is the ethnic cleansing" (6 Jun 2024); Zionism "through the colonization" (2 Oct 2024; 22 Jun 2025); the Gaza war dropping Hamas (26 May 2025); and the 2025–26 settling dates.
  - Each card also has a computed line: new terms and lasting terms in the 3 weeks from the event, against the 6-week average before it.
  - Every link is phrased as timing ("in the weeks of…", "Timing, not proof of cause").
- **Population claims removed** from the story: averages, the pre-registered test, the population figures and the low-tier bars. The single honesty line is in the trust box.
- **Research-process narration** (holdout, withdrawn measures, pre-specification, resampling, BH) now lives only in the evidence room's Part 2.

## Must-fix 1–3

- #against is rewritten as "Some edits went the other way, far fewer". It shows real opposite-direction edits only: "by Zionist militias" removed; "but Israel disputes this" added; antisemitism mentions 37→54; settler-colonialism attribution pulled back. It also gives the proportion, 61 out against 223 in.
- The Judaism null, "lopsided, not one-sided", and the claim that Jewish ties were "kept" are gone. Jewish ties now appear in the evidence room as mixed evidence with both directions: homeland 5→1 and "re-establishment" lost; 11 strengthened against 6 weakened; land names 11→19.
- The six-findings cards (#sixty) are cut from the page. They repeated the sections and carried the population and courts lines; takeaways.json is cleaned anyway.

## What moved to the evidence room (new "Evidence room" tab, between "The story" and "Data lab")

**Part 1, deeper into the story:**
- Zionism: the full before-and-after pair, the rest of the opening section, and notes.
- The charge: the full chart (#ppFig), counter-examples, and the apartheid, occupation and attribution notes.
- October 7: the three-article stepper (#o7Fig), the nine armed groups chart, and the More text.
- 1948: the Arab–Israeli War quote, links and categories, and the revision trace.
- Languages: the "In their own words" reader (#xrFig), the three sentences, the genocide-article titles chart, and language by language.
- Jewish ties, as mixed evidence.
- Seven sentences, then and now.
- Timing in detail (#when, without the courts clause).
- History, places and people (#news).
- Organised or organic, the full record: the ArbCom list, the timing and footprint tests, the pair tests, cross-language results, and blocs.

**Part 2, method and checks:** the full record and scoreboard (#board, incl. the pre-registered test and dropped results), core and long tail (#reach, the population analysis), samples and limits, method, the counter checks, the any-day sentence, tests, sourcing, cross-language counts, vocabulary, ratchet, coordination, and the ledger.

Routing changes:
- Links and the ledger drawer switch views automatically.
- All views are drawn at full width on load, and a hidden view is redrawn when it is shown after a resize.
- Phone folds no longer apply to the story sections.

## What was cut

- The old pre-registered-average scrolly content: the panel average, the fold-to-one-number step and the ICJ marker. The test itself is still described in the evidence room's #board.
- The #sixty cards.
- Story handoff lines.
- In the story copy of the network: the long how-to-read paragraph, the stats strip (its numbers are now in the deck: 14 linked pairs against about 2 by chance), the time-chip row and the caveat box. "No account is identified" is in the deck.

## ArbCom blocker (round_4 rank 3)

en.wikipedia.org does not resolve from this session (DNS blocked), so the primary case pages could not be fetched. The claim is softened instead:
- Story: "is reported to have sanctioned off-wiki canvassing on both sides; we could not check its case pages".
- Evidence room: items are tagged "As reported", the caption says the case pages were unreachable, and "documented" is replaced by "reported" in the network windows and labels.
- The publication blocker stays open until someone reads the primary pages.

## Claims I could not fully anchor (all phrased as timing or with a caveat)

- When the Hamas designation sentence moved: the copies show sentence 5 of 9 in July 2023 and 22 of 23 in October 2026. The only intermediate evidence is the terror-mention count, 4 (October 2023 copy) to 1 (January 2024 copy). The scrolly states only that.
- The Lebanon-weeks statement that "Nakba" entered the Israel and Hezbollah leads comes from events card EV7 (the 60-lead event panel) and was not re-read from diffs in this pass.
- The language grid still has a "Court ruling overstated" column: editions that say more than the ICJ did. It is evidence about wording, not the battles-versus-courts framing, so I kept it.
- The deferred #charge numerator issue (pre-modern and individual rows) is unchanged. The story deck says only that the share "moved little (23.6% to 26.4%)".

## Checks

- `python build_page.py` passes all assertions. The only build change is `ins7` in `v3_data`.
- Playwright at 390px and 1280px, story and evidence views:
  - 0 console errors and no page-level horizontal overflow. The only wide elements are chips inside their own horizontal scrollers.
  - The Zionism stepper steps.
  - The scrolly activates cards 1–5 in order and the window animates. On phones the chart stays above the cards, so its labels are never covered.
  - A language-grid square opens its sentence in the evidence reader.
  - Network node click fills the detail panel.
  - The October 7 stepper works in the evidence room.
  - Evidence charts render at full width.
  - The story, evidence and lab tabs switch.
- No duplicate ids, and no dead in-page anchors.
