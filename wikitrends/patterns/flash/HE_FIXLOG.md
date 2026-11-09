# Flash edition, Hebrew v2: fix log for the three proofs

**Sources**

- P1: `HE_PROOF_1.md`, the copy editor, 58 issues.
- P2: `HE_PROOF_2.md`, fidelity, 31 issues.
- BT: `HE_BACKTRANS.md`, the back-translation, 28 divergences.

**Files changed**

- `flash_i18n_he.json`
- `flash_he_overlay.html`
- `flash_he.py`

`page_flash_template.html` and `build_flash.py` are untouched. The English build is byte-identical (`cmp`).

**Status key**

- **A**: applied as proposed. A reviewer's "keep" or "none needed" that we followed also counts as A.
- **C**: changed differently. The reason is given.
- **R**: rejected. The reason is given.

## Totals

| Review | Items | A | C | R |
|---|---|---|---|---|
| P1 | 58 | 34 | 24 | 0 |
| P2 | 31 | 23 | 8 | 0 |
| BT | 28 | 16 | 8 | 4 |
| **All** | **117** | **73** | **40** | **4** |

## Conflict decisions (fidelity first, idiom second)

1. **Arabic الاستهداف ("targeting").**
   - P1 proposed התקיפה. P2 proposed keeping הפגיעה and fixing the preposition. The brief suggested וההכוונה נגד or התקיפה המכוונת של.
   - **Decision:** «ההרס של העם הפלסטיני ברצועת עזה **והפיכתו למטרה**, באופן שיטתי, מכוון ומתמשך, שישראל מבצעת…».
   - **Why not the others:**
     - "Targeting" means making someone a target, and «הפיכה למטרה» says exactly that. It does not assert that an attack took place.
     - התקיפה sharpens the word to "attack". התקיפה המכוונת also doubles המכוון, which the sentence already carries.
     - פגיעה softens it: it also means harm to rights, and it does not say "target".
     - הכוונה is ambiguous in unpointed Hebrew: it reads as "guidance" or as כוונה ("intention").
   - **Grammar:** each noun now takes its own preposition (הרס של… / הפיכתו), which fixes P2 #10. The three adjectives become the adverbial «באופן שיטתי, מכוון ומתמשך», so they govern both nouns, as they do in the Arabic.
2. **"Some have alleged".**
   - P2 said to keep «יש שטענו». BT said it softens, and proposed «יש שהאשימו».
   - **Decision:** «יש הטוענים», in the H2, in the translated quote and on the share card.
   - **Why:**
     - The present participle keeps the claim live and attributed.
     - האשימו means "blamed" (P2), which shifts the meaning.
     - The brief rules out the past form יש שטענו as softer.
3. **The "October 7 attacks" article name.**
   - P1 proposed מתקפות. P2 proposed using the name where the English names the article.
   - **Decision:** «מתקפת 7 באוקטובר» (singular, per the brief) everywhere the English names the article. That covers the hero row, both card 3 labels, the card 5 attributed label, the "moved the other way" item, the lane aria-label, the share card labels, the event label and the coding note.
   - Where the English says only "October 7", the date stands alone.
4. **ArbCom "heavily invested in influencing".**
   - P2 said the current wording was acceptable. BT flagged the money sense.
   - **Decision:** «לגורמים חיצוניים יש עניין רב בהשפעה על…», with "found" → «מצאו». This follows the brief.
   - "Invested in" is a stake, not spending. «בניסיון» is dropped with it.
5. **Spanish caption.**
   - P1 proposed «עימות מזוין… שחולל». P2 proposed «מתקפת תגמול… ושחולל».
   - **Decision:** «עימות מזוין … ושחולל רצח עם בעזה בידי ישראל».
   - **Why:**
     - The Spanish «y que» goes back to «conflicto».
     - The masculine verb then agrees with its real subject.
     - בידי replaces the calque מצד.
6. **The Hamas word "militant".**
   - P1 proposed ארגון ״חמוש״ in the hero row. P2 said the bare word is faithful. BT proposed a gloss.
   - **Decision:**
     - Keep ״חמוש״.
     - Add the gloss "(militant)" where it is first used: the hero row, the card 4 H2 and the card 4 body.
     - Use «כינתה» for "called".
     - The hero row stays bare, like the English row.
7. **The footer.**
   - P1 and P2 proposed different wordings.
   - **Decision:** «כל ציטוט מדויק, מתוארך ובשפת המקור; התרגומים לעברית הם שלנו». This is P2's wording, as the brief asked. It promises nothing about the play sheet or the grid tooltips.
8. **The edition name.**
   - BT #10 and #11 proposed מבזק or מהדורת הבזק.
   - **Decision:** rejected. P1 and P2 both keep «המהדורה המקוצרת», and the brief asks for it in the `<title>`.

