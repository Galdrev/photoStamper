# Pilot evaluation: new signals for 168 articles

Evaluator's report on `data/pilot/pilot.json` and `summary.json` (collected 2026-11-05, 7,517 requests, 115 min).

- **Strata.** 166 live records: topic 60, dispute comparison ("disp") 40, random comparison ("rand") 60, atrocity 6. Masalit massacres and El Geneina massacre were missing, so Sudan 2023 is not covered.
- **Windows.** w1 = 2021-01-01 to 2023-07-01 (pre-war, 30 months). w2 = 2023-07-01 to now (40 months). war = 2023-10-07 to now (a subset of w2).
- **Analysis.** Scripts are in the scratch folder. Chart data is in `chart_data/`, cards in `cards.json`, and the scaling plan in `mass_scope.json`.
- **Privacy.** No usernames are read or stored. Account counts below are derived from salted hashes and per-article shares, and no hash is written to any output.

---

## 0. Top findings

| # | Finding | Confidence |
|---|---|---|
| 1 | **Account profile.** Topic pages are edited by older, extended-confirmed accounts and are reverted less often. Edits by accounts with under 500 edits: 4% topic, 11% disp, 21% rand. Reverted share: 8.6% topic vs 18.2% disp. | STRONG (pilot n 60/40/60, p<0.001) |
| 2 | **Blocked accounts.** Now-indef-blocked accounts are over-represented in lead critical-term flips on topic pages. This holds for both insertions and removals, and a few accounts account for most of it. There is no such excess in disp. | SUGGESTIVE |
| 3 | **RfCs.** Topic RfCs rose from 11 to 88 between w1 and w2, while disp fell from 15 to 6. 64 of the 88 are on 4 pages. | SUGGESTIVE |
| 4 | **Atrocity voice.** Stating "genocide" in Wikipedia's voice is not unique to Gaza: Rohingya, Yazidi, Bosnian and Armenian do it too. The Uyghur article moved the other way in 2024. Gaza differs in speed and in how far the label reached (infobox, categories, short description). | ANECDOTE |
| 5 | **Short descriptions.** They change along with the lead, everywhere. On 5 flagship topic pages they now state a framing term (comparison: 0). | SUGGESTIVE |
| 6 | **Edit sizes.** Post-war growth came from 3.7x as many edits per month. Bytes per edit and churn stayed the same. | SUGGESTIVE |
| 7 | **Link diffusion.** Diffusion along links is modest once renames are resolved. Raw `watch_links` growth is mostly page moves. | SUGGESTIVE |
| 8 | **Protection.** Protection and contentious-topic (CT) notices spread in topic and disp alike. Protection marks the core pages; it does not predict change. | SUGGESTIVE |
| 9 | **LiftWing.** It works (433/433 calls, AUC 0.75) and treats insertions and removals alike. | SUGGESTIVE |
| 10 | **Categories and citations.** Categories show no reframing. Lead citations rose 33% in topic and fell 12% in disp, while the source mix moved as it did everywhere. | ANECDOTE / SUGGESTIVE |

---

## 1. Data quality per signal

### 1.1 Coverage (share of 166 live records)

| Signal | Coverage | Notes |
|---|---|---|
| Article wikitext @2021 / @2023 / now | 93% / 95% / 100% | Gaps are articles created later (Gaza war, Gaza genocide, October 7, etc.; 11 created in-window). |
| Talk wikitext @3 dates | 93% / 95% / 100% | |
| Short description @3 dates | 57% / 86% / 97% | The 2021 gap is real: short descriptions were still being rolled out. Some are literally `none` (6 topic, 8 rand). |
| Infobox | 56–66% | |
| Wikidata @3 dates | 93% / 95% / 99% | One 2021 snapshot caught a vandalised description (Zionism: "Jewish efterblivna nationalist movement"). |
| Protection at dates | 100% "known" | **But it is a lower bound** (see 1.3). |
| Pageviews | 100% | Includes the partial current month (4 days of Nov 2026), which biases the w2 mean by about −2%. |
| Watchers | 78% (rand 53%) | Hidden below 30 watchers, by design. |
| Revisions / talk revisions | 100%, none truncated | |
| Account facts | 100% of articles with registered edits | |
| Lead term events | 100% non-null; **w2 truncated for 6 topic articles** | Zionism stops at 2025-02, Israel at 2025-10, Hamas at 2024-10, October 7 at 2024-06, Gaza genocide at 2024-07 and Gaza war at **2023-10-07**. The key 2024–26 voice changes on these pages are therefore missing. |
| LiftWing | 433 calls, 0 failures | Cap of 12 per article: 433 of 662 distinct event revisions were scored. |
| RfC/RM scan | 100%; 1 archive list truncated; 4 undated | |
| Abuse log | 100% "present" but **unusable** | 0 hits in w1 for every stratum. Hits on 6 topic articles in w2 only. All filter names are blank (private filters). |
| Inbound links (`linksto:`) | 100% | Current state only. |

