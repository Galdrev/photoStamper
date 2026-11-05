# Study 3, Part C: frozen codebook of qualitative content KPIs

Version `study3-partC-v1.0-frozen-2026-11-05`. Frozen 2026-11-05, before any holdout coding. Machine-readable twin: `codebook.json` (the KPI blocks below are rendered from it). Coder prompt: `coder_instructions.md`. Code: `auto_kpis.py`, `make_batches.py`, `analyze_codes.py`.

## 1. What this is

Three close readers coded the DISCOVERY half of the lead pairs (`data/study3/qual_discovery.json`: 190 topic pairs, 42 control and 5 control_contaminated comparison pairs), each through a different lens: discourse and voice (`qual_voice/`), historiography and story grammar (`qual_history/`), and editorial process (`qual_process/`). This codebook merges their moves into 12 KPIs. It will be applied ONCE to the sealed holdout half (`data/study3/qual_holdout.json`) by two independent LLM coders, plus the automatic measures in `auto_kpis.py`. Nothing in it was checked against holdout material.

The question for every KPI is the same: **in what share of lead pairs does the move occur in topic articles, compared with comparison articles?** A move that comparison articles show just as often is general Wikipedia style, not a topic finding. Codes describe what the 2026 text states as its baseline relative to the 2021 text. They make no claim about truth or bias. Direction is coded per claim and per party, never per article.

## 2. How the readers' moves were merged

Rule 1: moves found independently by two or three readers get priority. Rule 2: a single-reader move stays only if its topic vs comparison contrast was large and its definition is crisp. Rule 3: moves that every reader called general Wikipedia style are dropped as KPIs and kept as style controls, measured in both groups. Rule 4: where the discovery data could test a definition automatically, it was calibrated on discovery. That calibration moved one KPI between families (K06, see below).

| KPI | merged from | readers | readers' counts (topic vs comparison, pairs read) | family |
|---|---|---|---|---|
| K01 voice_upgrade | Epistemic upgrade / wikivoice (attribution ladder) | 3 | voice: 8/85 topic (3 reverse) vs 0/37 comparison (legal/atrocity categories); consensus quantifier 11/85 vs 3/37; history: hardening 10/71 (softening 4) vs 4/20 (softening 2); process: 16/48 vs 3/16 | primary |
| K02 story_onset | Story start / causal re-anchoring | 3 | voice: ~14/85 vs ~3/37; history: 11/71 vs 3/20 (sub-type 'origin moved to a single originating agent' 7/71 vs 0/20); process: 11/48 vs 4/16 (process: not distinctive by rate) | primary |
| K03 name_primacy | Naming / place-name primacy | 3 | voice: ~11/85 vs 0/37 (macro-region-only edits excluded: ~5 topic, ~3 comparison); history: 12/71 vs 2/20; process: 15/48 vs 4/16 (process count includes macro-region labels) | primary |
| K04 definitional_class | Colonial (or atrocity / legal-violation) wording in the definitional slot | 3 | voice: change INTO colonial/atrocity/ethnic-nationalist class 6/85 vs 1/37 (any genus change 24% vs 24% = style); history: colonial in first sentence 3/71 vs 0/20; any colon* gain 8/71 vs 4/20 (not distinctive); process: 8/48 vs 2/16 by rate (not distinctive); the definitional location is what differs; auto K04a (colonial only, first sentence, discovery): 3/166 topic vs 1/46 comparison | primary |
| K05 actor_relabel | Zionist relabelling (actor label moves to an ideological category) | 2 | voice: ~8/85 toward 'Zionist' (+1 reverse) vs 0/37; history: 'Zionist(s)' as agent gained in 11 topic leads (regex); pre-state relabels within 12/71; auto proxy SUP_zionist_actor_gain (discovery): 14/166 topic vs 0/46 comparison (lexicon is topic-specific by construction) | primary |
| K09 camp_label | Camp labels for actors and sources | 1 | process: 8/48 vs 0-1/16; regex 7.6% vs 0% of substantial leads; auto K09_gain (discovery, frozen regex): 10/166 topic (6.0%) vs 0/46 comparison | primary |
| K06 presupposed_eval_np | Evaluative / legal category presupposed in a noun phrase | 1 | voice: ~12/85 vs ~1/37 with a topic-specific lexicon (regex 12/190 up vs 0/47); auto K06_gain (discovery, frozen GROUP-NEUTRAL lexicon): 19/166 topic (11.4%) vs 4/46 comparison (8.7%) | secondary |
| K07 harm_agent | Agent surfacing / backgrounding in harm clauses | 3 | voice: ~12/85 surfacing (4 backgrounding) vs ~5/37; history: 11/71 vs 4/20; process: 14/48 vs 6/16 | secondary |
| K08 party_denial | Record-the-denial / rebuttal tail | 2 | process: 11/48 vs 1/16 (regex does not reproduce it); voice: ~7/85 vs ~3/37; regex 9/190 vs 11/47 (voice: general style; who denies differs) | secondary |
| K10 refusal_recontextualised | Rejection recontextualised | 1 | history: 9/71 vs 0/20 (deleted 4, motive added 1, kept after a prior cause 3, newly added as trigger 2) | secondary |
| K11 belonging_claims | Belonging claims: continuity split and demography as belonging | 1 | history: continuity removed/attributed 6/71, strengthened 7/71 vs 3/20 analogues; demographic anchor 9/71 vs 2/20; auto proxy SUP_majority_gain (discovery): 12/166 vs 3/46 | secondary |
| K12 suffering_motive_slot | Suffering slotting (harm as motive) | 1 | history: harm added in motive slot 7/71 vs 0/20; consequence slot 11/71 vs 5/20 (not distinctive) | secondary |

Decisions that needed judgement:
- **K01 merges** voice M1 (legal/atrocity voice promotion), voice M2 (consensus quantifiers), history M6 and process M1 into one attribution ladder. The voice reader's 'many vs some' quantifiers are rungs 4 vs 2. Two of the three readers excluded claims that are new in B with no counterpart in A. The ladder code follows them. New narrator-voice claims are recorded as instances (0 to 5) for a secondary readout only.
- **K04 broadened.** 'Colonial wording in the definitional slot' is triangulated (all three readers), but the automatic version (colonial terms only, first sentence, narrator voice) fires in only 3/166 topic and 1/46 comparison discovery pairs. The voice reader's genus-destination finding (into a colonial, atrocity or ethnic-nationalist class: 6/85 vs 1/37) is the same slot. So K04 is coded by the LLM over four destination classes (colonial, atrocity, legal violation, apartheid/racism). The colonial-only regex K04a is kept as a validity check. 'Ethnic nationalist' is left out: it is a nationalism subtype, and the same edit histories show it oscillating.
- **K05 generalised.** 'Zionist relabelling' is coded as a move of any collective actor's label into an ideological category (Zionists, Islamists, jihadists ...), so comparison articles can show it too.
- **K06 demoted to secondary.** The voice reader's presupposition contrast (about 12/85 vs 1/37) rested on a topic-specific lexicon ('Israeli-occupied', 'occupied Palestinian', 'Gaza genocide'). Rewritten as group-neutral patterns ('<Name>-occupied', 'forced <removal noun>', '<Name> genocide'), the frozen regex gives 19/166 (11.4%) vs 4/46 (8.7%) on discovery, only +2.7 pp. Comparison conflict articles do the same thing (Uyghurs 'forced labor', Kashmir 'unlawful detentions', Egypt 'the occupied Sinai').
- **K09 promoted to primary** although only one reader found it. The contrast is large and survives a group-neutral regex (pro-X / anti-X + actor noun / 'and its supporters'): 10/166 (6.0%) vs 0/46 on discovery. The definition is mechanical.
- **K07 (agent surfacing) is secondary although all three readers found it.** All three said comparison atrocity articles surface agents at a similar rate. What differs is WHICH party, and the party breakdown is descriptive.
- **K08 (record-the-denial) is secondary.** The process reader found 11/48 vs 1/16 by reading. The voice reader found the same construction at similar rates by regex and called it general NPOV style.
- **K11 merges** history M4 (continuity split) and M5 (demography as belonging) into 'belonging claims', with a type field. Its primary indicator is 'any change', because the meaning lies in which party's tie is strengthened or weakened.

