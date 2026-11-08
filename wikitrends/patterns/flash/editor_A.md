# Flash edition: Editor A's cut (headline & visual)

Editor A: TV news desk plus social/visual-first. I proposed this cut blind to the story editor.
Sources read: the research edition (both tabs, rendered at 390 px with Playwright), page_template.html, PLAN.md, MUSTFIX_owner.md, SYNTHESIS.md, patterns/angle/OCT7.md, patterns/zionism/CODES.md, patterns/langs/langs.json, qa/round_7.json.

## The idea in one line

The Israeli reader should make one jump: *"this is what the world reads about us now."* Every screen sets an exact **then** against an exact **now**. In two places I also set **us** against **them**: how Wikipedia treats Israel against how it treats October 7 and Hamas, and Hebrew Wikipedia against English. No adjectives. The quotes do the work.

Notation in this file: `[-…-]` = removed words (amber, struck); `{+…+}` = added words (blue). This is the existing `.zi-p del/ins` styling (MUSTFIX 12). No new colours.

Length: 8 phone screens (opening, 6 cards, closing with the carousel). There is one more swipe carousel inside card 6.

---

## 1. The cards, in order

### Screen 0. OPENING: Israel's own article (merges hero + the Israel half of #charge)

- **Title (H1, keep the verified r7 text):** Before the war, no top article charged Israel with genocide. Now Israel’s own article does.
- **The one image:** the hero quote card `header.hero .news-q.hero-q`, as built:
  > ISRAEL · OPENING SECTION · NOW · WIKIPEDIA’S OWN VOICE
  > “After the Hamas-led October 7 attacks, Israel {+began committing genocide+} against Palestinians in Gaza.”
  > *The next sentence: “Israel has denied that its actions constitute genocide.”*
- **Focus line:** no sentence charging Israel with genocide → “Israel began committing genocide against Palestinians in Gaza.”
- **Deck (≤40 words):** In Wikipedia’s own voice. The word “genocide” has been in this opening section since 4 May 2025, and the article was viewed 4.6 million times in the past 12 months. Below are six more first lines, then and now.
- **Scope line (one line, small, under the deck; required by MUSTFIX 3):** These are the core articles that carry the narrative and that people read: Zionism, Israel, 1948, October 7, Hamas, the Gaza war.
- **Evidence-room anchor:** `#ev-charge` (the `#ppCard` genocide row).
- *Why first:* it is the most-read article (the country itself), the encyclopedia's own voice, and a genocide charge. It is also the H1 the r7 reviewers already accepted.

### Card 1. ZIONISM (from #zionism; heading kept verbatim, per the owner)

- **Headline:** Zionism was the “re-establishment” of a Jewish state. Now it is “a Jewish homeland through colonization.”
- **Proof visual:** `#ziSum`, the six chips (re-establishment REMOVED · colonization ADDED · ethnic ADDED · among the Jewish people REMOVED · a Jewish state in the territory → a Jewish homeland through colonization · as few Palestinian Arabs as possible ADDED). It reads in two seconds and needs no key. It is the best "what changed" visual on the page.
- **Focus line:** “the [-re-establishment of-] and support for a Jewish [-state in the territory-]” → “to establish and support a Jewish {+homeland through colonization+}”
- **Body (39 words):** This is Wikipedia’s one-line answer to “What is Zionism?” The next sentence now says Zionists wanted “as few Palestinian Arabs as possible.” “Re-establishment” left for good on 9 July 2024. “Colonization” went back in on 27 August 2026 and has stayed.
- **Anchor:** `#ev-zionism` (`#ziPair`, both versions word by word). The full `#ziFig` stepper is one tap away as "Every change, step by step."

### Card 2. 1948 AND THE NAKBA (from #palestine; heading kept)

