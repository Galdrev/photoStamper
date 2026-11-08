# Flash edition v1: build notes (cut round 1 synthesis)

Built by the editor-in-chief from `messaging_check.md` §3 (the binding synthesis), with every VETO and FIX applied, plus the owner's exception for card 7.

- Source: `page_flash_template.html` plus `build_flash.py` (`python build_flash.py OUT.html`).
- Research edition: unchanged. `build_page.py` and `page_template.html` were not edited. `python build_page.py OUT.html` still passes all its assertions, and its output is byte-identical to the published build (`final/out.html`).
- How the flash reuses the research edition:
  - `build_flash.py` runs `build_page.py` through `runpy`, so every research assertion runs. It writes the research output to a temp file and deletes it, then reuses the in-memory `res`.
  - It copies the research `<style>` block and the JS library (everything before `/* ---------- init`) from `page_template.html` at build time. A design change there therefore reaches both editions.
  - R is a slice of the data: zionism, oct7, v3, xw, 4 ratchet articles, and 4 article view series. The page is 1.5 MB, against 11.6 MB for the research edition.
  - Reused as they are: the CSS tokens and components (`.news-q`, `.zi-chips`, `.pos-row`, `.fig`, `#xmTip`, `#gloss`, `#tip`), `tnApply` (inline diff highlights on every `data-tn` pair), `tnTip` (punch plus compact diff in tooltips), `ziSummary` (the #ziSum chips), `ziData` (the phases), `o7Data`/`o7SpansAll` (the #o7Fig lanes), `drawKey` and `keyHover` (#kChart), and `drawXwGG`.
  - Written new for the flash: the carousel, a compact lane renderer in the #o7Fig grammar, a 2-row version of #o7Pos, and a static row of phases.
- Output: `scratchpad/flash/index.html`. It starts with `<!DOCTYPE html><meta charset><meta viewport>`; build_flash writes this wrapper.

## Build assertions (all pass)
- **Quotes.** All 106 curly-quoted strings (and the dinner sentence's single quotes) are substrings of stored text:
  - `data-q="en:Title"`: mass2 snapshots, leads.json and ratchet first sentences.
  - `he:`/`ar:`/`es:`: the langs.json orig and translation.
  - `arb`: arbcom_named.md.
  - Unlabelled quotes are checked against all stored text.
- **Numbers.** Every number on the page is printed in the research template. The exceptions come from the research code itself: 13.7 and 3.8 from `kStat` (the smoke test re-checks them), and 187 and 849 from `R.xw.gg` (asserted).
- **Vetoes.**
  - None of these appear: "afterthought", "the world reads first", 64/47-of, 336/650/386, "both sides", "documented".
  - "Undone within a day" appears only in its two Zionism scopes.
  - No account names except "Ïvana", which appears once.
- **Evidence anchors.** Every anchor exists in the research template.
- **Right to left.** Every mostly Hebrew or Arabic text run sits inside `dir="rtl"`.

## Card list as built
| # | Headline (house model) | Focus line | Proof | Carousel | Evidence link |
|---|---|---|---|---|---|
| Opening | Before the war, no top article charged Israel with genocide. Now Israel’s own article does. ("top article" has a glossary tooltip: 150 most-read opening sections, Jan 2021 and Jul 2023) | no charge in the 150 (Jan 2021, Jul 2023) → “Israel began committing genocide against Palestinians in Gaza”, since 4 May 2025 | hero-q with the denial line | — | #ev-charge |
| 1 Zionism | “re-establishment” → “a Jewish homeland through colonization.” | data-tn diff of the two first-sentence spans | #ziSum chips, plus the 4 phases from ziData (tooltip on each; phase 3 highlighted) | — | #ev-zionism, #ziFig |
| 2 Nakba | “the destruction of Palestinian society” → “the ethnic cleansing of Palestinian Arabs by Zionists.” | diff | THEN/NOW quote (Dec 2021 / since 6 Jul 2026), with the tag "the 2021 version also took a position" | — | #ev-1948 |
| 3 October 7 | “coordinated attacks” → “coordinated armed incursions.” The opening sections on Israel and Hamas never mention the hostages. | 2 diffs: attacks → armed incursions; the rape sentence | hostages block (107 versions; every snapshot since 2021; sentence 9) | — | #ev-oct7 |
| 4 Hamas | “militant” → “political organisation with a military wing.” | militant → political organisation… | EN 2021 / EN now (diff) and Hebrew now (RTL, with translation, "Other languages · exploratory"); #o7Pos rows for 2021 and the 31 Oct 2026 copy, stamped "as of our 5 Nov 2026 copy; days old, may be reverted" | — | #o7Fig, #ev-xl |
| 5 Genocide, both ways | “Allegations have been made” → “the ongoing, intentional, and systematic destruction … carried out by Israel.” | diff | 2 equal quote cards: Gaza genocide (own voice) and October 7 (“Some have alleged…”, attributed) | 1, "The charge, everywhere": Netanyahu (quote ends with a period); Arabic; Spanish; #xwGG titles; Hebrew, the exception (slides 2–5 tagged exploratory) | #ev-charge, #ev-xl |
| 6 What lasts | 45 minutes / “terrorist” five times, about 2.4 hours | list: alleged/described… ×10 → 45 min; terrorist ×5 → 2.4 h; resistance movement ×1 → next day; massacre → about an hour | the 4-sentence scope plus "no faster across the 254" (page wording) | 2, "How long a word lasts": lanes for Gaza genocide (10 attempt ticks), Hamas (militant, polmil, 5 terrorist dots, plus the resistance-movement and militant-returns caption), October 7 (massacre dots, empty hostages lane), Zionism (phase 3, 10 removal ticks), #kChart overview with 13.7 vs 3.8 and "a date, not a cause". Each mark has a tooltip with the what-changed punch, a compact diff and the full sentence. | #o7Fig, #when |
| 7 Arbitrators | “Outside actors are heavily invested…” They named no side. | — (not a then/now) | finding 10 quote with link (15–0, 23 Jan 2025); owner exception: Ïvana’s ban, finding 16 verbatim, with link; no direction colour; then the voting-camps fact line and "camp voting, not proof… Neither finding names a side." | — | #ev-organised |
| Close | once “re-establishment” (2021), “militant” (2021), “coordinated attacks” (October 2023) → “colonization,” “ethnic cleansing … by Zionists,” “genocide.” | per slide (data-tn) | — | 3, "Every line, then and now": Israel, Zionism, Nakba, October 7, Hamas, Gaza genocide, and "Moved the other way" (1948 expulsion with the Haganah, Irgun and Lehi clause; the October 7 clause, recent) | research edition, #reads |

The close also carries:
- the ratio line (223/61; comparison pages, other countries, conflicts and religions, 125/73);
- the reach line ("opening sections of the most-read pages that changed": 7.0M, 4.6M, 2.4M, 1.8M, 1.3M);
- ONE honesty line;
- the dinner sentence ("In one sentence");
- a button to the full research edition.

## Screen counts (Playwright, web fonts loaded)
| View | At rest (first slides) | Worst case (tallest slide open in every carousel) |
|---|---|---|
| iPhone 13, 390×844, light and dark | **8.08** | 8.91 (cap 9) |
| 1280×900, light and dark | 7.42 | 8.03 |

Per section on the phone, in screens: opening 0.72, c1 0.69, c2 0.69, c3 0.74, c4 1.07, c5 1.07, c6 0.99, c7 0.57, close 1.08 (margins between cards account for the rest).

Smoke test (4 contexts), all passing:
- 0 console errors or warnings, 0 horizontal overflow (before and after interaction).
- Carousels: next button, dots and arrow keys all move them; the counter is live; off-screen slides are `inert`; the height follows the current slide.
- Strip-mark tooltips work by tap on the phone and hover on the desktop, and Esc closes them.
- The phase tooltip and the "top article" glossary work; the #kChart hover tooltip works.
- All links go to the research artifact (#anchor), to Wikipedia (ArbCom) or to the fonts.

Screenshots are in `scratchpad/flash/*.png` (`{phone,desk}-{light,dark}_{top,c1…c7,close,full,tip,car2_when}.png`, plus carousel slides).

Note: a first measurement of 8.5 screens was taken before the web fonts had loaded. With Newsreader and Libre Franklin loaded it was 9.9. The phone typography was then tightened (headline 20.5 px, body 14 px, compact quote and slide padding) to reach 8.08.

## Where I deviated from the synthesis, and why
1. **Card 7 names Ïvana** (owner exception, overriding the messaging veto 3). It is one clause: finding 16, quoted verbatim and linked, with no side and no link to our network or blocs.
2. **Card 1 body.** The 33-in/32-out and the "10 more removals" figures are not repeated in the body. They are in the phase row, which ziData computes (the same code as #ziFig), and on slide 4 of carousel 2. The body keeps "as few Palestinian Arabs as possible", "undone within a day" (Zionism scope) and 37 of 41.
3. **Card 2 body.** “By Zionists” became "The Nakba’s first sentence has said “by Zionists”…", because the quote must match the stored lower-case text.
4. **Card 4 focus line.** It shows only militant → political organisation. The Hebrew line was cut there because it duplicated the Hebrew quote block directly below (screen budget). The Hebrew contrast stays in the proof element, with "already in 2021" in the body.
5. **Card 5 body.** It drops "10 edits … 45 minutes" (about 50 words otherwise), because card 6's headline and its first slide carry it.
6. **Card 5 proof.** “have alleged” is marked with the amber background but no strike-through, so it does not read as removed text.
7. **Card 6 slide 2.** "Resistance movement" is a caption line, not a dot: #o7Fig has no lane for it.
8. **Card 7 headline.** "found in January 2025: “Outside actors…”" keeps the capital O, because the quote is verbatim.
9. **Share cards (A's three).** Not built; they are not in the build brief. See the open items.
10. **No #o7Pos blue-square legend.** The 2-row inset leaves out the research legend about "Initially, Hamas was discreetly supported…", which would be a second thesis.

## Open items for round 2
- **Live re-check.** "Several countries" (Hamas, 31 Oct 2026 copy) and the October 7 clause removal are both recent. en.wikipedia.org is blocked from the sandbox.
- **Artifact anchors.** Whether claude.ai passes `#anchor` into the artifact iframe is untested. If it does not, the evidence links open the research edition at the top.
- **Overlapping ticks.** On the phone, 3 attempt ticks on 10 Oct 2025 overlap, and the top one wins the tap.
- **Phase row on the phone.** It shows only the name and date range; the sub-line is in the tooltip and in the aria-label.
- **Share cards.** A's three (1080×1350) are not built.
- **Tooltips.** The then/now quote blocks rely on the inline highlights and have no tooltip of their own. Tooltips are on the symbols: the strip marks, the phases, "top article" and #kChart.
- **Arabic slide.** It also highlights changed Arabic words. Check with a reader that the RTL highlight is not noisy.
- **Publishing.** The flash edition is not yet published as an artifact (PLAN step 6).