## 3. Coding set, unit and masking

- **Coding set:** topic pairs (group == treatment) with change > 0.05, plus all comparison pairs (control, control_contaminated); pairs flagged parse_artefact by auto_kpis are excluded. On discovery this is 212 pairs (166 topic, 46 comparison). The Islam pair is excluded because its 2026 lead is a navbox.
- **Unit:** the lead pair (K04 and SC1: the first sentence of each version). Every KPI yields one categorical code per pair and coder, plus instances (party, direction) for the breakdown.
- **What the coder sees:** cleaned lead texts as Version A and Version B in random order (independent per coder), plus an unordered list of other first-sentence variants from traced edits (text only), where available.
- **What the coder does not see:** title, group label, dates, edit summaries, timestamps, revert flags, which version is older. The order key lives in `KEY_DO_NOT_SHARE.json`, which only `analyze_codes.py` reads.
- **Honest limits of masking:**
  - The content usually reveals the subject, and so whether it is a topic article; masking guards against knowing the group label and the before/after direction, not the subject.
  - Party codes name Jewish/Israeli and Palestinian/Arab parties explicitly, so the coder knows what the study is about.
  - First-sentence variants exist for 17 topic and 7 comparison discovery articles, mostly heavily edited ones; their presence weakly signals salience.
- **Orientation:** coders always code 'B relative to A'. `analyze_codes.py` flips codes, instance directions and paired fields (level_A/level_B, from_cat/to_cat, onset years) back to OLD->NEW using the key. The fake-data test confirms the flip (planted 60%/10% recovered as 58%/7.5%; 0 orientation mismatches).

## 4. Length-matching rule (frozen)

Topic includes many stubs, while comparison articles are large (discovery median lead0: 178 words topic vs 413 comparison). Every KPI is therefore reported per lead pair AND within lead-length strata. The strata are terciles of word count of clean_lead(lead0) (auto_kpis.words). Cut points are fixed from discovery: **T1 <= 158 words, T2 = 159-340, T3 >= 341** (exact terciles (158.3, 340.7) of the discovery coding set before the artefact exclusion (n = 213), rounded down). Discovery cells: topic {'T1': 64, 'T2': 59, 'T3': 43}, comparison {'T1': 7, 'T2': 12, 'T3': 27}. The same cut points are applied unchanged to holdout, so holdout terciles will not be exactly equal in size. Pooled across strata, the length-adjusted estimate is the Mantel-Haenszel risk difference (weights n_t·n_c/(n_t+n_c)). A stratum with no pairs in one group gets weight 0.

## 5. KPI families and decision rule (frozen)

- **Primary family (BH):** K01 voice_upgrade, K02 story_onset, K03 name_primacy, K04 definitional_class, K05 actor_relabel, K09 camp_label.
- **Secondary family (BH separately, exploratory):** K06 presupposed_eval_np, K07 harm_agent, K08 party_denial, K10 refusal_recontextualised, K11 belonging_claims, K12 suffering_motive_slot.
- **Style controls (reported for both groups, never tested):** SC1 genus change (LLM) and the auto fields in `auto_kpis.style_controls` (length ratio, first-sentence vs rest change, protected opening, was/is flip, attribution-marker density, terror* leaving or entering sentence 1, naming formulas in sentence 1).
- **Pair score:** LLM KPI: mean of the two coders' binary primary indicators (0, 0.5, 1) after orientation is restored and non-verbatim evidence is voided; auto KPI: its 0/1 field.
- **Estimate:** Delta = mean pair score in topic minus mean pair score in comparison.
- **CI:** 95% percentile bootstrap, 10,000 resamples of pairs within group, seed 20261105.
- **p:** two-sided permutation p, 10,000 label permutations, seed 20261105 (used instead of a CI-derived p because several comparison cells are 0, which makes bootstrap p degenerate).
- **Multiplicity:** Benjamini-Hochberg at q = 0.10 across the 6 primaries (family fixed regardless of reliability); separately across the 6 secondaries (exploratory).
- **Length:** Mantel-Haenszel risk difference across the 3 lead0 terciles, weights n_t*n_c/(n_t+n_c); 95% CI by bootstrap within group x tercile; p by permuting group labels within tercile.
- **Verdict per KPI:**
  - `unreliable`: LLM KPI with Cohen's kappa (binary primary indicator) < 0.6, or no variance: reported, not interpreted.
  - `supported`: reliable AND BH-adjusted q <= 0.10 AND Delta > 0 AND MH risk difference > 0 with stratified permutation p <= 0.10.
  - `length_sensitive`: BH-significant with Delta > 0 but the MH condition fails.
  - `reverse`: BH-significant with Delta < 0.
  - `not_supported`: otherwise.
- **Pre-specified sensitivity analyses** (reported; they do not change verdicts): coder combination AND (both positive) and OR (either positive); comparison without control_contaminated; comparison restricted to change > 0.05 (same filter as topic); lead0 dated 2021 only (d0 starts '2021'); excluding pairs either coder marked usable = false.
- **Direction breakdown:** for every KPI, share of pairs with each (party, dir) instance, by group; descriptive, no tests. This is where 'which party' is answered. For example, K01 instances are tabulated by the target party of the upgraded claim, and K03 by the community whose name is promoted or demoted.

## 6. Reliability

- two independent LLM coding sessions, no shared context, same prompt (coder_instructions.md), independent A/B orientation and item order.
- Cohen's kappa per KPI on the binary primary indicator (threshold 0.6) and on the full categorical code (reported); raw agreement, PABAK and prevalence reported. A KPI with kappa < 0.6 is reported as **unreliable** and not interpreted. The BH family stays fixed, so an unreliable primary still uses one of the six slots. This prevents choosing the family after seeing the data.
- Evidence: a positive code whose evidence is not a verbatim substring of the cited version is set to none for that coder; if more than 15% of a coder's positive codes fail, that coder is re-run once in a fresh session and both runs are reported.
- Auto KPIs: deterministic; validity checks: K04a vs LLM K04 colonial subset (kappa), K09 span precision audit.
- Kappa is unstable at low prevalence (the kappa paradox). PABAK and raw agreement are reported next to it, but the 0.6 rule uses kappa.

