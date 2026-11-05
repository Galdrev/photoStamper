# Story, sources, languages, exposure: pattern cards

Folder: `patterns/story_sources_langs/`. Chart data in `chart_data/`. Ranked by interest × solidity.

## 1. The new wording sits in the most-read articles
**Confidence:** STRONG (n=407 vs 87, full deep panel, has a comparison group; but views are concentrated, so a handful of articles drive the views share.)

**What we see.** In the deep panel, only 60 of 407 topic articles (15%) gained critical vocabulary in the lead between 2021 and 2026, but those 60 carry 46% of all topic pageviews (615M views, 2021–26). In comparison articles it is the reverse: 24% of articles gained, and they carry 18% of views. The top gainers by traffic are Israel (lead rate 53 -> 138 per 10k words, 43M views), Benjamin Netanyahu (0 -> 74, 27M), Gaza Strip (30 -> 82), Israeli–Palestinian conflict (58 -> 116) and Zionism (28 -> 125).

**Chart.** paired horizontal bars (topic vs comparison): share of articles vs share of pageviews, for 'lead gained critical terms' and 'lead lost critical terms' (`chart_data/exposure_concentration.json`)

**So what.** The change is small when you count articles and large when you count readers. Anyone who audits by sampling articles will under-state it; audits should weight by traffic. For editors, the flagship pages are where the contest happened and where it was decided.

**Caveat.** Pageviews are by current title, so views logged under older titles are missed (e.g. 'Israel and the apartheid analogy', '2023 Israel–Hamas war').

**Examples.**
- Israel lead (2026): 'After the Hamas-led October 7 attacks, Israel began committing genocide against Palestinians in Gaza. Israel and its allies, including the United States, deny that Israel's actions constitute genocide.'
- Benjamin Netanyahu lead (2026): 'Netanyahu's government has been orchestrating the Gaza genocide, culminating in the South Africa v. Israel case before the International Court of Justice (ICJ) in December 2023.'

## 2. Atrocity labels moved into Wikipedia's own voice, and from niche pages to flagship ones
**Confidence:** SUGGESTIVE (A handful of very visible articles, traced edit by edit; one-way trend. There is no large comparison set of 'genocide' articles, so the contrast with Uyghur/Armenian is anecdotal.)

**What we see.** 'Genocide' went from attributed claim to plain statement in the Gaza genocide article in 8 steps (Jan 2024 – Oct 2025). The same plain statement then spread to the highest-traffic leads. Israel's lead has said 'Israel began committing genocide' continuously since 2025-05-04. October 7 attacks now says, in paragraph 1, 'actions scholars have concluded constitute genocide'. Israeli apartheid went from 'analogy' (2021) to 'is a system of institutionalized segregation' (2024-11). Comparison cases split: the Uyghur genocide lead still reads 'has often been characterized as persecution or as genocide'; the Armenian genocide lead (a settled historical case) is stated as fact.

**Chart.** step timeline per article (y = voice level: 0 alleged / 1 accused-by / 2 'X state that' / 3 'according to' / 4 own voice), x = date; one line each for Gaza genocide, Israeli apartheid, Nakba, Israel lead; a flat line for Uyghur genocide as contrast (`chart_data/exposure_timing.json`)

**So what.** The step that matters to readers is not the word appearing but the attribution disappearing. For a journalist, 'Wikipedia says X' is now literally true in the Israel article. For researchers, voice level is a better outcome measure than term counts.

**Caveat.** Voice coding here is done by hand on first sentences of ~6 articles; the Israel lead still carries a denial sentence right after.

**Examples.**
- Gaza genocide 2024-01-01: 'Allegations have been made that the 2023 Israel–Hamas war constituted a genocide against the Palestinians.' -> 2025-10-05: 'The Gaza genocide is the ongoing, intentional, and systematic destruction of the Palestinian people in the Gaza Strip carried out by Israel during the Gaza war.'
- Uyghur genocide 2026: 'Since 2014, the government of China has committed a series of ongoing human rights abuses against Uyghurs ... which has often been characterized as persecution or as genocide.'

## 3. Most readers met the earlier wording: the new definitions arrived after attention had peaked
**Confidence:** STRONG (Arithmetic on full monthly pageviews and the full revision timeline of each lead. 'Settled' means the last flip of the feature, so it is conservative.)

**What we see.** For 15 key topic articles whose current first sentence carries the new wording, 87% of their 172M views (2021–26) came before that wording settled; for the 8 most clearly reframed ones (Zionism, Nakba, Gaza genocide, Israeli apartheid, Hamas, Israeli settlement, West Bank, Gaza war) it is 88% of 67M. Peak month was October 2023 for 16 of 19 key articles (the other three are articles created or renamed during the war), while the current wording settled mostly in 2025–26 (Zionism 2026-08-27, Nakba 2026-07, Israel 2026-09). About 8.9M reader-views a year now meet the reframed wording of those 8 articles; 20.7M a year across the 15.

