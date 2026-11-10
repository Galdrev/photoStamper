# Flash edition: Hebrew fix log 3 (owner requests: "armed incursions", the hostages moment)

**Build:** `cd wikitrends && python build_flash.py --bilingual OUT.html`. The single-language builds (`build_flash.py OUT.html`, `build_flash.py --lang he OUT.html`) still run every check. The research edition is byte-identical (`build_page.py` output compared with `cmp` before and after each step).

**Standards:** `HE_PROOF_1.md` (idiom, grammar, RTL, punctuation, no italic, no-break space in dates, no English in the UI) and `HE_PROOF_2.md` (fidelity of agency, modality and attribution; no sharpening or softening).

## 1. "armed incursions": «פשיטות חמושות» replaces «חדירות חמושות»

**Decision: «פשיטות חמושות».** The owner's recommendation holds; I found no fidelity reason against it, and two reasons for it.

| Candidate | Sense in Hebrew | Verdict |
|---|---|---|
| «חדירות» (v1–v3) | penetration, crossing in; in news Hebrew also "infiltration" (חדירת מחבלים) | **Out.** It keeps the crossing but loses the hostile, armed, sudden attack that "incursion" names. It reads as a technical or clandestine entry. |
| **«פשיטות»** | raid: a sudden, limited armed entry into another's territory, then out | **Chosen.** It is the dictionary sense of "incursion" ("a hostile entrance into a territory: raid", Merriam-Webster; "an invasion or attack, especially a sudden or brief one", Oxford), and it does not claim more than the English. |
| «פלישות» | invasion | **Out, for fidelity.** It sharpens the English. English Wikipedia itself *removed* "invasion" from this first sentence: the January 2024 copy said "the first invasion of Israel since the 1948 Arab–Israeli War"; the current one does not. Rendering "incursions" as «פלישות» would put back, in our translation, the word the encyclopedia took out. |

**Consequences, all applied:**
- One rendering for "incursion" on the whole page. The event label "Israeli Jenin incursion (July 2023)" changes from «החדירה הישראלית לג׳נין» to «הפשיטה הישראלית על ג׳נין».
- Known collision: "raid" (Israeli raid on Al-Shifa Hospital) is also «פשיטה». This is acceptable: in every place the October 7 phrase is shown, the English original stands beside our translation, and the two events are never on the same line.
- `HE_PROOF_2.md` (row "October 7", glossary row "incursion(s)") chose «חדירה» and reserved «פשיטה» for Al-Shifa. That verdict is superseded by this decision. `HE_PROOF_2.md` issue 15 (Spanish "un ataque de comandos" = «מתקפת קומנדו», not «פשיטת קומנדו») stays right on its own ground: "ataque" is מתקפה.
- The original English stays visible everywhere, exactly as before (`.he-o` under the H2, the LTR pair in the what-changed line and the hero row, `(armed incursions)` in the lane label, `<bdi lang="en">` in the reach key).

**Every place changed (`flash_i18n_he.json`):**

| Place | Before | After |
|---|---|---|
| Card 3 H2 | «…כתוב היום ״חדירות חמושות מתואמות״…» | «…כתוב היום ״פשיטות חמושות מתואמות״…» |
| Card 3 what-changed pair | «״…מתקפות מתואמות״ ← ״…חדירות חמושות מתואמות״» | «״…מתקפות מתואמות״ ← ״…פשיטות חמושות מתואמות״» |
| Hero stack, October 7 row | «״מתקפות מתואמות״ ← ״חדירות חמושות מתואמות״» | «״מתקפות מתואמות״ ← ״פשיטות חמושות מתואמות״» |
| October 7 lanes (label, aria) | «״חדירות חמושות״ (armed incursions)»; «…חדירות חמושות, הימים…» | «״פשיטות חמושות״ (armed incursions)»; «…פשיטות חמושות, הימים…» |
| Reach key (critical wording) | «“armed incursions” (חדירות חמושות)» | «“armed incursions” (פשיטות חמושות)» |
| Scrolly event labels (library) | «7 באוק׳: ״מתקפות״ ← ״חדירות״»; «7 באוק׳: ״חדירות חמושות״» | «… ״מתקפות״ ← ״פשיטות״»; «… ״פשיטות חמושות״» |
| Language-grid coding note (en, October 7) | «״סדרה של חדירות חמושות מתואמות״» | «״סדרה של פשיטות חמושות מתואמות״» |
| Event label, Jenin | «החדירה הישראלית לג׳נין (יולי 2023)» | «הפשיטה הישראלית על ג׳נין (יולי 2023)» |

