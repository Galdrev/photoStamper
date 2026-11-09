# Flash edition: impact round 1 (creative director, fresh eyes)

Brief: the reader should get, in one mental jump, what the world now reads about Israel, and it must be true. It should land as an "oh", not as reading. Binding rules: `messaging_check.md`, `spin_review.md` (keep the scope line, no spin hooks), `qa/MUSTFIX_owner.md`, `PLAN.md`, and what `visual_critic.md` already did.

How I looked: Playwright Chromium, iPhone 13 (390×844, touch, fonts loaded) and 1280×900, light and dark. I let every animation finish, swiped every carousel, dragged #breathe, tapped the tiles, the grid and the lane ticks, and opened the three play sheets.
- Before screenshots: `scratchpad/flash/impact1/before/ph_s00–09.png` (one per phone screen).
- After screenshots: `scratchpad/flash/impact1/` (`phone-*_sNN.png`, `contact.png`).
- Baseline (spin build): **9.499** phone screens, 0 console errors.

---

## 1. Where the "oh" fails to land, screen by screen (before)

| Screen | What is there | Why the "oh" does not land |
|---|---|---|
| s00 (hero) | H1; the Israel quote card; the 150 tiles; the scope line. | **The single most important fact on the page, that the first lines of all six core articles changed, never appears as one picture.** The reader gets one quote (Israel) and an abstract grid of 150 grey squares, in which 7 light up. The tiles say "seven of 150", which is a *small*-looking number: the eye reads "mostly grey" and the shock deflates. The Israel card is static text. Nothing moves or rewrites on the first screen, and there is no "then" next to the "now". |
| s00–s01 (card 1) | Headline with del/ins; #breathe full-bleed. | The headline is the best line on the page. But #breathe ends its sweep on "Today", which shows the **cumulative diff against 2021**: 32 words removed and 23 added, a wall of amber and blue. The "oh" ("re-establishment" → "through colonization") is buried in noise. It is good as a toy, weak as a punch. |
| s01–s02 (card 2) | Nakba headline, lane, body. | OK. The lane makes the 2024 flip visible. |
| s02 (card 3) | Headline, "What changed" box, lane with the empty hostages lane. | Good. The empty dashed hostages lane is one of the most honest strong images in the flash. |
| s03 (card 4) | Hamas headline, Hebrew card, designation dots. | Solid but text-heavy; the English–Hebrew mirror works. |
| s03–s04 (grid) | 11×5 symbol grid with a 7-symbol legend. | **Five seconds is not enough.** The legend has to be decoded before anything is seen. The one line that is the answer, "Stated as fact: then 0, now 4/5/4", sits at the bottom in 10 px grey mono. |
| s04–s05 (card 5) | Headline; the "What changed" box; two voice cards; carousel 1 (titles strip first). | The two-voices pair lands. Carousel slide 1 (title strip by language) is a dense chart and is the first thing the swipe shows. |
| s05–s06 (card 6) | Headline, carousel 2 (lanes), the scope line, #kChart. | Fine for "how". It is not an "oh" card, and should not be. |
| s07 (card 7) | ArbCom quote, meter, count. | Deliberately colourless (messaging). Leave it. |
| s07–s09 (close) | Close H2, reach bars, **carousel 3 (6 posters + tier chart)**, score block, "In short", buttons. | **The payoff is at the very end and is mostly white space.** Carousel 3 has a fixed height set by its tallest slide, so the Israel poster shows one short line in a ~1-screen-tall box (s08). It repeats the headlines the reader has already seen, one per swipe, at the bottom of a 9.5-screen page: most phone readers never get there. The tier chart is the 7th slide and is effectively invisible. |

**Diagnosis in one line:** the flash has the right material but the wrong order of pictures. The one image that *is* the story ("six first lines, then and now") is the last carousel, cut into seven swipes. The first screen should be that image, rewriting itself in front of the reader.

## 2. Unused material that would hit harder (research edition, both tabs, and the data)

All already printed in the research edition, so no new numbers; quotes are stored text.