**Chart.** for each article: monthly pageviews area chart with shading for which first-sentence variant was live (old vs new); or a dot plot of 'peak month' vs 'wording settled' date (`chart_data/exposure_timing.json`)

**So what.** The reframing is a story about the encyclopedia as a record going forward, not about what the October 2023 audience read. The exception is Hamas: 'militant' left its definition within days of 7 October, so the 8.2M October 2023 readers already saw 'a Sunni Islamist political and military organization'. Hamas had 44% of its five-year views in Oct–Dec 2023.

**Caveat.** Title-based pageviews miss views under former titles (Gaza war, October 7 attacks, Gaza genocide had partial early data). 'Settled' depends on a simple text pattern per article.

**Examples.**
- Hamas, Sep 2023 (47k views): '... a Palestinian Sunni-Islamic fundamentalist, militant, and nationalist organization.' Oct 2023 (8.24M views): '... a Sunni Islamist political and military organization that is the de facto gover[ning authority]...'

## 4. English moved; most other Wikipedias barely did
**Confidence:** SUGGESTIVE (English is strong and replicated; the other-language nulls rest on ~500 articles per language and translated lexicons, so small shifts could be missed.)

**What we see.** On the mass tier, the topic-minus-comparison change in lead critical vocabulary is +0.24 per 1,000 words in English (all articles, p<0.001) and +0.43 in English Top-importance articles. In 10 other languages, on the top ~550 articles each, 8 of 10 point estimates are positive but small (mean +0.06), and only Portuguese is clearly above zero (+0.27, p=0.004). Dutch went the other way (−0.27, p=0.08). Arabic key-article leads became, if anything, less dense in these terms (mean −0.8 per 1,000).

**Chart.** forest plot: one row per language, point = topic-minus-comparison change per 1,000 lead words, bars = 95% CI; English rows highlighted (`chart_data/languages_lead_did.json`)

**So what.** This is an English-Wikipedia community story, not a global wave in all Wikipedias. Norms, editor pools and dispute processes (e.g. English arbitration rules for the topic) are the likely explanation, not world events alone. Researchers should not generalise English findings to 'Wikipedia'.

**Caveat.** Lexicons differ (English 7 terms, other languages 5 translated stems), so compare signs and rough size, not exact values.

## 5. One exception crossed languages: 'genocide' entered the Gaza war lead in 9 of 11 Wikipedias, but in different voices
**Confidence:** ANECDOTE (20 articles; term presence only, and voice was read by hand for one article.)

**What we see.** Across 16 key topic articles in 11 languages, the most common additions are 'occupation' (24 article-language additions) and 'genocide' (21). 'Genocide' is concentrated in Gaza war: added in 9 languages (en, de, es, it, nl, ru, he, ar, pl) and already present in fr. Colonial framing was added mainly in English, French, Italian, Dutch and Arabic (2–4 each), and not at all in German, Russian, Hebrew, Spanish or Polish. How it is said differs. Spanish states it as fact ('ha desencadenado un genocidio en Gaza por parte de Israel'). English, French and Dutch attribute it ('Many scholarly sources and international organizations... have concluded'; 'de nombreux observateurs ... qualifier'). Russian frames it as accusations ('подвергся обвинениям'). Hebrew mentions only South Africa's ICJ case.

**Chart.** heatmap: rows = 16 topic + 4 comparison articles, columns = 11 languages, cell = terms added (+) / dropped (−) (`chart_data/crosslang_key20_matrix.json`)

**So what.** Event-driven labels such as 'genocide' for Gaza spread across languages. Re-reading the past (colonialism, 1948) mostly did not. That separates a reaction to the news from a change in historical framing, and the second is mostly an English (and Romance-language) phenomenon.

**Caveat.** Term presence does not show stance; Hebrew and Russian additions are mostly about the accusation, not assertions.

**Examples.**
- es Gaza war: 'La Guerra de Gaza es un conflicto armado en curso ... que ha desencadenado un genocidio en Gaza por parte de Israel contra la población civil palestina.'
- he Gaza war: 'ב-29 בדצמבר 2023 ... דרום אפריקה הגישה תביעה נגד ישראל לבית הדין הבין-לאומי לצדק (ICJ) בגין רצח עם.'

## 6. Zionism and 1948 are retold as colonization and ethnic cleansing, with some pull-backs
**Confidence:** SUGGESTIVE (Matches the replicated finding that the lead change is in older-history sentences (+8.4 of +9.3 per 10k), but the examples are hand-picked flagships.)

**What we see.** Zionism: 're-establishment ... of a Jewish state in ... the historic Land of Israel' (2021) became 'an ethnic nationalist movement ... to establish and support a Jewish homeland through colonization in the region of Palestine' (stable since 2026-08-27). Nakba: 'destruction of Palestinian society' (2021) became 'the ethnic cleansing of Palestinian Arabs by Zionists' (2024-04 onward; perpetrator added 2025–26). Balfour and Israel leads now say Palestine had 'an overwhelming Arab majority'. Pull-backs: the 1948 expulsion article dropped 'by Zionist militias' from its first sentence (May 2025), and 'Zionism as settler colonialism' went back to 'described by some/several scholars'.

