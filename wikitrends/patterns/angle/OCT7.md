# October 7, Hamas and the hostages: how English Wikipedia's framing changed (Oct 2023 to Nov 2026)

Folder: `patterns/angle/`. Chart data: `chart_data/oct7_*.json`. Audience and rules: `ANGLE.md`.

**Data and limits, in one paragraph.** First sentences of every revision of the key leads come from `data/ratchet.json` (to about 4 Nov 2026). It also has term events for the whole lead: when "terrorism", "militant", "genocide" and the like entered or left. Full lead text exists only at snapshot dates: 2021-01-01, 2023-07-01 and the last revision before 5 Nov 2026 (`mass2_leads.json.gz`), and 2024-01-01 and 2026-10-01 (`leads.json`). So we can date first-sentence changes to the minute. Changes deeper in a lead can only be bracketed between two snapshots. "Gaza war" is not in the mass-v2 snapshot, so its newest full lead is 1 Oct 2026. There is no dedicated hostage article in our data. Al-Qaeda, Al-Shabaab and Boko Haram exist only at 2021-01 and 2026-10, plus quarterly first sentences in `results.json`. Sentence numbers come from a heuristic splitter and can be off by one. The tests reported below were checked by hand.

**A correction to the brief.** ANGLE.md says "'terrorist' moved out of Hamas's definition". Our data does not support that wording. From January 2021 on, the Hamas definition (first sentence) never contained "terrorist" for more than a few hours. What left the definition was **"militant"**. What moved was the **terrorist designation sentence**: from the first paragraph (sentence 5) to the last lines of the lead. Card 1 and card 2 give the exact story.

---

## 1. Hamas: "militant" left the definition five days after October 7; "terrorist" was never in it
*HAMAS · STRONG*

**What we see.** On 1 Jan 2021 the first sentence said Hamas "is a Palestinian Sunni-Islamic fundamentalist but pragmatic, militant, and nationalist organization". From 23 Aug 2021 to 9 Oct 2023 it said "...fundamentalist, militant, and nationalist organization."
- 9 Oct 2023, 22:58 UTC: "fundamentalist" was dropped and "political" added: "a Palestinian political and militant organization that currently governs the Gaza Strip".
- 12 Oct 2023, 19:12 UTC: "militant" became "military": "a Sunni Islamist political and military organization currently governing the Gaza Strip of the Palestinian territories."
- The lead then went from "organization" to "movement" (31 Jan 2024). On 19 Aug 2024 it became "political organisation with a militant wing", and on 31 Aug 2024 "with a military wing".
- Since 18 Feb 2025 the definition has kept the "political organisation with a military wing" form. Its last change was 2 Dec 2025. Today it reads: "The Islamic Resistance Movement, abbreviated Hamas (...), is a Sunni Islamist Palestinian nationalist political organisation with a military wing known as the al-Qassam Brigades."
- After 12 Oct 2023, "militant" came back to the first sentence only three times: 1–2 Aug 2024 (under one day), 19–31 Aug 2024 ("militant wing") and 12–18 Feb 2025 ("Sunni Islamist militant and political organisation", 6.1 days). It has been absent from the whole lead since 11 Dec 2025.
- Short description (the line shown in search and apps): "Palestinian Islamic militant nationalist organization" (2021) became "Islamist Palestinian political and paramilitary organization" (now).

The first sentence changed **114 times** between 7 Oct 2023 and Dec 2025, against 7 times in the 33 months before. "Militant" flipped in or out 19 times. "Terrorist" was added to the definition five times: 10 Oct 2023 ("political and terrorist organization", about 2 hours), 12 Oct 2023 (about 15 minutes), 19 Nov 2023 ("designated as a terrorist group by many countries (including the US, UK, EU, etc.)", about 45 minutes), 12 Mar 2024 ("Palestinian Sunni Islamist terrorist group", about 2.4 hours) and 22 Apr 2024 (minutes). Together that is under six hours in three years. "Resistance movement" got in once, on 1 Aug 2024 (01:56 UTC), with the edit summary "[[NPOV]] many relaible sources has described it as resistance movement which is less biased and more neutral. this is how the group identifies itself". It was gone the next day (2 Aug, 06:52). The talk page shows 8 RfCs in the war period, 2 of them formally closed with consensus (Nov 2023). Our data does not record their topics.