## 7. The KPIs

### K01 `voice_upgrade` (primary; LLM-coded)

**Move.** Epistemic upgrade / wikivoice (attribution ladder). Merged from: voice:M1 Voice promotion of legal/atrocity categories, voice:M2 Consensus quantification of sources, history:M6 Voice hardening of contested labels, process:M1 Epistemic upgrade.

**Question.** Does a contested characterisation that appears in both versions sit on a different rung of the attribution ladder in B than in A?

**Unit.** lead pair (instances: one per aligned characterisation).

**Ladder.** 0 = absent (only for the secondary readout of new claims); 1 = alleged / accused / claimed, or presented as a disputed allegation ('allegations have been made', 'has been accused of'); 2 = attributed to an unquantified minority, to 'some', to critics, or to one party ('some historians', 'critics call', 'Palestinians describe'); 3 = attributed to named authorities or institutions ('according to the UN', 'the ICJ found', 'the international community considers'); 4 = majority or consensus attribution ('many scholars', 'most experts', 'scholars widely', 'academic consensus'); 5 = narrator voice: main-clause assertion with no attribution, or part of the definitional predicate.

**Coding rule.** List each contested characterisation (an evaluative, legal or atrocity category, or an intent/historicity claim) applied to the same target in BOTH versions. Assign its ladder rung in A and in B. Code B_more_narrator if at least one characterisation is on a higher rung in B and none lower; B_less_narrator if at least one is lower and none higher; both if each occurs; none otherwise.

**Include.** Categories: genocide, ethnic cleansing, apartheid, illegal/unlawful/violation of international law, war crimes, crimes against humanity, terrorism/terrorist, massacre, colonial/settler-colonial, racism, antisemitism, propaganda; historicity claims (whether X existed or happened); intent claims ('intended to', 'aimed at'). Same category and same target in both versions, rungs differ by at least one step. Upgrades and downgrades, for any target, in either group.

**Exclude.** Rewording on the same rung ('accused' to 'charged'); swapping one named authority for another (3 to 3). A characterisation present in only one version (record it as an instance with level 0 on the absent side; it does NOT set the code). Casualty numbers, dates and other descriptive facts. Words inside a quotation of a named person when the quotation is the only carrier.

**Answer format.** Code: `none`, `B_more_narrator`, `B_less_narrator`, `both`. Primary binary indicator (OLD->NEW orientation): code in {`B_more_narrator`, `both`}. Instance fields: `party` (target of the characterisation); `dir` (B_more_narrator | B_less_narrator | new_in_B | dropped_in_B); `category` (short label, e.g. 'ethnic cleansing'); `level_A` (0-5); `level_B` (0-5). Evidence: one verbatim quote per positive code.

**Direction scheme (descriptive).** `B_more_narrator`: moves a characterisation of [party]'s conduct or nature from attributed/hedged toward narrator voice / `B_less_narrator`: moves a characterisation of [party]'s conduct or nature from narrator voice toward attributed/hedged.

**Discovery anchors (verbatim; before = lead0, after = lead1 of `qual_discovery.json`, checked by script).**

- *1948 Palestinian expulsion and flight* [topic] -> `B_more_narrator`, party JEWISH_ISRAELI (rung 2 -> 4)  
  before: "described by some historians as ethnic cleansing, while others dispute this charge"  
  after: "Scholars widely describe the event as ethnic cleansing, although some disagree."
- *Legality of Israeli settlements* [topic] -> `B_more_narrator`, party JEWISH_ISRAELI (rung 3 -> 5)  
  before: "The international community considers the establishment of Israeli settlements in the Israeli-occupied territories illegal"  
  after: "are illegal under international law."
- *Israeli settlement* [topic] -> `B_less_narrator`, party JEWISH_ISRAELI (reverse: rung 5 -> 3)  
  before: "built in violation of international law on lands occupied by Israel"  
  after: "The international community considers Israeli settlements to be illegal under international law, but Israel disputes this."
- *Kingdom of Israel (united monarchy)* [topic] -> `B_less_narrator`, party JEWISH_ISRAELI (historicity: a sceptical consensus (rung 4, 'generally held') becomes an open debate (rung 2))  
  before: "generally held to be a literary construction and not a historical reality"  
  after: "is a matter of ongoing academic debate."

**Automatable.** no (LLM). Auto style control SC_attr_density_up/down is a crude proxy and is not a substitute.

### K02 `story_onset` (primary; LLM-coded)

**Move.** Story start / causal re-anchoring. Merged from: voice:M9 Narrative onset and first-paragraph primacy, history:M1 Causal re-anchoring, process:M6 Causal-context insertion.

**Question.** Does B start the causal story of the subject earlier than A, or add an earlier prior cause or precondition, compared with A?

**Unit.** lead pair.

**Coding rule.** In each version find the earliest event or condition that the lead presents as the origin, cause or precondition of the subject (cues: 'has its origins in', 'began', 'dates (back) to', 'rooted in', 'marked the start', 'arose from', 'after', 'following', 'in response to', 'as a reaction to', or a premodifier that encodes a precondition at the start of the event, e.g. 'from the blockaded Gaza Strip'). B_earlier: B's earliest stated cause is earlier in time than A's, or B adds a prior cause or precondition before the event A presented as the start. B_later: B removes the earlier origin or prior cause, or starts the causal story later. both: one chain moves earlier and another later.

**Include.** Explicit causal or origin connectors, and precondition premodifiers attached to the starting event. A prior cause that is an action of any party, or a condition (e.g. a constitution, a coup, a blockade).

**Exclude.** Chronology without a causal link (founding dates, lists of later wars, updates to recent events). Background about the subject itself that is not presented as a cause. Consequences (what followed). The same origin with the same anchor in both versions, even if reworded.

**Answer format.** Code: `none`, `B_earlier`, `B_later`, `both`. Primary binary indicator (OLD->NEW orientation): code in {`B_earlier`, `both`}. Instance fields: `party` (party whose action (or condition it imposed) is the added/removed earliest cause; UNCLEAR if a condition with no actor); `dir` (B_adds_prior_cause | B_removes_prior_cause); `onset_year_A` (int or null); `onset_year_B` (int or null). Evidence: one verbatim quote per positive code.

**Direction scheme (descriptive).** `B_earlier`: moves the start of the causal story earlier, to an action or condition of [party] / `B_later`: moves the start of the causal story later / removes [party]'s earlier action as a cause.

**Discovery anchors (verbatim; before = lead0, after = lead1 of `qual_discovery.json`, checked by script).**

- *Israeli–Palestinian conflict* [topic] -> `B_earlier`, party JEWISH_ISRAELI (mid-20th century -> late 19th century)  
  before: "that began in the mid-20th century"  
  after: "The conflict has its origins in the rise of Zionism in the late 19th century in Europe"