**Chart.** then/now card stack, one per article, with the date of each step; colour = direction (`then_vs_now in cards.json`)

**So what.** The biggest shift in the story is about 1897–1948, not about the current war. Readers who look up Zionism now meet a definition that puts colonization in the first sentence. That is the kind of change worth explaining to non-specialists, along with its sourcing (New Historians, settler-colonial scholarship) and its contestedness (44 in-and-out cycles).

**Caveat.** First sentences summarise the body; the bodies still contain the competing views ('Advocates of Zionism have viewed it as a national liberation movement ... of an indigenous people').

**Examples.**
- Nakba 2026-07-06: 'The Nakba ... is the ethnic cleansing of Palestinian Arabs by Zionists through their violent displacement and dispossession ...'
- Israel lead 2026: '... the Zionist movement for a Jewish homeland in Palestine, then an Ottoman region with an overwhelming Arab majority.'

## 7. At scale, first sentences with a critical term rose in topic articles and stayed flat elsewhere
**Confidence:** STRONG (Large n with a comparison group; the timing matches the replicated post-war rise. Absolute levels are small (about 2 in 100 first sentences).)

**What we see.** Across ~4,000 topic articles in the mass tier, the share whose first sentence contains a critical term went 1.26% (Jan 2021) -> 1.48% (Jul 2023) -> 2.08% (Nov 2026), up 65%. Comparison articles: 0.59% -> 0.63% -> 0.66%. The rise is almost all after the war. In deep-panel leads, critical-term mentions in the first paragraph rose 30 -> 39 in topic leads and fell 21 -> 14 in comparison leads; most topic additions land in paragraph 3 or later (5 -> 29).

**Chart.** two-line chart over 3 dates (topic vs comparison share of first sentences with a critical term); inset bars of mentions by lead paragraph (`chart_data/first_sentence_critical_mass.json`)

**So what.** Even after the change, 98% of topic first sentences carry none of these terms. The change is a thin layer that is visible where it matters (flagships), not a rewrite of the whole topic.

**Caveat.** Lexicon-based; it misses rewordings without the listed terms (e.g. 'Southern Levant', 'Palestine').

## 8. The source mix shifted only at the margins: more Arab outlets, fewer advocacy sites, the same Israeli press
**Confidence:** STRONG (Large n (10k articles, ~65k deep-panel refs), comparison group, consistent in deep and mass tiers. Small absolute shares.)

**What we see.** In mass-tier topic articles, Arab and pro-Palestinian outlets rose from 0.63% to 1.68% of citations, and the Israeli-press to Arab-press ratio fell from 11.7:1 to 4.2:1 (comparison: flat at 0.2:1). Pro-Israel advocacy sites fell from 0.95% to 0.57%. Israeli press held at about 7% and rights groups/UN at about 1.5%. In the deep panel, advocacy citations fell in absolute terms (596 -> 429) while the citation pool grew 34%. The biggest shift, 'scholarly' rising from 37% to 54%, happened just as much in comparison articles (48% -> 63%): it is a Wikipedia-wide citation-style trend.

**Chart.** small multiples: one line per source class (share of citations, quarterly 2021–2026), topic vs comparison panels; scholarly drawn grey as Wikipedia-wide (`chart_data/citations.json`)

**So what.** The reframing did not come from a flood of partisan sources. Most of the new critical wording is attributed to scholarship and to rights bodies, which were already cited. A good line for presenters: 'the words changed more than the sources did'. Arab press is still cited about 4× less than Israeli press.

**Caveat.** Domain-based classes: the 'Arab & pro-Palestinian' class mixes Al Jazeera, +972 (Israeli) and Anadolu (Turkish); 'Other' (25–45%) is unclassified.

## 9. Hedging runs at two speeds: more attribution in the long tail, less in the flagship leads
**Confidence:** SUGGESTIVE (The mass trend has a comparison group; the deep-lead series is small (61–93 mentions per quarter).)

**What we see.** Across 10k mass-tier articles, the share of loaded-term mentions that carry attribution ('accused of', 'described as', ...) rose in topic articles from 21.8% to 25.0%; comparison stayed at 16.7–17.2%. In the 332 deep-panel topic leads, the hedged share climbed to 45% in Oct 2023, then fell to 26–28% by 2026, while unhedged mentions per lead rose 46% (0.13 -> 0.19). Comparison leads stayed flat (1.00 -> 1.01). In the coded study-3 pairs, though, 'attribution density down' was as common in comparison leads (31%) as in topic leads (25%).

**Chart.** two-panel line chart: hedged share over time, (a) mass full text, 3 dates, (b) deep leads, quarterly; topic vs comparison (`chart_data/hedging.json`)

**So what.** New loaded terms usually arrive hedged and get de-hedged later in the visible places. That is the Gaza genocide pattern at system scale. Stripping attribution is also a general editing habit (comparison articles do it too), so the topic-specific part is where it happened, not that it happened.

