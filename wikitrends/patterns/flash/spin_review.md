# Spin-risk review: both editions (2026-11-09)

Reviewers: political-communications analyst and senior Israeli news editor.
Inputs:
- the flash edition (`page_flash_template.html`, `build_flash.py`, v3 build);
- the research edition (`page_template.html`, `build_page.py`), story and evidence-room tabs.

Binding rules: `qa/MUSTFIX_owner.md` and `flash/messaging_check.md`. These require exact quotes, no new numbers, the hostage and "undone" scopes, no "on both sides", no "the world reads first", and no unanchored superlatives.

**The owner's concern.** Nothing in the report should be easy for Benjamin Netanyahu or his camp to turn to his benefit. Four lines to watch for:
- "even Wikipedia proves the whole world is against us, so only I can protect you";
- "the report shows criticism of my government is biased, so it can be ignored";
- "the Netanyahu finding is personal persecution";
- "the report vindicates my policies".

**Hard limit.** Everything stays true. Wording-only fixes (kind **a**) are applied. Fixes that remove or downplay a true finding (kind **b**) are listed as recommendations for the owner and are not applied.

Rating scale: 1 = negligible, 5 = a ready-made talking point.

## The scope line (added to both editions)

Nothing in either edition said what the report does not judge. The closest line was "This measures what Wikipedia says, not whether it is true", and it sat at the bottom of the flash and in the trust box of the research edition. That gap is the root of hooks H1, H4 and H6: a reader, or a campaign, can present a study of wording as a verdict on the war.

- **Flash** (`header.hero`, `p.fl-scope`, directly under the 150-tile picture): "This report measures how the wording of the core articles people read changed, not whether it is true, and does not assess the conduct of the war or of any government."
  - This one sentence replaces the old closing honesty line ("This measures what Wikipedia says, not whether it is true. We follow the core articles that carry the narrative and that people actually read."). Both its parts are kept, now up front.
  - The tier slide's caption still says "The change sits in the core articles people read…".
- **Research** (`p.scope`, "What this covers"): "This report measures how an encyclopedia’s wording changed, not whether it is true, and does not assess the conduct of the war or of any government."
  - The trust box H2 ("This study measures what Wikipedia says, not whether it is true.") stays as it is.
- **Build guard.** `build_flash.py` now asserts that the phrase "does not assess the conduct of the war or of any government" is in both editions.

## Hooks

Status key: **A** = wording fix applied in both editions where the text exists; **R** = content recommendation only (see the next section); **—** = no change needed.