- *Blockade of the Gaza Strip* [topic] -> `B_earlier`, party JEWISH_ISRAELI (2007 after Hamas takeover -> early 1990s)  
  before: "imposed by Israel and Egypt in 2007, after Hamas took control of the Gaza Strip"  
  after: "The restrictions on movement and goods in the Gaza Strip imposed by Israel date to the early 1990s."
- *Tigray war* [comparison] -> `B_earlier`, party MULTIPLE (comparison: prior hostilities added before the TPLF attack)  
  before: (no counterpart)  
  after: "After years of increased tensions and hostilities between the TPLF and the governments of Ethiopia and Eritrea, fighting began when TPLF forces attacked the Northern Command headquarters"

**Automatable.** no (LLM). Optional onset years are recorded for a secondary readout (median shift in years).

### K03 `name_primacy` (primary; LLM-coded)

**Move.** Naming / place-name primacy. Merged from: voice:M10 Primary-referent naming and co-name order, history:M9 Toponymic and temporal anachronism management, process:M5 Naming and toponym arbitration.

**Question.** Does B change which name is primary for the subject or for a place, territory or polity it mentions, or the status or order of alternative names associated with different communities?

**Unit.** lead pair (flag whether the change is in the first sentence).

**Coding rule.** Code changed when, for the SAME referent, B (a) uses a different name as head or primary name; (b) adds or removes an alternative name associated with another community, language or tradition; (c) reorders co-names or moves a name between primary status ('X or Y', bold co-name) and gloss status ('known to Muslims as Y', 'in Jewish tradition', '(roughly corresponding to Y)'); or (d) replaces the name used for an earlier period with another name for the same period (e.g. 'southern Syrian provinces' vs 'region of Palestine' vs 'Land of Israel').

**Include.** Head-noun toponym swaps, gloss added/removed, co-name order, period-name replacement; anywhere in the lead (most occur in paragraph 1).

**Exclude.** Transliteration, diacritics, script, pronunciation fixes. Macro-region labels for a present-day location (Middle East / West Asia / Western Asia / Levant / Southern Levant): general style, do NOT code. Administrative modifiers ('currently governed as part of X'). Labels for actors (code K05) and names inside quotations. A name that disappears only because the sentence about its referent was deleted entirely.

**Answer format.** Code: `none`, `changed`. Primary binary indicator (OLD->NEW orientation): code in {`changed`}. Instance fields: `party` (community whose name is promoted or demoted); `dir` (B_promotes | B_demotes); `in_first_sentence` (true | false). Evidence: one verbatim quote per positive code.

**Direction scheme (descriptive).** `B_promotes`: moves the name used by [party]'s tradition into primary position (head noun, first, or co-primary) / `B_demotes`: moves the name used by [party]'s tradition into a gloss, later position, or out of the lead.

**Discovery anchors (verbatim; before = lead0, after = lead1 of `qual_discovery.json`, checked by script).**

- *Temple Mount* [topic] -> `changed`, party PALESTINIAN_ARAB (B_promotes: Arabic name raised from gloss to co-primary)  
  before: "known to Muslims as the Haram esh-Sharif"  
  after: "The Temple Mount or al-Haram al-Sharif"
- *Zionism* [topic] -> `changed`, party JEWISH_ISRAELI (B_demotes Land of Israel from head to gloss; Palestine promoted)  
  before: "the historic Land of Israel (roughly corresponding to Canaan, the Holy Land, or the region of Palestine)"  
  after: "in the region of Palestine, which roughly corresponds to the Land of Israel in Judaism"
- *Western Wall* [topic] -> `changed`, party PALESTINIAN_ARAB (reverse direction: Arabic name removed from the first sentence)  
  before: "known in Islam as the Buraq Wall"  
  after: "is an ancient retaining wall of the built-up hill known to Jews and Christians as the Temple Mount of Jerusalem."
- *Jerusalem* [topic] -> `none` (EXCLUSION anchor: macro-region label only)  
  before: "is a city in the Middle East"  
  after: "is a city in the Southern Levant"

**Automatable.** no (LLM). Auto style controls SC_alt_names_fs_up/down count naming formulas only.

### K04 `definitional_class` (primary; LLM-coded)

**Move.** Colonial (or atrocity / legal-violation) wording in the definitional slot. Merged from: voice:M6 Definitional genus reclassification (destination class), history:M2 Colonial genus in the definition, history:M10 Genus re-classification (content of the swap), process:M4 Colonial-framework vocabulary in definitional position.

**Question.** Does the defining predicate of the first sentence gain (or lose) a colonial, atrocity, legal-violation or apartheid/racism category in narrator voice?

**Unit.** first sentence.

**Coding rule.** Take the defining predicate of the first sentence: the head noun phrase of 'X is/was a ...' (or 'X refers to', 'X was the ... of'), its modifiers, and its means or purpose adjunct ('through colonization'). B_gains: B's predicate contains a category from the four classes in narrator voice and A's does not (or has it only attributed). B_loses: the reverse. both: one class gained and another lost. Classes: colonial (colonization, colonies, colonial, settler-colonial); atrocity (genocide, ethnic cleansing, massacre, mass murder, mass expulsion, extermination); legal violation (illegal, unlawful, in violation of international law, war crimes); apartheid/racism (apartheid, racist, supremacist).

**Include.** Category in the defining predicate or its adjunct, stated without an attribution frame. Alternative names that carry the category ('also called Israeli colonies').

**Exclude.** Category inside an attribution frame within the first sentence ('has been described as a form of settler colonialism'). Category outside the first sentence (K01/K06 may apply). Same class in both versions (e.g. 'The Armenian genocide was the systematic destruction ...' in both). Changes into or out of militant/terrorist/nationalist/political classes: that is style control SC1, not K04. 'ethnic nationalist' and other nationalism subtypes.

**Answer format.** Code: `none`, `B_gains`, `B_loses`, `both`. Primary binary indicator (OLD->NEW orientation): code in {`B_gains`, `both`}. Instance fields: `party` (party whose conduct or nature the category characterises); `dir` (B_gains | B_loses); `class` (colonial | atrocity | legal_violation | apartheid_racism). Evidence: one verbatim quote per positive code.

**Direction scheme (descriptive).** `B_gains`: moves the definition of [party]'s project/act into a colonial / atrocity / legal-violation / apartheid class in narrator voice / `B_loses`: removes such a class from the definition of [party]'s project/act.

**Discovery anchors (verbatim; before = lead0, after = lead1 of `qual_discovery.json`, checked by script).**

- *Zionism* [topic] -> `B_gains`, party JEWISH_ISRAELI (class colonial (means adjunct))  
  before: "espouses the re-establishment of and support for a Jewish state in the territory defined as the historic Land of Israel"  
  after: "Zionism is an ethnic nationalist movement that emerged in late 19th-century Europe to establish and support a Jewish homeland through colonization in the region of Palestine"
- *Nakba* [topic] -> `B_gains`, party JEWISH_ISRAELI (class atrocity)  
  before: "was the destruction of Palestinian society and homeland in 1948"  
  after: "is the ethnic cleansing of Palestinian Arabs by Zionists"
- *Population exchange between Greece and Turkey* [comparison] -> `B_gains`, party OTHER_STATE (comparison: class atrocity (mass expulsion))  
  before: (no counterpart)  
  after: "was the mass expulsion of approximately 1,221,489 Greek Orthodox Christians"
