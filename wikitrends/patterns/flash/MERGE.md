# Flash edition, merge round: one bilingual page

**Build:** `cd wikitrends && python build_flash.py --bilingual OUT.html`. The single-language builds still work and still run every check: `python build_flash.py OUT.html` (English) and `python build_flash.py --lang he OUT.html` (Hebrew).

**Output:** `scratchpad/flash/merge/index.html` (it begins with `<!DOCTYPE html>`, then the charset meta and the viewport meta). Contact sheets: `scratchpad/flash/merge/contact_*.png`. Smoke logs: `smoke_r2.out` (core suite, both languages) and `smoke_bi_r2.out` (bilingual suite).

**The research edition is untouched.** `page_template.html` and `build_page.py` were not edited, so its output is byte-identical.

## Status per item

| # | Item | Status |
|---|---|---|
| 1 | One page with an עברית / English switch | Done |
| 2 | Fight lanes in Hebrew; the "land outside" label | Done (the gloss form; see below) |
| 3 | Exposure numbers in the reach section | Done |
| 4 | Treemap replacing the 150-tile grid | Done |
| 5 | Data lab tab | **Not done.** Blocked on data size; an owner decision is needed (see below) |
| 6 | Morph-slide inspection | Done |
| 7 | English "In short" fix | Done |

**Commits on `wiki-framing-research`:**
- `f30f6f5`: items 1, 2, 3 and 7.
- `9115261`: items 4 and 6.
- The next commit: this file.

Items 4 and 6 touch the same files and functions (`flDraw`, the carousel), so they went into one commit.

**How the first commit was checked:** the state it commits was rebuilt, and the output was compared with the smoke-tested build `index_r1.html`. They are byte-identical (`cmp`). That build passed the core suite (944 pass, 0 fail) and the bilingual suite (268 pass, 0 fail).

## 1. One page, two languages (`flash_bi.py`)

**How it is built:**
- Both language pages are built exactly as before, and every English and Hebrew assertion runs.
- `flash_bi.py` then packs them into one document:
  - each language's markup and CSS sit in a `<template>`;
  - each language's script (the research library, the flash script and, for Hebrew, the overlay) is wrapped in its own function, so the two languages share no variables;
  - the data `R` is in the file once.
- Hebrew starts from a `structuredClone` of the data, because its overlay relabels the grid's column names in place.

**How a switch works:**
- On the first switch, a language is mounted from its template.
- After that, both languages stay in memory, and switching moves their nodes in and out of the document, with no reload.
- The hidden language's window-level and document-level listeners are muted.
- Its queries go to its own detached nodes, so a late timer can never write English into the Hebrew page, or the reverse.
- The returning language runs `flRedraw()`, the same redraw a resize triggers. This re-renders the canvases, the fight lanes, the grid and the morph slides.
- The share images are drawn on demand by the active language's own `shSpec`/`shCard`, so they come out in that language.

**What a switch sets:**
- `<html lang dir>`, `document.title` and the description meta.
- The scroll position: the switch finds the smallest element with an id that spans the top of the viewport, then puts the same fraction of the same element back at the top. This is re-applied after layout settles, unless the reader scrolls in the meantime.

**How the language is chosen, in this order:**
1. `?lang=he|en`
2. `#lang=he|en`
3. The reader's last choice (`localStorage`, wrapped in try/catch)
4. `navigator.language`: `he*` or `iw*` opens Hebrew; anything else opens English

**The switch itself:**
- It sits in the masthead.
- It is a real button group: `role="group"` with a label in the page language, and `aria-pressed` on each button.
- **Deviation:** a floating copy of the switch appears at the bottom inline-end corner once the masthead has scrolled away. Without it, a reader in the middle of the page could not switch without scrolling to the top, and "keep the scroll position" would never apply. It has no transition under reduced motion and is hidden in print.
- Focus stays on the switch after a switch.

