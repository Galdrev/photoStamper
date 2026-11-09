# Flash edition, final round: Hebrew proof of the new strings (fix log 2)

**Scope:** every new Hebrew string listed in `MERGE.md` ("New Hebrew strings for proofreading"), plus the strings added in the final round:
- step 1, the reach bars for Benjamin Netanyahu and Palestine;
- step 2, the Data lab tab (`lab/lab_flash.py`);
- step 3, the length cut.

**Standards:**
- `HE_PROOF_1.md`: idiom, grammar, RTL, punctuation, no italic, NBSP in dates, no English in the UI.
- `HE_PROOF_2.md`: fidelity of agency, modality and attribution; no sharpening or softening.

**How it was read:**
- the rendered bilingual page (`scratchpad/flash/final/w4.html`) as an iPhone 13, with every `<details>` open, the fight lanes, the treemap tooltips, the Spanish and Israel/Netanyahu slides and the Data lab (flipbook and prism);
- the string maps (`flash_i18n_he.json`, `flash_he_overlay.html`, `lab/lab_flash.py`) against the English page and the stored English sentences (`patterns/angle/perp_codes.jsonl`).

**Status key:**
- **A**: changed.
- **K**: kept as is (checked, no change needed).
- **C**: a layout or build change, not a wording change.

**Totals:** 40 rows, covering about 70 strings. 20 changed (A), 3 layout or build fixes (C), and the rest kept (K). New entries in `HE_VETO` lock the changed forms.

## 1. The three items flagged in MERGE.md

| # | String | Decision | Status | Reason |
|---|---|---|---|---|
| 1 | "met" → «הציגו» (reach heading, lead, key, surge) | «בכמה מהצפיות **הוצג** הנוסח החדש»; «הצפיות **שבהן הוצג** הנוסח הביקורתי»; «**ב־92.6%** מהצפיות בערך על ישראל **הוצג** …»; «**ברוב** הצפיות הוצג הנוסח הישן»; «**ובאף אחת** מהן לא הוצג …»; «כמעט **בכל** צפייה הוצג הנוסח החדש» | A | <ul><li>«הצפיות הציגו» makes the page view the agent that displays the text. That is a calque and reads oddly.</li><li>«נתקלו ב־» (the alternative) implies a reader who stumbled on the text by chance, which is stronger than "met".</li><li>The passive «הוצג ב־» says exactly what was measured: the wording was on the page when it was viewed. No agent is added.</li><li>The old forms are vetoed.</li></ul> |
| 2 | The five new treemap charge sentences (`HE_TM`) | See §2. Three corrected, two kept | A/K | Checked word by word against the stored English sentences |
| 3 | The fight-lane phrase translations (`FB_HE`, 8 phrases) | All 8 kept: קולוניזציה · ארץ מחוץ לאירופה · פלסטין, אזור · ארץ ישראל · ההיסטוריה היהודית · מולדת · העם היהודי · מדינה יהודית | K | <ul><li>Each is the plain dictionary rendering.</li><li>"Jewish state" stays indefinite, as in the English ("a Jewish state").</li><li>"land outside (of) Europe" → «ארץ מחוץ לאירופה» covers both variants, so the "(of)" needs no Hebrew.</li></ul> |
| 3a | The same lanes, RTL (a rendering bug) | Each Hebrew translation was **cut off at the right edge** on phones: the SVG `<text>` had `direction="rtl"` with `text-anchor="end"`, which anchors the left end of an RTL run, so the run ran past the frame. It is now `text-anchor="start"`, so the text ends at the right margin. | C | Seen in the rendered page (`fb_he.png`, before and after) |

## 2. The treemap charge sentences (`HE_TM`)

