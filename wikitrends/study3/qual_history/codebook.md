# Codebook, lens: historiography and story grammar (study 3, phase A)

Reader: close reader 3 (history of the Middle East and collective memory).
Material: `data/study3/qual_discovery.json` only. I did not open the holdout file.
Machine-readable version: `codebook.json` in this folder. Every quoted before/after was checked by script as an exact substring of `lead0`/`lead1`, or of the cited `first_sentence_edits` entry.

## 1. What I read

- **Topic pairs: 71 read in full.** These were the top 60 by change, plus a sample from the middle and the tail (Haganah, Lehi, Jerusalem, Land of Israel, Balfour Declaration, Nakba denial, Second Aliyah, Palestinian right of return, and others). About 45 of the 71 are "conflict-core" (Zionism, Israel, Palestine, 1948, 1967, Gaza, settlements, militias). About 26 are about Jewish religion, communities or antiquity.
- **Comparison pairs: 20 read in full.** These were Quebec sovereignty movement, Tigray war, Turkish nationalism, Arab nationalism*, Aboriginal Australians, Indian diaspora, Persecution of Uyghurs in China, Armenian genocide, Palestinian nationalism*, Tibet, Greek diaspora, Kashmir conflict, Romani people, The Troubles, Native Americans in the United States, Population exchange between Greece and Turkey, History of South Africa, History of Australia, Turkish invasion of Cyprus, and Armenian nationalism. (* = control_contaminated)
- **First-sentence edit histories read:** Zionism, Israel, Nakba, Jews, Israeli–Palestinian conflict, History of Israel, Mandatory Palestine, Land of Israel, Jerusalem, Zionism as settler colonialism, Anti-Zionism, Hamas, Israeli settlement, 1948 Palestinian expulsion and flight, Balfour Declaration, October 7 attacks, Gaza war, and Gaza genocide.
- **Regex check of term gains and losses across all 237 discovery pairs** (script in `work/terms.py`). I used it only to sanity-check my counts.

**Caveats on the counts.**
1. My comparison sample over-weights conflict, genocide and colonial articles (Armenian, Uyghur, Tigray, Native Americans, Cyprus, Kashmir, Troubles). That inflates comparison rates for atrocity-related moves.
2. About a third of my topic pairs are non-conflict articles, which deflates topic rates.
3. The counts are one reader's rough tallies, not a reliability-tested coding.
4. For Gaza war, Gaza genocide and October 7 attacks, `lead0` is really a late-2023/early-2024 text, because the articles did not exist in Jan 2021. These pairs measure change within 2023–2026 and should be flagged in any KPI.

## 2. In-vivo codes (open coding, abbreviated)

`origins-in-Zionism`, `began-mid-20th-c deleted`, `through colonization`, `also called colonies`, `re-establishment -> establishment`, `long Jewish connection deleted`, `birthplace of the Jewish people deleted`, `Jewish presence persisted deleted`, `Jewish people -> Zionists viewed`, `since the First Temple`, `literary construction -> ongoing debate`, `renaming intent: disputed -> fact`, `overwhelming Arab majority`, `78% Muslim Arab`, `by Zionists`, `supported by the Haganah and Palmach`, `under Ben-Gurion's leadership ... expulsion`, `allegations -> is`, `some historians -> scholars widely`, `rejected, arguing ...`, `failure of the Arabs to accept deleted`, `Arab evacuation orders deleted`, `fleeing The Holocaust`, `stimulated by pogroms`, `133 Jews -> 133 Jews and 116 Arabs`, `exodus pair -> regional displacement`, `by Israel -> by Zionists (Plan Dalet before May 14)`, `emigration back to Israel -> emigration to Ottoman Syria`, `southern Syrian provinces -> region of Palestine`, `Mandatory Palestine since the 12th century`, `militant deleted from genus`, `terrorist means deleted`, `violence aimed at Israeli civilians deleted`, `blockade dates to 1990s`, `from the blockaded Gaza Strip`, `continuation of the Nakba`, `achievement list cut`, `polls/peace-process detail cut`, `events update (ceasefires, 2026 wars)`.

These were grouped into 10 moves.

## 3. Moves, ranked by how distinctive they are of topic vs comparison

Counts are "topic pairs out of 71 read / comparison pairs out of 20 read". Full definitions, include/exclude rules and verbatim examples are in `codebook.json`. Below is a summary with one or two examples each.