**Caveat.** Attribution is a regex window (~120 chars before, 60 after) and will count denials and quotations as hedges.

## 10. Neutral geography and 'Palestine' replace older names in first sentences
**Confidence:** SUGGESTIVE (Consistent with the replicated 'Palestine spreads' finding; small counts in the deep panel.)

**What we see.** 'Southern Levant' appears in 10 topic leads in 2026 (3 in 2021; first sentences 1 -> 7), and in no comparison lead. First sentences naming 'Palestine' rose 30 -> 43. The West Bank went from a 'landlocked territory ... bordered by ... Israel' with 'Yehuda VeShomron' in the first sentence to 'the larger of the two Palestinian territories ... that make up Palestine' (2026-04). Jerusalem: 'Middle East' -> 'Southern Levant'; 'Palestinian Authority' -> 'Palestine'. Israel's 'Southern Levant' wording flipped 15 times before settling (2026-09).

**Chart.** slope chart 2021 -> 2026 of the number of topic leads / first sentences using each name: Southern Levant, Palestine, Land of Israel/Eretz, Judea and Samaria, homeland (`chart_data/lead_vocabulary_deep.json`)

**So what.** Naming is where the change is quietest and most lasting: it rarely triggers revert wars (West Bank 1 revert in 14 first-sentence edits), and it shapes every downstream use (search snippets, AI answers).

**Caveat.** 'Palestine' counts include the region, the Mandate and the state; only reading tells them apart.

**Examples.**
- West Bank 2021-04-02: 'The West Bank (... HaGadah HaMa'aravit or Yehuda VeShomron) is a landlocked territory near the Mediterranean coast of Western Asia...' -> 2026-04-03: '... is the larger of the two Palestinian territories (the other being the Gaza Strip) that make up Palestine.'

## 11. Jewish history is kept, but the named tie between the people and the land is thinner
**Confidence:** ANECDOTE (A few flagship leads; aggregate counts are mixed.)

**What we see.** History of Israel dropped 'the birthplace of the Jewish people' (live 2022-12 to 2023-04) for 'spans the Southern Levant, from prehistoric African migrations'. The Jews lead dropped 'in the part of the Levant known as the Land of Israel' and 'their homeland'. 'homeland' in topic first sentences: 5 -> 1. It is not one-way: 'Land of Israel/Eretz' appears in 24 topic leads in 2026 (20 in 2021; 11 gained, 7 lost), and Zionism's definition keeps 'the Land of Israel in Judaism—itself central to Jewish history'.

**Chart.** gained/lost dot chart for 'Land of Israel' and 'homeland' across topic leads, with article names (`chart_data/lead_vocabulary_deep.json`)

**So what.** The 'adds on top, keeps Jewish history' finding holds for content, but the connecting phrases (birthplace, homeland) are what readers use to link ancient Jewish history to modern Israel. That framing effect is not caught by term counts.

**Caveat.** Some of these removals were style edits (MOS:FIRST, lead clutter), not stance edits.

**Examples.**
- History of Israel 2022-12-31: 'The Land of Israel, also referred to as the Holy Land or as Palestine, is the birthplace of the Jewish people and Judaism.' -> 2026-04-07: 'The history of Israel spans the Southern Levant, from prehistoric African migrations and the Natufian culture (c. 10,000 BCE) to the emergence of Canaanite civilization.'

## 12. Changes the other way are real but smaller and fewer
**Confidence:** SUGGESTIVE (Counted on the curated set; earlier blind coding found direction lopsided in small counts.)

**What we see.** Agency removed: the 1948 expulsion article dropped 'by Zionist militias' (May 2025). Hedge added: Israeli settlements moved 'built in violation of international law' out of the first sentence (2023-01) and now adds 'but Israel disputes this'. Claim narrowed: Israeli apartheid dropped 'to a lesser extent in Israel proper' (2026-09). Re-attributed: 'Zionism as settler colonialism' back to 'some/several scholars'. More antisemitism in leads: mentions in 54 topic leads in 2026 vs 37 in 2021 (18 gained, 1 lost), including Israel ('Israeli independence prompted antisemitism in the Arab world and Jewish exodus'). Hamas keeps its terrorist designations in the lead, and 'resistance movement' (Aug 2024) did not stick.

**Chart.** diverging bar: count of first-sentence/lead moves by direction (critical vs other way) for the 17 then/now cases (`then_vs_now in cards.json`)

**So what.** A fair presentation should say that the picture is lopsided, not one-sided. Editors pushed back successfully on agency claims and scope, while labels and definitions moved further.

**Caveat.** The 'then vs now' set was chosen for consequence, not randomly.

**Examples.**
- Israeli settlement 2021: '... built in violation of international law on lands occupied by Israel ...' -> 2026: '... The international community considers Israeli settlements to be illegal under international law, but Israel disputes this.'

## 13. Advocacy citations fell before Wikipedia's ADL ruling, not after it
**Confidence:** SUGGESTIVE (Deep panel only (~60 articles in the subgroup); no article-level test.)

