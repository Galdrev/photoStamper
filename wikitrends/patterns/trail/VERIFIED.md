# Elsewhere on Wikipedia: hand verification of the editor-trail candidates

**What this is.** The editor trail (`articles.md`, `cards.md`, `results.json`, run 42778075792) lists 53 articles outside our topic sets where 3 or more of the ~40 most active critical-term editors of the core articles made a qualifying edit. Its "first sentence 2021 → now" column comes from an automatic word list. Before any of these articles goes on the flash page, each candidate was read by hand, in the actual text, then and now.

**Data.** GitHub Actions, `.github/workflows/wikitrends-verify.yml`. User-Agent: `fetch.py`'s (no email address). Results are in `wikitrends-data:verify/<run>/verify/`.
- Run **42847367759**: the seven candidates named by the coordinator.
- Run **42848274633**: seven further candidates from the list, fetched because only one of the first seven held up.

For each article the workflow fetched:
- the raw wikitext of section 0 of the revision live on 1 Jan 2021 (`rvstart=2021-01-01T00:00:00Z`, `rvdir=older`, `rvlimit=1`), or of the first revision if the article is younger;
- section 0 of the latest revision;
- the section-0 history since 1 Jan 2021: revid, timestamp, revert tag, page moves, first sentence and opening prose. No usernames or edit comments were stored.

`patterns/trail/verify_extract.py` turns these into `patterns/trail/verified.json`, which holds the texts, the revision references, each key phrase's dated changes and the decisions below. The opening section is `analyze.prose(analyze.split_lead(...))` and the first sentence is `analyze.sentences(...)[0]`, as everywhere in the project. The flash build checks every carousel quote against `verified.json` (then and now) and against the stored crawl copies.

**Rules applied.**
- **DROP** if the "change" is a move (the words are in the next sentences), a rename artefact (a different article or title in 2021), a word-list false positive, or court-centric (owner, MUSTFIX 4).
- **DROP** if it is not on the subject: the owner's scope rule (MUSTFIX 3) excludes villages and unrelated topics.
- Quotes are exact. "Then" is the 1 Jan 2021 copy unless stated otherwise.
- No account is named. The trail shows only that 3 or more accounts of the group made a qualifying edit on the article. **It does not show who wrote the quoted words**, and the carousel says so.

## Verdicts

