# Flash edition: messaging and comprehensiveness check (round 1)

Checker: messaging/comprehensiveness agent, with veto power. I read both proposals (editor_A.md, editor_B.md) against PLAN.md, qa/MUSTFIX_owner.md, SYNTHESIS.md, angle/OCT7.md, zionism/CODES.md, langs/langs.json, angle/chart_data/*.json, data/leads.json, data/mass2.json and data/mass2_leads.json.gz. I also checked the research-edition build (scratchpad/final/index.html). I rendered it headless at 390 px, because several numbers, such as the #ziFig phase texts, exist only after the JS runs.

Status keys: **OK** = faithful as written. **FIX** = keep it, with the corrected text given. **VETO** = must not appear in the flash edition.

Two facts that I could not take from the page and checked in the stored data:
- **Latest stored copies:** in the 5 Nov 2026 crawl (data/mass2.json, `now`), Hamas is at rev 1383083378 (31 Oct 2026 22:20 UTC), October 7 attacks at rev 1383458606 (2 Nov 2026), Israel at rev 1383765294 (4 Nov 2026) and Netanyahu at rev 1383749085 (4 Nov 2026). en.wikipedia.org is blocked from this sandbox (proxy 403), so I could not check any live text.
- **View counts:** the sum of the last 12 stored months (Nov 2025 to Oct 2026) in mass2.json gives Netanyahu 6,987,725, Israel 4,617,834, Palestine 2,429,310, Zionism 1,805,729 and Hamas 1,334,167. These match 7.0M, 4.6M, 2.4M, 1.8M and 1.3M, which the page labels "Views are for the last 12 months".

---

## 1. FIDELITY

### 1a. The flagged items

| # | Item | Verdict | Finding and correct text |
|---|---|---|---|
| F1 | "undone within a day" scope | **FIX (both editors)**. VETO any subject-wide form. | The page says so explicitly: "Across the subject, no faster undoing… reverts of edits that removed critical terms came no faster than reverts of edits that added them (median 1.13 hours against 0.84; 227 and 260 reverts). The faster undoing above is a Zionism result, not a pattern across the subject." So any "critical wording lasts, the opposite is undone within a day" headline must name Zionism's first sentence, or name one word in one article with its dates. **Also, "gone" is not "undone".** The page defines the 64/70 vs 47/78 measure as "‘Gone within a day’ means the next edit of any kind came the same day or the next". That is not a revert. Only the #ziFig phase-3 text ("“colonial” taken out and put back 10 times … Each removal was undone within a day", Nov 2024 to Aug 2026) and "37 of the 41 removals [of colonization] we can check" were undone. Never write "64 of 70 were undone"; write "gone within a day". |
| F2 | One duration measure only (MUSTFIX 9) | **FIX**. | Neither editor mixes days live with stance-regime days. Good. But A card 6 and B card 3 put two "within a day" measures with different definitions side by side: 64/70 "gone" (any next edit) and the ziFig "undone" (put back). **Rule for the flash: on Zionism, use the ziFig fact plus 37/41 (both are "undone"). Drop 64/70 vs 47/78 from the flash.** If the EIC insists on keeping it, use the page's exact sentence with "gone", never on the same line as "undone", and never with "about N times as long". No days figure (336/38, 650/74) anywhere in the flash. The per-word lifespans (45 minutes, about 2.4 hours, about an hour) are counts of a single wording's time live, not a second "rate" measure. They are OK. |
| F3 | Scope of every hostage line | see 1b | The data supports three exact scopes and no others. (i) **October 7's first sentence:** "never, across 107 versions". (ii) **The Israel and Hamas opening sections:** "none, at every snapshot since 2021" (four copies: Jan 2021, Jul 2023, 1 Oct 2026, now). (iii) **The October 7 opening section DOES name the hostages**, in sentence 9: “251 Israeli and non-Israeli civilians and soldiers were taken as hostages to the Gaza Strip”. "The articles on Israel and Hamas", "at all" or "never" without a scope all overstate. The fixes are listed per line below. |
| F4 | 223/61 vs 125/73 | **OK**, with wording | The page says: "Critical terms in opening paragraphs, 2021 to now: topic articles, 223 in, 61 out; comparison articles (other countries, conflicts and religions), 125 in, 73 out". 223/61 = 3.66, so "almost four" holds. 125/73 = 1.71, so "fewer than two" holds. A's closing line is OK. B card 8, "On other countries' and conflicts' pages", drops "religions". FIX: "on comparison pages (other countries, conflicts and religions), fewer than two." |
| F5 | "Several countries" | **OK to use, with a date stamp and the caveat** | It still stands in the latest stored text. Hamas `now` = rev 1383083378 (31 Oct 2026). The 5 Nov 2026 crawl found no later Hamas revision, and its lead reads “Several countries have designated Hamas as a terrorist organisation.” (sentence 22 of 23). Live status cannot be checked from here. If shown, label it "as of our 5 Nov 2026 copy; days old, may be reverted" (the page's caveat). The headline must rest on the position (sentence 5 of 20 in 2021 → 22 of 23 in Oct 2026). That holds with either wording, so A's choice (use the 1 Oct 2026 row) and B's choice (end on "Several countries" with the caveat) are both acceptable. I prefer B's, because the shrinking list is itself a finding, but only with the stamp. |
| F6 | October 7 "Some have alleged … genocidal massacre against Israelis" | **OK** | It is verbatim in both the 1 Oct 2026 (rev 1377629133) and 2 Nov 2026 (rev 1383458606) leads: “Some have alleged that the attack was an act of genocide or a genocidal massacre against Israelis.” Its place is the last paragraph of the October 7 opening section. Its label is ATTRIBUTED. The page's own "What this means" states the asymmetry. |
| F7 | "every edit that tried to put ‘alleged’ back … within 45 minutes"; "terrorist ~2.4 h"; "massacre ~1 h" | **FIX** (alleged); **OK** (2.4 h, 1 h) | The page says: "Since then [26 Sep 2025], 10 edits tried to bring back attribution; each was gone within 45 minutes." The attempts were not all "alleged". The page gives “has been described by most scholars as” and “the alleged ongoing” as examples. **Correct text:** "Since 26 September 2025, 10 edits tried to bring back attribution (“alleged,” “described by most scholars as”); each was gone within 45 minutes." The count 10 IS printed on the page, so A's flag 1 is wrong and "10" may be used. The Hamas line is OK: “Terrorist” was written into the definition five times; the longest lasted about 2.4 hours. **Required counterpart, from the same page sentence group:** “Resistance movement” got in once, on 1 August 2024, and was gone the next day. “Militant” came back three times after October 2023 (1–2 Aug 2024; 19–31 Aug 2024; 12–18 Feb 2025). Without these, the "terrorist" line implies that only one side's words get removed. The massacre line is OK: "In 107 versions of October 7’s first sentence, “massacre” lasted about an hour in all." |
| F8 | Hebrew Hamas quote | **OK** | langs.json, Hamas he s1 latest, rev 43994741 (2026-10): “חַמַאס (בערבית: حماس) הוא ארגון טרור פלסטיני אסלאמיסטי-סוני הפועל גם כתנועה פוליטית.” The stored translation is "Hamas (in Arabic: حماس) is a Palestinian Sunni-Islamist terror organisation that also operates as a political movement." A's text is exact. Note for fairness: Hebrew already said "ארגון טרור" in 2021 (rev 30247104). The Hebrew line is a contrast with English, not a Hebrew change. Never present it as "Hebrew moved". Keep the tag "Other languages · exploratory" and `dir="rtl"`. The Hebrew October 7 quote (rev 44000524) is also exact. |
| F9 | Netanyahu quote punctuation | **FIX: end with a period inside the quote** | The stored text (rev 1383749085) reads: "Netanyahu's government has been orchestrating the Gaza genocide, culminating in the South Africa v. Israel case before the International Court of Justice (ICJ) in December 2023. The International Criminal Court (ICC) issued…" The sentence ends in a period, so quote it as «“Netanyahu's government has been orchestrating the Gaza genocide, culminating in the South Africa v. Israel case before the International Court of Justice (ICJ) in December 2023.”» (as #ev-charge does). The story card's version without the period should be harmonised. Keep the straight apostrophe in "Netanyahu's" as stored, or curl it consistently (a copy-edit choice; it does not change the quote). |
| F10 | "37 of 41 removals of colonization undone" | **OK** (A n/a). **FIX** (B's framing) | The page says: "Almost every removal of “colonization” was undone: 37 of the 41 removals we can check, where both versions of the sentence were kept." This covers the whole period, not "after" the 2024 tug of war. B card 3 writes "After that almost every removal was undone: 37 of the 41". FIX: "Almost every removal of “colonization” was undone: 37 of the 41 we can check." |
| F11 | View counts | **OK**, with a label | 7.0M / 4.6M / 2.4M / 1.8M / 1.3M are verified above (last 12 months). On the page they are "the most-read topic pages whose opening paragraph gained critical vocabulary". B's close calls them "the first lines of the most-read pages on the subject". FIX: "the opening sections of the most-read pages that changed: Benjamin Netanyahu, 7.0 million views in the past 12 months; …". Netanyahu's charge is in his opening section, not his first line. |

### 1b. Every other number and quote, by proposal

**Editor A**

| Where | Item | Verdict |
|---|---|---|
| Screen 0 | H1 “Before the war, no top article charged Israel with genocide. Now Israel’s own article does.” | **OK.** This is the page H1. It needs B's F6 tooltip: "top" = the 150 most-read opening sections on the subject that existed in 2021, checked Jan 2021 and Jul 2023. |
| Screen 0 | Hero quote and “Israel has denied that its actions constitute genocide.” | **OK.** This is the 4 Nov 2026 copy. On 1 Oct 2026 it read “Israel and its allies, including the United States, deny…”; the page notes this. |
| Screen 0 | "since 4 May 2025", "4.6 million … past 12 months" | **OK.** |
| Screen 0 | "Below are six more first lines, then and now." | **FIX:** "Below: the other core articles, then and now." Card 6 is not a first line, and the Israel quote is in the opening section, not the first sentence. |
| Card 1 | #ziSum chips; focus line; "next sentence … as few Palestinian Arabs as possible" | **OK.** Verbatim in rev 1383800290. |
| Card 1 | "“Re-establishment” left for good on 9 July 2024. “Colonization” went back in on 27 August 2026 and has stayed." | **OK.** #ziFig: "Settled 27 Aug 2026 to now … No change to the first sentence in 70 days." |
| Card 2 | Nakba then/now; "Three 1948 articles … ‘Zionists’ or ‘Zionist forces’ … ‘fled or were expelled from Arab states,’ no one is named" | **OK.** Verbatim from the #palestine bottom line. Keep the page's tag "the 2021 version also took a position". |
| Card 3 | "coordinated attacks" (23 Oct 2023) → "coordinated armed incursions" | **OK.** |
| Card 3 | Hostages blockquote ("never, across 107 versions" / "none, at every snapshot since 2021" / sentence 9) | **OK.** The scopes are kept exactly. |
| Card 3 | Rape sentence: Jan 2024 “by Hamas fighters” → now no perpetrator | **OK.** The 2 Nov 2026 copy reads “Numerous sources have reported dozens of cases of rape and sexual assault.” (ends with a period; the 1 Oct copy continued “, but Hamas officials denied the involvement of their fighters.”). |
| Card 3 | “massacring civilians in 21 communities” | **OK.** 2 Nov 2026 copy, sentence 4. |
| Card 4 | Hamas 2021 diff, now text, Hebrew line | **OK** (F8). |
| Card 4 | "sentence 5 of 20 (2021) to sentence 22 of 23 (October 2026)" | **OK.** chart_data/oct7_08: 2021-01-01 "5 of 20"; 2026-10-01 "22 of 23". |
| Card 4 | "“Militant” became “military” on 12 October 2023, five days after the attack." | **OK as a date. FIX for completeness:** add "it came back three times, last in February 2025". Otherwise the card implies a one-way, instant switch. |
| Card 5 | Headline "Wikipedia said “Allegations have been made” that Israel committed genocide." | **FIX.** That is a paraphrase inside a quote frame: the stored text does not say "Israel committed". Use: «In January 2024 Wikipedia said: “Allegations have been made that the 2023 Israel–Hamas war constituted a genocide.” Now: “the ongoing, intentional, and systematic destruction … carried out by Israel.”» |
| Card 5 | Gaza genocide sentence "since 26 September 2025" | **OK.** |
| Card 5 | "Of the 150 most-read opening sections, none charged Israel with genocide before the war; seven do now." | **FIX:** add "that existed in 2021". Also add the page's own split: "two state it as fact (Israel, Netanyahu); five attribute it". Without that split, "seven" next to "stated as fact" overstates. |
| Card 5 | "Netanyahu’s states it as fact, with no denial." | **FIX** (typo): "Netanyahu's article states it as fact and adds no denial." |
| Card 5 | Body "The charge against Israel is stated as fact. The charge about October 7 is “alleged.”" | **FIX:** "stated as fact in the Gaza genocide, Israel and Netanyahu articles", which is the page's exact scope. It is not stated as fact everywhere (five of the seven attribute it). |
| Card 6 | Headline ("alleged" back … 45 minutes; "terrorist" … 2.4 hours) | **FIX** per F7. |
| Card 6 | "Since November 2024, “colonial” was taken out 10 times, and each removal was undone within a day." | **OK.** #ziFig phase 3, Nov 2024 to Aug 2026. Add the end date "to August 2026". |
| Card 6 | "Of 70 own-voice edits that made it less critical, 64 were gone within a day, against 47 of 78…" | **FIX/DROP** per F1–F2. If kept: "In Zionism’s first sentence, of 70 own-voice edits that made it less critical, 64 were gone within a day (the next edit came the same day or the next), against 47 of 78 that made it more critical." |
| Card 6 | Implied frame "what stays and what is undone" | **VETO the unscoped frame.** The card must say it covers these four sentences. It needs the "resistance movement"/"militant came back" counterpart (F7) and the page's line "Across the subject … reverts … came no faster". The card can stay; the generalisation cannot. |
| Closing | "In 2021 / Before the war, these first lines spoke of “re-establishment,” “militant” and “coordinated attacks.”" | **VETO, both versions.** "In 2021" is false for "coordinated attacks", which is from 23 Oct 2023. A's own fix, "Before the war", is ALSO false: “re-establishment” left Zionism's first sentence in June 2021 and was absent before the war, except for two weeks in 2024 (page: "“Re-establishment” left in June 2021, went in and out for two weeks in 2024, and left…"). Replacement: «These first lines once said “re-establishment” (2021), “militant” (2021) and “coordinated attacks” (October 2023). Now they say “colonization,” “ethnic cleansing … by Zionists” and “genocide.”» |
| Closing | Ratio line | **OK** (F4). |
| Closing | Honesty line "…not in the long tail of short pages." | **FIX** to the page's strength: "…while the long tail of short pages barely changed." ("not in" is absolute; the page says "barely"). |
| Carousel A 7 | Hebrew October 7 first sentence; "English: neither, in its first sentence." | **OK.** The current English first sentence has neither "terror" nor "massacre"; "massacring" is in sentence 4. |
| Carousel A 8 | es/pt/ar now state it as fact; "un ataque de represalia" | **OK.** Verbatim (es Gaza war rev 175571073). |
| Carousel A 9 | "‘by Zionist militias’ left its first sentence in May 2025" | **FIX** (an overstated opposite). The page continues: "…and the next sentence names “the Zionist paramilitaries Haganah, Irgun, and Lehi.”" That clause must be on the slide, or the "moved the other way" example overstates. The date is 30 May 2025. |
| Carousel B 1–4 | captions | **FIX** slide 1 per F7. Slide 2 needs "“Resistance movement” got in once and was gone the next day." Slides 3 and 4 are OK. |
| Share card 1 | Footer "Israel’s denial appears in the Gaza genocide opening section's last paragraph." | **OK.** The stored lead has “Israel and its supporters maintain that its actions do not constitute genocide…” in its last paragraph. |
| Share card 2 | dates "Jan 2021 and Nov 2025 (English)" | **OK.** The Hamas wording has stood "since 29 November 2025" (page). |
| Share card 3 | "292 changes … Text as of 5 Nov 2026" | **OK.** |
| Flag 1 | "The count 10 … is NOT printed on the page" | **Incorrect flag.** It is printed ("Since then, 10 edits tried to bring back attribution"). |
| Cut-list note | Hannibal "then" unverified | **Resolved:** chart_data/oct7_06 records Hannibal as "absent" in the 1 Jan 2024 lead. A then/now is anchored: absent (Jan 2024) → “The IDF used the Hannibal Directive on that day, which may have led to at least 13 Israeli civilian deaths.” (2 Nov 2026). This is optional, see §3. |

**Editor B**

| Where | Item | Verdict |
|---|---|---|
| Card 1 | Headline, proof, "4.6 million" | **OK.** |
| Card 1 body | "The Israel and Hamas openings do not mention the hostages." | **FIX:** "In every copy we hold, the opening sections of the Israel and Hamas articles do not mention the hostages." (page wording) |
| Card 2 body | "Seven opening lines, 2021 → today" | **FIX:** "Seven opening lines, then and now, exact and dated." The October 7 and Gaza genocide articles start in 2023/2024. |
| Card 3 | "In June 2024 “colonial” went in 33 times and came out 32 times in six months." | **FIX:** "From June to November 2024, “colonial” went in 33 times and came out 32 times." (#ziFig: 5 Jun 2024 to 27 Nov 2024) |
| Card 3 | 37 of 41 | **FIX** per F10. |
| Card 3 | "64 of the 70 that softened it … 47 of the 78 that hardened it" | **FIX/DROP** per F1–F2. If kept, use the page's verbs ("made it less/more critical", not "softened/hardened") and say "gone", not "undone". |
| Card 4 | Nakba then/now; 1948 Palestine war pair (2023 → now, "about 78% … over 700,000"); "since 6 July 2026, apart from under an hour on 17 July" | **OK.** All verbatim. Label the 1948 Palestine war pair "2023 → now", not "Dec 2021". |
| Card 5 headline | "Its articles on Israel and Hamas do not mention the hostages." | **FIX:** "Its opening sections on Israel and Hamas never mention the hostages." (the page H2 overstates the scope; the article bodies may) |
| Card 5 | Sexual-violence quote ending in a comma | **FIX:** quote the 2 Nov 2026 text: «“Numerous sources have reported dozens of cases of rape and sexual assault.”» |
| Card 5 | "None of those insertions lasted more than about 2.4 hours." | **OK.** Needs the F7 counterpart if it sits in a "what lasts" frame. |
| Card 5 | "In 107 versions, October 7's first sentence never mentions the hostages." | **OK.** |
| Card 6 | Headline (page heading), "13.7 a week against 3.8", the truce, Rafah present tense, the Gaza war dropping "Hamas" in May 2025, "Timing gives a date, not a cause" | **OK.** All verbatim. Keep "a date, not a cause". |
| Card 7 | Headline, Arabic pair, "3 July 2024", Polish "April 2026" (26 Apr), +187 d / +849 d, the Hebrew exception | **OK.** Arabic: rev 67211953 → 76455756. Hebrew: "its Gaza war article does not state the charge … reports only South Africa’s court case". Keep the court reference to that one factual clause (no courts framing). |
| Card 8 headline | "…On other countries' and conflicts' pages, fewer than two." | **FIX** per F4. |
| Card 8 body | "In 217 talk-page votes, four groups of 3 to 6 accounts voted together 89 to 100% of the time, against about half by chance." | **FIX:** "In 217 formal talk-page discussions (requests for comment, moves, deletions)…". They are discussions, not votes. The rest is verbatim. Keep "camp voting, not proof of coordination; we did not code which side each group took". |
| Card 8 | ArbCom finding 10 quote, "January 2025", "15–0" | **OK.** PIA5 decision of 23 Jan 2025. |
| Card 8 | Ïvana clause (finding 16) | **VETO in the flash.** PLAN rule 5 for the flash says "no usernames". It stays in the research edition (MUSTFIX 11 governs there). |
| Card 8 | #net counter "14 found · 2.15 by chance" / "3 found · 0.28" | **OK.** It is verbatim, but it is a third statistic on one card. Drop it from the flash (see §2). |
| Card 8 | "Some lines moved Israel’s way. Since May 2025 the 1948 expulsion’s first sentence no longer names “Zionist militias.”" | **FIX:** add "…; its next sentence names “the Zionist paramilitaries Haganah, Irgun, and Lehi.”" (same reason as A's carousel slide 9) |
| Carousel A 1 | Netanyahu quote | **FIX** punctuation (F9). |
| Carousel A 7 | "moved the other way" slide | **FIX:** as card 8. |
| Carousel C 2 | Spanish quotes | **OK.** Verbatim from the stored latest text (es rev 175571073), so B's F9 is satisfied. |
| Arc / Close | "the denial is now an afterthought or absent" | **VETO** ("afterthought" is the editor's adjective, not a quote). |
| Close | "Israel's denial, where there is one, is the sentence after." | **FIX.** It is true only for the Israel article. In Gaza genocide the denial is in the opening's last paragraph; Netanyahu's has none. Use: "In Israel's article the denial is the next sentence; in Gaza genocide it comes in the last paragraph of the opening; Netanyahu's adds none." |
| Close | "These are not footnotes. They are the first lines of the most-read pages on the subject…" | **FIX** per F11 ("opening sections of the most-read pages that changed"). |
| Close | "The hostages are not in the Israel or Hamas openings at all." | **FIX:** "In every copy we hold since 2021, the Israel and Hamas opening sections do not mention the hostages." (drop "at all") |
| Opening deck | "The encyclopedia the world reads first now says…" | **VETO** "the world reads first" (an unanchored superlative). FIX: "English Wikipedia now says, in its own voice, that Israel ‘began committing genocide.’ In January 2021 its first line on Zionism spoke of ‘re-establishment.’" |
| Honesty line | "…while the long tail of short pages barely moved." | **OK** (this is the best version; use it). |
| Dinner sentence | "…and the Israel and Hamas articles don't mention the hostages." | **FIX** (scope). See §3. |

### 1c. Summary of vetoes
1. **The unscoped "critical wording lasts, the opposite is undone within a day"**, as a frame or headline, in either proposal. It is a Zionism-only result. Across the subject the page says reverts came no faster. "Gone" ≠ "undone".
2. **A's closing headline**, in both its forms. "In 2021 … coordinated attacks" is false (Oct 2023). "Before the war … re-establishment" is false (it left in June 2021).
3. **The Ïvana clause** in the flash (PLAN: no usernames).
4. **B's "afterthought"** and **"the encyclopedia the world reads first"** (adjective framing and an unanchored superlative).

Everything else is OK or fixable with the text given above.

---

## 2. MESSAGE

**The one mental jump.** "The first lines the world reads about us now say colonization, ethnic cleansing by Zionists and genocide in their own voice. The first lines about October 7 and Hamas got softer, and the hostages are not in them."

**Editor A** delivers this faster and harder. Every card is a then/now on a core article, each with one proof element. Its strongest invention is card 5 (the charge both ways): the page's own "What this means" asymmetry, made visible with two quotes of the same size. That is the shock built from juxtaposition that the PLAN asks for. Putting the Hebrew Hamas line next to the English one (card 4) is the second-best image for an Israeli reader. A also correctly splits October 7 from Hamas.
- **What A loses:** the "how". There is no timing or events (it cuts the scrolly the owner loves; MUSTFIX 4 says the events→wording link is "the interesting part"), no mechanism beyond card 6, and nothing about who edits. A reader finishes with "what" and no "how did this happen". A's card 6 is also the one place where it overreaches (F1/F7).

**Editor B** has the better arc (what → how → who), keeps the battles and the languages, and puts the opposite edits inside the scoreboard (MUSTFIX 1–2, done right). But it delivers the jump more slowly. The strongest juxtaposition (the genocide charge both ways) is missing. Card 2 spends a whole screen on a carousel that repeats cards 3–5. It reaches 8.6 screens with 8 cards and 3 carousels, which is too much for "flash".
- **What B loses:** the asymmetry card and the Hebrew–English Hamas mirror. B also leans on statistics (64/70, 13.7/3.8, 14 vs 2.15, 89–100%) where A leans on words.

**Verdict:** A's spine with B's hinge. Use A's six then/now cards, B's timing as one carousel slide (not its own card), and a short version of B's card 8.

**Guarding / voting camps / ArbCom.** Keep a SHORT version. Do not drop it entirely. Without it, the flash raises "who did this?" and leaves the answer to the reader's imagination, which is worse for neutrality than a precise answer. But A's risk is real: placed after six one-way cards, "outside actors are heavily invested" reads as "outside actors did this". Rules for the short version:
- **Placement:** after "What lasts" and before the close, never directly after the genocide-asymmetry card.
- **Two separate facts, each labelled with its source,** with no connective that suggests cause ("so", "because", "behind"): (i) Wikipedia's arbitrators, January 2025: “Outside actors are heavily invested in influencing Wikipedia's coverage of the topic area” (finding 10, adopted 15–0); (ii) our count: in 217 formal talk-page discussions, four groups of 3 to 6 accounts voted together 89 to 100% of the time, against about half by chance.
- **The no-side statement goes in the headline or deck, not the footnote:** "Neither names a side; we did not code which side the groups took."
- **Leave out of the flash:** account names (Ïvana), the network graph, the 14-vs-2.15 counter, the revert-narrowness finding (suggestive) and the press-reported motions.
- **No direction colours** on this card (no blue/amber), so it cannot be read as "this side's camp".
- **Frame it as an attribute of the topic area, not of Wikipedia** (PLAN: "the narrative, not Wikipedia"). One card of about 0.5 screen, no carousel. If the build exceeds 8 screens, collapse it to one line in the close, with the arbitrators' quote and "names no side".

---

## 3. RECOMMENDED SYNTHESIS (8 cards incl. opening and close; about 7.8 phone screens)

Source marks: **[A]**, **[B]**, **[A+B]**, **[chk]** (my fix).

### Opening [A+B]
- **Headline:** Before the war, no top article charged Israel with genocide. Now Israel’s own article does. [A+B, page H1] Add the tooltip on "top article": the 150 most-read opening sections on the subject that existed in 2021, checked Jan 2021 and Jul 2023. [B F6]
- **Proof:** `header.hero .hero-q`, with “began committing genocide” highlighted; under it, “Israel has denied that its actions constitute genocide.” [A+B]
- **What changed:** no genocide charge in the 150 most-read opening sections (Jan 2021, Jul 2023) → “Israel {+began committing genocide+} against Palestinians in Gaza” (since 4 May 2025). [B]
- **Deck:** In Wikipedia’s own voice. The word “genocide” has been in this opening section since 4 May 2025, and the article was viewed 4.6 million times in the past 12 months. Below: the other core articles, then and now. [A, chk]
- **Scope line:** We follow the core articles that carry the narrative and that people actually read: Zionism, Israel, 1948 and the Nakba, October 7, Hamas, the Gaza war. [A+B, page]
- **Anchor:** `#ev-charge`.

### Card 1 · Zionism [A+B]
- **Headline:** Zionism was the “re-establishment” of a Jewish state. Now it is “a Jewish homeland through colonization.” [both; owner's model]
- **Proof:** `#ziSum` chips [A+B], plus B's 4-phase label strip on `#ziChart` (Stable → Tug of war → Mostly in → Settled) as one static row, no stepper. [B]
- **What changed:** “the [-re-establishment of-] and support for a Jewish [-state in the territory-]” → “to establish and support a Jewish {+homeland through colonization+}” [A]
- **Body:** The next sentence now says Zionists wanted “as few Palestinian Arabs as possible.” From June to November 2024 “colonial” went in 33 times and out 32 times. From November 2024 to August 2026 it was taken out 10 more times, and each removal was undone within a day. Of the 41 removals of “colonization” we can check, 37 were undone. It has stood since 27 August 2026. [A+B, chk F1/F2/F10]
- **Carousel:** none (the stepper is a link: "Every change, step by step →" `#ev-zionism`). [A+B]

### Card 2 · 1948 and the Nakba [A+B]
- **Headline:** The Nakba was “the destruction of Palestinian society.” Now it is “the ethnic cleansing of Palestinian Arabs by Zionists.” [both]
- **Proof:** the `#palestine` THEN/NOW `.news-q` pair (Dec 2021 / since 6 July 2026), with the NOW quote cut after “belongings …”, plus the tag "the 2021 version also took a position". [A, page]
- **What changed:** “[-was the destruction of-] Palestinian [-society-]” → “{+is the ethnic cleansing of+} Palestinian {+Arabs by Zionists+}” [A]
- **Body:** Three 1948 articles now name, in Wikipedia’s own voice, who drove the Palestinians out: “Zionists” or “Zionist forces.” For the Jews who “fled or were expelled from Arab states,” no one is named. “By Zionists” has stood since 6 July 2026, apart from under an hour on 17 July. [A+B]
- **Carousel:** none. The 1948 Palestine war pair (2023 → now, “Zionist forces conquered about 78% …”) is a second line if space allows. [B]
- **Anchor:** `#ev-1948`.

### Card 3 · October 7 and the hostages [A, with B's headline fixed]
- **Headline:** Wikipedia’s first line on October 7 said “coordinated attacks.” Now it says “coordinated armed incursions.” Its opening sections on Israel and Hamas never mention the hostages. [A + B, chk F3]
- **Proof:** the hostages blockquote from `#ev-oct7`, as the hero of the card. First sentence: never, across 107 versions. Israel and Hamas opening sections: none, at every snapshot since 2021. Sentence 9 now: “251 Israeli and non-Israeli civilians and soldiers were taken as hostages to the Gaza Strip”. [A]
- **What changed:** “a series of coordinated [-attacks-]” → “a series of coordinated {+armed incursions+}” · “rape and sexual assault [-by Hamas fighters-]” → “{+dozens of cases of+} rape and sexual assault.” [A]
- **Body:** In January 2024 the rape sentence named “Hamas fighters”; on 2 November 2026 it names no one. The opening still says “massacring civilians in 21 communities,” and Hamas is named later in the same first sentence. [A, chk]
- **Optional extra (EIC):** Hannibal absent (Jan 2024) → “The IDF used the Hannibal Directive on that day, which may have led to at least 13 Israeli civilian deaths.” (2 Nov 2026). This is anchored (chart_data/oct7_06), but it is a second thesis, so I would leave it out. [chk]
- **Anchor:** `#ev-oct7`.

### Card 4 · Hamas, in English and in Hebrew [A, with B's proof inset]
- **Headline:** In 2021 Wikipedia called Hamas “militant.” Now it is a “political organisation with a military wing.” [A+B]
- **Proof:** A's three-line stack: EN 2021, EN now (since 29 Nov 2025), עברית now (RTL, with an English rendering, tagged "Other languages · exploratory"). [A] Under it, a two-row `#o7Pos` inset: 2021 sentence 5 of 20 → Oct 2026 sentence 22 of 23. If the EIC uses the 31 Oct row (“Several countries have designated Hamas as a terrorist organisation.”), stamp it "as of our 5 Nov 2026 copy; may be reverted". [A+B, chk F5]
- **What changed:** “[-militant-]” → “{+political organisation with a military wing+}” · Hebrew: “ארגון טרור … הפועל גם כתנועה פוליטית” (a terror organisation that also operates as a political movement) [A]
- **Body:** Hebrew Wikipedia puts it the other way around, as it already did in 2021. In English, “militant” left on 12 October 2023, five days after the attack. It came back three times, last in February 2025. [A, chk F8]
- **Anchors:** `#ev-oct7`, `#ev-xl`.

### Card 5 · The genocide charge, both ways [A, plus B's languages] · CAROUSEL 1
- **Headline:** In January 2024 Wikipedia said “Allegations have been made” of genocide in Gaza. Now it is “the ongoing, intentional, and systematic destruction … carried out by Israel.” [A, chk]
- **Proof:** two `.news-q` cards of equal size. GAZA GENOCIDE · FIRST SENTENCE · SINCE 26 SEP 2025 · WIKIPEDIA’S OWN VOICE, and OCTOBER 7 ATTACKS · OPENING SECTION · NOW · ATTRIBUTED: “Some have alleged that the attack was an act of genocide or a genocidal massacre against Israelis.” [A]
- **What changed:** “[-Allegations have been made that the 2023 Israel–Hamas war constituted a-] genocide” → “{+The Gaza+} genocide {+is the ongoing, intentional, and systematic destruction … carried out by Israel+}” [A]
- **Body:** The charge against Israel is stated as fact in the Gaza genocide, Israel and Netanyahu articles; the one about October 7 is “alleged.” Of the 150 most-read opening sections that existed in 2021, none charged Israel with genocide before the war; seven do now, two as fact. Since 26 September 2025, 10 edits tried to bring back attribution; each was gone within 45 minutes. [A, chk F7]
- **Carousel 1, "The charge, everywhere":**
  1. Netanyahu, now, no denial, quote ending “…in December 2023.” [B, chk F9]
  2. Arabic Gaza genocide: “has been accused of committing crimes of genocide” → “the systematic, deliberate and ongoing destruction …” (RTL plus English) [B]
  3. Spanish Gaza war: “un ataque de represalia” and “ha desencadenado un genocidio en Gaza por parte de Israel” [A+B]
  4. `#xwGG`: English dropped “allegations” from the title on 3 July 2024; Polish on 26 April 2026; Hebrew, German and Russian have none. [B]
  5. Hebrew, the exception: the Gaza war article reports only South Africa’s case; the first sentences call October 7 a “massacre” and Hamas a “terror organisation”. [A+B]
- Tag slides 2–5 "exploratory".
- **Anchors:** `#ev-charge`, `#ev-oct7`, `#ev-xl`.

### Card 6 · What lasts, in these four sentences [A, reworked; plus B's timing slide] · CAROUSEL 2
- **Headline:** Since September 2025, every attempt to make the Gaza genocide sentence attributed again was gone within 45 minutes. “Terrorist” went into Hamas’s first sentence five times; the longest stay was about 2.4 hours. [A, chk F7]
- **Proof:** the `#o7Fig` timelines as swipe slides. [A]
- **What changed:** “{+alleged+} / {+described by most scholars as+}” ×10 → gone within 45 minutes · “{+terrorist+}” ×5 → longest about 2.4 hours · “{+resistance movement+}” ×1 → gone the next day · “{+massacre+}” in October 7’s first sentence → about an hour in all, across 107 versions [A + chk]
- **Body:** These are four sentences, not the whole subject. Across the 254 core articles, edits that removed critical terms were reverted no faster than edits that added them. What these sentences show is which wording now holds. [chk; page wording]
- **Carousel 2, "How long a word lasts":**
  1. Gaza genocide attribution lane [A]
  2. Hamas: the “militant” lane, the “terrorist” dots, and the one “resistance movement” dot [A + chk]
  3. October 7: the “massacre” blips and the empty hostages lane [A]
  4. Zionism `#ziFig` frozen on “Mostly in” (Nov 2024 to Aug 2026) [A]
  5. **When:** `#kChart` with the 7 Oct marker: “In the three weeks after October 7, 13.7 new critical terms a week, against 3.8 before. Timing gives a date, not a cause.” [B; keeps the owner's chart in flash]
- **Anchors:** `#ev-oct7`, `#ev-zionism`, `#when`.

### Card 7 · The topic area, from Wikipedia’s arbitrators [B, cut down] · about 0.5 screen
- **Headline:** Wikipedia’s arbitrators found in January 2025 that “outside actors are heavily invested in influencing Wikipedia's coverage of the topic area.” They named no side. [B, chk]
- **Proof:** the finding 10 quote as a `.news-q` ("Arbitration Committee · PIA5 · finding 10 · adopted 15–0 · 23 Jan 2025", linked), with no direction colour. [B]
- **What changed:** none (this is not a then/now). Use a fact line instead: "Our count: in 217 formal talk-page discussions, four groups of 3 to 6 accounts voted together 89 to 100% of the time, against about half by chance." [B, chk]
- **Body:** "That is camp voting, not proof of coordination, and we did not code which side each group took." [B]
- **Carousel:** none. No usernames, no network graph, no counter. [chk]
- **Anchor:** `#ev-organised`.
- If the build exceeds 8 screens, fold this card into one closing line. [chk]

### Close [A+B] · CAROUSEL 3 (recap)
- **Headline:** These first lines once said “re-establishment” (2021), “militant” (2021) and “coordinated attacks” (October 2023). Now they say “colonization,” “ethnic cleansing … by Zionists” and “genocide.” [A, chk veto 2]
- **Carousel 3, "What the world reads now":** `#reads` slides in card order: Israel, Zionism, Nakba, October 7, Hamas, Gaza genocide. The last slide is "Moved the other way": the 1948 expulsion “by Zionist militias” left the first sentence on 30 May 2025, and the next sentence names “the Zionist paramilitaries Haganah, Irgun, and Lehi”; and October 7 dropped the “actions scholars have concluded constitute genocide” clause by 2 Nov 2026 (recent; may be undone). [A+B, chk]
- **Ratio line:** For every critical term taken out of these opening paragraphs, almost four went in: 223 in, 61 out. On comparison pages (other countries, conflicts and religions), 125 in, 73 out. [A+B]
- **Reach line:** These are the opening sections of the most-read pages that changed: Benjamin Netanyahu, 7.0 million views in the past 12 months; Israel, 4.6 million; Palestine, 2.4 million; Zionism, 1.8 million; Hamas, 1.3 million. [B, chk F11]
- **The one honesty line:** This measures what Wikipedia says, not whether it is true; the change sits in the core articles people read, while the long tail of short pages barely changed. [B]
- **Links:** “Full research edition →” · “Every quote, dated →” `#reads`. [A]

### Dinner sentence [B, chk]
“Before the war, none of the most-read Wikipedia openings on the subject charged Israel with genocide. Now Israel’s own article says, in Wikipedia’s voice, that Israel ‘began committing genocide.’ Zionism is ‘a Jewish homeland through colonization.’ And the Israel and Hamas opening sections never mention the hostages.”

### Three share cards [A]
Keep A's three. Fix share card 1's top line to the full “Allegations…” wording only if it is shown; the Hebrew card keeps the "exploratory" footer.

### Cut from the flash, confirmed
- B card 2 as a separate carousel (it duplicates cards 1–5; becomes the closing recap).
- The B card 6 scrolly as a card (it becomes one slide in carousel 2).
- The 64/70 vs 47/78 pair (F2).
- Ïvana; the #net counter; the press-reported motions.
- Settlements; Jewish-ties numbers; the “Hamas-led” title drop; the West Bank (`#news`).
- All days figures (336/38, 650/74, 386/96).

Screen estimate: opening 1.2 + cards 1–6 at about 0.9 each (5.4) + card 7 at 0.5 + close 0.7 ≈ 7.8.
