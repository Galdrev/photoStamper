# Flash edition: plan (owner request, after QA rounds 6–7 and the final publish)

1. Freeze the full report as the "research edition": tag the commit (research-edition-v1), copy the built page and all patterns into archive/research_edition/, keep the published artifact as is (link it from the flash edition as "Full research").
2. New "flash edition": a separate template (page_flash_template.html + build target), same data, same visuals, same design language.
3. Cut round 1:
   - two editorial agents, independent and blind to each other (owner merged two of the three): (a) a headline & visual editor (TV news desk + social/visual-first merged: the one-glance shock, the carousel, the quotable cards) and (b) a story editor (magazine/long-read: the arc, merges and splits, what the reader must understand). Each samples from BOTH tabs (story + evidence room) and proposes a cut for the most echo: what to keep, the order, merges and splits of sections, which visuals go into a carousel, and the headline/bottom line for each card;
   - a comprehensiveness & messaging agent checks each proposal: does the message survive, are the data and text faithful, is anything essential missing, are claims still anchored.
   - Editor-in-chief synthesises one cut and builds it.
4. Cut round 2: the same 2 editors (resumed with their memory) + the messaging agent review the built flash edition, then a final synthesis and build.
5. Hard rules carry over: MUSTFIX_owner.md, no unanchored claims, no usernames, the narrative not Wikipedia, no courts framing, no population claims.
6. Publish as a separate artifact; report both links.

## Owner brief for the editors: harsh in what to show
- Goal: a true shock for the Israeli public, so the reader gets what is going on in one simple mental jump.
- Show the hardest-hitting TRUE material first: the starkest then -> now first sentences (Zionism "re-establishment" -> "through colonization"; Israel "began committing genocide" in the encyclopedia's own voice; Nakba "ethnic cleansing ... by Zionists"; Hamas "militant" -> "political organisation"; the hostages never in the first sentence; critical wording lasts, the opposite is undone within a day).
- The shock comes from juxtaposition and the exact words, never from adjectives, loaded framing or overstatement. Each card has one quote/visual that proves its headline on sight.
- Cut anything soft, hedged-to-nothing or merely procedural. Keep exactly one honesty line (what this does and does not show).
- No lies: every number and quote is traceable to the research edition. The messaging/comprehensiveness agent vetoes anything that overstates.

## Focus catchers (owner, for the cut rounds)
- Every then/now in the flash edition shows WHAT changed at a glance: a one-line punch («“Allegations have been made” → “intentional, systematic destruction … carried out by Israel”») plus inline highlighted changed words (blue added, amber removed). Full text is secondary. Applies to tooltips, cards and carousel slides. See MUSTFIX_owner.md item 12.

## Queued after the Hebrew v1 build lands (owner, morph slides in "The charge, everywhere")
- The slow then->now morph is beautiful, but the reader has no way to actually inspect the change. Add reader controls to every morph slide (Arabic, Spanish, ...) and similar then/now visuals:
  - a segmented control: Then · Now · Both (Both = then above, now below, aligned), plus a scrub slider between then and now that the reader can drag;
  - tap/hover on any highlighted phrase shows what it replaced (the old phrase, plus its English rendering);
  - the English rendering line follows the same state.
- Bugs seen in the owner's screenshot (dark mode, Arabic slide): an English gloss chip "the genocide" sits inside the Arabic sentence and breaks the RTL line (move glosses below the line or into the tooltip); large empty space above and below the slide content (the fixed carousel height is too tall for this slide: vertically centre the content or size the carousel to the tallest real slide).
- Apply to both the English and the Hebrew builds.

## Queued: Data lab tab in BOTH flash versions (owner)
- Add the research edition's Data lab (wikitrends/lab/lab.html, lab.js, lab.css; wired in page_template.html via the tabs nav #tabLab, #view-lab and the shared surface ~line 4521) as a tab in the English and Hebrew flash editions: tabs "Flash" (default) and "Data lab".
- Reuse the research lab code as is (build_flash.py inlines it, same way build_page.py does); lazy-init when the tab opens; the flash page's length at rest is unchanged.
- The flash "Every change" / "Explore" buttons may open the lab on the right article (data-intent {"lab":"flip","title":...}) instead of leaving the page.
- Hebrew build: tab labels and lab UI chrome in Hebrew (proofread with the rest); data and quotes stay original.
- Smoke: the tab switches, the lab loads with 0 console errors, and Back/history works, in both languages.

## Queued: replace the 150-tile hero grid (owner: "this visual is meh")
- Problem: 150 equal grey squares with 7 marked reads as "almost nothing", and doesn't show who reads them.
- Replacement: a TREEMAP (or a proportional tile mosaic) of the same 150 most-read opening sections, each tile's AREA = its views (past 12 months; same view source as the Reach bars). Colour as now: stated as fact (solid teal), attributed (outlined), no charge (dim). Label the large tiles with the article name (Israel, Benjamin Netanyahu, Gaza war, ...).
- Headline number computed from the data: "7 of 150 openings carry the charge, and they get X% of the views of all 150" (only if computable from stored views; otherwise keep counts only). A then -> now toggle (Jan 2021 / Jul 2023 / now) animates tiles lighting up (watchable pacing).
- Tap a tile: the article name, its views, the exact charge sentence, own voice vs attributed.
- Same honesty: counts unchanged (0, 0, 7, two as fact); the area encodes reach, said in a one-line key.
- Both English and Hebrew; share-image variant if strong.
