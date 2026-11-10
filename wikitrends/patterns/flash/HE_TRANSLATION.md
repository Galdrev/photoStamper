# Flash edition, Hebrew: translation notes for the proofreaders

> v2 applied the three proofs. Every decision, and every changed rendering, is in `HE_FIXLOG.md`, which takes precedence over this file where they differ.

- **Build:** `cd wikitrends && python build_flash.py --lang he OUT.html`. The English page is built and checked first, in memory. `python build_flash.py OUT.html` without the flag is unchanged, and its output is byte-identical to the impact2e build (`cmp`).
- **Files:**
  - `flash_i18n_he.json` holds every string.
  - `flash_he_overlay.html` holds the Hebrew CSS and JS: fonts, RTL mirroring, Hebrew dates, the share images, and labels for data-driven strings.
  - `flash_he.py` applies the strings and runs the Hebrew checks.
  - No chart code or data logic was copied.
- **Output:** `scratchpad/flash/he1/index.html`. Contact sheets are `contact_*.png` in the same folder; the smoke log is `smoke_result.txt`.

## How to review

1. **The string map is `flash_i18n_he.json`.** Each entry is `[exact English, Hebrew]`. If an English string disappears from the English page, the build fails, so the map cannot go stale silently.
   - `template`: card text, aria labels and flash-script strings. Markup entries are whole lines, so they read top to bottom in card order.
   - `lib`: the research edition's chart and grid code (#breathe, #kChart, #xwGG, the language grid and its tooltips).
   - `slots`: the research markup cut into the page.
   - `events`: the 33 battles and ceasefires in the weekly chart's tooltips.
   - `coding_notes`: the 19 language-grid explanations.
   - `columns`: the grid's five column names.
2. **Quotes are evidence. Only Hebrew is ours.**
   - Every curly-quoted string (“…”) on the Hebrew page is an original Wikipedia quote, identical to the English page. The build asserts this both ways.
   - Our translations always use **״…״** and sit directly under the original, marked **תרגום שלנו**.
   - Please proofread the ״…״ text. Do not touch anything inside “…”.
