# Who changed what: anonymous-account patterns and the public record

Scope and boundary. Part 1 uses only our own data, where editors are stored as salted hashes. We link hashes only within one source file and, for mass2, only within one article. No account is named, profiled or tied to a person or organization. Part 2 summarises the public record about Wikipedia's processes and about organizations that others have reported on. It is context. It is **not** an attribution of any change we measured.

Numbers: `chart_data/who_metrics.json` (computed from `data/ratchet.json`, `data/bisect.json`, `data/mass2_events.json.gz`, `data/mass2.json`, `data/pilot/pilot.json`, `data/results.json` → `coordination`). Charts: `chart_data/zionism_first_sentence_accounts.json`, `chart_data/inserters_vs_removers.json`.

Terms used below:
- **Critical terms**: settler-colonial/colonization, apartheid, genocide, ethnic cleansing, occupation, Nakba/expulsion, war crimes. These are the project's lexicon families (`results.json` → `lexicon`).
- **Extended-confirmed (EC)**: an account at least 30 days old with at least 500 edits.
- **Now-indef-blocked**: an account indefinitely blocked at the time we collected the data, not necessarily when it made the edit.

---

## Part 1: what our data show (aggregate, anonymous)

### Card 1. The Zionism first sentence: many hands, no single author  [MODERATE]

**What we see.**
- The Zionism lead had 3,661 revisions from 455 distinct accounts (2021–2026). Its first sentence changed 292 times, across 169 distinct versions.
- The traced changes that carried each quarter's new wording (`bisect.json`, n=16) came from 14 distinct accounts. Two accounts made 2 changes each; every other account made 1.
- Concentration of those 16 changes: the top 1 account made 12.5%, the top 3 made 31%, the top 10 made 75%.
- In the war window (pilot), 366 accounts edited the whole article. One account made 17.4% of all 3,279 edits.

**Caveat.** The 16 traced changes are one per quarter. They are not every edit to the sentence.

### Card 2. "Colonization" went into the first sentence 44 times and out 41 times; removals almost never held  [MODERATE on counts; LOW on attribution]

**What we see.**
- Among first-sentence transitions where both versions' text is stored, "coloni-" was **inserted 44 times** and **removed 41 times**.
- 20 of the 44 insertions (45%) were reverted. 37 of the 41 removals (90%) were reverted.
- Timing: 63 of the 85 flips happened in 2024. After that there were 12 in 2025 and 10 in 2026.
- The word entered the sentence between the traced changes of April and July 2024. Every traced version since then contains it.

**We cannot count distinct inserting vs removing accounts for this word.**
- The first-sentence timeline in `ratchet.json` stores no editor hashes.
- The account-linked lead-event files (mass2 and pilot) record no settler-colonial flips on Zionism. "Colonization" was already somewhere in the lead in 2021, so moving it into the first sentence never changes the lead-level flag.

**Caveat.** 35 of the 292 transitions involve versions whose text was not stored, so the counts are lower bounds.

### Card 3. Other key articles: the account counts are small  [MODERATE]

Critical-term flips in the lead, 2021–2026 (mass2), with distinct accounts and median account age on the day of the edit:

| Article | Flips (with hash) | Distinct accounts | Top 1 / Top 3 share | Inserters / removers / both | Median age: inserts vs removes |
|---|---|---|---|---|---|
| Israel | 90 | 48 | 8% / 20% | 28 / 27 / 7 | 9.6 y vs 5.6 y |
| Hamas | 25 | 16 | 12% / 32% | 9 / 9 / 2 | 8.4 y vs 4.4 y |
| Zionism as settler colonialism | 17 | 9 | 29% / 65% | 6 / 5 / 2 | 8.2 y vs 8.9 y |
| Zionism (war window only) | 9 | 7 | 22% / 56% | 4 / 4 / 1 | 5.0 y vs 6.0 y |
| Nakba | 6 | 4 | 33% / 83% | 3 / 3 / 2 | 11 y vs 9.4 y |
| Gaza genocide | 6 | 6 | 17% / 50% | 4 / 2 / 0 | 14 y vs 3.1 y |
| 1948 Palestinian expulsion and flight | 1 | 1 | n/a | 1 / 0 / 0 | n/a |

Traced first-sentence changes (`bisect.json`):

