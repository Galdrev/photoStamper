# Flash edition: fix log 5 (Elsewhere on Wikipedia, card 7: the editor-trail visual and the outside-articles carousel)

**Build:** `cd wikitrends && python build_flash.py --bilingual OUT.html`. The single-language builds still run every check. The research edition is untouched: `page_template.html` and `build_page.py` were not edited, and its build output is byte-identical to the build before this change (`cmp`).

**Sources (aggregates only):**
- `patterns/trail/cards.md` and `results.json` (editor-trail run 42778075792);
- `patterns/trail/articles.md` (monthly views);
- `patterns/trail/VERIFIED.md` and `verified.json`, which hold the hand verification of 14 candidates (runs 42847367759 and 42848274633): 4 KEEP and 10 DROP.

**Standards:**
- `HE_PROOF_1.md`: idiom, grammar, RTL, punctuation, no italic, a no-break space in dates, no English in the UI.
- `HE_PROOF_2.md`: fidelity of agency, modality and attribution; no sharpening, no softening.
- `messaging_check.md`, `spin_review.md`, `qa/MUSTFIX_owner.md`: no courts framing, no editor names, aggregates only.

## 1. What was added (both languages)

**Card 7, "Elsewhere on Wikipedia"** (`section#cel`, between card 6 "How it got there" and the arbitrators' card, now 8):

1. **H2.** "The most active editors of these articles each pushed their usual way in a median of 11.5 articles; comparable editors elsewhere, in 2."

2. **The pattern visual** (`figure#flEt`), two rows:
   - "Most active editors, core Israel articles · median 11.5"
   - "Most active editors, comparison articles (other conflicts, countries) · median 2"
   - Each row is a binned bar strip of the published distribution (accounts per range: 0, 1, 2, 3–4, 5–9, 10–19, 20–49, 50+). The suppressed cells are drawn as a dotted stub labelled <3. The median is marked.
   - Beside each strip is the count of outside articles that 3 or more of that group moved: **53** against **5**.
   - Nothing is per account.

3. **The honesty line, visible:** "Consistent with a sustained push across many articles; it does not show coordination. After a revert, these editors made the same change again less often than the comparison group (34% vs 67%)."

4. **The carousel** (`#car3`, "Four outside articles, 2021 → now"). Each slide shows:
   - the article and its monthly views ("7.9k views a month");
   - the then and now key phrases, exact, with the page's `<del>` / `<ins>` diff marks;
   - the date of each key phrase and its scope (moved / still in paragraph 2).

   | Slide | Then | Now |
   |---|---|---|
   | **Criticism of Israel** | Jan 2021 sentence 2: “relating to a variety of topics, <del>both historical and contemporary</del>” | first sentence: “relating to <ins>Zionist political violence</ins> … <ins>human rights violations related to the Nakba and the Israeli occupation</ins>” (since 1 Jul 2025 / 31 Dec 2025 / 14 Oct 2026; renamed Jul 2023) |
   | **Palestinian political violence** | “acts of violence <del>or terror</del> motivated by Palestinian nationalism” | “As Palestinians have not had a fully recognized state with a regular army” … “has taken the form of <ins>insurgency</ins>” (since 10 Dec 2025; paragraph 2 still says “are considered terrorist organizations”) |
   | **Plan Dalet** | “a plan <del>worked out by the Haganah</del> … in March 1948” | “a <ins>Zionist military plan</ins> executed during the 1948 Palestine war <ins>for the conquest of territory</ins>” (since 4 Jun 2023, before the war; the Nakba in sentence 2 since 14 Aug 2024) |
   | **Causes of the 1948 Palestinian expulsion and flight** | sentence 2: “a matter of <del>great controversy among historians</del> …” | “a matter of dispute, though <ins>today most scholars consider that the majority of Palestinians were directly expelled</ins> or else fled due to fear” (since 15 Aug 2024; “by Israeli forces” moved to sentence 3) |

5. **The shared line under the carousel.** It is the summary of a disclosure: "All four are among the 53 outside articles above (comparison editors: 5). We counted accounts, not authors: we did not check who wrote these lines. *How we counted ▾*". The disclosure holds:
   - the definitions of both groups;
   - the usual way: of the 39 with 10+ such edits, 25 mostly added and 14 mostly removed critical terms;
   - the bins and the <3 suppression;
   - the outside-article rule;
   - the re-insertion numbers (57 of 166; 44 of 66);
   - the views definition;
   - "We read 14 … these 4 hold up, and 10 were dropped";
   - "No account is named or labelled" and "Concentrated interest is not by itself evidence of bad faith".

## 2. Deviations from the brief (and why)

- **The shared line.** The brief proposed: "The same group of the most active editors of the core articles made these changes, among 53 outside articles they pushed the same way."
  - The trail data hold no per-edit authorship. "Made these changes" (the quoted lines) would therefore be a claim we did not check, and it comes close to implying who wrote what.
  - The page says instead that the four articles are among the 53, and "We counted accounts, not authors: we did not check who wrote these lines."
- **The cards.** Only one of the brief's candidates 1–7 holds up: Criticism of Israel (VERIFIED.md). The other three cards come from the same discovery list, read the same way.
  - Dropped from the brief's list: Comparisons… (a rename from Holocaust inversion), Genocide and Settler colonialism (word-list artefacts), Sheikh Jarrah and Gaza genocide recognition (2021/2025 creations, attributed, court-centric), Samaritans (no critical change).
- **Placement.** Card 7 sits before the arbitrators' card, not after it.
  - The arbitrators' card ends "nor tie either finding to the edits above", which now covers card 7 too.
  - Placing the editor trail after "outside actors heavily invested" would invite the reading "those actors = these editors" (spin_review H5 and R7).
- **Headline verb.** "Each pushed their usual way": the metric is per account, in its own majority direction. 25 of 39 mostly added critical terms and 14 mostly removed them, which is stated in the disclosure. The brief's "pushed the same way" would read as one shared direction.
- **Re-insertion.** 34% vs 67% is the pooled rate (57/166 vs 44/66). The per-account means (34%, 66%) round the same way for the topic group.

## 3. Length budget (phone, 390×844, fonts loaded)

Card 7 adds about 750 px in English and about 800 px in Hebrew. To stay within 11.0 screens, nothing factual was cut. Three items were collapsed, one duplicate visual was removed, and spacing was tightened:

- **Card 6:** the weekly chart (chips and `#kChart`) moved behind a disclosure, "The weekly chart, battle by battle".
  - Its caption with the facts (13.7 vs 3.8 a week; "Timing gives a date, not a cause") stays visible.
  - The chart is built on the first open and redrawn on each later one.
- **Card 4:** "Its terror designation moved from sentence 5 to sentence 22" is now the summary of a disclosure that holds the two dated rows and quotes.
- **Card 8 (arbitrators):** the 89–100% meter graphic is gone. It drew exactly the numbers of the line under it ("four groups of 3 to 6 accounts voted together 89 to 100% of the time, against about half by chance"), which stays.
- **The transition line** "Wikipedia’s arbitrators have ruled on conduct in this topic." was dropped. It was a transition, not a fact; the arbitrators' card follows directly.
- **Phone spacing between and inside cards:** margin 16 → 12 px, padding 9 → 8 px, gap 7 → 5 px (Hebrew 4 px).
- **The Hebrew slides** give our translation first and the English original in the small `he-o` line under it, the pattern the Hebrew H2s already use. Every translation is still marked "תרגום שלנו".

**Smoke-run values** (bilingual page, iPhone 13 390×844, fonts loaded):

| Mode | English | Hebrew |
|---|---|---|
| Phone, light / dark | 10.94 | 10.97 |
| Phone, reduced motion | 10.92 | 10.96 |
| 1280 (no cap) | 10.67 | 11.42 |

The cap is 11.0 on the phone.

## 4. Hebrew proof of the new strings

Two passes, as in HE_PROOF_1 (idiom, RTL, typography) and HE_PROOF_2 (fidelity). What is inside “…” is evidence and was not touched. Each ״…״ was checked against its original.

| # | String | First draft | Final | Lens | Sev | Reason |
|---|---|---|---|---|---|---|
| 1 | "outside articles" (row numbers, carousel title, shared line, disclosure) | ערכים **מחוץ לנושא** | ערכים **מחוץ למדגם** | fidelity | 3 | מחוץ לנושא means "off-topic". Criticism of Israel and Plan Dalet are on the subject; they are only outside our sample of scoped articles. The build now asserts that "מחוץ לנושא" is absent from card 7. |
| 2 | H2, "each pushed their usual way" | — | דחפו, כל אחד לכיוון הרגיל שלו | fidelity | — | Keeps "each" and "usual", so the line does not read as one shared direction. "In a median of 11.5 articles" = בחציון של 11.5 ערכים. |
| 3 | "it does not show coordination" | — | הוא אינו מראה תיאום | fidelity | — | Not "אינו מעריך" (the scope-line trap, HE_PROOF_2 #1). "Consistent with" = עולה בקנה אחד עם, the page's standard rendering. |
| 4 | "After a revert" | אחרי שעריכה שלהם בוטלה | אחרי ביטול | idiom / length | 1 | The English is just as terse; "ביטול" is the page's word for revert (״כל הסרה בוטלה״). The disclosure spells out the metric. |
| 5 | "insurgency" | — | התקוממות | fidelity | — | Not התקוממות מזוינת and not טרור: that would sharpen or reverse the sentence. The verb agrees with the elided אלימות (לבשה). |
| 6 | "terrorist organizations" | — | ארגוני טרור | fidelity | — | Consistent with ״ארגון טרור״ in card 4. "Several groups" = כמה מהקבוצות, feminine plural with נחשבות. |
| 7 | "human rights violations" | — | הפרות של זכויות אדם | fidelity | — | הפרות, not פגיעה (the fix-log-2 rule; HE_VETO has "ובפגיעה שיטתית"). |
| 8 | "Mandatory Palestine" (Plan Dalet, the then quote; later shortened) | פלשתינה המנדטורית | ארץ ישראל המנדטורית, then cut with … | terminology | 2 | ארץ ישראל המנדטורית is the standard Israeli rendering of the English term. The final quote ends "… in March 1948", so the term no longer appears. |
| 9 | "the 1948 Palestine war" | — | מלחמת 1948 | fidelity | — | Neither "מלחמת העצמאות" (an Israeli framing that is not in the source) nor a calque "מלחמת פלסטין". The page already uses "1948" this way. |
| 10 | "a plan worked out by the Haganah" | — | תוכנית שגיבשה ההגנה | fidelity | — | "Worked out" = גיבשה (drafted), not "הוציאה לפועל" (executed), which belongs to the now sentence. |
| 11 | "known as the Nakba" | — | הידועים בשם הנכבה | grammar | — | Agrees with the two nouns, גירוש ובריחה (plural). |
| 12 | "directly expelled or else fled due to fear" | — | גורשו במישרין או שברחו מפחד | fidelity | — | Both halves kept. Dropping "or fled" would sharpen the claim; it was considered for length and rejected. |
| 13 | Causes, the article title | הסיבות לגירוש ולבריחה של הפלסטינים ב־1948 | סיבות הגירוש והבריחה של הפלסטינים ב־1948 | idiom | 1 | Construct state; shorter. The same words as the page's ״הגירוש והבריחה של הפלסטינים ב־1948״. |
| 14 | "The first sentence since 1 Jul 2025" | משפט ראשון מאז | המשפט הפותח מאז | idiom | 2 | "משפט ראשון מאז" reads as a fragment. |
| 15 | "Title until Jul 2023: Criticism of the Israeli government" | — | עד יולי 2023 שם הערך היה ״ביקורת על ממשלת ישראל״ (Criticism of the Israeli government) | RTL | 2 | The English title is wrapped in `lang="en" dir="ltr"` (HE_PROOF_1, English in the UI). |
| 16 | Row labels | העורכים הפעילים ביותר, ערכי הליבה על ישראל | הפעילים ביותר בערכי הליבה על ישראל | idiom / length | 1 | One line on a phone. A chart label may omit the noun; the H2 above names the editors. |
| 17 | Carousel and chart directions | — | the bins read 0 → 50+ left to right, the number column on the left | RTL | — | As every chart on the page (`direction:ltr` on the strip and the axis, as for `.fl-strip` and `#kChart`). The carousel swipes right-to-left (the page's existing carousel code). |
| 18 | Dates | — | 1 ביולי 2025, 31 בדצמבר 2025, 14 באוקטובר 2026, 10 בדצמבר 2025, 4 ביוני 2023, 14 באוגוסט 2024, 15 באוגוסט 2024 | typography | — | All with a no-break space (`nb()`; the smoke run checks it). |
| 19 | Disclosure | — | "No account is named or labelled" = אף חשבון אינו מזוהה בשמו או מתויג | fidelity | — | "Concentrated interest is not by itself evidence of bad faith" = עניין מרוכז אינו כשלעצמו ראיה לחוסר תום לב. |
| 20 | Typography | — | — | RTL | — | No italic in the new strings (the `.fl-next` transition was removed); the Hebrew `he-k` labels as elsewhere. |

**Build guards (new):**
- `build_flash.py`:
  - every number in the visual against `results.json`: bins, counts, medians and marker positions, 53/5, 57/166, 44/66, 34%/67%, 25/14/39, and the aria-labels;
  - every quote against `verified.json` then/now and the crawl copies; each `<del>` absent now, each `<ins>` absent then;
  - each date against the key-phrase histories;
  - the four slides = the four KEEP items; views = `articles.md`;
  - no "coordinated / campaign / court / ICJ / ruling" on the card; "does not show coordination" present; "made these changes" absent;
  - card 7 sits between cards 6 and 8.
- `flash_he.py`: the Hebrew honesty, shared and disclosure lines and the key translations, verbatim; eight translations marked as ours, each with its English original; no "מחוץ לנושא" and no court or campaign words.

## 5. Smoke results

- **`smoke_core.js`: 1468 passed, 0 failed.** English and Hebrew; phone and 1280; light and dark; plus phone with reduced motion. 0 console errors or warnings in all 10 runs; no horizontal overflow at rest or after interaction.
- **`smoke_bi.js`: 328 passed, 0 failed.** The bilingual text in each mode equals the single-language build; switching works at three scroll points.
- **`smoke_lab.js`: 185 passed, 0 failed.**
- **One bug found and fixed during the run.** Inside the closed-then-opened disclosure, the chips row of the weekly chart widened the `<details>` grid item. That zoomed the phone viewport out to 956 px, and the chart was drawn at 931 px. The fix is `#kMore{min-width:0}`. The suite now also asserts that the phone viewport stays 390 px wide after the chart opens and after the carousel.

### Suites

Suites:
- `scratchpad/flash/elsewhere/smoke_core.js`: the v3fix2 suite plus the card-7 checks and the weekly-chart disclosure;
- `scratchpad/flash/elsewhere/smoke_bi.js`;
- `scratchpad/flash/elsewhere/smoke_lab.js`.

Each runs on iPhone 13 and at 1280, light and dark, plus reduced motion.

New card-7 checks:
- two rows; 53 / 5; eight bins; the bar heights follow the counts;
- the median markers sit in the 10–19 and the 2 bins;
- nothing spills out of the figure;
- swipe (phone) or next (1280), and the dot to slide 4;
- no overflow;
- each slide carries its `<del>` and `<ins>`;
- the text carries 11.5, 53, 34% and 67%;
- Hebrew: no English outside the quotes;
- reduced motion: the carousel does not smooth-scroll.

The weekly chart is closed and unbuilt before its first open, then full width, with no overflow.

Screenshots: `scratchpad/flash/elsewhere/shots/cel_{en,he}_{light,dark}.png` and `car3_*.png`.