### Rank 1. M7 Rejection recontextualised (9/71 vs 0/20)
**Definition.** The "Arab rejection" plot point is changed in one of three ways: it is deleted, it is given a motive, or it is placed after a prior Zionist or British cause. The plot point covers rejection of the 1947 partition, rejection of the Quartet conditions, the Arab invasion presented as the start of the 1948 war, and Arab evacuation orders presented as a cause of the flight.

**Examples.**
- *Israel.* "The plan was accepted by the Jewish Agency, and rejected by Arab leaders." becomes "The Jewish leadership accepted the plan while the Palestinian Arab leadership rejected it, arguing it violated the principle of self-determination and constituted Western colonial interference."
- *1948 Palestinian expulsion and flight.* The cause list drops "Arab evacuation orders, and an unwillingness to live under Jewish control."
- *Reverse case, Israeli–Palestinian conflict.* The new lead adds "The plan was rejected by the Arab Higher Committee and the Arab League, triggering the 1947–1948 civil war in Mandatory Palestine." That sentence now sits in a paragraph that opens with Zionism as the origin.

**Direction.** Rejection is mostly kept, but it stops being the first cause.

### Rank 2. M1 Causal re-anchoring (11/71 vs 3/20; sub-type a: 7/71 vs 0/20)
**Sub-types.**
- (a) The origin of the conflict moves from "began in the mid-20th century", or from "the simultaneous rise of Zionism and Arab nationalism", to a single originating agent: Zionist settlement in the late 19th century.
- (b) A proximate event gains an earlier prior cause that is an action of the other party.

**Examples.**
- *Israeli–Palestinian conflict.* "The conflict has its origins in the rise of Zionism in the late 19th century in Europe, a movement which aimed to establish a Jewish state through colonization in the region of Palestine."
- *Zionism.* "The arrival of Zionist settlers in Palestine during this period is widely seen as marking the start of the Israeli–Palestinian conflict."
- *Blockade of the Gaza Strip.* "date to the early 1990s".

**Comparison.** Sub-type (b) appears in comparison articles too (Tigray war, Kashmir conflict, Turkish invasion of Cyprus). Sub-type (a) does not.

**Time anchor shift.** The anchor moves from 1947/48 to 1882–1897. 1917 is kept but reframed: the Mandatory Palestine lead adds "The declaration effectively overrode the emerging principle of self-determination for the territory's existing Palestinian Arab population."

### Rank 3. M9 Toponymic and temporal anachronism management (12/71 vs 2/20)
**What changes.** Pre-state actors are relabelled by movement rather than by the later state. The pre-1948 land is relabelled.

**Examples.**
- *Nakba*, first-sentence edit of 2026-07-06. "by Israel" becomes "by Zionists". The edit summary reads: "more precise: [[Plan Dalet]], for example, was executed before the declaration of May 14".
- *Jewish history.* "emigration back to Israel" becomes "emigration to Ottoman Syria ... in Palestine".
- *Old Yishuv.* "southern Syrian provinces" becomes "region of Palestine".

**Projections also created.**
- *Demographic history of Palestine (region).* "Mandatory Palestine (1920-1948) since at least the 12th century AD"
- *History of Israel.* The lead now opens with "prehistoric African migrations and the Natufian culture".

**Net drift.** "Palestine" is becoming the default name for the land before 1948. There is one swap the other way: Second Aliyah changes "Palestine" to "the Land of Israel".

### Rank 4. M5 Arab demographic-majority anchor (9/71 vs 2/20)
**What changes.** Palestinian belonging is asserted through numbers, not through the word "indigenous". Examples: "an overwhelming Arab majority" (Israel; Balfour Declaration), "approximately 11% Jewish, 9% Christian Arab, and 78% Muslim Arab" (Mandatory Palestine), and the partition land-versus-population shares (1948 Arab–Israeli War).

### Rank 5. M8 Suffering slotting and pairing
**Counts.** Jewish harm added in the motive slot: 7/71 vs 0/20. Palestinian harm added in the consequence slot: 11/71 vs 5/20, where the comparison cases are victim-detail expansions.

**Story grammar.** The modern story now runs: persecuted Jews (motive) -> colonising movement (action) -> Palestinian dispossession (consequence).

**Examples.**
- Motive slot: "fleeing The Holocaust" (Haganah); "stimulated by pogroms" (First Aliyah).
- Pairing added: "133 Jews and 116 Arabs were killed" (Western Wall).
- Pairing removed (History of Israel): the 2021 sentence paired "an exodus of Arabs" with "a subsequent Jewish exodus". It becomes "significant regional displacement".