**Equality with the single-language builds:**
- The smoke suite renders the single-language builds and the bilingual page in both modes and compares the full `innerText` with the switch removed.
- English mode equals the English build, and Hebrew mode equals the Hebrew build.

**A bug found and fixed on the way:**
- The build comment at the top of `page_flash_template.html` mentioned the `/*RESEARCH_JS*/` and `/*RESEARCH_CSS*/` slots by name, so the build pasted a second copy of the whole library and data into the comment.
- The English page drops from 2.04 MB to 1.08 MB.
- `build_flash.py` now asserts that the data and the CSS each appear once.

**The Hebrew build at HEAD was broken.** The trail and fight-lane commits (`2d7e633`, `d89afc0`) changed `SHEET_T` and added untranslated chrome, so `--lang he` failed. Fixing that was a precondition for item 1; it is part of item 2.

## 2. Fight lanes in Hebrew

**What the reader sees:**
- Each lane label stays the original English phrase, left to right, in its curly quotes (`<text lang="en">`).
- Our Hebrew translation of the phrase sits at the other end of the same row.
- The legend, header, tooltips, aria labels and the full word-trail sheet ("כל מילה שנכנסה ויצאה") are in Hebrew. The trail's sentence box stays English, left to right.
- The trail sheet no longer shows the "English only" note.

**Checks:**
- The page logs a console error if a lane has no Hebrew translation, and the smoke test requires 0 console errors.
- The smoke test's independent recount of every lane still passes in Hebrew, at rest and at three sweep dates.

**"land outside": the longer label does not hold.** We checked this against the stored Zionism first sentences (the ratchet variants and the sweep):
- 26 sweep steps read "a land outside of Europe";
- 20 read "a land outside Europe".
- So "a land outside of Europe" does not hold for every lane interval, and the lane keeps "land outside" with a muted gloss.

**Small deviation in the gloss:** the gloss reads **"(of) Europe"** rather than "(of Europe)", because the "of" is missing in 20 of the steps.
- The build asserts that every stored wording containing "land outside" continues "(of )Europe", and that both variants occur.
- The page checks the same thing again at load.

## 3. Exposure numbers (reach section)

**The figure:** the section heading is now "How many page views met the new wording". It shows the six hero articles from `exposure.json`.

| Article | Views (daily sums) | Share that met the critical wording |
|---|---|---|
| Israel | 5.1M | 100% |
| Zionism | 2.1M | 99.9% |
| October 7 attacks | 2.0M | 100% |
| Gaza genocide | 1.7M | 99.3% |
| Hamas | 1.5M | 95.1% |
| Nakba | 0.6M | 30.3% |

- Each bar's length is the article's views.
- The dark part of each bar is the share of those views that met the critical wording.
- A collapsed "What counts as the critical wording" names each article's wording. It includes Israel's 92.6% for "began committing genocide" and Nakba's 69.7% that met another "ethnic cleansing" wording.

**The surge line:** "From 7 Oct to 31 Dec 2023 most views met the older wording (Israel, 9.3 million views, 99.1% with no genocide charge; Hamas, 10.2 million, none with "political organisation"); in the past 12 months nearly every view met the new wording, except Nakba's "by Zionists"."

**The caveat** is kept: "Page views, not unique readers: one person can count many times."

**Checks:**
- Every row and number is rebuilt from `exposure.json` in `build_flash.py`, and the build fails on any drift.
- "Nearly every view … except Nakba" is asserted: five articles are at or above 95%, and Nakba is below 50%.

**Deviations:**
- **The period is 9 Nov 2025 – 8 Nov 2026, not 10 Nov.** `exposure.json` says `from: 20251109` (365 days). `EXPOSURE.md`'s "10 Nov" is a typo in that file.
- **Benjamin Netanyahu and Palestine leave the bars.** `exposure.json` does not cover them, and the brief asked for one source.
  - This also removes the old top bar (Netanyahu, 7.0M). `spin_review.md` R3 advised against dropping it for appearances.
  - It is dropped here only because of the single-source rule; the owner may want it back from the crawl, labelled separately.
