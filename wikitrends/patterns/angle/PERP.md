# Who does the harm? Perpetrators in the opening paragraphs, 2021 → 2023 → now

**Question.** When the most-read English Wikipedia articles on Israel, Palestine, Zionism and Judaism open with violence, harm, displacement, legal charges or rights, who is named as the one doing it? Israel and Jews, Hamas and Palestinians, someone else, or nobody? Is it said in Wikipedia's own voice, or attributed to a source? And what is the charge?

**Bottom line.** The *share* of harm sentences that name Israel or Jews as the perpetrator barely moved: 23.6% (Jan 2021), 24.1% (Jul 2023), 26.4% (now), and the change is not statistically clear. What changed is the *charge*. Before July 2023 no lead in the set accused Israel of genocide. Now 8 sentences in 7 leads do, and 2 of them say it in Wikipedia's own voice: the **Israel** article ("Israel began committing genocide against Palestinians in Gaza") and the **Benjamin Netanyahu** article ("Netanyahu's government has been orchestrating the Gaza genocide"). Occupation moved from attributed to stated as fact (46% to 80% own voice). The 1948 story moved from "fled or were expelled" to "expelled by Zionist/Israeli forces". The Hamas side is still named as a perpetrator in Wikipedia's own voice at about the same rate, but the "terrorist" label is now further from the text.

## Method in one paragraph

- **Articles.** The 150 most-viewed topic-group articles in the mass crawl (`data/mass2.json.gz`; views are monthly user views summed Jan 2021 to Oct 2026, current and former titles) that have a lead at all three dates (`data/mass2_leads.json.gz`: 2021-01-01, 2023-07-01, now = 2026-11-05). The set is what the readers read. That puts Hitler, the Holocaust, Oppenheimer and Anne Frank next to Israel, Hamas and Gaza. A **conflict subset** (54 of the 150 articles, any sentence with an Israeli, Jewish or Palestinian perpetrator, or an Israeli or Palestinian victim) is reported as well.
- **Comparison.** 50 high-view articles on other disputes, each with its own two sides: Ukraine/Russia (21 articles), Karabakh/Armenia (15), Northern Ireland (7), Kosovo (4), Cyprus (3), Kashmir (3).
- **Coding.** The leads were split into sentences. A keyword prefilter gave 2,786 candidates. The coder (Claude, reading every sentence) kept 1,731 unique sentences (2,012 sentence-date rows) that describe violence, harm, displacement, legal charges or rights. For each one it recorded the perpetrator *named as the agent* (passive voice with no agent = unclear), the victim, the voice (own / attributed / denied-disputed) and the charge class. Every sentence and code is in `perp_codes.jsonl`. Numbers are in `perp_results.json`. The codebook is in `perp_validation.md`.
- **Validation.** 100 rows were hand-rechecked: perpetrator precision 98%, voice precision 99% (60 random rows, plus 40 rows with an Israeli/Jewish or Palestinian perpetrator). This is a self-check by the same coder, not an independent second coder.
- **Weights.** *Article-weighted*: a share is computed within each article, then each article counts once. *Pageview-weighted*: the same per-article shares, weighted by total views. 95% intervals come from an article-level bootstrap (1,000 resamples).

---

## Card 1. Israel's share as perpetrator barely moved; the volume of harm text grew  [STRONG]

**What we see.** Of all harm sentences in the 150 leads, the share naming Israel/IDF/government or Jews/Zionists/Yishuv as perpetrator: **23.6% → 24.1% → 26.4%** (article-weighted). Pageview-weighted: 22.9% → 22.7% → 25.9%. The 2021 → now change is +2.8 points (95% CI −1.9 to +8.3), so it is not statistically clear. Hamas/PIJ/Palestinian armed groups or Palestinians/Arabs as perpetrator: **7.0% → 7.8% → 8.8%** (pageview-weighted 6.5% → 8.2% → 7.5%), change +1.8 points (CI −1.4 to +5.7). In the 54-article conflict subset: Israel/Jews 42.6% → 43.0% → 44.9% (pageview-weighted 42.9% → 42.6% → 48.8%); Hamas/Palestinians 12.7% → 13.9% → 15.0%. What did grow is the amount of harm text. Topic harm sentences went from 390 to 391 to 508. Sentences with an Israeli/Jewish perpetrator went from 108 to 109 to 164 (in 35, 37 and 44 articles). Sentences with a Palestinian perpetrator went from 32 to 31 to 52 (in 13, 16 and 23 articles). The largest perpetrator group at every date is "other state" (mostly Nazi Germany): 46.5%, 45.7%, 43.8%.