**Chart.** Step timeline, Oct 2023 to Nov 2026. Each band is the definition class (fundamentalist-militant / political-and-militant / political-and-military / political organisation with a military wing), with ticks for the five "terrorist" insertions and the "resistance movement" insertion, and a monthly pageviews strip under it (`chart_data/oct7_01_hamas_first_sentence.json`).

**So what.** Wikipedia stopped calling Hamas "militant" on 12 October 2023. That was five days after the massacre, and in the month its article drew 8,236,474 views, the most of any month in our 2021–26 data. The definition Israelis object to ("political organisation with a military wing") was in place from the first week. It was not a slow 2024 drift. Pro-Israel editors repeatedly tried to write "terrorist" into the definition. Each try was removed within hours.

**Caveat.** Day-level views are not in our data, so we cannot say how many October 2023 readers saw each version. The 114 changes include typo fixes and vandalism (e.g. 30 Sep 2024).

**Examples.**
- 1 Jan 2021: "...is a Palestinian Sunni-Islamic fundamentalist but pragmatic, militant, and nationalist organization."
- 12 Oct 2023 (19:12 UTC): "...is a Sunni Islamist political and military organization currently governing the Gaza Strip of the Palestinian territories."
- 2 Nov 2023 onward, the territory became "the Israeli-occupied Palestinian territories". The lead now says "It has governed the Israeli-occupied Gaza Strip since 2007."

## 2. The terrorist designation went from sentence 5 to the end of the Hamas lead, and in October 2026 lost its list of countries
*HAMAS · STRONG on position, SUGGESTIVE on the newest edit*

**What we see.**
- 2021-01-01: the designation is sentence 5 of 20, in paragraph 1, 16% of the way into the lead: "Canada, the European Union, Israel, Japan and the United States classify Hamas as a terrorist organization." Four sentences in a row deal with designations (4 "terror" mentions).
- 2023-07-01: sentence 5 of 9, opening paragraph 2: "Canada, the European Union, Israel, Japan, Australia, the United Kingdom and the United States have designated Hamas as a terrorist organization."
- In the quarterly snapshots, the count of "terror" words in the lead fell from 4 (Oct 2023) to 1 (Jan 2024) and has been 2 since Jan 2026.
- 2026-10-01: sentence 22 of 23, 95% of the way into the lead: "Australia, Canada, Costa Rica, Ecuador, Honduras, Israel, Japan, New Zealand, Paraguay, Trinidad and Tobago, the United Kingdom, the United States, and the European Union have designated Hamas as a terrorist organisation."
- 2026-10-31 (rev 1383083378): "Several countries have designated Hamas as a terrorist organisation."

Meanwhile, sentence 2 of paragraph 2 (22% into the lead) now says: "Initially, Hamas was discreetly supported by Israel, as a counter-balance to the secular Palestine Liberation Organization (PLO) to prevent the creation of an independent Palestinian state." This sentence is absent in 2021 and 2023-07. Violence against Israelis gets one sentence near the end: "Hamas has attacked Israeli civilians, including through suicide bombings as well as launching rockets at Israeli cities." October 7 appears once, as a date: "...an ongoing one since 2023, which began with the October 7 attacks." The lead contains no "hostage", "massacre" or "war crimes". War crimes left on 1 Aug 2024. The 2021 lead had "Human Rights Watch has condemned as war crimes and crimes against humanity both Hamas and Israel...".

**Chart.** Horizontal "position bar" per snapshot (0 = first word, 1 = last word), with a dot where "terrorist" first appears and a dot for "supported by Israel" (`chart_data/oct7_08_hamas_designation_position.json`).

**So what.** A reader who stops after the first paragraph, as most do and as AI summaries often do, no longer learns that Hamas is a designated terrorist organisation. The same reader does learn that Israel once "discreetly supported" Hamas. Since late October 2026, even a reader who gets to the end no longer sees which countries designate it. Israel, the US and the EU are no longer named.

**Caveat.** The "Several countries" edit falls between 1 Oct and 31 Oct 2026. We have no edit-level record of it, it is days old, and it may be reverted. Lead length also grew (154 words in Jul 2023, 525 now), which pushes any one sentence later. That said, the designation sentence is now the second-to-last sentence.

