# Codebook, lens: EDITORIAL PROCESS (study 3, qualitative phase A, discovery half only)

Reader: close reader 3 (ethnography of editing: contested claims, justification repertoire, settlement, bundling).
Material: `data/study3/qual_discovery.json` only. I read 48 topic lead pairs in full (from the most changed down to change 0.14, sampled through the middle) and 16 comparison pairs (plus 3 `control_contaminated`: Arab nationalism, Palestinian nationalism, Saudi Arabia, counted separately and not in comparison figures). I read all 198 traced first-sentence edits: 147 in 17 topic articles and 51 in 7 comparison articles (Islam, Islamic State, Tibet, Armenian genocide, Kashmir conflict, Irish nationalism; Islam and IS make up 30 of the 51).
Project code read (read-only): `trace_changes.py`, `ratchet.py`, and the term lists in `analyze.py`. I did not open holdout, `leads.json`, `bisect.json` or `ratchet.json`.

All statements describe what the text states as baseline and how that changed. Nothing here is a judgement of truth or bias.

## 0. Caveat that shapes everything below: the traces are a thinned sample

`trace_changes.py` bisects only between consecutive quarterly snapshots and returns the **first** revision in each interval that changed the first sentence. So each article has at most one traced edit per quarter, and any later edits in the same quarter are invisible. In the discovery traces, **66% of consecutive topic edits (85/129) and 64% of comparison edits (29/45) have an untraced change between them**: the `before` of edit k+1 is not the `after` of edit k. Several decisive frame changes happened in such untraced edits: the wikivoice definition of the Gaza genocide, "ethnic cleansing" entering the Nakba first sentence, "colonization" entering Zionism, and Hamas losing "fundamentalist"/"militant". In/out counts below are therefore lower bounds. "Reverted" is the `mw-reverted` tag only (7/147 topic, 1/51 comparison). Comments are truncated at 300 characters.

Consequence for the frozen codebook: process KPIs should be computed from `ratchet.py`'s full lead history (every revision of section 0), not from `bisect.json` alone.

## 1. Contested-claims catalogue (full table: `contested_claims.csv`, 36 topic and 7 comparison elements)

The most heavily worked elements, with a lower bound on traced changes and the winner at Oct 2026:

| Article | Element | Path (abridged) | Winner / stable since |
|---|---|---|---|
| Gaza genocide | epistemic status | "Allegations have been made" > "has been accused" > "state that" > "According to..." > "is committing" > wikivoice definition. 8 traced, 0 reverted, **monotone** | wikivoice, since about 2025-10 (21 months from first version) |
| Nakba | perpetrator in sentence 1 | absent > "the State of Israel's" (2025-08, **reverted**, "Israel fails to be mentioned in the lede") > "Israeli ethnic cleansing" [untraced, by 2025-12] > "by Israel" > "by Zionists" (2026-07, Plan Dalet chronology) | named perpetrator; identity still moving 3 months before window end |
| Nakba | "ethnic cleansing" | "destruction of Palestinian society" > "violent displacement" [u] > "ethnic cleansing" [u, Feb–Apr 2024] | stable about 30 months |
| Nakba | tense was/is | at least 5 flips | "is" (ongoing) |
| 1948 expulsion and flight | agent in sentence 1 | "by Zionist militias" in (2023-07, "avoid use of passive voice") > chain (2024-03, reverted) > chain back [u] > "Zionist" dropped (2024-05) > agent removed (2025-05, "not a coherent part of a sentence") | **relocated** to sentence 2, which names Haganah, Irgun, Lehi |
| 1948 expulsion and flight | "fled or were expelled" order | at least 6 flips | "were expelled or fled", anchored to the page title ("matching order of title", after the RM) |
| Zionism | territorial head noun | "LoI is the key word" (2022-10) > restoration "known in the Bible as the Land of Israel" (2023-07, **reverted**) > "in Palestine, a region roughly corresponding to the Land of Israel" [u] | Palestine as head noun since 2023-10 |
| Zionism | re-establishment | "re-establishment" > "establishment" [u, 2021] > restoration (2024-07, **reverted**) | "establish" |
| Zionism | colonization | absent > present [u, by 2024-07] > object churned 3 times | "through colonization in the region of Palestine" (about 27 months) |
| Zionism | nationalism adjective | ideology and nationalist > ethnic or ethno-cultural [u] > ethnocultural (per talk) > "ethnic nationalist" (2026-08, "roughly equal weight in sources") | not stabilised |
| Zionism as settler colonialism | attribution quantifier | unattributed > "some" > "several" > "founders... and several" > "many" > "some" ("more NPOV") | unresolved at end of series |
| Israeli settlement | "colonies" | added 2021-05 citing "a number of [[WP:RS]]"; removal 2023-10 **reverted** | stuck for 5.5 years |
| Israeli settlement | illegality | "built in violation of international law" in sentence 1 > removed [u] | relocated to sentence 3, attributed to "the international community" plus "Israel disputes this" |
| Hamas | genus | "fundamentalist... militant" > "political and military" [u] > "resistance movement" (2024-08, NPOV) > "political organisation with a military wing" [u] | stable since 2024-10 |
| Anti-Zionism | definition | minimal > critical definition (2022-06) > ethnonationalism variants > minimal | **returned to** "Anti-Zionism is opposition to Zionism." |
| Israel / Jerusalem | macro-region | 5 and 4 flips between Western Asia, West Asia, Levant and Southern Levant | "Southern Levant", settled by cross-article precedent ("per formatting on pages for [[Jordan]], [[Lebanon]]") and "least politically contentious" |
| History of Israel | "birthplace of the Jewish people" | in > out ("better NPOV language") > in (refs) > out (MOS:OPEN, MOS:FIRST) | out since 2023-04 |