**Chart.** Grouped bars: x = date; y = share of harm sentences (article-weighted); series = Israel/Jews, Hamas/Palestinians, other state, unclear. Second panel: sentence counts.

```json
{"chart":"perp_share_by_date","unit":"share of harm sentences, article-weighted (pageview-weighted in brackets)",
 "dates":["2021-01","2023-07","now"],
 "israel_jews":[0.236,0.241,0.264],"israel_jews_pv":[0.229,0.227,0.259],
 "hamas_palestinians":[0.070,0.078,0.088],"hamas_palestinians_pv":[0.065,0.082,0.075],
 "other_state":[0.465,0.457,0.438],"unclear_none":[0.284,0.259,0.264],
 "n_harm_sentences":[390,391,508],"n_israel_jews_perp":[108,109,164],"n_hamas_pal_perp":[32,31,52],
 "conflict_subset_israel_jews":[0.426,0.430,0.449],"conflict_subset_hamas_pal":[0.127,0.139,0.150],
 "change_2021_now_israel_jews":{"diff":0.028,"ci95":[-0.019,0.083]},"change_2021_now_hamas_pal":{"diff":0.018,"ci95":[-0.014,0.057]}}
```

**So what (Israeli audience).** There is no sudden flood of sentences blaming Israel. Israel was already the named agent in about a quarter of the harm sentences in 2021: wars, occupation, settlements. The story is not *how often*. It is *what Israel is now charged with*, and *in whose voice* (Cards 2 to 4).

**Caveat.** Leads got longer and gained new events (October 7, the Gaza war, the 2024 ICJ opinion). Some of the new text is news, not reframing. Shares are per harm sentence, not per word. Self-validated coding.

**Examples.** Stable in all three versions: Six-Day War, "Israel launched a series of preemptive airstrikes against Egyptian airfields" (2021) / "an Israeli surprise attack" (now). Hamas, in every version, attacks "Israeli civilians and soldiers" (2021) / "Israeli civilians, including through suicide bombings" (now).

---

## Card 2. Genocide enters the leads, twice in Wikipedia's own voice  [STRONG for the counts; they are exact sentences]

**What we see.** Sentences charging Israel with genocide: **0 (2021) → 0 (2023) → 8 now, in 7 articles**. Two are in Wikipedia's own voice:
- **Israel** (42.9M views since 2021): "After the Hamas-led October 7 attacks, Israel began committing genocide against Palestinians in Gaza." The next sentence: "Israel has denied that its actions constitute genocide."
- **Benjamin Netanyahu** (26.2M): "Netanyahu's government has been orchestrating the Gaza genocide, culminating in the South Africa v. Israel case before the International Court of Justice (ICJ) in December 2023."

Five are attributed: Palestine ("recognised as constituting genocide ... by a growing scholarly consensus"), Gaza Strip, Israeli–Palestinian conflict, Israel Defense Forces and Gaza–Israel conflict ("Many scholarly sources and international organizations have concluded..."). The eighth is the Israel denial. A ninth, in **Gaza City**, uses genocide in Wikipedia's voice but names no perpetrator ("until the Gaza war and ongoing genocide caused most of the population to be displaced or killed"), so it is coded unclear. Apartheid charged to Israel: 0 → 1 → 4 sentences. Only 1 is in own voice (Israeli–Palestinian conflict: "a system of institutionalized discrimination against Palestinians under its occupation referred to as Israeli apartheid"). The other 3 are attributed (Middle East experts; the 2024 ICJ opinion; Norman Finkelstein). Massacre/killing charged to Israel: 9 → 10 → 27 clause-charges, 25 of them now in own voice (mostly Gaza death tolls). No sentence charges Hamas or Palestinians with genocide or apartheid at any date.

**Chart.** Stacked bars by date for the Israel/Jews side: genocide, apartheid, ethnic cleansing, war crimes; dark = own voice, light = attributed or denied.