### 1.2 Five records checked by hand

- **Zionism (topic, key).**
  - Revisions, protection (EC), 0 anonymous edits under EC, and talk class all fit.
  - Lead citations went from 25 to 107. This is real: 95 of them are `{{sfn}}` short footnotes.
  - Lead events: 0 in w1. In w2, 28 events, truncated at 2025-02, so the 2026-08-27 "colonial" lock-in (SYNTHESIS) is **not** in the pilot.
  - The 2021 Wikidata English description is vandalised.
- **Nablus (topic, narrative).** Consistent throughout: GA class, ARBPIA notice, EC protection, a short description that became "Palestinian city in the northern West Bank", and 0 lead term events (its lead has no critical terms).
- **Kosovo (disp).** Consistent. The CT notice appears only in 2026 (topic "ee"). One lead citation in 2023 is classed "Israeli press", which looks like a classifier misfire.
- **Karbala (rand).** Consistent. 36–40% of edits are anonymous, there is no protection, and there are no events.
- **Rohingya genocide (atrocity).** Consistent. The CT notice is "ipa", which is correct. The short description changed from "Ongoing ethnic cleansing in Myanmar (Burma)" to "Ongoing genocide in Myanmar" after 2023-07. Lead genocide count is 7 at all three dates.

### 1.3 Problems found (fix before scaling)

1. **The `summary.json` screen double-counts topic articles.** `screen()` appends each value to both `vals[stratum]` and `vals[group]`, and these are the same key for topic. As a result `n_topic` is 2x, and `std_diff` and `p_perm` are wrong (too small), although the means are unaffected. The "comparison" pool also includes the atrocity stratum. All the screens below are recomputed with each article counted once, using Cliff's delta and a permutation test.
2. **The "48% indef" figure is an unweighted mean over 12 articles.** The pooled share is 34% (section 3.1).
3. **Protection reconstruction is a lower bound.** 12 of 168 current protections are missed. 415 log entries (mostly from before 2013) have no `details`, `move_prot` entries carry no levels, and logs filed under former titles are not fetched. Fix: parse the old log params, follow moves, and anchor the current level on `page_info`.
4. **Lead term events.** There are three problems.
   - The 40-page cap truncates the heaviest pages (see the table above).
   - The first revision of each window only seeds the state, so a change made in that revision is lost.
   - An "insert" includes **restoring** a term by revert, so the account that "inserts" may be undoing someone else's removal. These cases need to be tagged separately.
5. **`watch_links` are not redirect-resolved.** Renames inflate growth. Example: "1948 Palestinian exodus" became "1948 Palestinian expulsion and flight", which made that link go 0 → 9 when the concept actually went 9 → 11 (section 3.3).
6. **Account facts.**
   - "indef" means any block with infinite expiry, partial (page or namespace) blocks included.
   - It is the status at collection time.
   - The reason for the block is not recorded.
   - Per-event account flags are not stored, so linking block status to events has to be inferred (section 3.1).
7. **Titles and moves.** `title_at` returns a pre-creation title for dates before the page existed. The move `rm` flag is a loose regex: a vandal move ("Make Israel Great Again") and its revert are counted as RM moves. RM results were parsed for only 7 of 45 topic RMs.
8. **Atrocity stratum.** "Darfur genocide" is now a disambiguation page, because the article was moved to "Darfur genocide (2003–2005)" on 2025-12-02, so the record is empty. The two Sudan titles were missing. "Uyghur genocide" resolves to "Persecution of Uyghurs in China", which is fine but is a renamed page.
9. **Lead citations are stored as classes, not domains.** Per-outlet questions such as ADL or Al Jazeera cannot be answered. The "Other" class is 17–54% depending on the stratum.
10. **Categories** are explicit `[[Category:]]` links only. Template-added categories are missed.
11. **`shortdesc_from_wikidata` is 0 everywhere.** English Wikipedia no longer uses central descriptions. **`dispute_tag`** is almost always 0. Both are uninformative.
12. **Bandwidth.** 1.75 GB for 168 articles, mostly the 50-revision lead-content pages. Plan disk and time for the mass run.

