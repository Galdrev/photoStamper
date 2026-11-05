# Codebook: discourse and voice lens (study 3, phase A, open coding)

Reader lens: who speaks (wikivoice vs attribution), hedging/modality, agency and transitivity, labels, ordering/primacy, scare quotes. Grounded in Entman (selection/salience), Fairclough/van Dijk (transitivity, nominalisation, presupposition) and Wikipedia NPOV "words to watch".

## Material read
- Discovery half only (`data/study3/qual_discovery.json`, 237 pairs: 190 topic, 47 comparison).
- Read: about 85 topic pairs (all of the top 60 by change, plus a spread through the middle and tail, e.g. Sabra and Shatila, Irgun, Haganah, Lehi, Munich, Nakba denial, Land of Israel, Jerusalem, Never again, Beit Hanoun). Read 37 usable comparison pairs (Islam and Tibet leads are template/infobox parse artefacts and were set aside). Read all first-sentence edit histories (24 articles).
- Rough counts are from my reading ("n of 85 topic / n of 37 comparison"). Where noted, they are checked against crude regex counts over all 190/47 leads (`markers.py`). Regex counts are noisy and serve only as a sanity check.
- Data caveat: for articles created after Jan 2021 (Gaza war, Gaza genocide, October 7 attacks, Gaza Strip famine, January 2025 ceasefire) "before" is the earliest available lead (late 2023 to 2024), not a 2021 text.

## Moves ranked by how distinctive they are of topic vs comparison
| rank | move | topic (of 85) | comparison (of 37) | verdict |
|---|---|---|---|---|
| 1 | M5 Ideological relabelling of actors (Jewish/Israeli to Zionist) | ~8 (+1 reverse) | 0 | topic-specific |
| 2 | M7 Presupposed evaluation in NPs / lexicalised names | ~12 | ~1 (regex 0/47) | topic-specific |
| 3 | M1 Voice promotion of legal/atrocity categories | 8 (+3 reverse) | 0 (general attribution collapse 4) | topic-specific subset of a general move |
| 4 | M9 Narrative onset and first-paragraph primacy | ~14 | ~3 | moderately distinctive; direction differs by cluster |
| 5 | M10 Primary-referent naming and co-name order | ~11 | 0 (GEO-only ~3) | moderately distinctive; mixed direction |
| 6 | M2 Consensus quantification of sources | ~11 | ~3 | moderately distinctive |
| 7 | M4 Agent surfacing/backgrounding in harm clauses | ~12 surf. / 4 backgr. | ~5 | weakly distinctive (identity of agent is what differs) |
| 8 | M6 Definitional genus reclassification | ~20 (~24%) | ~9 (~24%) | general style; only the destination class is topic-specific |
| 9 | M3 Rebuttal tail | ~7 | ~3 (regex: 9/190 vs 11/47) | general NPOV style; only which party denies differs |
| 10 | M8 Terrorism-label relocation | ~6 | ~4 | general Wikipedia style (MOS on contentious labels); control move |


## M1 Voice promotion of legal/atrocity categories

**Definition.** A contested legal or atrocity category (genocide, ethnic cleansing, illegal/illegality, war crimes, apartheid, terrorism, state terrorism) that version A presents as someone's claim (accused of, allegations, considered by, critics call, may constitute) is presented in version B in Wikipedia's own voice: as a copular definition, a main-clause assertion, or an unhedged predicate. The broader parent move, attribution collapse for any evaluative claim, is coded as M1-general.

**Include.** The same proposition appears in both versions; in A it sits under an attribution or modal frame; in B it is stated without one, or with the attribution reduced to a trailing list of endorsers ('recognised by ...') that does not scope over the claim. Also code the REVERSE (wikivoice in A, attributed or hedged in B) and record which party the category is applied to.

**Exclude.** Do not code: a claim that is new in B with no attributed counterpart in A (code as content addition); a change only in who is cited (e.g. 'critics' to 'Amnesty International'), which is M2; a label only moved into a noun-phrase modifier, which is M7; descriptive facts (death tolls, dates).

**Examples (verbatim).**

- *Gaza genocide*  
  BEFORE: "Allegations have been made that the 2023 Israel–Hamas war constituted a genocide against the Palestinians."  
  AFTER: "The Gaza genocide is the ongoing, intentional, and systematic destruction of the Palestinian people in the Gaza Strip carried out by Israel during the Gaza war."
- *Israel*  
  BEFORE: "Israel's occupation of the Palestinian territories is internationally considered to be the world's longest military occupation in modern times."  
  AFTER: "After the Hamas-led October 7 attacks, Israel began committing genocide against Palestinians in Gaza."
- *Legality of Israeli settlements*  
  BEFORE: "The international community considers the establishment of Israeli settlements in the Israeli-occupied territories illegal on one of two bases"  
  AFTER: "Israeli settlements in the Israeli-occupied Palestinian territories of the West Bank and the Gaza Strip (former), as well as in the Syrian Golan Heights, are illegal under international law."
- *Israeli settlement (REVERSE direction)*  
  BEFORE: "Israeli settlements are civilian communities inhabited by Israeli citizens, almost exclusively of Jewish ethnicity, built in violation of international law on lands occupied by Israel in the 1967 Six-Day War."  
  AFTER: "The international community considers Israeli settlements to be illegal under international law, but Israel disputes this."
- *Persecution of Uyghurs in China (comparison: abuses promoted, genocide label stays attributed)*  
  BEFORE: "Critics of the policy have described it as the sinicization of Xinjiang and called it an ethnocide or cultural genocide"  
  AFTER: "the government of the People's Republic of China has committed a series of ongoing human rights abuses against Uyghurs and other Turkic Muslim minorities in Xinjiang which has often been characterized as persecution or as genocide."