- **Headline:** The Nakba was “the destruction of Palestinian society.” Now it is “the ethnic cleansing of Palestinian Arabs by Zionists.”
- **Proof visual:** the `#palestine` THEN/NOW `.news-q` pair (Dec 2021 / 2026), with inline diff highlights. Cut the NOW quote after “belongings …”, as the `#reads` Nakba card does, so it fits one screen.
- **Focus line:** “[-was the destruction of-] Palestinian [-society-]” → “{+is the ethnic cleansing of+} Palestinian {+Arabs by Zionists+}”
- **Body (33 words):** Three 1948 articles (Nakba, 1948 Palestine war, 1948 Arab–Israeli War) now name, in Wikipedia’s own voice, who drove the Palestinians out: “Zionists” or “Zionist forces.” For the Jews who “fled or were expelled from Arab states,” no one is named.
- **Anchor:** `#ev-1948` (`#trace`, the revision where each first sentence changed).
- *Juxtaposition:* Palestinian displacement gets a named agent, and Jewish displacement does not. That is the jump for an Israeli reader, and it rests only on the page's own quotes.

### Card 3. OCTOBER 7 AND THE HOSTAGES (split from #oct7)

- **Headline:** Wikipedia’s first line on October 7 said “coordinated attacks.” Now it says “coordinated armed incursions.”
- **Proof visual:** the hostages blockquote from `#ev-oct7`, moved up and made the hero of the card:
  > HOSTAGES · EVERY VERSION SINCE OCTOBER 2023
  > **First sentence:** never, across 107 versions. **Israel and Hamas opening sections:** none, at every snapshot since 2021.
  > *Sentence 9 now:* “251 Israeli and non-Israeli civilians and soldiers were taken as hostages to the Gaza Strip”

  Put the first-sentence then/now diff above it as the focus line.
- **Focus line:** “a series of coordinated [-attacks-]” → “a series of coordinated {+armed incursions+}” · “rape and sexual assault [-by Hamas fighters-]” → “{+dozens of cases of+} rape and sexual assault”
- **Body (30 words):** The hostages first appear in sentence 9. In January 2024 the rape sentence named “Hamas fighters”; now it names no perpetrator. The opening still says “massacring civilians in 21 communities.”
  - *Why the last sentence:* it is verbatim (`#ev-oct7` notes; OCT7.md §6, sentence 4) and stops the press reading the card as “Wikipedia erased October 7.”
- **Anchor:** `#ev-oct7` (the `o7Fig` "October 7" tab, with the "massacre" blips and the empty hostages lane).
- *Accuracy guard:* Hamas is still named later in the same first sentence (“carried out by Hamas and several other Palestinian militant groups”). The headline must not suggest otherwise, which is why only “attacks → armed incursions” is quoted. For the hostages in the Israel and Hamas openings, say “none of our four copies … since 2021”, not “never”.

### Card 4. HAMAS, IN ENGLISH AND IN HEBREW (split from #oct7, merged with the Hebrew cell of #crosslang)

- **Headline:** In 2021 Wikipedia called Hamas “militant.” Now it is a “political organisation with a military wing.”
- **Proof visual:** one three-line definition stack. Every string already appears on the page: the `#reads` Hamas card, and the Hebrew Hamas cell in the `#xmFig` / `#xrFig` tooltips.
  > ENGLISH · 2021: “… a Palestinian Sunni-Islamic [-fundamentalist but pragmatic, militant,-] and nationalist organization.”
  > ENGLISH · NOW: “… a Sunni Islamist Palestinian nationalist {+political organisation with a military wing+} known as the al-Qassam Brigades.”
  > עברית · NOW: “חַמַאס (בערבית: حماس) הוא ארגון טרור פלסטיני אסלאמיסטי-סוני הפועל גם כתנועה פוליטית.” *(“… a Palestinian Sunni-Islamist terror organisation that also operates as a political movement.”)*
