# Flash edition: visual critique (creative director's read)

Scope: the editing and the visual experience only. I take the facts and the wording rules (MUSTFIX_owner.md, messaging_check.md) as given. Anything below that adds a caption reuses numbers and quotes already printed in the research template, so build_flash.py's quote and number assertions keep passing.

How I looked: Playwright with Chromium, on an iPhone 13 (390×664 CSS viewport, touch) and on a 1280×800 desktop, in light mode. I swiped every carousel with real touch events (CDP `Input.dispatchTouchEvent`), tapped the dots and the arrows, pressed Play on #ziFig, dragged the #breathe strip, tapped cells in #xmFig and nodes in #net, replayed #xrFig, and tabbed through the page.
Screenshots are in `scratchpad/flash/critic/`:
- `ph_screen00–10.png`: the flash page, one phone screen per image. `ph_contact0/1.png` are contact sheets of them.
- `ph_car{1,2,3}_s*.png` and `ph_car*_strip.png`: every carousel slide.
- `dk_*.png`: the flash page on desktop.
- `rs_*` / `re_*`: research figures, story tab and evidence tab.
- `int_*.png`: interaction frames (Zionism play, the scrolly steps, a network tap, a grid tap, the breathe drag, the xr replay, the edit stream). `cs_*.png` are contact sheets of them.

Measured lengths:

| Page | Phone | Desktop |
|---|---|---|
| Flash | 6,818 px = **10.3 screens** | 7,013 px = 8.8 screens |
| Research, story tab | 23.4 screens | |
| Research, evidence tab | 81 screens, with nothing unfolded | |

**Verdict on the owner's complaint: mostly right.**
- The flash keeps the research edition's words and drops most of its pictures.
- Of the research edition's eight 4–5 "wow" pieces, the flash keeps two, and keeps them only in cut-down form:
  - the step-through timelines, reduced to static lanes;
  - the weekly chart, without its steps.
- The best phone interaction in the whole project, the #breathe "drag through time" sentence, is absent. In the research edition it is buried about 47,000 px down the evidence tab.
- One correction to the complaint: a carousel alone will not fix this. Two of the three existing carousels already *are* carousels, and they are stacked text. What the page lacks is visual-first slides and one or two full-bleed moments.

---

## 1. INVENTORY

Wow is scored 1–5 for a general reader on a phone. Flash status: **full**, **cut** (cut down) or **absent**.

### Story tab

| # | Element id | What it is | In flash? | Wow |
|---|---|---|---|---|
| S1 | `#ziFig` (`#ziChart`, `#ziPhases`, `#ziPlay`, `#ziTrk`, `#ziMoments`, before/after panes) | Zionism step-through timeline. Weekly edits, the "colonial" and "re-establishment" presence lanes, every-change ticks, 5 phases. You play or step through 292 changes and the before/after sentence updates. `ziInit`/`ziPlay`/`ziGo`/`ziSync`. | **cut**: static 4-box phase row `#flPh` (`flPhases`) and a 3-lane static strip `#stZI` (`flZi`) as car2 slide 4. No play, no sentence. | 5 on desktop, 4 on phone (the figure is 2,269 px tall on phone, 3.4 screens: `zi_crop.png`) |
| S2 | `#ziSum` | The Zionism "what changed" chips (removed/added words) | **full** (`ziSummary`) | 2 |
| S3 | `#oct7` figure (`#o7Pos`) | Hamas terror designation: a dot on a 0–1 "position in the opening" track per date, sentence 5 → 22 | **cut**: 2 of 4 rows (`flPos`, c4) | 3 |
| S4 | `#charge` | Israel and Netanyahu quote cards ("no denial") | **full**: hero card and car1 slide 1 | 2 |
| S5 | `#kChart` + `#stepsK` | Sticky scrolly weekly chart of new critical terms, 5 steps (`K_STEPS`, `keyInit`/`keyGo`/`drawKey`/`kStat`). The window zooms on each step (`int_scrolly0/2.png`). | **cut**: one static whole-period view in car2 slide 5, no steps | 4 |
| S6 | `#against` | "Other direction" text with inline diffs | **cut**: car3 slide 7 | 1 |
| S7 | `#palestine` | Nakba then/now card with diffs | **full** (c2) | 2 |
| S8 | `#xmFig` (`xmInit`/`xmDraw`/`xmTipWire`/`xmHow`, `XM.mode` then/now/both) | Language voice grid: 11 editions × 7 claims; solid, striped or dashed squares; tap a square for the exact sentence and translation (`int_xm_tap.png`) | **absent**. Only three of its sentences appear, as text slides in car1. | 4 (3 for the whole grid on a phone; 5 if it "lights up" then → now) |
| S9 | `#net` (`drawNetIn("#net",NETS,true)`, `netGraph`, `netCard`) | Co-editing network: clusters, "14 found · 2.15 by chance" bars, tap a node or edge (`int_net_tap.png`) | **absent**. c7 is text only. | 3 |
| S10 | `#trust` | Honesty box | **full** (one line in close) | 1 |

