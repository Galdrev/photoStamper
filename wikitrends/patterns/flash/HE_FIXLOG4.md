# Flash edition: fix log 4 (owner, tested on an iPhone: the treemap, the fight lanes, the hostages block)

**Build:** `cd wikitrends && python build_flash.py --bilingual OUT.html`. The single-language builds (`build_flash.py OUT.html`, `build_flash.py --lang he OUT.html`) still run every check. The research edition is untouched (`page_template.html` and `build_page.py` not edited).

**Standards:** `HE_PROOF_1.md` (idiom, grammar, RTL, punctuation, no italic, no-break space in dates, no English in the UI) and `HE_PROOF_2.md` (fidelity of agency, modality and attribution; no sharpening or softening). Scopes: `messaging_check.md` F3 and `FACTCHECK_hostages.md`; recount: `patterns/flash/factcheck_hostages.py` (rerun, `factcheck_hostages.json` unchanged).

## 1. The treemap is replaced by one 100% bar (hero, `#flTiles`)

**Owner:** "not looking good on iPhone": hyphenated, broken labels (Ne-tanyahu, Pa-les-tine); big unrelated tiles (Adolf Hitler, Debbie Rowe, Mel Brooks) pulling the eye; tiny unreadable tiles.

**Now:**
- Headline: "**Now 7 of the 150 most-read openings charge Israel with genocide**, two as fact, and they got **12.4%** of the views of all 150. In Jan 2021 and Jul 2023, none did." (the share is shown to the decimal, as fact-checked; it used to be rounded to 12%).
- The Jan 2021 / Jul 2023 / Now switch is kept.
- **One bar** of the 150 openings' views (Nov 2025 – Oct 2026, monthly sums from our crawl). The seven charged openings come first: solid teal = stated as fact (Benjamin Netanyahu, Israel), light teal = attributed (Palestine, Israeli–Palestinian conflict, Gaza Strip, Israel Defense Forces, Gaza–Israel conflict). The other 143 are one grey segment, labelled "143 other openings". A bracket over the coloured part: "7 openings: 12.4% of the views".
- **Under the bar, the seven by name**, each with its views (7.0 million … 155,000) and its voice tag ("stated as fact" / "attributed"). Tap a name or a segment: the tooltip with the exact charge sentence (Hebrew: with our translation), as before.
- Jan 2021 and Jul 2023: every segment grey, the label says "Jan 2021: none of the 150 charged Israel with genocide", the tags say "no charge". **Now:** the seven fill in left to right, one every 0.7 s (about 4.5 s). A touch ends the play at once. Reduced motion: the final state, no transitions.
- **No hyphenation and no mid-word breaks:** `hyphens:none`, `overflow-wrap:normal`, `word-break:normal` on the whole figure; article names wrap only between words. The build asserts it; the smoke suite checks every word of the figure has one line box.
- The unrelated large articles are no longer drawn at all; they are inside "143 other openings".

**Deviation:** the true width of the smallest segment (Gaza–Israel conflict, 0.11% of the views) is 0.4 px on a phone; each coloured segment is drawn at least 1.5 px so all seven can be seen. The grey segment absorbs the difference (at most 1.1 px in total). The smoke check allows for it.

**Checks:** the build recomputes the seven, their order and their printed views from `data/mass2.json` and `perp_codes.jsonl` and fails on any drift (`7.0 million, 4.6 million, 2.4 million, 1.0 million, 816,000, 745,000, 155,000`; 143 others; 12.4%). The page computes the bracket label and the share from `R.tm`; the smoke suite checks each segment's width against the stored views, the list against `R.tm`, the labels in all three states and the fill pacing.

## 2. The fight lanes, simplified (card 1, `#flFb`)

**Owner:** "too condensed, people don't understand it, too much text".