```json
{"chart":"israel_side_grave_charges","unit":"sentences (topic set, 150 leads)","dates":["2021-01","2023-07","now"],
 "genocide":{"all":[0,0,8],"own_voice":[0,0,2],"articles":[0,0,7]},
 "apartheid":{"all":[0,1,4],"own_voice":[0,0,1],"articles":[0,1,4]},
 "ethnic_cleansing_expulsion":{"all":[4,4,6],"own_voice":[3,2,5],"articles":[4,3,6]},
 "war_crimes":{"all":[1,1,2],"own_voice":[0,0,0]},
 "massacre_killing_sentences":{"all":[9,10,26],"own_voice":[6,8,24]},"massacre_killing_clause_charges":{"all":[9,10,27],"own_voice":[6,8,25]},
 "genocide_unnamed_perpetrator_own_voice":[0,0,1],
 "hamas_pal_side_genocide":[0,0,0],"hamas_pal_side_apartheid":[0,0,0],
 "comparison_side_A_genocide":{"all":[4,5,5],"own_voice":[2,2,2]}}
```

**So what.** This is the headline. The encyclopedia now states as fact, in the lead of the article on Israel itself, that "Israel began committing genocide". It does the same in the lead on its prime minister. Elsewhere the charge is attributed, to scholars, international lawyers and human-rights groups. These attributions are a choice too: the same sources could be paired with dissenting experts, and no lead does so except through Israel's own denial. The 50-article comparison set gained no new genocide charge against any state in the same period. Its 5 genocide sentences are historical (Armenian genocide, Holodomor, Crimean Tatars).

**Caveat.** There are few sentences, but each is an exact quote checked against the stored lead. "Own voice" is a coding judgement. The Israel lead puts the denial right after the claim. The comparison set has no ongoing war on the Gaza scale with an ICJ genocide case, so it is context, not a control.

**Examples.** Israel, 2023: "Israel's practices in its occupation of the Palestinian territories have drawn international condemnation for violating the human rights of the Palestinians." Now: "...most Middle East experts arguing that ... constitutes a system of apartheid." / "Israel began committing genocide against Palestinians in Gaza." Netanyahu, 2023: "Netanyahu has faced international criticism over his decades-long policy as prime minister of expanding Israeli settlements in the occupied West Bank, deemed illegal under international law." Now: "Netanyahu's government has been orchestrating the Gaza genocide..."

---

## Card 3. Occupation moves from "considered" to fact, but so does Russia's  [MODERATE]

**What we see.** Occupation charged to Israel: 35 → 35 → 55 clause-charges. Share stated in Wikipedia's own voice: **46% (16/35) → 51% (18/35) → 80% (44/55)**. In the comparison set, occupation charged to the side-A state (mostly Russia in Crimea and eastern Ukraine, and Turkey in northern Cyprus): 25% (2/8) → 70% (7/10) → 74% (14/19) own voice. Overall own-voice share for Israel/Jews as perpetrator (all charges, article-weighted): 75.8% → 78.9% → 81.3% (pageview-weighted 71.7% → 70.6% → 78.5%). The change is not statistically clear (2021 → now +5.5 points, CI −7.8 to +18.8).

**Chart.** Two lines: own-voice share of occupation charges, Israel vs comparison side A, by date.

```json
{"chart":"occupation_own_voice","dates":["2021-01","2023-07","now"],
 "israel":{"own_voice":[16,18,44],"all":[35,35,55],"share":[0.46,0.51,0.80]},
 "comparison_side_A":{"own_voice":[2,7,14],"all":[8,10,19],"share":[0.25,0.70,0.74]},
 "israel_jews_own_voice_all_charges_article":[0.758,0.789,0.813],"pageview":[0.717,0.706,0.785]}
```

**So what.** "Israeli occupation, which is illegal under international law" is now house style. Since the July 2024 ICJ advisory opinion, editors have a court to cite. But the same move happened on other disputes: Crimea "has been under Russian occupation since 2014", and the Turkish-held north of Cyprus. An Israeli critic should not present this one as singling out Israel. The genocide charge (Card 2) is where Israel differs.

**Caveat.** Comparison counts are small (8 to 19). The ICJ opinion is a real new source, not only an editorial choice.

**Examples.** West Bank, 2021: "Under Israeli occupation since 1967, the area is split into 167 Palestinian "islands"..." Now: "Since 1967, the territory has been under Israeli occupation, which is illegal under international law." Israel, 2021: "Israel's occupation of the Palestinian territories is internationally considered to be the world's longest military occupation in modern times." Now: "Israel's illegal occupation of the Palestinian territories has drawn international criticism..." Palestine, 2023: "subject to a long-term blockade by Egypt and Israel since 2007". Now: "The Gaza Strip has long been subject to Israeli military occupation and an illegal blockade."

---

## Card 4. 1948 gets an agent: "fled or were expelled" becomes "expelled by Zionist forces"  [STRONG for the quote pairs, MODERATE for the rate]