**What we see.** In deep-panel Judaism and antisemitism articles, ADL citations per article fell from 2.75 (Jan 2021) to 1.66 (Jul 2022), then held at 1.8–1.9 through and after the June 2024 reliability ruling (1.81 in Apr 2024, 1.89 in Oct 2024, 1.91 in Oct 2026). Topic-wide, the figure went 0.57 -> 0.40 by mid-2022 and was flat after.

**Chart.** line chart of ADL citations per article, quarterly, with a vertical marker at June 2024 (`chart_data/citations.json`)

**So what.** Formal source rulings may codify what editors already did, rather than trigger a purge. Journalists who covered the 2024 ruling as a turning point would find no visible step in these articles.

**Caveat.** Counts all adl.org links, including those on non-I/P topics where the ruling does not apply.

## Then vs now: first sentences and leads (17 changes)

### Zionism redefined

**Zionism** (critical)
- THEN (2021-01): "Zionism ... is both an ideology and nationalist movement among the Jewish people that espouses the re-establishment of and support for a Jewish state in the territory defined as the historic Land of Israel (roughly corresponding to Canaan, the Holy Land, or the region of Palestine)."
- NOW (2026-08-20 (stable since 2026-08-27)): "Zionism is an ethnic nationalist movement that emerged in late 19th-century Europe to establish and support a Jewish homeland through colonization in the region of Palestine, which roughly corresponds to the Land of Israel in Judaism—itself central to Jewish history."
- 're-establishment' -> 'establish'; 'colonization' enters Wikipedia's voice (first tried July 2024, kept in some form since Oct 2024); Land of Israel kept but demoted to a clause. 15.2M views 2021-26; 1.96M in the last 12 months.

**Zionism as settler colonialism** (other way)
- THEN (2025-09-08): "Zionism has been described by its founders and early leaders, as well as several scholars, as a form of settler colonialism ..."
- NOW (2026-01-13 / 2026-02): "Zionism has been described by some scholars [later: several scholars] as a form of settler colonialism in relation to the region of Palestine and the Israeli–Palestinian conflict."
- Edit summary 'more NPOV': the claim was pulled back to attributed, scholar-only framing.

### 1948 retold

**Nakba** (critical)
- THEN (2021-12-24): "The Nakba, also known as the Palestinian Catastrophe, was the destruction of Palestinian society and homeland in 1948, and the permanent displacement of a majority of the Palestinian Arabs."
- NOW (2026-07-06): "The Nakba (النَّكْبَة) is the ethnic cleansing of Palestinian Arabs by Zionists through their violent displacement and dispossession of land, property, and belongings, along with the destruction of their society and the suppression of their culture, identity, political rights, and national aspirations."
- 'ethnic cleansing' in Wikipedia's voice from 2024-04-24; perpetrator named 2025-12 ('by Israel'), then 'by Zionists' (2026-07, 'Plan Dalet ... was executed before the declaration'). Past tense 'was' -> present 'is'.

**1948 Palestinian expulsion and flight** (other way)
- THEN (2023-07-07): "In 1948 more than 700,000 Palestinian Arabs ... were expelled or fled from their homes by Zionist militias, during the 1948 Palestine war."
- NOW (2025-05-30 -> 2026-03-19): "During the 1948 Palestine war, more than 700,000 Palestinian Arabs – about half of Mandatory Palestine's predominantly Arab population – were expelled or fled from their homes."
- The agent ('by Zionist militias', later 'by Zionist paramilitaries ... by its military') was removed from the first sentence in May 2025 by an undo; 68% of 2021-26 views had seen the agent-named version.

**Balfour Declaration** (critical (emphasis))
- THEN (2022-10-19): "... in Palestine, then an Ottoman region with a small minority Jewish population."
- NOW (2026-06-04): "... in Palestine, then an Ottoman region with a small Jewish minority among an overwhelming Arab majority, mostly Muslim but also including Christians."
- The Arab majority is now named in the first sentence; same phrase added to the Israel lead ('then an Ottoman region with an overwhelming Arab majority').

**Deir Yassin massacre** (mixed)
- THEN (2021-01): "... when around 130 fighters from the Far-right wing Zionist paramilitary groups Irgun and Lehi killed at least 107 Palestinian Arabs ..."
- NOW (2026-10): "... when Zionist paramilitaries attacked the village of Deir Yassin near Jerusalem, then part of Mandatory Palestine, killing at least 107 Palestinian Arab villagers ..."
- 'Far-right wing' and the named groups (Irgun, Lehi) drop out of the first sentence; actor generalised to 'Zionist paramilitaries'.

### Land naming

**West Bank** (critical (naming))
- THEN (2021-04-02): "The West Bank (... HaGadah HaMa'aravit or Yehuda VeShomron) is a landlocked territory near the Mediterranean coast of Western Asia, bordered by Jordan ... and by Israel to the south, west and north."
- NOW (2026-04-03): "The West Bank is on the western bank of the Jordan River and is the larger of the two Palestinian territories (the other being the Gaza Strip) that make up Palestine."
- 'Judea and Samaria' dropped from the first sentence (2023-06); 'Palestinian territories' (2023-11), then 'that comprise the State of Palestine' (2024-08), then just 'Palestine' (2026-04).