3. **Hebrew Wikipedia quotes** (Hamas, and the Gaza war's South Africa sentence) are shown as they are, with no translation. The English translation that the English page carried under them is dropped.
4. **Headlines:**
   - The Hebrew headline carries our translation of the quoted words in ״…״.
   - The original English words follow directly below, in small LTR type (`.he-o`).
   - Inline quoted words in Hebrew prose follow the same pattern: Hebrew in the sentence, the English originals on a small LTR line under the paragraph.

## Glossary: choices and reasons

| English (as quoted) | Hebrew | Why |
|---|---|---|
| re-establishment (of a Jewish state) | **הקמה מחדש** | This is the literal sense of re- plus establishment. "השבה" (restoration/return) brings in שיבת ציון and reads more Zionist than the English, so it sharpens. |
| colonization | **קולוניזציה** | This is the exact loanword, the one Israeli academic and press Hebrew (Haaretz) uses for the English term. "התיישבות קולוניאלית" is rejected: in Israeli Hebrew "התיישבות" is the honoured Zionist word for settlement, so the phrase both softens (התיישבות) and doubles the charge (קולוניאלית). |
| colonial / settler colonial | קולוניאלי / (not used on the page) | Consistent with the row above. |
| a Jewish homeland | **מולדת יהודית** | "homeland" = מולדת. "בית לאומי" is Balfour's "national home", a different English phrase that the 2021 text did not use. |
| ethnic cleansing | **טיהור אתני** | This is the standard term. |
| genocide | **רצח עם** | <ul><li>It is the standard term in Israeli news coverage of the ICJ case (Kan, Ynet, Haaretz).</li><li>It is the word Hebrew Wikipedia itself uses in the sentence quoted on the page ("בגין רצח עם"), so the page stays consistent with its own Hebrew evidence.</li><li>"ג'נוסייד" marks the discourse about the term and would distance the reader from Wikipedia's own-voice claim, which is a softening.</li><li>"השמדת עם" is the statutory term of the 1950 law, more formal and less common in the news.</li></ul> |
| genocidal massacre | טבח בעל אופי של רצח עם | This is a precise paraphrase of the adjective. "טבח ג'נוסיידי" was rejected for the reason in the row above. *Uncertain.* |
| armed incursions / coordinated armed incursions | **פשיטות חמושות** / ״פשיטות חמושות מתואמות״ | Changed in fix log 3 (owner's request; `HE_FIXLOG3.md` §1): "incursion" is a sudden, limited armed entry, i.e. a raid (פשיטה). «חדירות» lost the hostile sense; «פלישות» (invasion) would sharpen, and English Wikipedia removed "invasion" from this sentence. «חדירות» is now vetoed. |
| coordinated attacks | מתקפות מתואמות | |
| political organisation with a military wing | **ארגון פוליטי בעל זרוע צבאית** | |
| militant (Hamas 2021) | **חמוש** | <ul><li>In English Wikipedia usage "militant" means an armed non-state group, which is "חמוש" in Israeli news Hebrew (Kan).</li><li>"מיליטנטי" in Hebrew leans toward "aggressively activist", a different sense.</li><li>The headline therefore reads ארגון ״חמוש״.</li><li>The English “militant” stands below it.</li></ul> |
| military (wing) | צבאי / צבאית | |
| terrorist (the word) | ״טרוריסטי״ (the word) | It is written as "המילה ״טרוריסטי״" so that it reads as a word that went in or out, not as our label. |
| terror organisation (Hebrew Wikipedia) | ארגון טרור | Quoted as is. |
| terrorist organisation (designation sentences) | ארגון טרור | This is the standard Hebrew rendering of "terrorist organisation". |
| Nakba | **הנכבה** | |
| hostages (our prose) | **החטופים** | This is the Israeli usage. |
| "taken as hostages" (inside a translated quote) | **נלקחו כבני ערובה** | Inside a quote we translate the English word exactly. "hostages" = בני ערובה; "חטופים" (abductees) is the Israeli usage and slightly stronger. *Uncertain: the proofreaders may prefer "נלקחו כחטופים".* |
| ArbCom / Arbitration Committee | **ועדת הבוררות של ויקיפדיה**; arbitrators = הבוררים של ויקיפדיה | |
| banned (an account) | הורחק | This is Wikipedia's "ban" (an editing ban), as distinct from "block" (חסימה). |
| own voice / in Wikipedia's voice | **בקולה של ויקיפדיה** | The badge reads "בקולה של ויקיפדיה". |
| attributed | **מיוחס לאחרים** (badge); מיוחס (legend) | |
| opening section / first sentence / opening lines / opening paragraphs | **פתיח הערך** / **המשפט הראשון** / **שורות הפתיחה** / **פסקאות הפתיחה** | The four are kept distinct, because the English scopes are binding (messaging F3, F11). |
| article (Wikipedia) | ערך | |
| version / wording / revision | גרסה / נוסח / גרסה (rev → "גרסה") | |
| critical terms | מונחים ביקורתיים | |
| Exploratory (chip) | **ראשוני** | It means "preliminary". "ניסיוני" sounds like an experiment. *Uncertain.* |
| carried out by Israel | ״מבוצע בידי ישראל״ (headline) / ״שמבוצע בידי ישראל״ (the sentence, agreeing with ההרס) | v2: "destruction" is ההרס, never השמדה (HE_FIXLOG.md). |
| Some have alleged | ״יש הטוענים״ | v2: keeps the strength of "alleged" (HE_FIXLOG.md, conflict 2). |
| Allegations have been made | ״הועלו האשמות״ | "allegation" = an accusation of wrongdoing, so האשמה. "טענות" would soften. |
| massacring civilians in 21 communities | ״תוך טבח באזרחים ב־21 יישובים״ | "communities" here means the kibbutzim and towns, which Israeli Hebrew calls יישובים. *Uncertain: the literal word is "קהילות".* |
| fighters (Hamas fighters) | לוחמי חמאס | This is literal. "מחבלים" would sharpen. |
| orchestrating (the Gaza genocide) | מתזמרת את | "מנצחת על" was the alternative. |
| truce (Nov 2023) | הפוגה | |
| ground invasion | הפלישה הקרקעית | This is literal. Israeli media say "התמרון הקרקעי", which would soften the event label. *Uncertain.* |
| killed (Nasrallah, Sinwar, Khamenei) | נהרג | This is neutral. "חוסל" is the common Israeli usage but sharper. "assassinated" (Haniyeh) = ההתנקשות. |

## Quote marks, dates, numbers

- **Quote marks.**
  - Our Hebrew uses ״ (U+05F4) throughout. It is safe inside the JS and HTML strings.
  - The same character is also the acronym mark (אצ״ל, לח״י, האו״ם), which appears once inside a quote: ״…ההגנה, אצ״ל ולח״י״.
  - If the house style is ASCII " instead, it is one global replace in `flash_i18n_he.json` and the overlay. Nothing in the checks depends on it.
- **Dates.**
  - The style is "7 באוקטובר 2023", month and year "אוקטובר 2023", and day ranges "1 בינואר 2021 ← מאז 27 באוגוסט 2026".
  - Short chart ticks use abbreviated months: ינו׳, פבר׳, אוק׳…
  - Year ticks keep ’23.
- **Arrows:**
  - Then→now arrows inside Hebrew text are mirrored (←), and the "evidence →" links become "←".
  - Inside the English evidence lines the arrows stay →.
  - The external-link arrow ↗ becomes ↖.
  - The ▶ play icons are not mirrored, by media convention.
- **Charts and timelines** keep time running left to right, by Hebrew news-chart convention. The lane labels inside them are right-aligned.
- **Numbers.** There are no new numbers.
  - The build checks that every number in the static Hebrew text is on the English page.
  - It checks that every number in each translated string is in its English source.
  - Three vote and score forms were changed so they read correctly right to left: "15 מול 0", "89%–100%" and "‎+187 ימים".

## The lines whose strength must not change (asserted by the build)

| Line | Hebrew |
|---|---|
| Scope | **הדוח מודד איך השתנה הנוסח של ערכי הליבה שאנשים קוראים, ולא אם מה שכתוב בו נכון, ואינו שופט את ניהול המלחמה או את התנהלותה של ממשלה כלשהי.** |
| Honesty | השינוי מרוכז בערכי הליבה שאנשים קוראים, בעוד הזנב הארוך של הדפים הקצרים כמעט לא השתנה. |
| Denial (hero) | בערך על ישראל, המשפט הבא: “Israel has denied that its actions constitute genocide.” ״ישראל הכחישה שמעשיה מהווים רצח עם.״ |
| Denial (car1) | המשפט הבא: ״ישראל הכחישה…״ / Netanyahu: אין הכחשה |
| Credibility 1 (Hamas context) | הקשר: בהתאם להנחיות הסגנון של ויקיפדיה כולה לגבי תוויות שנויות במחלוקת, המילה ״טרוריסטי״ יצאה מהמשפטים הראשונים של הערכים על המדינה האסלאמית (דאעש), אל־שבאב ובוקו חראם. המשפט הראשון על חמאס לא כלל אותה ב־2021. |
| Credibility 2 (Oct 7, own voice) | הערך על 7 באוקטובר מתאר את ההרג בקולה של ויקיפדיה: ״תוך טבח באזרחים ב־21 יישובים״; ״לפחות 1,195 בני אדם נהרגו כתוצאה מהמתקפות״ (with the English originals under it) |
| Gone vs undone (F1/F7) | <ul><li>The 10 attempts were "נעלמה" (gone).</li><li>"בוטלה בתוך יום" (undone within a day) appears only in the Zionism slide, which is asserted.</li></ul> |
| Camp voting | זו הצבעה לפי מחנות, לא הוכחה לתיאום; לא קידדנו באיזה צד צידדה כל קבוצה… |

The vetoed wordings' Hebrew equivalents are listed in `flash_he.py` (`HE_VETO`) and asserted absent: העולם קורא, שני הצדדים, מתועד, לטובת ישראל, למה זה חשוב, הערך של ישראל עצמה/עצמו, רק חמאס, 64 מתוך, 47 מתוך, and others.

To avoid the spin veto "Israel's own article", the H1 says "הערך על ישראל" (the article on Israel), never "הערך של ישראל עצמה".

## Where the Hebrew is not complete (v1 scope)

- **The play sheet** (#ziFig, #o7Fig, #xrFig) is the research edition's full instrument. It stays in English, left to right, inside a Hebrew frame: the title, the close button, the source link and a one-line note saying it is the research tool in its original language. Translating it means about 600 more data-driven strings; that is v2.
- **Tooltips** have Hebrew chrome: labels, dates, voice states and the coding notes. The revision sentence they show (one of 169 wordings, for example) stays in its original language without a Hebrew translation.
- **The language-grid tooltip** shows the original sentence and the stored English translation, labelled "התרגום שלנו לאנגלית". The term glosses ("= “terrorist”") also stay in English. Hebrew translations of the roughly 100 grid sentences are not in v1.
- **The 19 grid coding notes and the 33 chart events** are ours, translated into Hebrew. Where a note quotes another language, the Hebrew is our translation of the stored English rendering, a second-hand translation. Please check those against the original-language sentence shown in the same tooltip.
- **Screen count:** 10.55 phone screens at 390×844 with the fonts loaded, against 9.69 for the English page. The extra height is the translation lines.

## Renderings we were unsure of

1. ״נלקחו כבני ערובה״ against ״נלקחו כחטופים״, for "taken as hostages" inside the quote.
2. ״יישובים״ against ״קהילות״, for "communities" in "massacring civilians in 21 communities".
3. ״טבח בעל אופי של רצח עם״, for "genocidal massacre".
4. ״חמוש״, for "militant": the adjective standing alone in the hero row reads a little bare.
5. ״מתזמרת את רצח העם בעזה״, for "has been orchestrating the Gaza genocide". "מנצחת על" was the alternative.
6. The Arabic Gaza genocide sentence: "الاستهداف" (targeting) is rendered ״הפגיעה״. "targeting" is literally "הכוונה/סימון כמטרה", so this may soften.
7. The Spanish "ha desencadenado un genocidio" is rendered ״שחולל רצח עם״. Alternatives are "הצית" and "שילח".
8. Hebrew month abbreviations in charts (אוק׳ and the rest) against full names.
9. "Exploratory" is rendered ״ראשוני״.
10. "ground invasion" / "Lebanon invasion" are rendered הפלישה, against Israeli news usage "התמרון הקרקעי".
11. Quote-mark style: ״…״ against "…".
12. The Zionism first sentence, 2021 and today, in the "תרגום שלנו" details under #breathe:
    - "Land of Israel in Judaism—itself central to Jewish history" is rendered "ארץ ישראל ביהדות, שהיא עצמה מרכזית בהיסטוריה היהודית".
    - The English is ambiguous about what "itself" refers to.
13. The project name "סחף המסגור בוויקיפדיה" (Wikipedia Framing Drift). The edition name "המהדורה המקוצרת" was chosen over "בקצרה" and "מהדורת הבזק".
