# Flash edition v2: build notes (visuals back + round-2 edits)

Built by the editor-in-chief from, in priority order: `visual_critic.md` (TOP 10), `editor_A_r2.md` and `editor_B_r2.md`, then `messaging_check.md`, `PLAN.md` and `qa/MUSTFIX_owner.md` as binding rules. The owner's acceptance test, added mid-build, was: "It has to be cool and not only written info." Every card should lead with something the reader sees or touches.

- Source: `page_flash_template.html` and `build_flash.py`. Build with `cd wikitrends && python build_flash.py OUT.html`.
- Output: `scratchpad/flash/v2/index.html`, 1.99 MB. It begins `<!DOCTYPE html><meta charset="utf-8"><meta name="viewport" …>`.
- Research edition: unchanged. `page_template.html` and `build_page.py` were not edited. `python build_page.py` passes all its assertions, and its output is byte-identical (`cmp`) to `scratchpad/final/out.html`.

## How the visuals came back (no chart was rewritten)

- **Markup.** `build_flash.py` cuts the research edition's own markup out of `page_template.html` by id (outer HTML, balanced tags):
  - inline: `#breathe`, `#xmFig` and `#tierFig`;
  - inside `<template>`s for the play sheet: `#ziFig`, `#o7Fig` and `#xrFig`.
  - Each one fills a `<!--R:id-->` slot in the flash template.