**Jerusalem / Israel / History of Israel** (neutralising)
- THEN (2021-01): "Jerusalem is a city in the Middle East ... | Israel ... is a country in Western Asia ... | The Land of Israel, also known as the Holy Land or Palestine, is the birthplace of the Jewish people ..."
- NOW (2024-04-17 / 2025-07-31 / 2026-04-07): "Jerusalem is a city in the Southern Levant ... Both Israel and Palestine claim Jerusalem as their capital city | Israel ... is a country in the Southern Levant region of West Asia. | The history of Israel spans the Southern Levant, from prehistoric African migrations and the Natufian culture (c. 10,000 BCE) to the emergence of Canaanite civilization."
- 'Southern Levant' becomes the default neutral geography (topic leads using it 3 -> 10; comparison 0 -> 0). 'Palestinian Authority' -> 'Palestine' in Jerusalem. Israel's 'Southern Levant' wording flipped 15 times.

**Mandatory Palestine** (naming)
- THEN (2021-07-15): "Mandatory Palestine (... Pālēśtīnā (E.Y.), where 'E.Y.' indicates Ērētz Yīśrā'ēl, the Land of Israel) was a geopolitical entity ..."
- NOW (2026-09-19): "Mandatory Palestine, officially known as Palestine, was a British administrative territory in the region of Palestine between 1920 and 1948."
- The Hebrew 'E.Y.' (Eretz Yisrael) gloss left the first sentence in 2023-03 (MOS:LEADCLUTTER).

### Atrocity labels in Wikipedia's voice

**Gaza genocide** (critical)
- THEN (2024-01-01): "Allegations have been made that the 2023 Israel–Hamas war constituted a genocide against the Palestinians."
- NOW (2025-10-05): "The Gaza genocide is the ongoing, intentional, and systematic destruction of the Palestinian people in the Gaza Strip carried out by Israel during the Gaza war."
- 8 one-way steps: alleged -> accused -> 'state that' -> 'according to' -> own voice. Contrast: Uyghur genocide still opens '... has often been characterized as persecution or as genocide.'

**Israel (lead, 2nd paragraph)** (critical)
- THEN (2021-01): "(no genocide or apartheid in lead) ... Israel's occupation of the Palestinian territories is internationally considered to be the world's longest military occupation in modern times."
- NOW (2026-10 (genocide sentence continuous since 2025-05-04)): "... most Middle East experts arguing that Israel's treatment of Palestinians in the West Bank ... constitutes a system of apartheid. After the Hamas-led October 7 attacks, Israel began committing genocide against Palestinians in Gaza. Israel and its allies, including the United States, deny that Israel's actions constitute genocide."
- The most-read article in the topic set (43M views 2021-26; 4.7M last 12 months). Same move in Benjamin Netanyahu: 'Netanyahu's government has been orchestrating the Gaza genocide'.

**Israeli apartheid** (critical, then narrowed)
- THEN (2021-04-29): "Israel and the apartheid analogy is criticism of Israel charging that Israel has practiced apartheid against Palestinians, primarily in its occupation of the West Bank ..."
- NOW (2026-09-28): "Israeli apartheid is a system of institutionalized segregation and discrimination in the Israeli-occupied Palestinian territories."
- Analogy -> accusation -> 'assert' -> own voice (2024-08). Latest edit removed 'and to a lesser extent in Israel proper' (narrower claim). Title itself moved from 'Israel and the apartheid analogy'.

**October 7 attacks** (mixed)
- THEN (2024-01-21): "On 7 October 2023, the paramilitary wings of Hamas, the Palestinian Islamic Jihad, the PRC, PFLP, and the DFLP launched a series of coordinated armed incursions into the Gaza envelope ..., the first invasion of Israel since the 1948 Arab–Israeli War."
- NOW (2026-10): "On October 7, 2023, a series of coordinated armed incursions from the blockaded Gaza Strip ... were carried out by Hamas and several other Palestinian militant groups killing at least 1,195 people ... In response, Israel intensified its blockade and launched a major military operation in Gaza, actions scholars have concluded constitute genocide."
- Passive voice; 'blockaded' added; death toll added to first sentence (more detail on the victims); Israel's response and 'genocide' now in the opening paragraph of the attack article. 'massacring civilians in 21 communities' in paragraph 2.

### Armed groups

**Hamas** (softer label)
- THEN (2021-01): "Hamas ... is a Palestinian Sunni-Islamic fundamentalist but pragmatic, militant, and nationalist organization."
- NOW (2025-10-05): "The Islamic Resistance Movement, abbreviated Hamas ..., is a Sunni Islamist Palestinian nationalist political organisation with a military wing known as the al-Qassam Brigades."
- 'militant' and 'fundamentalist' gone; the change began within days of 7 Oct 2023 ('political and military organization' was live through the 8.2M-view October 2023). Terrorist designations kept in the lead, moved down; 'resistance movement' tried in Aug 2024 and not kept.

