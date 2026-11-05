# Storyline: a 12-minute talk

Working title: **"The average didn't move. The front page did."**

Twelve beats, about a minute each; the twist (beat 7) gets a minute and a half. Each beat has one sentence to say, the visual, and the number to land. Chart files are relative to `wikitrends/patterns/`; patterns refer to SYNTHESIS.md. Every number below matches the November 2026 update of SYNTHESIS.md (mass2, full scale). Study 2's withdrawn "1948 forced vs fled" result is not used anywhere in the talk.

---

### Beat 1. Hook (0:00 to 1:00)
- **Say:** "In 2021 Wikipedia's first sentence on the Nakba called it the destruction of Palestinian society; today it calls it 'the ethnic cleansing of Palestinian Arabs by Zionists', and that second version is what readers, search engines and AI assistants now take as the encyclopedia's answer."
- **Visual:** Two first sentences of the Nakba article, 2021 and 2026, one above the other, with the changed words highlighted. Source: `then_vs_now` in `story_sources_langs/cards.json`.
- **Number:** 4.4 million views of that one article since 2021.

### Beat 2. The question and the rule (1:00 to 2:00)
- **Say:** "We asked a measurable question, not 'is Wikipedia biased': did the wording on Israel, Palestine, Zionism and Judaism move between 2021 and 2026, more than on other countries and conflicts, and how?"
- **Visual:** One slide: 10,320 articles at full scale (4,642 topic, 5,678 comparison), 3 snapshots plus every lead edit; a deep panel of 513 articles, every quarter; every lead revision for 40 key articles; 11 languages; 87 real-world events fixed before looking.
- **Number:** 10,320 articles; the main test was replicated on a half of the data kept sealed until the end.

### Beat 3. The first answer was "no" (2:00 to 3:00)
- **Say:** "We wrote the test down before looking, and by our own rule the answer was 'not supported': on average, these articles did not gain critical vocabulary faster than the comparison articles."
- **Visual:** A flat, almost empty chart: the pre-registered estimate with its interval crossing zero.
- **Number:** −0.30 per 10k words, interval −2.7 to +1.7.

### Beat 4. Tension: but something did happen (3:00 to 4:00)
- **Say:** "In a sample twenty times bigger there is a small, real rise after October 2023, it replicated on the half of the data we had locked away, and it sits in the Israel and Palestine articles while articles on Judaism did not move at all."
- **Visual:** Bars by WikiProject: Palestine and Israel up, Judaism at zero, comparison projects around them (Pattern P2; `when_where_what/chart_data/04_geography_projects.json`).
- **Number:** +3.6 percentage points more articles gained, on sealed data. Judaism: −0.1.

### Beat 5. When: one wave, then a plateau (4:00 to 5:00)
- **Say:** "The change was not a slow drift: it came as one wave through 2024 and is back to the pre-war rate in 2026, and the editors came with the battles, not with the court rulings."
- **Visual:** Half-year bars of critical-term insertions per 1,000 topic edits, with 7 Oct 2023 and the ICJ order of 26 Jan 2024 marked; small inset heatmap of event type by outcome (Patterns P1, P10; `data/event_timing_mass2.json` → `half_years`, `events/chart_data/mass2_02_type_by_outcome.json`).
- **Number:** About 7 insertions per 1,000 edits before the war, 16 in 2024, 5 to 6 in 2026. After military escalations, topic edits rose 17%; after legal events they did not (0.94x).

### Beat 6. Where: a few hundred pages (5:00 to 6:00)
- **Say:** "Most pages never changed; the rise came from a few hundred of them."
- **Visual:** Lorenz curve, topic vs comparison, before and after (Pattern P2; `when_where_what/chart_data/03_concentration.json`).
- **Number:** 85% of topic articles unchanged; 40 articles supplied 38% of the new terms.

### Beat 7. The twist: the average didn't move, and yet... (6:00 to 7:30)
- **Say:** "Here is why the average test missed it: the few pages that changed are read far more than the average page, and the part that changed is the lead, the paragraph that search engines and AI assistants quote."
- **Visual:** Two bars per group: share of articles vs share of pageviews whose lead gained critical terms; then lead vs body growth (Pattern P3; `mass2/chart_data/10_pageviews_exposure.json`, `when_where_what/chart_data/09_lead_vs_body.json`).
- **Number:** 4% of topic articles, 15% of topic reading, three times the comparison share (1.5% of articles, 5% of reading). Leads +35%, bodies +13.5%.
- **Careful:** do not say "most readers". 83% of topic views still land on leads that did not change. Do not use the older deep-panel "15% of articles, 46% of readers"; it came from a hand-picked set of prominent pages.