| Article | Changes | Distinct accounts |
|---|---|---|
| Israel | 9 | 9 |
| Nakba | 12 | 10 |
| Gaza genocide | 8 | 7 |
| Hamas | 12 | 11 |
| 1948 expulsion | 9 | 9 |

No account made more than 2 traced first-sentence changes on any of these articles.

**Profile.** Virtually every account that flipped a critical term was EC at the time of collection, and none had under 500 edits, except Israel removals (5%).

**Caveat.** Medians are over events, not accounts. Several cells rest on fewer than 10 events. The Zionism and Gaza genocide lead-event lists start in 2024 because older events were truncated.

### Card 4. Tiny groups do most of the editing on some pages  [MODERATE]

**What we see.** In the war window (pilot), one account made the following share of all edits to each article:

| Article | Top-account share | Accounts editing |
|---|---|---|
| Nakba | 38.8% | 178 |
| 1948 Palestinian expulsion and flight | 22.6% | 88 |
| Gaza genocide | 18.0% | 616 |
| Zionism | 17.4% | 366 |
| Israel | 6.9% | 433 |
| Hamas | 6.8% | 550 |

Across mass2 articles with 10 or more critical-term flips:
- The median top-account share of flips is 32% on topic pages (16 articles) vs 20% on comparison pages (24 articles).
- The top 3 accounts made 56% vs 45% of those flips.

**Caveat.** High concentration on a page is common on Wikipedia, where one or two maintainers often do most of the work. The topic-vs-comparison gap rests on only 40 articles.

### Card 5. A two-camps pattern: insert and remove are mostly done by different accounts, but no more than elsewhere  [MODERATE]

**What we see.**
- Pooled over 196 topic articles with both insertions and removals of critical terms (restores excluded), 673 article-accounts were involved:
  - 318 only inserted;
  - 296 only removed;
  - 59 (8.8%) did both.
- Comparison articles show the same split: 335 / 363 / 84, so 10.7% did both.
- Israel shows it most clearly: 21 accounts only inserted, 20 only removed, 7 did both.

**Reading.** On these pages, adding and removing contested words is done by largely separate sets of accounts. The comparison group has nearly the same split, so this is how contested wording on Wikipedia generally works, not something unique to this topic.

**Caveat.** A single revert pair (one account adds, another removes) produces this pattern mechanically. The split says nothing about viewpoint or affiliation.

### Card 6. Before the war, removals on Israel came disproportionately from accounts later blocked  [LOW–MODERATE]

**What we see.**
- Israel lead, pre-war: 62% of the 24 critical-term removal events came from now-indef-blocked accounts, against 16% of the 25 insertion events.
- Removers were also younger: median 5.0 years vs 12.9 years for inserters. 21% of removal events came from accounts under 1 year old, against 0% of insertion events.
- After the war the gap closed: 16% of removal events vs 14% of insertion events came from now-indef-blocked accounts.
- At full scale (SYNTHESIS P8), pre-war topic removals by blocked accounts were 27.2% against a 20.2% base. In the war window there was **no** blocked-account excess in either direction (insertions 13.7% vs 12.3% base; removals 11.3% vs 11.0%).

**Caveat.**
- Block status is as of collection. Blocks have many causes (sockpuppetry, ECR violations, conduct).
- The share depends on how long each account had to get blocked.
- A few busy accounts produce many events.

### Card 7. Established accounts, but mostly new to each page  [MODERATE]

**What we see.**
- War-window editors were veterans:
  - Zionism: median account age 9.4 years, 99.9% of edits from EC accounts, 0% from accounts under 500 edits.
  - Gaza genocide: 9.4 years.
  - Hamas: 9.2 years.
- Few of them had edited the same page before the war. Of war-window editors, only these shares also appear among the page's 2021–mid-2023 editors:
  - Zionism: 8% (29 of 366);
  - Israel: 13%;
  - Nakba: 8%;
  - Hamas: 7%;
  - 1948 expulsion: 9%.
- Reused from SYNTHESIS P8:
  - Edits by accounts under 500 edits: 9.1% on topic pages vs 17.2% on comparison pages.
  - Accounts under a year old: 19.0% to 15.9% on topic pages (DiD −2.2 pp, project CI crosses zero).
  - Edits by accounts new that quarter: 41% in 2023-Q4, then 12–17% from late 2024 (`coordination.newcomers`).

**Reading.** The war drew experienced Wikipedians who had not worked on these particular pages before. It was not mainly a wave of brand-new accounts. That fits a topic where only EC accounts may edit.