- The heading changed from "most-read pages … gained critical vocabulary" to "How many page views met the new wording". The build assertion was updated to match.

## 4. Treemap

> **Superseded (fix log 4, `HE_FIXLOG4.md` §1):** the owner found the treemap unreadable on an iPhone. It is replaced by one 100% bar of the same 150 openings' views (the seven charged segments coloured, the other 143 grey) and a list of the seven with views and voice. The set, the views, the 7 / 2 and the 12.4% below are unchanged and still asserted.

**The set:** the same 150 opening sections as PERP.md: the 150 most-viewed topic-group articles of the mass crawl that have a lead at all three dates.
- The build rebuilds the set and checks it against `perp_codes.jsonl`.
- It also checks Israel's 42,920,851 views since 2021, the figure PERP.md gives.

**Tile area:**
- Area is the views in the last 12 stored months, **Nov 2025 – Oct 2026**, from the monthly sums in `data/mass2.json`.
- **Fallback, stated on the page:** `exposure.json` has daily views for only the six hero articles, so the treemap uses the crawl's monthly sums. The key says "monthly sums from our crawl".

**The charge per tile:**
- It comes from `perp_codes.jsonl`: a sentence that charges Israel with genocide, in Wikipedia's own voice or attributed, never the denial.
- The build asserts 7 such sentences now, 2 of them in Wikipedia's own voice (Israel, Netanyahu), and none in Jan 2021 or Jul 2023.
- Each sentence is checked against the stored lead.

**The headline, computed:** "Now 7 of 150 do, two as fact, and they got 12% of the views of all 150 (Nov 2025 – Oct 2026)."
- The exact share is 12.4%.
- This is merged into the existing caption to save height.

**What the reader can do:**
- Colours are as before: dim (no charge), outlined (attributed), solid teal (stated as fact).
- The large tiles are labelled with the English article titles.
- Tapping a tile shows the article, its views, its voice and, for the seven, the exact sentence. In Hebrew, the sentence is followed by our translation.
- The Jan 2021 / Jul 2023 / Now switch is a `.seg` button group with `aria-pressed`.
- On view the treemap plays Jan 2021, then Jul 2023, then Now, lighting the five attributed tiles and then the two stated as fact, one at a time (about 5 s).
- A touch hands control to the reader. Under reduced motion it shows the final state at once.

**Checks:**
- The smoke test compares each of the 40 largest tiles' area with its share of the stored views.
- It checks the three states and the tap.

**Share image:** no treemap share image was added. The four existing cards are unchanged.

## 5. Data lab tab: not done (decision needed)

The lab (`wikitrends/lab/`) reads the research edition's full data:
- `R.mass` is about 3.7 MB;
- `R.articles` is about 5.4 MB;
- with `ratchet`, `crosslang` and the rest, the lab needs about 10 MB.

Inlining that makes the flash page about 12 MB instead of 1.8 MB, which is wrong for a phone-first page. The artifact sandbox also cannot fetch the research artifact's data at run time.

**Options for the owner:**
- **(a)** Accept a heavy page, with the lab data as an inert JSON block parsed only when the tab opens.
- **(b)** Cut a lab data slice down to the views the flash links to (the definition flipbook and the language prism). This needs lab.js changes and is no longer "as is".
- **(c)** Keep the "Full research" link to the research edition's own Data lab tab.

The flash's "Every change" buttons keep opening the play sheet.

## 6. Morph slides (Arabic, Spanish)

**Controls:**
- **Then · Now · Both**, a segmented button group with `aria-pressed`.
- **A scrub slider** from then to now. Part-way, the removed words fade out and the added words fade in, in reading order.
- **Both** shows then above and now below, with the English rendering for each. The slide grows only while Both is on, because the reader chose it.

**Tap or focus a marked phrase:**
- An added phrase shows what it replaced.
- A removed phrase shows what replaced it.
- A changed word shows old → new.
- Each comes with the English rendering of the marked term.

