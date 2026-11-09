# Flash edition: impact round 2 (creative director)

Input: the fact-checked round-1 build (`scratchpad/flash/impact1c/index.html`, 9.51 phone screens), my own round-1 notes (`impact_r1.md` §6), and four coordinator messages:
- the round-2 brief;
- the claude.ai `downloads` capability;
- the owner decision that the two held credibility lines are now IN;
- the owner's pacing request, first for #breathe, then for every automatic animation.

The fact checker's round-1 fixes are kept: October 7 row "since 9 Dec 2023", "opening lines" in the stack header and kicker, and the two-voices image's denial footer.

Build: `scratchpad/flash/impact2/index.html` (wrapped: DOCTYPE, charset, viewport). Contact sheets:
- `impact2/contact.png` (phone light, 10 tiles);
- `phone-dark_contact.png`, `phone-light-rm_contact.png`, `desk-light_contact.png`.

Share images: `impact2/wikipedia-{first-lines,october-7,hamas-english-hebrew,two-voices}.png`. Sweep frames: `impact2/w/brmid_*.png`.

## 1. Fresh read, as a phone reader (before)
- **Hero (s00–s01).** It lands. The six rewrites read in one glance, and the denial sits under them. Keep it.
- **Card 1, #breathe (s01).** This was the weakest moment after the hero.
  - The sweep ran in 5.2 s, too fast to see any single change.
  - It then rested on the research edition's cumulative diff: 32 words removed and 23 added, all marked in amber and blue, a wall in which "re-establishment" → "colonization" is lost.
- **Cards 2–3.** Fine. The empty hostages lane is honest and strong. Card 3 had no shareable form, although it is the card Israeli readers would most want to send.
- **Card 4 (Hamas).**
  - The strongest second "oh" was there but split: the English definition only in the headline, the Hebrew one in a separate full-width card.
  - The reader had to assemble the mirror themselves.
  - It was also open to the first rebuttal a critic will throw: "Wikipedia drops 'terrorist' for every group."
- **Grid.** Readable since r1. The flip ran at 70 ms per row: one blink, no change visible.
- **Card 5.** The two voices land.
  - Open to the rebuttal "so Wikipedia doesn't report the atrocities either".
  - The morph slides (Arabic, Spanish) ran in about 0.9 s.
- **Close.** Its H2 was a five-line repeat of the hero (my r1 note). The tiles lit at 140 ms each, the headline sweeps fired the strike and the highlight together, and the stack advanced every 0.65 s. Every automatic animation was faster than the eye can follow.
- **Saving.** In the claude.ai viewer, plain download links, blob saves and `navigator.share` are blocked, so "Save as image" did nothing for real viewers.

## 2. What was built