Comparison elements are of the same kinds: Islamic State "former" quasi-state toggles; "terrorist" in and out of the first sentence; the alternative-name list removed per talk and then restored; Tibet's "Greater Tibet"/"Xizang" names; Armenian genocide's perpetrator moved **out** of sentence 1 "per FAC". **No monotone ratchet appears in the comparison traces.**

Trajectory tally (`contested_claims.csv`). Topic, 36 elements: oscillation 13 (5 finally anchored by a talk outcome, page title, style rule or cross-article precedent), bold edit that stuck 12, ratchet 5, relocation 4, return to minimum or start 2. Seven elements were still changing in the last 6 months. Comparison, 7 elements: oscillation 4, relocation 2, short-lived 1.

## 2. Justification repertoire

Regex coding of edit summaries (`scripts/trace_stats.py`), hand-checked:

| | topic (147 edits) | comparison (51) |
|---|---|---|
| empty summary | 24 (16%) | 10 (20%) |
| talk / forum reference (per talk, discussion, RM, FAC) | 15 (10%) | 2 (4%) |
| style code (MOS:FIRST, AVOIDBOLD, LEADCLUTTER, OPEN, LEADCITE) | 10 | 4 |
| source-based argument (RS, "sources", "per body", "per source") | 16 | 2 |
| explicit neutrality appeal (NPOV, "neutral", "less contentious") | 5 | 0–1 |
| "RfC", "restore consensus", WP:DUE/UNDUE | **0** | 0 |
| substantive change (word similarity < 0.8) under an empty or copyedit-type summary | 16 (11%) | 2 (4%) |
| anticipatory hedging ("I hope this isn't contentious", "If problematic, revert and join the discussion") | 7 | 1 |
| first-sentence change riding on a >1000-byte article edit (bundling proxy) | 11 (7.5%) | 2 (4%, both Tibet infobox) |

Justification by direction. I hand-coded the 40 or so frame-relevant topic edits. A = adds a critical term or Israeli/Zionist agent, removes attribution, or adds Palestinian context. B = adds attribution, removes an agent or critical term, or restores Jewish-tradition anchoring. J− = removes a Jewish-tradition gloss or toponym.
- **A (18 edits):** source-count or reliability 5 ("a number of [[WP:RS]]"; "many relaible sources"; "roughly equal weight in sources"; "unreliable definition from MW"); clarity, cleanup or style labels 6 (including "avoid use of passive voice" for adding "by Zionist militias", and "Copy edit for clarity" for adding the Arab majority to Balfour); neutral-word argument 2; omission argument 1; talk or procedural 1; empty 2. Reverted 2 of 18. Both reverted A-claims reappeared later in the window.
- **B (12 edits):** sources 5 (including 'the sources referenced in the article use the word "re-establishment"'); accuracy, clarification or grammar 4; procedural complaint 2 ("removed without discussion", "without any explanation"); NPOV 1. Reverted 3 of 12. None of the reverted B-claims reappeared in the window.
- **J− (4 edits with summaries):** 3 of 4 cite style rules (MOS:OPEN/FIRST, LEADCLUTTER, "removing low-quality link introduing [sic] an unnecessary element of history and politics") or "better NPOV language".
- **Neutrality is used as rhetoric in both directions:** for removing "birthplace of the Jewish people" (History of Israel), for "resistance movement" (Hamas), for "state" over "accuse" (Gaza genocide), and for "many" back to "some scholars" (Zionism as settler colonialism).
- Analogy and precedent appear as a separate repertoire: "compare [[The Holocaust]]" (Nakba word order), "per formatting on pages for [[Jordan]], [[Lebanon]]" (Israel), "per title" (October 7 attacks, 1948).

## 3. Settlement patterns and time to stabilise

- **Forum-settled (talk, RM, FAC):** Gaza war name (bold name reverted under MOS:FIRST, then "Reworked lead, according to discussion on Talk page", about 5 months); Israeli–Palestinian conflict stakes clause ("per discussion in Talk"); Zionism adjective and goal verb ("Per talk"); 1948 order (title fixed by RM, and the first sentence later forced to match it); October 7 "blockaded" restored "per talk page—disagreement with edit is procedural rather than substantive". **No traced RfC closures.**
- **Bold edit that sticks:** "colonies" (2021-05, 5.5 years); Eretz Yisrael gloss removed via LEADCLUTTER (3.5 years); History of Israel MOS rewrite (3 years); Mandatory Palestine "British". The most consequential ones are untraced: Gaza genocide wikivoice, Nakba "ethnic cleansing", Zionism "colonization".
- **Ratchet:** small one-directional steps with no traced reversal (Gaza genocide, 8 steps over 21 months). The Nakba perpetrator was reverted once and stuck within at most 5 months.
- **Attrition / oscillation:** labels with no dominant usage in sources (geography, nationalism adjective, verb order, quantifiers). These end either by an external anchor (title, precedent) or not at all.
- **Return to minimum:** Anti-Zionism, settlement quantifier "almost exclusively".
- **Relocation as compromise:** the element leaves sentence 1 but stays in the lead (1948 agent, settlement illegality, Jews/Judaism). Comparison: Armenian genocide perpetrator ("per FAC").
- Activity: the share of article-quarters with a first-sentence change rose from 32% (51/158) before Oct 2023 to 45% (95/209) after, in topic traces. Comparison stayed flat (38% to 36%, 25/65 and 26/72). Note that the comparison article with the most first-sentence change overall was Islamic State (20 traced edits): churn alone is not a topic feature.

## 4. Bundling