### Rank 6. M4 Jewish continuity split by period (removed/attributed 6, strengthened 7, out of 71; vs 3/20 analogues)
**Modern-political leads cut or re-attribute the link to the land.** Examples:
- Zionism's first sentence goes from "re-establishment" to "establish". An attempt in 2024 to restore "re-establishment" was reverted.
- "Jewish presence in the region has persisted to a certain extent over the centuries." is deleted (Israel).
- "regarded by the Jewish people as their ancestral homeland" becomes "Zionists viewed ... as the Jewish ancestral homeland" (Arab–Israeli conflict).

**Antiquity and religion leads harden the link.** Examples:
- Homeland for the Jewish people now begins "since the destruction of the First Temple and the Babylonian exile".
- Kingdom of Israel goes from a skeptical consensus to "ongoing academic debate".
- Bar Kokhba Revolt: the renaming intent goes from "is disputed" to stated fact.
- Western Wall: the earliest attestation moves from the 17th to the 10th century.

### Rank 7. M2 Colonial genus in the definition (first sentence 3/71 vs 0/20; any colon* gain 8/71 vs 4/20)
- The rate of colonial vocabulary gain is **not** distinctive. Comparison articles on indigenous and settler topics gained it too (Native Americans in the United States, Aboriginal Australians, Turkish invasion of Cyprus).
- What is distinctive is placement in wikivoice in the protagonist's definition. Examples: "through colonization in the region of Palestine" (Zionism) and "also called Israeli colonies" (Israeli settlement).

### Rank 8. M6 Voice hardening of contested labels (hardening 10/71 vs 4/20; softening 4/71 vs 2/20)
- Examples: "Allegations have been made ..." becomes "The Gaza genocide is ..."; "some historians ... others dispute" becomes "Scholars widely describe the event as ethnic cleansing".
- This is general practice in mass-atrocity articles (Armenian genocide: "concurring with the academic consensus"). It is not distinctive by rate.

### Rank 9. M3 Perpetrator specification (11/71 vs 4/20)
- Examples: "by Zionists" (Nakba); "supported by the Haganah and Palmach" (Deir Yassin massacre); the Ben-Gurion biography adds "the expulsion and flight of a majority of the Palestinian Arab population".
- Comparison genocide articles sharpen perpetrators too (CUP and Talaat in the Armenian genocide; Chen Quanguo for the Uyghurs). Not distinctive by rate.

### Rank 10. M10 Genus re-classification and displacement (genus change 15/71 vs 5/20; displacement about 20/71 vs about 6/20)
- **General Wikipedia style.** Replacing rather than appending, and rewording the genus, is common everywhere.
- **The topic-specific content of the swap:**
  - Zionist and Israeli subjects gain colonial or crime genera.
  - Palestinian armed groups, and also Lehi, lose violence words from their first sentence. Hamas loses "militant". The PLO loses "violence aimed at Israeli civilians". Lehi loses "used terrorist means".
  - Israel's achievement list and the poll and peace-process material in Israeli–Palestinian conflict are displaced by occupation, apartheid and genocide material.

### Not topic findings
- Updating to recent events (ceasefires, the 2025–26 wars, Hamas disarmament in July 2026) and compressing leads both appear at a similar rate in comparison articles (Tigray war, History of South Africa, Kashmir conflict).
- Adding causal backstory (M1b), perpetrator detail (M3), voice hardening (M6) and victim detail are all also visible in comparison articles.

## 4. KPIs