| # | Change | Why | Effort |
|---|---|---|---|
| 1 | **#breathe readable end state.** By default only the words that carry the change are marked: the removed "re-establishment" (the op that holds it) and "state", and the added colonial/colonization wording. Other removed words are left out; other added words read as plain text. So the line reads as that day's sentence. A "Show every changed word" toggle (`#brAll`, aria-pressed) restores the research diff and its legend. A muted caption says what is marked. The height is held at the longest wording that was live for at least a day, so the page never jumps during the sweep. | The headline's two words now jump out at rest and at every step of the sweep. The text itself is never altered. | M |
| 2 | **#breathe watchable sweep (owner).** `brPlan()` turns every date where the marked words change into a stop. Stops are clustered (window grows from 45 days until there are at most 14). Each stop dwells 0.6–1 s, the travel between stops is quick and proportional to calendar time, and the total is about 13.5 s (measured 14.26 s). The bold date in the "· wording N of 169" line shows the sweep's current day. `#brPP` cycles Pause / Play / Replay. Any pointerdown, touchstart or key on the strip hands control to the reader at once. Reduced motion: no sweep and no control, as before. The sweep ends on today's readable state. | The change is seen landing, not blurred past. | M |
| 3 | **Second "oh": Hamas, English and Hebrew side by side** (`#c4vs`). Two same-size cards, neutral (no voice colours). English, first sentence since 29 Nov 2025, with "political organisation with a military wing" marked. Hebrew (RTL, with our translation, "Exploratory"), with "ארגון טרור" / "terror organisation" marked. It replaces the single Hebrew card. The body line "Hebrew Wikipedia puts it the other way around, as it already did in 2021" stays (messaging F8: not "Hebrew moved"). | The mirror is the image an Israeli reader will remember. | S |
| 4 | **Credibility line, card 4 (owner).** "Context: in line with Wikipedia-wide style on contentious labels, “terrorist” left the first sentences of Islamic State, al-Shabaab and Boko Haram. Hamas’s first sentence did not have it in 2021." Muted, 26 words. **No contrast clause:** see §3. | Pre-empts the first rebuttal without implying Hamas lost "terrorist" (its 2021 first sentence never had it). | S |
| 5 | **Credibility line, card 5 (owner).** The card's last line, muted, after the carousel: "The October 7 article states the killings in Wikipedia’s own voice: “massacring civilians in 21 communities”; “at least 1,195 people were killed by the attacks” (2 Nov 2026 copy)." It is also a footer line on the two-voices image. | Shows that the asymmetry is about the genocide label, not about whether the atrocities are reported. The headline is unchanged. | S |
| 6 | **Share cards for card 3 and card 4.**<br>Card 3 rows: the "attacks" → "armed incursions" diff, the rape-sentence diff, and the hostages row (the scope line plus sentence 9's “251 …”, so the image cannot be read as "Wikipedia erased the hostages"). Footer: the "massacring … names Hamas" line.<br>Card 4: English row; Hebrew original drawn right to left on the canvas, then our translation; footer: the body line plus the context line.<br>Both carry the scope line, the date stamp and the source URL. | Both hold up: each image carries its own scope and counter-facts. | M |
| 7 | **Saving through `claude.use("downloads")`.** At startup, if `window.claude.use` exists, the Save buttons are hidden and `use("downloads")` is called without blocking render. If it resolves to a handle, the buttons show; null keeps them hidden. A click calls `await handle.save({filename, data: Blob})`. If that is rejected for a reason other than a decline (NotAllowedError/AbortError), it retries once with a `Uint8Array`. Errors show "Not saved". `window.claude.downloads` is never read; only the result of `use()` is used. The old path (`navigator.share` on touch, then an `<a download>`) runs **only** when `window.claude` is absent, as in a local file or the headless tests. | Saving now works for real viewers. | S |
| 8 | **Pacing of every automatic animation (owner).** Each one is listed below the table. | Each change is seen landing; stretches with no change stay quick. | M |
| 9 | **The close's bookend H2 replaced** by the reach headline "The most-read pages whose opening sections changed". The bars caption is now "Views, past 12 months:", the eyebrow is "Reach and the count", and card 7's transition is "Last: how many people read these pages, and the overall count." | Removes a five-line repeat of the hero. Saves about 90 px. | S |
| 10 | `<meta name="description">` for link previews. | Best practice. | S |

The pacing in row 8, per animation:
- **Hero stack:** 1.2 s per row. The strike lands (0.45 s), then the new words highlight in (0.8 s, after 0.5 s). Total about 8.6 s. A tap on the stack while it plays jumps to the final state. Replay is kept.
- **Headlines (c1, c2, c4):** the strike and amber sweep first (0.6 s), then the blue highlight (0.9 s, after a 0.9 s delay). `box-decoration-break:clone` keeps multi-line spans whole.
- **Morph slides** (Arabic, Spanish): the old words fade out one by one over about 1 s, then the new words come in over 1.1 s. Each word's transition is 0.55 s, about 2.85 s in all. They start only when the slide becomes active (unchanged). Replay is kept.
- **Language grid:** flips row by row at 0.25 s per row (11 rows, about 3.3 s). A new "▶ Replay the flip" button appears when it ends. A tap on the grid cancels a pending flip.
- **150 tiles:** each attributed charge lights 0.6 s apart, then the two "as fact" tiles fill 0.8 s apart (about 5.7 s). A tap ends it at once.
- **Reduced motion, everywhere:** the final state, no animation, no replay controls.

### Deferred, and why
- **The #breathe height gap.** About 150 px stays below the sentence at rest. The hold height is the longest day-long wording, which keeps the page from jumping during the sweep. A shorter hold would make content below move while the reader drags. Next round: animate the height instead.
- **Card 5's "What changed" box.** Kept: it is the focus catcher by the two voices.
- **Card 6.** Still the densest card (carousel, scope paragraph, chart). The scope paragraph is binding (messaging F1); I did not cut it.
- **The "Titles by language" slide** leads carousel 1 and is a dense chart; I would move it to slide 3. Not done: the smoke tests and the reader index depend on the slide order, so it needs its own pass.

## 3. Credibility lines: verification against stored data
- **"terrorist" left the first sentences of Islamic State, al-Shabaab and Boko Haram:**
  - **Al-Shabaab and Boko Haram:** `data/leads.json`. The 2021 first sentences say "a terrorist, jihadist fundamentalist group" and "a jihadist terrorist organization"; the 2026 ones say "militant organization" and "militant organisation".
  - **Islamic State:** `data/ratchet.json`. "terrorist" is in stored first-sentence variants (e.g. 15 Jun 2023, "transnational militant Islamist terrorist group"; also briefly in May 2026). The latest variants (Sep–Oct 2026) have no "terror". The Jan 2021 snapshot did not have it either, so the line says "left", not "was in 2021".
  - **Hamas:** its 2021 first sentence (mass2 2021-01-01) has no "terror". Hence the clause "Hamas’s first sentence did not have it in 2021", so the line cannot be read as "Hamas lost 'terrorist' like the others".
- **Contrast clause ("only Hamas became a political organisation"): NOT added.**
  - The research edition (`#ev-oct7` More, and `angle/OCT7.md`) and `chart_data/oct7_02_designated_groups.json` show that Hezbollah ("political party … with an active paramilitary wing", "militant" dropped in 2024) and PIJ ("paramilitary organization") were also reframed as political or paramilitary bodies.
  - The owner's condition (no other group reframed) fails, so the context line stands alone. The build asserts that no "no other group" or "only Hamas" wording appears.
- **October 7 own voice:** "massacring civilians in 21 communities" and "at least 1,195 people were killed by the attacks" are both verbatim in the latest stored October 7 copy (mass2 `now`, rev of 2 Nov 2026). The numbers 21, 1,195 and 2 Nov 2026 are already printed by the research edition.

## 4. Build assertions added (`build_flash.py`)
- **Islamic State:** a stored first sentence with "terrorist", and none in the latest.
- **Al-Shabaab and Boko Haram:** "terrorist" in the 2021 first sentence (leads.json `lead0`), absent in 2026 (`lead1`).
- **Hamas:** no "terror" in its 2021 first sentence.
- **Hezbollah:** reframing check from the groups chart data.
- **Card 4's context sentence:** exact text.
- **No contrast-clause wording.**
- **Card 5's two own-voice quotes** are in the latest October 7 copy, and the line sits after `#car1` and before `#c6` (the card's last line).
- **The English Hamas definition** is in the latest Hamas copy.
- **Share cards:** four `data-share` buttons, each with a `shSpec` branch.
- **Downloads:** `window.claude.use("downloads")` is present and `window.claude.downloads` is absent.
- **Earlier assertions:** all pass (quotes, numbers, the hero stack, the r1 fact-check date guard, vetoes, spin guards, the scope line). The quote check also verifies every new quote against its own article (`data-q`, including the three-article source on the context line).