**Examples.**
- 2021: "It is not considered a terrorist organization by Brazil, China, Egypt, Iran, Norway, Qatar, Russia, Syria and Turkey." (sentence 7)
- Now: "In 2018 and 2023, motions at the United Nations to condemn Hamas as a terrorist organization failed to meet the two-thirds threshold." (last sentence)

## 3. Dropping "terrorist" from first sentences is Wikipedia-wide style; dropping "militant" is not
*COMPARISON · SUGGESTIVE (9 groups, hand-picked)*

**What we see.**

| group | first sentence 2021 | first sentence now | first "terror" mention, then -> now |
|---|---|---|---|
| Hamas | "fundamentalist but pragmatic, militant, and nationalist organization" | "political organisation with a military wing" | sentence 5/20 (16%) -> 22/23 (95%) |
| Hezbollah | "Shia Islamist political party and militant group" | "political party with an active paramilitary wing" | 4/25 (11%) -> 25/33 (77%) |
| Palestinian Islamic Jihad | "Damascus-based Palestinian Islamist organization" | "Islamist Palestinian paramilitary organization" | 4/14 (26%) -> 10/12 (81%) |
| Islamic State | "militant Islamist group" | "transnational Salafi jihadist militant organisation" | 3/22 (18%) -> 4/15 (22%) |
| Al-Qaeda | "militant Sunni Islamist multi-national organization" | "pan-Islamist militant organization" | 3/16 (16%) -> 4/27 (14%) |
| Al-Shabaab | "a terrorist, jihadist fundamentalist group" | "Salafi Jihadist militant organization" | 1/22 (2%) -> 4/17 (16%) |
| Boko Haram | "a jihadist terrorist organization" | "jihadist militant organisation" | 1/20 (10%) -> not in lead |
| IRGC | "branch of the Iranian Armed Forces" | "multi-service military force of Iran" | 11/11 (95%) -> 13/18 (68%) |
| Taliban | (no "terror" in lead) | "Sunni Islamist political and militant organization" | none -> last sentence |

