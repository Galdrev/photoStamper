# Copy edit: full line edit and new hero title (2026-11-08)

Files changed: `page_template.html` (HTML and the JS strings that render visible text) and `build_page.py` (cross-language column labels, cell notes and moment captions). The build assertions still pass. One of them, `check_quotes`, now strips a trailing comma as well as a period from a quote, so American quote punctuation passes; the check is otherwise unchanged.

## Hero title

1. **Israel’s story once opened with a return. Now it opens with “colonization” and “genocide.”** (13 words, 4 lines at 390px) **This is the pick.**
2. In 2021, no top article charged Israel with genocide. Now Israel’s own article does. (14 words)
3. How the world’s encyclopedia rewrote the first lines of Israel’s story. (11 words)

**Why the pick.** It is the only candidate that follows the model's shape: two full sentences, then and now, with the exact quoted words. The narrative is the subject, and Wikipedia does not appear in it. It sums up the whole story where the other two cover only one section. It does not repeat the Zionism heading word for word: “a return” is the paraphrase the Zionism bottom line already uses.

Candidate 2 would duplicate the #charge headline, which now has the same then/now shape. Candidate 3 is a summary with no then/now, and it makes the encyclopedia the subject.

The deck gives the exact quotes and dates: the Israel genocide sentence (since 4 May 2025), Zionism’s “re-establishment” in 2021 and “a Jewish homeland through colonization” since 27 August 2026, the Nakba, Hamas, and the hostages.

The eyebrow “How the world’s reference retold Israel’s story, 2021–2026” is now “Israel’s story on Wikipedia, 2021–2026”. It is shorter and no longer breaks inside the date range on a phone.

## The 15 most important edits

| # | Where | Before | After |
|---|---|---|---|
| 1 | Hero H1 | Zionism “through colonization”, Israel “began committing genocide”: how Wikipedia tells it now. | Israel’s story once opened with a return. Now it opens with “colonization” and “genocide.” |
| 2 | #zionism H2 | …“a Jewish homeland through colonization”. | …“a Jewish homeland through colonization.” (punctuation only, as the owner asked) |
| 3 | #charge H2 | Israel “began committing genocide”: a charge absent in 2021 is now stated as fact in the encyclopedia’s own voice | In 2021, no top article charged Israel with genocide. Now Israel’s own article says it “began committing genocide.” |
| 4 | #oct7 H2 | October 7 is “armed incursions” in its first sentence. The Israel and Hamas openings omit the hostages. Hamas’s terror designation moved to the end. | October 7 was “coordinated attacks.” Now it is “armed incursions.” The Israel and Hamas openings do not mention the hostages. (The designation move is now in the figure title, “moved from sentence 5 to sentence 22”, and in the bottom line.) |
| 5 | #palestine H2 | 1948 now has a perpetrator: the Nakba is “the ethnic cleansing of Palestinian Arabs by Zionists”, in Wikipedia’s own voice | The Nakba was “the destruction of Palestinian society.” Now it is “the ethnic cleansing of Palestinian Arabs by Zionists.” (“Own voice” moved to the bottom line.) |
| 6 | #crosslang H2 | Outside English, “genocide” is now stated as fact in Spanish, Portuguese and Arabic. Hebrew’s Gaza-war article mentions it only as South Africa’s court case. | Spanish, Portuguese and Arabic once attributed the genocide charge. Now they state it as fact. Hebrew’s Gaza war article cites only South Africa’s court case. |
| 7 | #after H2 | …the opening lines moved; most first tries bounced, and today’s definitions settled… | After some battles, the opening lines moved within weeks. Most first tries were undone; today’s definitions settled in 2025 and 2026. |
| 8 | #zionism bottom line | …no longer calls it a return (that word went in 2021)… stayed up about four times as long. | …no longer calls it a return… lasted about four times as long. (The parenthesis contradicted the deck, which dates the final removal to 9 July 2024.) |
| 9 | #organised bottom line and deck | …no account changed three or more… Nine accounts made 48 of the 216 changes | A handful of accounts, each changing three or more first sentences… Nine such accounts made 48 of the 216 changes. (This restores the WHO.md qualifier the round-5 data review found missing.) |
| 10 | #after card stat line | Three weeks from Ground invasion (27 Oct 2023): 8.7 new terms a week, against 8.3 in the six weeks before: no clear rise; 14 still there a week later. | Three weeks from the ground invasion (27 Oct 2023): 8.7 new terms a week, against 8.3 in the prior six weeks (no clear rise); 14 in all lasted a week. (This fixes the missing article and the capital letter, and makes clear that 14 is a three-week total.) |
| 11 | Zionism stepper, “What this edit did” | …disputed description · in Wikipedia’s own voice; neutral: “wording only · style only”; mixed: “mixed” | …disputed description · stated in Wikipedia’s own voice; neutral: “wording only, no change in stance”; mixed: “some criticism added, some removed” |
| 12 | Zionism coding line | 88 changes made it more critical, 77 less (37 not coded); the critical wordings stayed up 386 days in all, the others 96. | 88 changes made the sentence more critical and 77 less critical (37 not coded). The more critical wordings lasted 386 days in all; the others, 96. |
| 13 | #against bottom line | Critical terms entering… outnumbered those leaving almost four to one, against under two to one in other conflicts’ articles; the few edits… | Critical terms going into topic opening paragraphs outnumbered those coming out almost four to one; in other conflicts’ articles, under two to one. |
| 14 | #trust H2 and bottom line | This measures what the encyclopedia says… / …what the world’s reference now says… | This study measures what Wikipedia says, not whether it is true. / They show what Wikipedia now says about Israel, not who is right or whether anyone coordinated. |
| 15 | Evidence links in every section | “Every charge, side and voice…: see the evidence: the charge chart.” (double colon, link on “see the evidence”) | “See the evidence: the charge chart, with every charge, side and voice, sentence by sentence.” (one pattern everywhere; the link carries the description) |

