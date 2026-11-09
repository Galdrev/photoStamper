# Flash edition v1: Editor A review (cut round 2)

How I reviewed: I rendered `scratchpad/flash/index.html` with Playwright on an iPhone 13 (390×844, about 8.1 screens) and at 1280×900, and swiped through every carousel. I read it as a reader would, then checked it against `messaging_check.md`, whose vetoes and fixes are binding. Nothing below adds a number: every figure and quote is already on the v1 page or in the research edition. The owner's exception for the Ïvana clause (card 7) is left as built.

## Verdict on the five questions

- **First screen:** it lands. The H1 and the hero quote card with “began committing genocide” highlighted are a real shock. But the WHAT CHANGED box repeats the same sentence a second time above the fold, and the deck repeats “In Wikipedia’s own voice” after the card label already says it. One screen spends half its space repeating itself.
- **What-changed lines:** they work in cards 2, 3 and 4: one strike, one highlight, read in under a second. Cards 1 and 5 fail by triple repetition: the headline, the focus box and the proof element all say the same words. In card 5 that pushes the real shock, the asymmetry, into the third block.
- **Carousels:** carousel 2 (“How long a word lasts”) is worth the swipe. The Gaza genocide ticks and the Hamas “terrorist” dots read at a glance. Carousel 1 is good except slide 4, the title bars: “+110 d / renamed +180 d” is a data table, not a flash slide. Carousel 3 (“Every line, then and now”) is 7 slides of exactly what the reader has just read. It is redundant and slow, so convert it.
- **Soft, redundant or slow:** the card 4 inset uses the 31 Oct “Several countries” row with a “may be reverted” stamp. That weakens the most shareable card. The card 6 headline runs 6 phone lines. Card 7's headline repeats its quote card word for word. The closing “In one sentence” box is four sentences and uses single quotes.
- **Structure:** keep the order. No merges. One conversion: carousel 3 becomes a static board (change 4).

---

## The 12 changes, ranked

### 1. Card 5 (`#c5`): headline on the asymmetry, not a repeat of the focus line
The shock is “stated as fact” against “alleged”, and it is now buried in the third block. The then → now stays in the focus line, so the owner's focus-catcher rule still holds.
- **New H2:** Wikipedia says genocide in Gaza is “carried out by Israel.” Of October 7, it says “Some have alleged.”
- **Focus line (shorter):** “[-Allegations have been made that the 2023 Israel–Hamas war constituted a-] genocide” → “{+is the ongoing, intentional, and systematic destruction … carried out by Israel+}”
- **Gaza genocide quote card:** move the blue highlight from “is the ongoing, intentional, and systematic destruction” to **“carried out by Israel”**. The two equal cards then show the contrast in one glance: blue “carried out by Israel” against amber “have alleged”.
- Scope stays in the body as built (“stated as fact in the Gaza genocide, Israel and Netanyahu articles … seven do now, two as fact”). The headline names only Gaza genocide, its exact scope.

### 2. Card 3 (`#c3`): the hostages in the headline, in two sentences, with the page's own count
The current H2 is three sentences, and its third (“Its opening sections …”) has an unclear “its”. For an Israeli reader, the hostage absence is the shock; “armed incursions” is the setup.
- **New H2:** Wikipedia’s first line on October 7 now says “coordinated armed incursions.” In 107 versions, it has never mentioned the hostages.
- The focus line keeps “coordinated [-attacks-]” → “coordinated {+armed incursions+}”, so the then/now is not lost.
- **Hostages box label:** “Israel and Hamas opening sections: none, in every copy we hold since 2021.” This is the messaging-check wording (§1b) and replaces “at every snapshot”.