- Single-edit bundles: History of Israel 2022-09 (−2563 bytes: removes "birthplace", "better NPOV language", drops citation); Anti-Zionism 2022-06 (+4406 bytes, new definition); Israeli settlement 2023-10 (removes "colonies", "civilian" becomes "residential", adds "established by Israel": **reverted as a bundle**); 1948 2024-03 (agent chain, "forcibly expelled", "made to flee": **reverted**, then the agent chain reappeared separately by 2024-05). Hypothesis to test: **bundles get reverted, and their components return one at a time.**
- Interval bundles (one untraced interval containing several frame changes): Hamas Oct 2023 to Jan 2024 (drops "fundamentalist" and "militant", adds "governing", adds "occupied ... under international law"); Zionism Apr–Jul 2024 ("ethnic or ethno-cultural", "late 19th century", "colonization", "deeply embedded in Jewish history").
- Same-week pairs across articles: Zionism (2023-10-24) and Zionism as settler colonialism (2023-10-23); Israeli–Palestinian conflict (2024-03-09) and Zionism as settler colonialism (2024-03-10, "No engagement on talk page, WP:DRNC"). Editor hashes in `bisect.json` could test whether these are the same hand.
- Many traced edits fall in the first weeks of January, April, July and October. This is a bisect artifact (the first change after each snapshot), so traces cannot measure bursts at week level.

## 5. Contrast with comparison traces (thin)

There are 7 comparison articles; Kashmir, Armenian genocide and Irish nationalism have 1–2 edits each, and Islam and Islamic State dominate. The same mechanics appear there: naming wars, tense/status toggles, MOS:FIRST clutter fights, labels relocated out of sentence 1, anticipatory hedging ("this should be less controversial i hope"). What I did not see in comparison traces: a monotone attribution ladder, a named perpetrator moved **into** sentence 1, source-count arguments, or explicit neutrality appeals used in opposite directions. Treat these differences as hypotheses, not findings.

## 6. Moves

Moves 1–8 can be coded from lead pairs. Moves 9–10 need edit summaries or revision sequences. They are ordered by my estimate of how distinctive they are of topic vs comparison (see the counts in each move). M6–M8 are mostly general Wikipedia style.

### M1 Epistemic upgrade (attribution to assertion)

**Definition.** A contested characterisation of an actor or event (e.g. genocide, ethnic cleansing, apartheid, illegality, terrorism, an intent claim) climbs one or more steps on the attribution ladder between A and B: 0 absent; 1 'allegations'/'accused'; 2 attributed to a named minority ('some historians', 'critics'); 3 attributed to named authorities ('According to the UN...'); 4 majority or consensus claim ('scholars widely', 'growing scholarly consensus'); 5 stated in the encyclopedia's own voice (wikivoice) or used as the article's definitional genus. A downgrade is the same move in reverse and is coded with negative sign.

**Include.** The same proposition appears in both versions (or is absent in A) and its ladder level differs by at least one step. Counts in either direction and for any subject (Israeli, Palestinian, Jewish, Roman...). Code each proposition once per pair.

**Exclude.** Pure rewording at the same level ('accused' to 'charged'); new facts with no evaluative content; quantity updates (death tolls); attribution changes that only swap one named authority for another at the same level.

**Examples (verbatim).**

- *1948 Palestinian expulsion and flight*  
  before: "The expulsion of the Palestinians has since been described by some historians as ethnic cleansing, while others dispute this charge."  
  after: "Scholars widely describe the event as ethnic cleansing, although some disagree."
- *Legality of Israeli settlements*  
  before: "The international community considers the establishment of Israeli settlements in the Israeli-occupied territories illegal on one of two bases"  
  after: "are illegal under international law."
- *Gaza genocide*  
  before: "Allegations have been made that the 2023 Israel–Hamas war constituted a genocide against the Palestinians."  
  after: "The Gaza genocide is the ongoing, intentional, and systematic destruction of the Palestinian people in the Gaza Strip carried out by Israel during the Gaza war."
- *Bar Kokhba Revolt*  
  before: "The common view that the name change was intended to "sever the connection of the Jews to their historical homeland" is disputed."  
  after: "an act intended to sever the region's historical association with the Jewish people"

**Count (my reading).** Topic: 16 of 48 topic pairs read (15 toward wikivoice for claims about Israeli/Zionist conduct; 1, Bar Kokhba, toward wikivoice for a claim about Roman intent against Jews). Comparison: 3 of 16 comparison pairs (Kashmir conflict, Armenian genocide 'concurring with the academic consensus', Persecution of Uyghurs)

**Direction.** Moves contested characterisations from reported speech into the narrator's voice; in topic articles this mostly concerns Israeli or Zionist conduct (genocide, ethnic cleansing, illegality, apartheid).

**KPIs.**

- `attribution_ladder_delta` (per contested proposition per pair (mean per pair); automatable: partly: candidate propositions found by regex on a term list (genocid*, ethnic cleansing, apartheid, illegal, terroris*, colonial*), level needs LLM). LLM coder lists each evaluative proposition in A and B, aligns them, assigns ladder level 0-5 in each version, reports B minus A. Report share of pairs with any upgrade, any downgrade, and net sum.
- `wikivoice_share_contested_terms` (per lead (share of occurrences); automatable: yes (regex + clause split); validate on 50 hand-coded sentences). For each occurrence of a contested term, check whether the clause contains an attribution marker (according to, described, accused, alleged, critics, some/many scholars, considered, regarded) within the same clause; share without marker.

### M2 Record-the-denial (assert then append counter-position)

