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

## 6. Tooltips on symbol grids, so the reader never loses their place (owner, round 5)
- In the language voice grid (#crosslang: the "-> " squares with quote marks, dots, "...", n/a, the ▲/▼ rings) and every similar symbol-based visual (Zionism/Oct 7 stepper marks, network nodes/edges, charge bars, reach rows, scrolly markers), hovering or keyboard-focusing an item shows a tooltip IN PLACE:
  (a) what the symbol means in plain words (e.g. "attributed -> stated as fact, moved toward Wikipedia's own voice");
  (b) the source: the exact sentence quoted (original language + English rendering for non-English, RTL where needed), its date/version.
- Clicking must not jump or scroll away. On touch, a tap opens an anchored popover with a close button; the existing "open the full sentence" panel stays as a secondary action inside the tooltip.
- Accessible: role="tooltip"/aria-describedby, Esc closes, works at 390px without overflowing the viewport (flip/clamp position).

## 7. The network graph must say something at a glance (owner, round 5)
Owner: "this doesn't mean anything with how it looks - also with the same tabs in it". The current #organised graph (Groups/Network/Table tabs, two panels, colour/size/thickness/ring-style legend) does not convey the finding.
- Redesign around ONE message, readable in 5 seconds: how many linked pairs we found among topic editors vs what chance gives (14 vs ~2), vs comparison articles; where the links cluster (Bloc A, the low-confidence group); and what we did NOT find (no synchrony, no copy-paste sweeps). Headline the answer in the chart title, annotate directly on the graph (labels on the blocs saying what they did in words), no legend-decoding needed.
- Show chance visibly: e.g. a ghost/"expected by chance" version side by side, or a counter "14 links found / ~2 expected".
- Encode only what matters (keep at most 2 channels: e.g. colour = adds vs removes critical terms; drop the line darkness/thickness and ring dash/dot encodings or move them to the evidence room).
- Remove the in-story tabs: one default annotated view in the story; Groups and Table move to the evidence room. Fix the label overlap ("Low-confidence group" label collides with a node).
- Comparison panel: either make it a direct visual contrast (same scale, labelled "comparison articles: 3 pairs") or fold it into the counter.
- Keep anonymity (A1…, no accounts identified) and the tooltip rule from must-fix 6 (hover = meaning + numbers vs chance, in place).
- Must-fix 5 data notes (from patterns/zionism/CODES.md): show "uncodable" as "not coded" (never as neutral). The finding to surface with the encoding: the two directions are close in COUNT (more critical, stated as fact, contested: 78 changes; the mirror: 70), but not in DURATION: the more-critical wordings stayed live 336 days vs 38, and 64 of the 70 opposite changes were undone within a day (vs 47 of 78). Use regime_days for "how long it lasted". Same coding exists for October 7 attacks, Hamas and Gaza genocide (other_articles) and may feed the Oct 7 stepper; direction there is judged from Israel's standpoint (stated in the codebook). All coders are LLMs (κ 0.91/0.82/0.87); say "double-coded by two independent automated readers, agreement κ≈0.8–0.9" in the evidence room.

## 8. Full copy edit of every visible text, starting with the title (owner, round 5)
Owner asked whether the hero title is good English. It is not: "Zionism, “through colonization”. Israel “began committing genocide”. How the reference the world reads now tells Israel’s story." = fragments, clunky "the reference the world reads now", inconsistent quote punctuation, five phone lines.
- Title: one clear line that says what happened; the exact quotes and dates go in the deck. Candidate directions: "Colonization, genocide, ethnic cleansing: the new first lines of Israel's story" / "How the world's encyclopedia rewrote the first sentence of Israel's story". The editor picks/refines; max ~12 words, max 3 phone lines at 390px.
- Line-edit every visible string in both tabs (headlines, bottom lines, decks, step cards, chart titles, axis labels, legends, buttons, tooltips, captions, alt text): grammar, idiom, native American English, consistent punctuation (periods/commas inside quotes, curly quotes, en dashes for ranges), no translationese, no stacked noun phrases, no fragments, short sentences.
- Never change a number, a quote, a date or a claim's strength. Flag (don't silently fix) anything that would need a data change.
- Owner: the #zionism heading "Zionism was the “re-establishment” of a Jewish state. Now it is “a Jewish homeland through colonization”." is VERY STRONG: keep it (only fix punctuation to American style: “colonization.”). It is the model for every headline, the hero included: two complete sentences, then -> now, the exact quoted words, no explaining. The hero title should follow this pattern (e.g. a then/now pair for the whole story) rather than a list of fragments. Do not repeat the Zionism pair verbatim in the hero if it is the next section's heading; pick the strongest other then/now or a summary line in the same shape.
- Must-fix 6 is NOT yet built (round 5 did not add it). Round 6 TOP PRIORITY: the #crosslang voice grid (#xmFig: every from -> to square pair, the ▲/▼ rings, the column headers) gets the in-place tooltip first: plain meaning of both states and the change ("attributed -> stated as fact; moved toward Wikipedia's own voice"), plus the source sentence (original + English rendering, date). Owner asked twice.
- Per owner's "no courts" rule: move the "Court ruling overstated" column out of the story grid into the evidence-room version of the grid (it stays as wording evidence there).