### Jewish history kept, link loosened

**History of Israel / Jews** (loosened)
- THEN (2021-01): "The Land of Israel ... is the birthplace of the Jewish people ... | Jews originated as an ethnic and religious group in the Middle East during the second millennium BCE, in the part of the Levant known as the Land of Israel."
- NOW (2026-04 / 2026-10): "The history of Israel spans the Southern Levant ... | The Israelites emerged from the pre-existing Canaanite peoples to establish the kingdoms of Israel and Judah in the Southern Levant during the Iron Age."
- Jewish origins are still there, but the named link 'Land of Israel' / 'homeland' left both leads. 'homeland' in topic first sentences: 5 -> 1.

### Other way

**Israeli settlement** (other way (hedge added))
- THEN (2021-05-12): "Israeli settlements, or Israeli colonies, are civilian communities ... built in violation of international law on lands occupied by Israel in the 1967 Six-Day War."
- NOW (2024-02-28 / 2026-10): "Israeli settlements, also called Israeli colonies, are the civilian communities built by Israel throughout the Israeli-occupied territories. ... The international community considers Israeli settlements to be illegal under international law, but Israel disputes this."
- Illegality moved out of the first sentence (2023-01) and now carries Israel's dissent; though the 2024 ICJ opinion was added to the lead.

**Antisemitism** (mixed)
- THEN (2021-01): "Antisemitism ... is hostility to, prejudice, or discrimination against Jews. ... Antisemitism is generally considered to be a form of racism."
- NOW (2026-06-17): "Antisemitism, or Jew-hatred, is hostility to, prejudice towards, or discrimination against Jews. ... Whether antisemitism is considered a form of racism depends on the school of thought. ... 'new antisemitism' ... criticism of Israel can serve as a vehicle for attacks against Jews in general."
- 'Jew-hatred' added (2024-09); 'new antisemitism' and Israel now in the lead. Across topic leads, antisemitism mentions rose from 37 to 54 articles (18 gained, 1 lost).

## New questions

### Q1. Does the voice of the Gaza 'genocide' label differ by language (stated as fact vs attributed vs accusation)?
- **Can our data answer it?** Yes, partly. crosslang.json has lead text at each quarter for 20 articles.
- **Quick check:** Done for Gaza war 2026 leads: es states it as fact; en, fr, nl attribute it to scholars and organisations; ru frames it as 'accusations'; he mentions only the ICJ case. A full answer needs a small voice codebook applied to the ~60 language-article leads that contain the term.
- **What we'd need:** Nothing new; hand or LLM coding of existing leads.
- **Feasibility:** 0 requests; ~1 hour of coding
- **Why interesting:** Separates 'the label spread' from 'the encyclopedia asserts it'. That is the core public question.

### Q2. Are other contested atrocity articles (Uyghur, Rohingya, Tigray, Darfur, Yazidi, Bosnian, Sudan 2023) stated in Wikipedia's voice as quickly as Gaza?
- **Can our data answer it?** Only Uyghur and Armenian are in ratchet.json.
- **Quick check:** Uyghur genocide still says 'has often been characterized as persecution or as genocide' after 73 first-sentence variants; Armenian genocide is stated as fact (historical consensus); Gaza genocide is stated as fact after 21 months.
- **What we'd need:** Category:Genocides and Category:Ethnic cleansing members (list=categorymembers), then the first-sentence history per article (prop=revisions&rvprop=content&rvsection=0 at quarterly timestamps, or the full revision walk as in ratchet.py).
- **Feasibility:** 1 request for the list + 24 per article (quarterly) or ~N_revisions/50 for a full walk; ~30 articles -> under 1,000 requests
- **Why interesting:** This is the right comparison group for the voice upgrade. Without it we cannot tell 'Gaza is special' from 'Wikipedia de-hedges genocide labels once UN or court findings arrive'.

### Q3. Did the ADL reliability ruling (June 2024) change citation behaviour?
- **Can our data answer it?** Yes (deep panel, explore.citations).
- **Quick check:** No visible step. ADL per article in Judaism/antisemitism articles fell 2.75 -> 1.66 in 2021–22 and was flat (1.8–1.9) around and after June 2024 (see card adl_before_ruling).
- **What we'd need:** To confirm per article: reference URLs per quarterly revision for the mass tier (rvprop=content at snapshot dates, already fetched in mass.py but only aggregated).
- **Feasibility:** 0 new requests if the en_*.json.gz shards are regenerated with per-domain counts
- **Why interesting:** Tests whether formal source rulings drive content or just ratify it.