- **Code.** The research JS library is copied in as in v1. The flash calls the research functions as they are: `drawBreathe`/`brMove`, `xmDraw`/`xmTipWire`, `ziInit`/`ziPlay`, `o7Init`/`o7Tab`/`o7Play`, `xrInit`/`xrOpen`/`xrReplay`, `xTokens` (the reader's morph tokens and CSS), `drawTier`, `drawKey`/`keyGo`/`kStat`/`K_STEPS`, `drawXwGG` and `wdiff`/`renderW`.
- **New flash code:**
  - the carousel mechanics;
  - the sheet;
  - the breathe sweep;
  - the grid flip;
  - the morph slides;
  - the posters;
  - the hero tiles;
  - the Nakba lane (the same `flStrip` lane renderer as v1, fed by `R.ratchet`).
- **Lazy init.**
  - `#breathe`, the grid, `#kChart` and `#tierFig` are drawn when they come within 600 px of the screen. Their animations run only when they are on screen.
  - `ziInit`, `o7Init` and `xrInit` run only on the first open of the sheet. Their template is cloned once and guarded by a ready flag.
- **Data slice added to R:**
  - `dates` (for `drawBreathe`);
  - `mass3` (for `drawTier`);
  - `ratchet.articles.Nakba` (the Nakba lane);
  - `langs`, sliced: 11 editions; 5 columns (genocide, Zionism as colonization, apartheid, October 7 called terror, Hamas called terrorist); the 6 articles those cells use, with every `k_icj` slot removed; 20 of the 26 moments.
  - The court column and the court moments are not in the page at all.

## Card list as built (phone order)

| Block | Leads with (see / touch) | Text kept |
|---|---|---|
| Hero | Israel quote card ("began committing genocide" highlighted, with the denial line), then **150 tiles**. On view, 7 tiles light up (outline) and 2 fill solid. The 2 solid tiles carry tooltips for Israel and Netanyahu. | H1 (with the "top article" glossary); a 2-line tile caption |
| 1 Zionism | Headline with the changed words highlighted. **#breathe**, full-bleed: one 5.2 s sweep from 2021 to today, then a "◀ Drag through time ▶" pill. Under reduced motion there is no sweep and it starts at today. **▶ Every change, step by step** opens #ziFig. | B8: «Of the 41 removals of "colonization" we can check, 37 were undone.» |
| 2 Nakba | Highlighted headline. A **Nakba lane**: "the destruction of Palestinian society", "ethnic cleansing" and "by Zionists" in and out, plus 15 tappable change ticks with punch, diff and full sentence. | Body (A11 cut); both full sentences behind "Both full sentences ▾" |
| 3 October 7 | A2 headline. Focus line (attacks → armed incursions; the rape sentence). The **October 7 lane**, moved from car2, with the empty hostages lane. **▶ Play the October 7 sentence** opens #o7Fig on its October 7 tab. | Hostage scope line (messaging F3); B12 fairness clause |
| 4 Hamas | Highlighted headline. Hebrew card with "ארגון טרור" / "terror organisation" highlighted (A5). Designation dots for 2021 and the **1 Oct 2026 row** (A5; the stamp is no longer needed). **▶ Play the Hamas sentence** opens #o7Fig on its Hamas tab. | F-required body ("came back three times") |
| Languages | **#xmFig**, full-bleed: 11 × 5 squares that flip from our first copy to now (a staggered card flip, row by row), with a Then → now / Now only / Then only toggle. Tapping a square shows its sentence and our translation; "Open the full sentence" opens the #xrFig reader in the sheet. | Title, and "Tap a square" |
| 5 The charge | A1 headline. A1 short focus line. **Two voice cards side by side**: OWN VOICE, with "carried out by Israel" in blue, against ATTRIBUTED, with "have alleged" in amber. **Carousel A**, rebuilt visual-first: (1) #xwGG title strip; (2) Arabic, morphing then → now, with ▶ Replay and a reader button; (3) Spanish, morphing; (4) Israel vs Netanyahu: denial vs "No denial"; (5) Hebrew, the exception, with a reader button. | none beyond captions |
| 6 How it got there | A6 headline. **Carousel B**: Gaza genocide, Hamas and Zionism lanes, each with "▶ Every change". **#kChart stepped**: the chips Whole period plus the 5 `K_STEPS`, calling `keyGo(i)`, with the `kStat` caption; the overview keeps 13.7 vs 3.8. | The binding scope line on the 254 articles, shortened (A7/B6) |
| 7 Arbitrators | A9 headline. The finding-10 quote card with the Ïvana clause (owner exception). A **meter**: 89 to 100% against "about half by chance", in ink only, with no direction colours. | "Our count" and B10's single no-side line |
| Close | B11 headline. B1 **Why it matters**: 5 view bars. **Carousel C posters**: 6 merged then/now lines in the #ziPair grammar with big mono dates, and a final **#tierFig** slide, captioned with the honesty clause. B2 **score block**: 223/61 and 125/73 as in/out bars, and directly under them, visible, the 1948 and October 7 edits that moved the other way. One honesty line, the B4/A12 "In short" (one sentence), buttons. | |

Every card except the close ends with a B3 one-line transition. The c4 line became a question ("How do the other Wikipedias put it?") because the language grid now sits between c4 and c5. B3's «Then came the charge itself.» follows the grid. The "Full evidence →" links moved into each card's eyebrow row, to save a line per card. All the v1 anchors are kept.

## Applied, by source

### Visual critic TOP 10: all 10 applied
1. **#breathe in card 1:** full-bleed on the phone, auto-sweep once, then the finger. Its height is locked to the longest wording, so the sweep never moves the page. The research comparison box (`brRelease`) is switched off.
2. **Carousel mechanics:**
   - 88% slides with a peek;
   - a fixed height: the slides stretch to the tallest, and nothing re-measures per slide, so the dots and arrows never move. Measured: the heights are identical before and after swiping, in all contexts;
   - a one-time CSS nudge on first view (not under reduced motion);
   - a "Swipe → 1 / 5" pill until the first move;
   - the dots overlaid on the slide's bottom edge;
   - the arrows hidden on touch;
   - keyboard support kept (arrow keys, buttons, dots);
   - tapping a peeking slide goes to it.
3. **Triple quoting cut:**
   - the hero "What changed" box, the c2 blockquote (now behind ▾), the c4 English pair and the c6 "What changed" box are gone;
   - the c1, c2 and c4 focus boxes were replaced by highlighting the changed words inside the headline itself. That keeps the owner's focus catcher (must-fix 12) without repeating the words.
4. **The language grid moment flips from then to now.** See "Skipped" for why it shows 5 columns, not 3.
5. **The play sheet:**
   - a `<dialog>` opened with `showModal()`, plus an explicit Tab trap, Esc, a 44 px "Close ✕" button, and backdrop click to close;
   - focus moves to Close on open and returns to the opener on close;
   - play timers stop on close;
   - `#tip`, `#xmTip` and `#gloss` move into the dialog while it is open, so tooltips inside the top layer work;
   - the sheet holds the real #ziFig, #o7Fig (opened at the right tab) and #xrFig (opened at the right moment).
6. **150-tile hero picture.**
7. **Carousel A rebuilt visual-first**, in the critic's order.
8. **October 7 lane moved into card 3**, with ▶ buttons in c3 and c4.
9. **Close posters plus the #tierFig slide.** The "moved the other way" slide left the carousel for the visible score block (B2).
10. **#kChart stepped with chips.**

- Desktop: the two moments are wide (up to 1000 px).
- The #net network is not built. It was optional, and the messaging check leaves it out of the flash.
- The court grid is out, and the build asserts that no court column or court moment is present.

### Editors A and B (round 2)
- **The must-takes, all applied:**
  - A1: headline, short focus line, blue on "carried out by Israel";
  - A2;
  - A5, plus the Hebrew highlight;
  - B1;
  - B2/A4: the score block with bars and the two opposite edits, visible, not on a last slide;
  - B3;
  - B4/A12: "In short", one sentence, double quotes, the messaging-check hostages wording;
  - B8.
- **Also applied:**
  - A6 and A7 (scope line kept verbatim from "Across the 254…");
  - A9 and B10;
  - A11 and B11;
  - B5, via the tiles;
  - B6: eyebrow "How it got there";
  - B12, in part.
- **A3:** the box was deleted, as A3 asked. The deck was then dropped for length; its 4.6 million figure is in "Why it matters".

### Messaging check (binding): all VETOs and FIXes still hold
- F1: "undone within a day" appears only in its Zionism scope.
- F2: the 64/70 pair is hidden in the #ziFig sheet (`#ziCodes`), and the smoke test scans every sheet tab and all 20 reader moments for vetoed strings.
- F3: hostage scopes.
- F4: almost four.
- F5: no longer used; it is replaced by the 1 Oct row.
- F7: "resistance movement" counterpart.
- F9: Netanyahu's period.
- F10: 37 of 41.
- F11: "most-read pages that changed".
- Veto 1: no unscoped "lasts/undone" frame.
- Veto 2: the dated close headline.
- Veto 4: no "afterthought" and no "the world reads first".
- No sides, and no direction colours on card 7.
- Ïvana appears once (the owner exception).

## Skipped or changed, and why
- **Grid columns: 5, not the critic's 3.** On a 390 px phone, 5 columns fit without a horizontal scroll at 24 px squares. October 7 and Hamas carry the Hebrew contrast the cards build up to. Occupation, hostages and courts are out (the last by owner rule).
- **A4/B2 "cut carousel 3".** The critic wins: the carousel stays, rebuilt as posters (no repeated text blocks) plus the tier chart. Only the opposite-direction edits left it, for the visible score block (B2's honesty point).
- **A8 "cut the title strip slide".** The critic wins: it is slide 1, compacted on the phone to one line per edition.
- **A10 chips.** Superseded: #breathe replaces both the chips and the phase row (critic 1).
- **B7 "battles first in carousel 2".** The critic wins: #kChart is its own stepped figure directly under carousel B. Chips inside a swipe carousel would fight the swipe.
- **B9.** The Hebrew slide keeps only the South Africa case: the Hebrew Hamas "terror organisation" is in card 4, and the October 7 "massacre" line was cut for length.
- **B12.** The fairness clause is kept. The rape sentence lives in card 3's focus line (struck "by Hamas fighters" → "dozens of cases of"), not repeated in the body.
- **A3 deck, and card 5's "stated as fact in the Gaza genocide, Israel and Netanyahu articles" body.** Cut for the screen budget. The tiles (two as fact, with Israel and Netanyahu tooltips) and the two voice cards carry them.
- **Spanish morph slide.** It shows the Spanish original only; the English punch is the caption. The translation is one tap away in the reader. This was cut for slide height.
- **The #hero edit-stream canvas and the #net graph.** Not built (critic: not in the top 10; messaging: no network in the flash).
- **Tension noted:** MUSTFIX 3 removes "low-tier bars presented as findings" from the story layer, yet critic 9 asks for #tierFig. It is used as the picture of the honesty line, not as a finding: the caption is the existing honesty clause, and no tier number is in the flash text.

## Build assertions
All the v1 assertions are kept: quotes, numbers, vetoes, "undone within a day" scope, no names but Ïvana once, evidence anchors, RTL.

Added in v2:
- The 1 Oct 2026 Hamas designation row exists: sentence "22 of 23", starts "Australia, Canada, ", ends "…, and the European Union have designated Hamas as a terrorist organisation." The flash elides the middle with "…".
- `dates` ends 2026-10. `mass3` has its tiers.
- `langs` has 11 editions (the card says "Eleven Wikipedias") and exactly the 5 columns. No `icj` cells, no `k_icj` moments, no court-finding moments.
- Each morph slide's sentence exists, with a then copy where it morphs.
- The three Nakba lane terms are in the stored first sentences, and the latest says "by Zionists".
- Every curly-quoted term the flash *script* draws (lane labels, tooltip heads) is checked against the stored text of its article. Any other quote in the script fails the build.
- Each research slot is present once, each sliced id appears exactly once in the output, and no court grid is in the slices. The visible text of the slices passes the veto list and the no-names list (Ïvana included).
- Result: 73 quoted strings, 50 numbers, 4 RTL runs, all passing.

## Measurements (Playwright, Chromium, web fonts loaded, every lazy piece drawn, carousels at rest)

| View | Screens |
|---|---|
| iPhone 13, 390×844, light / dark / reduced motion | **9.48** (v1: 8.08; critic's reading of v1: 10.3 at 664 px) |
| 1280×900, light / dark | 9.63 |

**Visual vs text share, phone**, measured as the critic did (area share of the page):

| | v1 | v2 |
|---|---|---|
| strict: svg and canvas pixels only | 2% | **8%** |
| graphics: svg/canvas plus HTML-drawn graphics and touch targets (tiles, breathe sentence and strip, grid, morphs, bars, meter, posters, voice cards, ▶ buttons, chips) | 3% | **30%** |
| visual blocks: figure-type boxes (tiles, quote cards, moments, lanes, carousels, chart, score, meter) | 35% | **68%** |

**Per card** (strict / graphics / visual blocks):

| Card | Strict | Graphics | Blocks |
|---|---|---|---|
| Hero | 0% | 15% | 72% |
| 1 Zionism | 8% | 48% | 77% |
| 2 Nakba | 34% | 34% | 45% |
| 3 October 7 | 19% | 23% | 44% |
| 4 Hamas | 0% | 11% | 59% |
| Languages | 0% | 64% | 98% |
| 5 The charge | 0% | 46% | 74% |
| 6 How it got there | 26% | 30% | 77% |
| 7 Arbitrators | 0% | 11% | 44% |
| Close | 0% | 15% | 70% |

These are measured at rest. Off-screen carousel slides are excluded, so the tier chart and four of the five car1 visuals are not counted.

## Smoke test: 282 checks, 0 failures
Run on 5 contexts: iPhone 13 light, dark and reduced motion; 1280 light and dark.
- 0 console errors or warnings, and 0 horizontal overflow, at rest and after interaction.
- **Touch swipe** with CDP touch events on the phone: car1 goes to 2 / 5. On desktop, the next button, dots and the arrow key were used. Carousel heights stay identical across slides.
- **#breathe:**
  - the sweep ends at "Today" and shows the drag hint;
  - a touch drag (phone) or mouse drag (desktop) moves it to 2023;
  - under reduced motion there is no sweep.
- **Play sheet:**
  - #ziFig opens with focus on Close;
  - 40 Tabs stay inside the sheet;
  - the Close button returns focus to the opener and stops playback;
  - Esc closes it;
  - #o7Fig opens on the October 7 tab;
  - the Hebrew slide opens the reader at Hebrew;
  - the grid tip opens the reader.
- **Grid:** a tap shows the Spanish sentence and translation; the Then only toggle works. The Arabic slide morphs then → now.
- **Other interactives:**
  - the #kChart chips: step 1 shows 13.7 and 3.8, step 3 shows Rafah;
  - the #kChart tooltip, by tap on the phone and hover on desktop;
  - the Nakba lane tick tooltip, closed with Esc;
  - the hero tile tooltip;
  - the "top article" glossary;
  - the tiles end at 7 lit and 2 solid.
- **Vetoed strings:** none in `main`, in the #ziFig sheet, in the 3 #o7Fig tabs or in the 20 reader moments.

Screenshots are in `scratchpad/flash/v2/`:
- per-screen tiles `{phone-light,phone-dark,phone-light-rm,desk-light,desk-dark}_sNN.png`;
- **phone contact sheets** `phone-light_contact.png` and `phone-dark_contact.png` (one tile per screen), plus `phone-light-rm_contact.png` and `desk-*_contact.png`;
- interaction frames `*_sheet_{zi,o7,xr}.png`, `*_int_{breathe_drag,grid_tap,kchart,lane_tip}.png` and `*_car1_s2.png`;
- `phone-light_interactions_contact.png`.

The smoke, measuring and contact-sheet scripts are copied there as well.

## Open items
- **Live re-check.** The October 7 clause removal is recent. en.wikipedia.org is still blocked from the sandbox.
- **Card 4 and card 7 are the least visual** (11% graphics). Card 4 leads with the Hebrew card and the designation dots. Card 7's meter is a small picture, deliberately colourless. A Hamas lane in card 4 would duplicate carousel B. #net is excluded for card 7.
- **Hero tiles.** Only the 2 "as fact" tiles map to named articles (Israel, Netanyahu). The 5 attributed tiles are placed illustratively, because the flash slice has no per-article list for them.
- **Research-edition bug, guarded in the flash only.** In #xrFig, hovering a marked word outside its `.x` span throws in `light()` (`el.closest(".x")` is null). The flash stops that event before it reaches the reader. The research edition still has the bug.
- **Overlapping ticks.** On the phone, close ticks still overlap: the Gaza genocide attempts on 10 Oct 2025, and Nakba changes in mid-2024. The top one wins the tap; the sheet's step-through reaches every change.
- **Artifact anchors.** Whether claude.ai passes `#anchor` into the artifact iframe is still untested.
- **Publishing.** v2 is not yet published as an artifact (PLAN step 6).
- **Length.** 9.48 screens leaves almost no room for growth. Anything added should come with a cut.

## v2.1: fidelity re-check and the no-courts legend (messaging agent)
- **Hero label:** "since 4 May 2025" → "now". 4 May 2025 dates the word "genocide", not this exact wording (research #reads note). The Israel poster now reads "then · “genocide” since".
- **Card 3 focus label:** "Oct 2023 → now" → "Oct 2023 / Jan 2024 → now". The rape-sentence "then" is the 1 Jan 2024 copy.
- **Card 5 headline:** "Of October 7, it says “Some have alleged.”" → "Of genocide on October 7, …". The old wording could be read as Wikipedia doubting the attack itself.
- **Carousel B, Hamas slide:** "The words … was gone" → "were gone" (grammar).
- **No-courts rule, flash display only:**
  - the legal code (§) is folded into "attributed" in the grid data (`_fold` in build_flash.py);
  - removed from the flash copy of the grid JS: the "§ court case only" legend entries (inline and full key), the "he → court case only" call-out, and "or now reported as a court case" in the ring key;
  - the A-state wording is now "attributed or disputed";
  - from the coding note: the court-ruling pointer, and the occupation and hostages columns the flash does not show;
  - the Hebrew moment title is now "the Gaza war article does not state the charge";
  - build assertions: no "legal" code or "court case" text in R.langs, no court-case strings in the flash grid JS, no "court" in the sliced grid.
  - langs.json and the research edition are unchanged.
- **Re-check:** every other headline, caption, tooltip string, poster date, morph sentence and sheet entry point matches the stored text and the binding vetoes and fixes. One standing exception: Ïvana is still named once, on the owner's instruction, against PLAN rule 5.
- **Measured:** 9.48 screens on the phone (390×844, fonts loaded) and 9.61 at 1280. The smoke test (282 checks, 5 contexts) gives 282 pass and 0 fail: 0 console errors and 0 overflow. Build: `scratchpad/flash/v3/index.html`.