---

## 2. Screen of every signal

Full table: `chart_data/screen_all.json`. It has 153 level metrics and 104 change metrics, each with n per stratum, mean, median, Cliff's delta for topic vs disp and topic vs rand, and permutation p values. Atrocity is reported separately (n ≤ 6).

### 2.1 Separates topic from disp (Cliff |δ| ≥ 0.3, p < 0.05), and usually from rand as well

| Metric (war window unless noted) | topic | disp | rand | n (t/d/r) | δ vs disp | δ vs rand |
|---|---|---|---|---|---|---|
| Edits by accounts with <500 edits | 4.1% | 11.3% | 20.6% | 60/40/59 | −0.42 | −0.64 |
| Extended-confirmed now | 95% | 88% | 79% | 60/40/59 | +0.38 | +0.58 |
| Median account age (days) | 3,471 | 2,495 | 2,242 | 60/40/59 | +0.41 | +0.44 |
| Accounts < 30 days | 2.2% | 6.1% | 6.8% | 60/40/59 | −0.42 | −0.48 |
| Reverted share of edits | 8.6% | 18.2% | 8.9% | 60/40/60 | −0.59 | +0.03 (n.s.) |
| Empty edit summary | 10.6% | 16.1% | 21.5% | 60/40/60 | −0.45 | −0.53 |
| Watch-list links in article (now) | 4.05 | 0.73 | 0.05 | 60/40/60 | +0.62 | +0.79 *(by construction: the list is topic-centred)* |
| Israeli press share of lead citations | 6.8% | 0 | 0 | 55/40/51 | +0.40 | +0.40 *(by construction)* |

### 2.2 Separates topic from rand but not from disp (a "contested topic" signal, not a topic-specific one)

These signals are useful as markers of contested topics but do not single out this topic:

- EC protection now: 63 / 45 / 3%
- CT notice: 67 / 48 / 3%
- Talk/article edit ratio, talk edits per month, watchers, talk archives, class rank, redirects, views
- `cmt_npov`, `cmt_consensus`, `cmt_voice`, `cmt_title_name` summary classes
- Inbound links (topic 3.4k vs disp 6.4k, n.s.)

### 2.3 Changed differently in topic (Δ war − w1, or 2023 → now)

| Change | topic | disp | rand | n (t/d/r) | δ vs disp (p) |
|---|---|---|---|---|---|
| Edits per month | +18.3 | −6.7 | +0.5 | 60/40/60 | +0.65 (0.005) |
| Views per month | +44k | −28k | −0.1k | 57/39/56 | +0.78 (<0.001) |
| Talk edits per month | +22.3 | −3.8 | +0.1 | 60/40/60 | +0.43 (0.03) |
| Critical lead insertions per month | +0.031 | −0.028 | −0.004 | 60/40/60 | +0.32 (0.009) |
| RfCs per year | +0.40 | −0.10 | 0 | 60/40/60 | +0.23 (0.05) |
| Net KB added (war − w1) | +15.8 | −6.7 | +4.3 | 56/39/55 | +0.41 (0.03) |
| Lead citation count, 2023 → now | +4.7 | −3.1 | +0.2 | 56/39/57 | +0.25 (0.06) |
| English Wikidata description changed, 2023 → now | 68% | 38% | 36% | 57/39/56 | +0.30 (0.008) |
| Hebrew Wikidata description changed, 2023 → now | 40% | 5% | 13% | 57/39/56 | +0.35 (<0.001) |
| Watch links added, 2023 → now *(raw, inflated by renames)* | 1.38 | 0.13 | 0.02 | 56/39/57 | +0.42 (<0.001) |
| Indef share among critical inserters, war − w1 | −0.50 | +0.30 | – | **8/7/0** | −0.68 (0.01) |
| Mobile *view* share | +6.3 pp | +2.2 | +2.7 | 57/39/56 | +0.35 (0.001) |

**What does not separate:**

- **Lead critical rate per 10k words, 2023 → now:** topic +2.9, disp +2.6, n.s. This pilot sample is too small for the main outcome; the mass tier already measures it.
- Short description changed (62 / 49 / 48%, n.s.)
- Categories added
- Dispute tags
- CT notice change
- Revert-risk of insertions
- Account-age shares of inserters (n ≤ 27 articles)