### 3. Opening (`#top`): fold WHAT CHANGED into the hero card and tighten the deck
- **Delete** the separate WHAT CHANGED box. **Add a THEN line** as the first row inside `.hero-q`, above the quote:
  `THEN · JAN 2021, JUL 2023` no genocide charge in any of the 150 most-read opening sections.
  `NOW · SINCE 4 MAY 2025` “After the Hamas-led October 7 attacks, Israel {+began committing genocide+} against Palestinians in Gaza.”
  The denial line stays under it.
- **New deck:** The article was viewed 4.6 million times in the past 12 months. Below: the other core articles, then and now.
  (The “genocide since 4 May 2025” date moves into the NOW tag, and “own voice” is already in the card label.)
- This saves about 0.2 screen and puts the first card's headline above the fold on taller phones.

### 4. Close (`#close`, `#car3`): replace the 7-slide recap carousel with one static board
On a phone, swiping 7 slides of what was just read is the slowest part of the edition. A six-row board of focus words gives the same recap in about a third of a screen. It is also the best screenshot in the piece (share card 3).
- **Board title:** What the world reads now
- **Rows (diff styling; quotes as already on the page):**
  - Israel · no genocide charge → “Israel {+began committing genocide+}”
  - Zionism · “[-re-establishment-]” → “{+through colonization+}”
  - Nakba · “[-the destruction of Palestinian society-]” → “{+the ethnic cleansing of Palestinian Arabs by Zionists+}”
  - October 7 · “coordinated [-attacks-]” → “coordinated {+armed incursions+}”
  - Hamas · “[-militant-]” → “{+political organisation with a military wing+}”
  - Gaza genocide · “[-Allegations have been made-]” → “{+carried out by Israel+}”
- Keep the **MOVED THE OTHER WAY** block (1948 expulsion with the Haganah, Irgun and Lehi clause; the October 7 clause, recent) as a static block directly under the board, then the 223/61 ratio line. This keeps MUSTFIX 1–2 next to the main direction.
- The full then/now sentences stay one tap away via the existing “Every quote, dated →” link (`#reads`).
- **Close H2:** keep as built (the veto-safe dated version).

### 5. Card 4 (`#c4`): a safe designation row, and a highlight on the Hebrew words
- **Replace the 31 Oct 2026 row** (“Several countries…”, stamped “days old, may be reverted”) with the research edition's **1 Oct 2026 row**: `1 Oct 2026 · sentence 22 of 23` “Australia, Canada, … and the European Union have designated Hamas as a terrorist organisation.” A stamp saying the row may be reverted kills a share card; the 1 Oct row shows the same position (22 of 23) with no caveat.
- In the Hebrew block, highlight (blue, as added wording) **“ארגון טרור”** in the original and **“terror organisation”** in the English rendering. This is the word the card is about, and it is the only proof block in the edition with nothing highlighted.

### 6. Card 6 (`#c6`): shorter headline (6 phone lines → 3)
- **New H2:** Since September 2025, 10 edits tried to make the Gaza genocide sentence attributed again. Each was gone within 45 minutes.
  (The count 10 and the 45 minutes are both printed on v1, in carousel 2 slide 1, per messaging F7. “Terrorist ×5, about 2.4 hours” stays in the focus line, where it already is.)

### 7. Card 6 body: keep the binding scope, drop the last sentence
- **New body:** These are four sentences, not the whole subject. Across the 254 core, Top- and High-importance topic articles, reverts of edits that removed critical terms came no faster than reverts of edits that added them.
- Drop “What these sentences show is which wording now holds.” It adds a claim (“holds”) and a line, and the scope sentence the messaging check requires is kept verbatim.