**Caveat.** "Same page before" is computed within one pilot record. The pre-war window (30 months) is shorter than the war window (37 months).

### Card 8. Same accounts across hot articles: a tight community of regulars, not detected tag-teams  [MODERATE as a null]

**What we see.**
- Across 25 topic key articles, 216 traced first-sentence changes came from 151 accounts:
  - 27 accounts changed the first sentence of 2 or more articles;
  - **9 accounts changed 3 or more**, making 48 of the 216 changes (22%);
  - the maximum was one account on 7 articles.
- The comparison key articles had 0 accounts on 3 or more (`coordination.lead_authors`).
- Overlap among the 150 most active topic editors rose from 1.11x to 1.61x a popularity-preserving null. Comparison pages went from 1.17x to 1.08x.
- **Zero** recurring editor pairs edited within 30 minutes of each other on 5 or more articles, before or after the war, in both groups.

**Caveat.**
- Cross-article overlap arises naturally from shared watchlists and subject expertise.
- These tests cannot detect off-wiki coordination or sockpuppets that were never caught.

---

## Part 2: the public record (context only)

Sources marked **[snippet]** were read only as search-result summaries. Page fetches were blocked in this session (en.wikipedia.org could not be reached). Most press accounts come from outlets with a stated position, so they are labelled.

### Card 9. Wikipedia's governance: the topic is under the strictest standing regime  [STRONG on existence; dates partly from snippets]

**What the record says.**
- The Arab–Israeli conflict ("ARBPIA") is an Arbitration Committee contentious topic.
- Under the **extended-confirmed restriction**, only EC accounts may edit anything related to the topic, on articles and on internal discussions in every namespace except userspace. Non-EC users may only post non-disruptive edit requests.
- Uninvolved admins may block violators.
- The current general sanctions come from the 2019 case Palestine-Israel articles 4 (motion passed 6–0, 20 Dec 2019). They were amended on 14 Dec 2022, when the "contentious topics" procedure replaced discretionary sanctions.
- In Oct 2023 there were clarification requests about how ECR applies on Talk pages.

**Palestine-Israel articles 5 (opened 30 Nov 2024, closed 23 Jan 2025).**
- Reported outcome: indefinite topic bans for roughly eight editors. Counts vary by outlet: some say 8, others give splits such as "6 vs 2" or "7 vs 3" by perceived camp, or 10–11 in total.
- The committee also created a **"balanced editing restriction"**: a sanctioned user may make no more than one third of their edits in a 30-day period to ECR-covered pages.
- Grounds reported: disruptive editing and battleground conduct.
- A separate, private ArbCom case on off-wiki misconduct ended with two site bans (announced 25 Apr 2025).
- A 2026 clarification request (28 Feb 2026) asks whether Israel–Iran topics fall under ECR. Its outcome was not confirmed.

**Caveat.** The exact sanction counts should be checked on the case page.

### Card 10. Organized-effort allegations exist on several sides; Wikipedia acted mainly on conduct, not viewpoint  [the record of claims is STRONG; the claims themselves are contested]

**What the record says.**
- **2008 (pro-Israel):** leaked "Isra-pedia" emails from CAMERA. A handful of linked accounts were blocked or topic-banned.
- **2010 (pro-Israel):** training courses run by the Yesha Council and My Israel. Wikipedia's co-founder later said the effort had "no impact".
- **Oct 2024 (alleging pro-Palestinian coordination):** Pirate Wires alleged that about 40 editors coordinated, partly through the Tech for Palestine Discord. These are allegations from a partisan outlet.
- **Mar 2025:** the ADL alleged that about 30 editors coordinated. The WMF said the report's conclusions were not supported by its own data.
- **Oct 2026:** an ADL follow-up said coordinated editing had fallen by about 95% after the bans, but that biased content remained. The WMF did not comment.
- **Jan 2025:** the Heritage Foundation reportedly planned to unmask editors. In response, editors blacklisted its website as a source.
- **Aug 2025:** US House Oversight asked the WMF for records, including on "nation state actors".
- **Government involvement:** documented only in older episodes (2009–2010 programs reported by the press) and in general increases to Israel's public-diplomacy budget (2024–2026). We found **no** reputable report of 2021–2026 Wikipedia editing directed by any government.

### Card 11. How settled wording emerges, according to observers  [MODERATE]