### Evidence tab

| # | Element id | What it is | In flash? | Wow |
|---|---|---|---|---|
| E1 | `#ziPair` (`.wow-grid`) | The whole Zionism opening, 2021 vs now, in big type, word by word: amber strike-through vs blue insert | **cut** to the c1 focus line and chips | 4 |
| E2 | `#trace` (`traceInit`/`traceDraw`) | Nakba: 12 lasting changes traced to single revisions | **absent** | 2 |
| E3 | `#o7Fig` (`o7Init`/`o7Play`/`o7Tab`/`o7Sync`, tabs `#o7Art`) | Step-through timelines for Hamas, October 7 and Gaza genocide: lanes, ticks, play, before/after | **cut**: static lanes `flO7` in car2 slides 1–3. Ticks have tooltips; there is no play. | 4 |
| E4 | `#ev-oct7` figure "Nine armed groups" | Dumbbells for the first "terror" mention, 2021 → now | **absent** | 3 |
| E5 | `#ppFig` / `#ppGrid` (`ppCard`) | Charge bars: who is charged with what, in whose voice, 2021 / Jul 2023 / now | **absent**. Reduced to one sentence ("seven do now, two as fact"). | 2 (dense on a phone) |
| E6 | `#hero` canvas (`drawHero`, `heroHover`) | Edit stream: 513 article rows × weeks; the 7 Oct surge is a visible texture (`int_hero.png`) | **absent** | 4 |
| E7 | `#whenChart` (`whenInit`/`drawWhen`) and `#waveStrip` (`drawWave`) | Weekly chart with event dots; half-year rate bars | **absent** (`#kChart` stands in) | 2 |
| E8 | `#xrFig` (`xrInit`/`xrOpen`/`xrReplay`/`xrMoment`/`xrTime`, `#xrPlay`) | Bilingual morphing reader: original and translation side by side; Replay morphs then → now; 26 moments; tapping a word lights its counterpart | **absent**. Static Arabic, Spanish and Hebrew quotes in car1. | 4 |
| E9 | `#xmIcjFig` (`xmCourt`) | Court rulings overstated, by language | **absent**, and must stay out (no courts framing) | 1 |
| E10 | `figure.xw-gg` / `#xwGG` (`drawXwGG`) | Genocide-article creation strip: bar to creation, tick at the rename, per language | **full** (car1 slide 4) | 3 |
| E11 | `#reads` | Seven sentences, then and now | **full** as car3 | 2 |
| E12 | `#newsFig` (`drawNews`) | "About 80 to 90%" stacked bar: older history vs recent events | **absent** | 2 |
| E13 | `#netEv` (`drawNetIn("#netEv",NETE,false)`) | Evidence network with presets, windows and activity strips | **absent** | 2 |
| E14 | `#orgPeriods`, `#orgVotes`, footprint test | Period ratio chart, voting camps, footprint null | **absent** | 1 |
| E15 | `#coordWrap` (`drawCoord`, `clockSVG`) | Clock-face timing SVGs | **absent** | 2 |
| E16 | `#whoGrid` / `#spreadGrid` (`drawWho`/`drawSpread`) | Who the editors are; protection and process spread | **absent** | 1 |
| E17 | `#board` (`drawBoard`) | Pre-registered scoreboard | **absent** | 1 |
| E18 | `#wvu` | Three honest ways to count (dot ranges) | **absent** | 1 |
| E19 | `#tierFig` (`drawTier`, `R.mass3`) | Tier/reach chart: share gaining critical vocabulary by importance grade, core vs long tail | **absent**. The close says it in a sentence. | 3 |
| E20 | `#reachFig` (`drawReach`) | Bars by reading share; the most-read pages list | **absent** (numbers in close text) | 2 |
| E21 | `#breathe` (`drawBreathe`, `brStrip`, `brMove`, `brRelease`, `brCompare`, `#brRange`) | "The same sentence, any day you choose." Drag along a tick strip and the Zionism first sentence rewrites itself live, with amber strike-throughs and blue inserts (`int_breathe0/1/end.png`) | **absent** | **5** (the best thing on a phone in either edition) |
| E22 | `#forest`, `#chFig` (`drawForest`, `drawChance`) | Main test forest; 5,000 shuffles | **absent** | 1 |
| E23 | `#ratWrap`, `#survFig`, `#beatFig` (`drawRatchet`, `ratSurv`, `ratBeat`) | Survival curves; single-article beat trace | **absent** (car2's lanes tell the same "what lasts" story better) | 3 |
| E24 | `#exploreWrap`, `#xlWrap`, `#trend`/`#minis`, `#ledger` | Sourcing, language counts, vocabulary small multiples, table | **absent** | 1 |
| — | `#gloss`, `#tip`, `#xmTip` | Glossary pop-ups and tooltips | **full** | — |

The research edition's third tab, Data lab (`#view-lab`), is out of scope.

**Count.** Of the research edition's ten pieces scored 4–5 (S1, S5, S8, E1, E3, E6, E8, E21, plus the 4-on-desktop versions), the flash carries:
- 0 in full;
- 3 cut down to a static trace: S1, S5, E3;
- the rest absent.

---

## 2. DIAGNOSIS

### First screen (`ph_screen00.png`)
- **Good:**
  - The headline is strong: "Before the war, no top article charged Israel with genocide. Now Israel's own article does."
  - The Israel quote card proves it on sight, with the blue highlight on "began committing genocide."
- **Weak:** the next 40% of the screen repeats it.
  - The "What changed" box restates the same sentence in italic serif ("Israel began committing genocide against Palestinians in Gaza") on top of the quote just above it.
  - Then a 4-line body paragraph and a scope box.
- **Net:** three text blocks under the headline and no picture. The first screen reads like the top of an op-ed, not a graphics piece.
- **Masthead:** it takes two lines, with "FULL RESEARCH EDITION ↗" wrapped to its own line.

### Rhythm: one skeleton, eight times
Every card has the same stack (`ph_contact0.png`):
1. Eyebrow number.
2. A 3–5 line serif h2 that itself contains the then and now quotes.
3. A "What changed" box with the same quotes.
4. One or two blockquote cards with the same quotes in full.
5. A body paragraph.
6. Two links.

The same words appear three times per card. For example, Nakba's "destruction of Palestinian society":
- h2: `ph_screen02.png`
- focus line
- THEN blockquote

The page has no change of pace: no full-bleed moment, no figure that breaks the 760 px column, no screen that is mostly picture. On desktop (`dk_full_sheet.png`) the effect is a long grey column of boxes.

### Text vs visual per phone screen (at rest, nothing swiped)
I measured only svg and canvas pixels:
- Flash: about **2%** of the page's area. Only car2's first lane chart, about 18% of screen 7.
- Research story tab: about 4%, plus HTML-built grids such as #xmFig.

Adding the HTML-drawn mini graphics (phase row, designation dots), my screen-by-screen estimate:

| Screen | Content | Picture share |
|---|---|---|
| 0 | Hero | 0% |
| 1 | Zionism | ~15% (chips and phase row, which are really text in boxes) |
| 2 | Nakba | 0% |
| 3 | October 7 | 0% |
| 4–5 | Hamas | ~25% (designation chart) |
| 6 | Genocide charge | 0% (car1 slide 1 is a quote) |
| 7–8 | What lasts | ~35% (car2 lane chart) |
| 8 | Arbitrators | 0% |
| 9–10 | Close | 0% |

**Six to seven of the ten screens are pure type.** That is the "text article" feeling, and the numbers confirm it.

### Carousels: stacked text or compelling?
- **car1 "The charge, everywhere"** (`ph_car1_strip.png`): 4 of 5 slides are text. The only chart (the xwGG title strip) is slide 4, where nobody reaches it.
  - Slide heights jump: 169 → 309 → 303 → 589 → 314 px.
  - `.car-vp` animates its height on each swipe (`transition:height .25s`), so the dots and arrows move under the thumb and the page below reflows. On a phone this feels broken.
- **car2 "How long a word lasts"** (`ph_car2_strip.png`): the one good carousel. All 5 slides are visual-first lanes with one caption, which is exactly the right format.
  - Problems:
    - The "What changed" box above it lists the same four words and numbers, so the carousel arrives pre-spoiled.
    - Slide 3 (the October 7 lane, "hostages: never in the first sentence, in 107 wordings") is the visual proof of **card 3's** headline, yet it sits three screens later in card 6.
    - Slide 5 (#kChart) is a different message (timing) wedged into a "what lasts" set.
    - The Zionism slide's "Mostly in" phase label collides with the lane label on phone.
- **car3 "Every line, then and now"**: 7 slides of small then/now text that re-run cards 1–5. It reads as an appendix inside the close.
- **Affordance.**
  - The only cue is "1 / 5 · swipe" in 11.5 px muted mono at the top right.
  - Slides are 100% wide, so nothing peeks.
  - The dots sit under the slide, often below the fold of a tall slide.
  - Swiping works (I confirmed it with real touch events), but nothing invites it.
  - Desktop arrows and dots work, and arrow keys work.

### Where it is an article rather than an interactive piece
- The c1 "Every change, step by step →" link and every "Full evidence →" link leave the page, to the other artifact. The interactives exist but sit behind a context switch.
- The flash already ships every interactive's code: build_flash.py copies the whole JS library, including `ziInit`, `o7Init`, `xrInit`, `xmInit`, `drawNetIn`, `drawBreathe`, `drawTier` and `keyGo`. Its R slice already holds `zionism`, `oct7`, the four ratchet articles with `fs_timeline`/`fs_variants`, and the four articles' `w_edits`/`pv_monthly`.
- So bringing the visuals back is mostly markup plus small data slices, not new code.

### Desktop (1280)
- 8.8 screens long. The 760 px column leaves 500 px of empty margin, and the figures never use it.
- Lane tooltips on hover and the keyboard focus rings work (`dk_tab.png`).
- The carousels are fine with arrows, but slides still change height.

---

## 3. PROPOSAL: bring the visuals back at about 9.5 phone screens

### Principles
1. **One proof per card, and it is a picture where a picture exists.** The headline carries the words once. The focus line ("What changed") stays only on cards whose proof is a sentence. Drop every blockquote that repeats the focus line.
2. **Two full-bleed moments:**
   - the **Zionism sentence rewriting itself** (#breathe), at screen 2;
   - the **language grid lighting up** (#xmFig), between Hamas and the genocide card, at about screen 5.
3. **Carousels are visual-first:** each slide is a visual (≥55% of slide height) plus a one-line caption (≤ 120 characters) plus a mono meta line. A text-only slide is not allowed.
4. **The heavy interactives come back as a "▶ Play / Explore" button that opens a full-screen sheet** with the real research figure, not as more page length.

### Screen budget (phone, at rest)

| Block | Now | Proposed | Change |
|---|---|---|---|
| Hero | 0.91 | 0.95 | Replace the "What changed" box (a duplicate) with the **150-tile strip** (below). Move the scope note to the close. |
| c1 Zionism | 0.88 | 1.15 | Replace chips (`#ziSum`) and phase row (`#flPh`) with **#breathe**, auto-sweep on reveal. Add a "▶ Every change, step by step" sheet with **#ziFig**. |
| c2 Nakba | 0.88 | 0.60 | Drop the THEN/NOW blockquote (the focus line already shows the diff). Put the full sentences behind "full sentence ▾". |
| c3 Oct 7 | 0.94 | 0.95 | Replace the "Hostages" text box with the **October 7 lane** (moved from car2 slide 3), plus "▶ Play" for the **#o7Fig** sheet (tab October 7). |
| c4 Hamas | 1.35 | 1.05 | Drop the two English blockquotes (they duplicate the focus line). Keep the Hebrew card and the designation dots (`flPos`); add "▶ Play" for the **#o7Fig** sheet (tab Hamas). |
| Moment: languages | — | 0.65 | **#xmFig mini**, auto-toggling then → now. |
| c5 Charge | 1.36 | 1.05 | Drop the own-voice Gaza genocide blockquote (a duplicate). Rebuild car1 as visual-first (below). |
| c6 What lasts | 1.25 | 1.00 | Remove the "What changed" box (it spoils car2). car2 is lanes only. Move #kChart out to its own slide set with steps. |
| c7 Arbitrators | 0.73 | 0.80 | Optional: a mini **#net** graph in place of half the "Our count" paragraph (needs the messaging agent; see below). |
| Close | 1.37 | 1.15 | car3 becomes poster slides plus a **#tierFig** last slide, replacing the 3 text paragraphs. |
| **Total** | **10.3** | **≈9.4** | |

### The two full-bleed moments

**Moment 1: "The sentence rewrites itself" (c1, #breathe).**
- **Code to reuse, as is:**
  - `drawBreathe`, `brEvents`, `brStrip`, `brStripSVG`, `brMove`, `brRender`, `brThumb`, `brRelease`;
  - the state object `BR`;
  - CSS `.breathe .br-s .br-strip .br-head .br-key`.
- **Markup:** copy `<section class="breathe" id="breathe">` lines 1997–2007 of page_template.html into c1. Remove `#brLab` (data-lab link) and `#brCmp`, or keep `#brCmp` hidden.
- **Data:**
  - `brEvents("Zionism")` reads `R.ratchet.articles.Zionism.fs_timeline`/`fs_variants`, which the flash slice already has.
  - `drawBreathe` also reads `R.dates.at(-1)`. **Add `"dates": res["dates"]` to the R slice in build_flash.py** (241 bytes).
- **Auto-sweep:**
  - On first reveal, use `revealOnView(host, go)` (exists) and animate `brMove(t)` from `BR.t0` to `BR.t1` over about 4 s with `requestAnimationFrame`.
  - Then stop at "now" and show the hint "Drag the strip ↔".
  - With `prefers-reduced-motion`, skip the sweep and start at now.
  - Stop the sweep the moment the user touches `#brRange`.
- **Layout:**
  - On phone, make the section full-bleed: `margin-inline:calc(50% - 50vw)`, padded 16 px, `background:var(--sheet)`.
  - Set `.br-s` to 18 px on phone. The Zionism sentence is about 300 px tall at that size.
- This replaces the chips and the phase row, which say the same thing statically.
- **"▶ Every change, step by step" opens the #ziFig sheet** (see "The sheet"), instead of the external link.

**Moment 2: "Which Wikipedias say it as fact" (between c4 and c5, #xmFig mini).**
- **Code to reuse:** `xmInit`, `xmDraw`, `xmHow`, `xmTipWire`, `xmTipShow`, `xmRove`/`xmMove`; state `XM`. The flash already has `#xmTip` and its CSS (`.xm-*`).
- **Markup:** copy `<figure class="fig xm-keep" id="xmFig">` from page_template.html. On phone, hide `#xmFind`, `#xmCall`, the full key `<details>` and the "Our coding" block. Keep 3 columns: Genocide, Colonization, Apartheid. The phone layout already shows 3 columns with "swipe for 4 more claims".
- **Data:** add `R.langs = {order, voice, missing, cols, cells}` (about 15 KB) to the slice. `arts` is not needed for the grid itself, because the tip text comes from `cells`. Check `xmTipHTML` for any `R.langs.arts` read. If it needs the sentence, slice `arts` to the 3 columns' articles.
- **"Lighting up":**
  - On reveal, render `XM.mode="then"`, wait 900 ms, then switch to `XM.mode="now"` and call `xmDraw()`.
  - CSS transition on `.tl` background and border (`transition:background .4s, border-color .4s`), staggered by row with `transition-delay: calc(var(--r)*60ms)`. Set `--r` inline in `xmDraw`'s row template.
  - Show a small "Then · Now" segmented control after the animation, using the existing `seg`/`setSeg` helpers on the research `#xmMode` buttons.
- **Caption (one line):** an existing sentence from the research xmFig header ("How each language edition voices seven claims, then and now"). Tap a square for the sentence and translation (`xmTipWire`, `int_xm_tap.png`).
- **Payoff:** this replaces the three text slides (Arabic, Spanish, Hebrew) in car1. Their exact sentences live in the grid's tips.

### The sheet: real interactives on demand, at zero page length
- One `<dialog id="flSheet" class="fl-sheet">`:
  - full-screen on phone (`width:100vw; height:100dvh; max-width:none`, slide-up `transform` transition);
  - a centred 900 px modal on desktop.
  - Sticky top bar: a title and a 44 px "Close ✕". `Esc` closes. Focus returns to the opener. `showModal()` gives the focus trap for free.
- **Build:**
  - In build_flash.py, slice each figure's outer HTML from `rtpl` by id, the same way it already slices `<style>` and the JS library. Use a balanced `<figure …id="X">…</figure>` cut.
  - Insert each into a `<template id="tpl-X">`.
  - On first open, clone into the dialog and call the init once:

| Button (where) | Template | Init on open | Extra data |
|---|---|---|---|
| ▶ Every change, step by step (c1) | `#ziFig` | `safe(ziInit)`, then `ziPlay(true)` | none (R.zionism and the article `w_edits` are already sliced) |
| ▶ Play the October 7 sentence (c3) | `#o7Fig` | `safe(o7Init)`, `o7Tab(1)`, `o7Play(true)` | none (R.oct7 is already sliced) |
| ▶ Play the Hamas sentence (c4) | `#o7Fig` | `o7Tab(0)`, `o7Play(true)` | none |
| ▶ Gaza genocide, every change (car2 slide 1) | `#o7Fig` | `o7Tab(2)` | none |
| ▶ Hear it in Arabic / Hebrew (car1 slides) | `#xrFig` | `safe(xrInit)`, `xrMoment(i,true)` | `R.langs.arts` sliced to Gaza genocide, Hamas, Gaza war (about 100 KB); `R.langs.moments` filtered to those |

- Ids are unique because each template is cloned once. Guard repeat opens with a `data-ready` flag.
- On close, call `ziPlay(false)` / `o7Play(false)` so the timers stop.
- **Do not port** `#xmIcjFig` (courts framing), `#board`, `#forest`, `#wvu` or `#ledger`. Those belong to the research edition.

### The carousel designs

**Shared mechanics (fix in `carInit` and `.car-*` CSS):**
1. **Peek.**
   - `.car-s{flex:0 0 88%}`, `.car-vp{gap:10px; scroll-padding-inline:16px; padding-inline:16px}` on phone, full-bleed (`margin-inline:-16px`).
   - The next slide shows by 10%. This is the strongest swipe cue there is.
2. **Fixed height.**
   - At init and on resize, set `vp.style.height = max(slide heights)`.
   - Remove `transition:height` from `.car-vp` and align slides to the top.
   - This stops the controls jumping (car1 currently jumps 169 → 589 px).
3. **Nudge once.**
   - `revealOnView(c, ()=>{ if(!reduced){ vp.scrollBy({left:56}); setTimeout(()=>vp.scrollBy({left:-56}),420) } })`, only the first time.
4. **Counter and control placement.**
   - Replace "1 / 5 · swipe" with a pill at the top left of the first slide: `Swipe → 1/5`, 12 px, `var(--ink)` on `var(--add-bg)`. It disappears after the first swipe.
   - Move the dots to overlay the slide's bottom edge, so they are visible without scrolling.
   - Keep ‹ › for desktop. Hide them on touch (`@media (hover:none)`), because peek and dots suffice there.
5. **Slide template.**
   - Order: `.w` meta (mono), then the visual (svg, grid or sentence-poster), then `.cp` caption (one line).
   - Captions longer than 120 characters fail review.

**Carousel A: "The charge, everywhere" (c5). Order:**
1. **Genocide-article title strip** (`#xwGG`, `drawXwGG`). Today it is slide 4; it moves to slide 1.
   - Caption: "English dropped "allegations" from the title on 3 July 2024 (+187 days); Polish on 26 April 2026 (+849 days)." (existing text, trimmed)
2. **Arabic, then → now, morphing.**
   - A mini of `#xrPair`: the Arabic sentence with its translation; tap ▶ and it morphs.
   - Cheapest version: render the two existing spans with `tnApply` (already used) and toggle a `.st-f` / `.st-n` class with a crossfade.
   - Full version: the "▶" opens the #xrFig sheet at the Arabic Gaza genocide moment.
3. **Spanish, then → now.** Same treatment.
4. **Israel vs Netanyahu, side by side.**
   - Two mini quote cards in a 2-column grid, each with a badge: "denial in next sentence ✓" vs "no denial".
   - The visual is the asymmetry. The text already exists.
5. **Hebrew, the exception.** The Hebrew sentence large (RTL) plus one-line translation. "▶" opens the xrFig sheet at the Hebrew moment.

Remove the current Netanyahu-first ordering: a text card should not open a carousel.

**Carousel B: "How long a word lasts" (c6). Already right; tighten:**
- Remove the "What changed" box above it. Its four rows are the four slides' captions.
- Order:
  1. Gaza genocide lane, ticks tappable (as now).
  2. Hamas lane.
  3. Zionism lane. Fix the "Mostly in" label collision: hide phase labels under 400 px, or drop the label 12 px.
  4. Optional, from the research edition: a fourth lane for Nakba via `flO7`-style `flStrip`, only if the data is already in `R.ratchet`. The research ratchet has Nakba with 74 timeline rows (about 20 KB).
- The October 7 lane moves to c3.
- Each lane slide gets a small "▶ every change" chip that opens the #o7Fig or #ziFig sheet.

**Carousel B2: "When" (replaces car2 slide 5). A stepped mini of the scrolly chart:**
- Use `#kChart` with `drawKey` plus a row of 5 step chips taken from `K_STEPS[i].k`. Tapping a chip calls `keyGo(i)`. Nothing new: `keyGo` and `kStat` exist. The research scrolly only drives the same function through IntersectionObserver.
- Show the caption from `kStat` for the active step (13.7 vs 3.8 for step 1, already asserted by the build).
- This is the scrolly chart without scroll-jacking, about 0.55 screen. It sits in c6 under carousel B, as a single figure, not a carousel.

**Carousel C: "Every line, then and now" (close). From text recap to posters:**
- Slides 1–6 become **posters**:
  - one article per slide;
  - the first sentence as ONE merged line in `#ziPair` style (`.wow-grid` type scale, 20 px on phone), with amber strike-throughs and blue inserts inline. Use `tnOps`/`tnPunch` or `wdiff` to merge, as #ziPair does;
  - a big mono date range;
  - no separate THEN and NOW blocks.
  - At a glance the slide is a picture of the change: colour density.
- Slide 7, "Moved the other way", stays as it is. The honesty slide stays text by design.
- **Slide 8 (new): the tier chart** (`#tierFig`, `drawTier`, add `R.mass3` to the slice, about 6.5 KB).
  - Caption: the existing close sentence, "the change sits in the core articles people read, while the long tail of short pages barely changed."
  - This turns the honesty paragraph into the single most persuasive "it is the core, not the tail" picture.
  - Remove that paragraph from the close body.

### Hero: give the first screen a picture
- Replace the "What changed" box with a **150-tile strip**: 150 small squares (10×15 on phone, 30×5 on desktop), labelled with existing words:
  - "the 150 most-read opening sections";
  - "Jan 2021, Jul 2023: none";
  - "now: seven, two as fact" (all already printed in c5).
- On load, the squares are all grey, then 7 light up (amber outline), and 2 fill solid: `var(--topic)`, 120 ms stagger. With reduced motion, show the end state.
- Pure CSS grid plus about 15 lines of JS. No library, no new data.
- Keep the Israel quote card above it. Move "We follow the core articles…" to the close, beside the honesty line.

### Optional: c7 network mini
- **Code:** `drawNetIn` with a third state object (copy `NETS`) into a `#flNet` host, graph view only (hide `netTable`, the window presets and the strip).
- **Data:** `R.network` (about 15 KB).
- **Risk:**
  - #net shows co-editing pairs ("14 linked pairs, 6.5 times chance"). c7's text is about talk-page voting groups.
  - Mixing them confuses the reader. Show #net only with its own research caption, and run it past the messaging agent (the no-names rule: nodes show "A6", "A8"; that is fine).
- If vetoed, leave c7 as text; it is short.

### Desktop
- Let the two moments and carousel slides use up to 1,080 px: `.fl-wide{width:min(1080px,100vw - 48px); margin-inline:calc(50% - min(540px,50vw - 24px))}`.
- At ≥1100 px, Carousel C can show 2 posters at once (`.car-s{flex-basis:calc(50% - 5px)}`).

---

## 4. TOP 10 CHANGES (ranked by impact on the experience)

1. **Put #breathe in card 1 as a full-bleed moment that auto-sweeps 2021 → now once, then hands over to the finger.** It replaces the chips and the static phase row. This is the best phone visual in the project and the clearest one-glance proof. Reuse `drawBreathe`/`brMove`/`brStrip` as they are; add `R.dates` to the slice. **Effort: S**
2. **Fix carousel mechanics:** 88% slides with a 10% peek, fixed height (stop the 169→589 px jumps), a one-time nudge on reveal, a "Swipe → 1/5" pill, dots overlaid on the slide, arrows hidden on touch. Changes go in `carInit` and `.car-*` CSS only. **Effort: S**
3. **Cut the triple-quoting.** Drop the blockquotes that repeat the focus line (hero, c2, c4 English pair, c5 own-voice) and the c6 "What changed" box that spoils car2. This buys about 1.2 screens for the visuals and breaks the identical card skeleton. **Effort: S**
4. **Language grid "lighting up" moment between c4 and c5** (#xmFig mini, 3 columns, then → now on reveal, tap for exact sentence). It replaces car1's three text slides. Reuse `xmInit`/`xmDraw`/`xmTipWire`; add `R.langs.{order,voice,missing,cols,cells}`. **Effort: M**
5. **The play sheet** (`<dialog id="flSheet">` plus `<template>` copies of #ziFig, #o7Fig and #xrFig sliced from page_template.html at build time; init with `ziInit`/`o7Init`/`xrInit` on first open). All the cool step-through and play machinery comes back at zero page length, replacing the out-of-page "Every change, step by step →" link. **Effort: M**
6. **Hero picture: the 150-tile strip** (0 → 7 lit, 2 solid), replacing the duplicate "What changed" box, so screen 1 has a visual and a moment. CSS grid plus about 15 lines of JS, existing numbers only. **Effort: S**
7. **Rebuild Carousel A visual-first:** xwGG title strip first; Arabic and Spanish as then → now morph slides (`tnApply` crossfade, ▶ opens the xrFig sheet); Israel vs Netanyahu as a side-by-side "denial / no denial" pair; Hebrew last. **Effort: M**
8. **Move the October 7 lane (car2 slide 3) into card 3** as the proof of "never mention the hostages", and add the ▶ #o7Fig sheet buttons to c3 and c4. The right picture goes under the right headline. **Effort: S**
9. **Close: Carousel C as posters (merged #ziPair-style diffs) plus a final #tierFig slide** replacing the "core vs long tail" paragraph. Add `R.mass3`; reuse `drawTier`, `tnOps`/`tnPunch`. **Effort: M**
10. **#kChart as a stepped mini:** 5 chips from `K_STEPS` calling `keyGo(i)`, with the `kStat` caption. Move it out of car2 into its own figure under carousel B. This is the scrolly chart's payoff without the scroll. **Effort: S**

Not in the top 10, but worth doing:
- desktop wide figures, `.fl-wide` (S);
- the c7 #net mini, if the messaging agent clears it (M);
- the #hero edit-stream canvas as a pre-rendered PNG backdrop for the timing figure (M; the live version needs the 5 MB `R.articles`).