**The gloss chip is gone from the Arabic right-to-left line.** The English glosses ("the genocide", …) now live only in those tooltips.

**Hebrew:** our translation follows the state on screen (Then, Now, or the scrub position). Both shows both translations.
- **Deviation from HE_FIXLOG BT #6:** the proofreaders chose "both translations always visible, the inactive one dimmed". The owner's later brief says the rendering follows the state, so this follows the brief.
- The smoke test checks it.

**Carousel empty space:**
- The carousel is still sized to its tallest slide.
- The Hebrew Spanish slide was the outlier (605 px against 218–503 px), because it always showed both translations.
- With the translation following the state it is now 566 px, and the hidden "Both" box no longer reserves space.
- The content stays vertically centred in the slide.

## 7. "In short"

The English now reads: "…that Israel "began committing genocide"; the Zionism article calls Zionism "a Jewish homeland through colonization"; and, in every copy we hold, …".
- The quotes are unchanged.
- The Hebrew pair's English key was updated in the same commit. The Hebrew text already carried the fix.

## Phone length (390×844, fonts loaded, every lazy piece drawn)

| Build | English | Hebrew |
|---|---|---|
| Before (trail2 / he2 smoke) | 10.22 | 10.77 (without the fight lanes) |
| Items 1–3, 7 (`index_r1`) | 10.54 | 11.56 |
| **Final (`index.html`)** | **10.85** (1280: 10.38) | **11.78** (1280: 11.32) |

**English meets the ≤11 target. Hebrew does not.**
- The Hebrew page was already 11.27 once the fight lanes went in, before any merge-round content.
- The merge round adds the reach key and surge line, the treemap (about 0.3 screens) and the morph controls (about 0.06).
- Cuts made to hold the length:
  - the critical-wording key is collapsed;
  - the surge line was shortened to Israel and Hamas;
  - the treemap's headline was merged into its caption;
  - the treemap is 215 px tall on phones.
- Bringing Hebrew to 11 needs an editorial cut of about 0.7 screens, which would need proofreading. Candidates:
  - card 5 (1.60 screens in Hebrew, against 1.31 in English);
  - the hero stack's translation lines;
  - the surge line, moved into the collapsed key.

## Smoke tests

**The suite:**
- `scratchpad/flash/merge/smoke_core.js` merges the trail2 (English) and he2 (Hebrew) suites into one, parameterised by language.
- It runs on iPhone 13 and 1280, light and dark, plus reduced motion, in both languages, and adds the treemap and morph checks.
- `scratchpad/flash/merge/smoke_bi.js` holds the bilingual checks:
  - text equality with the single-language builds;
  - default language from `navigator.language` (he-IL, he, en-US, fr-FR, ar);
  - remembered choice, `?lang=` and `#lang=` precedence, blocked `localStorage`;
  - switching both ways mid-page at #c2, #c5 and #close, with lang/dir, the scroll anchor within 80 px, focus, no overflow, labels redrawn in the new language and share images in the active language, on phone and 1280, light and dark, plus reduced motion.

**Results on the final build (`index.html`):**
- Core suite (`smoke_r3.out`): **1044 pass, 0 fail**, across 5 configurations × 2 languages. That includes 0 console errors or warnings and 0 horizontal overflow, at rest and after interaction.
- Bilingual suite (`smoke_bi_r2.out`): **268 pass, 0 fail**.
- Both logs are combined in `smoke_result.txt`.

## New Hebrew strings for proofreading

The quotes inside `“…”` are originals; please do not touch them.

### The switch (`flash_bi.py`)

- Group label: «שפה». Buttons: «עברית» / «English».

### Fight lanes (`flash_i18n_he.json`, template)

**Legend:**
- «במשפט, נוסף מאז 2021»
- «במשפט, כמו בינואר 2021»
- «לא במשפט, אף שהיה בו בינואר 2021»
- «שינוי אחד»
- «⇄ n = הוסר או הוחזר n פעמים · הקישו על שורה כדי לראות את התאריכים»