**What we see.** Sentences with Palestinians as victims: 71 → 78 → 141. Share of them that name **no** perpetrator: **62% (44/71) → 51% (40/78) → 38% (54/141)**. Sentences naming Israel or Jews/Zionists as the agent of harm to Palestinians: 50 → 53 → 100. Ethnic-cleansing/expulsion charges with an Israeli or Zionist agent: 4 → 4 → 6 (own voice 3 → 2 → 5). The new ones are 1948 sentences in 1948 Arab–Israeli War, 1948 Palestine war, Israeli–Palestinian conflict and Gaza Strip. The Jewish side of 1948 stays agentless at all dates: "Hundreds of thousands of Jews fled or were expelled from Arab states" (1948 Palestine war, now). Of sentences with Israeli or Jewish victims, the share with a Hamas or Palestinian perpetrator was 20/171 → 19/165 → 41/211; most Jewish-victim sentences have Nazi Germany as perpetrator.

**Chart.** Bars for Palestinian-victim sentences by date, split by perpetrator: Israel/Jews named vs no perpetrator named.

```json
{"chart":"palestinian_victim_agent","dates":["2021-01","2023-07","now"],
 "pal_victim_sentences":[71,78,141],"perp_unnamed":[44,40,54],"perp_israel_jews":[50,53,100],
 "share_unnamed":[0.62,0.51,0.38],
 "israeli_jewish_victim_sentences":[171,165,211],"of_which_hamas_pal_perp":[20,19,41],"of_which_other_state_perp":[104,104,112]}
```

**So what.** The encyclopedia now tells 1948 as expulsion *by Zionist forces*, in its own voice, in the articles readers use for 1948. Here the earlier regex approach failed, because it scored the victims, not the agent. The change is real, and it is one-directional: the expulsion of Jews from Arab countries still has no named agent.

**Caveat.** Counts in a sentence with two victims are counted once per side. Some of the "named agent" growth comes from Gaza-war sentences, not 1948. The 1948 pairs below are the clean cases. Counter-example: the **Israel** lead itself went the other way on 1948. In 2023 it said "over 700,000 Palestinian Arabs were expelled from or fled Israeli territory"; now it says "Most Palestinian Arabs fled or were expelled during the Nakba". Both are agentless.

**Examples.** 1948 Palestine war, 2023: "During the war, around 700,000 Palestinian Arabs were displaced." Now: "During the war, Zionist forces conquered about 78% of the former territory of the mandate, causing the expulsion and flight of over 700,000 Palestinians." 1948 Arab–Israeli War, 2021: "Around 700,000 Palestinian Arabs fled or were expelled from their homes in the area that became Israel..." Now: "In April 1948, Zionist forces launched an offensive codenamed Plan Dalet, during which they conquered and depopulated cities, villages, and territories in Mandatory Palestine in preparation for the establishment of a Jewish state." Israeli–Palestinian conflict, now: "...more than half of the mandate's predominantly Palestinian Arab population fled or were expelled by Israeli forces". Even-handed counter-example, 1948 Palestine war, now: "During the war, massacres and acts of terror were conducted by both sides."

---

## Card 5. Hamas: still named as perpetrator, but "terrorist" is thinner and further away  [MODERATE]

**What we see.** Of sentences with a Hamas or Palestinian perpetrator, the share in Wikipedia's own voice is about the same: 83.4% → 73.8% → 81.8% (article-weighted; pageview-weighted 78.3% → 66.2% → 85.7%; no clear change). Terrorism charges on the Palestinian side: 9 → 10 → 9 sentences. Own voice: 2 → 3 → 4. These are Munich ("a terrorist attack"), the 1985 PLO attack in the Israeli Air Force lead, the 2023 History of the Israeli–Palestinian conflict sentence, and "the terrorists" in Entebbe now. The attributed designations got thinner. The **Hamas** lead named the designating states (5 plus 4 for the military wing in 2021; 7 plus 2 in 2023). Now it says "Several countries have designated Hamas as a terrorist organisation." In History of the Israeli–Palestinian conflict, "terrorist attacks by Palestinian militants" (2023) became "Palestinian political violence" (now). Counter-example: the Gaza–Israel conflict lead now states in its own voice that on 7 October "Palestinian militants attacked Israel, killing 1,195 people (mostly civilians), committing war crimes, taking hostages". It is the only own-voice war-crimes charge against either side in the topic set.

