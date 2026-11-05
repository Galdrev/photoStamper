# Close-reading brief (study 3, qualitative phase A: open coding)

You are one of three close readers. Each takes a different lens on the same raw material. The project asks whether, and how, English Wikipedia's baseline story about Jews, Judaism, Israel, Zionism, Palestinians and Palestinian history changed between Jan 2021 and Oct 2026. Comparison articles cover other countries, conflicts and religions. Statistics alone came out mixed: the average vocabulary barely moved, but some articles changed a lot. We now want to understand the CONTENT. What do editors actually do to these texts? Which recurring "moves" can we name, define and later count reliably?

## Material (discovery half ONLY)
/home/user/photoStamper/wikitrends/data/study3/qual_discovery.json is a list sorted by how much the lead changed. Each entry has:
- title, group (treatment = topic; control and control_contaminated = comparison)
- change (1 − similarity)
- lead0 (opening section, Jan 2021) and lead1 (Oct 2026)
- first_sentence_edits: exact revisions that changed the first sentence, with timestamp, edit summary (comment), reverted flag, and before/after text. These exist for 24 key articles.

Do NOT open data/study3/qual_holdout.json, data/leads.json, data/bisect.json, or anything else containing the other half. A frozen codebook will be tested on that half later.

## Method: grounded open coding, then sharpening
1. Read at least 40 topic lead pairs in full, starting from the most changed but also sampling the middle, plus at least 15 comparison pairs as contrast. A move that comparison articles show just as often is general Wikipedia style, not a topic finding. Say so explicitly.
2. Write short in-vivo codes for each change you see, then group them into 6–10 named MOVES.
3. For each move give:
   - a definition precise enough that two coders would agree
   - an inclusion rule and an exclusion rule
   - 2–3 verbatim before/after examples with article titles
   - a rough count in your reading of topic vs comparison, e.g. "seen in 14 of 45 topic pairs, 2 of 15 comparison pairs"
   - the direction it pushes the story, described neutrally, e.g. "moves agency from X to Y"; never "biased" or "correct"
4. Propose content KPIs: measurable indicators derived from the moves, each with a unit (per article pair, per sentence, per first sentence) and a coding procedure that an LLM coder could apply to a masked before/after pair. Also mark which KPIs could instead be computed automatically from text (regex or parse) and which need human or LLM judgement.
5. Name what you expected but did NOT find, and what surprised you.

## Rules
- Describe, don't judge. No claim about truth or bias. Report which narrative the text now states as baseline, and how.
- Quote exactly. Never paraphrase inside quotation marks.
- Write to your own folder (given in your task) as codebook.md, with a JSON version codebook.json: [{move, definition, include, exclude, examples:[{title,before,after}], topic_count, comparison_count, direction, kpis:[{name, unit, procedure, automatable}]}].
- Final message: at most 700 words. Give the moves ranked by how distinctive they are of topic vs comparison, the KPIs, and the surprises.