**Button:** «כל מילה שנכנסה ויצאה ←»

**Header:** «<b>N מילים שנאבקו עליהן</b> מאז ינואר 2021 · N הביטויים שנאבקו עליהם יותר מכול»

**Tooltip:**
- «בינואר 2021: במשפט» / «בינואר 2021: לא במשפט»
- «כניסה ב־…» / «יציאה ב־…»
- «(שינויים: N; האחרון ב־…)»
- «, עדיין בלי שינוי»

**Lane aria:** «… (תרגום): שינויים: N; הצגת התאריכים» / «שינויים עד …: N»

**SVG aria:** «N הביטויים שנאבקו עליהם יותר מכול במשפט הראשון של הערך על הציונות, מ־2021 עד היום: מתי כל אחד מהם היה במשפט, וכל שינוי»

**Lane translations (`flash_he_overlay.html`, `FB_HE`):**

| English | Hebrew |
|---|---|
| colonization | קולוניזציה |
| land outside (of) Europe | ארץ מחוץ לאירופה |
| Palestine, a region | פלסטין, אזור |
| Land of Israel | ארץ ישראל |
| Jewish history | ההיסטוריה היהודית |
| homeland | מולדת |
| Jewish people | העם היהודי |
| Jewish state | מדינה יהודית |

### The word trail (play sheet)

**Range aria:** «מעבר בזמן: כל מילה שהייתה אי־פעם במשפט הראשון, כפי שעמד באותו יום»

**Key:** «כל מילה שהייתה במשפט הראשון של הערך על הציונות מאז ינואר 2021; שום מילה לא נעלמת מהשובל: מחוק בכתום מילה שהוסרה מאז ינואר 2021, כחול מילה שנוספה, במסגרת מקווקוות מילה שנוספה ואחר כך הוסרה; ⇄ n = הוסרה או הוחזרה n פעמים; +n מילים שהיו במשפט פחות משעה, הקישו כדי להציג. מילות המפתח מודגשות.»

**Meta line:**
- «נוסח שבוטל · בתוקף מ־… עד …»
- «נוסח N מתוך N, בתוקף עד … / בתוקף כעת»
- «· N מילים הוסרו ו־N נוספו מאז … · N מילים נכנסו ויצאו · N מילים שנאבקו עליהן»

**Screen-reader prefixes:** «הוסרה: », «נוספה: », «נוספה ואחר כך הוסרה: »

**Chips:**
- «קיפול המילים שהיו במשפט פחות משעה»
- «מילים נוספות: N, כל אחת הייתה במשפט פחות משעה בסך הכול; הצגתן»

**Marker aria:** «הוסרה או הוחזרה N פעמים; הצגת התאריכים»

**Tooltip extra:** «· המילה שהשתנתה הכי הרבה כאן: …»

**Sheet title:** «ציונות: כל מילה שנכנסה ויצאה»

### Reach section

**Heading:** «כמה מהצפיות הציגו את הנוסח החדש»

**Lead:** «צפיות בדף בשישת הערכים שלמעלה, 9 בנובמבר 2025 – 8 בנובמבר 2026 (סכום של צפיות יומיות). החלק הכהה של כל פס, והאחוז, הם חלק הצפיות שהציגו את הנוסח הביקורתי:»

**Rows:** «N מיליון · N%», with the article names ישראל, ציונות, מתקפת 7 באוקטובר, רצח העם בעזה, חמאס, נכבה.