- **Focus line:** “[-militant-]” → “{+political organisation with a military wing+}” · Hebrew: “ארגון טרור … הפועל גם כתנועה פוליטית” (terror organisation that also operates as a political movement)
- **Body (34 words):** Hebrew Wikipedia puts it the other way around. In English, the terror designation moved from sentence 5 of 20 (2021) to sentence 22 of 23 (October 2026). “Militant” became “military” on 12 October 2023, five days after the attack.
- **Anchors:** `#ev-oct7` (the `o7Fig` Hamas tab) and `#ev-xl` (the `#xrFig` Hamas Hebrew moment). Label the Hebrew line "Other languages · exploratory", as the research edition does.
- *Why the merge:* the Hebrew/English mirror is the cleanest "us versus the world" image in the whole study, and it is exactly what an Israeli reader does not know. The `#o7Pos` strip (sentence 5 → 22) becomes a small two-row inset (1 Jan 2021 and 1 Oct 2026 rows only). Do NOT use the 31 Oct 2026 “Several countries” row: the page itself says it may be reverted.

### Card 5. THE GENOCIDE CHARGE, BOTH WAYS (split from #charge, new juxtaposition from #reads + #ev-oct7)

- **Headline:** Wikipedia said “Allegations have been made” that Israel committed genocide. Now it says “the ongoing, intentional, and systematic destruction … carried out by Israel.”
- **Proof visual:** two quote cards stacked, the same component (`.news-q`), the same size:
  > GAZA GENOCIDE · FIRST SENTENCE · SINCE 26 SEPTEMBER 2025 · WIKIPEDIA’S OWN VOICE
  > “The Gaza genocide is the ongoing, intentional, and systematic destruction of the Palestinian people in the Gaza Strip carried out by Israel during the Gaza war.”
  >
  > OCTOBER 7 ATTACKS · OPENING SECTION · NOW · ATTRIBUTED
  > “Some have alleged that the attack was an act of genocide or a genocidal massacre against Israelis.”