**Chart.** Small multiples by date for the Palestinian side: terrorism (own voice vs attributed vs denied), massacre/killing (own voice), war crimes.

```json
{"chart":"pal_side_charges","dates":["2021-01","2023-07","now"],
 "terrorism":{"all":[9,10,9],"own_voice":[2,3,4]},
 "massacre_killing":{"all":[8,8,24],"own_voice":[8,7,23]},
 "war_crimes":{"all":[1,0,3],"own_voice":[0,0,1]},
 "own_voice_share_article":[0.834,0.738,0.818],"own_voice_share_pageview":[0.783,0.662,0.857],
 "hamas_lead_designating_states_named":[9,9,0]}
```

**So what.** For an Israeli audience: the encyclopedia did not stop saying that Hamas kills Israeli civilians. It says so in its own voice, more often now than in 2021 (23 own-voice killing charges now vs 8). What faded is the *label*. The list of states that call Hamas terrorist became "several countries". In one overview article, "terrorist attacks" became "political violence". On Israel's side the opposite happened: from "criticism" to "genocide". The two lines did not move by the same rules.

**Caveat.** Few sentences. The Munich lead keeps "terrorist attack" but changed the group from "Palestinian terrorist group" (2021) to "Palestinian militant organization" (2023 onward). Hamas-side counts include Fatah/PLO fighters (coded H).

**Examples.** Hamas, 2023: "Canada, the European Union, Israel, Japan, Australia, the United Kingdom and the United States have designated Hamas as a terrorist organization." Now: "Several countries have designated Hamas as a terrorist organisation." History of the Israeli–Palestinian conflict, 2023: "The conflict has been marked by violence, including terrorist attacks by Palestinian militants and military operations by Israel." Now: "The conflict has been marked by violence, including Palestinian political violence and Israeli military operations." Munich massacre, 2021: "...by eight members of the Palestinian terrorist group Black September". Now: "...a terrorist attack ... carried out by eight members of the Palestinian militant organisation Black September."

---

## Card 6. Context: on other disputes the stronger state's share as perpetrator rose more  [MODERATE]

**What we see.** In the 50 comparison articles, side A (Russia/USSR, Azerbaijan/Ottoman/Turkey, Turkey in Cyprus, Serbia, the British state and loyalists, India) as perpetrator: **32.9% → 43.5% → 43.2%** of harm sentences (article-weighted). Pageview-weighted: 50.1% → 46.8% → 44.3%; the top Ukraine articles already had it in 2021. Own voice for side A: 64.6% → 78.8% → 79.5%. Side B: 18.8% → 21.6% → 21.6%, own voice 86.9% → 92.3% → 93.6%. Ethnic-cleansing charges on side A: 8 → 13 → 16 (own voice 7 → 12 → 14), driven by the 2023 Karabakh offensive and the Crimean Tatars. Genocide on side A: 4 → 5 → 5, all historical.

**Chart.** Paired bars: share as perpetrator for topic Israel/Jews vs comparison side A, by date; markers for own-voice share.

```json
{"chart":"topic_vs_comparison","dates":["2021-01","2023-07","now"],
 "topic_israel_jews_share":[0.236,0.241,0.264],"topic_israel_jews_own_voice":[0.758,0.789,0.813],
 "topic_hamas_pal_share":[0.070,0.078,0.088],"topic_hamas_pal_own_voice":[0.834,0.738,0.818],
 "comparison_side_A_share":[0.329,0.435,0.432],"comparison_side_A_share_pv":[0.501,0.468,0.443],"comparison_side_A_own_voice":[0.646,0.788,0.795],
 "comparison_side_B_share":[0.188,0.216,0.216],"comparison_side_B_own_voice":[0.869,0.923,0.936],
 "comparison_n_sentences":[217,241,265],"comparison_by_dispute_articles":{"UA":21,"AM":15,"NI":7,"KS":4,"CY":3,"KM":3}}
```

**So what.** "Wikipedia names the state as the perpetrator more often" is not unique to Israel. It happened on Russia and Azerbaijan too, after their own wars. That makes the Israel finding more credible, not less. It is not a general rise in blame. What is specific to the Israel set is the *gravest charge*, genocide, stated as fact in two of the most-read leads.

**Caveat.** The comparison disputes differ in size, period and events. Kosovo, Cyprus and Kashmir have only 2 to 17 harm sentences per date. This is context, not a matched control.