## 5. Measurements and smoke
- **Length, phone (390×844, fonts loaded, at rest):** **9.68 screens** (r1c 9.51); reduced motion 9.63. Within the preferred ≤ 9.8.
  - **Growth:** card 4 mirror plus context line (+160 px), card 5 credibility line (+60 px), the #breathe toggle and caption row, and the share buttons.
  - **Cuts:** the close bookend H2 (−90 px).
- **Length, 1280:** 9.42.
- **Smoke** (`impact2/smoke.js`, extended from impact1c): **391 pass, 0 fail.** Contexts: iPhone 13 light, dark and reduced motion; 1280 light and dark; plus a hosted-viewer test with a mocked `window.claude`.
  - 0 console errors or warnings, 0 horizontal overflow at rest and after interaction.
  - All earlier interactions pass.
- **New checks:**
  - the stack plays in 6–11 s (8.6 s), and a tap on it ends it;
  - the #breathe sweep takes 10–18 s (14.26 s);
  - #breathe rests on today with at most 3 dels and 2 inserts marked; the toggle restores the full diff (more than 10 marks);
  - Replay restarts the sweep and the date moves; Pause holds it; a touch on the strip hands control to the reader;
  - under reduced motion: no sweep and no Pause control;
  - the tiles take at least 3 s (5.7 s);
  - the grid's last row delay is 2.5 s, and its Replay appears;
  - the headline insert delay is 0.9 s;
  - the Arabic morph takes 1.5–3 s (2.85 s);
  - all four share images download (local path);
  - hosted: the buttons are hidden until `use("downloads")` resolves and then shown; Save calls `save()` with a PNG Blob; a null result keeps the buttons hidden; no page errors.
