# Owner must-fixes, queued for the editor-in-chief pass after round 4 (2026-11-08)

1. **#against overclaims balance.** The H2 and bottom line say "Not one-sided: Jewish ties to the land were kept...", and the bullet at page_template.html ~line 1425 repeats it.
   - **Why it's wrong:** Judaism articles not changing is the expected null, not counter-evidence. And "kept" is contested: 'homeland' in first sentences fell 5→1 (SYNTHESIS D8); Zionism lost "re-establishment"; the K11 11-vs-6 is small and exploratory; Jewish land names rose 11→19.
   - **Fix:**
     - H2 something like "Some edits went the other way, far fewer".
     - Evidence = only genuine opposite-direction edits: "by Zionist militias" removed from the 1948 expulsion first sentence; "Israel disputes this" added to the settlements sentence; antisemitism mentions in topic openings 37→54. Plus the proportion: 61 critical terms removed vs 223 added.
     - Drop "lopsided, not one-sided".
     - Move the Jewish-ties point out of this section. If kept elsewhere, state it as mixed evidence with both directions' numbers.
2. **General rule:** never present a non-change as counter-evidence. Every balance or "not one-sided" claim must show real opposite-direction edits together with their proportion against the main direction.

3. **Cut non-informative content; scope to where the story lives** (owner, 2026-11-08).
   - The trend is clear in some kinds of articles and absent in others. The core and high-importance articles and the conflict, history and identity articles (Zionism, Israel, 1948/Nakba, October 7, Hamas, the Gaza war, the charges) are where it lives. The long tail of low-importance pages (villages, minor people, unrelated topics) doesn't change and isn't interesting.
   - State the scope once, up front, in plain words: the story is about the articles that carry the narrative, the ones people actually read.
   - REMOVE from the story layer the material that shows only non-change and adds nothing to the narrative:
     - population-wide averages as headline framing;
     - low-tier bars presented as findings;
     - the Judaism-null-as-balance point;
     - repeated "no difference" statements;
     - comparisons that only show nothing happened.
   - Keep honesty with ONE short line in the trust box (e.g. "Across all 49,000 articles in these projects, most are short pages that never changed; averaged over them, the change is no larger than in other conflicts' articles"). Put the full population analysis in the evidence room.
   - Do not delete evidence files. Move material out of the story, and drop it from the page only if it truly adds nothing.

## 4. Drop the court-ruling contrast and the research-process narration; lead with what events changed (owner, round 4)
- Remove the "battles, not the court rulings" framing everywhere (headline, bottom line, FAQ "Is it just the war?", talking points). Courts are not part of the story.
- Instead show the interesting part: when a battle or major event happened (Oct 7, ground invasion, Rafah, Lebanon, Iran, ceasefires), what changed right after it in WORDING and in the ORDER/arrangement of the opening (e.g. Hamas designation moved from sentence 5 to 22; "militant" -> "political organisation with a military wing"; new first sentences of Zionism/Israel). Event -> concrete wording/reordering change, anchored to diffs and the edit timeline.
- No claims about a "general population" of articles: it is not well defined and cannot be. Remove population-wide averages, the pre-registered average test, Horvitz-Thompson/population figures, and any "the average didn't move" framing from the story layer. Scope = the core, high-importance conflict/history/identity articles where the narrative lives.
- This is not academia: do not narrate the research process (holdout halves, withdrawn measures, pre-specification, BH, resampling methods) in the story. Keep one honesty line in the trust box and move the rest to the evidence room/method appendix, or cut it if irrelevant. Not lying; cleaning noise.
- Use these cuts to shorten the page: the story layer must hit <=20 phone screens.
- KEEP the scrolly vocabulary chart (sticky chart + step cards): the owner loves it. Keep the mechanic and look; it may be re-pointed to the scoped core articles and to event markers (battles/escalations instead of the "ICJ case" line), but do not delete or flatten it.

## 5. Zionism stepper shows what each edit DID (owner, round 5)
- Each change in the step-through timeline gets a visual encoding of its essence, from patterns/zionism/change_codes.json (blind double-coded): direction (more vs less critical of Israel/Zionism, or wording only), voice (stated as fact vs attributed), claim type (checkable fact vs contested characterisation). The key highlight: contested characterisation stated as fact.
- Reader-facing labels are NOT fixed by the owner or by me: the newsroom/editorial agent picks them from change_codes.json "label_options". They must be precise, non-loaded and defensible (no "hostile"; no "alleged" when "attributed" is meant).
- Keep the stepper's mechanic and look; add the encoding (colour/mark per change, a small legend, and the per-step live text naming the category).