### Beat 8. What: the story moved back to 1948 (7:30 to 8:30)
- **Say:** "The war did not mostly add war coverage; it sent editors back to retell 1897 to 1948 and to rename the land, from Zionism's definition to Palestinian village pages."
- **Visual:** Then/now cards for Zionism ('re-establishment ... of a Jewish state' to 'a Jewish homeland through colonization'), West Bank and Nakba; small inset of the most-added framing categories (1948 Palestinian expulsion and flight, Zionist political violence, Israeli massacres of Palestinians, Israeli apartheid) (Patterns P4, P12; `mass2/chart_data/12_narrative_residual.json`, `mass2/chart_data/06_categories_infobox_seealso.json`).
- **Number:** 89% of the post-war lead change is in sentences that are not about recent events. Framing categories were added to 7.2% of topic articles, against 2.2% of comparison articles. Zionism's 'colonial' went in and out 44 times.

### Beat 9. How and who: quiet pages, regulars, the same sources (8:30 to 9:45)
- **Say:** "This was not a flood of new accounts, blocked accounts or partisan sources: established editors wrote it, mostly on pages where nobody reverted it, citing much the same sources as before, and the formal process (protection, RfCs) grew on a few core pages."
- **Visual:** Grouped bars by revert tercile (low-revert topic pages stand out), next to bars of low-edit-count accounts, topic vs comparison, and a Pareto of RfCs by page (Patterns P7, P8, P11; `how_who/chart_data/revert_tercile_gain.json`, `mass2/chart_data/01_who_edits.json`, `mass2/chart_data/03_rfc_rm.json`).
- **Number:** Low-revert topic pages gained 28.5% of the time, against 13% for contested ones. Accounts with under 500 edits made 9% of topic edits, against 17% on comparison pages. Now-blocked accounts made 13.7% of insertions, against a 12.3% base. RfCs per article-year nearly tripled; 5 pages hold half of them.

### Beat 10. Is this just what wars do to Wikipedia? (9:45 to 10:45)
- **Say:** "Partly: other wars get their own vocabulary waves, but theirs stayed inside the war articles, the same amount of editing changed these pages more often, and most other language editions did not follow."
- **Visual:** Small multiples of Tigray, Nagorno-Karabakh, Sudan and Ukraine (flat after their step), next to the share gaining by project (Pattern P6; `when_where_what/chart_data/10_other_conflicts_waves.json`, `how_who/chart_data/busiest_by_project.json`).
- **Number:** Busiest pages gaining: Palestine 57%, Israel 44%, Ukraine and Armenia 30%. Other Wikipedias' leads: mean +0.06 against English +0.24.

### Beat 11. Honesty slide: lopsided, not one-sided, and what we cannot say (10:45 to 11:15)
- **Say:** "Changes went both ways and most new labels arrived attributed, but where a few flagship leads dropped the attribution, it went one way; and nothing here tells us whether the new wording is true, what editors intended, or whether anyone coordinated off-wiki."
- **Visual:** Gaza genocide's first sentence as a staircase from 'Allegations have been made' to 'The Gaza genocide is', beside the Uyghur lead that still says 'often been characterized as' and a strip of the atrocity set (most now stated); a short "cannot conclude" list underneath (Pattern P9; `story_sources_langs/chart_data/exposure_timing.json`, `mass2/chart_data/11_atrocity_voice.json`).
- **Number:** 8 one-way steps in 21 months. 9 of 11 other atrocity leads also state 'genocide' in Wikipedia's voice. In the other direction: "terrorism" fell 24% in topic leads, and 'by Zionist militias' was cut from the 1948 expulsion first sentence.

### Beat 12. What to do (11:15 to 12:00)
- **Say:** "If you read Wikipedia, check the history and the attribution; if you build on it, carry the attribution through and watch the first sentence; and if you study it, weight by readers and always bring a comparison group, which is why we will keep watching the 50 pages that carry most of what people see."
- **Visual:** Four columns (readers, editors, platforms, researchers), one action each, and a mock-up of the "hot core" monitor showing 50 article names with a weekly lead-diff light.
- **Number:** 50 pages to watch, and the most-read of them, Israel, only settled its lead on 4 September 2026.

---

**Timing note.** If time runs short, merge beats 9 and 10. Never cut beats 3 and 7: the honest null followed by the reader-weighted twist is the spine of the talk.
