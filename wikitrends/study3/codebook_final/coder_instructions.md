# Coder instructions: study 3, Part C content KPIs (codebook study3-partC-v1.0, frozen 2026-11-05)

This file is the exact prompt for each LLM coder. Give it, followed by ONE batch file (`batch_XX.json` from `make_batches.py`), to a fresh session with no other context. The two coders run in separate sessions and never see each other's output.

---

## PROMPT (copy everything below this line)

You are coding changes between two versions of the opening section ("lead") of encyclopedia articles. For each item you get **Version A** and **Version B** of the same lead. Some items also include `other_first_sentence_variants`: other wordings that the first sentence had at some point. They are unordered, carry no dates, and are context only. **Code only the difference between A and B.**

You are not told the article title, which group of articles it belongs to, or which version is older. The A/B order was randomised. Do not try to work out which version is older, and do not let a guess affect your codes. **Every code describes B relative to A.** "B_more_X" means B has more X than A, whatever the dates.

Describe what the text does. Do not judge whether either version is true, fair or biased. Do not use outside knowledge to fill gaps. If something is not in the text, it is not there.

### General rules
1. Answer all 12 items (K01–K12, minus the two automatic ones K06 and K09, plus SC1) for every pair. That is K01, K02, K03, K04, K05, K07, K08, K10, K11, K12, SC1.
2. Each answer has a `code` from the allowed values. `none` means the move does not occur between A and B.
3. One pair can show a move in opposite directions (e.g. one claim upgraded, another downgraded). Use `both` and list each instance.
4. **Evidence is required for every code other than `none`.** Give exactly one line, `"A: <quote>"` or `"B: <quote>"`. The quote must be copied character for character from that version: one contiguous span, at most 30 words, no ellipses, no paraphrase, no added words. Take it from the version where the feature is present (usually the version that has the new wording). A code whose quote is not verbatim is discarded.
5. **Parties.** For directional KPIs, list the party the move concerns. Use exactly one of these values:
   - `JEWISH_ISRAELI`: Jews as a people or community; Israel, its government, forces or citizens; the Zionist movement and its organisations; the Yishuv and pre-state Jewish militias; Hebrew or Jewish-tradition names.
   - `PALESTINIAN_ARAB`: Palestinians and Palestinian organisations (PLO, Hamas, PA, militias); Arab states and forces in the Arab–Israeli context; Arabic or Islamic names of places and shared holy sites in Israel/Palestine.
   - `OTHER_STATE`: any other state, government, empire or ruling power.
   - `OTHER_GROUP`: any other people, community, movement or non-state armed group.
   - `MULTIPLE`: several parties at once that cannot be split. `UNCLEAR`: cannot tell from the text.
6. Ignore pure length changes, reordering that changes nothing listed below, typo fixes, transliteration, markup, and updates of numbers or dates.
7. Set `"usable": false` only if a version is not a readable lead (template code, a list of links, empty). Still fill in the codes as best you can.

### The items

**K01 voice_upgrade.** *Does a contested characterisation that appears in both versions sit on a different rung of the attribution ladder in B than in A?*
- Contested characterisation: an evaluative, legal or atrocity category, or an intent or historicity claim, applied to an actor's conduct or an entity's nature. Examples: genocide, ethnic cleansing, apartheid, illegal / violation of international law, war crimes, terrorism, massacre, colonial / settler-colonial, racism, antisemitism, propaganda, "whether X existed", "intended to".
- Ladder: 1 alleged/accused/claimed ("allegations have been made", "has been accused of"); 2 attributed to "some", critics, a minority or one party ("some historians", "critics call"); 3 attributed to named authorities or institutions ("according to the UN", "the ICJ found", "the international community considers"); 4 majority or consensus ("many scholars", "most experts", "scholars widely", "academic consensus"); 5 narrator voice (stated with no attribution) or part of the definition. Use 0 for "absent".
- Code only characterisations with the same category and the same target in BOTH versions. Code `B_more_narrator` if one or more is on a higher rung in B and none is lower; `B_less_narrator` if one or more is lower and none higher; `both` if both happen; otherwise `none`.
- Exclude: rewording on the same rung; swapping one named source for another; casualty numbers and dates. You MAY list a characterisation present in only one version as an instance with `dir` `new_in_B` or `dropped_in_B` (level 0 on the absent side), but it does not set the code.
- Instance fields: `party` (the target of the characterisation, not the source), `dir`, `category`, `level_A`, `level_B`.
- Example. A: "described by some historians as ethnic cleansing, while others dispute this charge" / B: "Scholars widely describe the event as ethnic cleansing, although some disagree." gives `B_more_narrator`, JEWISH_ISRAELI, 2 to 4. Example in the other order. A: "The international community considers Israeli settlements to be illegal under international law, but Israel disputes this." / B: "built in violation of international law on lands occupied by Israel" gives `B_more_narrator`, 3 to 5.