**Share images and lab chrome:** the share images read their text from the page (`shSpec`), so they change with it. The Data lab's Hebrew chrome (`lab/lab_flash.py`) never carried the phrase; it is checked against the new vetoes all the same.

**Locks (`flash_he.py`):**
- `HE_VETO` gains «חדירות», «החדירה הישראלית» and «פלישות חמושות». The vetoes run over the visible Hebrew page, the library and figure strings, the overlay script, the event labels, the grid notes and the lab chrome.
- New assertions: the H2, the pair, the hero row, the reach key, the lane label, the event label and the grid note each carry «פשיטות».

## 2. The hostages moment (card 3, `#c3m`), both languages

**What it is.** A full-bleed black block inside card 3, after the what-changed pair. It replaces the card's October 7 strip and its hostages caption (`figure.fl-lane`, `#stO7`), which it supersedes; the strip's three lanes are one tap away ("Play the October 7 sentence" opens the full October 7 instrument). This was the trim inside card 3 that keeps the length; no fact outside card 3 was cut.
- **251**, huge (78 px on phones, up to 176 px on desktop), beside its source: "English · only here: sentence 9 of the opening section" and the sentence, “251 Israeli and non-Israeli civilians and soldiers were taken as hostages to the Gaza Strip” (Hebrew page: with our translation under it).
- **Ten editions in native names** (עברית, العربية, English, Deutsch, Français, Español, Italiano, Português, Nederlands, Русский; the language-grid order; Polish has no article on the attack). Each shows its first sentence's hostage slot: an **empty dashed hole** for nine; **filled, with "rapimento"**, for Italian.
- **Pacing:** the 251 first (fade 1.4 s), its sentence at 0.8 s, then one edition every 0.45 s from 1.8 s, the scope line at 6.6 s; all shown by about 8.6 s. A tap on any edition ends the pacing at once. **Reduced motion:** the final state, no transitions. Print: dark on paper.
- **Tap an edition:** its first sentence in the original (curly quotes, its own direction), the empty slot after it (Italian: the words marked), our translation (English page: the stored English rendering; Hebrew page: our Hebrew), and "Further on": where that opening section does mention them. Esc or a second tap closes it.
- **Scope line:** "**9 of 10.** In our latest copies (Oct–Nov 2026), the October 7 article’s first sentence names no hostages in 9 of the 10 Wikipedias with an article on it, though all ten opening sections mention them. Italian’s does; Hebrew’s did, in our copies from October 2024 to October 2025."
- **Contrast line:** "English · only here: sentence 9 of the opening section" (under the 251), and the English panel's "only in sentence 9" plus the Israel and Hamas line.
- **Share image** (button in the block's top row): `wikipedia-hostages-first-sentence.png` / `-he.png`, 1080×1350, black, the 251, sentence 9 (and our translation), the ten slots, the scope line, the report's scope line, the date ("Wikipedia text as of 5 November 2026") and the source URL. Card 3's own share image keeps its hostages rows, now from the moment.
- **Palette:** no new hue. The block uses the page's own dark-scheme neutrals (#0b0e10 ground, ink #e7ebec, muted #8f9aa2, rule #2a3237) in both schemes; in the dark scheme it gets a 1 px rule so it does not melt into the page. No red, no imagery.

**spin_review.md:** the block states wording facts only, each with its scope: no "erased", "missing in all languages", "the world", or any verdict. The exceptions (Italian now; Hebrew 2024–25; the Hamas 2024 copies) are on the page, not hidden. The scope line of the report stays at the top and is on the share image.

**A correction the fact check forced (see `FACTCHECK_hostages.md` (c)).** Our quarterly English Hamas copies of April and July 2024 said "…and taking hostages back to Gaza". So:
- the old caption "Israel and Hamas opening sections: none, in every copy we hold since 2021" is gone;
- "In short" now reads "…and, in our latest copies, the Israel and Hamas opening sections do not mention the hostages" (Hebrew: «ובעותקים האחרונים שבידינו, פתיחי הערכים על ישראל ועל חמאס אינם מזכירים את החטופים»);
- the English panel says: "Israel’s opening section: none, in every copy we hold since 2021. Hamas’s: none now; our April and July 2024 copies said “taking hostages back to Gaza”."

**Length (phone 390×844, fonts loaded, every lazy piece drawn; our measuring script):** English 10.83, Hebrew 10.99 (both ≤ 11.0). Before: 10.81 / 10.97. The smoke suite's own figures are in §4.

## 3. Hebrew proof of every new or changed string (HE_PROOF_1 / HE_PROOF_2 standard)

Read on the rendered page (iPhone 13, light and dark), every panel open in turn, and in the string map (`flash_i18n_he.json`, the overlay's share-image strings). Quotes in “…” are originals and were not touched. **A** = changed during the proof; **K** = kept.

| # | String | Decision | Status | Reason |
|---|---|---|---|---|
| 1 | Kicker «החטופים · המשפט הראשון, בעשר ויקיפדיות · הקישו על שפה» | keep | K | Plural imperative הקישו, as elsewhere on the page. "Wikipedias" = ויקיפדיות, the page's plural. |
| 2 | Save aria «שמירת רגע החטופים כתמונה» | «שמירת כרטיס החטופים כתמונה» | A | «רגע» (moment) is a design word and reads oddly; «כרטיס» matches «שמירת הכרטיס כתמונה». |
| 3 | «אנגלית · רק כאן: משפט 9 בפתיח הערך» | keep | K | "opening section" = פתיח הערך (binding glossary). «רק כאן» = "only here", no sharpening. |
| 4 | Tile labels «…: אין חטופים במשפט הראשון; להצגתו» / Italian «…: המשפט הראשון מזכיר אותם; להצגתו» | keep | K | "hostages" in our prose = החטופים (glossary). |
| 5 | Scope line, «המשפט הראשון על 7 באוקטובר» | «המשפט הראשון **בערך** על 7 באוקטובר» | A | Without «בערך» it reads "the first sentence about 7 October" in general; the scope is the article's first sentence (F3 (i)). |
| 6 | Scope line, rest: «…אינו מזכיר חטופים ב־9 מתוך 10 הוויקיפדיות שיש בהן ערך עליו, אף שכל עשרת פתיחי הערכים מזכירים אותם. באיטלקית הוא מזכיר אותם; בעברית הזכיר, בעותקים מאוקטובר 2024 עד אוקטובר 2025.» | keep | K | "names no hostages" = «אינו מזכיר חטופים» (not «מעלים», which would add intent). «אף ש» keeps the English "though". The Hebrew 2024–25 exception keeps its scope ("our copies", quarterly). |
| 7 | Panel heads «Deutsch · ויקיפדיה בגרמנית · המשפט הראשון · אוקטובר 2026» etc. | keep | K | Native name first (lang-marked), as on the tiles. NBSP in «2 בנובמבר 2026» (build). |
| 8 | Empty-slot aria «אין חטופים במשפט הזה» | keep | K | |
| 9 | en first sentence: «ב־7 באוקטובר 2023 בוצעה סדרה של פשיטות חמושות מתואמות מרצועת עזה הנתונה במצור אל עוטף עזה שבדרום ישראל, בידי חמאס וכמה קבוצות חמושות פלסטיניות אחרות.» | keep | K | Passive kept ("were carried out by" = «בוצעה … בידי»); "blockaded" = «הנתונה במצור»; "militant groups" = «קבוצות חמושות» (glossary); incursions = «פשיטות» (§1). |
| 10 | de: «(ובפשטות גם 7 באוקטובר)» | «(ובקיצור גם 7 באוקטובר)» | A | "vereinfacht" = shortened form of the name; «בפשטות» reads as "simply put". |
| 11 | de: «עם 1195 הרוגים, רובם המכריע יהודים» (draft) | «עם 1195 הרוגים, רובם יהודים» | A | "überwiegend" = predominantly; «רובם המכריע» (the overwhelming majority) sharpens. Fixed before the first build. |
| 12 | fr: «…סדרה של מתקפות טרור [attentats] פלסטיניות…» | keep | K | «פיגועים» is the idiom for "attentats", but it is a vetoed v1 rendering; «מתקפות טרור» is the page's rendering of the same French phrase in the grid note, and the original noun is kept in brackets (as the Portuguese grid note does). |
| 13 | es: «המתקפות של 7 באוקטובר נגד ישראל, כפי שהן מוכרות בעולם…» | keep | K | Avoids the vetoed «מתקפות 7 באוקטובר». Both "denominados" clauses kept. |
| 14 | it: «…שהביאו להריגתם של לפחות 1200 … ולחטיפתם של כ־250 מהם; היא אירעה…» | keep (draft «ובעקבותיהן הריגתם…» replaced before the first build) | A | "con conseguente" = resulting in: «שהביאו ל». The kidnapping is marked in both the original and the translation. The semicolon keeps one sentence. |
| 15 | pt: «…סדרה של התקפות [atentados] מתואמות שביצעה הקבוצה החמושה האסלאמית הפלסטינית חמאס…» | keep (draft «הארגון החמוש» → «הקבוצה החמושה» before the first build) | A | "grupo" = קבוצה; «ארגון» is a different word. «התקפות [atentados]» as in the grid note. |
| 16 | nl, ru first sentences | keep | K | ru "Вторжение" = «הפלישה» (as in the grid note); "проникли" = «חדרו» (a verb; not the vetoed noun «חדירות»). |
| 17 | ar clause: «…כולם מתייחסים למבצע הצבאי הממושך שפתחו בו פלגי ההתנגדות הפלסטיניים ברצועת עזה, בהובלת תנועת חמאס, נגד הכיבוש הישראלי…» | keep | K | The grid note's renderings («מבצע צבאי ממושך», «פלגי ההתנגדות הפלסטיניים», «נגד הכיבוש הישראלי»). Ellipses mark the clause. |
| 18 | ar note «ההמשך מביא את שמות המבצע…» | «**שאר המשפט** מביא…» | A | The names come *before* the clause; "the rest of the sentence", not "the continuation". |
| 19 | ar further-on gloss «״שבו״, לא המילה בני ערובה» | «״שבו״ (לקחו בשבי), לא המילה ״בני ערובה״» | A | «שבו» alone can read as "in which"; the gloss removes the ambiguity. |
| 20 | en further-on «(ולקח בני ערובה בחזרה לעזה)» | «(ולקיחת בני ערובה בחזרה לעזה)» | A | "taking" is a gerund with no subject in the fragment; «ולקח» supplied one. Inside a translated quote, "hostages" = בני ערובה (glossary). |
| 21 | nl/ru further-on translations «…נלקחו בשבי והועברו לעזה כבני ערובה», «ועוד 251 נלקחו כבני ערובה» | keep | K | Literal; numbers as in the originals. |
| 22 | de/fr/es/pt further-on «בהמשך, מעבר ל־1,200 התווים שבידינו: לראשונה במשפט 9 מתוך 19 (לפי הספירה שלנו, 8 בנובמבר 2026).» | keep | K | Says it is our count and its date; no quote of text we do not hold. |
| 23 | he further-on «…בעותקים שלנו מאוקטובר 2024 עד אוקטובר 2025 המשפט הראשון הזה כלל את המילים “חטיפת אזרחים”.» | keep | K | The exception, stated in the Hebrew edition's own words. |
| 24 | "In short" «ובעותקים האחרונים שבידינו, פתיחי הערכים על ישראל ועל חמאס אינם מזכירים את החטופים.» | keep | K | The corrected scope (see §2). |
| 25 | Share images: kicker «ויקיפדיה · המשפט הראשון של הערך על 7 באוקטובר · החטופים · התרגום לעברית: שלנו»; card 3 rows «החטופים · המשפט הראשון, בעשר ויקיפדיות», «מתקפת 7 באוקטובר · משפט 9» | keep | K | Drawn right to left; the English sentence 9 left to right with our translation under it. |

**RTL and type:** the English quote under the 251 and every Latin or Cyrillic original sit in `dir="ltr"` spans; Arabic and Hebrew originals in `dir="rtl"`; the mono kicker and labels drop the uppercase and tracking in Hebrew (Heebo); no italic; translation labels «תרגום שלנו» on every non-Hebrew sentence (nine). The build checks: no English outside lang-marked originals (it now exempts de, fr, it, pt, nl, ru originals as well as en, es, ar), nine translations, nine empty slots, the must-keep lines, and the vetoes.

**Totals:** 25 rows; 9 changed (A, 4 of them drafts fixed before the first build), 16 kept.

## 4. Smoke tests (final build)

**Build:** `scratchpad/flash/hostages/index.html` (begins with `<!DOCTYPE html>`, the charset meta and the viewport meta). Rebuilt from this commit and compared with `cmp`: identical. Research edition: `build_page.py` output byte-identical to the pre-change build.

**Suites** (`scratchpad/flash/hostages/smoke_core.js`, `smoke_bi.js`, `smoke_lab.js`; the extended copies also replace those in `flash/final/` and `flash/merge/`). New checks for the moment, in every configuration (iPhone 13 and 1280, light and dark, plus reduced motion, both languages):
- ten editions in order, nine empty slots, only Italian filled; the 251 at ≥ 70 px on the black ground; the scope line ("9 of 10", Hebrew's 2024–25 copies);
- at rest every slot shown; no overflow inside the block or the page;
- pacing (replayed from the start): the 251 first with the slots hidden at 1.3 s, slots filling one by one at 2.6 s and 4.2 s, all ten by 9.3 s; the pacing starts only when the block is in view; reduced motion: static, no transitions;
- each of the ten taps opens that language's panel only, inside the screen; nine panels show the empty slot, Italian marks “rapimento di circa 250 di questi”; our translation where needed; Esc and a second tap close it;
- an **in-page recount**: of the ten sentences shown, only the Italian one matches the hostage words;
- Hebrew: no English outside the originals, in the block and in every open panel;
- the share image downloads `wikipedia-hostages-first-sentence(-he).png` (core and bilingual suites, in the active language);
- vetoes extended: «חדירות», and the old "in every copy we hold, the Israel and Hamas …" wording.

**Results:**

| Suite | Pass | Fail |
|---|---|---|
| core (5 configurations × 2 languages) | 1193 | 0 |
| bilingual | 308 | 0 |
| Data lab | 185 | 0 |

0 console errors or warnings and 0 horizontal overflow in every configuration.

**Phone screens (smoke):** English 10.85 (reduced motion 10.83), Hebrew 10.99 (10.98); both ≤ 11.0. At 1280: English 10.52, Hebrew 11.30 (no target at 1280; before 10.40 / 11.18).

**Screenshots:** `scratchpad/flash/hostages/moment_{en,he}_light.png` (the moment at rest, phone), `moment_{en,he}_tap_{he,it,en}.png` (panels), and the share images `wikipedia-hostages-first-sentence.png`, `wikipedia-hostages-first-sentence-he.png`.