- **Research edition:** `page_template.html` and `build_page.py` are untouched (git diff empty).

## 6. Notes for round 3
- **Real-device checks:** the #breathe sweep on an iPhone (rAF at 60 Hz, `wdiff` per new wording is cached), and the RTL canvas line in the Hamas image on iOS Safari.
- **Next:**
  1. Animate the #breathe height instead of holding it (about −150 px).
  2. Reorder carousel 1 so a quote slide leads.
  3. Consider merging card 3's "What changed" box into its lane, now that the share image carries it.

## Fact check (messaging agent)
- **Card 4 context line: OK.**
  - "terrorist" left the first sentences of al-Shabaab (2021: "a terrorist, jihadist fundamentalist group") and Boko Haram (2021: "a jihadist terrorist organization"); both now say "militant". Islamic State's first sentence had it in stored variants, for example in 2023, and its latest has none.
  - "Hamas’s first sentence did not have it in 2021" is exact (2021: "fundamentalist but pragmatic, militant, and nationalist organization"). The five later insertions were all reverted.
  - "in line with Wikipedia-wide style" is the research edition's own wording.
  - Withholding the contrast clause was right: Hezbollah went from "political party and militant group" to "political party with an active paramilitary wing", and the research edition groups PIJ with Hamas as political or paramilitary.
- **Card 5 own-voice line: OK.** Both quotes are verbatim in the 2 Nov 2026 copy (rev 1383458606).
- **Hamas mirror: FIXED.**
  - The Hebrew quote, the translation (the stored `tr`) and both dates are exact.
  - But "ארגון טרור" / "terror organisation" was marked in the added-word blue. Hebrew already said it in 2021, so blue implied a change. It now gets a neutral mark (`b.mk`, faint background, ink), on the page and in the share image.
  - The Hamas image's Hebrew label now carries "exploratory" (messaging F8).
- **#breathe caption: FIXED.**
  - The default view drops the other removed words and leaves the other added words unmarked. The old caption ("Other changes read as plain text") did not say that.
  - It also named only "colonization", while the sweep marks "colonial" too.
  - New caption: "Marked: “re-establishment” and “state” (out), “colonial” or “colonization” (in). Other words changed too; the button shows them all." The toggle is unchanged and works.