| KPI | Move | Unit | Procedure (short) | Automatable |
|---|---|---|---|---|
| origin_anchor_year | M1 | article pair | Year named in the origin sentence, B minus A | partly (regex cue plus year; LLM confirms) |
| originating_agent | M1 | article pair | Actor shown as initiating: Zionist / Arab / British / shared / none | LLM |
| prior_cause_inserted | M1 | article pair | New earlier action by the opposing party placed before the start event | partly |
| colonial_genus_first_sentence | M2 | first sentence | colon* applied to the subject, not attributed; count 0->1 switches | yes |
| colonial_token_delta | M2 | pair, per 1,000 words | Token count change | yes |
| agented_harm_ratio | M3 | harm clause | Share of harm clauses with a named agent, by victim group | partly (parse plus LLM) |
| perpetrator_scope | M3 | event article | Widest perpetrator named: faction / mainstream organisation / state or movement | LLM |
| jewish_continuity_claims | M4 | pair | Count of continuity claims, wikivoice vs attributed, split modern vs ancient | partly |
| return_link_present | M4 | first sentence | re-establish / return / restore / repatriate present | yes |
| pre1948_majority_mentions | M5 | pair | Pre-1948 population composition statements and which group is the majority | yes (light LLM check) |
| indigeneity_term_by_group | M5 | occurrence | "indigenous/native" applied to Jews / Palestinians / generic; voice | partly |
| label_voice_score | M6 | label occurrence | 2 assert, 1 consensus, 0 attributed, -1 alleged; mean B minus mean A, by target | partly |
| first_sentence_assertion_flip | M6 | first sentence | accusation framing <-> definitional "is" | yes |
| rejection_position | M7 | pair | absent / first cause / after a prior cause / with motive | partly |
| flight_cause_list | M7 | pair | Share of Arab-agency causes in lists of causes for the 1948 flight | LLM |
| suffering_slot_counts | M8 | harm mention | group x slot (motive / consequence / standalone) | LLM |
| paired_suffering_sentence | M8 | sentence | Both groups' harm in one sentence | partly |
| pre1948_actor_label | M9 | actor mention before May 1948 | state label vs pre-state label | partly |
| pre1948_land_label | M9 | place mention | Palestine / Eretz Israel / Ottoman Syria / Israel | partly |
| projection_created | M9 | pair | Later polity name applied to an earlier period | LLM |
| first_sentence_genus_class | M10 | first sentence | Head noun phrase class transition, by subject side | partly |
| proposition_retention | M10 | pair | Dropped / retained / new propositions; displacement index | partly (embeddings plus LLM) |

For masked pairs, give the LLM coder versions A and B without dates. All "slot", "agent" and "voice" codes should be done per clause, with the clause quoted, so they can be audited.

## 5. Expected but not found
- **Deletion of the Arab rejection of partition.** Mostly not found. It is kept (Palestine, 1948 Arab–Israeli War) and even newly added (Israeli–Palestinian conflict). What changes is its place in the causal order.
- **Deletion of the Jewish exodus from Arab lands.** Not found. It is kept in Israel, 1948 Arab–Israeli War and Mizrahi Jews. Only History of Israel merged it into "regional displacement".
- **"Indigenous" applied to Palestinians in wikivoice.** Rare. In my sample, "indigenous" in Zionism and Zionism as settler colonialism appears mainly in an *attributed* frame for Jews ("repatriation of an indigenous people", in advocates' and critics' voice). Palestinian belonging is carried by demography (M5).
- **A Holocaust lead linked to Israel or the Nakba.** Not found. The Holocaust lead stayed Jewish-centred, with tighter wording.
- **Large reframing of the Balfour Declaration lead.** Not found. The only substantive change is the "overwhelming Arab majority" descriptor.

## 6. Surprises
1. **Bidirectional continuity (M4).** The ancient Jewish past is asserted more firmly in 2026 (temples, kingdom historicity, Bar Kokhba, Western Wall), while the modern bridge from that past to Zionism ("re-establishment", "return", "long connection") is cut. Two stories now coexist: a deep Jewish antiquity, and a modern colonial origin, with the link between them removed from the narrator's voice.
2. **Suffering is re-slotted, not removed (M8).** Both groups' suffering is more present than in 2021. Jewish suffering is now the motive for migration; Palestinian suffering is the consequence of Zionist action.
3. **Anachronism edits cut both ways (M9).** Some are careful corrections ("by Israel" to "by Zionists" because Plan Dalet predates 14 May). Others create new projections ("Mandatory Palestine" for the 12th century; "history of Israel" starting with the Natufians).
4. **Violence words are removed from the first sentence of armed groups on both sides (M10):** Hamas, PLO, Lehi. The Irgun lead keeps and expands "terrorism", now "against Palestinian Arabs".
5. **Comparison articles move the same way on generic frames.** Native Americans in the United States (biological warfare, genocide, "European settler colonizers"), Turkish invasion of Cyprus (ethnic cleansing, settler colonialism) and Aboriginal Australians (colonisation, continuity) gained similar vocabulary. A pure lexicon count would therefore partly measure a Wikipedia-wide turn toward colonial and atrocity framing. The topic-specific signal is in story order (M1, M7), naming (M9), demography (M5) and slotting (M8).