- *Hamas* [topic] -> `none` (EXCLUSION anchor: militant -> political is SC1, not K04)  
  before: "is a Palestinian Sunni-Islamic fundamentalist but pragmatic, militant, and nationalist organization."  
  after: "is a Sunni Islamist Palestinian nationalist political organisation with a military wing known as the al-Qassam Brigades."

**Automatable.** partly. Auto sub-indicator K04a (auto_kpis.k04a_colonial_fs: colonial class only, regex + attribution-cue check) is reported next to the LLM code and their agreement is given as kappa(K04a, LLM colonial subset). The LLM code is the KPI.

### K05 `actor_relabel` (primary; LLM-coded)

**Move.** Zionist relabelling (actor label moves to an ideological category). Merged from: voice:M5 Ideological relabelling of actors, history:M9 (pre-1948 actor labels) and M3 (collective agent 'Zionists').

**Question.** Does B change the category of the label for a collective actor that is present in both versions, and in particular move it to an ideological label?

**Unit.** lead pair (instances: one per actor).

**Coding rule.** Label categories: E ethnoreligious or national people ('Jewish militias', 'the Jewish population', 'Arab forces', 'Turks'); S state ('Israel', 'IDF', 'Israeli forces', 'the Ottoman government'); I ideological or movement ('Zionists', 'Zionist militants', 'Islamists', 'jihadists', 'Kemalists'); O named organisation ('Irgun', 'Haganah', 'Hamas', 'the CUP'). For the same real-world actor in both versions: B_more_ideological if B uses I where A used E, S or O; B_less_ideological if the reverse; other_change if the category changes without involving I; both if I is gained for one actor and lost for another.

**Include.** The subject's own genus when it names a collective actor ('paramilitary organization of the Jewish population' -> 'Zionist paramilitary organization'). Actors in by-phrases, subjects and premodifiers.

**Exclude.** The ideology as an idea or its proper name ('Zionism', 'the Zionist movement', 'Islamism'). Self-designations in quotation. An actor mentioned in only one version (the scope of who did harm is K07). Same-category synonyms ('Israel' -> 'the IDF' is S -> S).

**Answer format.** Code: `none`, `B_more_ideological`, `B_less_ideological`, `both`, `other_change`. Primary binary indicator (OLD->NEW orientation): code in {`B_more_ideological`, `both`}. Instance fields: `party` (party of the relabelled actor); `dir` (B_more_ideological | B_less_ideological | other_change); `from_cat` (E|S|I|O); `to_cat` (E|S|I|O). Evidence: one verbatim quote per positive code.

**Direction scheme (descriptive).** `B_more_ideological`: relabels [party]'s actor from an ethnoreligious, state or organisation label to an ideological label / `B_less_ideological`: relabels [party]'s actor from an ideological label to an ethnoreligious, state or organisation label.

**Discovery anchors (verbatim; before = lead0, after = lead1 of `qual_discovery.json`, checked by script).**

- *Haganah* [topic] -> `B_more_ideological`, party JEWISH_ISRAELI (E -> I)  
  before: "was the main paramilitary organization of the Jewish population"  
  after: "main Zionist paramilitary organization"
- *Deir Yassin massacre* [topic] -> `B_more_ideological`, party JEWISH_ISRAELI (E -> I)  
  before: "than the Jewish militias had expected"  
  after: "The Zionist militants massacred Palestinian Arab villagers"
- *First Aliyah* [topic] -> `B_less_ideological`, party JEWISH_ISRAELI (reverse: I -> E)  
  before: "was a major wave of Zionist immigration (aliyah) to Ottoman Palestine"  
  after: "was a major wave of Jewish immigration (aliyah) to Ottoman Palestine"

**Automatable.** partly. Auto support proxy SUP_zionist_actor_gain counts 'Zionist(s) + actor noun'; it is topic-specific by construction and is reported, never tested.

### K09 `camp_label` (primary; automatic)

**Move.** Camp labels for actors and sources. Merged from: process:M3 Camp labelling of actors and sources.

**Question.** Does B attach more partisan-alignment labels to actors or sources than A?

**Unit.** lead pair (counts).

**Coding rule.** Frozen regex auto_kpis.CAMP, outside quotation marks: 'pro-<Capitalised>' / 'pro-government|independence|regime|democracy'; 'anti-<Capitalised>|anti-government' + actor noun (groups, activists, organisations, lobby, forces, militias, campaigners, movements, advocacy, advocates, bias, commentators, media, parties, factions); 'and/or its/their/his/her supporters|allies|backers|defenders'; 'supporters of <Capitalised>'. K09_gain = count(new) > count(old).

**Include.** Narrator-voice labels anywhere in the lead; the pattern is group-neutral (pro-Russian, pro-government and pro-Israel all count).

**Exclude.** Spans inside straight or curly double quotes.

**Answer format.** Code: `0`, `1`. Primary binary indicator (OLD->NEW orientation): code in {`1`}. Auto field: `K09_gain`. Evidence: one verbatim quote per positive code.

**Direction scheme (descriptive).** `1`: adds a partisan-alignment label to an actor or source (party read off the matched spans, descriptive only).

**Discovery anchors (verbatim; before = lead0, after = lead1 of `qual_discovery.json`, checked by script).**

- *Anti-Defamation League* [topic] -> `1`, party JEWISH_ISRAELI  
  before: (no counterpart)  
  after: "The ADL is also known for its pro-Israel advocacy."
- *Francesca Albanese* [topic] -> `1`, party JEWISH_ISRAELI  
  before: "a bipartisan group of 18 members of the United States Congress called for Albanese to be removed"  
  after: "Pro-Israel organizations, including the U.S. government, have accused Albanese of antisemitism and anti-Israel bias"

**Automatable.** yes (regex). Precision audit: after the holdout run, coder 1 reviews all K09 gain spans (or 40 at random if more) for false positives; precision is reported, the KPI is not re-tuned.

### K06 `presupposed_eval_np` (secondary; automatic)

**Move.** Evaluative / legal category presupposed in a noun phrase. Merged from: voice:M7 Presupposed evaluation in noun phrases and lexicalised names.

**Question.** Does B pack more contested evaluative or legal categories into noun phrases (presupposed, not asserted) than A?

**Unit.** lead pair (count and rate per 100 words).

**Coding rule.** Frozen regex list auto_kpis.PRESUP, outside quotations: '<Name>-occupied/-annexed/-controlled/-blockaded'; '(the|in|of|from|into|on|across|throughout) occupied <Name>'; 'occupied territories/lands/areas/zones/regions'; 'illegal|unlawful (+1 word) settlements/occupation/annexation/outposts/wall/barrier/blockade/siege/detentions/invasion/regime/...'; '(the|a|an|from|in|into|of) blockaded|besieged'; 'forced evacuation/displacement/deportation/expulsion/transfer/.../labour/starvation'; '<Name> genocide|ethnic cleansing|apartheid' used as a name, excluding the version's own first-sentence subject. K06_gain = count and rate both higher in new.

