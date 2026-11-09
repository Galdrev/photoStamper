# Flash edition, Hebrew v1: proof 1 (chief copy editor)

- **Read:** `flash_i18n_he.json` (every pair), `flash_he_overlay.html`, `HE_TRANSLATION.md`.
- **Rendered page:** opened on an iPhone 13 (390×844) and at 1280×900. I checked every screen, both carousels, the hero, the grid tooltip, the lane tooltip, the play sheet frame, and the four share cards.
- **Screenshots:** `scratchpad/flash/he_proof1/`. Files `RTL1…RTL8_*.png` are the evidence for the RTL rows below; `raw_*` are the full screen captures.
- **Untouched:** I did not touch anything inside “…” (the original quotes).
- **Lens:** does this read as native, top-tier Israeli journalism?
- **Verdict:** yes, mostly. The register is sober and the terminology is mostly right. The main faults are:
  - a handful of calques ("הגיע ל־1948", "נותן תאריך", "נקבו בשום צד");
  - one real accuracy slip in the "In short" paragraph;
  - English strings left over in the data-driven UI;
  - three RTL rendering bugs: the run-on in the titles chart, dates breaking across lines, and reversed quotes in a share card.

Severity: **3** = must fix before publication (wrong meaning, broken rendering, English on the Hebrew page). **2** = a top desk would fix it (calque, ambiguity, inconsistency a reader notices). **1** = polish.

## Counts

| Severity | Issues |
|---|---|
| 3 | 7 |
| 2 | 25 |
| 1 | 26 |
| **Total** | **58** |

## Top 10

1. **R1, the titles chart in carousel 1, slide 1 (sev 3).** The `<br>` does not break, so the row reads "‎+110 ימיםשם חדש ‎+180": two words fused, the second number has no unit, and the bidi order is scrambled. Screenshot: RTL1.
2. **R2, dates break across lines (sev 3).** "7 / באוקטובר" splits across lines in the H2s of cards 3 and 5 and in a caption. Use a no-break space between the day and the month, globally. Screenshots: RTL2, RTL3.
3. **T106, the "In short" paragraph (sev 3).** "היום הערך על ישראל אומר … שישראל ״החלה לבצע רצח עם״, הציונות היא ״מולדת יהודית…״" makes the Zionism quote read as part of the Israel article. It comes from the Zionism article. Name the source of each quote.
4. **L33 / L36 / L42 / L52 (sev 3).** "court case only" and "now reported as a court case" are left in English inside Hebrew tooltips and grid labels. XSHORT/XM_SHORT `icj:"icj"` shows a lowercase code as a label.
5. **The grid legend and rows (sev 3).** The chip reads "n/a" in English. The Hebrew row reads "עברית / עברית"; the English row has no Hebrew name. Screenshot: RTL4.
6. **The flRw share card (sev 2).** The English quote inside the Hebrew label is drawn as ”genocide“, with reversed curly quotes. Screenshot: RTL5.
7. **T62, the Spanish slide caption (sev 2).** ״מתקפת תגמול … שחולל רצח עם״ reads as a gender-agreement error (מתקפה is feminine, שחולל masculine). "מצד ישראל" is a calque of "por parte de".
8. **T24 / T31 (sev 2).** "שינוי מאותו סוג הגיע גם ל־1948" and "הגיע גם ל־7 באוקטובר" are calques: the change reached the articles, not the year.
9. **T71, the card 6 headline (sev 2).** "מאז ספטמבר 2025, 10 עריכות…" puts two numbers in collision. Write "מאז ספטמבר 2025 ניסו עשר עריכות…".
10. **Typography (sev 2).** The `.fl-next` lines and the empty-lane notes are set in synthetic italic. Hebrew has no italic, and Frank Ruhl Libre and Heebo have none, so the browser slants the letters. Screenshot: RTL6.

## Issue table

The location column uses JSON keys: `T` = template[i], `L` = lib[i], `S` = slots[i], `ev` = events, `cn` = coding_notes, `OV` = overlay. "Locked" means the line's strength is asserted by the build; I propose the change anyway and flag it.