**Examples.** Russo-Ukrainian war, now: "Russia has repeatedly carried out deliberate and indiscriminate attacks on civilians far from the frontline." Republic of Artsakh, now: "...followed by the effective expulsion of the entire population." Crimea, now: "The region, internationally recognised as part of Ukraine, has been under Russian occupation since 2014."

---

## Best before/after quote pairs (most-read first)

| Article (views since 2021) | Before | After (now) |
|---|---|---|
| Israel (42.9M) | 2023: "Israel's practices in its occupation of the Palestinian territories have drawn international condemnation for violating the human rights of the Palestinians." | "Israel's illegal occupation of the Palestinian territories has drawn international criticism, with most Middle East experts arguing that Israel's treatment of Palestinians in the West Bank in relation to Israeli settlers constitutes a system of apartheid." + "After the Hamas-led October 7 attacks, Israel began committing genocide against Palestinians in Gaza." + "Israel has denied that its actions constitute genocide." |
| Palestine (30.9M) | 2023: "The Gaza Strip has been ruled by the militant Islamic group Hamas and has been subject to a long-term blockade by Egypt and Israel since 2007." | "The Gaza Strip has long been subject to Israeli military occupation and an illegal blockade." |
| Benjamin Netanyahu (26.2M) | 2023: "Netanyahu has faced international criticism over his decades-long policy as prime minister of expanding Israeli settlements in the occupied West Bank, deemed illegal under international law." | "Netanyahu's government has been orchestrating the Gaza genocide, culminating in the South Africa v. Israel case before the International Court of Justice (ICJ) in December 2023." |
| Hamas (23.0M) | 2023: "Canada, the European Union, Israel, Japan, Australia, the United Kingdom and the United States have designated Hamas as a terrorist organization." | "Several countries have designated Hamas as a terrorist organisation." |
| Israeli–Palestinian conflict (18.4M) | 2023: "The 1947 United Nations Partition Plan for Palestine was never implemented and provoked the 1947–1949 Palestine War." | "During the ensuing 1948 Palestine war, the State of Israel was founded and more than half of the mandate's predominantly Palestinian Arab population fled or were expelled by Israeli forces, referred to by Palestinians as the Nakba." |
| Mossad (8.3M) | 2023: "Mossad is responsible for intelligence collection, covert operations, and counter-terrorism." | "Mossad is responsible for intelligence collection, covert operations, extrajudicial killings and counterterrorism." |
| West Bank (9.4M) | 2021: "Under Israeli occupation since 1967, the area is split into 167 Palestinian "islands"..." | "Since 1967, the territory has been under Israeli occupation, which is illegal under international law." |
| 1948 Arab–Israeli War (6.0M) | 2021: "Around 700,000 Palestinian Arabs fled or were expelled from their homes in the area that became Israel..." | "In April 1948, Zionist forces launched an offensive codenamed Plan Dalet, during which they conquered and depopulated cities, villages, and territories in Mandatory Palestine in preparation for the establishment of a Jewish state." |
| History of the Israeli–Palestinian conflict (3.4M) | 2023: "...including terrorist attacks by Palestinian militants and military operations by Israel." | "...including Palestinian political violence and Israeli military operations." |
| 1948 Palestine war (2.9M) | 2023: "During the war, around 700,000 Palestinian Arabs were displaced." | "During the war, Zionist forces conquered about 78% of the former territory of the mandate, causing the expulsion and flight of over 700,000 Palestinians." |

**Counter-examples worth printing.** Gaza–Israel conflict, now (new): "On 7 October 2023, Palestinian militants attacked Israel, killing 1,195 people (mostly civilians), committing war crimes, taking hostages, and beginning the Gaza war." Hamas, now: "Hamas has attacked Israeli civilians, including through suicide bombings as well as launching rockets at Israeli cities." 1948 Palestine war, now: "During the war, massacres and acts of terror were conducted by both sides." Israel, now, on 1948, agentless: "Most Palestinian Arabs fled or were expelled during the Nakba." Itamar Ben-Gvir: Baruch Goldstein is "Israeli-American terrorist" (2023) and "a Jewish terrorist and mass murderer" (now), in Wikipedia's own voice. So own-voice "terrorist" is not reserved for one side.

## Files

- `perp_codes.jsonl`: one row per kept sentence per date (2,012 rows): exact text, perpetrator, victim, voice, charge class, all clauses, views.
- `perp_validation.md`: codebook, the 100 re-checked rows with verdicts, precision, recall sweep.
- `perp_results.json`: all aggregates (article-, pageview- and pooled weights, bootstrap CIs, charge tables, victim framing, comparison by dispute).