**Now:**
- Header: "**The fight over the words:** since Jan 2021, 100 words were put in and taken out of this sentence, some again and again." (100 is the page's own count, asserted in the build).
- **The top 4 phrases by default;** "Show all 8" (at the end of the legend line, just above the list) expands to eight and becomes "Show the top 4".
- Each row: the phrase in large type (18 px; Hebrew: our gloss beside it), the count in words ("put in or taken out **81** times"), a one-word state (**IN** / **OUT**, at the cursor's date) and a thin lane strip under it (blue = in, empty = out, one tick per change, the 7 October line dotted).
- **One legend sentence:** "Each line is one phrase over time: blue = in the sentence, empty = out; every tick is one edit." The "⇄n = removed or restored n times" key is gone; the grey "in, as in Jan 2021" and the amber "out, though in Jan 2021" encodings are gone (every in-span is blue).
- The sweep still drives the lanes: the counts run to the cursor's date, the states follow it, a row pulses when its phrase flips; reduced motion: no pulse.

**Deviations, for precision and length:**
- The owner's header "100 words were put in and taken out again and again" does not hold for every word: a word that went out once and came back once has two changes. So "again and again" is attached to "some".
- "Tap a line for its dates" was dropped from the legend to stay inside the phone length budget. The rows are still buttons (tap or Enter: the dated history, as before).

**Checks:** counts as computed and asserted (`colonization 81, land outside 54, Palestine a region 40, Land of Israel 40, Jewish history 37, homeland 35, Jewish people 35, Jewish state 29`). The smoke suite's independent recount now also checks each row's count in words and its IN/OUT state, at rest and at three sweep dates.

## 3. The hostages block, with its message in words (card 3, `#c3m`)

**Owner:** "a nice visual, but it's not really understood what it means or what it's trying to convey".

**Now:**
- **A plain headline leads the block:** "251 people were taken hostage on October 7. In 9 of 10 Wikipedias, the article’s first sentence does not mention them." It is visible at once; the slow fill (the 251, its sentence, the ten editions one by one) follows as before.
- The big **251** and its source line ("English · only here: sentence 9 of the opening section" and the sentence) are kept.
- **Each slot says what it holds:** "no hostages" in muted type inside the dashed box (nine editions); Italian, filled: "names them: rapimento". No tap is needed to get it.
- **Under the grid:** "The nine mention them further down the opening section; English, only in sentence 9."
- **The scope line, shortened:** "Latest copies, Oct–Nov 2026, of the ten Wikipedias with an article on the attack. Hebrew’s first sentence named them in our copies from October 2024 to October 2025." (The "9 of 10" and "all ten mention them" of the old paragraph now sit in the headline and the line above.)
- **Share image** (`wikipedia-hostages-first-sentence(-he).png`): the headline, the 251 and sentence 9, the ten slots with their words, the further-down line, the scope line, the report's scope line, date and source. Card 3's own image carries the headline and the scope line in its hostages row.

**Scope check (messaging_check.md F3, FACTCHECK_hostages.md, factcheck_hostages.json):**
- "251 … taken hostage": sentence 9 of the 2 Nov 2026 English copy, the only one with a hostage word.
- "9 of 10 … the first sentence does not mention them": latest copies; only Italian matches.
- "The nine mention them further down the opening section": every one of the nine has a mention after sentence 1 (held text for he, ar, nl, ru; the 2 Nov 2026 English copy; full-section counts for de, fr, es, pt). Arabic says "captured", not "hostages"; its panel says so, as before. "The nine" excludes Italian on purpose (Italian names them in sentence 1).
- "English, only in sentence 9": `hostage_sentences: [9]`.
- Hebrew Oct 2024 – Oct 2025: five quarterly copies.

**Deviations, for precision:** the owner's "doesn't say so" became "does not mention them" ("say so" could be read as "does not say 251", and Italian says "about 250"). The owner's "They are mentioned further down the opening" became "The nine mention them further down the opening section" (Italian's is in the first sentence).

## 4. Hebrew strings (HE_PROOF_1 / HE_PROOF_2 standard)

Read on the rendered page (iPhone 13, light and dark), in the string map (`flash_i18n_he.json`) and in the overlay. Quotes in “…” are originals and were not touched. **A** = changed during the proof; **K** = kept as drafted.

| # | String | Status | Reason |
|---|---|---|---|
| 1 | Bar headline «**היום 7 מתוך 150 פתיחי הערכים הנקראים ביותר מאשימים את ישראל ברצח עם**, שניים מהם כעובדה, והם קיבלו **12.4%** מהצפיות בכל ה־150. בינואר 2021 וביולי 2023 אף אחד מהם לא האשים.» | K | "openings" = פתיחי הערכים (glossary); «מאשימים … ברצח עם» and «כעובדה» as in the old caption (HE_FIXLOG2 #13); «בכל ה־150» kept. |
| 2 | Bracket «7 פתיחים: 12.4% מהצפיות»; grey segment «143 פתיחים אחרים» | K | Short noun labels; the percent sign after the number, as elsewhere on the page. |
| 3 | Then labels «ינואר 2021: אף אחד מ־150 הפתיחים לא האשים את ישראל ברצח עם» (and יולי 2023) | K | Past tense, the same verb as the headline. |
| 4 | Voice tags «נקבע כעובדה» / «מיוחסת לאחרים» / «אין האשמה» | K | The three voice labels of the treemap (HE_FIXLOG2 #14): attributed is not «נטען» (softer), fact is not «הוכח» (sharper). «מיוחסת» agrees with the implied האשמה. |
| 5 | Views «7.0 מיליון», «816,000» | K | Numbers as on the English page. |
| 6 | Caption «150 פתיחי הערכים הנקראים ביותר שהיו קיימים ב־2021. צפיות בנובמבר 2025 – אוקטובר 2026, סכומים חודשיים מהסריקה שלנו. הקישו על שם כדי לראות את המשפט.» | A | Draft «על שם הערך» → «על שם»: one word shorter, same referent (length budget). Article names stay in the original (HE_FIXLOG2 #29). |
| 7 | Bar and list aria «פס אחד: הצפיות בדפים של 150 הפתיחים. היום שבעת הפתיחים שמאשימים את ישראל ברצח עם קיבלו 12.4% מהן; שניים מהם קובעים זאת כעובדה.» / «שבעת הפתיחים שמאשימים את ישראל ברצח עם» | K | "page views" = «צפיות בדף» (as the old key). |
| 8 | Grey-segment tooltip «אין האשמה ברצח עם בפתיח הערך, לא אז ולא היום» | K | |
| 9 | Lanes header «**המאבק על המילים:** מאז ינואר 2021 הוכנסו למשפט הזה והוצאו ממנו 100 מילים, חלקן שוב ושוב.» | K | Passive, as the English (no editor is named or implied); "some" = «חלקן» (fem., מילים). |
| 10 | Count «הוכנס או הוצא 81 פעמים»; «פעמיים»; «פעם אחת»; «עדיין בלי שינוי» | K | Masculine singular (הביטוי). Hebrew dual for 2 and «פעם אחת» for 1 instead of «2 פעמים» / «1 פעמים». «עדיין בלי שינוי» as in the lane tooltip. |
| 11 | State «בפנים» / «בחוץ» | K | One word each, like IN / OUT; set in Heebo, not in the mono face. |
| 12 | Legend «כל שורה היא ביטוי אחד לאורך זמן: כחול = במשפט, ריק = מחוץ למשפט; כל סימון הוא עריכה אחת.» | A | "tick" = «סימון», not the loan «טיק». The draft's «הקישו על שורה כדי לראות את התאריכים» was dropped with the English (length). |
| 13 | Toggle «הצגת כל 8 הביטויים» / «הצגת 4 המובילים בלבד» | K | Noun-form UI action, as «הצגת התאריכים» elsewhere. |
| 14 | Row aria «…(קולוניזציה): הוכנס או הוצא 81 פעמים עד …; הצגת התאריכים» | K | |
| 15 | Phrase glosses (FB_HE: «קולוניזציה», «ארץ מחוץ לאירופה», …) | K | Unchanged; now beside the phrase, at the reading start of the row (right). The phrase stays the original English, left to right; the strip stays left to right. |
| 16 | Hostages headline «ב־7 באוקטובר נחטפו 251 בני אדם. ב־9 מתוך 10 ויקיפדיות, המשפט הראשון של הערך אינו מזכיר אותם.» | A | Draft «המשפט הראשון **בערך**» → «**של הערך**»: «בערך» alone reads as "approximately". "taken hostage" = «נחטפו» (glossary: hostages = החטופים). No-break spaces in «7 באוקטובר» (build) and «9 מתוך». |
| 17 | Slots «אין חטופים» | K | The owner's wording; it matches the panel's slot label «אין חטופים במשפט הזה» (HE_FIXLOG3 #8). It sits under the kicker «המשפט הראשון» and right after the headline that states 251 were abducted, so it reads "no hostages [in this sentence]", not a denial. |
| 18 | Italian slot «מזכיר אותם: rapimento» | K | Masculine (המשפט); the Italian word stays in the original (lang="it"). |
| 19 | Under the grid «בתשע האחרות הם מוזכרים בהמשך פתיח הערך; באנגלית, רק במשפט 9.» | A | Draft «תשע האחרות מזכירות אותם» → passive «הם מוזכרים»: the Wikipedias do not act; their opening sections contain the mention. No-break space in «במשפט 9». |
| 20 | Scope «לפי העותקים האחרונים שלנו (אוקטובר–נובמבר 2026) של עשר הוויקיפדיות שיש בהן ערך על המתקפה. בעברית, המשפט הראשון הזכיר אותם בעותקים שלנו מאוקטובר 2024 עד אוקטובר 2025.» | K | Both scopes kept: our latest copies; the ten editions with an article; the Hebrew exception in our quarterly copies. |
| 21 | Share images: the same strings, drawn right to left; the English sentence 9 left to right with our translation under it | K | |

**Totals:** 21 rows; 4 changed (A), 17 kept. No English in the visible Hebrew UI outside the originals and article names (smoke check), no italic, every day–month date with a no-break space (smoke check).

## 5. Length, smoke tests, screenshots

**Build:** `scratchpad/flash/v3fix/index.html` (begins with `<!DOCTYPE html>`, the charset meta and the viewport meta). Rebuilt twice from this commit: byte-identical (`cmp`). Research edition: `page_template.html` and `build_page.py` untouched.

**Phone length** (390×844, iPhone 13 profile, fonts loaded, every lazy piece drawn; the smoke suite's figure): **English 10.87** (reduced motion 10.85), **Hebrew 10.97** (10.97); both ≤ 11.0. Before: 10.85 / 10.99. At 1280: English 10.52, Hebrew 11.27 (no target). Per block on the phone (English / Hebrew, px): reach bar 372 / 377 (treemap 423 / 404); fight lanes 396 / 380 (409 / 410); hostages block 387 / 368 (305 / 324).

**Suites** (`scratchpad/flash/v3fix/smoke_core.js`, `smoke_bi.js`, `smoke_lab.js`; iPhone 13 and 1280, light and dark, plus reduced motion, both languages). New checks:
- reach bar: seven segments sized by the stored views, the other 143 one segment, the bar 100% wide; the list of seven in order with their views; labels and tags in all three states; Now fills one by one (≥ 3 s), reduced motion at once; a tap shows the voice and the sentence; **no word broken across lines and no hyphenation** anywhere in the figure (every word has one line box);
- fight lanes: 8 lanes, the top 4 shown, "Show all 8" / "Show the top 4" (Hebrew too); counts in words and IN/OUT states equal the independent recount at rest and at three sweep dates; no ⇄; the phrase ≥ 17 px; the Hebrew gloss on every row; the one-sentence legend;
- hostages block: the headline leads and is visible from the start of the pacing; every slot's words ("no hostages" ×9, "names them: rapimento"; Hebrew «אין חטופים», «מזכיר אותם: rapimento») and that they fit their box; the further-down line; the short scope line; the share image carries the same headline, slot words and lines;
- the bilingual suite checks the new headline, the bar label, the toggle and the counts switch language;
- `hosted()`: the downloads capability now resolves on the test's signal instead of a 700 ms timer (a slow font load made the old timing flaky; the check itself is unchanged).

| Suite | Pass | Fail |
|---|---|---|
| core (5 configurations × 2 languages) | 1331 | 0 |
| bilingual | 328 | 0 |
| Data lab | 185 | 0 |

0 console errors or warnings and 0 horizontal overflow in every configuration.

**Phone screenshots** (`scratchpad/flash/v3fix/phone/`): `bar_{en,he}_{light,dark}.png`, `bar_{en,he}_jul2023.png`, `lanes_{en,he}_{light,dark}.png`, `lanes_en_all8.png`, `moment_{en,he}_{light,dark}.png`, and the share images `wikipedia-hostages-first-sentence.png`, `wikipedia-hostages-first-sentence-he.png`.

## 6. Follow-up: shares in the bar's list, not absolute views; the then-label on one line

**Why:** the list showed Netanyahu 7.0M and Israel 4.6M (monthly crawl sums, Nov 2025 – Oct 2026), while the reach section shows 7.9M and 5.1M (daily sums, 9 Nov 2025 – 8 Nov 2026). Two numbers for the same page cost trust.

**Now:**
- The list shows each opening's **share of the 150 openings' views**: Benjamin Netanyahu 5.2%, Israel 3.4%, Palestine 1.8%, Israeli–Palestinian conflict 0.8%, Gaza Strip 0.6%, Israel Defense Forces 0.6%, Gaza–Israel conflict 0.1%. It is the same monthly source as the 12.4% (the rounded shares add to 12.5%; the 12.4% is the exact total, rounded once). The tooltips say "5.2% of the 150 openings’ views, Nov 2025 – Oct 2026". The bar and its tooltips print **no absolute views**; absolutes appear only in the reach section (daily sums).
- Caption: "The 150 most-read opening sections that existed in 2021. Shares of their views, Nov 2025 – Oct 2026 (monthly sums from our crawl). Tap a name for its sentence."
- The then-labels are shorter, so they fit one line in both languages: "Jan 2021: no opening charged Israel with genocide" (Jul 2023 likewise). The label line is also kept to one line, so the bar no longer moves when the reader switches between Jan 2021, Jul 2023 and Now (the Hebrew Jul 2023 label used to wrap and push the bar down about 20 px).
- Build: the seven shares are asserted from `data/mass2.json` (`5.2, 3.4, 1.8, 0.8, 0.6, 0.6, 0.1`). No share sits on a rounding edge, so JS `toFixed` and Python agree. The bar code holds no "million" and no `TM_T.views(`. Smoke: the list equals the shares computed from `R.tm`; the figure has no absolute views; the label line has one height and the bar one position in all three states.

| # | String | Status | Reason |
|---|---|---|---|
| 22 | List value «5.2%» (the percent alone; the caption names what it is a share of) | A | The draft «5.2% מהצפיות» wrapped a name onto two lines in English; both languages use the bare percent under the caption. |
| 23 | Tooltip «5.2% מהצפיות בכל 150 הפתיחים, נובמבר 2025 – אוקטובר 2026» | K | The same phrase as the headline («מהצפיות בכל ה־150»), with its referent spelled out. |
| 24 | Caption «150 פתיחי הערכים הנקראים ביותר שהיו קיימים ב־2021. חלקו של כל אחד מהצפיות בהם, נובמבר 2025 – אוקטובר 2026 (סכומים חודשיים מהסריקה שלנו). הקישו על שם כדי לראות את המשפט.» | K | "Shares of their views" = «חלקו של כל אחד מהצפיות בהם»: the share of each one in the views of the 150. It names the source and the period, as the English does. |
| 25 | Then-labels «ינואר 2021: אף פתיח לא האשים את ישראל ברצח עם» / «יולי 2023: …» | A | Was «אף אחד מ־150 הפתיחים…», which wrapped. «אף פתיח» keeps the same scope, because the headline and the caption say which 150. The verb and the object are unchanged. |
