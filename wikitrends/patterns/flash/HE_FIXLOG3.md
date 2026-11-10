# Flash edition: Hebrew fix log 3 (owner requests: "armed incursions", the hostages moment)

**Build:** `cd wikitrends && python build_flash.py --bilingual OUT.html`. The single-language builds (`build_flash.py OUT.html`, `build_flash.py --lang he OUT.html`) still run every check. The research edition is byte-identical (`build_page.py` output compared with `cmp` before and after each step).

**Standards:** `HE_PROOF_1.md` (idiom, grammar, RTL, punctuation, no italic, no-break space in dates, no English in the UI) and `HE_PROOF_2.md` (fidelity of agency, modality and attribution; no sharpening or softening).

## 1. "armed incursions": «פשיטות חמושות» replaces «חדירות חמושות»

**Decision: «פשיטות חמושות».** The owner's recommendation holds; I found no fidelity reason against it, and two reasons for it.

| Candidate | Sense in Hebrew | Verdict |
|---|---|---|
| «חדירות» (v1–v3) | penetration, crossing in; in news Hebrew also "infiltration" (חדירת מחבלים) | **Out.** It keeps the crossing but loses the hostile, armed, sudden attack that "incursion" names. It reads as a technical or clandestine entry. |
| **«פשיטות»** | raid: a sudden, limited armed entry into another's territory, then out | **Chosen.** It is the dictionary sense of "incursion" ("a hostile entrance into a territory: raid", Merriam-Webster; "an invasion or attack, especially a sudden or brief one", Oxford), and it does not claim more than the English. |
| «פלישות» | invasion | **Out, for fidelity.** It sharpens the English. English Wikipedia itself *removed* "invasion" from this first sentence: the January 2024 copy said "the first invasion of Israel since the 1948 Arab–Israeli War"; the current one does not. Rendering "incursions" as «פלישות» would put back, in our translation, the word the encyclopedia took out. |

**Consequences, all applied:**
- One rendering for "incursion" on the whole page. The event label "Israeli Jenin incursion (July 2023)" changes from «החדירה הישראלית לג׳נין» to «הפשיטה הישראלית על ג׳נין».
- Known collision: "raid" (Israeli raid on Al-Shifa Hospital) is also «פשיטה». This is acceptable: in every place the October 7 phrase is shown, the English original stands beside our translation, and the two events are never on the same line.
- `HE_PROOF_2.md` (row "October 7", glossary row "incursion(s)") chose «חדירה» and reserved «פשיטה» for Al-Shifa. That verdict is superseded by this decision. `HE_PROOF_2.md` issue 15 (Spanish "un ataque de comandos" = «מתקפת קומנדו», not «פשיטת קומנדו») stays right on its own ground: "ataque" is מתקפה.
- The original English stays visible everywhere, exactly as before (`.he-o` under the H2, the LTR pair in the what-changed line and the hero row, `(armed incursions)` in the lane label, `<bdi lang="en">` in the reach key).

**Every place changed (`flash_i18n_he.json`):**

| Place | Before | After |
|---|---|---|
| Card 3 H2 | «…כתוב היום ״חדירות חמושות מתואמות״…» | «…כתוב היום ״פשיטות חמושות מתואמות״…» |
| Card 3 what-changed pair | «״…מתקפות מתואמות״ ← ״…חדירות חמושות מתואמות״» | «״…מתקפות מתואמות״ ← ״…פשיטות חמושות מתואמות״» |
| Hero stack, October 7 row | «״מתקפות מתואמות״ ← ״חדירות חמושות מתואמות״» | «״מתקפות מתואמות״ ← ״פשיטות חמושות מתואמות״» |
| October 7 lanes (label, aria) | «״חדירות חמושות״ (armed incursions)»; «…חדירות חמושות, הימים…» | «״פשיטות חמושות״ (armed incursions)»; «…פשיטות חמושות, הימים…» |
| Reach key (critical wording) | «“armed incursions” (חדירות חמושות)» | «“armed incursions” (פשיטות חמושות)» |
| Scrolly event labels (library) | «7 באוק׳: ״מתקפות״ ← ״חדירות״»; «7 באוק׳: ״חדירות חמושות״» | «… ״מתקפות״ ← ״פשיטות״»; «… ״פשיטות חמושות״» |
| Language-grid coding note (en, October 7) | «״סדרה של חדירות חמושות מתואמות״» | «״סדרה של פשיטות חמושות מתואמות״» |
| Event label, Jenin | «החדירה הישראלית לג׳נין (יולי 2023)» | «הפשיטה הישראלית על ג׳נין (יולי 2023)» |

**Share images and lab chrome:** the share images read their text from the page (`shSpec`), so they change with it. The Data lab's Hebrew chrome (`lab/lab_flash.py`) never carried the phrase; it is checked against the new vetoes all the same.

**Locks (`flash_he.py`):**
- `HE_VETO` gains «חדירות», «החדירה הישראלית» and «פלישות חמושות». The vetoes run over the visible Hebrew page, the library and figure strings, the overlay script, the event labels, the grid notes and the lab chrome.
- New assertions: the H2, the pair, the hero row, the reach key, the lane label, the event label and the grid note each carry «פשיטות».