**Include.** Group-neutral patterns; the topic-specific forms ('occupied Palestinian', 'Gaza genocide') are instances of generic patterns.

**Exclude.** Quoted spans; the article's own subject name in its first sentence; 'the Holocaust' and '<Place> massacre' event names.

**Answer format.** Code: `0`, `1`. Primary binary indicator (OLD->NEW orientation): code in {`1`}. Auto field: `K06_gain`. Evidence: one verbatim quote per positive code.

**Direction scheme (descriptive).** `1`: adds presupposed evaluative noun phrases (spans listed; party read off the spans, descriptive only).

**Discovery anchors (verbatim; before = lead0, after = lead1 of `qual_discovery.json`, checked by script).**

- *Criticism of Israel* [topic] -> `1`, party JEWISH_ISRAELI  
  before: "regarding Israeli settlements in the Palestinian territories"  
  after: "establishment and expansion of illegal Israeli settlements in the Palestinian territories"
- *Persecution of Uyghurs in China* [comparison] -> `1`, party OTHER_STATE  
  before: (no counterpart)  
  after: "forced labor"

**Automatable.** yes (regex). Demoted from primary: with a group-neutral lexicon the discovery contrast is +2.7 pp.

### K07 `harm_agent` (secondary; LLM-coded)

**Move.** Agent surfacing / backgrounding in harm clauses. Merged from: voice:M4 Agent surfacing/backgrounding, history:M3 Perpetrator specification, process:M7 Agent naming for harm.

**Question.** For a harm event present in both versions, is the doer of the harm more or less explicit in B?

**Unit.** lead pair (instances: one per harm event).