**Definition.** B states or strengthens a claim and adds, in the same or the next sentence, the subject's or its allies' denial or dispute ('X and its supporters deny...', 'X disputes this'), often followed by a rebuttal ('The ICJ ... countered many of Israel's arguments'). The dissent is recorded as a position held by a party, not as a competing scholarly view.

**Include.** A denial/dispute sentence attributed to the accused party or its allies is new in B or newly adjacent to a claim that was upgraded (M1). Include the variant where B adds a rebuttal of the denial.

**Exclude.** Symmetric 'proponents argue / critics argue' paragraphs that were already present in A; denials of a factual incident unrelated to the article's main characterisation.

**Examples (verbatim).**

- *Israel*  
  before: "(no corresponding text in A)"  
  after: "Israel and its allies, including the United States, deny that Israel's actions constitute genocide."
- *Legality of Israeli settlements*  
  before: "Israel has consistently argued that the settlements are not in violation of the Fourth Geneva Convention"  
  after: "The ICJ's 2024 advisory opinion countered many of Israel's arguments."
- *Nakba*  
  before: "(no corresponding text in A)"  
  after: "Israel negates or denies the atrocities it committed, claiming that many of the expelled Palestinians left willingly or that their expulsion was necessary and unavoidable."

**Count (my reading).** Topic: 11 of 48 topic pairs. Comparison: 1 of 16 (Persecution of Uyghurs; Armenian genocide already had the pattern in A). Regex proxy over all substantial leads does NOT reproduce the difference (denial-word density up in 10% topic vs 22% comparison), so this count rests on close reading only.

**Direction.** Recasts the dissenting position from a scholarly counter-view into a party position held by the accused state and its allies; the claim itself becomes the baseline.

**KPIs.**

- `party_denial_after_claim` (per pair (0/1) and per contested proposition; automatable: no (needs LLM; regex on deny|dispute is too noisy)). LLM coder: does B contain a sentence attributing denial/dispute of a central claim to the subject or its allies, positioned after the claim? Was it present in A? Code new=1.
- `dissent_carrier_type` (per dissent statement; automatable: partly (named-entity heuristics), LLM for final code). Code who carries dissent: scholars/experts, governments/parties, 'supporters of X', unnamed 'others'. Compare distributions A vs B.

### M3 Camp labelling of actors and sources

**Definition.** B identifies an organisation, source or set of critics by its partisan alignment ('pro-Israel organizations', 'pro-Palestinian', 'Israel and its supporters', 'its pro-Israel advocacy') where A named them neutrally, by institution, or not at all.

**Include.** A new partisan-alignment label attached to an actor that speaks, acts or is the subject. Includes 'X and its supporters/allies' as a grouping of dissenters.

**Exclude.** Self-descriptions in quotation; alignment labels already present in A; country lists without an alignment adjective.

**Examples (verbatim).**

- *Anti-Defamation League*  
  before: "is an international Jewish non-governmental organization based in the United States."  
  after: "The ADL is also known for its pro-Israel advocacy."
- *Francesca Albanese*  
  before: "In February 2023, a bipartisan group of 18 members of the United States Congress called for Albanese to be removed from her position"  
  after: "Pro-Israel organizations, including the U.S. government, have accused Albanese of antisemitism and anti-Israel bias, and have called for her removal."
- *Palestinian right of return*  
  before: "The government of Israel does not view the admission of Palestinian refugees to their former homes in Israel as a right"  
  after: "The government of Israel, and its supporters, state that Palestinian refugees do not have the right of return under international law."

**Count (my reading).** Topic: 8 of 48 topic pairs (regex proxy: new label in 7.6% of substantial topic leads). Comparison: 0-1 of 16 (Uyghurs groups signatory states by region, not by alignment; regex proxy 0% of substantial comparison leads)

**Direction.** Shifts the description of critics or defenders from institutional identity to alignment, which positions their statements as advocacy.

**KPIs.**

- `camp_label_rate` (per lead (count per 10 sentences) and per pair (new=1); automatable: yes for detection; LLM for quotation check). Regex: pro-Israel|pro-Palestinian|pro-Zionist|anti-Israel|and its (supporters|allies)|supporters of; count in A and B; flag new labels; LLM check that the label is the narrator's, not a quotation.

### M4 Colonial-framework vocabulary in definitional position

**Definition.** B introduces or strengthens colonial/settler-colonial vocabulary (colonization, colonies, colonial, settler colonial, imperial power) as part of the definition or origin story of the subject, in the first paragraph, in wikivoice or attributed.

**Include.** Term family coloni*/settler colonial*/imperial added to the first paragraph, or moved from an attributed critics' sentence into the definitional sentence. Record attribution level separately (M1).

**Exclude.** Purely historical uses already in A ('Colonial Office'); uses about other empires unrelated to the subject; vocabulary in quotations of named persons only.

**Examples (verbatim).**

- *Zionism*  
  before: "espouses the re-establishment of and support for a Jewish state in the territory defined as the historic Land of Israel"  
  after: "to establish and support a Jewish homeland through colonization in the region of Palestine"
- *Israeli settlement*  
  before: "Israeli settlements are civilian communities inhabited by Israeli citizens"  
  after: "Israeli settlements, or Israeli colonies, are civilian communities inhabited by Israeli citizens"
- *Irish nationalism*  
  before: "chiefly descended from people from Great Britain who arrived as settlers"  
  after: "chiefly descended from people of Great Britain who colonised the land as settlers"

**Count (my reading).** Topic: 8 of 48 topic pairs (Zionism, Israeli–Palestinian conflict, Arab–Israeli conflict, Zionism as settler colonialism, Israeli settlement, Anti-Zionism, Genocide of indigenous peoples, Israel). Comparison: 2 of 16 (Irish nationalism, Aboriginal Australians). Frequency is NOT distinctive; regex proxy is higher in comparison (8% vs 4%). What is distinctive is location: in topic it enters the first sentence of the core concept (Zionism) and the origin paragraph of conflict articles.

**Direction.** Places the subject within a colonisation narrative of origins rather than a return/national-revival narrative.

**KPIs.**

- `colonial_vocab_position` (per lead (index of first sentence containing the term; 0 = first sentence); automatable: yes). Regex coloni[sz]*|settler[- ]colonial*|imperial; report earliest sentence index in A and B and whether in wikivoice (no attribution marker in clause).

### M5 Naming and toponym arbitration

**Definition.** B changes the names used for the subject or its place: which name is the head noun, which are glosses, whether alternative names get parity ('X or Y', 'also called Y'), and which macro-region label locates it (Western Asia, the Levant, Southern Levant; Land of Israel vs Palestine).

**Include.** Change of head name or toponym, addition/removal of an alternative name, reordering of names, removal of a traditional-name gloss, change of macro-region label.

**Exclude.** Transliteration, diacritics and pronunciation fixes; template/markup changes that drop or restore a name accidentally (check against the edit summary or the following snapshot).

**Examples (verbatim).**

- *Temple Mount*  
  before: "known to Muslims as the Haram esh-Sharif"  
  after: "The Temple Mount or al-Haram al-Sharif"
- *Zionism*  
  before: "centered in the area roughly corresponding to what is known in Jewish tradition as the Land of Israel"  
  after: "a homeland for the Jewish people in Palestine, a region roughly corresponding to the Land of Israel in Jewish tradition"
- *Mandatory Palestine*  
  before: "Mandatory Palestine (where "E.Y." indicates ’Eretz Yiśrā’ēl, the Land of Israel) was a geopolitical entity"  
  after: "Mandatory Palestine was a geopolitical entity"  
  edit summary: "[[MOS:LEADCLUTTER]]"
- *Jerusalem*  
  before: "Jerusalem is a city in West Asia, on a plateau"  
  after: "Jerusalem is a city in the Southern Levant, on a plateau"  
  edit summary: ""West Asia" is far too broad, and "Southern Levant" is probably the least politically contentious way to describe where the city is located"

**Count (my reading).** Topic: 15 of 48 topic pairs. Comparison: 4 of 16 (Islamic State, Tibet, Tigray war, Quebec sovereignty movement)

**Direction.** In topic articles: from Jewish-traditional toponyms as primary (Land of Israel, Eretz Yisrael gloss) to Palestine/regional terms as primary, and toward parity of Arabic and Hebrew names; settles disputes by inclusion of names rather than choice.

**KPIs.**

- `alt_names_first_sentence` (per first sentence (count); automatable: yes). Count name-introducing constructions (also known as, also called, or the, officially, abbreviated) and bolded/parenthetical names in the first sentence of A and B.
- `toponym_head_noun` (per lead; automatable: partly (parse), LLM to confirm). For leads mentioning both 'Land of Israel'/'Eretz Israel' and 'Palestine', code which term is syntactic head and which is gloss (LLM or dependency parse).

### M6 Causal-context insertion

**Definition.** B adds to the opening of an event or actor a prior condition, grievance or enabling circumstance that frames the cause ('from the blockaded Gaza Strip', 'despite the village having agreed to a non-aggression pact', 'rooted in the Israeli–Palestinian conflict').

**Include.** A new clause or sentence in the first paragraph that explains why the event happened or what preceded it, or new modifiers that encode a precondition (blockaded, occupied, after X).

**Exclude.** Chronological background already present in A; consequences (what followed) rather than antecedents.

**Examples (verbatim).**

- *October 7 attacks*  
  before: "launched a series of coordinated armed incursions into the Gaza envelope of neighboring Israeli territory"  
  after: "a series of coordinated armed incursions from the blockaded Gaza Strip into the Gaza envelope of southern Israel"
- *Deir Yassin massacre*  
  before: "(no corresponding text in A)"  
  after: "The massacre was carried out despite the village having agreed to a non-aggression pact."
- *Liberation Tigers of Tamil Eelam*  
  before: "(no corresponding text in A)"  
  after: "The LTTE was subsequently founded in 1976 as a reaction to the Sri Lankan Constitution of 1972"

**Count (my reading).** Topic: 11 of 48 topic pairs. Comparison: 4 of 16 (LTTE, Kashmir conflict, Al-Shabaab, Armenian genocide). Not distinctive in frequency; general Wikipedia practice. Direction-specific content only.

**Direction.** Adds antecedent grievances or conditions, which shifts the explanatory weight of an event toward prior conduct of the other party (in topic: Israeli blockade/occupation; in the Gaza famine pair the reverse, adding Palestinian-side causes such as looting).

**KPIs.**

- `antecedent_clauses_first_paragraph` (per first paragraph (count new in B); automatable: no). LLM coder lists causal/antecedent clauses in paragraph 1 of A and B and attributes each to a party whose conduct it describes.

### M7 Agent naming for harm

**Definition.** B names the actor responsible for a harm where A used passive voice, an agentless nominal, a fringe-only actor, or no actor ('were expelled' to 'were expelled by Zionist paramilitaries'; 'a militia' to 'with the support of the IDF').

**Include.** New 'by X', possessive ('Israel's'), active-voice subject, or widening of the responsible set (e.g. adding Haganah to Irgun/Lehi). Code the reverse (agent removed) with negative sign.

**Exclude.** Agents named elsewhere in A in the same paragraph; changes of the agent's name only (Israel to Zionists) unless the scope of responsibility changes (then code and note).

**Examples (verbatim).**

- *Nakba*  
  before: "is the ethnic cleansing of Palestinian Arabs by Israel through their violent displacement"  
  after: "is the ethnic cleansing of Palestinian Arabs by Zionists through their violent displacement"  
  edit summary: "more precise: [[Plan Dalet]], for example, was executed before the declaration of May 14"
- *Sabra and Shatila massacre*  
  before: "by a militia close to the Kataeb Party"  
  after: "by the Lebanese Forces, one of the main Christian militias in Lebanon, with the support of the Israel Defense Forces (IDF)."
- *Persecution of Uyghurs in China*  
  before: "the Chinese government has pursued a policy which has led to more than one million Muslims"  
  after: "the government of the People's Republic of China has committed a series of ongoing human rights abuses"

**Count (my reading).** Topic: 14 of 48 topic pairs. Comparison: 6 of 16 (Uyghurs, Armenian genocide, LTTE, Kashmir, Tigray, PKK). NOT distinctive in frequency; general preference for active voice in atrocity leads. Possible topic-specific feature: agent moved INTO the first sentence (Nakba, Sabra and Shatila, Gaza genocide) vs comparison Armenian genocide where the perpetrator moved OUT of the first sentence 'per FAC'.

**Direction.** Makes responsibility for harms explicit, in topic articles mainly assigned to Israeli/Zionist forces.

**KPIs.**

- `agentive_harm_clauses` (per lead (share of harm predicates with explicit agent); automatable: yes with dependency parse; LLM spot-check). Parse harm verbs (killed, expelled, displaced, destroyed, massacred, starved...) and check for agent (by-phrase, active subject, possessive). Compare A/B; separately for first sentence.

### M8 Relocation (demotion/promotion within the lead)

**Definition.** A claim or label present in both versions changes its position: moved out of the first sentence or paragraph into a later one (demotion), or into it from later (promotion). Often accompanied by a change of attribution.

**Include.** Same proposition, different sentence index (at least one sentence, or across paragraph 1 boundary). Includes terrorist designations, illegality, agents, genocide claims.

**Exclude.** Position changes caused only by insertion or deletion of unrelated sentences before it (compute relative rank, not raw index).

**Examples (verbatim).**

- *Israeli settlement*  
  before: "built in violation of international law on lands occupied by Israel in the 1967 Six-Day War."  
  after: "The international community considers Israeli settlements to be illegal under international law, but Israel disputes this."
- *1948 Palestinian expulsion and flight*  
  before: "were expelled or fled from their homes, at first by Zionist paramilitaries, and after the establishment of Israel, by its military."  
  after: "were expelled or fled from their homes."  
  edit summary: "Undid revision [[Special:Diff/1292987917|1292987917]] by [[Special:Contributions/IOHANNVSVERVS|IOHANNVSVERVS]] ([[User talk:IOHANNVSVERVS|talk]]) that the Palestinians "fled from their homes, at first by Zionist paramilitaries..." is not a coherent part of a sentence."
- *Al-Shabaab (militant group)*  
  before: "is a terrorist, jihadist fundamentalist group based in East Africa."  
  after: "is a transnational Wahhabi-Salafi Jihadist militant organization."

**Count (my reading).** Topic: 10 of 48 topic pairs. Comparison: 5 of 16 (Al-Shabaab, Islamic State, Armenian genocide, Al-Qaeda, Tibet). General Wikipedia style (labels and designations leave the first sentence); NOT a topic finding as such.

**Direction.** Demotion moves labels and agents out of the definitional sentence (in topic: Hamas terrorist designations, settlement illegality, 1948 agent); promotion moves claims into it (Gaza war, October 7 attacks, Sabra and Shatila).

**KPIs.**

- `relative_position_shift` (per proposition per pair; automatable: yes for term-based propositions). Locate proposition (term list or LLM alignment) in A and B; relative rank = sentence index / number of sentences; report shift and whether it crosses the first-sentence and first-paragraph boundaries.
- `protected_opening_gap` (per pair; automatable: yes (current values: substantial leads, topic 31% vs comparison 39% have gap < -0.2)). 1 - similarity(first sentence A,B) minus 1 - similarity(rest of lead A,B). Negative = opening kept stable while the rest changed.

### M9 Policy-and-procedure justification (process move, needs edit summaries)

**Definition.** The edit summary justifies a first-sentence change by citing a content policy (NPOV/neutral, RS, OR, weight), a style rule (MOS:FIRST, MOS:AVOIDBOLD, LEADCLUTTER, MOS:OPEN), a forum outcome (per talk, per RM, per FAC, RfC), a precedent in another article ('compare The Holocaust', 'per formatting on pages for Jordan, Lebanon'), source counting ('many reliable sources', 'roughly equal weight in sources'), an omission claim ('fails to be mentioned', 'omission is ridiculous'), or a procedural complaint ('removed without discussion').

**Include.** Any first-sentence edit whose summary contains one of these justification types. Code type(s) and the direction of the substantive change (A: adds critical term/agent/Palestinian context or removes attribution; B: adds attribution/removes agent or critical term/adds Jewish-tradition anchoring; T: toponym/naming; N: none).

**Exclude.** Bot and template maintenance (AWB, Monkbot), typo fixes. Code summaries that are empty or say 'ce'/'clarify' on a substantive change separately as LABEL MISMATCH.

**Examples (verbatim).**

- *History of Israel*  
  before: "is the birthplace of the Jewish people, the place where the final form of the Hebrew Bible is thought to have been compiled"  
  after: "is a region that has come under the sway of various empires"  
  edit summary: "/* top */ copyediting lead into better NPOV language and removing unnecessary citation, per [[WP:LEADCITE]]"
- *Hamas*  
  before: "is a Palestinian Sunni Islamist political and military movement governing parts of the Israeli-occupied Gaza Strip since 2007."  
  after: "is a Palestinian Sunni Islamist resistance movement governing parts of the Israeli-occupied Gaza Strip since 2007."  
  edit summary: "[[NPOV]] many relaible sources has described it as resistance movement which is less biased and more neutral. this is how the group identifies itself"
- *Zionism as settler colonialism*  
  before: "Zionism has been described by its founders and early leaders, as well as by many scholars, as a form of settler colonialism"  
  after: "Zionism has been described by some scholars as a form of settler colonialism"  
  edit summary: "more NPOV"
- *Zionism*  
  before: "Zionism is an ethnocultural nationalist movement that emerged in late 19th-century Europe to establish and support a Jewish homeland through colonization in the region of Palestine"  
  after: "Zionism is an ethnic nationalist movement that emerged in late 19th-century Europe to establish and support a Jewish homeland through colonization in the region of Palestine"

**Count (my reading).** Topic: Trace data, 17 topic articles, 147 traced first-sentence edits: explicit neutrality appeal in 5 edits used for opposite directions (A 2, B 1, removal of Jewish-tradition anchor 1, toponym 1); talk/forum reference 15 (10%); MOS/style code 10; source-based argument 16; 'RfC' 0; empty summary 24 (16%); substantive change (word similarity < 0.8) under empty or light summary 16 (11%); anticipatory hedging ('I hope this isn't contentious') 7.. Comparison: Trace data, 7 comparison articles, 51 edits: talk/forum 2 (4%), MOS/style 4, source-based 2, neutrality appeal 0-1, RfC 0, empty 10 (20%), substantive under light summary 2 (4%), hedging 1. Contrast is thin (7 articles, 2 with only 1-2 edits).

**Direction.** Neutrality is invoked for changes in both directions (policy as rhetoric). Style rules (MOS:OPEN, LEADCLUTTER, MOS:FIRST, AVOIDBOLD) accompany removals of Jewish-tradition glosses and block bold naming; source-count arguments accompany insertions of critical terms; procedural complaints ('removed without discussion') accompany attempts to restore earlier wording and were all reverted.

**KPIs.**

- `justification_repertoire_shares` (per traced first-sentence edit; automatable: mostly (regex), LLM for ambiguous). Code each edit summary into types: content-policy, style-MOS, forum (talk/RM/RfC/FAC), precedent, source-count, omission, procedural complaint, accuracy/clarity, copyedit, empty, bot. Regex first pass (see scripts/trace_stats.py), LLM second pass for multi-type summaries.
- `justification_by_direction` (cross-tab of edits (type x direction); automatable: no (direction needs LLM)). Pair the summary type with the LLM-coded direction of the before/after change (A/B/T/N); report shares and survival (reverted flag; after==snapshot_after in bisect.json).
- `label_mismatch_rate` (per edit; automatable: yes). Summary empty or matches copyedit/clarify/minor/tweak AND word-level similarity of before/after first sentence < 0.8 OR a contested term enters/leaves.
- `forum_reference_rate` (per edit and per article-year; automatable: yes). Regex per talk|talk page|discussion|consensus|RfC|RM|FAC in summary.

### M10 Trajectory type: ratchet, oscillation, return-to-minimum (process move, needs revision sequence)

**Definition.** The sequence of first-sentence versions for one contested element follows one of: RATCHET (monotone steps in one direction, no traced reversal, e.g. attribution ladder climbs); OSCILLATION (two or more variants alternate at least twice); RETURN-TO-MINIMUM (after elaborations the sentence returns to its shortest earlier form); BOLD-STICK (one change, then no further change for at least 12 months); RELOCATION-SETTLEMENT (the element leaves the first sentence but stays in the lead).

**Include.** Contested elements with at least two traced changes, or one traced change plus a gap showing an untraced change (before of edit k+1 differs from after of edit k).

**Exclude.** Elements touched only by copyedits; single-edit elements unless BOLD-STICK applies.

**Examples (verbatim).**

- *Gaza genocide*  
  before: "Experts, governments, United Nations agencies, and non-governmental organisations have accused Israel of carrying out a genocide"  
  after: "state that Israel has committed genocidal acts against the Palestinian people"  
  edit summary: ""state" is more neutral than "accuse""
- *Israel*  
  before: "Israel, officially the State of Israel, is a country in the Southern Levant region of West Asia."  
  after: "Israel, officially the State of Israel, is a country in Western Asia."  
  edit summary: "minor tweak"
- *Anti-Zionism*  
  before: "Anti-Zionism is opposition to Zionism."  
  after: "Anti-Zionism views Zionism as a colonialist, racist or exceptionalist ideology or movement."  
  edit summary: "/* top */ Material and refs copied from [[Zionism]] article lead to replace unreliable definition from MW"
- *Islamic State*  
  before: "is a transnational Salafi jihadist group and a former unrecognised quasi-state."  
  after: "is a transnational Salafi jihadist group and a unrecognised quasi-state."  
  edit summary: "as pointed out below, and can be read in the ISWAP article, IS still operates as quasi-state in its African territories"

**Count (my reading).** Topic: Of 36 contested elements catalogued in the 17 topic traces (contested_claims.csv): ratchet 5, oscillation 13 (5 of them finally anchored by a talk outcome, page title, style rule or cross-article precedent), bold-stick 12, relocation-settlement 4, return-to-minimum/start 2; 7 elements still changed in the last 6 months of the window.. Comparison: Of 7 contested elements in the 7 comparison traces: oscillation 4, relocation 2, short-lived insertion 1; no ratchet observed. Thin: 2 of the 7 comparison articles have only 1-2 traced edits.

**Direction.** Ratchets in the trace sample all move toward stronger characterisation of Israeli/Zionist conduct or away from Jewish-tradition anchoring; oscillations concern labels that have no dominant source usage (geography, adjective choice, name order).

**KPIs.**

- `monotonicity_index` (per contested element; automatable: yes once variants are coded (ratchet.py fs_timeline gives variant ids)). Order versions; assign ladder level (M1) or variant id; index = |sum of signed steps| / sum of |steps| (1 = ratchet, ~0 = oscillation).
- `time_to_stabilise` (days per contested element; automatable: yes from ratchet.json). From first traced insertion to start of the final run that lasts >= 180 days or is censored at window end (ratchet.py events: survived, censored).
- `hidden_change_rate` (per article; automatable: yes). Share of consecutive traced edits where before(k+1) != after(k); lower bound on untraced first-sentence churn (discovery: topic 66%, comparison 64%).

## 7. Process KPIs that need only lead pairs or existing revision metadata

The fields available are listed in `trace_changes.py` (bisect.json: revid, parentid, timestamp, comment ≤300 chars, tags, size_delta, reverted = mw-reverted, before, after, snapshot_after, salted editor hash) and in `ratchet.py` (ratchet.json: every section-0 revision since 2021 with ts, salted user hash, reverted, reverting = mw-undo/rollback/manual-revert, lead word count, presence of CRITICAL/CONNECTION frames plus terrorism and militant, first sentence ≤400 chars; derived: term insert/remove events with survival and censoring, failed attempts before a term stuck, attempt editors, first-sentence variants with live days and re-entries, fs timeline, big rewrites with reverted flag).

**From lead pairs only** (automatable; script `scripts/leadpair_kpis.py`; values for discovery leads ≥1500 chars, topic n=79 vs comparison n=36):
- `protected_opening_gap`: first-sentence change minus rest-of-lead change; share with gap < −0.2 is 31% vs 39%.
- `fs_tense_flip` (was/is in sentence 1): 20% vs 14%.
- `camp_label_new`: 7.6% vs 0%.
- `genocide/ethnic-cleansing/apartheid new in lead`: 11.4% vs 5.6%.
- `alt_names_in_first_sentence` up/down: 14%/10% vs 14%/6%.
- `attribution_marker_density` up/down: 14%/44% vs 22%/44%.
- `denial_word_density_up`: 10% vs 22%. The regex is noisy and does not reproduce my reading, so this needs an LLM.
- `colonial_vocab_new`: 4% vs 8%. The regex is not distinctive; only position (definitional sentence) is.
- Lead length ratio: 1.01 vs 1.11.

Composition warning: across all 237 discovery pairs, most regex proxies do not separate the groups. The comparison set is 42 large, salient articles, while the topic set contains many stubs. Compare like with like (stratify by lead length or salience).

**From bisect.json (trace_changes metadata):**
- `hidden_change_rate`: share of consecutive traced edits with before(k+1) ≠ after(k). Discovery: 66% vs 64%.
- `quarter_survival`: after == snapshot_after, i.e. whether the first change of the quarter survived to the quarter end.
- `article_quarter_change_rate` before/after 2023-10: topic 32% to 45%, comparison 38% to 36%.
- `revert_tag_rate` from mw-reverted plus reverting tags.
- `summary_repertoire_shares` and `label_mismatch_rate` (M9).
- `bundling_share`: |size_delta| > 1000 bytes. Discovery: 7.5% vs 4%.
- `editor_concentration`: distinct editor hashes per article and per contested element; top-editor share.
- `same_hand_cross_article`: same editor hash changing first sentences of two articles within 7 days.

**From ratchet.json (full lead history):**
- `fs_n_variants` and `variant_reentries` (variants with entries > 1 = recurring contested wording).
- `modal_variant_dominance` (share of live days in the modal first sentence).
- `lead_revert_rate`, `reverting_share`.
- `insert_survival_30d`, `remove_survival_30d` and `asymmetry_30d` per frame.
- `failed_attempts_before_stick`; `attempt_editors` (one persistent hand vs many).
- `big_rewrite_reverted_share` (bundles reverted?).
- `time_to_stabilise` (first insertion to start of final run of ≥180 days, or censored).
- `monotonicity_index` from fs_timeline once variants are coded on the M1 ladder.

Gaps to fix before freezing:
- ratchet.py tracks term **presence** only, so it cannot see M1 (attribution level), M7 (agent) or M8 (position). The Gaza genocide ladder is invisible to it because "genocide" is present throughout.
- The settler_colonial regex in analyze.py does not match "colonies" (Israeli settlement), because `coloni[sz]` requires s/z after "coloni".
- Add per-revision features: sentence index of each frame term, attribution marker in the clause, and agent presence for harm verbs.

## 8. Expected but not found

- No RfC, "per RfC" or "restore consensus" in any of the 198 traced summaries. WP:DUE/UNDUE is never cited, WP:RS once, WP:OR once, bracketed NPOV once. Settlement runs through talk-page mentions, page titles (RM), style rules and precedent, not through cited RfC closures.
- Few visible edit wars: 7 reverted traced edits in topic. Thinning hides most of the cycling.
- No fight over "terrorist" in Hamas's first sentence is traced. The designations moved silently from paragraph 1 to the last paragraph, and "militant" left in an untraced interval.
- The Oct 2023 shock did not produce large first-sentence rewrites in that month; traced Oct 2023 edits are mostly small. The frame changes come later, through 2024–2025, and largely in untraced edits.
- Jewish-history articles (Jews, Land of Israel, Balfour) are not battlegrounds at first-sentence level.

## 9. Surprises

- Style policy (MOS:FIRST, AVOIDBOLD, LEADCLUTTER, MOS:OPEN) does substantive framing work: removing the Eretz Yisrael gloss, redefining History of Israel, blocking a bold war name, flipping the October 7 attacks name formula.
- Neutrality appeals point in opposite directions.
- The Gaza genocide status moved by small monotone steps with no traced revert.
- Cross-article coordination of vocabulary ("Southern Levant" in Israel, Jerusalem and Palestine; "compare The Holocaust").
- Page titles act as anchors: the RM outcome fixes word order in the first sentence.
- The direction of M1 is not fixed by subject. Bar Kokhba moves a Roman-intent claim about the Jews into wikivoice.
- Gaza Strip famine moves the other way from most topic pairs: Israeli denials are removed from the lead and Palestinian-side causes are added ("looting").

Files: `codebook.json`, `contested_claims.csv`, `leadpair_kpis_discovery.json`, `scripts/trace_stats.py`, `scripts/leadpair_kpis.py`, `scripts/check_quotes.py` (verifies that every quotation in codebook.json is verbatim in the data: 0 missing), `scripts/make_codebook.py`.