| # | Article | Verdict | Then (revision, date) | Now (revision, date) | Reason |
|---|---|---|---|---|---|
| 1 | Comparisons between Israel and Nazi Germany | **DROP** | 994022813, 13 Dec 2020 | 1384426373, 8 Nov 2026 | Rename and rewrite. In 2021 the article was **Holocaust inversion**; it was moved on 7 Apr 2022 (moved back and forth on 8 Apr). The 2021 "antisemitic" sat in sentence 2: the splitter merged two sentences after `"copycats."`. Now antisemitism and the Holocaust are in sentence 2. "30 connection terms gone" mostly counts the word Holocaust in an article that is no longer about "Holocaust inversion". |
| 2 | Criticism of Israel | **KEEP** | 996551777, 27 Dec 2020 | 1384749928, 9 Nov 2026 | A real rewrite. The 2021 second sentence became the first on 1 Jul 2025 and gained "human rights violations … occupation" (1 Jul 2025), "the Nakba and the Israeli occupation" (31 Dec 2025) and "Zionist political violence" (14 Oct 2026). Renamed from "Criticism of the Israeli government" on 16 Jul 2023. |
| 3 | Genocide | **DROP** | 996450724, 26 Dec 2020 | 1383146448, 1 Nov 2026 | Word-list artefact. The critical count 7 → 20 is mostly the article's own subject word ("genocide"). The opening is a general scholarly rewrite that never mentions Israel, Palestine or Gaza. One addition is notable but not about our subject: "It is associated with colonialism, especially settler colonialism" (in the opening since 19 Jan 2026). |
| 4 | Settler colonialism | **DROP** | 996491101, 26 Dec 2020 | 1384059383, 6 Nov 2026 | Word-list artefact. "Indigenous" here is the general term ("a land and its indigenous peoples"), not the Jewish-indigeneity frame the list looks for. Critical terms fell from 20 to 11. No mention of Israel or Palestine in the opening, then or now. |
| 5 | Sheikh Jarrah controversy | **DROP** | created 1023202464, 15 May 2021 (no 2021 copy) | 1368967502, 12 Aug 2026 | The article is a 2021 creation, so "then" is a history stub. The wording has been settled since 14 Sep 2021. Both framings are attributed ("property/real estate dispute" to the Israeli government, "expulsion" / "ethnic cleansing" to Palestinians). It is a legal property dispute (court-centric). |
| 6 | Gaza genocide recognition | **DROP** | created 1307159893, 21 Aug 2025 | 1383537837, 3 Nov 2026 | Created in 2025 as a split list, then renamed twice (List of country positions → List of state positions, 21 Aug 2025 → Gaza genocide recognition, 3 Oct 2025). The "+95" is the split itself. The opening is attributed ("has been accused … by several states") and centred on the ICJ case (court-centric). |
| 7 | Samaritans | **DROP** | 997396616, 31 Dec 2020 | 1384768862, 10 Nov 2026 | No critical change (critical terms 0 → 0). The first sentence gained "often preferring to be called Israelite Samaritans", a Jewish-history term, i.e. the opposite direction. It has gone in and out since 2023, and has been in since 18 Sep 2026. |
| 8 | Plan Dalet | **KEEP** | 991916313, 2 Dec 2020 | 1369979005, 18 Aug 2026 | A real change: "a plan worked out by the Haganah" (out 24 May 2023) became "a Zionist military plan … for the conquest of territory" (since 4 Jun 2023, before the war). Sentence 2 adds the Nakba (since 14 Aug 2024). |
| 9 | Palestinian political violence | **KEEP** | 991829003, 2 Dec 2020 | 1383869304, 5 Nov 2026 | A real change: "or terror" is gone from the first sentence, which now explains the violence as insurgency by a people without a state (since 10 Dec 2025). "Terror(ism)" went in and out of the first sentence from 2022 to 2025. The section still says several groups "are considered terrorist organizations". |
| 10 | Causes of the 1948 Palestinian expulsion and flight | **KEEP** (sentence 2) | 990147549, 23 Nov 2020 | 1379281874, 9 Oct 2026 | A real change in sentence 2: "a matter of great controversy" became "today most scholars consider that the majority of Palestinians were directly expelled" (since 15 Aug 2024). The first sentence only swapped "fled or were expelled" to "were expelled or fled" and moved "by Israeli forces" to sentence 3 ("direct expulsions by Israeli forces"), so that part is a move. Renamed from "Causes of the 1948 Palestinian exodus" (Mar–Apr 2023). |
| 11 | East Jerusalem | **DROP** | 992714539, 6 Dec 2020 | 1378661048, 5 Oct 2026 | Legal-status wording ("under illegal occupation by Israel … according to international law"), close to the court framing the owner excluded. "Occupied by Jordan" left the first sentence but is in paragraph 2 ("held by Jordan"), a move. |
| 12 | Bar Kokhba Revolt | **DROP** | 997255412, 30 Dec 2020 | 1383659108, 4 Nov 2026 | A move: "Judea" left the first sentence but is in sentence 2 ("the near-total depopulation of Judea proper"). |
| 13 | Ancient Israel and Judah | **DROP** | 995346184, 20 Dec 2020 | 1380468211, 15 Oct 2026 | Rename artefact. The article was "History of ancient Israel and Judah" until 20 Jan 2026, and its first sentence now names the title ("Ancient Israel and Judah were two Israelite kingdoms"). Both kingdoms are named in sentence 4. |
| 14 | Majdal Shams | **DROP** | 996336874, 26 Dec 2020 | 1381385435, 22 Oct 2026 | A real change, but a village (owner's scope rule). "Governed by Israel" became "Under Israeli occupation since 1967", and "north of the Golan Heights" became "Golan Heights region, Quneitra Governorate, Syria". |

**Result:** 14 read; 4 KEEP; 10 DROP. Of the coordinator's 1–7, only "Criticism of Israel" holds up.

## The four KEEP items: exact quotes

### Criticism of Israel (7.9k monthly views; trail: 3 accounts inserting critical terms)
- **Then**, sentence 2 (rev 996551777, 27 Dec 2020). Sentence 1 was "Criticism of the Israeli government, often referred to simply as criticism of Israel, is an ongoing subject of journalistic and scholarly commentary and research within the scope of international relations theory, expressed in terms of political science."
  > Within the scope of global aspirations for a community of nations, Israel has faced international criticism since its declaration of independence in 1948 relating to a variety of topics, both historical and contemporary.
- **Now**, sentence 1 (rev 1384749928, 9 Nov 2026):
  > Israel has faced international criticism since its establishment in 1948 relating to Zionist political violence and a variety of other issues, many of which are centered around human rights violations related to the Nakba and the Israeli occupation of the West Bank and the Gaza Strip.
- **Dates (first sentence):**
  - 1 Jul 2025 (rev 1298331589): the definitional sentence went and this sentence led, with "human rights violations in its occupation of the West Bank and the Gaza Strip".
  - 31 Dec 2025 (rev 1330414960): "related to the Nakba and the Israeli occupation".
  - 10 Aug 2026 (rev 1368711237): "its political violence".
  - 14 Oct 2026 (rev 1380289192): "Zionist political violence".
  - Each phrase has stayed since it came in.
- **Opening-section critical terms:** 1 → 6.
- **Card key phrase:** “relating to a variety of topics, <del>both historical and contemporary</del>” → “relating to <ins>Zionist political violence</ins> … <ins>human rights violations related to the Nakba and the Israeli occupation</ins> of the West Bank and the Gaza Strip”.

### Palestinian political violence (6.2k)
- **Then**, sentence 1 (rev 991829003, 2 Dec 2020):
  > Palestinian political violence refers to acts of violence or terror motivated by Palestinian nationalism.
- **Now**, sentence 1 (rev 1383869304, 5 Nov 2026):
  > As Palestinians have not had a fully recognized state with a regular army, much of Palestinian political violence in the context of the Israeli–Palestinian conflict has taken the form of insurgency.
- **Dates for "terror" in the first sentence:**
  - in, Jan 2021;
  - out, 18 Oct 2022;
  - back, 19 Nov 2023 ("including Palestinian terrorism");
  - out and back, 13 Oct 2025, and again 21–23 Nov 2025;
  - out, 10 Dec 2025 (rev 1326720518), when the insurgency sentence came in, and still out.
- **Scope:** "terror" left the first sentence only. Paragraph 2 still says "Several of these groups are considered terrorist organizations by the governments of the United States, Canada, the United Kingdom, Japan, New Zealand and the European Union." Sentence 3 now says "This includes the objective of ending the Israeli occupation." The 2021 opening's Martyrs' Fund paragraph ("the Authority continues to incentivize terrorism by awarding large stipends …") and the Israeli casualty figures are no longer in the opening.
- **Card key phrase:** “acts of violence <del>or terror</del> motivated by Palestinian nationalism” → “As Palestinians have not had a fully recognized state with a regular army, much of Palestinian political violence … has taken the form of <ins>insurgency</ins>”.

### Plan Dalet (4.7k)
- **Then**, sentence 1 (rev 991916313, 2 Dec 2020):
  > Plan Dalet (Tokhnit dalet) was a plan worked out by the Haganah in Mandatory Palestine in March 1948.
- **Now**, sentences 1–2 (rev 1369979005, 18 Aug 2026):
  > Plan Dalet (תוכנית ד', Tokhnit dalet "Plan D"; 1 April – 14 May, 1948) was a Zionist military plan executed during the 1948 Palestine war for the conquest of territory in Mandatory Palestine in preparation for the establishment of a Jewish state. The plan was the blueprint for Israel's military operations, starting in March 1948 until the end of the war in early 1949, and so played a central role in the 1948 Palestinian expulsion and flight known as the Nakba.
- **Dates:**
  - "worked out by the Haganah" out, 24 May 2023;
  - "for the conquest of territory", 4 Jun 2023 (rev 1158511326);
  - "a Zionist military plan", 4 Jun 2023 (rev 1158522985; it first went in at 15:47, was reverted two minutes later and was back at 16:03);
  - "known as the Nakba" in the opening, 14 Aug 2024 (rev 1240263491).
  - The first-sentence change dates from June 2023, four months before the war.
- **Critical terms:** 3 → 6.
- **Card key phrase:** “a plan <del>worked out by the Haganah</del> in Mandatory Palestine” → “a <ins>Zionist military plan</ins> executed during the 1948 Palestine war <ins>for the conquest of territory</ins>”, and sentence 2 “played a central role in the 1948 Palestinian expulsion and flight known as the Nakba”.

### Causes of the 1948 Palestinian expulsion and flight (1.6k)
- **Then**, sentence 2 (rev 990147549, 23 Nov 2020):
  > The causes for this mass displacement is a matter of great controversy among historians, journalists, and commentators.
- **Now**, sentence 2 (rev 1379281874, 9 Oct 2026):
  > The causes of this mass displacement have been a matter of dispute, though today most scholars consider that the majority of Palestinians were directly expelled or else fled due to fear.
- **Dates:**
  - 24 Jun 2024: "great controversy" became "controversy";
  - 15 Aug 2024 (rev 1240544511): "though today most scholars consider …"; "controversy" later became "dispute".
- **Sentence 1:** "fled or were expelled from their homes by Israeli forces" became "were expelled or fled from their homes" (24 Jun 2024). "by Israeli forces" now opens the list of causes in sentence 3 ("direct expulsions by Israeli forces"). This is reported as a move, not shown as a change.
- **Critical terms:** 1 → 4.
- **Card key phrase:** “a matter of <del>great controversy among historians, journalists, and commentators</del>” → “a matter of dispute, though <ins>today most scholars consider that the majority of Palestinians were directly expelled</ins> or else fled due to fear”.

## How the cards may be described (messaging rules)
- **Allowed:**
  - "These four articles are among the 53 outside articles where 3 or more of the most active editors of the core articles made this kind of change (comparison editors: 5)."
  - "We counted accounts, not authors: we did not check who wrote these lines."
- **Not allowed:**
  - "the same editors made these changes" (not checked; the trail holds no per-edit authorship);
  - any account name, label or per-account count;
  - "coordinated" or "campaign";
  - the court-centric items above.
- **The honest counterweight**, shown on the page next to the pattern visual (`cards.md` card 4): after a revert, these editors made the same change again less often than the comparison group (57 of 166 reverted episodes, 34%, against 44 of 66, 67%).