**Key:**
- Summary: «מה נחשב לנוסח הביקורתי»
- Text: «ישראל, “genocide” (רצח עם) בפתיח הערך (92.6% הציגו את “began committing genocide”, החלה לבצע רצח עם); ציונות, “colonization” (קולוניזציה) במשפט הראשון; מתקפת 7 באוקטובר, “armed incursions” (חדירות חמושות); רצח העם בעזה, רצח עם בקולה של ויקיפדיה; חמאס, “political organisation with a military wing” (ארגון פוליטי בעל זרוע צבאית); נכבה, “ethnic cleansing … by Zionists” (טיהור אתני … בידי ציונים; 69.7% האחרים הציגו נוסח אחר של “ethnic cleansing”, טיהור אתני).»

**Surge:** «<b>גל הצפיות.</b> מ־7 באוקטובר עד 31 בדצמבר 2023 רוב הצפיות הציגו את הנוסח הישן (ישראל, 9.3 מיליון צפיות, 99.1% מהן בלי האשמה ברצח עם; חמאס, 10.2 מיליון, ואף אחת מהן לא הציגה את “political organisation”, ארגון פוליטי); ב־12 החודשים האחרונים כמעט כל צפייה הציגה את הנוסח החדש, חוץ מ־“by Zionists” (בידי ציונים) בערך על הנכבה.»

**Caveat:** «צפיות בדף, לא קוראים ייחודיים: אדם אחד יכול להיספר פעמים רבות.»

**Unsure:** "met" is rendered «הציגו» (the views displayed the wording). «נתקלו ב־» was the alternative.

### Treemap

**Caption:** «… <b>היום 7 מתוך 150 מאשימים</b>, שניים מהם כעובדה, והם קיבלו <b>12%</b> מהצפיות בכל 150 הערכים (נובמבר 2025 – אוקטובר 2026).»

**Switch:**
- Labels: «ינואר 2021» / «יולי 2023» / «היום»
- Aria: «הצגת הפתיחים נכון ל־»

**Aria:** «150 אריחים, אחד לכל פתיח ערך מהנקראים ביותר, בגודל לפי מספר הצפיות. …»

**Key:** «השטח = צפיות בדף, נובמבר 2025 – אוקטובר 2026 (סכומים חודשיים מהסריקה שלנו) · הקישו על אריח»

**Tooltip:**
- «N מיליון צפיות» / «N,000 צפיות»
- «אין האשמה ברצח עם בפתיח הערך» / «ההאשמה, מיוחסת לאחרים» / «נקבע כעובדה, בקולה של ויקיפדיה»
- «בינואר 2021 וביולי 2023: אין האשמה»

**The seven charge sentences, our translations (`HE_TM`).** These are new, except Netanyahu, which is the page's existing rendering. Please check each against its English original in the tooltip:

| Article | Our translation |
|---|---|
| Israel | «אחרי המתקפות בהובלת חמאס ב־7 באוקטובר, ישראל החלה לבצע רצח עם נגד פלסטינים בעזה.» The full sentence; the page previously had only the fragment. "Hamas-led October 7 attacks" is rendered «המתקפות בהובלת חמאס ב־7 באוקטובר», to keep the plural without the vetoed «מתקפות 7 באוקטובר». |
| Benjamin Netanyahu | The existing rendering. |
| Palestine | «בעקבות המתקפות של חמאס בישראל ב־7 באוקטובר 2023, שבהן נהרגו 1195 בני אדם, פתחה ישראל במבצע צבאי רחב היקף בעזה, שבו נהרגו יותר מ־72,000 פלסטינים, ושגרם לעקירה המונית של האוכלוסייה, למשבר הומניטרי ולרעב ברצועת עזה; המעשים האלה הוכרו כרצח עם נגד העם הפלסטיני בידי קונצנזוס מחקרי הולך וגדל.» |
| Gaza Strip | «פעולות אלה תוארו בידי חוקרים, מומחים למשפט בין־לאומי וארגוני זכויות אדם כרצח עם נגד העם הפלסטיני.» |
| Israeli–Palestinian conflict | «פעולותיה של ישראל בעזה במלחמה הזאת תוארו בידי מומחים למשפט בין־לאומי, חוקרי רצח עם וארגוני זכויות אדם כרצח עם.» |
| Israel Defense Forces | «פעולותיו ומדיניותו של צה״ל בשטחים הפלסטיניים ספגו ביקורת נרחבת, עם האשמות בדיכוי, באפליה ממוסדת, בהרג שלא כדין ובפגיעה שיטתית בזכויות הפלסטינים, וארגוני זכויות אדם וחוקרים רבים מאשימים את צה״ל ברצח עם.» "systematic abuses" is rendered «פגיעה שיטתית». **Unsure:** «הפרות שיטתיות» is the alternative. |
| Gaza–Israel conflict | «מקורות מחקריים וארגונים בין־לאומיים רבים הגיעו למסקנה שפעולותיה של ישראל בעזה מהוות רצח עם.» |