### Q4. Do short descriptions and Wikidata descriptions (the text Google, mobile apps and voice assistants show) follow the lead changes, and in which languages?
- **Can our data answer it?** No. Short descriptions are stripped from our prose extracts.
- **What we'd need:** Current: prop=pageprops&ppprop=wikibase-shortdesc (50 titles per request). History: {{Short description}} from section-0 wikitext at each snapshot (prop=revisions&rvprop=content&rvsection=0&rvstart=DATE&rvlimit=1). Wikidata: wbgetentities&props=descriptions|labels|aliases&languages=en|de|fr|...; history via Wikidata item revisions (prop=revisions on Q-id).
- **Feasibility:** current: ~1 request per 50 articles; history: 24 per article (en) + ~5 per Wikidata item
- **Why interesting:** Short descriptions reach more people than leads (search snippets, app headers, AI answers) and are edited by a smaller crowd. 'Zionism: ...' as a short description may differ from the lead.

### Q5. Are page moves (renaming) part of the reframing?
- **Can our data answer it?** Indirectly. The bolded first-sentence names in bisect/leads show at least 4 retitlings: 'Israel and the apartheid analogy' -> 'Israeli apartheid', '1948 Palestinian exodus' -> '1948 Palestinian expulsion and flight', '2023 Israel–Hamas war' -> 'Gaza war', and the Gaza genocide page's earlier titles.
- **Quick check:** In the 40 bisect articles, at least 4 topic articles changed title, against 0 obvious retitlings among the 15 comparison articles (Russo-Ukrainian War only changed case).
- **What we'd need:** list=logevents&letype=move&letitle=<title> (plus redirects: prop=redirects) for all deep and mass articles.
- **Feasibility:** 1–2 requests per article; ~20k for the mass tier, 1k for the deep panel
- **Why interesting:** Titles set the frame in search results and links, and moves need a formal RM discussion, so they track community consensus. Also fixes our pageview undercount (views under old titles).

### Q6. Do categories and navboxes change alongside the lead (e.g. articles newly placed in 'Settler colonialism', 'Genocides in Asia', 'Ethnic cleansing' categories, or a 'Zionism' vs 'Palestinian nationalism' navbox)?
- **Can our data answer it?** No (prose extraction drops categories and templates).
- **What we'd need:** Section-free full wikitext at snapshot dates (prop=revisions&rvprop=content) to parse [[Category:...]] and {{navbox}}; current state via prop=categories|templates.
- **Feasibility:** 24 requests per article for quarterly history; 1 per 50 for current state
- **Why interesting:** Categories are the encyclopedia's own classification. Moving an article into 'Genocides' or 'Colonialism' is the strongest institutional statement, and it feeds Wikidata, search and AI training.

### Q7. Do the lead's own citations (not the whole article's) shift toward rights groups or scholarship when the wording changes?
- **Can our data answer it?** No. Citation counts are for the whole article.
- **What we'd need:** Section-0 wikitext with <ref> bodies at each snapshot (prop=revisions&rvprop=content&rvsection=0), classify domains with explore.SOURCE_CLASSES.
- **Feasibility:** 24 requests per article; ~12k for the deep panel
- **Why interesting:** Tests whether the new lead claims are backed by new kinds of sources, or by the same sources read differently. That is our sources story at the point readers see.

### Q8. Is the same small set of editors driving changes across several language editions?
- **Can our data answer it?** No. Editor IDs are salted hashes and per-wiki only.
- **What we'd need:** Raw usernames of first-sentence editors (bisect/ratchet before hashing), then meta.wikimedia.org action=query&meta=globaluserinfo&guiuser=<name>&guiprop=merged|editcount to see their home wikis and edit counts.
- **Feasibility:** 1 request per editor (~500 editors); needs an ethics/privacy decision
- **Why interesting:** It would distinguish a cross-wiki diffusion of framing by the same people from independent convergence. But it touches individual editors, so report only aggregates.

### Q9. Where in the lead does new critical vocabulary land (first paragraph vs deeper)?
- **Can our data answer it?** Yes (leads.json has paragraphs).
- **Quick check:** Done. Topic leads: first paragraph 30 -> 39 mentions, paragraph 4+ 5 -> 29. Comparison leads: first paragraph 21 -> 14. Most new text goes deep in the lead, but the first paragraph also grew in topic articles while it shrank in comparison ones.
- **What we'd need:** Nothing new; could extend to the mass tier if paragraph indices are stored.
- **Feasibility:** 0 requests
- **Why interesting:** Search snippets and AI summaries draw mostly on the first paragraph, so position decides exposure.

### Q10. How do readers reach the reframed pages, e.g. does 'Israel' send traffic to 'Gaza genocide', and did internal links to 'Nakba' / 'Israeli apartheid' grow?
- **Can our data answer it?** No.
- **What we'd need:** Wikimedia clickstream monthly dumps (dumps.wikimedia.org/other/clickstream/, en, 2021-01..2026-10) for referrer->article pairs; current incoming links via list=backlinks&blnamespace=0.
- **Feasibility:** ~70 monthly dump files (~0.5–1 GB each), offline filtering; backlinks 1–5 requests per article
- **Why interesting:** Turns 'exposure' from pageviews into paths. It would show whether the flagship articles now route readers into the critical-framing articles.