**What the record says.** Settlement happens through formal processes rather than through any outside body:
- **RfCs and source rulings.**
  - The ADL was ruled "generally unreliable" on the Israeli–Palestinian conflict (RfC closed June 2024; more than 120 participants).
  - A Jan 2025 RfC on a Zionism lead sentence found it NPOV-compliant, followed by a one-year moratorium on rediscussing it (Mar 2025).
- **Sanctions** that remove the most active participants (PIA5).
- **Attrition.** Lir (2025, *Convergence*; 19 interviews) reports that editors described burnout and trauma, and the use of dispute processes against opponents.
- **Top-down intervention is rare and contested.** In Nov 2025, co-founder Jimmy Wales called the Gaza genocide lead non-neutral and proposed attributed wording. The page had already been locked by an admin on 28 Oct. Editors split over his intervention, and CAIR objected in writing (Dec 2025).

**Connection to our data.** Cards 2 and 8 are consistent with this account: removals of settled words are reverted quickly, and a small overlapping pool of veterans does the work. Our data cannot show that any process caused the outcome.

---

## Public-record timeline

| Date | Event | Source |
|---|---|---|
| 21 Apr 2008 | Electronic Intifada publishes leaked CAMERA "Isra-pedia" emails; linked accounts later blocked or topic-banned [snippet] | https://www.jta.org/2008/05/14/ny/latest-front-in-mideast-wars-wikipedia ; https://signpost.news/2008-05-19/Wikilobbying |
| 18 Aug 2010 | Yesha Council and My Israel run a Wikipedia editing course from a Zionist viewpoint (~50 attendees) [snippet] | https://signpost.news/2010-08-23/In_the_news (cites The Guardian, 18 Aug 2010) |
| 20 Dec 2019 | ARBPIA4 general sanctions (ECR on the whole topic area) pass 6–0 [snippet] | https://wiki.riteme.site/wiki/Wikipedia:PIA (mirror of the Wikipedia:Arbitration/Index/Palestine-Israel_articles page) |
| 14 Dec 2022 | ARBPIA remedies amended as part of the move to the "contentious topics" procedure [snippet] | same as above |
| Oct 2023 | Clarification requests on applying ECR to Talk pages after 7 Oct [snippet] | https://www.gwern.net/wiki/Wikipedia:Arbitration/Requests/Clarification_and_Amendment/Archive_125 |
| Jan 2024 | Tech for Palestine founded; reported to have a Wikipedia workgroup [snippet] | https://en.wikipedia.org/wiki/Tech_for_Palestine |
| Jun 2024 | RfC: ADL "generally unreliable" on the Israeli–Palestinian conflict; WMF defends the community process [snippet] | https://www.thewikipedian.net/p/anti-defamation-league-reliable-sources ; https://www.timesofisrael.com/wikipedia-rebuffs-jewish-groups-call-to-override-editors-move-against-adl/ |
| Jul–Sep 2024 | Press controversy over "colonization" in the Zionism first sentence [snippet] | https://jewishjournal.com/commentary/opinion/375345/wikipedia-describes-zionism-as-colonization/ ; https://jewishpress.com/news/media/social-media/war-over-wikipedias-definition-of-zionism-pits-provoked-users-against-biased-editors/2024/09/17 |
| 24 Oct 2024 | Pirate Wires alleges about 40 editors coordinated (partisan) [snippet] | https://www.piratewires.com/p/how-wikipedia-s-pro-hamas-editors-hijacked-the-israel-palestine-narrative |
| 30 Nov 2024 – 23 Jan 2025 | ArbCom case Palestine-Israel articles 5: about 8 indefinite topic bans (counts vary); balanced editing restriction [snippet] | https://signpost.news/2025-02-07/Arbitration_report ; https://forward.com/news/691180/edit-wars-over-israel-spur-rare-ban-of-8-wikipedia-editors-from-both-sides |
| 7 Jan 2025 | Forward reports Heritage Foundation plan to "identify and target" editors; editors later blacklist its site (Mar 2025) [snippet] | https://forward.com/news/686797/heritage-foundation-wikipedia-antisemitism ; https://signpost.news/2025-01-15/In_the_media |
| 4 Jan / Mar 2025 | RfC finds a Zionism lead sentence NPOV-compliant; one-year moratorium follows [snippet] | https://jewishjournal.com/news/380108/wikipedia-editors-place-moratorium-on-controversial-sentence-in-zionism-article/ |
| 18 Mar 2025 | ADL "Editing for Hate" alleges about 30 coordinated editors; WMF calls it flawed [snippet] | https://www.adl.org/resources/editing-hate-how-anti-israel-and-anti-jewish-bias-undermines-wikipedias-neutrality ; https://www.algemeiner.com/2025/03/18/malicious-wikipedia-editors-manipulated-sites-coverage-israel-adl-report-alleges/ |
| 25 Apr 2025 | Private ArbCom case: two site bans for off-wiki misconduct in PIA [snippet] | https://jewishjournal.com/news/worldwide/381221/wikipedias-supreme-court-bans-two-editors-for-offsite-misconduct-in-israel-palestine-topic-area/ |
| 2025 | Lir (*Convergence*): interviews with 19 veteran editors on burnout and harassment [snippet] | https://www.jns.org/news/u-s-news/jewish-wikipedia-editors-traumatized-after-editing-israel-related-content-study-finds |
| 27 Aug 2025 | US House Oversight letter to the WMF, including on "nation state actors" [snippet] | https://oversight.house.gov/wp-content/uploads/2025/08/082725-letter-to-Wikimedia.pdf |
| 28 Oct – 4 Nov 2025 | Gaza genocide page locked by an admin; co-founder calls the lead non-neutral; editors split [snippet] | https://www.aljazeera.com/news/2025/11/4/why-did-wikipedia-cofounder-block-edits-to-the-gaza-genocide-page ; https://www.ynetnews.com/article/9ugq7564k |
| Nov 2025 | INSS (Israel) report describes about 40 editors coordinating via Discord (policy stake) [snippet; not opened] | via https://en.wikipedia.org/wiki/Tech_for_Palestine |
| 15 Dec 2025 | CAIR letter urges the WMF board to reject the co-founder interventions [snippet] | https://www.cair.com/wp-content/uploads/2025/12/CAIR-Letter-2025-12-15b-Wikipedia-Gaza-Genocide-entry-final.pdf |
| 28 Feb 2026 | Clarification request: do Israel–Iran topics fall under ECR? (outcome unconfirmed) [snippet] | https://wikwiand-revamp.pages.dev/en/Wikipedia:ARCA |
| Oct 2026 | ADL follow-up: coordinated editing down about 95% after bans, biased content "remains"; WMF no comment [snippet] | https://jewishinsider.com/2026/10/wikipedia-editors-adl-report-campaign-anti-israel-narratives/ ; https://www.timesofisrael.com/biased-wikipedia-edits-on-israel-oct-7-remain-on-site-despite-editor-bans-adl-says/ |

