# Pattern hunt brief (scope change, 2026-11-05)

We are switching from academic hypothesis testing to sense-making. The owner wants to look at the data from different angles, see the patterns and trends, and decide what we can conclude or do with them. They will present this to smart non-specialists.

## What we already know (use it, don't re-derive it)
- **Study 1:** the pre-registered average test on critical vocabulary (colonial, apartheid, genocide, occupation, ethnic cleansing, Nakba/expulsion, war crimes) was null on the deep panel (513 articles, quarterly 2021-01 → 2026-10).
- **Study 3, sealed-half replication:**
  - After Oct 2023, more topic articles gained critical vocabulary than comparison articles: +3.6 pp on the mass tier (10k articles).
  - The gain shows in leads and in Top/High-importance articles.
  - It is concentrated in the Israel and Palestine WikiProjects; Judaism is flat.
  - It is a sustained rise, driven by post-war edit surges rather than habitual churn.
  - It arrives as added text. Jewish-history content is kept; the change layers on top of it.
  - "Palestine" spreads as the modern land name.
- **Event filter:** the lead change sits in sentences about older history, not in war coverage. Topic lead +8.4 of +9.3 per 10k words is narrative residual.
- **Content coding:** rhetorical moves (voice upgrades, story start, renaming) are not more frequent than in comparison articles. Their direction is lopsided in small counts.
- **Process:**
  - The Zionism definition: "colonial" went in and out 44 times and has stuck since 2026-08-27.
  - The Gaza genocide lead went from "allegations" to Wikipedia's own voice in 8 one-way steps over 21 months.
  - Revert-heavy articles change less.

## Data (all of it is open to you now; there is no holdout restriction)
All files are under /home/user/photoStamper/wikitrends/data/:
- `results.json`: deep panel. `articles[]` holds per-article series (crit_series, lcrit_series, frame_series, words_series), plus quarter_edits, w_edits, revert_rate, talk_edits, top10, editors, views, pv_monthly, first_sentences and lead_diff. Also trends, event_study, did, robustness, explore, coordination.
- `mass_results.json` → `mass`: 10,433 articles, each with `lab_articles` {t, g, p project, i importance, f full [[words + 12 frames] × 3 dates], l lead, e edits, rv reverts}. Also by_project, histogram, hedging, citations, first_sentence_critical, tests, coordination, languages.
- `ratchet.json`: lead of every revision for key articles; insertion/removal survival. Inspect it.
- `bisect.json`: exact first-sentence edits for 40 key articles, with dates and edit summaries.
- `crosslang.json`: 20 key articles in 11 languages.
- `leads.json`: lead text, 2021 vs 2026, for 473 deep articles.
- `kwic_coded.json`, `blind/*`: earlier coding.
- `study3/*`: qualitative packs, codebooks, coding results.
- Code for definitions: `../analyze.py` (lexicons), `../corpus.py` (groups and seeds).

## How to work
- Python 3 with numpy and pandas (`pip install` anything else).
- Work in your own scratch folder, given in your task. Write final outputs only to your folder under /home/user/photoStamper/wikitrends/patterns/.
- For each pattern, write a card:
  - **title:** a plain statement, for example "The change came in waves after events, not as a slow drift".
  - **what we see:** 2–3 sentences with the key numbers.
  - **chart:** the chart that shows it best (type and axes), plus a small JSON of chart-ready data.
  - **confidence:**
    - STRONG: large n, survives a comparison group or replication;
    - SUGGESTIVE: consistent but small or unreplicated;
    - ANECDOTE: a single vivid case.
  - **so what:** what this lets us conclude, or what someone (reader, editor, researcher, journalist, platform) could do with it.
  - **caveat:** one line.
  - **examples:** 1–3 concrete article examples with real quotes, where useful.
- Always look at the comparison articles too. A "pattern" that other conflicts show just as much is a Wikipedia-wide pattern. Say so; that is itself interesting.
- Be curious. If you find something surprising outside your angles, include it.
- Deliverables:
  - `cards.json`: a list of cards.
  - `cards.md`: readable.
  - `chart_data/*.json`.
- Final message: at most 500 words, with the cards ranked by how interesting and solid they are.