**Counts.** Topic: Legal/atrocity-category promotion: 8 of 85 topic pairs read (Gaza genocide, Israel, Legality of Israeli settlements, Nakba, Irgun, Purity of arms, Criticism of Israel, Israel and state-sponsored terrorism); reverse: 3 (Israeli settlement, Kingdom of Israel, Munich massacre). M1-general (any evaluative claim): about 13 of 85 forward, 6 reverse.. Comparison: Legal/atrocity-category promotion: 0 of 37 comparison pairs. Uyghurs makes the abuses fact but keeps 'genocide' attributed; Armenian genocide was already in wikivoice in A. M1-general: 4 of 37 (Uyghurs, LTTE, Algerian War, Population exchange)..

**Direction.** In topic articles, moves the categories genocide, ethnic cleansing, illegality and state terrorism, applied to Israel or Zionist actors, from 'claimed by others' to 'stated by Wikipedia'. The reverse cases move 'illegal' (settlements first sentence) and the historicity of the United Monarchy from stated to attributed or hedged. Attribution collapse in general is ordinary encyclopedic tightening that comparison articles show too. Only its application to the highest-stakes legal categories is topic-specific in this sample.

**KPIs.**

- `legal_label_voice_shift` (unit: per article pair; automatable: partly: label location by regex; voice class needs LLM (a dependency-parse heuristic, label inside a complement clause of a reporting verb, gets about 80%)). Regex-locate every token of the label lexicon (genocid*, ethnic cleansing, illegal*, unlawful, war crime*, apartheid, terror*, state terrorism) in A and B. For each, an LLM coder assigns voice class: W (wikivoice assertion), P (presupposed modifier, see M7), A-named (attributed to a named source), A-agg (attributed to an aggregate, e.g. 'many scholars'), H (hedged/modal), D (reported as denied). Score = (#W+#P in B − #W+#P in A), split by the party to whom the label applies (Party X / Party Y, masked).
- `attribution_collapse_events` (unit: per article pair; automatable: no: LLM judgement). LLM aligns propositions between A and B; for each aligned proposition, code frame in A and B (attributed / hedged / wikivoice). Count A→W transitions (collapse) and W→A transitions (re-attribution). Report net and the beneficiary party.

## M2 Consensus quantification of sources

**Definition.** Attribution is given to an aggregate expert or institutional collective carrying a quantifier or consensus term ('many scholars', 'most Middle East experts', 'increasing consensus', 'widely seen', 'numerous', 'a growing number of'), or that quantifier is changed (e.g. 'some' to 'many', or 'many' to 'some'). The quantifier, not the named source, carries the epistemic weight.

**Include.** Code when a quantifier or consensus noun is added, removed or changed on the source of a claim, including asymmetric quantifiers on the two sides of the same issue within one lead (e.g. 'many' for one side and 'some' for the other).

**Exclude.** Named single sources ('Human Rights Watch stated'); quantifiers over victims or events rather than sources; 'scholars differ' or 'debated' with no lean (code as neutral debate framing).

**Examples (verbatim).**

- *Gaza war (asymmetric quantifiers in one lead)*  
  BEFORE: "Widespread civilian deaths have led to both Israel and Hamas being accused of war crimes."  
  AFTER: "Many scholarly sources and international organizations—including UN bodies, NGOs, and the International Association of Genocide Scholars—have concluded that Israel's actions in Gaza constitute genocide under international law."
- *Gaza war (same lead, other side)*  
  BEFORE: "Widespread civilian deaths have led to both Israel and Hamas being accused of war crimes."  
  AFTER: "Some have described the 7 October attacks as a genocide or genocidal massacre of Israelis."
- *Zionism as settler colonialism (first-sentence edits 2025-09-08 and 2026-01-13, 'more NPOV'; the Oct 2026 lead has 'many' again)*  
  BEFORE: "Zionism has been described by its founders and early leaders, as well as by many scholars, as a form of settler colonialism in relation to the region of Palestine and the Israeli–Palestinian conflict."  
  AFTER: "Zionism has been described by some scholars as a form of settler colonialism in relation to the region of Palestine and the Israeli–Palestinian conflict."
- *Israel*  
  BEFORE: "Israel's occupation of the Palestinian territories is internationally considered to be the world's longest military occupation in modern times."  
  AFTER: "Israel's illegal occupation of the Palestinian territories has drawn international criticism, with most Middle East experts arguing that Israel's treatment of Palestinians in the West Bank in relation to Israeli settlers constitutes a system of apartheid."

**Counts.** Topic: about 11 of 85 topic pairs (Gaza war, Gaza genocide, Israel, Zionism, Zionism as settler colonialism, October 7 attacks, Francesca Albanese, Hamas, Kingdom of Israel, Anti-Zionism, Israeli settlement); a regex for quantifier+source+reporting verb rises in 13 of 190 topic leads and falls in 6. Comparison: about 3 of 37 (Romani people 'now believed by historians', Al-Shabaab 'some consider', Native Americans); regex: up in 6 of 47, down in 3.

**Direction.** Shifts epistemic authority from named parties to 'the field'. In the most-changed topic leads, a 'many/most/consensus' quantifier is attached to claims against Israel, and a 'some' quantifier to the parallel claims against Palestinian actors and to the settler-colonial frame when it is challenged. The 'some'/'many' slot is actively contested in edit histories.

**KPIs.**

- `source_quantifier_balance` (unit: per lead (version); automatable: partly: extraction by regex; side assignment needs LLM). Regex-extract quantifier + source-noun spans (many|most|numerous|several|some|a few|growing number|consensus|widely + scholars|experts|historians|organizations|countries|sources). An LLM assigns each to the side whose claim it supports (masked Party X / Party Y) and scores strength (some=1, several=2, many/numerous=3, most/consensus=4). KPI = strength sum for X minus Y; report change A→B.

## M3 Rebuttal tail (asymmetric attribution)

**Definition.** A proposition stated in wikivoice or with consensus framing is followed by a sentence or clause in which a party to the conflict is the grammatical subject of deny / dispute / maintain / reject. The denial is attributed and the claim is not, and the denial comes last.

**Include.** Denial or rebuttal clause added or moved to the end of a paragraph or lead, with a conflict party (state, government, 'X and its supporters') as subject; also code its removal.

**Exclude.** Symmetric 'X describes it as..., whereas Y describes it as...' constructions (both attributed; see West Bank barrier); denials by non-parties (scholars) which are M2.

**Examples (verbatim).**

- *Gaza war*  
  BEFORE: "The United States has sided with Israel in rejecting calls for a ceasefire"  
  AFTER: "Israel and its supporters, including the United States, deny that genocide has occurred."
- *Gaza genocide*  
  BEFORE: "Allegations have been made that the 2023 Israel–Hamas war constituted a genocide against the Palestinians."  
  AFTER: "Israel and its supporters maintain that its actions do not constitute genocide, that they are a response to the October 7 attacks, and that Israel's aim has been to destroy Hamas and free Israeli hostages."
- *Kurdistan Workers' Party (comparison)*  
  BEFORE: "The Kurdistan Workers' Party or PKK  is a Kurdish militant and political organization"  
  AFTER: "Some analysts and organizations disagree with this designation"

**Counts.** Topic: about 7 of 85 (Gaza war, Gaza genocide, Israeli settlement, Two-state solution, Zionism as settler colonialism, Francesca Albanese, Palestine); regex for deny/dispute/maintain: up in 9 of 190 topic leads, down in 4. Comparison: about 3 of 37 (PKK, Islamic State, Uyghurs); regex: up in 11 of 47, down in 3.

**Direction.** Places a party's position as the residual 'other view' after a baseline claim. Frequency is the same in comparison articles, so the construction itself is ordinary Wikipedia NPOV style. What is topic-specific is which party is the subject of 'deny' (in topic leads read: Israel 6, Palestinian actors 0).

**KPIs.**

- `rebuttal_tail_presence_position` (unit: per lead (version); automatable: mostly: regex plus party lexicon; LLM confirmation optional). Regex for (deny|denies|denied|dispute[sd]?|maintain[s]?|reject[s]?) with a sentence subject naming a state, government, organisation or 'supporters'. Record sentence index / number of sentences (position) and subject party (masked). An LLM confirms that the clause rebuts a claim made earlier in the same lead.

## M4 Agent surfacing / backgrounding in harm clauses

**Definition.** Change in how the doer of a harmful act (kill, expel, displace, destroy, besiege, blockade, massacre, annex, capture) is realised grammatically: active subject, by-phrase, possessive ('Israel's actions'), agentive modifier ('Israeli blockade'), or none (agentless passive, nominalisation, ergative 'resulting in displacement'). Surfacing means the agent becomes explicit or more prominent; backgrounding is the reverse.

**Include.** The same harm event appears in A and B and the agent's realisation moves up or down the scale: active subject > by-phrase in same clause > possessive/premodifier > agent in a later sentence > none. Also code agent replacement (militia name to state; state to ideology, which also counts for M5).

**Exclude.** New events with no counterpart; agent changes in non-harm clauses (e.g. 'signed', 'founded'); changes of only the victim description.

**Examples (verbatim).**

- *Nakba*  
  BEFORE: "The Nakba, also known as the Palestinian Catastrophe, was the destruction of Palestinian society and homeland in 1948, and the permanent displacement of a majority of the Palestinian people."  
  AFTER: "The Nakba (النَّكْبَة) is the ethnic cleansing of Palestinian Arabs by Zionists through their violent displacement and dispossession of land, property, and belongings"
- *Sabra and Shatila massacre*  
  BEFORE: "a widespread massacre was carried out by the militia in plain sight of the Israeli Defence Forces (IDF), its ally."  
  AFTER: "between 1,300 and 3,500 civiliansmostly Palestinians and Lebanese Shiaswere killed in Beirut's Sabra neighbourhood and the adjacent Shatila refugee camp by the Lebanese Forces, one of the main Christian militias in Lebanon, with the support of the Israel Defense Forces (IDF)."
- *1948 Palestinian expulsion and flight (first-sentence edit 2023-07-07, summary 'add to avoid use of passive voice'; agent later moved out of sentence 1 on 2025-05-30)*  
  BEFORE: "In 1948 more than 700,000 Palestinian Arabs – about half of prewar Palestine's Arab population – were expelled or fled from their homes, during the 1948 Palestine war."  
  AFTER: "In 1948 more than 700,000 Palestinian Arabs – about half of prewar Palestine's Arab population – were expelled or fled from their homes by Zionist militias, during the 1948 Palestine war."
- *History of Israel (backgrounding: agent absent in both, displaced group also unnamed in B)*  
  BEFORE: "Israeli independence in 1948 was accompanied by an exodus of Arabs from Israel, the Arab–Israeli conflict and a subsequent Jewish exodus from Arab and Muslim countries to Israel."  
  AFTER: "Israel's 1948 independence sparked the 1948 Arab–Israeli War, repelling neighboring armies but resulting in significant regional displacement."
- *Turkish invasion of Cyprus (comparison: surfacing)*  
  BEFORE: "was launched on 20 July 1974, following the Cypriot coup d'état on 15 July 1974."  
  AFTER: "Turkey invaded Cyprus on 20July 1974 in an operation that progressed in two phases over the following month."

**Counts.** Topic: Surfacing of an Israeli/Zionist agent: about 12 of 85 (Nakba, 1948 expulsion, Deir Yassin, Sabra and Shatila, Gaza genocide, Gaza war, Blockade, Palestine, Israeli settlement, Six-Day War, Munich (IDF to 'Israel'), Gaza famine). Backgrounding of an Israeli agent: 3 (History of Israel, Jerusalem 'incorporated into Israel', 1948 expulsion first sentence 2025). Palestinian agent demoted from subject to by-phrase: 1 (October 7 attacks first sentence).. Comparison: about 5 of 37 (Turkish invasion of Cyprus, Armenian genocide 'Spearheaded by the ruling Committee of Union and Progress', Population exchange, Uyghurs, Tigray war).

**Direction.** Overall, moves Israeli or Zionist actors from implicit to explicit doers of displacement and killing, and turns agentless 'exodus/flight/displacement' into agentive 'expelled by / ethnic cleansing by'. Comparison articles show agent surfacing at a lower but real rate. The topic-specific part is the identity and number of surfaced agents and the oscillation in first-sentence edit histories.

**KPIs.**

- `harm_clause_agent_explicitness` (unit: per harm clause, aggregated to share per lead; automatable: mostly: passive/by-agent/nominalisation detection by parse; party mapping needs NER plus LLM). Dependency parse (e.g. spaCy) finds clauses headed by a harm verb or harm nominal from a lexicon. Code realisation: 4 active subject, 3 by-agent, 2 possessive/premodifier, 1 agent elsewhere in paragraph, 0 none. An LLM maps the agent to masked party. KPI = mean explicitness per party and share of agentless harm clauses, A vs B.

## M5 Ideological relabelling of actors (Jewish/Israeli <-> Zionist)

**Definition.** The label for an organised Jewish or Israeli actor changes between ethnoreligious ('Jewish militia', 'Jewish population'), state ('Israel', 'IDF', 'Israeli forces') and ideological ('Zionist(s)', 'Zionist paramilitaries/militants/settlers'), or a specific organisation name is replaced by the collective ideological label.

**Include.** Any mention where the head noun or premodifier designating a Jewish/Israeli collective actor changes category between A and B (in either direction), including first-sentence agent replacement ('by Israel' to 'by Zionists').

**Exclude.** 'Zionism'/'Zionist movement' used as the name of the ideology itself (not an actor); quoting self-designations; changes on Palestinian/Arab actor labels (code separately as M5-P if needed).

**Examples (verbatim).**

- *Haganah*  
  BEFORE: "Haganah (lit. The Defence) was the main paramilitary organization of the Jewish population ("Yishuv") in Mandatory Palestine between 1920 and 1948"  
  AFTER: "The Haganah (הַהֲגָנָה) was the main Zionist paramilitary organization that operated for the Yishuv in the British Mandate for Palestine."
- *Deir Yassin massacre*  
  BEFORE: "The villagers put up stiffer resistance than the Jewish militias had expected and they suffered casualties."  
  AFTER: "The Zionist militants massacred Palestinian Arab villagers, including women and children, using firearms and hand grenades"
- *Nakba (first-sentence edit 2026-07-06, summary 'more precise: [[Plan Dalet]], for example, was executed before the declaration of May 14')*  
  BEFORE: "The Nakba (النَّكْبَة) is the ethnic cleansing of Palestinian Arabs by Israel through their violent displacement and dispossession of land, property, and belongings"  
  AFTER: "The Nakba (النَّكْبَة) is the ethnic cleansing of Palestinian Arabs by Zionists through their violent displacement and dispossession of land, property, and belongings"
- *First Aliyah (REVERSE)*  
  BEFORE: "was a major wave of Zionist immigration (aliyah) to Ottoman Palestine between 1881 and 1903."  
  AFTER: "was a major wave of Jewish immigration (aliyah) to Ottoman Palestine between 1881 and 1903."

**Counts.** Topic: about 8 of 85 toward 'Zionist' (Haganah, Deir Yassin, Nakba, Jewish insurgency in Mandatory Palestine, Arab–Israeli conflict, Zionism 'Zionist settlers', 1948 expulsion, 1948 Arab–Israeli War); 1 reverse (First Aliyah). Regex 'Zionist + actor noun': up in 5 of 190 topic leads, down in 0.. Comparison: 0 of 37; no comparison article relabels an ethnic or state actor with an ideological collective noun.

**Direction.** Moves responsibility for 1947–49 violence from 'Jewish' (ethnoreligious) or named-militia actors to an ideological collective ('Zionists'). It thereby separates the actor from Jews as a people and widens it beyond the State of Israel to pre-state bodies. The one reverse case moves late-Ottoman immigration from ideological to ethnoreligious framing, with a persecution motive added ('stimulated by pogroms').

**KPIs.**

- `actor_label_category_shift` (unit: per actor mention, aggregated per pair; automatable: partly: regex counts of 'Zionist(s) + actor noun' are automatic; cross-version coreference needs LLM). Regex finds mentions with premodifiers/heads in {Jewish, Israeli, IDF, Zionist, Yishuv, named org}. An LLM resolves coreference to the same real-world actor across A and B and codes the category (E ethnoreligious, S state, I ideological, O organisation name). KPI = share of I-labels among Jewish/Israeli actor mentions, A vs B.

## M6 Definitional genus reclassification (first sentence)

**Definition.** The genus (the head noun phrase of 'X is/was a ...', or the equivalent defining predicate) of the first sentence changes category, e.g. from event/allegation to atrocity, from movement to colonial project, from militant/terrorist to political/nationalist, or from 'name given to' to 'existed'.

**Include.** Any change of the head noun or its first defining modifier/adjunct in the first sentence that changes semantic class. Record old and new class from: neutral-descriptive, self-description/nationalist, ethnic-nationalist, colonial/colonization, harm/atrocity, legal-violation, terrorism/militant, contested ('allegations', 'concept', 'may have existed').

**Exclude.** Synonym swaps within the same class ('organization' to 'organisation', 'ideology' to 'movement'); change only in geography or dates; reorder only.

**Examples (verbatim).**

- *Zionism*  
  BEFORE: "is both an ideology and nationalist movement among the Jewish people that espouses the re-establishment of and support for a Jewish state in the territory defined as the historic Land of Israel"  
  AFTER: "Zionism is an ethnic nationalist movement that emerged in late 19th-century Europe to establish and support a Jewish homeland through colonization in the region of Palestine"
- *Palestine Liberation Organization*  
  BEFORE: "is an organization founded in 1964 with the purpose of the "liberation of Palestine" through armed struggle, with much of its violence aimed at Israeli civilians."  
  AFTER: "is a Palestinian nationalist coalition that is internationally recognized as the official representative of the Palestinian people in the occupied Palestinian territories."
- *Jewish Voice for Peace*  
  BEFORE: "is a United States left-wing activist organization focused on the Israeli–Palestinian conflict."  
  AFTER: "is an American anti-Zionist, pro-Palestinian solidarity, and left-wing advocacy organization."
- *Population exchange between Greece and Turkey (comparison)*  
  BEFORE: "stemmed from the "Convention Concerning the Exchange of Greek and Turkish Populations""  
  AFTER: "The 1923 population exchange between Greece and Turkey was the mass expulsion of approximately 1,221,489 Greek Orthodox Christians"
- *Turkish nationalism (comparison)*  
  BEFORE: "Turkish nationalism is a political ideology that promotes and glorifies the Turkish people"  
  AFTER: "Turkish nationalism (Türk milliyetçiliği) is nationalism among the people of Turkey and individuals whose national identity is Turkish."

**Counts.** Topic: Any genus class change: about 20 of 85 (~24%). Change INTO colonial / harm-atrocity / ethnic-nationalist class: 6 (Zionism, Nakba, Gaza genocide, Israeli settlement 'also called Israeli colonies', Genocide of indigenous peoples 'colonial genocide, or settler genocide', Gaza Strip famine). Change OUT of terrorism/armed-struggle class into political/nationalist: 3 (Hamas, PLO, Lehi).. Comparison: Any genus class change: about 9 of 37 (~24%: Population exchange, Al-Shabaab, Al-Qaeda, Taliban, Tigray war, Turkish nationalism, Arab nationalism, Quebec sovereignty, Ukrainian nationalism). Into harm class: 1 (Population exchange). Comparison nationalisms gain no 'ethnic'/'colonization' qualifier..

**Direction.** Genus rewriting as such is ordinary Wikipedia lead maintenance at the same rate in both groups, so it is NOT itself a topic finding. The topic-specific part is the destination class. Jewish/Israeli national subjects move toward ethnic-nationalist and colonization classes, while comparison nationalisms are redefined in neutral or self-descriptive terms. Palestinian armed organisations move from armed-struggle or terrorism genus to nationalist/political genus, the same direction as comparison jihadist groups.

**KPIs.**

- `first_sentence_genus_class` (unit: per first sentence (A and B); automatable: partly: genus extraction by parse is automatic; class assignment by lexicon is automatic for colonial/atrocity/terror lexemes, LLM for the rest). Parse the first sentence; extract the predicate nominal of the copula (or the equivalent 'refers to'/'was the X of'). Include its first adjunct of means/purpose ('through colonization'). An LLM or lexicon assigns one of the eight classes. KPI 1 = genus changed (y/n); KPI 2 = transition matrix old→new class; KPI 3 = presence of colonial/atrocity/legal-violation lexeme in genus or its means adjunct.

## M7 Presupposed evaluation in noun phrases and lexicalised names

**Definition.** An evaluative or legal category is packed into a noun-phrase premodifier, possessive or lexicalised event name ('Israeli-occupied', 'illegal Israeli settlements', 'the blockaded Gaza Strip', 'Israel's forced evacuations', 'the Gaza genocide' used in passing in another article). It is presupposed, not asserted, so it bears no attribution.

**Include.** Addition or removal of such modifiers or names in any sentence of the lead, especially in sentences whose main topic is something else. Count the use of another article's contested title as a common noun phrase (e.g. 'and the Gaza genocide').

**Exclude.** Modifiers that are uncontested official names ('Gaza Strip', 'West Bank'); modifiers inside quotations; main-clause assertions of the same category (M1).

**Examples (verbatim).**

- *Hamas (first-sentence edit 2024-01-11, summary 'extremely unconventional way of saying the territories are occupied')*  
  BEFORE: "is a Palestinian Sunni Islamist political and military organization governing the Gaza Strip of the Palestinian territories, which are occupied by Israel under international law."  
  AFTER: "is a Palestinian Sunni Islamist political and military organization governing the Gaza Strip of the Israeli-occupied Palestinian territories."
- *October 7 attacks (first-sentence edit 2026-02-22)*  
  BEFORE: "The October 7 attacks were a series of coordinated armed incursions from the Gaza Strip into the Gaza envelope of southern Israel"  
  AFTER: "The October 7 attacks were a series of coordinated armed incursions from the blockaded Gaza Strip into the Gaza envelope of southern Israel"
- *Criticism of Israel*  
  BEFORE: "The government of Israel has been criticized for issues regarding Israeli settlements in the Palestinian territories"  
  AFTER: "establishment and expansion of illegal Israeli settlements in the Palestinian territories"
- *Francesca Albanese*  
  BEFORE: "Albanese recommended in her first report that UN member states&nbsp;develop "a plan to end the Israeli settler-colonial occupation and apartheid regime""  
  AFTER: "many corporate entities, including Microsoft, Alphabet Inc., and Amazon, were enabling and profiting from the occupation of Palestinian territories and the Gaza genocide."

**Counts.** Topic: about 12 of 85 (Hamas, Israel, Palestine, October 7 attacks, Criticism of Israel, Francesca Albanese, Purity of arms, Benjamin Netanyahu, Israeli–Palestinian conflict, PLO, Blockade, Human rights in Israel). Regex (illegal occupation/settlement, Israeli-occupied, occupied Palestinian, blockaded): up in 12 of 190 topic leads, down in 2. 'Gaza genocide' as a name: up in 4 leads.. Comparison: about 1 of 37 (Tibet, first-sentence edit 'currently governed as a part of China', a neutral administrative modifier); regex: 0 of 47.

**Direction.** Moves contested legal statuses (occupation, illegality, blockade, genocide) from debated propositions into the taken-for-granted background of other sentences, including first sentences of articles about Palestinian actors or Israeli attacks. The effect is that they travel across articles without attribution. Of all moves this is the most cleanly topic-specific in this sample.

**KPIs.**

- `presupposed_evaluative_np_rate` (unit: per 100 words of lead, and presence in first sentence; automatable: yes (regex); LLM only for quotation/negation exclusion). Regex lexicon of evaluative premodifiers and lexicalised names: (illegal|unlawful) + N; Israeli-occupied; occupied (Palestinian|territor*); blockaded; besieged; forced (evacuation|displacement); '<Place> genocide'; Nakba used outside its own article. Count per 100 words in A and B; flag first-sentence presence separately. An LLM check excludes quotations.

## M8 Terrorism-label relocation (general style; control move)

**Definition.** 'Terrorist/terrorism' is moved out of the first-sentence genus or actor label into an attributed designation list, often moved to the end of the lead, or moved from actor to act ('terrorist group' to 'terrorist attack ... militant organisation'). Also the reverse: terrorism stated in wikivoice for an act or actor.

**Include.** Any change in the position (genus / actor premodifier / act noun / attributed designation sentence) or voice of terror* lexemes.

**Exclude.** Changes inside the list of designating countries only (count changes); 'counter-terrorist' operation labels unless the actor label also changes.

**Examples (verbatim).**

- *Munich massacre*  
  BEFORE: "by eight members of the Palestinian terrorist group Black September"  
  AFTER: "The Munich massacre was a terrorist attack during the 1972 Summer Olympics in Munich, West Germany, carried out by eight members of the Palestinian militant organisation Black September."
- *Lehi (militant group)*  
  BEFORE: "was a Zionist paramilitary organization founded by Avraham ("Yair") Stern in Mandatory Palestine that used terrorist means in its actions."  
  AFTER: "was a Zionist paramilitary militant organization founded by Avraham ("Yair") Stern in Mandatory Palestine in 1940."
- *Irgun (REVERSE: added in wikivoice)*  
  BEFORE: "was a Zionist paramilitary organization that operated in Mandate Palestine between 1931 and 1948."  
  AFTER: "The organization committed acts of terrorism against Palestinian Arabs, as well as against the British authorities"
- *Al-Shabaab (militant group) (comparison)*  
  BEFORE: "is a terrorist, jihadist fundamentalist group based in East Africa."  
  AFTER: "is a transnational Wahhabi-Salafi Jihadist militant organization."

**Counts.** Topic: about 6 of 85 (Hamas, Munich massacre, Lehi, PLO, Irgun [reverse], Entebbe raid); regex terror*: down in 13 of 190 topic leads, up in 6. Comparison: about 4 of 37 (Al-Shabaab, Al-Qaeda, Islamic State first-sentence history: 'terrorist' added 2023 then removed, PKK); regex: down in 6 of 47, up in 4.

**Direction.** Moves 'terrorist' from Wikipedia's naming of an actor to governments' designation of it (attributed), consistent with the Wikipedia style guideline on contentious labels. It is applied to Palestinian groups, pre-state Zionist groups and comparison jihadist groups alike. This is NOT topic-distinctive and should be treated as a baseline move that KPIs must net out. The only asymmetry seen is that one Zionist group (Irgun) gained a wikivoice terrorism statement while Lehi lost one.

**KPIs.**

- `terror_label_slot` (unit: per lead (version); automatable: yes (regex and position rules); party via lexicon). Regex terror*; classify slot by position/pattern: G (in first-sentence genus), M (actor premodifier), E (act/event noun), D (designation sentence with 'designated/classified/listed by'), W (other wikivoice predicate). Record sentence index. KPI = slot distribution A vs B, by actor party.

## M9 Narrative onset and first-paragraph primacy

**Definition.** Change in (a) the earliest causal event or condition the lead names as the start of the story, and (b) which party, act or toll fills the first paragraph and first grammatical-subject slots. Examples: a conflict now 'has its origins in the rise of Zionism', a 2007 blockade now 'dates to the early 1990s', terror designations moved from paragraph 1 to the last paragraph.

**Include.** Insertion, deletion or movement (across paragraph boundaries) of a causal-background clause, a casualty figure, a designation, or a response clause that changes what the first paragraph says happened first or matters most.

**Exclude.** Pure length trimming that keeps order; updating of numbers in place; moves within the same paragraph that do not change the first subject.

**Examples (verbatim).**

- *Israeli–Palestinian conflict*  
  BEFORE: "Public declarations of  claims to a Jewish homeland in Palestine, notably the 1897 First Zionist Congress and the 1917 Balfour Declaration, created early tension in the region."  
  AFTER: "The conflict has its origins in the rise of Zionism in the late 19th century in Europe, a movement which aimed to establish a Jewish state through colonization in the region of Palestine."
- *Blockade of the Gaza Strip*  
  BEFORE: "The blockade of the Gaza Strip is the ongoing land, air, and sea blockade of the Gaza Strip imposed by Israel and Egypt in 2007, after Hamas took control of the Gaza Strip during the Battle of Gaza"  
  AFTER: "The restrictions on movement and goods in the Gaza Strip imposed by Israel date to the early 1990s."
- *October 7 attacks*  
  BEFORE: "The attacks initiated the 2023 Israel–Hamas war, almost exactly 50 years after Operation Badr and the greater Yom Kippur War of 6 October 1973."  
  AFTER: "In response, Israel intensified its blockade and launched a major military operation in Gaza, actions scholars have concluded constitute genocide."
- *Antisemitism in the United States (onset shifts toward rising-threat frame)*  
  BEFORE: "Despite this, however, antisemitic incidents were following a generally decreasing trend in the last century along with the general reduction in socially sanctioned racism in the United States since World War II and the Civil Rights Movement."  
  AFTER: "As of 2023, the FBI calculated that antisemitic incidents accounted for 68% of all religion-based hate crimes, an increase of 63% since 2022"
- *History of Australia (comparison: onset moved from Aboriginal arrival to 1901 state)*  
  BEFORE: "The history of Australia is the story of the land and peoples of the continent of Australia."  
  AFTER: "The Commonwealth of Australia was proclaimed on 1 January 1901 as a federation of six self-governing former British colonies."

**Counts.** Topic: about 14 of 85 (Israeli–Palestinian conflict, Arab–Israeli conflict, Palestine, Israel, History of Israel, Hamas, Gaza war, October 7 attacks, Blockade, Criticism of Israel, Anti-Zionism, Human rights in Israel, Antisemitism in the United States, Wikipedia and the Israeli–Palestinian conflict). Comparison: about 3 of 37 (History of Australia, Turkish invasion of Cyprus, Tigray war).

**Direction.** In conflict articles, moves the story's starting point earlier, from 1947–48 or 2007 to Zionist colonization (1880s) or the 1990s closures. It places Israeli action and Palestinian tolls or legal findings in paragraph 1, and moves designations of Palestinian groups as terrorist to the end. In antisemitism articles, it moves from a 'declining, fringe' frame to a 'rising' frame. The two subcorpora move in different directions, so the KPI must be computed per article cluster.

**KPIs.**

- `onset_event_and_first_subject` (unit: per lead (version); automatable: partly: (4) and casualty-number presence by regex; (1)–(2) need LLM). An LLM answers for each version: (1) the earliest year/event presented as a cause of the article's subject; (2) the grammatical subject of the first main clause of paragraphs 1 and 2 (masked party / neutral); (3) whether paragraph 1 contains casualty figures for each party; (4) the paragraph index of any terrorist-designation sentence. KPI = change in onset year; change in first-subject party; designation paragraph index moved (Δ).

## M10 Primary-referent naming and co-name order

**Definition.** Change in which name or framework is the primary referent of the subject or its region in the first sentence (Land of Israel / Palestine / Southern Levant / Holy Land; Temple Mount / al-Haram al-Sharif; Western Wall / Buraq Wall; Eretz Yisrael gloss), and in the order and status of co-names (bold alternative names, 'known to Muslims as', 'in Jewish tradition').

**Include.** Addition, deletion, reordering or demotion (to 'in Jewish tradition', 'known in the Arab world as', later sentence) of a religious-national toponym in the first sentence or first paragraph.

**Exclude.** Transliteration/script fixes; region-scale tweaks only (West Asia to Southern Levant), which comparison country articles show equally; mark them as GEO and do not count.

**Examples (verbatim).**

- *History of Israel*  
  BEFORE: "The Land of Israel, also known as the Holy Land or Palestine, is the birthplace of the Jewish people"  
  AFTER: "The history of Israel spans the Southern Levant, from prehistoric African migrations and the Natufian culture (c. 10,000 BCE) to the emergence of Canaanite civilization."
- *Mandatory Palestine (first-sentence edit 2023-03-24, summary '[[MOS:LEADCLUTTER]]')*  
  BEFORE: "Mandatory Palestine (where "E.Y." indicates ’Eretz Yiśrā’ēl, the Land of Israel) was a geopolitical entity established between 1920 and 1948 in the region of Palestine under the terms of the League of Nations Mandate for Palestine."  
  AFTER: "Mandatory Palestine was a geopolitical entity established between 1920 and 1948 in the region of Palestine under the terms of the League of Nations Mandate for Palestine."
- *Temple Mount (Arabic name raised to co-primary)*  
  BEFORE: "known to Muslims as the Haram esh-Sharif"  
  AFTER: "The Temple Mount or al-Haram al-Sharif (הַר הַבַּיִת, الحَرَم الشَّرِيف or الأَقْصَى) is an elevated plateau in the Old City of Jerusalem that comprises the Islamic religious compound known as al-Aqsa"
- *Western Wall (REVERSE: Arabic name demoted)*  
  BEFORE: "The Western Wall, Wailing Wall (HaKotel HaMa'aravi), often shortened to The Kotel or Kosel, known in Islam as the Buraq Wall"  
  AFTER: "The Western Wall (הַכּוֹתֶל הַמַּעֲרָבִי; Ashkenazi Hebrew pronunciation: HaKosel HaMa'arovi) is an ancient retaining wall of the built-up hill known to Jews and Christians as the Temple Mount of Jerusalem."

**Counts.** Topic: about 11 of 85 (History of Israel, Israel, Mandatory Palestine, Zionism, Homeland for the Jewish people, Land of Israel, Place names of Palestine, Temple Mount, Western Wall [reverse], Aliyah, Hamas [Arabic full name now leads]); plus about 5 GEO-only tweaks (Jerusalem, Israel 'Southern Levant'). Comparison: 0 of 37 non-GEO; GEO-only tweaks in about 3 (Jordan, Saudi Arabia, Egypt); Tibet's 'currently governed as a part of China' is an administrative modifier, not a co-name change.

**Direction.** Mostly moves the first-sentence frame from Jewish-tradition referents (Land of Israel, Eretz Yisrael, 'birthplace of the Jewish people') to geographic or Palestine-region referents, keeping the Jewish name as a subordinate gloss ('corresponds to the Land of Israel in Judaism'). Islamic co-names are raised for shared holy sites. One holy-site article (Western Wall) moves the other way. Direction is mixed, so code per name.

**KPIs.**

- `first_sentence_toponym_primacy` (unit: per first sentence; automatable: yes (regex and pattern rules); LLM only to resolve 'Israel' state vs region). Regex lexicon of region/site names (Land of Israel, Eretz Yisrael, Israel [region sense], Palestine, Holy Land, Canaan, Southern Levant, Judea, Temple Mount, al-Haram al-Sharif, al-Aqsa, Western Wall, Buraq, Kotel). Record order of first appearance, whether bolded/co-primary ('X or Y') or subordinate ('known to Muslims as', 'in Jewish tradition'). KPI = rank change of each name A→B.

## Cross-cutting KPI notes for an LLM coder on masked pairs
- Mask party names as Party X / Party Y consistently within a pair, and keep the label lexemes (Zionist, Jewish, Israeli, militant, terrorist) visible, because they are the object of M5/M8. Randomise A/B order.
- Every KPI should be computed for comparison articles too, and topic effects reported net of the comparison rate. This matters most for M3, M6 and M8, which are general style.
- Code direction per proposition and per party, never per article, because single articles contain opposite moves (Israeli settlement vs Legality of Israeli settlements; Temple Mount vs Western Wall; Irgun vs Lehi).
- Fully automatable (regex/parse): M7 rate, M8 slot, M10 toponym order, M3 presence/position, M5 'Zionist + actor noun' counts, M4 passive/agentless share, label-token location for M1/M2.
- Need LLM judgement: M1 voice class and proposition alignment, M2 side assignment, M4/M5 cross-version coreference, M6 genus class (outside a lexicon), M9 onset event and first subject.

## Expected but NOT found
- **"so-called"**: zero occurrences in any lead, before or after, in either group.
- **Scare quotes as a stance device are declining, not rising**: quoted spans fall in both groups (topic: up in 26 leads, down in 50; comparison: up 8, down 18). This is general de-quoting/cleanup. Residual topic scare quotes are few ("Axis of Resistance", "open-air prison", "wall of apartheid", "Jewish homeland").
- **"Terrorist" added to Palestinian actors**: not found. The move runs the other way (M8), in line with comparison jihadist groups.
- **"Settler-colonial" as the first-sentence genus of Zionism**: not found. The colonial frame enters as a means adjunct ("through colonization"), while "settler colonialist" stays attributed to "Opponents of Zionism".
- **Contested denominations in wikivoice** ("Judea and Samaria", "Zionist entity", "neighbourhood" for East Jerusalem settlements): not found. "Judea and Samaria" appears only as an attributed Israeli administrative name ("the Israeli government administers the West Bank as the Judea and Samaria Area"), as before. "Zionist entity" never occurs. The Israeli settlement before-lead's "Jewish neighborhoods" framing, which it attributed to Israel, has left the lead.
- **Removal of Jewish origin claims from the Jews article**: not found; "originating from the Israelites" is stable across 10 first-sentence edits. The removals happen in region and history articles (History of Israel, Mandatory Palestine) instead (M10).

## Surprises
1. **Grammatical compromise in the genus.** Zionism keeps "nationalist movement" as head noun but gains a means adjunct ("through colonization") and a modifier ("ethnic"), each added and fought over separately in the edit history ("ethnocultural" then "ethnic", "colonization of" then "colonization in"). Coders should code the head, the modifier and the adjunct separately.
2. **Explicit templating on comparison atrocities.** An editor reordered the Nakba definition "to put the action ahead of the perpetrator compare [[The Holocaust]]". The Gaza genocide and Nakba first sentences now share the syntax of The Holocaust and Armenian genocide ("X is/was the [systematic] [destruction|ethnic cleansing] of [group] by [agent]"). The genus template is borrowed, and only its application is new.
3. **NPOV and MOS rhetoric is used to justify both directions**: "'state' is more neutral than 'accuse'" (toward wikivoice), "more NPOV" (many to some scholars), "add to avoid use of passive voice" (agent added), "[[MOS:AVOIDBOLD]]" (October 7 first sentence turned passive with Hamas in a by-phrase).
4. **Asymmetric quantifiers within one lead** (Gaza war: "Many scholarly sources ... have concluded" vs "Some have described the 7 October attacks as a genocide"). A sentence-level check misses this; the KPI has to compare quantifiers across sentences of the same lead.
5. **Presupposition travels across articles.** "The Gaza genocide" as a proper-name NP shows up in Albanese, Netanyahu and Purity of arms, and "blockaded Gaza Strip" in the October 7 first sentence. The category spreads through backgrounded noun phrases more than through assertions. M7 is the cleanest topic-specific signal and is regex-countable.
6. **Antisemitism articles move in the opposite salience direction from conflict articles**: "decreasing trend" / "fringe phenomenon" sentences are removed and rising hate-crime figures lead; Protocols becomes "an antisemitic hoax and forgery". Pooling all topic articles into one direction score would cancel real movement.
7. **Agent oscillation in first sentences**: 1948 expulsion gained "by Zionist militias" (2023), had it rephrased (2024), then lost it from sentence 1 (2025), with the agents moved to sentence 2. Static A/B snapshots understate this churn, so a KPI on first-sentence edit counts per move would add information.