### Morph controls (`MO_T`)

| Key | Hebrew |
|---|---|
| Then / Now / Both | «אז» / «היום» / «שניהם» |
| Group | «הצגת המשפט» |
| Slider | «גררו מאז ועד היום» |
| Added | «נוסף» |
| Removed | «הוסר» |
| in place of | «במקום» |
| replaced by | «והוחלף ב־» |
| Changed | «שונה» |
| In English: | «באנגלית:» |
| nothing was removed here | «כאן לא הוסר דבר» |

The vetoed v1 wordings (`HE_VETO`) are asserted absent across all of these.

## Open items

1. Data lab tab: the owner decides between options (a), (b) and (c) above.
2. Hebrew length: 11.78 screens, 0.78 over the target; this needs an editorial cut, then proofreading.
3. The Netanyahu and Palestine view bars were dropped by the single-source rule (spin_review R3): the owner should confirm.
4. Proofread the new Hebrew strings above, especially the five new charge-sentence translations and «הציגו».
5. The treemap has no share-image variant.
6. Tile labels on the treemap are English article titles in both languages. These are the data. Hebrew names for the largest tiles would be a small addition.

## Final round (after this file): status of the open items

| # | Open item above | Final round |
|---|---|---|
| 1 | Data lab tab | Done. The owner chose a slim lab: flipbook and language prism, the flash's articles only, lazy. See `lab/lab_flash.py`. The other five views say "not in this edition" and link to the research lab. |
| 2 | Hebrew length | 10.98 phone screens, measured by the smoke test (English 10.84). See `HE_FIXLOG2.md` §5 and the layout notes there. |
| 3 | Netanyahu and Palestine bars | Back in the reach section, from the same daily-views source (run 42704500939). Their critical wording is "genocide" in the opening section. See `EXPOSURE.md`, "Run 2". |
| 4 | Proofread the new Hebrew strings | Done in `HE_FIXLOG2.md`. «הציגו» became the passive «הוצג». Three charge sentences were corrected. The fight-lane translations were clipped on phones; that is fixed. |
| 5 | Treemap share image | Still open. |
| 6 | Hebrew tile labels | Still open. They are data, so they stay English. |

All new numbers were recomputed from the raw sources in `FACTCHECK_merge.md`; nothing was wrong.

## Fix log 3 (owner requests, after the final round)

1. Hebrew "armed incursions" is «פשיטות חמושות» everywhere; «חדירות» is vetoed (`HE_FIXLOG3.md` §1).
2. Card 3's hostages moment, both languages, with its share image (`HE_FIXLOG3.md` §2). Facts in `FACTCHECK_hostages.md`: the October 7 first sentence names no hostages in 9 of the 10 editions we hold (Italian does; Hebrew did in our Oct 2024 – Oct 2025 copies); all ten opening sections mention them. The old "Israel and Hamas … in every copy we hold" line overstated (our April and July 2024 English Hamas copies said "taking hostages back to Gaza"), and is corrected. **The research edition still carries the four-snapshot wording; the owner decides.**
3. Smoke: core 1193/0, bilingual 308/0, lab 185/0; phone screens English 10.85, Hebrew 10.99 (`HE_FIXLOG3.md` §4).