**K02 story_onset.** *Does B start the causal story of the subject earlier than A, or add an earlier prior cause or precondition?*
- In each version find the earliest event or condition presented as the origin, cause or precondition of the subject (cues: "has its origins in", "began", "dates (back) to", "rooted in", "marked the start", "arose from", "after", "following", "in response to", or a premodifier that sets a precondition at the start of the event, such as "from the blockaded ...").
- `B_earlier`: B's earliest stated cause is earlier in time, or B adds a prior cause before the event A presented as the start. `B_later`: the reverse. `both`, `none`.
- Exclude: chronology with no causal link (founding dates, lists of later events); background about the subject that is not presented as a cause; consequences.
- Instance fields: `party` (whose action or imposed condition is the added or removed cause; UNCLEAR if no actor), `dir` (`B_adds_prior_cause` / `B_removes_prior_cause`), `onset_year_A`, `onset_year_B` (integer or null).
- Example. A: "that began in the mid-20th century" / B: "The conflict has its origins in the rise of Zionism in the late 19th century in Europe" gives `B_earlier`, JEWISH_ISRAELI, B_adds_prior_cause.

**K03 name_primacy.** *Does B change which name is primary for the subject or for a place, territory or polity, or the status or order of alternative names from different communities?*
- Code `changed` when, for the same referent, B (a) uses a different head or primary name, (b) adds or removes an alternative name associated with another community, language or tradition, (c) reorders co-names or moves a name between primary ("X or Y") and gloss status ("known to Muslims as Y", "in Jewish tradition", "(roughly corresponding to Y)"), or (d) uses a different name for the same earlier period ("southern Syrian provinces" vs "region of Palestine" vs "Land of Israel").
- Exclude: transliteration, script, pronunciation; **macro-region labels for a modern location (Middle East / West Asia / Western Asia / Levant / Southern Levant): do not code**; administrative phrases ("governed as part of"); actor labels (K05); names inside quotations.
- Instance fields: `party` (community whose name moves), `dir` (`B_promotes` / `B_demotes`), `in_first_sentence` (true/false).
- Example. A: "known to Muslims as the Haram esh-Sharif" / B: "The Temple Mount or al-Haram al-Sharif" gives `changed`, PALESTINIAN_ARAB, B_promotes. Not coded: A "is a city in the Middle East" / B "is a city in the Southern Levant".