Not verified in this session: the 2015–2016 origin of the 500/30 rule, and the exact PIA5 sanction count. Check both on the Wikipedia:Arbitration pages, which could not be reached here.

---

## What we can and cannot say about who

**We can say:**
- The measured changes came from anonymous accounts that were, almost without exception, extended-confirmed veterans with a median age of 5 to 14 years.
- Few accounts are involved per article: 4 to 48 distinct accounts flipped critical lead terms on each key article, and 14 accounts made the 16 traced Zionism first-sentence changes.
- On some pages a few accounts dominate the editing; on Nakba, one account made 39% of war-window edits.
- Insertions and removals are done by largely separate accounts, but the comparison topics show the same split.
- A small pool of regulars works across several hot articles: 9 accounts changed 3 or more key first sentences.
- We found no synchronized tag-teaming. In the war window, now-blocked accounts did no more than their share of the flips.

**We cannot say:**
- who any account belongs to;
- whether accounts share an operator;
- whether anyone is affiliated with or paid by any organization or government;
- what anyone intended;
- whether off-wiki coordination happened.

Our data are blind to off-wiki channels, and block status is a present-day snapshot.

**The public record alleges** coordination by pro-Palestinian editor groups (Pirate Wires 2024, ADL 2025/2026, INSS 2025) and, earlier, by pro-Israel programs (CAMERA 2008, Yesha/My Israel 2010). Wikipedia's documented response was conduct-based sanctions (PIA5, the 2025 private case) and source rulings (ADL, Heritage). These allegations **do not map onto our measured edits**. We have not linked, and by design cannot link, any hashed account to any named editor, group or report. Nothing here should be read as saying that a particular change was made by a particular camp.