"Terrorist" left the first sentences of Al-Shabaab (by Jul 2022) and Boko Haram (by Apr 2023), both before October 7 (Boko Haram's came back briefly in the Apr 2025 snapshot, as "self-proclaimed jihadist terrorist organization"). Islamic State's first sentence said "transnational militant Islamist terrorist group" from 15 Jun 2023 and lost "terror" on 20 Nov 2023. These moves are consistent with Wikipedia's style guidance on contentious labels. We did not check whether edit summaries cite it. No group in the set keeps "terrorist" in its definition today.

The difference is "militant". The global jihadist groups keep "militant" in sentence 1 and mention designations in the first four sentences. The three groups that fight Israel lost "militant" (Hamas, Hezbollah) or never had it (PIJ). They are now defined as political or paramilitary bodies, and their designations sit in the last fifth of the lead. Hezbollah's change came in 2024: "militant group" became "paramilitary group" on 24 Jun 2024 and, after a fight in Sep–Oct 2024, settled on 16 Oct 2024. PIJ's short description went from "Palestinian Islamist terror organization" (2021) to "Palestinian political party paramilitary force" (now).

**Chart.** Dumbbell chart: one row per group, x = position of first "terror" mention as share of lead (0–1), dots for 2021 and now, with rows colored by whether "militant" is in the first sentence now (`chart_data/oct7_02_designated_groups.json`).

**So what.** Israeli critics are right that Hamas is treated differently. But the difference is not the missing word "terrorist": ISIS and al-Shabaab lost that too. It is that Hamas, Hezbollah and PIJ are now introduced as political organisations with armed wings, while ISIS and al-Qaeda are still introduced as militant organisations. This is the precise, defensible version of the claim.

**Caveat.** Nine groups, not a sample. Al-Shabaab's first sentence briefly read "Sunni Islamist political and paramilitary organisation" (Jan 2026 snapshot) before going back to "militant", so the pattern is not airtight. Hamas and Hezbollah also really do run political parties, which is not true of ISIS.

**Examples.**
- Hezbollah, 26 Oct 2026: "Hezbollah is a Lebanese Shia Islamist political party with an active paramilitary wing."
- Islamic State, now: "...is a transnational Salafi jihadist militant organisation and internationally unrecognised former quasi-state."

## 4. October 7's first sentence says "armed incursions". It has never kept "massacre", "terror", the death toll or the hostages
*OCTOBER 7 · STRONG*

**What we see.** The article's first sentence has had 107 variants and 132 changes. Hours after the attack (7 Oct 2023, 05:28 UTC) the page described "an extended military operation launched by the Palestinian resistance" (seconds). At 07:45 it said rockets "were fired by Palestinian terrorists" (about 3 minutes). From 12 to 22 Oct 2023 the article was titled with Hamas's own name for the attack, "Operation Al-Aqsa Flood", and opened: "Operation Al-Aqsa Flood is the name used by Islamist militant group Hamas for its coordinated attacks from the Gaza Strip onto bordering areas in Israel on October 7, 2023." Title history:
1. "Operation Al-Aqsa Flood"
2. "2023 Hamas attack on Israel" (22 Oct 2023, requested move)
3. "2023 Hamas-led attack on Israel" (28 Nov 2023)
4. "7 October Hamas-led attack on Israel" (10 Oct 2024)
5. "October 7 Hamas-led attack on Israel" (30 Dec 2024)
6. "October 7 attacks" (26 May 2025)

"Coordinated attacks" became "coordinated incursions" on 27 Nov 2023 and "armed incursions" on 9 Dec 2023. That has been the wording ever since. The perpetrators went from "the Palestinian Islamist militant group Hamas" (Oct–Dec 2023), to "the paramilitary wings of Hamas, the Palestinian Islamic Jihad, the PFLP, and the DFLP" (16 Dec 2023), to "Hamas and several other Palestinian militant groups" (21 Mar 2024 to now). Here is the whole record, across every revision, for words that never stayed:
- "massacre": in the first sentence twice, about an hour in total (23 Jan 2024, 25 Nov 2025)
- "terror": three times, 0.2 days in total, all in October 2023
- the death toll: once, 30 Sep to 1 Oct 2026 ("killing at least 1,195 people", 1.2 days)
- "hostages": never

Two things were added. "Blockaded" ("from the blockaded Gaza Strip") has been there since 20 Feb 2026 (first tried 3 Jun 2025). The Jewish-holiday clause ("a Sabbath day and date of several Jewish holidays" in Oct 2023, "during the Jewish holiday of Simchat Torah" from Aug 2025) was moved out of the first sentence on 8 Oct 2026.

**Chart.** Swimlane timeline, Oct 2023 to Nov 2026, with lanes for: title (6 steps), perpetrator wording, act wording ("attacks" / "armed incursions"), and dots for every short-lived "massacre", "terror", toll and "blockaded" variant, sized by how long they lived (`chart_data/oct7_03_oct7_first_sentence_and_title.json`).

**So what.** The encyclopedia's one-line answer to "what was October 7?" is "a series of coordinated armed incursions ... carried out by Hamas and several other Palestinian militant groups". It says nothing of murder or hostages, and since February 2026 it does mention Gaza's blockade. Wikipedia's own sub-articles are blunter. "Be'eri massacre": "During the October 7 attacks on Israel, Hamas militants carried out a massacre at Be'eri". The article on a 2002 attack on Israeli targets in Kenya: "two coordinated terrorist attacks". The short description of the October 7 article itself reads "2023 armed incursions and massacres in Israel". That shows the main sentence is a choice, not a lack of sources.

**Caveat.** The killing is described plainly in paragraph 2 ("massacring civilians in 21 communities"), not hidden. Leaving the toll out of a first sentence is common on Wikipedia: "March 2025 Israeli attacks on the Gaza Strip" also gives its toll only in sentence 2. Our comparison set of attack articles is small and not systematic.

**Examples.**
- 23 Oct 2023: "A series of coordinated attacks, conducted by the Palestinian Islamist militant group Hamas, from the Gaza Strip onto bordering areas in Israel, commenced on Saturday 7 October 2023, a Sabbath day and date of several Jewish holidays."
- Since 8 Oct 2026: "On October 7, 2023, a series of coordinated armed incursions from the blockaded Gaza Strip into the Gaza envelope of southern Israel were carried out by Hamas and several other Palestinian militant groups."

## 5. October 7's lead: the facts got fuller, sentence 2 now turns to Israel, and October 2026 brought three quiet edits
*OCTOBER 7 · STRONG on text, SUGGESTIVE on timing inside October 2026*

**What we see.** On 1 Jan 2024 the lead (329 words) had 1,139 dead ("695 Israeli civilians, among them 36 children"). It had about 250 hostages "including 30 children". It said "Israel and international media have reported rape and sexual assault by Hamas fighters with documentary footage and photographs, which Hamas has denied", and it carried the Israeli name "the Simchat Torah Massacre". Now (2 Nov 2026, 406 words), in reading order:
1. Sentence 2: "In response, Israel launched a major military operation in Gaza."
2. Sentence 4: "massacring civilians in 21 communities, including Be'eri, Kfar Aza, Nir Oz, Netiv Haasara, and Alumim"
3. Sentence 7: "at least 1,195 people were killed by the attacks: at least 828 civilians (including 36 children and 71 foreign nationals)"
4. Sentence 9: "251 Israeli and non-Israeli civilians and soldiers were taken as hostages to the Gaza Strip"
5. Sentence 10: "Numerous sources have reported dozens of cases of rape and sexual assault." No perpetrator is named in this sentence.
6. Sentence 11: "The IDF used the Hannibal Directive on that day, which may have led to at least 13 Israeli civilian deaths."
7. The last sentence (16): "The governments of 44 countries denounced the attack and described it as terrorism..."

The lead keeps a genocide claim about Israelis, attributed: "Some have alleged that the attack was an act of genocide or a genocidal massacre against Israelis." "Terrorism" has stayed in the lead since 28 Jun 2024, after 4 failed attempts.

Three changes fall between 1 Oct and 2 Nov 2026:
- Sentence 2 on 1 Oct 2026 read "In response, Israel intensified its blockade and launched a major military operation in Gaza, actions scholars have concluded constitute genocide." The genocide clause is gone.
- "At least 14 Israeli civilians were killed by the IDF's use of the Hannibal Directive" became "may have led to at least 13".
- "...but Hamas officials denied the involvement of their fighters" was removed.

**Chart.** Three-column then/now grid (1 Jan 2024 / 1 Oct 2026 / 2 Nov 2026), one row per item: toll, civilians, hostages, sexual violence, massacre, terrorism, Hannibal, genocide (`chart_data/oct7_06_oct7_lead_then_now.json`).

**So what.** On facts, the 2026 lead is more complete than the 2024 one: higher verified toll, named kibbutzim, attacker count. Two choices stand out for Israelis. The Hannibal Directive now sits in the opening section of the article about the massacre. And until October 2026 the second sentence of that article called Israel's response genocide. That clause was removed in October 2026, so the newest text is less hostile to Israel than the 1 Oct 2026 text. Another card in this project (`story_sources_langs` card 2) still quotes the removed clause as current. It should be updated.

**Caveat.** We do not have the October 2026 edits themselves, only the before and after texts. They may be reverted. Sentence numbers come from a heuristic splitter.

**Examples.**
- 1 Jan 2024: "At least 44 nations denounced the attack as terrorism, while many Arab and Muslim countries blamed the Israeli occupation of the Palestinian territories as the root cause of the attack."
- 2 Nov 2026: "Hamas said its attack was in response to the continued Israeli occupation, the blockade of the Gaza Strip, the expansion of illegal Israeli settlements, rising Israeli settler violence, recent escalations and Israel's holding of Palestinian prisoners, and that it was in defense of the Palestinian people and their cause."

## 6. Hostages: absent from the Hamas and Israel leads, one line in October 7, and fewer mentions but a higher spot in Gaza war
*HOSTAGES · STRONG for the snapshots, NOT TESTABLE between them*

**What we see.** Mentions of "hostage/captive/abducted/kidnapped" in the opening section:

| article | 2021-01 | 2023-07 | 2024-01 | 2026-10-01 | now (2–4 Nov 2026) |
|---|---|---|---|---|---|
| Hamas | 0 | 0 | – | 0 | 0 |
| Israel | 0 | 0 | – | 0 | 0 |
| October 7 attacks | – | – | 1 (sentence 7 of 11, para 2) | 1 (sentence 9 of 16, para 3) | 1 (sentence 9 of 16, para 3) |
| Gaza war | – | – | 4 (sentences 9, 14, 23 of 24; paras 2, 3, 5) | 1 (sentence 2 of 29, para 1) | not in snapshot |
| Gaza genocide | – | – | 0 | 1 (para 5 of 5) | 1 (second-to-last sentence) |

In first sentences, across every revision of these five articles (615 variants), the hostages appeared twice, for 0.58 days in total. Gaza war, 1 Nov 2023 (0.24 days): "...a Hamas attack on southern Israel that killed 1,400 Israelis and took 200 others hostage in a single day." Gaza genocide, 18 Feb 2024 (0.34 days).

**Chart.** Small multiples: one row per article, x = snapshot date, y = position in the lead (sentence share), a dot per mention sized by count (`chart_data/oct7_04_hostages_in_leads.json`).

**So what.** The Israel article, read about 5 million times in the last 12 months, says nothing about the hostages. It mentions October 7 only as the lead-in to its genocide sentence. The Hamas article, the group that took and held them, does not mention them at all. In the Gaza war article the hostages moved up to sentence 2 ("251 were taken hostage"). But the 2024 lead's detail is gone: the truce exchange ("105 Israeli hostages were exchanged for 240 Palestinian prisoners"), the rescue attempt, the hostages "reportedly killed during the bombing of Gaza". In Gaza genocide, the hostages appear only inside Israel's stated position ("...to destroy Hamas and free Israeli hostages").

**Caveat.** We have no full-lead text between snapshots, so we cannot see whether hostage coverage rose during the 2025 release deals. Mentions are a narrow measure: the Gaza war lead does describe ceasefires and the US-backed peace plan without the word "hostage". There is no dedicated hostage article in our dataset.

**Examples.**
- Gaza war, 1 Jan 2024: "Freeing hostages held by Palestinian militants was another stated goal, although it rescued only one; dozens more were reportedly killed during the bombing of Gaza and by friendly fire."
- Gaza war, 1 Oct 2026: "The war began on 7 October 2023, when Palestinian militant group Hamas led an attack on Israel, in which 1,195 Israelis and foreign nationals were killed and 251 were taken hostage."

## 7. "Genocide" became Wikipedia's own voice in September 2025; Israel's position sits at the end
*GENOCIDE · STRONG*

**What we see.** The Gaza genocide article's first sentence went through these steps:
1. 1 Jan 2024: "Allegations have been made that the 2023 Israel–Hamas war constituted a genocide against the Palestinians."
2. 4 Jan 2024: "The State of Israel has been accused of genocide"
3. 29 Aug 2024: "Experts, governments, United Nations agencies, and non-governmental organisations have accused Israel"
4. 9 Jan 2025: "According to a United Nations agency ... Israel has committed genocidal acts"
5. 24 Feb 2025: "...Israel has committed genocide"
6. 29 Apr 2025: "...Israel is committing genocide"
7. 21 Sep 2025, 01:53 UTC: the first own-voice version, "The Gaza genocide is the ongoing systematic destruction..."
8. 26 Sep 2025, 04:26 UTC: the current sentence

The current sentence reads: "The Gaza genocide is the ongoing, intentional, and systematic destruction of the Palestinian people in the Gaza Strip carried out by Israel during the Gaza war." The title had become "Gaza genocide" by requested move on 3 Jul 2024, replacing "Allegations of genocide in the 2023 Israeli attack on Gaza". Since 26 Sep 2025 there have been 10 edits (9 distinct wordings) trying to bring back attribution, from 10 Oct 2025 to 20 Jul 2026. Examples: "has been described by most scholars as", "the alleged ongoing...", "The accusations of a Gaza genocide are allegations of...". Each was gone within 45 minutes.

In the Israel article, "genocide" has stayed in the lead since 4 May 2025 (00:45 UTC), after 8 earlier insertions from 4 Nov 2023 that did not last. The longest lasted 18.9 days, in April 2025. Today it reads: "After the Hamas-led October 7 attacks, Israel began committing genocide against Palestinians in Gaza. Israel has denied that its actions constitute genocide." These are the last two sentences of paragraph 2. On 1 Oct 2026 the denial read "Israel and its allies, including the United States, deny...". The US was dropped in October 2026.

The Gaza war article (1 Oct 2026) attributes the finding in paragraph 1 and denies it two sentences later: "Many scholarly sources and international organizations ... have concluded that Israel's actions in Gaza constitute genocide under international law." Then: "Israel and its supporters, including the United States, deny that genocide has occurred." In Gaza genocide, Israel's view is in the fifth and last paragraph, second-to-last sentence: "Israel and its supporters maintain that its actions do not constitute genocide, that they are a response to the October 7 attacks, and that Israel's aim has been to destroy Hamas and free Israeli hostages." The next and final sentence answers it: "There is increasing consensus among genocide and international legal scholars on the genocide assessment, although some academics and countries challenge it." The words "self-defence" or "self-defense" appear in none of these leads.

**Chart.** Step chart of voice level (0 alleged, 1 accused, 2 according to, 4 own voice) for the Gaza genocide first sentence, 2024–2026, with red ticks for the 10 reverted attribution attempts after Sep 2025 (`chart_data/oct7_05_genocide_voice.json`).

**So what.** The encyclopedia now states as fact, in its own voice, that Israel is committing genocide. This is the main article on the subject, and also the article on the country. Israel's answer survives in each case as a one-line denial, placed after the charge, or as the second-to-last line of a five-paragraph lead. Meanwhile, the genocide charge against Hamas for October 7 stays attributed ("Some have alleged"). The asymmetry is in the grammar, not just the facts.

**Caveat.** The Israel article's genocide wording on 4 May 2025 is not in our data, only that the word has been there continuously since. The Gaza war lead is as of 1 Oct 2026, its newest full text in our data. The 10 attribution attempts are counted from first-sentence variants. Several were tagged as reverted. We do not know who made them, and under our privacy rules we do not try to find out.

**Examples.**
- Gaza genocide, 10 Oct 2025 (reverted within minutes): "The Gaza genocide has been described by most scholars as the ongoing, intentional, and systematic destruction..."
- October 7 attacks, now: "Some have alleged that the attack was an act of genocide or a genocidal massacre against Israelis."

## 8. 26 May 2025: Hamas's name left the Gaza war's first sentence and the October 7 title on the same day
*WHO IS NAMED · STRONG on dates, NOT TESTED for connection*

**What we see.** From October 2023 the Gaza war's first sentence named the two sides. On 1 Jan 2024 it read "An armed conflict between Israel and Hamas-led Palestinian militant groups has been taking place chiefly in and around the Gaza Strip since 7 October 2023". Until 26 May 2025 it read "The Gaza war has been fought between Israel and Hamas-led Palestinian militant groups in the Gaza Strip and Israel since 7 October 2023." Then:
- 26 May 2025, 16:37 UTC: "The Gaza war is an armed conflict in the Gaza Strip and Israel since 7 October 2023."
- 24 Sep 2025: the date of 7 October was dropped as well.
- Since 16 Oct 2025: "The Gaza war is an armed conflict in the Gaza Strip and Israel, fought as part of the unresolved Israeli–Palestinian and Gaza–Israel conflicts."

Since 26 May 2025 Hamas has been named in that sentence for less than 2 days (23 Nov 2025). Hamas moved to sentence 2. The same day, at 13:08 and 13:13 UTC, the article "October 7 Hamas-led attack on Israel" was moved to "October 7 Attacks" and then "October 7 attacks".

**Chart.** Two aligned ribbons, Oct 2023 to Nov 2026: Gaza war first sentence (green = names Hamas, grey = does not) and the October 7 title (green = contains "Hamas"), with a vertical line on 26 May 2025 (`chart_data/oct7_07_who_is_named_first.json`).

**So what.** In the opening line of the war article, read 2.7 million times in the last 12 months, there is no attacker and, since September 2025, no start date. There is only "an armed conflict in the Gaza Strip and Israel". The October 7 article still names Hamas in its first sentence, but no longer in its title.

**Caveat.** Our data does not link the two edits, and we do not identify editors. A short, generic title ("October 7 attacks") also matches common usage. The Gaza war's sentence 2 names Hamas and gives the toll and hostages, so the information is one sentence later, not gone.

**Examples.**
- Gaza war, 2 Mar 2024: "...since 7 October 2023, when Hamas launched a surprise attack on southern Israel from the Gaza Strip."
- Gaza war, 23 Nov 2025 (1.4 days): "...fought between the State of Israel and Hamas as part of the unresolved Israeli–Palestinian and Gaza–Israel conflicts."

---

## Then vs now: exact quotes

| article / item | then (date) | now (date) |
|---|---|---|
| Hamas, definition | "a Palestinian Sunni-Islamic fundamentalist, militant, and nationalist organization." (2021-08-23 to 2023-10-09) | "a Sunni Islamist Palestinian nationalist political organisation with a military wing known as the al-Qassam Brigades." (since 2025-11-29; last change 2025-12-02) |
| Hamas, short description | "Palestinian Islamic militant nationalist organization" (2021-01) | "Islamist Palestinian political and paramilitary organization" (2026-11) |
| Hamas, terror designation | "Canada, the European Union, Israel, Japan and the United States classify Hamas as a terrorist organization." (sentence 5 of 20, 2021-01-01) | "Several countries have designated Hamas as a terrorist organisation." (sentence 22 of 23, 2026-10-31) |
| Hamas, Israel's role | absent (2021-01-01, 2023-07-01) | "Initially, Hamas was discreetly supported by Israel, as a counter-balance to the secular Palestine Liberation Organization (PLO) to prevent the creation of an independent Palestinian state." (2026) |
| Hezbollah, definition | "a Shia Islamist political party and militant group based in Lebanon." (2021-01) | "a Lebanese Shia Islamist political party with an active paramilitary wing." (2026-10-26) |
| October 7, title | "Operation Al-Aqsa Flood" (12–22 Oct 2023) | "October 7 attacks" (since 2025-05-26) |
| October 7, first sentence | "A series of coordinated attacks, conducted by the Palestinian Islamist militant group Hamas, from the Gaza Strip onto bordering areas in Israel, commenced on Saturday 7 October 2023, a Sabbath day and date of several Jewish holidays." (2023-10-23) | "On October 7, 2023, a series of coordinated armed incursions from the blockaded Gaza Strip into the Gaza envelope of southern Israel were carried out by Hamas and several other Palestinian militant groups." (2026-10-08) |
| October 7, sexual violence | "Israel and international media have reported rape and sexual assault by Hamas fighters with documentary footage and photographs, which Hamas has denied." (2024-01-01) | "Numerous sources have reported dozens of cases of rape and sexual assault." (2026-11-02) |
| October 7, sentence 2 | "In response, Israel intensified its blockade and launched a major military operation in Gaza, actions scholars have concluded constitute genocide." (2026-10-01) | "In response, Israel launched a major military operation in Gaza." (2026-11-02) |
| October 7, hostages | "Approximately 250 Israeli civilians and soldiers were taken as hostages to the Gaza Strip, including 30 children, with the stated goal to force Israel to release Palestinian prisoners." (2024-01-01) | "251 Israeli and non-Israeli civilians and soldiers were taken as hostages to the Gaza Strip." (2026-11-02) |
| Gaza war, first sentence | "An armed conflict between Israel and Hamas-led Palestinian militant groups has been taking place chiefly in and around the Gaza Strip since 7 October 2023..." (2024-01-01) | "The Gaza war is an armed conflict in the Gaza Strip and Israel, fought as part of the unresolved Israeli–Palestinian and Gaza–Israel conflicts." (since 2025-10-16) |
| Gaza war, hostages | "During a seven-day truce, 105 Israeli hostages were exchanged for 240 Palestinian prisoners." (2024-01-01) | "...in which 1,195 Israelis and foreign nationals were killed and 251 were taken hostage." (2026-10-01; only mention) |
| Gaza genocide, first sentence | "Allegations have been made that the 2023 Israel–Hamas war constituted a genocide against the Palestinians." (2024-01-01) | "The Gaza genocide is the ongoing, intentional, and systematic destruction of the Palestinian people in the Gaza Strip carried out by Israel during the Gaza war." (since 2025-09-26) |
| Israel, war sentence | absent; 2023-07-01: "Israel's practices in its occupation of the Palestinian territories have drawn international condemnation for violating the human rights of the Palestinians." | "After the Hamas-led October 7 attacks, Israel began committing genocide against Palestinians in Gaza. Israel has denied that its actions constitute genocide." (2026-11-04) |
| Israel, denial | "Israel and its allies, including the United States, deny that Israel's actions constitute genocide." (2026-10-01) | "Israel has denied that its actions constitute genocide." (2026-11-04) |

## Not answerable with this data
- Exact dates of changes deeper than the first sentence (e.g. when "discreetly supported by Israel" or the Hannibal Directive entered a lead). We can only bracket them between snapshots.
- How hostage coverage in leads changed during the 2025 release deals (no full-lead text between snapshots).
- Who made any of these edits, and whether the 26 May 2025 changes were linked (privacy rule; no coordination test run here).
- Topics of the Hamas RfCs (only counts and close status are stored).