- **Focus line:** “[-Allegations have been made that the 2023 Israel–Hamas war constituted a-] genocide” → “{+The Gaza+} genocide {+is the ongoing, intentional, and systematic destruction … carried out by Israel+}”
- **Body (38 words):** The charge against Israel is stated as fact. The charge about October 7 is “alleged.” Of the 150 most-read opening sections, none charged Israel with genocide before the war; seven do now. Netanyahu’s states it as fact, with no denial.
- **Anchors:** `#ev-charge` (`#ppFig`, genocide row 0 · 0 · 7+1) and `#ev-oct7` (the notes paragraph quoting “Some have alleged”).
- *Why this card exists:* the owner's list has Israel's genocide in Wikipedia's own voice. On its own, that is the opening card again. The shock comes from the asymmetry, which is in the research edition's own "What this means" line (#ev-oct7): “the genocide charge against Israel is stated as fact … while the one against Hamas is ‘alleged.’” Both quotes are verbatim and already on the page (template lines ~1591 and ~1618; OCT7.md §7).

### Card 6. WHAT STAYS AND WHAT IS UNDONE (new card from #ev-oct7, #o7Fig and #zionism; the owner's "critical wording lasts" point)

- **Headline:** Every edit that tried to put “alleged” back into the Gaza genocide sentence was gone within 45 minutes. “Terrorist” went into Hamas’s first sentence five times; the longest stay was about 2.4 hours.
- **Proof visual:** carousel B (below): the `#o7Fig` timelines, one swipe per article, each showing the short-lived marks.
- **Focus line:** “{+alleged+}” put back → gone within 45 minutes · “{+terrorist+}” ×5 → longest about 2.4 hours · “{+massacre+}” in October 7’s first sentence → about an hour in all, across 107 versions
- **Body (40 words):** Zionism’s sentence, too. Since November 2024, “colonial” was taken out 10 times, and each removal was undone within a day. Of 70 own-voice edits that made it less critical, 64 were gone within a day, against 47 of 78 that made it more critical.
- **Anchor:** `#ev-oct7` (`#o7Fig`, all three tabs) and `#ev-zionism` (“the fight, and how changes were counted”).
- *Honesty inside the card:* I keep the 47-of-78 counterpart on purpose. Without it, “64 of 70” overstates, and the messaging agent would veto it. The concrete words (45 minutes, 2.4 hours, an hour) carry the shock without overstating.

### Screen 7. CLOSING: "What the world reads now" (carousel A) + one ratio + the honesty line

- **Headline (two sentences, the summary in house shape):** In 2021 these first lines spoke of “re-establishment,” “militant” and “coordinated attacks.” Now they say “colonization,” “ethnic cleansing … by Zionists” and “genocide.”
  - *Literal check:* “re-establishment” (Zionism 2021), “militant” (Hamas 2021) and “coordinated attacks” (October 7, Oct 2023: technically not 2021) → change to “Before the war, these first lines …” so the dates hold. “Colonization” (Zionism), “ethnic cleansing … by Zionists” (Nakba) and “genocide” (Gaza genocide first sentence; Israel's opening section) all appear in first sentences or opening sections. Every word can be checked on the carousel slides below it.
- **Visual:** carousel A (below).
- **Closing line (the ratio, from #against):** For every critical term taken out of these opening paragraphs, almost four went in: 223 in, 61 out. On comparison pages: 125 in, 73 out.
- **The one honesty line:** This measures what Wikipedia says, not whether it is true; the change is in the core, most-read articles, not in the long tail of short pages.
- **Link:** “Full research edition →” (the frozen research-edition artifact) and “Every quote, dated →” `#reads`.

---

## 2. Carousels

### Carousel A: "What the world reads now" (closing screen). The spine is `#reads`.

Each slide is one `#reads` then/now card with the diff already built. Slide order follows the cards above, so the carousel works as a recap:

1. **Israel** (`#reads` card 2): “Before the war: no sentence. Now: ‘Israel began committing genocide against Palestinians in Gaza.’”
2. **Zionism** (`#reads` card 1): “‘Re-establishment’ out; ‘through colonization’ in.”
3. **Nakba** (`#reads` card 5): “From ‘the destruction of Palestinian society’ to ‘ethnic cleansing … by Zionists.’”
4. **October 7** (`#reads` card 4): “‘Coordinated attacks’ became ‘coordinated armed incursions.’”
5. **Hamas** (`#reads` card 3): “‘Militant’ out; ‘political organisation with a military wing’ in.”
6. **Gaza genocide** (`#reads` card 6): “‘Allegations have been made’ became ‘systematic destruction … carried out by Israel.’”
7. **Hebrew vs English, October 7** (`#xrFig` / the `#xmFig` Oct 7 column, Hebrew row): Hebrew first sentence “טבח שבעה באוקטובר היה מתקפת פתע רחבת היקף שביצעו ארגוני הטרור הפלסטיני…” (“The Seventh of October massacre was a large-scale surprise attack carried out by the Palestinian terror organisations…”). Caption: “Hebrew: ‘massacre’ and ‘terror,’ in its own voice. English: neither, in its first sentence.” Tag: exploratory.
8. **Other languages, genocide** (`#xmFig` genocide column, the outlined es · pt · ar cells; or `#xmFind`): “Spanish, Portuguese and Arabic once attributed the genocide charge. Now they state it as fact, as English does.” Optional second line: Spanish Gaza war calls October 7 “un ataque de represalia” (a retaliatory attack). Tag: exploratory.
9. **Moved the other way** (`#reads` card 7, 1948 expulsion): “One 1948 article went the other way: ‘by Zionist militias’ left its first sentence in May 2025.” This keeps a real opposite edit in view (MUSTFIX 1), with the ratio line directly under the carousel.

### Carousel B: "How long a word lasts" (card 6). The spine is `#o7Fig`.

Use the existing `#o7Art` switch as swipe slides, at a fixed frame (no stepper controls in flash):

1. **Gaza genocide** tab: attribution lane plus attempt ticks. Caption: “Own voice since September 2025; every attempt to put ‘alleged’ back was gone within 45 minutes.”
2. **Hamas** tab: “militant” lane plus amber “terrorist” dots. Caption: “‘Terrorist’ went in five times; the longest stay was about 2.4 hours.”
3. **October 7** tab: “armed incursions” lane, “massacre” blips, empty hostages lane. Caption: “‘Massacre’: about an hour in all, across 107 versions. Hostages: never in the first sentence.”
4. **Zionism** `#ziFig`, frozen on phase 3 “Mostly in”. Caption: “‘Colonial’ taken out 10 times since November 2024; each removal undone within a day.”

(Optional carousel C, only if the EIC wants the scrolly kept in some form, since the owner loves it: one slide of `#kChart` with the October 7 spike. Caption: “In the three weeks after October 7, new critical terms ran at 13.7 a week, against 3.8 before.” I would not spend a screen on it. See the cut list.)

---

## 3. Merges and splits

| Action | What | Why |
|---|---|---|
| MERGE | hero + the Israel half of `#charge` → Screen 0 | The hero quote and the #charge Israel card are the same sentence; showing it twice wastes a screen. |
| SPLIT | `#charge` → Israel (Screen 0) / Netanyahu + 0→7 + the asymmetry (Card 5) | The 0→7 count and “Netanyahu, no denial” are strongest next to the October 7 “Some have alleged” quote, not as a repeat of the Israel quote. |
| SPLIT | `#oct7` → Card 3 (October 7 + hostages) and Card 4 (Hamas) | #oct7 packs four findings into one deck paragraph. In flash, each needs its own one-glance proof. |
| MERGE | Hebrew Hamas cell from `#crosslang` into Card 4 | The 11×7 grid fails the five-second test on a phone. One Hebrew sentence beside the English one gives the cross-language finding at a glance. |
| MERGE (new card) | `#ev-oct7` deck (2.4 h, massacre ~1 h) + the `#o7Fig` Gaza genocide note (45 min) + `#zionism` phase 3 + the CODES 78/70 line → Card 6 | The owner's "critical wording lasts, the opposite is undone within a day" is spread over four places in the research edition. Brought together, it makes one card. |
| PROMOTE | `#reads` (evidence room) → closing carousel A | It is already the flash edition in miniature: seven then/now cards with diffs. |
| SHRINK | `#against` → one ratio line + carousel A slide 9 | Keeps exactly the opposite-direction evidence and its proportion (MUSTFIX 1–2). No balance claims from non-changes. |
| SHRINK | `#trust` → the one honesty line | Owner: exactly one honesty line. |

---

## 4. Cut list (dropped from flash; all stay in the research edition)

- **`#after` scrolly (battles).** The owner loves it, but its own caption says “a change that lands after a battle gives a date, not a cause,” and four of its five cards show “no clear rise.” In flash, a chart that needs that caveat is soft. *Flag to the EIC: the owner may want it kept; if so, carousel C, one slide.*
- **`#organised` (network graph, voting camps, ArbCom).** The findings are a pool of regulars and camp-like voting, “not proof of coordination”, and ArbCom names no side. After six cards that all move one way, an ArbCom quote about “outside actors” would *imply* a side to an Israeli reader. That breaks MUSTFIX 10/11 by juxtaposition, even with exact words. It is too nuanced for one glance, so it stays in the research edition.
- **`#crosslang` full grid (`#xmFig`) and the court-overstatement grid.** Too dense for a phone flash; reduced to carousel slides 7–8 and the Hebrew line in Card 4.
- **`#ziFig` full stepper and `#ziCard`.** Kept as a link. Flash shows the result (`#ziSum`), not the 292-step process.
- **`#ppFig` full charge grid, the killing/massacre counts (9→26, 8→23), the 23.6% → 26.4% shares.** Not clear statistically, and they need long explanation (Book of Joshua, Entebbe). Only the genocide row's 0 · 0 · 7 survives.
- **`#trust` statistics (10.3% vs 4.4%, +5.9 points), `#reach`, `#tierFig`, `#board`, `#test`, `#vocab`, `#sourcing`, `#ratchet` survival curves, `#checks`, the method, the ledger, the data lab.** Research process and population framing (MUSTFIX 3–4).
- **The “Several countries” Hamas row (31 Oct 2026).** The page says it may be reverted. Too fragile for a screenshot.
- **The October 7 genocide clause removed from sentence 2 (1 Oct → 2 Nov 2026).** A genuine opposite-direction edit, but “recent and may be undone.” The 1948 expulsion slide covers that role more safely.
- **Israeli settlement history.** It goes both ways (out in 2022, back on 4 Nov 2026) and needs three dates to explain. Soft for flash.
- **Jewish ties to the land (homeland 5→1, K11 11 vs 6, land names 11→19), antisemitism 37→54.** Mixed or uncoded. MUSTFIX 1 says never as balance, and in flash there is no room to give both directions properly.
- **Hamas dropped from the Gaza war first sentence, and “Hamas-led” dropped from the October 7 title (26 May 2025).** The research edition says the title change matches common usage and that nothing links the two edits. It invites a conspiracy reading. Cut.
- **Hannibal Directive sentence (October 7 sentence 11).** High echo, but I can only anchor its *now* (and the 1 Oct 2026 “at least 14 … killed” variant), not a clean *then*. It would need a verified “not in Jan 2024” check before it could be a then/now. *Flag: possible add if the EIC verifies the 1 Jan 2024 lead lacks it (OCT7.md lists the Jan 2024 lead contents; it does not mention Hannibal, but that is not stated as an absence check).*
- **1948 Arab–Israeli War “Plan Dalet” sentence, the West Bank, Hezbollah, the heartbeat chart, the galaxy.** Already covered by Card 2, or off the core.

---

## 5. Opening and closing (summary)

- **Title:** Before the war, no top article charged Israel with genocide. Now Israel’s own article does.
- **Deck:** In Wikipedia’s own voice. The word “genocide” has been in this opening section since 4 May 2025, and the article was viewed 4.6 million times in the past 12 months. Below are six more first lines, then and now.
- **Single image:** the hero quote card (`.hero-q`) with “began committing genocide” highlighted, and the denial line under it.
- **Closing line:** For every critical term taken out of these opening paragraphs, almost four went in: 223 in, 61 out.
- **Honesty line:** This measures what Wikipedia says, not whether it is true; the change is in the core, most-read articles, not in the long tail of short pages.

---

## 6. The three shareable quote cards (screenshot-ready, 1080×1350 / phone frame)

**Share card 1: "Stated as fact / ‘alleged’"** (strongest)
> ENGLISH WIKIPEDIA · FIRST SENTENCE · GAZA GENOCIDE · SINCE 26 SEP 2025
> “The Gaza genocide is the ongoing, intentional, and systematic destruction of the Palestinian people in the Gaza Strip carried out by Israel during the Gaza war.”
> ENGLISH WIKIPEDIA · OPENING SECTION · OCTOBER 7 ATTACKS · NOW
> “Some have alleged that the attack was an act of genocide or a genocidal massacre against Israelis.”
> *Footer:* Exact text, dated. Israel’s denial appears in the Gaza genocide opening section's last paragraph.
  - The footer clause about the denial is fair-play context (OCT7.md: “Israel and its supporters maintain that its actions do not constitute genocide …”). Keep it short, or link it.

**Share card 2: "Hamas, in two languages"**
> HAMAS · ENGLISH WIKIPEDIA · 2021: “… fundamentalist but pragmatic, militant, and nationalist organization.”
> HAMAS · ENGLISH WIKIPEDIA · NOW: “… nationalist political organisation with a military wing …”
> חמאס · ויקיפדיה העברית · עכשיו: “ארגון טרור פלסטיני אסלאמיסטי-סוני הפועל גם כתנועה פוליטית.”
> *(Hebrew, now: “a Palestinian Sunni-Islamist terror organisation that also operates as a political movement.”)*
> *Footer:* Opening sentences, Jan 2021 and Nov 2025 (English) / Oct 2026 (Hebrew). Exploratory language comparison.

**Share card 3: "Zionism, then and now"**
> ZIONISM · ENGLISH WIKIPEDIA · FIRST SENTENCE
> 2021: “… the [-re-establishment-] of and support for a Jewish state in the territory defined as the historic Land of Israel …”
> NOW: “… to establish and support a Jewish homeland {+through colonization+} in the region of Palestine …”
> + the next sentence: “Zionists wanted to create a Jewish state in Palestine with as much land, as many Jews, and {+as few Palestinian Arabs as possible+}.”
> *Footer:* 292 changes to this one sentence since 2021. Text as of 5 Nov 2026.

(The runner-up is the opening Israel quote card, which works as a share card already.)

---

## 7. Flags for the EIC and the messaging agent (no new numbers introduced)

1. **“10 attempts … each gone within 45 minutes” (Gaza genocide).** “Within 45 minutes” is page text (the `#o7Fig` Gaza genocide how-to). The count 10 is in OCT7.md §7 but is NOT printed on the page (the chart draws ticks from `D.T.attempts`). I wrote “every edit that tried”, with no count. If the EIC wants “10”, assert it in the build from `D.T.attempts`.
2. **Card 6 Zionism numbers.** I use the page's 78/70 and 64/70 vs 47/78 (CODES headline cell), as the r7 EIC chose. Do NOT mix in “336 vs 38 days” (CODES) or 88/77 (old page): MUSTFIX 9. “Colonial taken out 10 times … each undone within a day” is the `#ziFig` phase 3 text.
3. **Closing headline dates.** “Coordinated attacks” is from Oct 2023, not 2021. Use “Before the war, …”, not “In 2021, …”.
4. **Hebrew quotes.** Taken from `langs.json` (Hamas `he` s1 latest, rev 43994741, 2026-10; October 7 `he` s1 latest, rev 44000524). Both render in the `#xmFig`/`#xrFig` tooltips. Keep the “exploratory” tag. Render RTL with `dir="rtl"`.
5. **Netanyahu quote.** The page shows it with and without a final period (story card ends “December 2023”; #ev-charge ends “December 2023.”). Pick the stored text.
6. **Card 5 date for the October 7 “Some have alleged.”** It is from the “now” lead (2 Nov 2026 copy per OCT7.md). Print “now (2 Nov 2026 copy)” if space allows.
7. **Hostages.** “Never, across 107 versions” is for October 7's first sentence; “none of our four copies since 2021” is for the Israel/Hamas openings. Do not merge them into one “never”.
8. **4.6 million views** is generated by the build from page-view data (the hero deck). Reuse the same variable, not a hard-coded string.

## Reasoning notes (for my round-2 review)

- Order logic: the country (Israel) → the idea (Zionism) → the founding (1948) → the trauma (October 7) → the enemy's name (Hamas) → the charge, both ways → the mechanism (what lasts) → the recap. Each card escalates the "us vs how they write us" jump, and the asymmetry card (5) is the peak, placed after the reader has seen the individual shifts.
- What I would fight for in synthesis: Card 5 (asymmetry) and the Hebrew line in Card 4. These are the two juxtapositions that make Israelis share, and both are verbatim from material already verified in the research edition.
- What I would give up first: carousel B slide 4 (Zionism repeat), then carousel A slides 7–8 (languages, exploratory).
- The review test for the built flash: can each card be understood from its focus line alone, in under a second, with highlighted words? Does any card need its body to be true? (It shouldn't.) Is there any adjective that does work the quotes should do?