**Coding rule.** Explicitness scale: 4 active-voice subject; 3 by-phrase in the same clause; 2 possessive or premodifier ('Israel's blockade', 'Turkish strikes'); 1 agent named elsewhere in the same paragraph; 0 none (agentless passive, nominalisation, 'resulting in displacement'). Widening the responsible set (adding a sponsor or accomplice, faction -> state/movement) counts as more explicit. B_more_explicit / B_less_explicit / both / none by the same logic as K01.

**Include.** Harms: killing, massacre, expulsion, displacement, destruction, dispossession, blockade, siege, starvation, annexation, persecution, attack.

**Exclude.** Harm events present in only one version; non-harm acts (founded, signed); a pure name swap for the same actor (K05); changes only to the victim description.

**Answer format.** Code: `none`, `B_more_explicit`, `B_less_explicit`, `both`. Primary binary indicator (OLD->NEW orientation): code in {`B_more_explicit`, `both`}. Instance fields: `party` (party of the agent); `dir` (B_more_explicit | B_less_explicit); `level_A` (0-4); `level_B` (0-4). Evidence: one verbatim quote per positive code.

**Direction scheme (descriptive).** `B_more_explicit`: moves [party] from implicit to explicit doer of the harm (or widens its share) / `B_less_explicit`: moves [party] from explicit to implicit doer of the harm.

**Discovery anchors (verbatim; before = lead0, after = lead1 of `qual_discovery.json`, checked by script).**

- *Sabra and Shatila massacre* [topic] -> `B_more_explicit`, party JEWISH_ISRAELI (IDF moves from bystander-ally to supporting agent)  
  before: "a widespread massacre was carried out by the militia in plain sight of the Israeli Defence Forces (IDF), its ally."  
  after: "by the Lebanese Forces, one of the main Christian militias in Lebanon, with the support of the Israel Defense Forces (IDF)."
- *Nakba* [topic] -> `B_more_explicit`, party JEWISH_ISRAELI (agentless displacement -> by-phrase)  
  before: "and the permanent displacement of a majority of the Palestinian people"  
  after: "is the ethnic cleansing of Palestinian Arabs by Zionists through their violent displacement"
- *Turkish invasion of Cyprus* [comparison] -> `B_more_explicit`, party OTHER_STATE (agentless passive -> active subject)  
  before: "was launched on 20 July 1974, following the Cypriot coup d'état on 15 July 1974."  
  after: "Turkey invaded Cyprus on 20"

**Automatable.** no (LLM). All three readers found the rate not distinctive; it is secondary for the party breakdown.

### K08 `party_denial` (secondary; LLM-coded)

**Move.** Record-the-denial / rebuttal tail. Merged from: process:M2 Record-the-denial, voice:M3 Rebuttal tail.

**Question.** Does B newly record that a party to the dispute (or 'X and its supporters/allies') denies or disputes a claim made earlier in the lead?

**Unit.** lead pair.

**Coding rule.** B_adds: B contains a clause whose subject is a party to the dispute (state, government, organisation, or that party with its allies) with deny/dispute/reject/maintain that not/negate/counter, placed after the claim it answers, and A has no such clause for that claim. B_removes: reverse. both / none.

**Include.** Denial by the accused party or its allies; also a rebuttal of the denial added after it ('countered many of Israel's arguments').

**Exclude.** Symmetric 'X says ..., Y says ...' passages present in both versions. Dissent by scholars, analysts or other non-parties (that is K01 territory). Denials of a minor incident unrelated to the lead's central characterisation.

**Answer format.** Code: `none`, `B_adds`, `B_removes`, `both`. Primary binary indicator (OLD->NEW orientation): code in {`B_adds`, `both`}. Instance fields: `party` (denying party); `dir` (B_adds | B_removes). Evidence: one verbatim quote per positive code.

**Direction scheme (descriptive).** `B_adds`: places [party]'s position as a denial recorded after a baseline claim / `B_removes`: removes [party]'s recorded denial.

**Discovery anchors (verbatim; before = lead0, after = lead1 of `qual_discovery.json`, checked by script).**

- *Israel* [topic] -> `B_adds`, party JEWISH_ISRAELI  
  before: (no counterpart)  
  after: "Israel and its allies, including the United States, deny that Israel's actions constitute genocide."
- *Nakba* [topic] -> `B_adds`, party JEWISH_ISRAELI  
  before: (no counterpart)  
  after: "Israel negates or denies the atrocities it committed"

**Automatable.** no (LLM). Readers disagree on whether it is distinctive; secondary.

### K10 `refusal_recontextualised` (secondary; LLM-coded)

**Move.** Rejection recontextualised. Merged from: history:M7 Rejection recontextualised.

**Question.** Does B change the narrative role of a party's refusal, rejection or first attack that A presented as the trigger of a war, a displacement or a failed settlement?

**Unit.** lead pair.

**Coding rule.** B_recontextualises: in B that refusal or first act is (a) deleted, (b) given a stated motive or reason, or (c) preceded in the same paragraph by an earlier cause attributed to another party. B_reinstates: the reverse (added as an unexplained trigger, motive removed, prior cause removed). both / none.

**Include.** Rejection of partition or peace plans or conditions; an invasion or attack presented as starting a war; evacuation orders or voluntary departure presented as a cause of flight; refusal to recognise.

**Exclude.** Refusals that are not presented as a trigger or cause; unchanged role; pure relocation within the lead without change of role.

**Answer format.** Code: `none`, `B_recontextualises`, `B_reinstates`, `both`. Primary binary indicator (OLD->NEW orientation): code in {`B_recontextualises`, `both`}. Instance fields: `party` (refusing / first-acting party); `dir` (B_recontextualises | B_reinstates); `how` (deleted | motive | prior_cause | added_trigger). Evidence: one verbatim quote per positive code.

**Direction scheme (descriptive).** `B_recontextualises`: moves [party]'s refusal/first act from inciting cause to a response with reasons, or out of the lead / `B_reinstates`: moves [party]'s refusal/first act into the role of unexplained trigger.

**Discovery anchors (verbatim; before = lead0, after = lead1 of `qual_discovery.json`, checked by script).**

- *Israel* [topic] -> `B_recontextualises`, party PALESTINIAN_ARAB (motive added)  
  before: "The plan was accepted by the Jewish Agency, and rejected by Arab leaders."  
  after: "The Jewish leadership accepted the plan while the Palestinian Arab leadership rejected it, arguing it violated the principle of self-determination and constituted Western colonial interference."
- *Mandatory Palestine* [topic] -> `B_recontextualises`, party PALESTINIAN_ARAB (deleted as cause)  
  before: "After the failure of the Arab population to accept the United Nations Partition Plan for Palestine"  
  after: "The United Nations Partition Plan for Palestine, adopted by the UN General Assembly in November 1947, recommended dividing the territory into two states, one Arab and one Jewish."
- *Israeli–Palestinian conflict* [topic] -> `B_reinstates`, party PALESTINIAN_ARAB (reverse: rejection added as trigger)  
  before: (no counterpart)  
  after: "The plan was rejected by the Arab Higher Committee and the Arab League, triggering the 1947–1948 civil war in Mandatory Palestine."

**Automatable.** no (LLM). Comparison analogues are rare by construction; read as a topic-internal description.

### K11 `belonging_claims` (secondary; LLM-coded)

**Move.** Belonging claims: continuity split and demography as belonging. Merged from: history:M4 Jewish continuity split by period, history:M5 Arab demographic-majority anchor.

**Question.** Does B add, strengthen, remove or re-attribute a claim that grounds a group's tie to a land?

**Unit.** lead pair (instances: one per group x claim type).

**Coding rule.** Claim types: continuity (ancestral homeland, return, re-establishment, birthplace, persisting presence, ancient polity as the group's own); demography (the group as historical majority or minority, percentages, 'since at least the 12th century'); indigeneity ('indigenous', 'native' applied to a group). B_strengthens: claim added, or moved toward narrator voice / de-hedged. B_weakens: deleted, or moved into a party's voice ('Zionists viewed ...') / hedged. both / none.

**Include.** Any group, in either group of articles.

**Exclude.** Present-day population statistics with no historical frame; diaspora history that is not about the tie to the land; unchanged claims.

**Answer format.** Code: `none`, `B_strengthens`, `B_weakens`, `both`. Primary binary indicator (OLD->NEW orientation): code in {`B_strengthens`, `B_weakens`, `both`}. Instance fields: `party` (group whose tie is claimed); `dir` (B_strengthens | B_weakens); `type` (continuity | demography | indigeneity). Evidence: one verbatim quote per positive code.

**Direction scheme (descriptive).** `B_strengthens`: strengthens [party]'s stated tie to the land (by type) / `B_weakens`: removes or re-attributes [party]'s stated tie to the land (by type).

**Discovery anchors (verbatim; before = lead0, after = lead1 of `qual_discovery.json`, checked by script).**

- *Balfour Declaration* [topic] -> `B_strengthens`, party PALESTINIAN_ARAB (type demography)  
  before: "then an Ottoman region with a small minority Jewish population."  
  after: "then an Ottoman region with a small Jewish minority among an overwhelming Arab majority, mostly Muslim but also including Christians."
- *Bar Kokhba Revolt* [topic] -> `B_strengthens`, party JEWISH_ISRAELI (type continuity; hedge removed)  
  before: "The common view that the name change was intended to "sever the connection of the Jews to their historical homeland" is disputed."  
  after: "an act intended to sever the region's historical association with the Jewish people"
- *Israel* [topic] -> `B_weakens`, party JEWISH_ISRAELI (type continuity; sentence deleted)  
  before: "Jewish presence in the region has persisted to a certain extent over the centuries."  
  after: (deleted)

**Automatable.** partly. Auto support proxy SUP_majority_gain (majority/minority/percentage wording) is reported, never tested.

### K12 `suffering_motive_slot` (secondary; LLM-coded)

**Move.** Suffering slotting (harm as motive). Merged from: history:M8 Suffering slotting and pairing.

**Question.** Does B newly present harm suffered by a group as the motive or cause of that same group's later action?

**Unit.** lead pair.

**Coding rule.** B_adds_motive: B adds or makes explicit a causal link from harm or grievance suffered by group X (pogroms, genocide, persecution, expulsion, discrimination, occupation) to an action by group X (migration, organising, armed struggle, state-building), via 'fleeing', 'stimulated by', 'in response to', 'as a reaction to', 'driven by'. B_removes_motive: the reverse. both / none.

**Include.** Explicit causal links only.

**Exclude.** Harm presented as the consequence of another party's act (consequence slot); casualty updates; harm mentioned with no causal link to the group's own action.

**Answer format.** Code: `none`, `B_adds_motive`, `B_removes_motive`, `both`. Primary binary indicator (OLD->NEW orientation): code in {`B_adds_motive`, `both`}. Instance fields: `party` (group whose suffering); `dir` (B_adds_motive | B_removes_motive). Evidence: one verbatim quote per positive code.

**Direction scheme (descriptive).** `B_adds_motive`: places [party]'s suffering as the motive of [party]'s later action / `B_removes_motive`: removes the motive link between [party]'s suffering and its later action.

**Discovery anchors (verbatim; before = lead0, after = lead1 of `qual_discovery.json`, checked by script).**

- *Haganah* [topic] -> `B_adds_motive`, party JEWISH_ISRAELI  
  before: "ships used to deport illegal Jewish immigrants, as well as assisting in bringing Jews to Palestine"  
  after: "ships used to deport illegal Jewish immigrants fleeing The Holocaust"
- *First Aliyah* [topic] -> `B_adds_motive`, party JEWISH_ISRAELI  
  before: "Jews who migrated in this wave came mostly from Eastern Europe and from Yemen."  
  after: "Jews who migrated in this wave came mostly from Eastern Europe, stimulated by pogroms and violence against the Jewish communities there."

**Automatable.** no (LLM).

## 8. Style controls and dropped moves

**SC1 genus_change (LLM).** Does the class of the head noun of the first sentence's defining predicate change at all (any class, e.g. ideology -> nationalism, terrorist group -> militant organisation)? Values: none / changed. All readers: genus rewriting is general Wikipedia style (voice ~24% vs ~24%; history 15/71 vs 5/20). Measured in both groups as a denominator for K04. Anchors (comparison): *Turkish nationalism*: "is a political ideology that promotes and glorifies the Turkish people" -> "is nationalism among the people of Turkey and individuals whose national identity is Turkish."; *Al-Shabaab (militant group)*: "is a terrorist, jihadist fundamentalist group based in East Africa." -> "is a transnational Wahhabi-Salafi Jihadist militant organization.".

**Auto style controls.** `SC_len_ratio` = lead word ratio new/old; `SC_fs_change` = 1 - word similarity of first sentences; `SC_rest_change` = same for the rest of the lead; `SC_protected_opening` = fs_change < rest_change - 0.2; `SC_fs_tense_flip` = was/is flip in sentence 1; `SC_attr_density_up/down` = attribution-marker density per sentence; `SC_terror_fs_removed/added` = terror* leaves/enters sentence 1 (voice M8: general MOS:LABEL style); `SC_alt_names_fs_up/down` = naming formulas in sentence 1. Readers called these general style (terror-label relocation, relocation/demotion, compression, de-quoting, tense flips, attribution clean-up). Reported for both groups; never tested.

**Dropped as KPIs:**
- Terrorism-label relocation (voice M8): general MOS:LABEL style, same rate in comparison jihadist groups; kept as style control SC_terror_fs_*.
- Relocation / demotion within the lead (process M8): general style (10/48 vs 5/16); partly visible in SC_protected_opening.
- Genus reclassification as such (voice M6, history M10): same rate both groups; kept as SC1; destination class kept as K04.
- Proposition displacement / update to recent events / compression (history M10, process): general style; SC_len_ratio and SC_rest_change.
- Colonial vocabulary rate anywhere in lead (history M2 KPI colonial_token_delta): not distinctive (comparison indigenous/settler articles gain it too); only definitional position kept (K04).
- Policy-and-procedure justification, trajectory type (process M9, M10): need revision histories (edit summaries / ratchet.json); first_sentence_edits exist for 24 discovery articles only; out of scope for masked lead-pair coding.
- Asymmetric source quantifiers as a separate KPI (voice M2): merged into the K01 ladder (rung 2 vs rung 4).
- Suffering pairing in one sentence (history M8b): few cases (3 added, 1 removed); not crisp enough to code reliably.
- Scare quotes, 'so-called': voice reader: declining in both groups; 'so-called' never occurs.

## 9. Discovery numbers for the automatic measures (frozen regexes; coding set minus artefacts: 166 topic, 46 comparison)

These are discovery values, given for calibration. They are not results.

| measure | topic | comparison | diff | topic T1/T2/T3 | comparison T1/T2/T3 |
|---|---|---|---|---|---|
| K09 camp label added (PRIMARY) | 0.06 | 0.0 | +0.060 | 3/64, 4/59, 3/43 | 0/7, 0/12, 0/27 |
| K06 presupposed evaluative NP added | 0.114 | 0.087 | +0.027 | 4/64, 6/59, 9/43 | 1/7, 1/12, 2/27 |
| K06 ... removed | 0.042 | 0.022 | +0.020 | 0/64, 3/59, 4/43 | 0/7, 1/12, 0/27 |
| K04a colonial term enters sentence 1, narrator voice | 0.018 | 0.022 | -0.004 | 0/64, 1/59, 2/43 | 0/7, 0/12, 1/27 |
| support: 'Zionist(s)+actor' added (topic lexicon) | 0.084 | 0.0 | +0.084 | 3/64, 6/59, 5/43 | 0/7, 0/12, 0/27 |
| support: majority/minority wording added | 0.072 | 0.065 | +0.007 | 1/64, 3/59, 8/43 | 0/7, 1/12, 2/27 |
| style: protected opening | 0.276 | 0.341 | -0.065 | 17/52, 14/57, 11/43 | 2/5, 2/12, 11/27 |
| style: was/is flip in sentence 1 | 0.133 | 0.109 | +0.024 | 3/64, 11/59, 8/43 | 0/7, 2/12, 3/27 |
| style: attribution density up | 0.157 | 0.196 | -0.039 | 10/64, 11/59, 5/43 | 0/7, 2/12, 7/27 |
| style: attribution density down | 0.289 | 0.435 | -0.146 | 7/64, 18/59, 23/43 | 3/7, 6/12, 11/27 |
| style: terror* leaves sentence 1 | 0.006 | 0.022 | -0.016 | 0/64, 0/59, 1/43 | 0/7, 0/12, 1/27 |
| style: naming formulas up in sentence 1 | 0.084 | 0.152 | -0.068 | 1/64, 4/59, 9/43 | 1/7, 2/12, 4/27 |
| style: naming formulas down | 0.084 | 0.043 | +0.041 | 2/64, 6/59, 6/43 | 0/7, 0/12, 2/27 |

## 10. Holdout procedure (run once)

1. `python auto_kpis.py data/study3/qual_holdout.json OUT/holdout_auto.json`
2. `python make_batches.py data/study3/qual_holdout.json OUT/holdout_batches` (default seed `study3-partC`, 2 coders, about 20 pairs per batch). Keep `KEY_DO_NOT_SHARE.json` away from the coders.
3. For each coder and batch: a fresh session gets `coder_instructions.md` (the PROMPT part) plus `coderN/batch_XX.json`. Save the JSON array it returns as `OUT/codes/coderN/out_batch_XX.json`. Two independent sessions; no retries except the evidence re-run rule in section 6.
4. `python analyze_codes.py --key OUT/holdout_batches/KEY_DO_NOT_SHARE.json --batches OUT/holdout_batches --codes coder1=OUT/codes/coder1 --codes coder2=OUT/codes/coder2 --auto OUT/holdout_auto.json --codebook codebook.json --out OUT/holdout_partC_results.json`
5. Report every KPI: kappa, shares, delta with CI, p, BH q, terciles, MH, verdict, party breakdown, sensitivity analyses, style controls. Also the K09 span precision audit and the K04a/K04 agreement.

## 11. Known weaknesses

- Thin comparison group: 46 discovery pairs, only 7 in T1, and a few heavily edited ones dominate. Shares of 0/46 make bootstrap CIs degenerate. That is why p comes from permutation, but power for moves with a 5-10% topic rate is low.
- The reader counts behind the LLM KPIs are one reader's tallies on non-random subsets; no LLM pilot on discovery was run. The primary family is chosen on triangulation, not on measured discovery effect sizes, except for the auto KPIs.
- The selection is asymmetric: topic pairs must have change > 0.05, comparison pairs are all included. In discovery every comparison pair has change > 0.05; on holdout the pre-specified sensitivity analysis applies the same filter to both groups.
- Party codes name Jewish/Israeli and Palestinian/Arab parties, so coders know the study's subject. The content reveals the subject anyway. Masking protects the group label and the before/after direction only.
- K03 and K11 have no inherent forward direction. Their primary indicator is 'any change', and their meaning lies in the per-party breakdown, which is descriptive.
- K10 and K12 have few comparison analogues by construction. Their contrasts should be read as topic-internal descriptions.
- For articles created after Jan 2021 (Gaza war, Gaza genocide, October 7 attacks and others), lead0 is a 2022-2025 text. A sensitivity analysis restricted to d0 in 2021 is pre-specified.
- Lead-pair snapshots miss intra-window oscillation (process reader: 66% of traced edits hide an untraced change). Process KPIs (justification repertoire, ratchet/oscillation) need ratchet.json and are out of scope here.
