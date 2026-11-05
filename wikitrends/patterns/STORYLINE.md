# Storyline: a 12-minute talk

Working title: **"The average didn't move. The front page did."**

Twelve beats, about a minute each; the twist (beat 7) gets a minute and a half. Each beat has one sentence to say, the visual, and the number to land. Chart files are relative to `wikitrends/patterns/`; patterns refer to SYNTHESIS.md.

---

### Beat 1. Hook (0:00 to 1:00)
- **Say:** "In 2021 Wikipedia's first sentence on the Nakba called it the destruction of Palestinian society; today it calls it 'the ethnic cleansing of Palestinian Arabs by Zionists', and that second version is what readers, search engines and AI assistants now take as the encyclopedia's answer."
- **Visual:** Two first sentences of the Nakba article, 2021 and 2026, one above the other, with the changed words highlighted. Source: `then_vs_now` in `story_sources_langs/cards.json`.
- **Number:** 4.4 million views of that one article since 2021.

### Beat 2. The question and the rule (1:00 to 2:00)
- **Say:** "We asked a measurable question, not 'is Wikipedia biased': did the wording on Israel, Palestine, Zionism and Judaism move between 2021 and 2026, more than on other countries and conflicts, and how?"
- **Visual:** One slide: 10,433 articles, 3 snapshots; a deep panel of 513 articles, every quarter; every lead revision for 40 key articles; 11 languages; a comparison group of other conflicts and countries.
- **Number:** 10,433 articles, half of them sealed until the end.

### Beat 3. The first answer was "no" (2:00 to 3:00)
- **Say:** "We wrote the test down before looking, and by our own rule the answer was 'not supported': on average, these articles did not gain critical vocabulary faster than the comparison articles."
- **Visual:** A flat, almost empty chart: the pre-registered estimate with its interval crossing zero.
- **Number:** −0.30 per 10k words, interval −2.7 to +1.7.

### Beat 4. Tension: but something did happen (3:00 to 4:00)
- **Say:** "In a sample twenty times bigger there is a small, real rise after October 2023, it replicated on the half of the data we had locked away, and it sits in the Israel and Palestine articles while articles on Judaism did not move at all."
- **Visual:** Bars by WikiProject: Palestine and Israel up, Judaism at zero, comparison projects around them (Pattern P2; `when_where_what/chart_data/04_geography_projects.json`).
- **Number:** +3.6 percentage points more articles gained, on sealed data. Judaism: −0.1.

### Beat 5. When: one wave, then a plateau (4:00 to 5:00)
- **Say:** "The change was not a slow drift: it came as one wave in the first half of 2024, months after the news peak, and it has been flat since early 2025."
- **Visual:** Quarterly bars, topic vs comparison, with 7 Oct 2023 and the ICJ order marked; faint pageview line spiking and falling in Oct 2023 (Pattern P1; `when_where_what/chart_data/01_timeline_quarterly.json`, `how_who/chart_data/views_vs_edits_index.json`).
- **Number:** 46 terms per 100 articles in 2024-Q2, against about 7 before the war and about 4 now.

### Beat 6. Where: a few hundred pages (5:00 to 6:00)
- **Say:** "Most pages never changed; the rise came from a few hundred of them."
- **Visual:** Lorenz curve, topic vs comparison, before and after (Pattern P2; `when_where_what/chart_data/03_concentration.json`).
- **Number:** 85% of topic articles unchanged; 40 articles supplied 38% of the new terms.

### Beat 7. The twist: the average didn't move, and yet... (6:00 to 7:30)
- **Say:** "Here is why the average test missed it: the pages that changed are the ones people read, and the part that changed is the lead, the paragraph that search engines and AI assistants quote."
- **Visual:** Two bars per group: share of articles vs share of pageviews whose lead gained critical terms; then lead vs body growth (Pattern P3; `story_sources_langs/chart_data/exposure_concentration.json`, `when_where_what/chart_data/09_lead_vs_body.json`).
- **Number:** 15% of topic articles, 46% of topic readers. Leads +35%, bodies +13.5%.

### Beat 8. What: the story moved back to 1948 (7:30 to 8:30)
- **Say:** "The war did not mostly add war coverage; it sent editors back to retell 1897 to 1948 and to rename the land, from Zionism's definition to Palestinian village pages."
- **Visual:** Then/now cards for Zionism ('re-establishment ... of a Jewish state' to 'a Jewish homeland through colonization'), West Bank and Nakba; small inset of article types gaining per year (Pattern P4; `when_where_what/chart_data/05_geography_type_importance.json`).
- **Number:** 8.4 of the 9.3-point lead rise is in sentences about older history. Zionism's 'colonial' went in and out 44 times.

### Beat 9. How and who: quiet pages, regulars, the same sources (8:30 to 9:45)
- **Say:** "This was not a flood of new accounts or partisan sources: experienced regulars wrote it, mostly on pages where nobody reverted it, citing much the same sources as before, while the famous edit wars were confined to four pages."
- **Visual:** Grouped bars by revert tercile (low-revert topic pages stand out), with a small line of newcomer share falling after the war (Patterns P7, P8, P9; `how_who/chart_data/revert_tercile_gain.json`, `how_who/chart_data/who_edits_by_quarter.json`).
- **Number:** Low-revert topic pages gained 28.5% of the time, against 13% for contested ones. Newcomer edits fell from about 25% to 12 to 17%. Four pages held 68% of all lead flips.

### Beat 10. Is this just what wars do to Wikipedia? (9:45 to 10:45)
- **Say:** "Partly: other wars get their own vocabulary waves, but theirs stayed inside the war articles, the same amount of editing changed these pages more often, and most other language editions did not follow."
- **Visual:** Small multiples of Tigray, Nagorno-Karabakh, Sudan and Ukraine (flat after their step), next to the share gaining by project (Pattern P6; `when_where_what/chart_data/10_other_conflicts_waves.json`, `how_who/chart_data/busiest_by_project.json`).
- **Number:** Busiest pages gaining: Palestine 57%, Israel 44%, Ukraine and Armenia 30%. Other Wikipedias' leads: mean +0.06 against English +0.24.

### Beat 11. Honesty slide: lopsided, not one-sided, and what we cannot say (10:45 to 11:15)
- **Say:** "Changes went both ways and most new labels arrived attributed, but where a few flagship leads dropped the attribution, it went one way; and nothing here tells us whether the new wording is true, what editors intended, or whether anyone coordinated off-wiki."
- **Visual:** Gaza genocide's first sentence as a staircase from 'Allegations have been made' to 'The Gaza genocide is', beside the Uyghur genocide lead that still says 'often been characterized as'; a short "cannot conclude" list underneath (Pattern P9; `story_sources_langs/chart_data/exposure_timing.json`).
- **Number:** 8 one-way steps in 21 months. In comparison: "terrorism" fell 24% in topic leads, and 'by Zionist militias' was cut from the 1948 expulsion first sentence.

### Beat 12. What to do (11:15 to 12:00)
- **Say:** "If you read Wikipedia, check the history and the attribution; if you build on it, carry the attribution through and watch the first sentence; and if you study it, weight by readers and always bring a comparison group, which is why we will keep watching the 50 pages that carry most of what people see."
- **Visual:** Four columns (readers, editors, platforms, researchers), one action each, and a mock-up of the "hot core" monitor showing 50 article names with a weekly lead-diff light.
- **Number:** 50 pages to watch, and the most-read of them, Israel, only settled its lead on 4 September 2026.

---

**Timing note.** If time runs short, merge beats 9 and 10. Never cut beats 3 and 7: the honest null followed by the reader-weighted twist is the spine of the talk.