### 8. Carousel 1 (`#car1`): cut slide 4, the title-by-language bars
- Remove the “THE GENOCIDE ARTICLE’S TITLE, BY LANGUAGE” slide (`#xwGG` rendering). It is the tallest slide (it sets the carousel's worst-case height) and the slowest to read (“+110 d / renamed +180 d …”). The carousel goes from 5 to 4 slides: Netanyahu → Arabic → Spanish → Hebrew, the exception.
- Make **Hebrew, the exception** slide 2, right after Netanyahu: it is the strongest slide for an Israeli reader, and most readers stop swiping after two.

### 9. Card 7 (`#c7`): the headline should not repeat the quote card word for word
- **New H2:** Wikipedia’s arbitrators found that outside actors are “heavily invested in influencing” its coverage of this topic. They named no side.
  (The fragment is verbatim, lower case as in finding 10. The full quote with its capital O stays in the quote card below, as the builder chose.)
- **Last line, de-duplicated:** That is camp voting, not proof of coordination, and we did not code which side each group took.
  (Drop the trailing “Neither finding names a side.”: the headline now says it, as messaging §2 requires: the no-side statement goes in the headline.)
- Placement (after card 6, not directly after card 5), no direction colours, and the Ïvana clause (owner exception) all stay as built.

### 10. Card 1 (`#c1`): remove the duplicate chip
- Delete the chip “a Jewish state in the territory → a Jewish homeland through colonization”. It is the focus line again, one block lower. Keep the other six chips in this order, strongest first: **re-establishment REMOVED · colonization ADDED · as few Palestinian Arabs as possible ADDED · ethnic ADDED · among the Jewish people REMOVED · Canaan, the Holy Land REMOVED**.

### 11. Card 2 (`#c2`): trim the last body sentence
- Delete: “The Nakba’s first sentence has said “by Zionists” since 6 July 2026, apart from under an hour on 17 July.” The date is already in the proof label (“SINCE 6 JUL 2026”), and the 17 July detail is evidence-room material.
- The body ends on the juxtaposition: “For the Jews who “fled or were expelled from Arab states,” no one is named.” That is the strongest last line in the edition and should not be followed by a date note.

### 12. Close: fix the “In one sentence” box
- It is four sentences and uses single quotes. **Relabel** it “In short” and switch to double curly quotes:
  Before the war, none of the most-read Wikipedia openings on the subject charged Israel with genocide. Now Israel’s own article says, in Wikipedia’s voice, that Israel “began committing genocide.” Zionism is “a Jewish homeland through colonization.” And in every copy we hold, the Israel and Hamas opening sections do not mention the hostages.
  (The last sentence uses the messaging-check scope wording, which replaces “never mention”.)
- If changes 3 and 4 still leave the page over 8 screens, cut this box entirely. The board from change 4 does its job.

---

## The 3 share cards to build (1080×1350)

1. **“Carried out by Israel” / “Some have alleged”** (from card 5). Two equal quote cards: Gaza genocide, first sentence, since 26 Sep 2025, Wikipedia’s own voice, with “carried out by Israel” in blue; October 7 attacks, opening section, now, attributed, with “have alleged” in amber (no strike). Footer: “English Wikipedia · exact text, dated · Israel’s denial is in the Gaza genocide opening section’s last paragraph.”
2. **Hamas in two languages** (from card 4). English 2021 (“militant” struck), English now (“political organisation with a military wing” in blue), Hebrew now (RTL, with “ארגון טרור” in blue and the English rendering under it). Footer: “Opening sentences · English Jan 2021 and since 29 Nov 2025 · Hebrew Oct 2026 · exploratory language comparison.”
3. **What the world reads now** (the six-row board from change 4). Six lines of then → now focus words, one per core article, in diff colours. Footer: “English Wikipedia opening sections, 2021–2026 · every quote exact and dated · one 1948 article moved the other way.”

My round-1 Zionism chip card is now the runner-up: the board covers Zionism in one line, and the board is the stronger single image.

## Expected effect
Changes 3, 4, 8, 11 and 12 should save about 0.7–0.9 phone screens (estimated from the v1 section heights: opening 0.72, close 1.08, car1 worst-case slide). That brings the edition to about 7.2–7.4 screens without dropping a finding. If the editor-in-chief can take only three changes: 1, 2 and 4.