**K04 definitional_class.** *Does the defining predicate of the FIRST SENTENCE gain or lose a colonial, atrocity, legal-violation or apartheid/racism category in narrator voice?*
- The defining predicate is the head noun phrase of "X is/was a ...", "X refers to", "X was the ... of", with its modifiers and any means or purpose phrase ("through colonization"). Alternative names in the first sentence count ("also called ... colonies").
- Classes: `colonial` (colonization, colonies, colonial, settler-colonial); `atrocity` (genocide, ethnic cleansing, massacre, mass murder, mass expulsion, extermination); `legal_violation` (illegal, unlawful, in violation of international law, war crimes); `apartheid_racism` (apartheid, racist, supremacist).
- `B_gains`: B's predicate has one of these in narrator voice and A's does not (or A has it only as someone's description). `B_loses`: the reverse. `both`, `none`.
- Exclude: a category in an attribution frame ("has been described as a form of settler colonialism"); categories outside the first sentence; the same class in both versions; changes between militant, terrorist, nationalist or political labels (those go to SC1); "ethnic nationalist" and other nationalism labels.
- Instance fields: `party` (whose project or act the category characterises), `dir`, `class`.
- Example. A: "was the destruction of Palestinian society and homeland in 1948" / B: "is the ethnic cleansing of Palestinian Arabs by Zionists" gives `B_gains`, JEWISH_ISRAELI, atrocity.

**K05 actor_relabel.** *Does B change the category of the label for a collective actor present in both versions, especially to an ideological label?*
- Label categories: E ethnoreligious/national people ("Jewish militias", "Arab forces", "the Jewish population"); S state ("Israel", "IDF", "the Ottoman government"); I ideological/movement ("Zionists", "Zionist militants", "Islamists", "jihadists"); O named organisation ("Irgun", "Haganah", "Hamas").
- `B_more_ideological`: for the same actor, B uses I where A used E, S or O. `B_less_ideological`: the reverse. `other_change`: the category changes without involving I. `both`, `none`.
- Exclude: the ideology as an idea or its name ("Zionism", "the Zionist movement"); self-designations in quotation; an actor in only one version; same-category synonyms ("Israel" to "the IDF").
- Instance fields: `party`, `dir`, `from_cat`, `to_cat` (from = A, to = B).
- Example. A: "The Zionist militants massacred Palestinian Arab villagers" / B: "than the Jewish militias had expected" gives `B_less_ideological`, JEWISH_ISRAELI, I to E.

**K07 harm_agent.** *For a harm event present in both versions, is the doer more or less explicit in B?*
- Scale: 4 active-voice subject; 3 by-phrase; 2 possessive or premodifier ("Israel's blockade", "Turkish strikes"); 1 named elsewhere in the same paragraph; 0 none (agentless passive, nominalisation, "resulting in displacement"). Adding a sponsor or accomplice, or widening a faction to a state or movement, counts as more explicit.
- Harms: killing, massacre, expulsion, displacement, destruction, dispossession, blockade, siege, starvation, annexation, persecution, attack.
- `B_more_explicit` / `B_less_explicit` / `both` / `none`. Exclude: harm events in only one version; non-harm acts; a pure name swap for the same actor (K05).
- Instance fields: `party` (of the agent), `dir`, `level_A`, `level_B`.
- Example. A: "was launched on 20 July 1974, following the Cypriot coup d'état on 15 July 1974." / B: "Turkey invaded Cyprus on 20July 1974" (copied as it appears, missing space included) gives `B_more_explicit`, OTHER_STATE, 0 to 4.

**K08 party_denial.** *Does B newly record that a party to the dispute (or "X and its supporters/allies") denies or disputes a claim made earlier in the lead?*
- `B_adds`: B has a clause in which a party (state, government, organisation, or that party with its allies) denies, disputes, rejects, maintains that ... not, negates or counters a claim stated earlier in the lead, and A has no such clause for that claim. `B_removes`: the reverse. `both`, `none`.
- Exclude: symmetric "X says ..., Y says ..." passages present in both; dissent by scholars, analysts or other non-parties (K01); denials of a minor incident.
- Instance fields: `party` (the denying party), `dir`.
- Example. A: (no such sentence) / B: "Israel and its allies, including the United States, deny that Israel's actions constitute genocide." gives `B_adds`, JEWISH_ISRAELI.

**K10 refusal_recontextualised.** *Does B change the role of a party's refusal, rejection or first attack that A presented as the trigger of a war, a displacement or a failed settlement?*
- `B_recontextualises`: in B that refusal or first act is (a) deleted, (b) given a stated motive or reason, or (c) preceded in the same paragraph by an earlier cause attributed to another party. `B_reinstates`: the reverse (added as an unexplained trigger, motive removed, prior cause removed). `both`, `none`.
- Include: rejection of partition or peace plans; an invasion or attack presented as starting a war; evacuation orders or voluntary departure presented as a cause of flight; refusal to recognise.
- Instance fields: `party` (who refused or acted first), `dir`, `how` (`deleted` / `motive` / `prior_cause` / `added_trigger`).
- Example. A: "The plan was accepted by the Jewish Agency, and rejected by Arab leaders." / B: "the Palestinian Arab leadership rejected it, arguing it violated the principle of self-determination" gives `B_recontextualises`, PALESTINIAN_ARAB, motive.

**K11 belonging_claims.** *Does B add, strengthen, remove or re-attribute a claim that grounds a group's tie to a land?*
- Types: `continuity` (ancestral homeland, return, re-establishment, birthplace, persisting presence, ancient polity as the group's own); `demography` (the group as historical majority or minority, percentages, "since at least the 12th century"); `indigeneity` ("indigenous" or "native" applied to a group).
- `B_strengthens`: the claim is added, or moved toward narrator voice, or de-hedged. `B_weakens`: deleted, moved into a party's voice ("Zionists viewed ... as the Jewish ancestral homeland" where A had "regarded by the Jewish people as their ancestral homeland"), or hedged. `both`, `none`.
- Exclude: present-day population figures with no historical frame; diaspora history not about the tie to the land.
- Instance fields: `party` (whose tie), `dir`, `type`.
- Example. A: "then an Ottoman region with a small minority Jewish population." / B: "then an Ottoman region with a small Jewish minority among an overwhelming Arab majority" gives `B_strengthens`, PALESTINIAN_ARAB, demography.

**K12 suffering_motive_slot.** *Does B newly present harm suffered by a group as the motive or cause of that same group's later action?*
- `B_adds_motive`: B adds or makes explicit a causal link from harm or grievance suffered by group X (pogroms, genocide, persecution, expulsion, discrimination, occupation) to an action by group X (migration, organising, armed struggle, state-building), via "fleeing", "stimulated by", "in response to", "as a reaction to", "driven by". `B_removes_motive`: the reverse. `both`, `none`.
- Exclude: harm presented as the consequence of another party's act; casualty updates; harm with no causal link to the group's own action.
- Instance fields: `party` (whose suffering), `dir`.
- Example. A: "Jews who migrated in this wave came mostly from Eastern Europe and from Yemen." / B: "came mostly from Eastern Europe, stimulated by pogroms and violence against the Jewish communities there." gives `B_adds_motive`, JEWISH_ISRAELI.

**SC1 genus_change.** *Does the class of the head noun of the first sentence's defining predicate change at all?* (any class: ideology to nationalism, terrorist group to militant organisation, event to atrocity, and so on). `changed` / `none`. No parties needed; evidence required if `changed`.

### Output format
Return ONLY a JSON array with one object per item, in any order, using exactly these keys. Omit `parties` when the code is `none`. Example (codes illustrative):

```json
[
  {
    "id": "P1a2b3c4d",
    "usable": true,
    "K01": {"code": "B_more_narrator", "evidence": "B: Scholars widely describe the event as ethnic cleansing, although some disagree.",
            "parties": [{"party": "JEWISH_ISRAELI", "dir": "B_more_narrator", "category": "ethnic cleansing", "level_A": 2, "level_B": 4}]},
    "K02": {"code": "none"},
    "K03": {"code": "changed", "evidence": "B: The Temple Mount or al-Haram al-Sharif",
            "parties": [{"party": "PALESTINIAN_ARAB", "dir": "B_promotes", "in_first_sentence": true}]},
    "K04": {"code": "none"},
    "K05": {"code": "none"},
    "K07": {"code": "none"},
    "K08": {"code": "none"},
    "K10": {"code": "none"},
    "K11": {"code": "none"},
    "K12": {"code": "none"},
    "SC1": {"code": "none"}
  }
]
```

Allowed codes:
- K01: none, B_more_narrator, B_less_narrator, both. Instance dir: B_more_narrator, B_less_narrator, new_in_B, dropped_in_B.
- K02: none, B_earlier, B_later, both. Instance dir: B_adds_prior_cause, B_removes_prior_cause.
- K03: none, changed. Instance dir: B_promotes, B_demotes.
- K04: none, B_gains, B_loses, both. Instance dir: B_gains, B_loses.
- K05: none, B_more_ideological, B_less_ideological, both, other_change. Instance dir: B_more_ideological, B_less_ideological, other_change.
- K07: none, B_more_explicit, B_less_explicit, both. Instance dir: B_more_explicit, B_less_explicit.
- K08: none, B_adds, B_removes, both. Instance dir: B_adds, B_removes.
- K10: none, B_recontextualises, B_reinstates, both. Instance dir: B_recontextualises, B_reinstates.
- K11: none, B_strengthens, B_weakens, both. Instance dir: B_strengthens, B_weakens.
- K12: none, B_adds_motive, B_removes_motive, both. Instance dir: B_adds_motive, B_removes_motive.
- SC1: none, changed.

### Before you answer, check
- Every item id in the batch appears once.
- Every code is from the list, and every non-`none` code has a one-line verbatim `evidence` prefixed `A:` or `B:`.
- Directions are B relative to A. For instances, `level_A`/`from_cat` describe A and `level_B`/`to_cat` describe B.
- You coded what the text says, not what you believe happened.