Other edits:
- Every #after card was split into short sentences.
- The #oct7 and #palestine decks lost their fragments (“sentence 9, “…””, “The Israel and Hamas openings: no mention…”).
- The scope line is now a full sentence.
- The Hamas legend and caption were tidied.
- The cross-language key and coding note now say “October 7”, use “≈:”, and print “gray”.
- The #organised headline drops “would have shown up”.
- The network hint now reads “to see its numbers next to what chance would give”.
- In the evidence room, the #when H2 was split, the ArbCom sentence in #ev-organised was split, “arbitration committee” is now capitalized, and the glossary uses curly quotes.

## Punctuation and style decisions

- **Quotes.** Curly quotes everywhere. Periods and commas go inside the closing quote (American style), including after single-word quotes. Semicolons and colons stay outside. The one exception is a quote that already ends in “...”: no period is added. Quoted Wikipedia text keeps its own spelling (“organisation”, “recognised”, straight apostrophes such as “Netanyahu's”) and is never altered.
- **Ranges.** En dash (2021–2026, May–June 2025). The mast keeps a spaced en dash because the range has internal spaces (1 Jan 2021 – 5 Nov 2026).
- **Dates.** Day-month-year, as in FT and Economist house style and as an Israeli reader expects: 8 November 2026 in prose, 8 Nov 2026 in chart labels. The event is “October 7”, after the Wikipedia article title; the date is “7 October 2023”. Column and note labels that used “7 October” for the event now say “October 7”.
- **Numbers.** Figures for all counts and percentages, as the page already did. Spelled-out counts stay where the sentence already used them (“four to one”, “three weeks”). No number changed.
- **Spelling.** American spelling in our prose: organized, synchronized, anonymized, analyzed, labeled, favors, colored, color, center, judgment, gray, programs, prewar, postwar, wartime, retelling.
  - `#organised` and other IDs are code and are unchanged.
  - Our English translations of other editions (langs.json) keep British spelling, because the build checks every quoted translation against that file. Our glosses of those words (“terror organisation”) were left to match.
- **Headlines.** Sentence case, as complete sentences ending with a period. Where a then/now pair fits (Zionism, charge, October 7, Nakba, languages), it follows the model: “X was … Now it is ….”
- **Serial comma.** None, as in NYT and Upshot style, unless needed for clarity.
- **Labels and captions.** Lowercase after “·”. Evidence links always read “See the evidence: <description>.”
- **Stepper labels** (from change_codes.json `label_options`):
  - direction: “adds or strengthens a criticism”, “removes or softens a criticism”, “wording only, no change in stance”, “some criticism added, some removed”;
  - claim: “disputed description”, “date, place, number or name”;
  - voice: “stated in Wikipedia’s own voice”, “attributed to a source”, “removed, nothing in its place”;
  - “not coded” is never shown as neutral, and the labels use no “hostile” and no “alleged”.
- **Length.**
  - Every story section’s prose is at or below its round-5 word count (zionism 119→112, charge 170→170, oct7 129→129, palestine 226→226, after 124→123, crosslang 101→101, against 176→176, organised 139→139, trust 103→95).
  - The rendered story text is 3,679 words, the same as before. The evidence room is 23,207→23,208 words: one word over, from capitalizing “Arbitration Committee” and the curly-quoted glossary.
  - Phone height went from 15,857 to 15,806px: **18.73 screens at 844**, under the 20 cap. Desktop is 15.67.
  - The smoke test passes in four contexts (phone and desktop, light and dark): 0 console errors and 0 horizontal overflow in both views. Scrolly cards 1–5 activate on phone. Desktop scrolly activation is unchanged from before (the smoke script reports −1 both before and after).

## Flagged for a data check (not changed)

1. **Zionism coding counts disagree with MUSTFIX 7.** The page, built from change_codes.json, shows 88 more critical, 77 less critical and 37 not coded, with 386 vs 96 days. MUSTFIX_owner.md item 7 cites 78 vs 70 and 336 vs 38 days, with 64 of 70 undone within a day. The bottom line’s “about four times as long” matches the page data (386/96) but not the MUSTFIX figures (about 9×). Confirm which coding run is current.
2. **“though” vs “but”.** The settlements bullet quotes “though Israel disputes this”; EIC_cut.md and MUSTFIX 1 quote “but Israel disputes this”. Check against the stored revision.
3. **Nakba “by Zionists” since 6 July 2026.** Round-5 data review found a same-day revert on 17 July 2026. “Since” is defined as the start of the current run, so it is probably fine, but say so if challenged.
4. **#after stat lines.** The “lasted a week” count is a three-week total shown next to a weekly rate. The wording now says “in all”, but a reader may still compare 17 with 13.7. Consider showing the three-week total of new terms alongside it, which would be a data and design change.
5. **Ratchet figures differ by panel.** Evidence #ratchet says 47.3% vs 42.9% of added terms lasted 30 days on the crawl; the ratchet chart’s note says 36% vs 56% on the deep panel. Attribution is 21%→25% on the crawl vs 26%→25% on the deep panel. Both are labeled by panel, but the comparison-article direction flips. Worth a sentence or a check.
6. **#zionism bottom line.** I removed “(that word went in 2021)” because the deck dates the final removal to 9 July 2024. The bottom line now just says “no longer”.
7. **Unchanged known items.** ArbCom primary pages are still unverified, and that remains the publication blocker. The deck/phase-card mismatch (44/41 vs 43/42) lives only in the evidence room now.