Cells for disp_P events, rand inserters and atrocity are tiny (n 0–7). Do not read them.

---

## 3. Deep dives

### 3.1 Accounts that inserted (and removed) critical terms, now indefinitely blocked

**Method.**

- **Events.** An event is a lead critical-term presence flip between consecutive revisions.
- **Account status.** It comes from `term_events.by_window` (the per-article share of events whose account is now indef-blocked) and is converted to counts.
- **Base rate.** The share of all registered non-bot edits to the same articles in the same window (`win.*.accounts.share_indef_now`, edit-weighted).
- **Number of distinct blocked accounts.** I solved an integer program over the salted hashes: which accounts must be blocked so that every per-article share is matched, with each hash's status the same across articles. This gives a minimum and maximum. No hash is reported.

**Events** (registered accounts only; "base" = share of all registered edits to the same stratum's articles):

| Window | Stratum | Kind | Articles | Events | By now-indef accounts | Pooled share | Article mean | Base (same articles) |
|---|---|---|---|---|---|---|---|---|
| w1 | topic | insert | 12 | 62 | 21 | **34%** | 48% | 26% |
| w1 | topic | remove | 12 | 62 | 35 | **56%** | 50% | 25% |
| w1 | disp | insert | 18 | 71 | 11 | 15% | 10% | 18% |
| w1 | disp | remove | 17 | 61 | 11 | 18% | 21% | 18% |
| war | topic | insert | 23 | 142 | 21 | 15% | 12% | 10% |
| war | topic | remove | 23 | 135 | 22 | 16% | 14% | 9% |
| war | disp | insert | 13 | 52 | 8 | 15% | 21% | 15% |
| war | disp | remove | 16 | 42 | 6 | 14% | 13% | 15% |
| w2 | topic | insert | 24 | 148 | 21 | 14% | 12% | 10% |
| w2 | topic | remove | 23 | 139 | 23 | 17% | 14% | 9% |

Rand and atrocity have 0–5 events per cell, which is too few to read.

**Accounts.**

- **w1 topic, insert.** 22 inserting accounts, of which **exactly 6** are now indef-blocked. Their events: 8, 5, 5, 1, 1, 1, so **3 accounts made 18 of the 21**.
- **w1 topic, remove.** 9 to 11 of 26 accounts; the top 3 made 26 of 35 events.
- **w1 topic, insert and remove together.** 11 to 13 of 38 accounts, and 3 of them made 44 of 56 events.
- **w1 disp, insert.** 6 to 8 of 44 accounts, spread out (at most 4 events each).
- **War topic, insert.** 10 to 15 of 73 accounts (the top 4 made 15 events). War topic, remove: 10 to 17 of 73.
- **Overall pattern.** Pre-war it is **a handful of accounts**. Post-war it is a **small minority of many** accounts.

**Concentration and robustness.**

- **Israel.** Israel holds 27 of the 56 pre-war events by now-indef accounts. On Israel itself, insertions by indef accounts (8 of 35, 23%) are *below* that page's base (33%). Removals are above it (19 of 35, 54%).
- **Excluding Israel.** The pre-war excess holds on small counts: insertions 13 of 27 (48%) and removals 16 of 27 (59%), against a base of 22%.
- **Accounts on both sides.** 4 of the 12 pre-war indef accounts in topic both inserted and removed terms.

**Fate of the insertions.**

| Window | Inserts reverted, indef accounts | Inserts reverted, other accounts | Removals reverted, indef | Removals reverted, other |
|---|---|---|---|---|
| w1 topic | 38% | 17% | 46% | 41% |
| war topic | 48% | 21% | 35% | 35% |

These are minimum-solution labels; the w1 insert labels are unique.

**Base rates.** Across all registered edits, the share made by now-indef accounts is 25% in w1 topic, 21% in disp, 14% in rand and 24% in atrocity. In the war window it is 10% topic, 12% disp, 11% rand and 6% atrocity. The drop from w1 to the war window happens in every stratum. That is mostly **time at risk**: accounts active in 2021–23 have had 3 to 6 years to be blocked.

**What the data can show.** On Israel/Palestine leads, the flips of critical terms, in both directions and removals even more than insertions, involve now-blocked accounts more often than ordinary editing on the same pages does. Before the war this is a few accounts. After the war it is about 1 in 7 flip edits, against 1 in 10 edits overall. Dispute comparison topics show no such excess. Insertions by these accounts were reverted about twice as often as other insertions, so blocked accounts are not the main source of the wording that stuck.

**What it cannot show.**

- **Why they were blocked.** In this topic area indef blocks often follow sockpuppetry investigations or arbitration enforcement, but vandalism, compromised accounts and self-requested blocks also exist. The pilot does not record the reason, or whether the block is sitewide or partial.
- **Viewpoint.** Which side any account was on cannot be told. "Insert" includes restoring a term that someone else removed, so an inserter can be reverting a blocked remover, and the reverse.
- **Status at the time.** Block status at the time of the edit is unknown.
- **Coordination.** This says nothing about coordination, and it is not evidence of a campaign by one side.

### 3.2 Extended-confirmed protection and CT notices

| | 2021-01 | 2023-07 | now |
|---|---|---|---|
| EC edit protection: topic / disp / rand / atrocity | 47 / 10 / 0 / 0% | 52 / 25 / 0 / 0% | 63 / 45 / 3 / 17% |
| Semi-protection: topic / disp | 0 / 25% | 0 / 20% | 2 / 13% |
| CT notice: topic / disp / rand | 57 / 31 / 0% | 59 / 38 / 0% | 67 / 48 / 3% |

**Relation to change.**

- **Topic.** Pages EC-protected in Jul 2023 later gained lead critical terms in 14 of 31 cases (45%), against 1 of 25 unprotected pages (4%). The protected pages also had higher edit growth (median log growth 0.25 vs 0.12).
- **Disp.** No difference: 3 of 10 protected vs 8 of 29 unprotected.
- **Newly protected pages after 2023.** No more change than others (topic 1 of 5).

Protection therefore marks which pages are the core, not a mechanism of change. The topic's extended-confirmed restriction applies regardless of technical protection, which limits what page protection can explain. Dispute topics also moved toward EC protection, from 10% to 45%.

### 3.3 Watch links: diffusion of concept links

**Raw counts.** In the 54 topic articles present at all three dates, links to watch-list concepts went from 143 to 160 to 200; in the lead, from 77 to 88 to 97. Dispute: 32, 26, 26. Random: about 0.

**Alias-resolved counts** (articles linking to the concept):

| Concept (aliases) | 2021 | 2023 | now |
|---|---|---|---|
| Palestinian 1948 expulsion / Nakba ("1948 Palestinian exodus", "An Nakba", ...) | 9 | 10 | 11 |
| Israeli apartheid ("Israel and the apartheid analogy", "Israel and apartheid") | 1 | 4 | 6 |
| Settler colonialism (+ "Zionism as settler colonialism") | 0 | 2 | 4 |
| Gaza genocide | 0 | 0 | 5 |
| Israeli occupation (various) | 17 | 18 | 20 |
| Genocide / Ethnic cleansing (generic) | 8 | 8 | 12 |
| Land of Israel / Israelites / Jewish history | 17 | 20 | 23 |
| Jewish exodus from Arab and Muslim countries | 9 | 8 | 9 |
| Antisemitism / New antisemitism | 15 | 13 | 14 |

**Inbound links, now** (only current counts exist): Antisemitism 8,000, Zionism 6,669, Anti-Zionism 2,601, Gaza genocide 2,278, 1948 Palestinian expulsion and flight 1,307, Nakba 955, Israeli apartheid 794, Zionism as settler colonialism 412.

**Conclusion.** The diffusion is real but modest (a few articles per concept). It runs in both narrative directions, and most of the raw growth is renames. For the mass run, resolve links through a redirect table and get inbound history from the pagelinks dumps, not from the API.

### 3.4 Short descriptions and Wikidata descriptions

**Co-movement with the lead.**

- Short description changed from 2023-07 to now: topic 35 of 56 (62%), disp 49%, rand 48%.
- Among topic articles whose lead gained critical terms, 11 of 13 changed it, against 24 of 43 that did not.
- In disp, 8 of 8 against 11 of 31.

So the short description moves with the lead everywhere; this is not topic-specific.

**Framing terms in short descriptions.** Topic 3 of 56 in 2023 and 5 now; comparison 0. Examples:

- **Israeli apartheid.** "Comparison of Israel's treatment of Palestinians to apartheid" (2021) → "Accusation that Israel's actions rise to the crime of apartheid" (2023) → "Israeli system of racial segregation and discrimination" (now). This is attributed → stated.
- **Nakba.** "Fracturing, dispossession, and displacement of Palestinian society" → "Ethnic cleansing of Palestinians".
- **1948 Palestinian expulsion and flight.** "Expulsion and flight of Palestinians during the 1948 Palestine war" → "Ethnic cleansing, expulsion, and flight of Palestinians during the 1948 Palestine war".
- **Israeli settlement.** "Israeli communities built on land occupied in the 1967 Six-Day War" → "Illegal Israeli communities built on land occupied in the 1967 Six-Day War".
- **West Bank.** "Territory claimed by the State of Palestine" (2021) → "Territory in West Asia" (2023) → "Palestinian territory occupied by Israel".
- **Other direction and neutral rewordings:**
  - Hamas: "Palestinian Sunni Islamic militant nationalist organization" → "Islamist Palestinian political and paramilitary organization".
  - Zionism: "Movement supporting a Jewish homeland" → "Jewish nationalist movement".
  - October 7 attacks: "2023 armed incursions and massacres in Israel".

**Wikidata.** The English description changed in 68% of topic articles and 38% of disp. It sometimes diverges from the enwiki short description:

- October 7 attacks, Wikidata: "terrorist attack and massacre ... carried out by the Islamic Fundamentalist Terrorist Group Hamas", against the enwiki "2023 armed incursions and massacres in Israel".
- Hezbollah, Wikidata: "... terrorist organization in Lebanon".

Hebrew and Arabic descriptions changed in 40% and 42% of topic articles, mostly rewording within each community's own framing (Nakba in Hebrew: "... during the War of Independence of the State of Israel in 1948"). The short description and the English Wikidata description are identical in only 23% of topic articles.

### 3.5 Lead citations

Pooled over articles present at all three dates:

| | 2021 | 2023 | now |
|---|---|---|---|
| Topic lead citations | 711 | 727 | **965** |
| Disp lead citations | 799 | 997 | **876** |
| Rand lead citations | 206 | 248 | 260 |
| Scholarly share, topic / disp / rand | 53 / 42 / 33% | 58 / 56 / 38% | 67 / 67 / 42% |
| Topic: Rights & UN | 1.8% | 1.9% | 2.9% |
| Topic: Israeli press | 5.1% | 5.2% | 5.2% |
| Topic: Pro-Israel advocacy | 1.3% | 0.8% | 0.4% |
| Topic: Arab & pro-Palestinian | 0.6% | 0.8% | 0.9% |

Contested topic leads were cited more heavily, mostly with scholarly short footnotes. Zionism's lead alone went from 25 to 107 citations. The class mix moved as it did in the comparison groups. Domains are not stored (see 1.3, problem 9).

### 3.6 Categories, See also, navboxes, infobox

**Framing categories** (genocide, colonial, apartheid, occupation, massacre, terror, Zionism, antisemitism), 2023-07 → now:

- Topic: 29 added, 15 removed across 56 articles. The additions run in both directions:
  - terrorist-designation categories (Hamas 5, Hezbollah 2)
  - "Massacres of Jews" (Bar Kokhba Revolt, Farhud)
  - "Israeli apartheid" (2)
  - "History of colonialism" (Balfour Declaration)
  - "Terrorist incidents against Muslims" (Nakba, Cave of the Patriarchs)
- Disp: 10 added, 9 removed. Rand: 0 and 0.

There is **no settler-colonialism category reframing** in the topic sample. "Settler colonialism in Asia" was added to the Uyghur article instead.

**Gaza genocide** now sits in "21st-century genocides", "Genocide of indigenous peoples in Asia" and "Incitement to genocide of Palestinians". Rohingya and Yazidi also gained "21st-century genocides", and Armenian gained "Genocide of indigenous peoples in Asia".

**Other structure.** See also links: +0.9 per topic article vs +0.1 disp (n.s.). Navboxes: +0.4 vs +0.2 (n.s.). Categories overall: +1.8 vs +0.4 (δ 0.29, p 0.06).

**Infobox** fields carry voice:

- Nakba gained an infobox whose type field begins "Genocide, ethnic cleansing, forced displacement, dispossession, mass killing, settler colonialism, ...".
- Gaza genocide's type field begins "Genocide, war crimes, crimes against humanity, ...".
- The Uyghur infobox type field does not contain "genocide".

There are 16 framing-term infobox field changes in topic, 8 in disp and 15 in atrocity (many of them field renames).

### 3.7 Talk: RfCs and requested moves

| | RfC w1 → w2 | Articles with RfC (w2) | RM w1 → w2 | RfCs closed (w2) |
|---|---|---|---|---|
| Topic (60) | 11 → **88** | 12 | 12 → 45 | 40 of 88 |
| Disp (40) | 15 → 6 | 4 | 16 → 14 | 3 of 6 |
| Rand (60) | 0 → 0 | 0 | 0 → 0 | – |
| Atrocity (6) | 2 → 0 | 0 | 4 → 1 | – |

**Where.** In w2, Gaza war has 22 RfCs and 20 RMs, Gaza genocide 21 and 10, October 7 attacks 13 and 12, and Zionism 13 RfCs. Pre-war, 8 of the 11 RfCs were on Israel.

**Timing.** Per-RfC dates are reduced to window totals in the pilot, so finer timing needs the mass run to keep each date.

**Moves with timestamps:**

- Gaza genocide: "Allegations of genocide in the 2023 Israeli attack on Gaza" → "Gaza genocide" on 2024-07-03, after an RM. This came after a same-day move to "Attempted genocide ..." on 2024-02-29, which was reverted.
- October 7 attacks: 12 moves in 2023-10 to 2025-05.
- Israeli apartheid: "Israel and the apartheid analogy" → "Israel and apartheid" (2022-09, RM) → "Israeli apartheid" (2024-08-05).
- 1948 Palestinian expulsion and flight: renamed from "1948 Palestinian exodus" (2022-10 RM, reverted 2022-12, re-done 2023-03 RM).

**Outcomes.** Not reliable: RM results were parsed for 7 of 45 topic RMs (3 moved, 4 not moved).

### 3.8 Edit sizes

| | Edits/month w1 → w2 | Net bytes per edit w1 → w2 | Removed / added w1 → w2 | Median net KB/article (war) |
|---|---|---|---|---|
| Topic | 373 → 1,384 | 56 → 53 | 0.82 → 0.82 | 11.2 |
| Disp | 563 → 348 | 33 → 52 | 0.81 → 0.84 (0.92 in war) | 5.5 |
| Rand | 127 → 153 | 41 → 83 | 0.75 → 0.51 | 1.6 |

The topic grew through volume, not through bigger or more destructive edits. Mean net growth per article in the war window is +47.6 KB for topic vs +8.3 KB for disp (δ +0.30, p 0.02).

### 3.9 Revert-risk (LiftWing)

- **Did it work?** Yes: 433 of 433 calls succeeded with 0 failures.
- **Validity.** AUC against the `mw-reverted` tag is 0.75 (topic 0.69, n 209; disp 0.77, n 192).
- **Direction.** Topic insertions average 0.615 and removals 0.631. Among unreverted edits, 0.583 and 0.599. Disp: 0.68 and 0.72. Rand removals score 0.885, but n is 13.
- **What drives it.** Anonymous edits score 0.95 and registered ones 0.62, so the model is largely a proxy for user type.
- **Conclusion.** There is no directional asymmetry. As a fairness check this answers SYNTHESIS question 7 ("no difference detected"). Its marginal value for the mass run is low.

### 3.10 Atrocity comparison: voice of the genocide label

Sources: pilot titles, moves, short descriptions, Wikidata descriptions, infoboxes and categories, plus first sentences from `data/leads.json`. Table: `chart_data/atrocity_voice.json`.

| Article | Title | Short description now | First sentence 2021 → 2026 | Change after 2023 |
|---|---|---|---|---|
| **Gaza genocide** | allegations → **stated** (RM 2024-07-03) | "Ongoing genocide in the Gaza Strip" | (2024-01 attributed: "Allegations have been made ...") → stated | attributed → stated within 21 months; infobox and categories as well |
| Rohingya genocide | stated | "Ongoing genocide in Myanmar" | stated → stated | short description upgraded from "ethnic cleansing" |
| Yazidi genocide | stated (2025-08 move to "Persecution of Yazidis" reverted) | "2014-2017 genocide campaign by the Islamic State" | n/a | survived a de-escalation attempt |
| Bosnian genocide | stated | "1995 genocide in Bosnia and Herzegovina" | stated → stated | short description upgraded to the label |
| Armenian genocide (disp) | stated | "Systematic campaign in the Ottoman Empire" | stated → stated | none |
| **Persecution of Uyghurs** | **stated → neutral** (RM 2024-02-27) | "none" | attributed → attributed ("often been characterized as persecution or as genocide") | de-escalated |
| War crimes in the Tigray war | no label | "none" | Tigray war lead: "accused of genocide" | attributed |
| Darfur genocide | stated | – | n/a (record now a disambiguation page) | – |

Gaza is not alone in being stated in Wikipedia's voice. What is distinctive is the speed and the timing (during an ongoing war, with the ICJ case pending), and the spread of the label into the infobox, categories and short description. The Rohingya article, whose ICJ case is also pending, was already stated in 2021. The Uyghur article moved the other way in the same period. The n is tiny (ANECDOTE), and the Sudan 2023 cases are missing.

---

## 4. Shortlist for the mass rerun

The plan covers about 9,062 unique articles in 4 shards, with a ceiling of 300k requests. Full detail is in `mass_scope.json`.

**Cost basis.**

- The pilot cost model reproduces 6,124 of the 7,054 successful pilot requests, so the model is calibrated by x1.15.
- That model is applied to the mass edit distribution (median 76 edits since 2021, p99 1,732).
- 6% is added for 429 retries.
- The existing mass run already costs about 4.2 requests per article (3 snapshots plus about 1.16 history pages).

### 4.1 Free (no extra requests)

**Revision metadata.** Add `size|comment|flags|sha1` to the history `rvprop` mass already pages through. This gives:

- edit sizes (added, removed, net, big adds and removes)
- tags (mw-reverted, reverting, mobile, VisualEditor)
- hidden revisions
- edit-summary classes (reduce summaries to flags in memory)
- page moves and titles at each date
- top-editor share, anonymous and bot shares

**Parse the existing 3 snapshots:**

- short description
- infobox type and key fields
- lead image
- explicit categories
- See also and navboxes
- **alias-resolved** concept links
- lead citation classes and **domains**
- the disp_P / disp_J split
- maintenance and pp templates
- headings

### 4.2 Scale (ranked by interest × separation × quality / cost)

| Rank | Signal | Requests/article | Why |
|---|---|---|---|
| 1 | page_info batched (current protection, watchers, short description, QID, assessments) | 0.05 | Ground truth for "now"; cheap |
| 2 | Account facts (age, edit count, EC, block incl. partial flag) | 0.5 | Strongest separator; needs a fixed salt |
| 3 | Talk wikitext **now only** (CT notice, class, press, FAQ) | 1.0 | Separates from rand; old dates add little |
| 4 | Inbound links for the ~35 watch concepts only | ≈0 (35 total) | Diffusion targets |
| 5 | Pageviews all-access, summed over former titles from moves | 1.3 | Exposure weighting (data note 3) |
| 6 | Talk revision history | 1.2 | Talk volume, participants, overlap |
| 7 | RfC/RM scan (keep per-discussion dates, better close parsing) | 1.3 | Process question (SYNTHESIS question 4) |
| 8 | Wikidata now (batched) + snapshot at 2023-07-01 | 1.0 | Reuse surfaces |
| 9 | Protection log (with the parsing fixes from 1.3) | 1.0 | Platform-rule question; a lower bound without the fixes |
| 10 | Lead term events w1 + w2, with insert / remove / restore split and per-event hashed account flags | 5.0 | Needed for who-inserts and who-removes. The cheaper variant (only pages whose lead changed between snapshots, plus all topic pages) costs about 1.6 |

**Optional: LiftWing** at a cap of 6 per article, about 1.0 request per article. It works but shows no asymmetry.

### 4.3 Drop

- Talk snapshots at 2021 and 2023 (saves 2 requests per article)
- `linksto:` for every article (1 per article)
- Abuse log (1)
- AfD lookup (1)
- `shortdesc_from_wikidata` (always 0)
- `dispute_tag` as a headline metric (near 0)

### 4.4 Cost

| Item | Requests/article | Total (9,062 articles) |
|---|---|---|
| Existing mass run | 4.2 | ~38k |
| Recommended extras, raw | 12.35 | – |
| Recommended extras, with calibration (x1.15) and retries (+6%) | **≈15.1** | ≈136k |
| **Total** | – | **≈177k** (≈59% of the ceiling), about 44k per shard |
| Total with LiftWing | ≈16.3 extra | ≈188k |
| Using the cheaper lead-event variant | – | about 147k |

There is room to raise the lead-event cap on the roughly 1% heaviest pages (needed for Gaza war, Gaza genocide, Zionism and Israel), which adds about 2k requests. Plan for about 10 MB per heavy article of downloaded content.

**Fix before the run** (section 1.3): the screen double-count, the protection parsing, the lead-event window boundary and restore tagging, redirect resolution for links, the partial-month pageviews, the atrocity titles, and a fixed salt across pilot and mass.