| Article | English (stored) | Before | Now | Status | Reason |
|---|---|---|---|---|---|
| Israel | "After the Hamas-led October 7 attacks, Israel began committing genocide against Palestinians in Gaza." | «אחרי המתקפות בהובלת חמאס ב־7 באוקטובר, ישראל החלה לבצע רצח עם נגד פלסטינים בעזה.» | unchanged | K | Exact. The plural "attacks" is kept without the vetoed «מתקפות 7 באוקטובר» |
| Palestine | "…the October 7 attacks by Hamas in Israel in 2023 **which killed** 1195 people, Israel launched a large-scale military operation in Gaza **that has killed** over 72,000 Palestinians, **caused** mass population displacement…; these acts have been recognised as constituting genocide…" | «…שבהן **נהרגו** 1195 בני אדם, … במבצע … שבו **נהרגו** יותר מ־72,000 פלסטינים, **ושגרם** …» | «…**שהרגו** 1195 בני אדם, פתחה ישראל במבצע צבאי רחב היקף בעזה, **שהרג** יותר מ־72,000 פלסטינים **וגרם** לעקירה המונית…» | A | <ul><li>Agency. In the English, the attacks killed and the operation killed. The passive «נהרגו» removed the agent from both clauses, in the same way.</li><li>The active verbs restore the agency on both sides, symmetrically.</li><li>"1195" stays without a comma, as in the original.</li></ul> |
| Gaza Strip | "…described by scholars, international law experts, and human-rights organizations **as constituting** a genocide against the Palestinian people." | «…כרצח עם נגד העם הפלסטיני.» | «…**כמהוות** רצח עם נגד העם הפלסטיני.» | A | Precision (sev 1). "as constituting" is a legal characterisation; «כמהוות» keeps it |
| Israeli–Palestinian conflict | "…described by international law experts, genocide scholars and human rights organizations as a genocide." | «…תוארו בידי מומחים למשפט בין־לאומי, חוקרי רצח עם וארגוני זכויות אדם כרצח עם.» | unchanged | K | Exact; the attribution ("described by") is kept |
| Israel Defense Forces | "…unlawful killings and **systematic abuses** of Palestinian rights, with **multiple** human rights organizations and scholars accusing the IDF of genocide." | «…ובפגיעה שיטתית בזכויות הפלסטינים, וארגוני זכויות אדם וחוקרים **רבים** מאשימים…» | «…ובהפרות שיטתיות של זכויות הפלסטינים, ו**מספר** ארגוני זכויות אדם וחוקרים מאשימים את צה״ל ברצח עם.» | A | <ul><li>"abuses of rights" is «הפרות זכויות» in Israeli legal and press usage. «פגיעה» is vaguer (MERGE "unsure" item, resolved).</li><li>"multiple" means several, not many; «רבים» sharpened it (sev 2).</li></ul> |
| Gaza–Israel conflict | "Many scholarly sources and international organizations have concluded that Israel's actions in Gaza constitute genocide." | «מקורות מחקריים וארגונים בין־לאומיים רבים הגיעו למסקנה שפעולותיה של ישראל בעזה מהוות רצח עם.» | unchanged | K | Exact; «רבים» = "Many" here |
| Benjamin Netanyahu | (the page's existing, proofed rendering) | | unchanged | K | Not new |

## 3. Other MERGE.md strings

| # | Location | String(s) | Status | Note |
|---|---|---|---|---|
| 4 | Switch | «שפה» · «עברית» / «English» | K | "English" is the language's own name, set `lang="en"` |
| 5 | Lane legend | «במשפט, נוסף מאז 2021» · «במשפט, כמו בינואר 2021» · «לא במשפט, אף שהיה בו בינואר 2021» · «שינוי אחד» · «⇄ n = הוסר או הוחזר n פעמים · הקישו…» | K | Idiomatic; the variable "n" matches the English key |
| 6 | Lane header, tooltips, aria | «N מילים שנאבקו עליהן מאז ינואר 2021 · N הביטויים שנאבקו עליהם יותר מכול»; «כניסה ב־…» / «יציאה ב־…»; «(שינויים: N; האחרון ב־…)»; «, עדיין בלי שינוי» | K | «מכול» is the correct spelling; the dates are NBSP-joined by `heD` |
| 7 | Trail sheet | the range aria, key, meta line, screen-reader prefixes, chips, marker aria, «ציונות: כל מילה שנכנסה ויצאה» | K | The key's colour words match the legend; the feminine «הוסרה / נוספה» agrees with «מילה» |
| 8 | Reach rows | «N מיליון · N%», the article names (now 8, with «בנימין נתניהו», «פלסטין») | K | |
| 9 | Reach key (step 1 extension) | «בנימין נתניהו, ישראל ופלסטין, “genocide” (רצח עם) בפתיח הערך (ב־92.6% מהצפיות בערך על ישראל הוצג “began committing genocide”, החלה לבצע רצח עם; ב־13.6% מהצפיות בערך על נתניהו, “orchestrating the Gaza genocide”, מתזמרת את רצח העם בעזה; ב־41.0% מהצפיות בערך על פלסטין, “recognised as constituting genocide”, הוכרו כרצח עם); …» | A | <ul><li>Uses «הוצג» (item 1).</li><li>The phrase translations match the page's existing renderings (Netanyahu slide; `HE_TM` Palestine).</li></ul> |
| 10 | Reach lead (step 1) | «צפיות בדף בשישת הערכים שלמעלה ובערכים על בנימין נתניהו ועל פלסטין, 9 בנובמבר 2025 – 8 בנובמבר 2026 (סכום של צפיות יומיות). … שבהן הוצג הנוסח הביקורתי:» | A | |
| 11 | Reach key summary (step 3) | «מה נחשב לנוסח הביקורתי · גל הצפיות של אוקטובר 2023» | K | The surge line now sits inside this collapsed key |
| 12 | Caveat | «צפיות בדף, לא קוראים ייחודיים: אדם אחד יכול להיספר פעמים רבות.» | K | |
| 13 | Treemap caption | «… <b>היום 7 מתוך 150 מאשימים</b>, שניים מהם כעובדה, והם קיבלו <b>12%</b> מהצפיות בכל ה־150 (…)» | A | Step 3: «בכל 150 הערכים» → «בכל ה־150». Same referent, one word shorter |
| 14 | Treemap switch, aria, key, tooltip | «ינואר 2021 / יולי 2023 / היום»; «הצגת הפתיחים נכון ל־»; «השטח = צפיות בדף…»; «אין האשמה ברצח עם בפתיח הערך» / «ההאשמה, מיוחסת לאחרים» / «נקבע כעובדה, בקולה של ויקיפדיה» | K | The three voice labels keep their strength: attributed is not «נטען» (softer), and fact is not «הוכח» (sharper) |
| 15 | Morph slider aria | «גררו מאז ועד היום» → «גררו בין אז להיום» | A | «מאז ועד היום» is the idiom "ever since", not "from Then to Now" (the two button labels) |
| 16 | Morph controls | «אז» / «היום» / «שניהם»; «הצגת המשפט»; «נוסף» / «הוסר» / «במקום» / «והוחלף ב־» / «שונה» / «באנגלית:» / «כאן לא הוסר דבר» | K | |

## 4. Step 2: the Data lab (`lab/lab_flash.py`)

The data, article titles and Wikipedia sentences stay in the original; the chrome is Hebrew. `lab_flash.check_he()` asserts, in the build, that no Hebrew run holds an English word (bar the language code EN) or a vetoed wording, and that day–month dates are joined by a no-break space.

| # | String | Status | Note |
|---|---|---|---|
| 17 | Tabs «המהדורה המקוצרת» / «מעבדת נתונים»; aria «תצוגות» | K | «המהדורה המקוצרת» is the masthead's name for the flash edition |
| 18 | Tag "Exploratory": «גישוש» → «ראשוני» | A | Consistency: the page's own "Exploratory" chips are «ראשוני» |
| 19 | Deck: «תצוגות מעשיות» → «תצוגות אינטראקטיביות של הנתונים…» | A | «מעשיות» means "practical", not "hands-on" |
| 20 | Not-in-this-edition note: «לא במהדורה הזאת: התצוגה **הזאת** דורשת…» → «…התצוגה דורשת את מערך הנתונים המלא. למעבדה המלאה (באנגלית) ↖» | A | A doubled «הזאת» was removed. The arrow ↖ is the Hebrew page's external-link arrow |
| 21 | Prism ramp «מהתמונה הראשונה לאחרונה» → «מצילום המצב הראשון לאחרון» | A | "snapshot" |
| 22 | Prism ramp direction | C | <ul><li>The ramp was drawn left to right (fell → rose), while its labels read right to left.</li><li>For Hebrew the gradient runs 270°, so «ירד» sits over the falling colour.</li></ul> |
| 23 | Flipbook meta: «שינוי N מתוך N» · «הנוסח ההתחלתי · אחריו שינויים: N» · «נוסח N מתוך N · ימים בתוקף בסך הכול: N · צפיות של קוראים: כ־N · העריכה הזאת בוטלה» | K | Numbers after a colon avoid singular/plural agreement; "reverted" = «בוטלה», as on the page |
| 24 | «הנוסח לא נשמר (היה בתוקף זמן קצר)» · «השתנו רק רווחים או עיצוב» · «הנוסח הקודם לא נשמר, ולכן השינויים אינם מסומנים» | K | |
| 25 | Block chart: «מלבן לכל נוסח, מהישן (משמאל) לחדש…» · «חריץ כתום: עריכה שבוטלה» · «ימים בתוקף →» · «נוסחים שמורים: N (ועוד N שהיו בתוקף זמן קצר ולא נשמרו) · ימים: N» | K | The time axes stay left to right (older on the left), and the text says so |
| 26 | Prism: «הקישו למיון / גררו את EN ←» · «יש נתונים ב־N מתוך N שפות» · «אין ערך, אין נתונים» · «אנגלית פחות X» · «חזרה לטבלה» · «ממוצע, ערכים: N» | K | The arrow points to the other languages, which in the mirrored grid are on the left |
| 27 | «מימין לקו: שיעור המונחים הביקורתיים (לכל 10,000 מילים) עלה באנגלית יותר מאשר ב…» | K | <ul><li>The positive bars are drawn to the right in both directions, so the text is right.</li><li>"loaded words" = «מונחים ביקורתיים», the page's term.</li></ul> |
| 28 | «מעט מדי כדי לקבוע: פחות מ־30 ערכים, ולכן הממוצע הוא תיאור ולא ממצא.» | K | Keeps the English hedge exactly |
| 29 | Banner: «מהמהדורה המקוצרת: הערך Hamas, עכשיו בדפדפת ההגדרות. → חזרה למהדורה המקוצרת» | K | <ul><li>The article title stays as data, in the original.</li><li>The research lab quoted the section heading (cut at 60 characters). Here it is dropped in both languages, because the flash headings carry their own quotes and the cut split them.</li></ul> |
| 30 | Month names (Hebrew), DLL «5 בינואר 2021» with NBSP; language names | K | |
| 31 | Deep link «לחקירה במעבדת הנתונים ←» | K | |

## 5. Step 3: the length cut (wording)

Every cut keeps the claim and its strength; the asserted lines in `flash_he.py` (the must-keep list) are untouched.

| # | Location | Before → after | Status | Why it holds |
|---|---|---|---|---|
| 32 | c3 H2 | «השורה הראשונה של ויקיפדיה על 7 באוקטובר **מדברת היום על** ״חדירות…״» → «**בשורה הראשונה** של ויקיפדיה על 7 באוקטובר **כתוב היום** ״חדירות חמושות מתואמות״» | A | "now says" is literally «כתוב היום». The second sentence (P1 #22) is unchanged |
| 33 | c7 H2 | «על הסיקור שלה בנושא הזה» → «על סיקורה בנושא הזה» | A | The same words. The binding parts («מצאו», «יש עניין רב בהשפעה», «הם לא נקבו בשמו של צד או של מדינה כלשהם») are untouched |
| 34 | #breathe key | «כל מילה שהוסרה מאז ינואר 2021 מסומנת בקו מחיקה; כל מילה שנוספה בכחול. מילות המפתח מודגשות:» → «מחוקה: כל מילה שהוסרה מאז ינואר 2021; בכחול: כל מילה שנוספה. מודגשות מילות המפתח:» | A | Key style, the same content |
| 35 | c5 bridge | «…היסטוריית הגרסאות של ארבעה משפטים ראשונים מראה…» → «…בארבעה משפטים ראשונים, ההיסטוריה מראה איזה נוסח נשאר ואיזה הוצא.» | A | It is now closer to the English ("In four first sentences, the history shows…") |
| 36 | c3 "What changed", our translation | «״סדרה של מתקפות מתואמות״ ← ״סדרה של חדירות חמושות מתואמות״» → «״…מתקפות מתואמות״ ← ״…חדירות חמושות מתואמות״» | A | <ul><li>The shared «סדרה של» is elided on both sides, so the contrast is the same.</li><li>The full English sentence is directly above.</li></ul> |
| 37 | Spanish slide, the punch line | «״עימות מזוין … ושחולל רצח עם בעזה בידי ישראל״» → «״… ושחולל רצח עם בעזה בידי ישראל״» | A | <ul><li>The changed clause is unchanged, and the subject stays the conflict (P2 #14).</li><li>The full translation is right above.</li></ul> |
| 38 | Hero stack, Israel row date | «יולי 2023 ← ״רצח עם״ (“genocide”) מאז 4 במאי 2025» → «יולי 2023 ← ״רצח עם״ מאז 4 במאי 2025» | A | The original “began committing genocide” is on the next line of the same row |
| 39 | c7 ArbCom note | «…PIA״ (הסכסוך הישראלי־פלסטיני) (ממצא 16, 9 בדצמבר 2024).» → «…PIA״ (הסכסוך הישראלי־פלסטיני; ממצא 16, 9 בדצמבר 2024).» | A | One parenthesis, not two in a row (punctuation) |
| 40 | Originals lines removed: c3, c4 H2s; c4 militant line; c5 and c7 H2s; "In short" | The English originals of the heading quotes now sit only in the block that follows: c3 "What changed", the c4 blockquotes, the c5 "What changed" and blockquotes, the ArbCom quote, and the hero stack for "In short". | C | <ul><li>The quote check is relaxed: an English original may appear inside a longer quoted original.</li><li>It is capped at 6 such quotes.</li><li>No quote is altered, and the set of quotes the English page does not carry stays empty.</li></ul> |

**Layout, Hebrew phone only (no wording):**
- the English originals are a little smaller where our translation sits under them (blockquote 13.5 px, hero 13.5 px, morph 12 px, pair 12 px, originals lines 10.5 px), and so are the translations (13 px, card 5 pair 12.5 px);
- H2 is 19.5 px, as in English;
- the card 5 own-voice column is wider (1.3 : 1);
- the carousel and pair gaps are tighter, and the eyebrow links use line-height 1.2.

## 6. Global checks on the final build

- **No italic:** the smoke test's synthetic-italic check passes in Hebrew.
- **NBSP:** every visible day–month date is joined by a no-break space (smoke test). The lab's `DLL` emits «N ב<month>».
- **No English in the UI:** the smoke test's text scan of the visible Hebrew page passes, and the build checks the lab chrome (§4).
- **Vetoes:** all old and new `HE_VETO` entries are absent.