| # | Location | Current Hebrew | Proposed Hebrew | Type | Sev | Reason |
|---|---|---|---|---|---|---|
| 1 | L29, car1 slide 1 (#xwGG rows) | ‎+110 ימים`<br>`שם חדש ‎+180 (rendered: "‎+110 ימיםשם חדש ‎+180") | ‎+110 ימים · שינוי שם: ‎+180 ימים (separator, not `<br>`, or force `display:block` on the inner span) | RTL | 3 | The line break is lost in the RTL cell, so words fuse and the bidi order of the two numbers flips. "renamed +180 d" lost its unit. "שם חדש" is a noun ("new name"), not the event. Screenshot RTL1. |
| 2 | Global: c3H, c5H, T36 cp, every "7 באוקטובר" | 7␠באוקטובר (breakable) | 7&nbsp;באוקטובר (U+00A0), also "ב־7&nbsp;באוקטובר" and "ל־7&nbsp;באוקטובר" | RTL | 3 | The date splits as "…על 7 / באוקטובר" in the card 3 and card 5 headlines on iPhone. Screenshots RTL2, RTL3. Apply in heD() as well. |
| 3 | T106 fl-dinner | …היום הערך על ישראל אומר, בקולה של ויקיפדיה, שישראל ״החלה לבצע רצח עם״, הציונות היא ״מולדת יהודית באמצעות קולוניזציה״, ובכל עותק שבידינו, פתיחי הערכים על ישראל ועל חמאס אינם מזכירים את החטופים. | …היום הערך על ישראל קובע, בקולה של ויקיפדיה, שישראל ״החלה לבצע רצח עם״; הערך על הציונות מגדיר אותה ״מולדת יהודית באמצעות קולוניזציה״; ובאף עותק שבידינו פתיחי הערכים על ישראל ועל חמאס אינם מזכירים את החטופים. | strength / grammar | 3 | Attribution: in Hebrew the Zionism quote is governed by "הערך על ישראל אומר". The English has the same weakness; flag it to the EN desk too. |
| 4 | L33 XVB.legal, L36, L42, L52 | court case only / (court case only) / now reported as a court case | ״רק התביעה המשפטית״ / (רק התביעה המשפטית) / היום מדווח כתביעה משפטית | terminology | 3 | English left in Hebrew tooltips and grid states. |
| 5 | L38 XSHORT.icj, L50 XM_SHORT.icj | icj | בית הדין בהאג (or ICJ, in capitals) | terminology | 3 | A lowercase code shown as a column or tooltip label. |
| 6 | Grid legend chip (xTile na) | n/a | אין | terminology | 3 | English on the Hebrew page, shown in the legend and in 3 cells. Screenshot RTL4. |
| 7 | Grid rows: he and en | עברית / עברית ; English (no Hebrew) | עברית (one line) ; English / אנגלית | RTL / consistency | 3 | The native name and the Hebrew name are the same for he, so drop one. Every other row has two lines, but en has one. |
| 8 | OV shSpec flRw (share card) | (”genocide“) in the Israel label | Draw the English segment through shWrap (LTR), or put U+2066…U+2069 around it | RTL | 2 | The canvas RTL pass mirrors the curly quotes. Screenshot RTL5. |
| 9 | T62 cp, Spanish slide | ״מתקפת תגמול … שחולל רצח עם בעזה מצד ישראל״ | ״עימות מזוין … שחולל רצח עם בעזה בידי ישראל״ (or keep ״מתקפת תגמול…״ and cut at ״…ושחולל רצח עם בעזה בידי ישראל״) | grammar | 2 | Next to the ellipsis, מתקפה (fem.) plus שחולל (masc.) looks like an agreement error. "מצד ישראל" is a calque; the page's term is "בידי". Screenshot RTL7. |
| 10 | T62 he-tr (now) | ״…ושחולל רצח עם בעזה מצד ישראל נגד האוכלוסייה האזרחית הפלסטינית.״ | ״…ושחולל רצח עם שישראל מבצעת בעזה נגד האוכלוסייה האזרחית הפלסטינית.״ | idiom | 2 | The calque again; also matches the Arabic slide ("שישראל מבצעת"). |
| 11 | T24 fl-next | שינוי מאותו סוג הגיע גם ל־1948. | שינוי דומה הגיע גם לערכים על 1948. | idiom | 2 | "הגיע ל־1948" reads as time travel. |
| 12 | T31 fl-next | והשינוי הגיע גם ל־7 באוקטובר. | והוא הגיע גם לערך על 7 באוקטובר. | idiom | 2 | As above. |
| 13 | T71 c6H | מאז ספטמבר 2025, 10 עריכות ניסו להחזיר למשפט על רצח העם בעזה ניסוח מיוחס. כל אחת מהן נעלמה בתוך 45 דקות. | מאז ספטמבר 2025 ניסו עשר עריכות להחזיר ייחוס למשפט על רצח העם בעזה. כל אחת מהן נעלמה בתוך 45 דקות. | headline / number | 2 | "2025, 10" puts two numbers side by side, and Hebrew style spells out numbers under 11 in headlines. The number 10 itself is kept, and "נעלמה" (locked) stays. |
| 14 | `.fl-next`, `.fl-lane .empty` CSS | synthetic italic | `font-style:normal` for `html[lang=he]`; mark with colour or weight instead | RTL / typography | 2 | Hebrew has no italic and the browser slants the letters. Screenshot RTL6. |
| 15 | T81 kCap | התזמון נותן תאריך, לא סיבה. | התזמון מלמד על מועד, לא על סיבה. | idiom | 2 | A calque of "gives a date". |
| 16 | T81 kCap | …לעומת 3.8 בשישה השבועות שלפני. | …לעומת 3.8 בשישה השבועות שקדמו לו. | grammar | 1 | "שלפני" dangles at the end of the sentence. |
| 17 | T84 c7H | הם לא נקבו בשום צד ובשום מדינה. | הם לא נקבו בשמו של צד או של מדינה כלשהם. | idiom | 2 | "נקב ב־" takes a name or number ("נקב בשם/במחיר"), not a side. |
| 18 | T28 | שלושה ערכים על 1948 נוקבים היום, בקולה של ויקיפדיה, במי שגירש את הפלסטינים | שלושה ערכים על 1948 נוקבים היום, בקולה של ויקיפדיה, בשם מי שגירש את הפלסטינים | idiom | 2 | As above. |
| 19 | T28 | על היהודים ש״נמלטו או גורשו ממדינות ערב״, לא נזכר שום גורם. | על היהודים ש״נמלטו או גורשו ממדינות ערב״ לא נאמר מי גירש אותם. | idiom / punctuation | 1 | A parallel, concrete close. No comma before the main clause. |
| 20 | T103 | המשפט הבא נוקב ב״ארגונים הצבאיים־למחצה הציוניים ההגנה, אצ״ל ולח״י״. | המשפט הבא נוקב בשמות ״ההגנה, האצ״ל והלח״י, הארגונים הצבאיים־למחצה הציוניים״. | punctuation | 2 | "לח״י״" makes the acronym mark and the closing quote collide. Reordering inside our translation removes the collision and adds the name idiom. |
| 21 | T37 | הפתיח עדיין אומר ״תוך טבח באזרחים ב־21 יישובים״, והמשפט הראשון נוקב בשם חמאס, בהמשכו. | הפתיח עדיין אומר ״תוך טבח באזרחים ב־21 יישובים״, ושמו של חמאס מופיע במשפט הראשון, אבל רק בהמשכו. | idiom | 2 | "נוקב בשם חמאס, בהמשכו" is awkward and the sense of "later on" is lost. |
| 22 | T33 c3H | …ב־107 גרסאות היא מעולם לא הזכירה את החטופים. | …באף אחת מ־107 הגרסאות שלה לא הוזכרו החטופים. | headline | 2 | "ב־107 גרסאות … מעולם" clashes logically; the "none of" form is the native headline structure. Same strength. |
| 23 | T125 lane vs c3H | ב־107 נוסחים (lane) / ב־107 גרסאות (H2) | One term, "גרסאות", in both | terminology | 1 | The same number has two nouns on one screen. The English also mixes versions and wordings; the Hebrew reader notices more. |
| 24 | T41 c4H | ב־2021 ויקיפדיה הגדירה את חמאס ארגון ״חמוש״. | ב־2021 הגדירה ויקיפדיה את חמאס ארגון ״חמוש״. | headline | 1 | Verb–subject inversion after a fronted adverbial is the newsroom register. |
| 25 | T12 hero he-tr (Hamas) | ״חמוש״ ← ״ארגון פוליטי בעל זרוע צבאית״ | ארגון ״חמוש״ ← ״ארגון פוליטי בעל זרוע צבאית״ | idiom | 1 | A bare adjective set against a noun phrase; match the H2 (see U4). |
| 26 | T45 | באנגלית, ״חמוש״ יצא ב־12 באוקטובר 2023 | באנגלית, המילה militant (״חמוש״) הוסרה ב־12 באוקטובר 2023 | terminology | 2 | A Hebrew word cannot leave an English article, so the reader needs the English word in the sentence. See global decision G4. |
| 27 | T45 | ויקיפדיה בעברית מנסחת זאת הפוך | ויקיפדיה בעברית מנסחת זאת בסדר הפוך | idiom | 1 | It is the order that is reversed, not the claim. |
| 28 | T44 fig-t | ההכרזה עליו כארגון טרור עברה ממשפט 5 למשפט 22 | ההכרזה על חמאס כארגון טרור ירדה ממשפט 5 למשפט 22 | idiom | 1 | A figure title should stand alone; "עליו" has no antecedent there. |
| 29 | T118 pos-row | `<br><small> · משפט 5 מתוך 20` | `<br><small>משפט 5 מתוך 20` | punctuation / RTL | 2 | A stray leading "·" on the new line at 1280. Screenshot RTL8. |
| 30 | T46 fl-ctx (locked) | המדינה האסלאמית | המדינה האסלאמית (דאעש) | terminology | 1 | An Israeli reader knows the group as דאעש. |
| 31 | T50 cxH | אחת־עשרה ויקיפדיות, חמש טענות: העותק הראשון שלנו, ואחריו היום | אחת־עשרה ויקיפדיות, חמש טענות: אז (העותק הראשון שלנו) והיום | headline | 2 | "ואחריו היום" is translationese for "then now". |
| 32 | L37 / L40 grid caption | איך כל מהדורת שפה מנסחת 5 טענות | איך כל ויקיפדיה מנסחת חמש טענות, אז והיום | number / idiom | 1 | The H2 spells the number out but the caption uses a digit. "מהדורת שפה" is acceptable but heavy. |
| 33 | T60 car1 caption | האנגלית הסירה מהכותרת את ״האשמות״ ב־3 ביולי 2024 (‎+187 ימים); הפולנית ב־26 באפריל 2026 (‎+849 ימים). | ויקיפדיה באנגלית הסירה את ״האשמות״ מהכותרת ב־3 ביולי 2024, 187 ימים אחרי פתיחת הערך; ויקיפדיה בפולנית, ב־26 באפריל 2026, אחרי 849 ימים. | idiom | 2 | A language does not edit. "+187" is a chart convention, not prose. The numbers are unchanged. |
| 34 | L29 / L26 | ראשונה ; שם חדש | הראשונה ; שינוי שם | terminology | 1 | See #1. |
| 35 | T67 slide label | עברית · היוצאת מן הכלל | עברית · יוצאת הדופן | idiom | 1 | This is the journalistic idiom. |
| 36 | T67 cp | הערך העברי על מלחמת עזה אינו קובע את ההאשמה. הוא מדווח רק על התביעה של דרום אפריקה. | הערך העברי על מלחמת עזה אינו קובע שמתבצע רצח עם; הוא מדווח רק על התביעה של דרום אפריקה. | strength / idiom | 2 | "קובע את ההאשמה" reads as "determines the charge". The meaning is "does not state it in its own voice". |
| 37 | T53 c5H vs T13/T54/T55 | ״מבוצע בידי ישראל״ (H2) / ״שמבוצעת בידי ישראל״ (rows) | Keep both inflections, but in the rows use ״…שמבוצעת בידי ישראל״ with a leading ellipsis | punctuation / consistency | 1 | A clause cut at "ש" reads as a fragment. The two inflections of one English phrase are legitimate (agreement) but need the ellipsis cue. |
| 38 | T34 hfr:b | ״עשרות מקרים של אונס ותקיפה מינית.״ | ״עשרות מקרים של אונס ותקיפה מינית״. | punctuation | 1 | A fragment takes the full stop outside the quote in Hebrew. A full sentence (T14) keeps it inside, which is correct. |
| 39 | T74 cp | (״לכאורה״, ״מתואר בידי רוב החוקרים כ־״) | (״לכאורה״, ״מתואר בידי רוב החוקרים כ…״) | punctuation | 1 | A maqaf next to gershayim looks like a glyph error. |
| 40 | T73 / T72 | כמה זמן מחזיקה מילה | כמה זמן שורדת מילה | idiom | 1 | "מחזיקה" is colloquial. |
| 41 | T69 | בארבעה משפטים ראשונים, ההיסטוריה מראה איזה נוסח נשאר ואיזה הוצא. | היסטוריית הגרסאות של ארבעה משפטים ראשונים מראה איזה נוסח נשאר ואיזה הוצא. | idiom | 2 | "ההיסטוריה" reads as history, not the page history. |
| 42 | T77 | בכל 254 ערכי הליבה וערכי החשיבות העליונה והגבוהה בנושא | בכל 254 הערכים בנושא, ערכי הליבה וערכים שדורגו בחשיבות עליונה או גבוהה | idiom | 1 | Wikipedia jargon; this form is clearer. |
| 43 | T85 | התקבל ברוב של 15 מול 0 | התקבל פה אחד, 15 מול 0 | idiom | 2 | "ברוב" with no one opposed is odd. "15 מול 0" is kept. |
| 44 | T85 cap | …הקשורה לתחום PIA | …הקשורה לתחום הסכסוך הישראלי־פלסטיני (PIA) | terminology | 1 | An unexplained code. |
| 45 | T88 fl-fact | …ב־89% עד 100% מהמקרים, לעומת כמחצית במקרה. | …הצביעו באותו אופן ב־89% עד 100% מהמקרים, כשבהצבעה מקרית היה מתקבל כמחצית. | idiom | 2 | "לעומת כמחצית במקרה" is a calque. "voted together" is more precise as "הצביעו באותו אופן". |
| 46 | T86 aria | מקריות נותנת כמחצית | בהצבעה מקרית: כמחצית | idiom | 1 | A calque. |
| 47 | T89 (locked) | זו הצבעה במחנות | זו הצבעה מחנאית | idiom | 1 | This is the native term. The strength is identical. |
| 48 | T92 clH | הדפים הנקראים ביותר שבפתיח שלהם נוספה שפה ביקורתית | הדפים הנקראים ביותר שלפתיח שלהם נוספו מונחים ביקורתיים | terminology | 2 | The page's fixed term is "מונחים ביקורתיים"; "שפה" changes it. |
| 49 | T0 `<title>` vs mast/foot | בקצרה: כך מספרת… | המהדורה המקוצרת: כך מספרת… | terminology | 2 | The edition name is "המהדורה המקוצרת" everywhere else, and "בקצרה" is also the "In short" label. |
| 50 | T108 foot | כל ציטוט מדויק, מתוארך ובשפת המקור, ולצידו תרגום שלנו | כל ציטוט מדויק, מתוארך ובשפת המקור; לציטוטים בשפה זרה צורף תרגום שלנו | strength | 2 | This overclaims: the Hebrew quotes and the tooltip revision sentences have no translation. |
| 51 | T107 | כל ציטוט, עם תאריך ← | כל הציטוטים, מתוארכים ← | idiom | 1 | A tighter link label. |
| 52 | T61 he-mo (Arabic, now) | ״…ההרס והפגיעה, השיטתיים, המכוונים והמתמשכים, בעם הפלסטיני…״ | ״…ההרס והתקיפה, השיטתיים, המכוונים והמתמשכים, של העם הפלסטיני…״ | strength | 2 | "الاستهداف" is concrete targeting. "פגיעה" in Hebrew also covers "harm to rights", so it softens. See U6. |
| 53 | T61 he-mo (Arabic, then) | בביצוע פשעים של רצח עם | בביצוע פשעי רצח עם | grammar (סמיכות) | 1 | The construct state is the native form. |
| 54 | T26 c2H and T10 | ״ההרס של החברה הפלסטינית״ | ״הרס החברה הפלסטינית״ | grammar (סמיכות) | 1 | The construct state is tighter in a headline. The English "the" adds nothing. |
| 55 | T21 brKwF | כל מילה שהוסרה מאז ינואר 2021 מחוקה | כל מילה שהוסרה מאז ינואר 2021 מסומנת בקו מחיקה | idiom | 1 | "מחוקה" means deleted, which is not the same as struck through. |
| 56 | T27 / L2 | הקישו על סימון / קו לכל שינוי | הקישו על קו / קו לכל שינוי | terminology | 1 | One word for "tick". |
| 57 | T7 / T50 / L133 buttons | ▶ שוב | ▶ הפעלה חוזרת | terminology | 1 | Every other button uses the action noun (שמירה, הפעלת…, סגירה); "שוב" alone is an adverb. |
| 58 | T56 label vs hero | מתקפות 7 באוקטובר (T56, T104, L125) / 7 באוקטובר (T11, T35) | Article name: "מתקפות 7 באוקטובר" in every article label; "7 באוקטובר" only for the date or event | terminology | 1 | The same article has two names. |

Also noted, not counted (correct as is):
- "נ׳" in "דרום אפריקה נ׳ ישראל".
- "בית הדין הבין־לאומי לצדק" follows the Academy.
- The ktiv male is consistent throughout: לצידו, אידאולוגיה, מתואמות, ייתכן.
- "כ־2.4 שעות".
- The ↖ external-link mirror.
- The chart direction (time runs left to right).

## Verdicts on the unsure renderings (HE_TRANSLATION.md)

The file numbers 13 items. Item 13 holds two decisions, the project name and the edition name, so I rule on them separately as 13 and 14.

| # | Rendering | Verdict | Note |
|---|---|---|---|
| U1 | ״נלקחו כבני ערובה״ vs ״נלקחו כחטופים״ | **Keep ״נלקחו כבני ערובה״.** | It is exact, and it is a natural Hebrew news form. "חטופים" inside a quote would sharpen it. Our prose keeps "החטופים". The gap between the two is the point of card 3. |
| U2 | ״יישובים״ vs ״קהילות״ | **Keep ״יישובים״.** | "קהילות" is a calque. Kibbutzim and towns are יישובים. The strength is equal. |
| U3 | ״טבח בעל אופי של רצח עם״ | **Keep.** | "בעל אופי של רצח עם" is established legal Hebrew. "ג׳נוסיידי" would distance the reader. The length is acceptable in a quote. |
| U4 | ״חמוש״ for "militant" | **Keep the word, fix the bare adjective.** | Use ארגון ״חמוש״ in the hero row, as in the H2. Never "מיליטנטי" (it means aggressively activist). |
| U5 | ״מתזמרת את רצח העם בעזה״ | **Keep "מתזמרת".** | It is the idiomatic Hebrew for orchestrating something bad ("תזמר את המהלך"). "מנצחת על" carries a positive, leading sense and softens. |
| U6 | الاستهداف → ״הפגיעה״ | **Change to ״התקיפה״.** | "ההרס והתקיפה … של העם הפלסטיני". "פגיעה" softens (it also covers injury to rights). "סימון כמטרה" is too long for a running sentence. |
| U7 | "ha desencadenado" → ״שחולל״ | **Keep "שחולל".** | "חולל" is strong and idiomatic ("חולל טבח"). "הצית" is a fire metaphor and "שילח" is archaic. Fix the surrounding "מצד ישראל" → "בידי ישראל" and the fragment agreement (#9, #10). |
| U8 | Month abbreviations in charts (אוק׳…) | **Keep in ticks and chart labels only.** | Where space allows, use full names: the lane label "מאז 26 בספטמבר 2025", not "26 בספט׳". "7 באוק׳ 2023" is fine on the chart. |
| U9 | "Exploratory" → ״ראשוני״ | **Keep.** | "ניסיוני" suggests an experiment. "ראשוני" (preliminary) is what an Israeli desk would print on a chip. |
| U10 | ground invasion → הפלישה הקרקעית | **Keep.** | Kan, Ynet and Haaretz all used "הפלישה הקרקעית" for Gaza (Oct 2023) and Lebanon (Oct 2024). "התמרון" is IDF jargon and would soften our own event labels. |
| U11 | Quote marks ״…״ vs "…" | **Keep ״…״.** | It is typographically correct and clearly separates our text from the original “…”. The one collision, "לח״י״", is fixed by reordering (#20). It does not justify going back to ASCII. |
| U12 | Zionism today, "…ארץ ישראל ביהדות, שהיא עצמה מרכזית…" | **Change.** | "שהיא" can attach to היהדות (both are feminine). Proposed: "…החופף בקירוב את ארץ ישראל שביהדות, ארץ שהיא עצמה מרכזית בהיסטוריה היהודית." Also "תנועה לאומית־אתנית", with a maqaf. |
| U13 | Project name "סחף המסגור בוויקיפדיה" | **Keep.** | "סחף" captures drift exactly and has no political charge. |
| U14 | Edition name "המהדורה המקוצרת" | **Keep, and enforce it.** | "מהדורת הבזק" is a calque of "flash". The `<title>` still says "בקצרה:" (#49). Keep "בקצרה" only as the label of the closing paragraph. |

## Global house-style decisions

- **G1. Quote marks.**
  - Our translations use ״…״ (U+05F4). The originals use “…” and are never touched.
  - The full stop goes outside ״…״ when the quote is a fragment and inside when it is a whole sentence.
  - Where ״ the acronym mark (gershayim) would meet the closing ״, reorder the translation (#20).
- **G2. Dates.**
  - The format is "7 באוקטובר 2023" with a **no-break space** between the day and the month, done once in heD().
  - The prefix takes a maqaf: ב־, ל־, מ־.
  - Abbreviated months appear in charts only.
- **G3. Numbers.**
  - Use digits for counts and data.
  - In headlines and prose, spell out numbers up to ten: עשר עריכות, חמש טענות.
  - Never put two numbers in contact across a comma.
  - The "+N ימים" form is for charts; in prose write "N ימים אחרי…".
- **G4. A word that went in or out.**
  - On first mention in a paragraph write "המילה militant (״חמוש״)", or the Hebrew followed by the English in brackets, as the lanes already do.
  - The Hebrew alone implies the Hebrew word was in the English article.
  - The .he-o line under the paragraph stays as the evidence line.
- **G5. Fixed terms.** One term per concept, page-wide:
  - מונחים ביקורתיים (never שפה ביקורתית);
  - גרסה for a version (נוסח only for a wording);
  - בידי for agency (never מצד);
  - מתקפות 7 באוקטובר for the article name;
  - קו for a tick;
  - ויקיפדיה ב[שפה] for a language edition as an agent (never האנגלית / הפולנית).
- **G6. Names (נקב).** Write "נקב בשם/בשמות", never "נקב ב[צד/מי ש…]".
- **G7. UI register.** Buttons take an action noun (שמירה כתמונה, הפעלה חוזרת, סגירה). Instructions use the plural imperative (הקישו, גררו, החליקו). Do not mix the two within one control.
- **G8. No English in the Hebrew UI.**
  - Codes and leftovers are not acceptable: n/a, icj, court case only.
  - English is allowed only in the original quotes and the .he-o evidence lines.
  - Native-script language names go next to the Hebrew name, never instead of it.
- **G9. Typography.**
  - No italic and no letter-spacing in Hebrew.
  - Use weight or colour for the `.fl-next` bridges and the empty-lane notes.
- **G10. Locked lines.** Five proposals touch lines whose strength the build asserts: #30, #47, #13 (keeps "נעלמה"), and the denial wording ("מהווים" may stay; "עולים כדי" is the more legal alternative, same strength). None of them changes strength. They need the build's asserted strings updated together with the JSON.