- **Close heading: FIXED.** "The most-read pages whose opening sections changed" was not exact: the October 7 article (1.6M views) changed but is not in the list. It is now "…whose opening sections gained critical vocabulary" (research #reach).
- **Card 7 transition: FIXED.** "how many people read these pages" is now "how often these pages are read". The figures are views, not people.
- **Share images: OK.** The October 7 and Hamas images carry the scope line, the date stamp and the source URL. The hostage row keeps its scopes, with sentence 9's “251 …”, and the Hebrew renders right to left with the quote marks placed correctly.
- **Measured:** 9.70 phone screens (9.65 with reduced motion) and 9.46 at 1280. The smoke test gives 391 pass and 0 fail. Build: `scratchpad/flash/impact2c/index.html`.

## r2d: #breathe consistent baseline marks, no jumps (owner bug report)
- **Bug:** during the sweep, marks popped in and out and the sentence jumped. There were three causes:
  - The key-word filter kept or dropped whole diff ops. Ops are re-chunked as the alignment shifts (for example "espouses the re-establishment of" in one step, "re-establishment" alone in the next), so the marked span changed shape from step to step.
  - The research renderer's `.anim` class re-animated every `ins` on each wording change.
  - The height hold skipped wordings that were live for less than a day.
- **Fix:**
  - Every step of the sweep, the drag and the rest state is marked against the **Jan 2021 wording** (`BR.base`), never against the previous step.
  - Key-word mode now marks word **tokens**: removed "re-establishment" / "state", and added colonial/colonization words. Other removed words are left out and other added words read plain, identically at every step.
  - "Show every changed word" switches the whole sweep to the full diff against the same baseline.
  - Newly appearing marks fade in over 250 ms. Only marks that were not on screen at the previous step fade, and there is no width animation.
  - The research `.anim` animation is off.
  - The box height is fixed (height and min-height) at the tallest of **all** stored wordings in the current mode.
  - The pacing is unchanged (about 14 s).
- **Smoke** (`impact2d/smoke.js`): **399 pass, 0 fail**, 5 contexts plus the hosted mock.
  - At 5 points of the sweep (25 Dec 2021 to 6 Apr 2025), the marked set equals the key-word diff against Jan 2021. This is checked independently from token counts, with no other marks present.
  - The #breathe box height is constant through the sweep.
- **Length:** 9.70 phone screens. Build: `scratchpad/flash/impact2d/index.html`.

## r2e: #breathe full diff by default, key-word emphasis (owner feedback)
- **Default:** the full diff against Jan 2021 at every step of the sweep, the drag and the rest state. Every removed word is struck amber and every added word is blue, all persistent. The diff is rendered one element per word, so the marks stay put and build up as time moves forward. New marks fade in over 250 ms.
- **Emphasis layer, not a filter:** the key words carry `.kw`, a bold weight with a solid amber or blue fill:
  - removed "re-establishment" and "state";
  - added colonial/colonization.
- **Caption:** "Every word removed since Jan 2021 is struck; every word added is blue. The key words, “re-establishment”, “state” and “colonization”, are bold."
- **Toggle:** "Key words only" (aria-pressed) switches to the old filtered view, with its own caption.
- **Box:**
  - Its height is fixed at the tallest full-diff wording. It is recomputed only when the reader toggles. A bug in which the height style survived a re-measure is fixed.
  - The phone font inside the box is 15.5 px, which keeps the box at 245 px, about 1.2× the previous 205 px.
  - The pacing is unchanged (about 14 s, with dwells at the key-word changes).
- **Smoke** (`impact2e/smoke.js`): **399 pass, 0 fail**, 5 contexts plus the hosted mock.
  - At rest and at 5 sweep points, deleting the struck words from the box gives exactly that day's stored wording, and deleting the blue words gives exactly the Jan 2021 wording.
  - Only the key words, and all of them, carry the emphasis.
  - The box height stays at 245 px through the sweep.
  - "Key words only" shows at most 3 marks.
- **Length:** 9.72 phone screens; 9.59 at 1280. Build: `scratchpad/flash/impact2e/index.html`.