| Material | Where | Why it hits | Verdict for the flash |
|---|---|---|---|
| The **#reads seven lines** as one stack (then → now, dated). | Evidence room `#reads`; the flash has it only as carousel 3. | It is the whole thesis at a glance. | **Use it as the hero (change 1).** |
| The research **hero deck** ("Before the war … no genocide charge … Zionism, the “re-establishment” … is now “a Jewish homeland through colonization.” The Nakba …"). | Story, `#deck`. | Shows that the research edition's own opening is a stack of then/nows. | Folded into change 1. |
| **#ziPair**: the whole Zionism opening, 2021 vs now, in big type. | Evidence `#ziPair`. | Strong, but it repeats #breathe. | Not used. |
| **#hero edit-stream canvas** (513 articles × weeks; the 7 Oct surge is a visible texture). | Evidence, `#hero`. | A real "wall" image for "how much moved". | Deferred: 1 screen tall, says "activity", not "wording". |
| "Nine armed groups: first “terror” mention" + "“terrorist” also left the first sentences of Islamic State, al-Shabaab and Boko Haram … Wikipedia-wide style". | Evidence `#o7Grp` / More. | It cuts *against* the Hamas card. Honest context. | **Recommend to the owner** as one line in card 4 (kind-b content decision: it weakens a finding, so I did not apply it). |
| October 7 opening: "at least 1,195 killed", "251" hostages, "44 countries described the attack as terrorism". | Story, `#oct7` More. | Answers the "double standard on everything" spin (spin R4). | Deferred (spin R4 is the owner's call); length. |
| Hannibal: absent Jan 2024 → "The IDF used the Hannibal Directive …" (2 Nov 2026). | Messaging §3. | A second thesis. | Not used (messaging advice). |
| Rate per 1,000 edits: about 7 → 13.5 → 16.0 → … → 5.1 ("volume fell, but the defining sentences kept moving"). | Story `#when` deck. | A good "the words stayed after the storm" line. | Deferred: card 6 already carries timing. |
| Antisemitism mentions 37 → 54. | Evidence. | Uncoded (could be accusations). | Not used (the research edition itself refuses to call it an edit the other way). |

## 3. Tricks and patterns: which suit this data and audience, and how to keep them honest

| Trick | Fit for this data / Israeli phone readers | Manipulation risk | How we avoid it | Use? |
|---|---|---|---|---|
| **A first sentence that types and rewrites itself** | Perfect: the finding *is* a rewrite of first sentences. Seeing the old words get struck and the new ones typed is the "oh". | Animation order implies time order; a "typing" effect can suggest one actor writing it. | Each row carries its **own two dates** (then / since). The stagger is a fixed reading rhythm and is not mapped to a time axis; no shared clock implies the rows changed together. Quotes are exact, verified by the build. Final state = the static truth; reduced motion shows only that. | **Yes (change 1)** |
| **Stacked first sentences changing in sync** | The one picture of "what the world now reads". | "In sync" implies they changed at the same time. | Not in sync in time: staggered, each with its real dates (see above). | **Yes, merged into change 1** |
| A counter that ticks (2021 → 2026) | Tempting over the stack. | A shared year counter would imply each row flipped at that year. The Zionism "then" left in June 2021 but "colonization" settled in Aug 2026: a single clock lies about one of them. | Not used. | **No** |
| Then/now wipe or before/after slider | Good for one sentence. | Low. | #breathe already is the slider (drag through time). | Already there |
| **Scroll-triggered highlight** | Lets the eye land on the changed words in under a second (must-fix 12) as each headline arrives. | Low: highlighting only, no text change. | Same del/ins colours; final state is static; reduced motion: no animation. | **Yes (change 4)** |
| **Share-ready quote cards (download as image)** | Israeli readers share on WhatsApp/Instagram; a screenshot of a phone page loses the dates and the scope. | The image travels without the page: a quote stripped of date, voice and scope becomes a slogan. | The image is drawn from the page's own verified DOM text, and **always** carries: article · section · dates, the voice label, the denial line where the page has it, the scope line, "Wikipedia text as of 5 November 2026", and the research URL. No text is typed into the canvas by hand. | **Yes (change 3)** |
| **Sticky progress** | Phones: shows how short the page is and where you are; reduces drop-off. | None. | Decorative, aria-hidden, no height. | **Yes (change 5)** |
| **Colour restraint with one accent** | Already the system: blue = in now, amber = removed. | — | Keep; no new colours (must-fix 12). | Kept |
| **Typography scale contrast** | The rewritten phrases in display type, the labels in small mono. | — | Used in change 1 and the grid total (change 6). | **Yes** |
| A full-screen moment with a single quote | Strong, but a single quote out of six invites "cherry-picked". | High: it makes one line stand for the whole. | The hero stack is the "full-screen moment", with all six lines, not one. | Covered by change 1 |
| Tap-to-reveal (guess first, then see) | Engaging. | Priming: the guess options frame the answer; a quiz about hostages gamifies trauma; it also costs a tap before the truth. | Not used this round; if tried later, only on neutral facts (for example "how many Wikipedias state it as fact?"), with an open guess, no options. | **No (deferred)** |
| "You are reading this now" framing | Makes the stakes concrete: these are the first lines anyone opening the page sees. | "The world reads" is vetoed (spin H3/H11); "now" must be dated. | Wording: "Open these articles today and this is what they say first" plus "our copy: 5 Nov 2026". No "world". | **Yes (in change 1)** |
| Small multiples | The language grid already is one. | — | Make its answer row readable (change 6). | Tweak only |
| Sound-free micro-animation | Strike draws, highlighter sweeps, typed reveal. | — | All CSS, reduced-motion off. | Yes |

## 4. Top 8 changes, ranked by impact

1. **The rewrite stack as the hero (L).**
   - Replace the static Israel quote card with `figure#flRw`: six rows in card order (Israel, Zionism, Nakba, October 7, Hamas, Gaza genocide).
   - Each row: a mono label "Article · section" plus the dates, then `<del>“then”</del> → <ins>“now”</ins>`, with an `.zi-sr` "became" for screen readers. Each `li` carries `data-q` so the build checks every quote against its own article.
   - Text is reused from the posters (already verified): “re-establishment” → “a Jewish homeland through colonization”; “the destruction of Palestinian society” → “the ethnic cleansing of Palestinian Arabs by Zionists”; “coordinated attacks” → “coordinated armed incursions”; “militant” → “political organisation with a military wing”; “Allegations have been made” → “carried out by Israel”; Israel: no genocide charge → “began committing genocide”. Dates are as on the posters.
   - The Israel denial line stays directly under the stack (messaging, spin): "In the Israel article, the next sentence: “Israel has denied that its actions constitute genocide.”"
   - Header: "Open these articles today. Their first lines, then and now" plus "our copy: 5 Nov 2026".
   - Animation: CSS default is the final state. JS adds `.pre` (old words plain, new words clipped), then row by row adds `.go`: the strike draws (0.35 s), then the new words "type" in (clip-path steps, 0.7 s), every 0.6 s.
   - ▶ Replay button. Reduced motion or no JS: the final state, no animation.
   - The tiles stay in the hero (they prove the H1), under the stack.
2. **Cut carousel 3 (posters plus tier slide) from the close (S).** It is now redundant with the hero, and it is about 1.3 screens of mostly white space. The tier slide's honesty caption is kept as one line in the close ("The change sits in the core articles people read, while the long tail of short pages barely changed.").
   - `build_flash.py`: drop `tierFig` from SLOTS and drop the mass3 slice. Drop `flPosters` and the `drawTier` lazy init from the template. This resolves BUILD_v2's MUSTFIX-3 tension.
3. **Share as image (M)** for two cards: the hero stack, and card 5's two voices.
   - `flShare(el,opts)` walks the element's DOM into segments (del, ins, plain; `.zi-sr` skipped) and draws a 1080×1350 PNG in the page's light palette.
   - It draws the title, the rows, a footer with the scope line, "Wikipedia text as of 5 November 2026 · Flash edition", and the research URL.
   - On touch devices that support `navigator.canShare({files})` it opens the share sheet; otherwise it downloads `wikipedia-first-lines.png`.
   - Buttons: "Save as image". The script holds no curly-quoted literals (the build's script-quote guard stays intact).
4. **Scroll-triggered highlight on the then/now headlines (S).** `.fl-hd` (c1, c2, c4) gets `.pre` on init. On view, the highlighter sweeps under the `ins` (background-size 0→100%, 0.9 s) and the strike fades in on the `del`. Reduced motion: no `.pre`.
5. **Sticky progress bar (S).** A fixed 3 px top bar, `aria-hidden`, width = scroll progress, `var(--add-bd)`. No layout height.
6. **Grid: make the answer row readable (S).** In `#flXm tfoot`: the row label in ink, the "now N" figure in 17 px bold display, and a faint band behind it. CSS only; the numbers are the grid's own.
7. **Card 5: the "What changed" box duplicates the hero row (S).** Kept this round: it is the focus catcher right next to the two voices, and removing it gains only ~90 px. Revisit if over budget.
8. **#breathe ends on a readable state (M, deferred).** End the sweep on the current sentence with only the "re-establishment"/"colonization" spans highlighted, instead of the full cumulative diff. This needs a flash-side `renderW` filter on #breathe's output. It is risky to do without touching the research function's contract; next round.

Deferred, with reasons: tap-to-reveal (priming risk, see §3); #hero canvas (activity, not wording); the Nine-groups context line and the October 7 toll line (owner content decisions: spin R4 and kind-b).

---

## 5. Phase B: what was built

Built: `scratchpad/flash/impact1/index.html` (1.98 MB). It begins with the DOCTYPE, charset and viewport meta. Phone contact sheet: `impact1/contact.png` (10 tiles). Also `phone-dark_contact.png`, `phone-light-rm_contact.png` and `desk-light_contact.png`. The share images are `impact1/wikipedia-first-lines.png` and `wikipedia-two-voices.png`. Mid-animation frame: `impact1/w/hero_mid.png`.

| # | Change | Status |
|---|---|---|
| 1 | **Rewrite stack as the hero** (`#flRw`). Six rows; the old words are struck and the new words highlight in, one row every 0.65 s. Each row shows its own dates. ▶ Replay. The denial line stays under it. "copy of 5 Nov 2026" stamp. The Israel quote card is removed (its sentence is row 1, its denial is kept). The tiles stay. | **Done** |
| 2 | **Carousel 3 cut** (posters and the tier slide). The honesty caption is kept as one line (`p.fl-honest`) before "In short". `tierFig` and `mass3` are out of the build, and `flPosters`/`drawTier` are out of the template. | **Done** |
| 3 | **Save as image**: the hero stack and card 5's two voices. 1080×1350 PNG drawn from the page's DOM. The footer always carries the scope line, "Wikipedia text as of 5 November 2026", the source URL and, on the stack, the denial. On touch devices with `navigator.canShare({files})` it opens the share sheet; otherwise it downloads. Attributed spans (`.att`) are drawn amber **without** a strike: an early draft struck "have alleged", which would have implied the words were removed. Caught in review and fixed. | **Done** |
| 4 | **Scroll-triggered highlight** on the `.fl-hd` headlines (c1, c2, c4): the highlighter sweeps in and the strike fades in. Headlines already on screen at load are not reset. | **Done** |
| 5 | **Sticky progress bar** (`#flProg`, 3 px, aria-hidden, scaleX). | **Done** |
| 6 | **Grid answer row**: the "Stated as fact" row is in ink, with a blue band and 18 px "now N". | **Done** |
| 7 | Card 5 "What changed" box. | Kept (deliberately; see §4) |
| 8 | #breathe readable end state. | **Deferred** (needs a filter on the research renderer's output; next round) |

**Honesty mechanics, as built:**
- The stack's markup *is* the final state. JS only adds `.pre`/`.go` classes, so no JS or reduced motion shows the truth with no animation, and the text never changes.
- The rhythm is explicitly not a time axis: no shared counter, and every row carries its two dates.
- No new numbers or quotes. Every stack phrase was already on the page (posters, headlines) and is checked by the build.

**Build assertions added** (`build_flash.py`):
- The stack rows are exactly Israel, Zionism, Nakba, October 7 attacks, Hamas and Gaza genocide.
- Each "now" phrase is a substring of that article's **latest** stored copy (mass2 `now`, 5 Nov 2026 crawl), and each "then" phrase is **absent** from it.
- Israel's "no genocide charge" is checked: no "genocide" in the Jan 2021 or Jul 2023 Israel copies.
- The denial line is present.
- Both share buttons exist, and the share spec includes the scope line.
- All earlier assertions pass: 72 quoted strings, 48 numbers (down because the posters left), 4 RTL runs, the vetoes, the spin-review guards and the scope line.

**Research edition:** `page_template.html` and `build_page.py` are untouched. `build_page.py` output equals `scratchpad/spin/research.html` minus its 105-byte wrapper, byte for byte.

**Length (390×844, fonts loaded, at rest):** **9.486 screens** (baseline 9.499). The hero grew by about 430 px, paid for by cutting carousel 3 (about 490 px). Desktop 1280: 9.45.

**Smoke** (`impact1/smoke.js`, extended from v3): **325 pass, 0 fail**, across 5 contexts (iPhone 13 light, dark and reduced motion; 1280 light and dark).
- 0 console errors or warnings; 0 horizontal overflow at rest and after interaction.
- All v3 interactions still pass: swipe, sheets, focus trap, grid, kChart, lanes, tiles, glossary.
- New checks:
  - the stack at rest shows all 6 rewrites;
  - Replay replays the stack and ends in its final state; under reduced motion there is no `.pre` and no Replay;
  - every headline is highlighted at rest;
  - the progress bar is full at the bottom;
  - both "Save as image" buttons download the right file on the phone and on desktop.

## 6. Notes for my next-round judgement
- **Watch the hero on a real iPhone.** `box-decoration-break:clone` on multi-line `ins` (a clip-path reveal broke the second line in Chromium, so I switched to a background sweep). The Web Share path cannot be tested headless.
- **Judge** whether the close H2 ("These openings once said …") is now a redundant bookend of the hero. It could become the reach line alone, saving about 120 px.
- **Owner decisions still open:**
  - the Nine-armed-groups context line for Hamas ("terrorist" also left Islamic State, al-Shabaab and Boko Haram: Wikipedia-wide style);
  - spin R4 (the October 7 toll in Wikipedia's own voice next to the two voices).
- **The next biggest win** is #breathe's end state (change 8), then a share card for the hostages lane.

## Fact check (messaging agent)
- **Hero stack, October 7 row:** "23 Oct 2023 → since 8 Oct 2026" is now "→ since 9 Dec 2023". 8 Oct 2026 dates the whole sentence's exact wording. The row shows the phrase "coordinated armed incursions", which has stood since 9 Dec 2023: ratchet.json shows it in every stored first sentence since that date. A build assertion was added. Every other row's phrase date matches its own phrase, checked in ratchet.json:
  - Zionism: last restored 27 Aug 2026;
  - Nakba: 6 Jul 2026, apart from under an hour on 17 Jul;
  - Hamas: back on 29 Nov 2025 after a 4–29 Nov 2025 gap;
  - Gaza genocide: 26 Sep 2025, reverted attempts excepted;
  - Israel: "genocide" since 4 May 2025.
  The "then" dates are each phrase's own copy. The stagger runs in card order, not in time order, so it implies no simultaneity.
- **Stack header and share kicker:** "first lines" is now "opening lines". The Israel row is in the opening section, not the first sentence.
- **Share image "two voices":** it now carries one more unquoted footer line: "The Gaza genocide article reports Israel's denial in the last paragraph of its opening section." The image travels without the page. The footer block moves up 60 px for each line beyond two.
- **Both images carry** the scope line, the date stamp and the source URL. Attributed text ("have alleged") is drawn amber and not struck.
- **Headline highlights** (c1, c2, c4): every `del` and `ins` sits on the right words. OK.
- **Language-grid answer row:** the numbers are computed by the grid (0→4, 0→5, 0→4, 4→5, 2→2) and the label is right. OK.
- **Honesty caption in the close:** "The change sits in the core articles people read, while the long tail of short pages barely changed." Without the tier chart it is still the research wording ("…barely changed"). OK.
- **Measured:** 9.51 phone screens and 9.45 at 1280. The smoke test gives 325 pass and 0 fail. Build: `scratchpad/flash/impact1c/index.html`.