| # | Where | Exact text (before) | How his camp could spin it | Risk | Fix | Status |
|---|---|---|---|---|---|---|
| H1 | **Netanyahu finding.** Flash: card 5, carousel `#car1` slide "Israel and Netanyahu" (`.fl-pair`, caption `p.cp`). Research: `#charge` (`#chargeH`, the Netanyahu blockquote label). | Flash caption: "Israel’s own article adds a denial in the next sentence. Netanyahu’s adds none." Research H2: "Two of the most-read articles now state genocide as fact. Netanyahu’s adds no denial." Label: "Benjamin Netanyahu, opening section, now · no denial" | "Wikipedia singles me out by name and won't even print my side; this is persecution of me, and of you through me." "Netanyahu's adds none" also reads as if *Netanyahu* failed to deny, and it makes him the grammatical subject of the finding. | **5** | Present it as a finding about the encyclopedia's voice and attribution, with the encyclopedia as the subject, Netanyahu not personalised, and no echo of "persecution". Flash caption: "The Israel article reports the denial in its next sentence; the Netanyahu article reports none." Research H2: "Wikipedia now states genocide in its own voice in two of its most-read articles, and reports Israel’s denial in only one." The label gains "Wikipedia’s own voice", matching the Israel card. The quote now ends with its period, as stored (messaging F9). Every fact stays: the quote, "no denial", the bottom line naming both articles and "only Israel’s adds a denial", and the tile tooltip. "In its own voice" replaces "as fact" in the H2 only. It is the page's own definition, and it cannot be read as *the report* calling genocide a fact. | A (+ R1, R2) |
| H2 | **View-count bar.** Flash: close, `figure.fl-score` `#whyK` + `ul.fl-bars`. Research: evidence room `#reach` (prose). | "**Why it matters.** These lines sit at the top of the most-read pages that changed (views, past 12 months): Benjamin Netanyahu 7.0 million …" | "The most-read target of this campaign is me: 7 million people a year are being told I committed genocide." "Why it matters" plus the leader's name in the first and longest bar makes it about him. Also imprecise: the flash shows no then/now line for Netanyahu or Palestine, so "these lines" is not accurate for two of the five bars. | **4** | "**Reach.** The most-read pages whose opening sections changed (views, past 12 months):". This drops the stakes framing and fixes the "these lines" imprecision (messaging F11 wording kept: "most-read pages that changed"). The numbers and the descending order are unchanged. | A (+ R3) |
| H3 | **The close.** Flash: `#close` eyebrow and `#whyK` label. | "What the world reads now" · "Why it matters." | The "whole world against us" frame almost verbatim: the world reads this, and it matters because the world is turning. | **4** | Eyebrow: "What the openings say now". "Why it matters" is replaced as in H2. The close H2 (the then/now quotes) is unchanged. | A |
| H4 | **The asymmetry card.** Flash: card 5 eyebrow and `#c5H`. | Eyebrow "The charge, both ways". H2: "Wikipedia says genocide in Gaza is “carried out by Israel.” Of genocide on October 7, it says “Some have alleged.”" | "Double standard: our genocide is fact, theirs is 'alleged'. The world holds Jews to a different rule; only I stand up to it." This is a true finding, and the strongest emotional hook in the flash. | **4** | Eyebrow: "The charge, two voices". This names what is measured (voice and attribution), not a two-sided contest. The H2 is exact quotes and stays. The scope line now sits on the first screen. | A (+ R4) |
| H5 | **ArbCom / outside influence.** Flash: card 6's last line (`p.fl-next`), card 7 `#c7H` and body. Research: `#organised` bottom line. | "Who edits this topic? Wikipedia’s own arbitrators looked." → "Wikipedia’s arbitrators found that outside actors are “heavily invested in influencing” its coverage of this topic. They named no side." Research: "Neither finding names a side." | Placed after five one-way cards, "outside actors" becomes "foreign enemies (Qatar, Iran, the left) did this to us". The question "Who edits this topic?" sets up exactly that answer. | **4** | Flash transition: "Wikipedia’s arbitrators have ruled on conduct in this topic." (no "who did it" setup). H2: "Wikipedia’s arbitrators found outside actors “heavily invested in influencing” its coverage of this topic. They named no side or country." The finding's full text, quoted from `guard/arbcom_named.md`, names neither. Body: "That is camp voting, not proof of coordination; we did not code which side each group took, nor tie either finding to the edits above." Research bottom line: "Neither finding names a side or a country, and we do not link either to the edits in this report." This states the report's own practice (MUSTFIX 11). Quotes, votes, dates and the Ïvana clause are unchanged. | A (+ R5) |
| H6 | **No statement of what is not judged.** Both editions, top of page. | (missing) | Two opposite misuses, both convenient: (i) "even this study says Wikipedia is biased, so the genocide charge is a libel and criticism of my government's conduct can be dismissed" (deflection or vindication); (ii) "the report is a genocide indictment by the back door, part of the campaign against us". | **5** | The scope line (above). | A |
| H7 | **"Israel’s own article".** Flash: `h1`, "In short" (`p.fl-dinner`). Research: `h1`. | "Now Israel’s own article does." · "now Israel’s own article says, in Wikipedia’s voice, …" | "Even *our own* page has been turned against us." It is also ambiguous: it can be read as an article written by Israel. | 2 | "Now the article on Israel does." · "now the article on Israel says, …". The same fact, without the betrayal note. | A |
| H8 | **Hostage headline, research.** `#o7H`. | "Its articles on Israel and Hamas do not mention the hostages." | "Wikipedia erased our hostages." It also overstates (messaging F3: only the *opening sections* are measured). Once the camp debunks it, it can wave away the whole report. | **4** | "The opening sections of its Israel and Hamas articles do not mention the hostages." This is the scope the data supports. The flash card 3 wording was already scoped ("In 107 versions, it has never mentioned the hostages", about the first sentence, with sentence 9's “251 …” quoted below). | A |
| H9 | **"Moved Israel’s way".** Research `#agH`. | "Some lines moved Israel’s way: …" | It casts the study as a scoreboard between sides, with Israel as a team the report keeps score for, and it invites "see, the few fair edits are the ones that favour us". | 3 | "Some lines moved the other way: …" (as the flash already says). | A |
| H10 | **"The score."** Flash close, `#scK`. | "**The score.** For every critical term taken out …, almost four went in." | The game metaphor: "4 to 1 against us". It feeds the siege frame. | 3 | "**The count.**" The ratio sentence and both bars are unchanged. | A |
| H11 | **"The world reads first".** Research evidence room `#reachH` and its bottom line. | "The articles the world reads first on Israel changed; the long tail did not" · "the pages the world reads first on Israel" | "The world" frame again, and an unanchored superlative already vetoed for the flash. | 3 | "The core, most-read articles on Israel changed; the long tail did not" · "the most-read pages on the subject". | A |
| H12 | **"Not shown: Israeli government editing".** Research evidence room, `#orgRec` "More" list. | "Israeli government Wikipedia editing in 2021 to 2026: no reputable report found." | "The study clears the government: no Israeli influence; only the other side." | 2 | It gains ", which is an absence of reports, not a finding that none took place." This is the same evidential status the page states elsewhere ("“Not detected” means the test could not see it"). | A |
| H13 | **Hero H1.** Both editions. | "Before the war, no top article charged Israel with genocide. Now [the article on Israel] does." | "Since we went to war to defend ourselves, the world turned on us." The H1 is accurate, glossed ("top article") and the owner's chosen line. | 3 | Only H7's "own" is changed. The scope line now sits on the same screen. | — |
| H14 | **"What lasts" card.** Flash card 6 `h2` and carousel `#car2`. | "Since September 2025, 10 edits tried to make the Gaza genocide sentence attributed again. Each was gone within 45 minutes." | "Any defence of Israel is erased in minutes: a rigged system." | 3 | It is already balanced on the page: "resistance movement" was gone the next day, "militant" came back three times, and the card states "These are four first sentences …, not the whole subject … no faster". No change. | — |
| H15 | **"In short".** Flash `p.fl-dinner`. | "… and, in every copy we hold, the Israel and Hamas opening sections do not mention the hostages." | The closing emotional note: "they forgot our hostages". It is accurate and scoped. | 3 | Only H7. | — (R6) |
| H16 | **Timing.** Flash card 6 `#kCap`; research `#after`. | "13.7 new critical terms a week, against 3.8 …" | "They punished Israel for defending itself." | 2 | Already "Timing gives a date, not a cause." / "Timing does not prove cause." | — |
| H17 | **"Hebrew, the exception".** Flash `#car1` slide 5; research `#crosslang`. | "Hebrew’s Gaza war article does not state the charge." | "Only our own Wikipedia tells the truth." It is tagged "exploratory" and is a contrast, not a verdict. | 2 | No change. | — |
| H18 | **Ïvana clause.** Flash card 7, research `#organised`. | "the account Ïvana was banned “for off-wiki misconduct …”" | It could be paired with press reports to suggest "their" side's misconduct. The decision names no side, and neither edition implies one. | 1 | No change (owner exception, MUSTFIX 11). | — |

I searched both editions for "blood libel", "lies", "propaganda", "hostile", "enemies", "against us", "whole world", "persecut", "vindicat" and "exonerat": none appear. "Foreign" does not appear in either edition. "Outside actors" appears only inside the ArbCom quote.

## Content recommendations (NOT applied; the owner decides)

| # | Recommendation | What it would do | Trade-off |
|---|---|---|---|
| R1 | **Netanyahu, flash:** show the Netanyahu sentence next to the five *attributed* charges in the evidence (Palestine, Gaza Strip, Israeli–Palestinian conflict, IDF, Gaza–Israel conflict), or move it out of the flash carousel into the evidence link only. | It puts the encyclopedia's attribution standard at the centre, not the man. | It downplays the single most newsworthy voice finding. The flash would lose the clearest example of "stated as fact with no denial". Moving it looks like protecting him. **We advise keeping it**, with the H1 wording. |
| R2 | **Netanyahu, both editions:** add the evidence room's own context line: "Stating genocide in Wikipedia’s own voice is common on atrocity articles (of 11 we checked by hand, an anecdote, not a sample, 4 did so in 2023 and 9 do now); Gaza differs in speed and reach, not in the label itself." | It undercuts the persecution story ("only us"). The numbers are already printed in the research edition. | It costs about 2 lines (the flash is at 9.499 of 9.5), and it is an anecdote, not a sample. It can also be read as "Wikipedia does this to everyone", which softens the Gaza finding. |
| R3 | **View bars:** order them Israel, Palestine, Zionism, Hamas, Netanyahu (by topic, not by views), or drop the Netanyahu bar from the flash. | It ends the "most-read target is me" image. | Descending order is the honest default, and reordering or dropping the top bar would look like hiding the largest number. **We advise keeping the order**, with the H2 wording. |
| R4 | **Asymmetry card:** add, in card 5, the own-voice facts about October 7 already on the page ("massacring civilians in 21 communities"; 1,195 killed in the Gaza–Israel conflict sentence, in Wikipedia's own voice). | It shows that the encyclopedia also states the October 7 killings as fact. That blunts the "double standard on everything" spin. | It dilutes a deliberate juxtaposition (messaging check: A's strongest card), adds length, and partly repeats card 3. |
| R5 | **ArbCom card, flash:** fold card 7 into one closing line ("Wikipedia's arbitrators found outside actors heavily invested in influencing the topic's coverage, and named no side or country"), as the messaging check allowed if over budget. | It removes the one-card "who did this" beat that follows the one-way cards. | It loses the voting-camp count and the Ïvana clause (an owner exception), and leaves "who edits this?" less answered. The messaging check warned that silence invites worse speculation. |
| R6 | **"In short":** end on a fuller hostage sentence: "…the Israel and Hamas opening sections do not mention the hostages; October 7’s ninth sentence gives the 251 taken as hostages." | It stops the closing line being read as "Wikipedia erased the hostages". | It adds a line (over the flash cap unless something else is cut), and it softens the dinner sentence that editors A and B built. |
| R7 | **Card order:** do not place the ArbCom card directly after the "How it got there" card, which ends on reverts and timing. Put it after the close's score block, or before card 1 as context. | It weakens the implied cause-and-effect between "edits stuck" and "outside actors". | It breaks the what → how → who arc that the messaging check chose. |

## Measurements after the fixes

Playwright Chromium, web fonts loaded (`document.fonts.ready`; 12 faces loaded in the flash, 14 in the research edition), every lazy piece drawn, carousels at rest.

| Edition | iPhone 13 390×844 | 1280 | Cap |
|---|---|---|---|
| Flash | **9.499** screens (v3: 9.485) | 9.60 | ≤ 9.5 |
| Research, story tab | **18.967** screens (before: 18.724) | 14.10 | ≤ 19.3 |

How the flash stayed within its cap:
- the scope line replaced the closing honesty line;
- card 7's H2 drops "that … are" around the exact quote (the quoted words are unchanged);
- the scope line uses a line-height of 1.35.

Smoke tests, light and dark, phone and 1280:
- **Flash:** the full v3 smoke suite, which also covers reduced motion. Result: 0 console errors or warnings, no horizontal overflow at rest or after interaction, 0 failures.
- **Research:** both tabs, plus a language-square tap. Result: 0 console errors and 0 overflow in the story tab, the evidence tab and back.

Build assertions:
- All existing assertions pass: 74 quoted strings, 50 numbers, the vetoes, the RTL runs, K_STEPS, #against and ArbCom.
- No assertion needed changing.
- New guards in `build_flash.py`:
  - the scope line is in both editions;
  - "the world reads", "israel’s way", "why it matters", "the score." and "israel’s own article" are absent from both editions' visible text.

Wrapped builds, each beginning with DOCTYPE, charset and the viewport meta: `scratchpad/spin/flash.html` and `scratchpad/spin/research.html`.