## P1: copy editor (58)

| # | St | What we did |
|---|---|---|
| 1 | C | The titles-chart run-on is fixed.<br>• The cell is now two stacked lines in RTL: «‎+110 ימים» / «שינוי שם ‎+180 ימים».<br>• The `<br>` was hidden by the flash CSS. A one-line separator would overflow the 124 px nowrap column. |
| 2 | A | The NBSP is applied in `heD`/`heDs` and to every static Hebrew day-month in `flash_he.py` (`nb()`).<br>• The build asserts that none is left.<br>• The smoke test checks the visible text. |
| 3 | C | The source of each quote is named: «…; לפי הערך על הציונות, הציונות היא ״…״; ובכל עותק…».<br>• We kept «אומר» ("says") rather than «קובע», which would sharpen it.<br>• We kept «בכל עותק… אינם מזכירים» (literal).<br>• The English fix is in `EN_FOLLOWUPS.md`. |
| 4 | C | Court-case strings: «תביעה משפטית בלבד» / «מדווח היום כתביעה משפטית». This is P2's wording; P1's «רק התביעה» sits close to the vetoed «רק כתביעה». |
| 5 | C | `icj` is translated by meaning: «פסיקה מוגזמת» (short label), «הצגה מוגזמת של פסיקת בית הדין» (tooltip), «ICJ, כל ערך».<br>• «בית הדין בהאג» would drop "overstated".<br>• The XCOLW `icj` states are translated too. |
| 6 | A | n/a → «אין». |
| 7 | C | The Hebrew row shows «עברית / he»; the English row «English / אנגלית · היום = 1 באוק׳ 2026».<br>• The "en" code is dropped to fit the phone column. |
| 8 | A | English runs in share-card text are isolated with LRI/PDI, so (“genocide”) draws the right way round. Checked in the PNG. |
| 9 | C | See conflict 5. |
| 10 | C | «ושחולל רצח עם בעזה בידי ישראל». This keeps the Spanish structure and the brief's «בידי ישראל», rather than recasting it as «שישראל מבצעת». |
| 11 | C | «שינוי מאותו סוג הגיע גם לערכים על 1948». We kept "the same kind" (P1's «דומה» is weaker) and fixed the target. |
| 12 | C | «והשינוי הגיע גם לערך על מתקפת 7 באוקטובר», which also takes the article name. |
| 13 | A | «מאז ספטמבר 2025 ניסו עשר עריכות להחזיר ייחוס…». «נעלמה» is kept. |
| 14 | A | `font-style:normal` for all Hebrew. The bridges and the empty-lane notes are weight 500.<br>• The smoke test checks that no element outside the en/es blocks is italic. |
| 15 | A | «התזמון מלמד על מועד, לא על סיבה». The assertion is updated with the same strength. |
| 16 | A | «שקדמו לו». |
| 17 | A | «הם לא נקבו בשמו של צד או של מדינה כלשהם». The assertion is updated. |
| 18 | A | «בשם מי שגירש». |
| 19 | C | «…ממדינות ערב״ לא ננקב שום גורם».<br>• This is P2's verb, parallel to נקב and narrower than "not mentioned".<br>• The comma is dropped, as P1 asked. |
| 20 | A | «נוקב בשמות ״ההגנה, האצ״ל והלח״י, הארגונים הצבאיים־למחצה הציוניים״». |
| 21 | C | «ושמו של חמאס מופיע בהמשך המשפט הראשון». P1's «אבל רק» adds an "only" that the English lacks. |
| 22 | A | «באף אחת מ־107 הגרסאות שלה לא הוזכרו החטופים». |
| 23 | A | The lane now reads «ב־107 גרסאות». |
| 24 | A | «ב־2021 כינתה ויקיפדיה את חמאס…». The inversion and «כינתה» follow the brief. |
| 25 | C | The hero row has a gloss «״חמוש״ (militant)» but no ארגון, because the English row is bare (P2). |
| 26 | C | «המילה militant (״חמוש״) יצאה». We kept "left" (יצאה), not "removed" (הוסרה). |
| 27 | A | «בסדר הפוך». |
| 28 | C | «ההכרזה על חמאס כארגון טרור עברה…». The antecedent is fixed; we kept «עברה» ("moved"), since «ירדה» adds a direction. |
| 29 | A | The stray "·" is removed. |
| 30 | A | «המדינה האסלאמית (דאעש)». The asserted line is updated; its strength is unchanged. |
| 31 | A | «אז (העותק הראשון שלנו) והיום». |
| 32 | C | The grid caption and title now read «באיזה קול מציגה כל מהדורת שפה חמש טענות…».<br>• The number is spelled out (P1).<br>• "voices" keeps its analytic sense (P2 #27, BT #15). |
| 33 | C | The prose drops "+N": «…187 ימים אחרי פתיחת הערך באנגלית; ויקיפדיה בפולנית, ב־26 באפריל 2026, 849 ימים אחרי אותה פתיחה».<br>• The reference point is named, because both counts run from the English opening. |
| 34 | A | «הראשונה» / «שינוי שם». |
| 35 | A | «יוצאת הדופן» in the label and the aria-label. |
| 36 | A | «אינו קובע שמתבצע רצח עם». |
| 37 | A | «״…שמבוצע בידי ישראל״» in the hero row and the diff. The gender now agrees with הרס. |
| 38 | A | The full stop goes outside the fragment. |
| 39 | A | «כ…». |
| 40 | A | «כמה זמן שורדת מילה». |
| 41 | A | «היסטוריית הגרסאות של ארבעה משפטים ראשונים…». |
| 42 | C | «בכל 254 ערכי הנושא שהם ערכי ליבה או שדורגו בחשיבות עליונה או גבוהה». This is the same scope without the comma-apposition, which would be ambiguous. |
| 43 | C | «התקבל 15 מול 0».<br>• «ברוב של» is dropped.<br>• «פה אחד» is not used: 15–0 says nothing about abstentions. |
| 44 | C | «…לתחום הנושא PIA״ (הסכסוך הישראלי־פלסטיני)».<br>• P2's term goes inside the quote.<br>• The gloss stays outside the quote. |
| 45 | C | «הצביעו באותו אופן … לעומת כמחצית בהצבעה מקרית». This is a simpler fix of the same calque. |
| 46 | A | «בהצבעה מקרית: כמחצית». The bar label is updated too. |
| 47 | C | «הצבעה לפי מחנות», as the brief and P2 #8 asked. The assertion is updated. |
| 48 | A | «שלפתיח שלהם נוספו מונחים ביקורתיים». |
| 49 | A | The `<title>` reads «המהדורה המקוצרת: …». |
| 50 | C | P2's footer wording; see conflict 7. |
| 51 | A | «כל הציטוטים, מתוארכים ←». |
| 52 | C | See conflict 1. |
| 53 | A | «פשעי רצח עם». |
| 54 | A | «הרס החברה הפלסטינית» in the hero row, the H2, the lane and the full sentence. |
| 55 | A | «מסומנת בקו מחיקה». |
| 56 | A | «הקישו על קו». |
| 57 | A | «▶ הפעלה חוזרת» on all four buttons. The smoke regex is updated. |
| 58 | C | The article name is singular; see conflict 3. |

**P1 verdicts on the unsure renderings**

- **Followed:** U1, U2, U3, U5, U7, U8, U9, U10, U11, U13, U14.
- **U4:** kept ״חמוש״ and added the gloss.
- **U6:** decided by conflict 1.
- **U12:** we added «ארץ שהיא עצמה» and the maqaf in «לאומית־אתנית». We kept «ביהדות» for fidelity.

**Global house-style decisions**

- **Adopted:** G1, G2, G3 (headline numbers), G4, G5, G6, G7, G8 and G9.
- **G5:** the article name is singular (see conflict 3).
- **G10:** every locked line we touched has its assertion updated with the same claim.

## P2: fidelity (31)

| # | St | What we did |
|---|---|---|
| 1 | A | «ואינו שופט». `HE_SCOPE` is updated. «אינו מעריך» is now vetoed. |
| 2 | A | השמדה → «ההרס המתמשך, המכוון והשיטתי… שמבוצע».<br>• The gender is fixed in the hero row and the diff.<br>• «השמדה» is vetoed page-wide. |
| 3 | A | «שרצח עם בעזה ״מבוצע בידי ישראל״». |
| 4 | A | Both translations on the Israel and Netanyahu slide carry «תרגום שלנו». So does the denial line.<br>• Asserted. |
| 5 | A | The share image foot now opens with «בערך על ישראל, המשפט הבא: ״…״». Checked in the PNG. |
| 6 | A | The footer reads «התרגומים לעברית הם שלנו». |
| 7 | A | «להנחיות הסגנון». The assertion is updated. |
| 8 | A | «הצבעה לפי מחנות». |
| 9 | C | «ארץ ישראל ביהדות, ארץ שהיא עצמה מרכזית…». The antecedent is fixed; we kept «ביהדות», since «שבמסורת היהודית» adds "tradition". |
| 10 | C | See conflict 1. The preposition fix is applied. |
| 11 | C | «השתנה, בלי שינוי בקול» (the brief's wording) in every tooltip and aria-label. The key reads «שינוי שאינו שינוי קול». |
| 12 | A | «התקפות [atentados] מתואמות». |
| 13 | A | Kept (no change requested). |
| 14 | C | See conflict 5. |
| 15 | A | «ובמתקפת קומנדו». |
| 16 | C | See conflict 4. |
| 17 | A | «לתחום הנושא PIA», plus a gloss outside the quote. |
| 18 | A | «באיזה צד צידדה», «אף אחד משני הממצאים». |
| 19 | A | «ולא אם מה שכתוב בו נכון». |
| 20 | A | «לא ננקב שום גורם». |
| 21 | A | Kept «עקירתם». |
| 22 | C | «יש הטוענים» (the brief); see conflict 2. |
| 23 | A | «עובדה מבוססת». |
| 24 | A | «ומעשי טבח». |
| 25 | A | hos F → «מכונים בני ערובה». |
| 26 | A | Translated: «תביעה משפטית בלבד» / «מדווח היום כתביעה משפטית». |
| 27 | C | «באיזה קול מציגה…». The number is spelled out (P1). |
| 28 | A | «חמאס: טרוריסטי» in both headers. |
| 29 | C | The article name is singular; see conflict 3. |
| 30 | A | The `<title>` is fixed. |
| 31 | A | Kept. |

**P2 verdicts on the unsure renderings:** all followed except #6 (פגיעה), which was decided by conflict 1, and #14 ("Some have alleged"), which was decided by conflict 2.

## BT: back-translation (28)

| # | St | What we did |
|---|---|---|
| 1 | A | הרס. |
| 2 | A | «יש עניין רב בהשפעה», «מצאו». |
| 3 | A | The lead-in is restored on the share card. |
| 4 | A | «השתנה, בלי שינוי בקול». |
| 5 | A | Gloss «(militant)», «כינתה». |
| 6 | A | The Arabic and Spanish slides show both translations, «תרגום שלנו · אז» and «· היום». They are no longer hidden by state: the inactive one is only dimmed. The "now" Arabic includes «שישראל מבצעת».<br>• Asserted in the build and the smoke test. |
| 7 | C | «יש הטוענים», not «יש שהאשימו»; see conflict 2. |
| 8 | A | «נהרגו כתוצאה מהמתקפות». The quote names no agent, so it does not say Hamas. The assertion is updated. |
| 9 | C | The article name is singular. |
| 10 | R | Keep «המהדורה המקוצרת» (P1, P2, the brief). |
| 11 | R | The same reason as #10. |
| 12 | C | «ולא אם מה שכתוב בו נכון» (P2's option). |
| 13 | R | P1 and P2 keep «ראשוני». גישושי is rare on a chip. |
| 14 | A | «להנחיות הסגנון». |
| 15 | C | «באיזה קול מציגה…». |
| 16 | A | «צידדה». |
| 17 | R | «עקירה» is the standard term (P2 #21); הגליה would change the meaning. |
| 18 | C | Conflict 5. |
| 19 | C | We kept the Arabic second noun, as «הפיכתו למטרה»; we did not drop it to match the English. The translation is of the Arabic. |
| 20 | A | The coding note is translated. |
| 21 | C | The label now says «התרגום שלנו (באנגלית בלבד):».<br>• The term glosses (12 strings) are now Hebrew.<br>• Hebrew terms get no gloss.<br>• Hebrew translations of the roughly 100 grid sentences remain out of v1 scope, and the label says so. |
| 22 | A | «הוסר» / «נוסף», set as Hebrew inside the English tooltip line. |
| 23 | A | The sheet note now says plainly that the tool is shown in English only, with no Hebrew translation. The footer promises nothing more. |
| 24 | C | The footer is reworded (conflict 7). |
| 25 | A | Indefinite. |
| 26 | A | «איך זה הגיע לשם». |
| 27 | A | None needed. |
| 28 | A | None needed. |

## Beyond the three reviews (found while checking)

- **English strings left in the grid tooltips:**
  - the term glosses («…» = “genocide”);
  - the `#xmNote` coding note;
  - the XCOLW `icj` states;
  - "Enter" in the aria-label (now «לחיצה על אנטר»).
- **Coding notes:** three notes now put the English title in quote marks («הערך האנגלי “Gaza genocide”»).
- **The c4vs share card:** the foot ran off the bottom. The foot is now measured before the rule is drawn.
- **Canvas wrap:** it no longer splits at a no-break space.
- **New build checks in `flash_he.py`:**
  - vetoes on the v1 renderings (השמדה, אינו מעריך, יש שטענו, מצד ישראל, משקיעים רבות, הצבעה במחנות, לכלל הסגנון, אך לא בקול, פיגועים, עובדה מוכחת, והפגיעה, מתקפות 7 באוקטובר);
  - no English UI leftovers in the string map;
  - no day-month without an NBSP;
  - the labels on the Israel and Netanyahu translations;
  - both sides of the morph slides translated.
- **New smoke checks:**
  - visible English outside the original-language blocks, page-wide and in all 55 grid tooltips;
  - synthetic italic;
  - both morph translations shown;
  - NBSP in the visible text.
