# Design council, round 2: interaction design

Author: the interaction designer behind the Zionism step-through timeline (`#zionism`).
Scope: recommendations only, nothing built. Inputs: `patterns/angle/ANGLE.md` (audience: Israeli media), the current page `page_template.html`, `analyze_coord.py` (the `network.json` schema), `patterns/angle/PERP.md`, `patterns/angle/OCT7.md` and its `chart_data/oct7_*.json`.

**Short answer to the owner: not a graph first.** Lead with a **community view tested against chance**: cards with an activity timeline, the Discord window and an observed-vs-chance marker. Offer the graph as a second tab, with a fixed layout and placed side by side with the comparison network. Use time as a **filter with named presets**, not an edge animation. Reasons:
- An animated hairball is the image most likely to be read as "a conspiracy network", and the one that is hardest to defend in a studio debate.
- Our edges are aggregates over the whole period, so they never "appear" at one moment. Animating them would show something the data does not contain.

---

## 1. The coordination network

### 1.1 What the data supports, and what it does not

From `analyze_coord.py` → `chart_data/network.json` (`{generated, method, topic:{nodes,edges,communities,counts}, comparison:{...}}`):

| object | fields we can show | notes |
|---|---|---|
| node | `id` (A1…), `insert_share`, `events`, `articles`, `community`, `age_bucket` (`<30d`, `30d-1y`, `1-5y`, `>5y`, `unknown`) | Labels are per network: A3 in topic is **not** A3 in comparison. Say so on the page. |
| edge | `weight` = log2((obs+1)/(null+1)), `observed`, `null_mean`, `null_p95`, `p`, `basis` (`t30` or `shared`), `significant_on`, `windows` (t10/t30/t60), `same_direction_share`, `example_article_pairs`, `shared_article_examples`, `time_span` [first,last] | Every edge already passes p<0.01 with observed≥3. Each edge carries its own chance value. That is the key to keeping the null visible. |
| community | `size`, `density`, `strength`, `n_articles`, `articles[{title,events}]`, `direction{insert,remove,insert_share}`, `active{first,last,busiest_month,events}`, `inserted_phrases`, `confidence` (high / medium / low / "n/a (pair)"), `significance{fixed_set_null, null_worlds_with_community_this_large_dense_and_strong, null_worlds}`, `window_share{email_canvassing,tfp_discord}`, `expected_window_share{…:{mean,ci95,p_high,p_low}}`, `post_sanction_drop{date:{ratio,ci95,p_drop,testable}}`, `profile` | `window_share` vs `expected_window_share` is the Discord test, and it carries its own CI. |
| counts | `accounts_tested`, `articles`, `events`, `edges`, `communities_3plus`, `communities_significant`, `expected_by_chance{null_worlds, edges_mean, communities_mean, communities_p95, communities_max}` | This gives the headline "found vs expected by chance". |

**Schema additions to request from the analyst** (small, all aggregate, no privacy cost):
1. `community.weekly`: events per ISO week, 2021-01 to 2026-11. Needed for the activity strip and the time filter.
2. `community.weekly_insert` / `weekly_remove`: optional, to split the strip by direction.
3. `node.first` / `node.last` (month only). Needed for the time filter on the graph tab.
4. Precomputed layout coordinates `node.x`, `node.y` (deterministic, seeded, one per network). This keeps the graph identical on every load and in every screenshot.

Without (1), the time features below fall back to `active.first/last/busiest_month` plus the window shares. That works, but it is coarser.

### 1.2 Section layout (desktop, 1240px content width)

```
┌───────────────────────────────────────────────────────────────────────────────┐
│ PROCESS · Organised or organic?                    [Exploratory · not pre-reg]│
│ H2  Accounts whose edits cluster in time, measured against chance             │
│ deck (2 lines)                                                                │
├───────────────────────────────────────────────────────────────────────────────┤
│ HOW TO READ THIS  (one line, always visible)                                  │
│ "Each group is a set of accounts that edited different articles within 30     │
│  minutes of each other more often than chance allows. Chance = the same       │
│  accounts with their timelines shifted by 1–7 days, 1,000 times."             │
├──────────────────────────────────────┬────────────────────────────────────────┤
│ ISRAEL / JEWISH-TOPIC ARTICLES       │ COMPARISON ARTICLES                    │
│ Groups beyond chance   4             │ Groups beyond chance   1               │
│ ▕████████▏ found                     │ ▕██▏ found                             │
│ ▕··▏ expected by chance 0.6 (95%≤2)  │ ▕··▏ expected by chance 0.5 (95%≤2)   │
│ Linked pairs 212 · chance ≈120       │ Linked pairs 88 · chance ≈80          │
├──────────────────────────────────────┴────────────────────────────────────────┤
│ View: [Groups] [Network] [Table]     Articles: [Topic] [Comparison] [Both]    │
│ Time: [All 2021–26] [Before 7 Oct 2023] [Discord window] [After sanctions]    │
└───────────────────────────────────────────────────────────────────────────────┘
```
(Numbers in sketches are placeholders. Every printed number comes from `network.json`.)

**The headline strip is the null model made visible.** Each count is a pair: a solid bar for what was found and a dotted "ghost" bar for what chance gives (`expected_by_chance.communities_mean`, with its p95 as a thin whisker). Topic and comparison sit side by side **on the same scale**. This strip appears above every view, on every device. If the comparison side also shows groups, the reader sees it immediately. That is what makes the piece credible to a hostile reader.

### 1.3 Default view: "Groups" (community cards)

One card per community with size ≥3, sorted by confidence, then size. Pairs ("n/a (pair)") are folded into one line at the bottom: "plus N linked pairs, too small to test as a group".

```
┌ Group 1 ─ [HIGH confidence] ───────────────────────────────────────────────────┐
│ 7 accounts · 23 articles · 92% of their edits ADD critical terms   ■■■■■■□ (mix)│
│                                                                                │
│ activity, per week, 2021 ─────────────────────────────────────────────── 2026  │
│        ░░░░░░(email canvassing, Oct 23–Jan 24)                                 │
│                     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ (Discord channel public, Jan–Sep 2024)      │
│  ▁ ▁  ▁▁ ▂▃▅▇█▇▅▆█▇▅▃▂▁   ▁  ▁        ▏9 Dec 2024 sanctions  ▏25 Apr 2025 bans │
│                                                                                │
│ Share of this group's activity inside the Discord window                       │
│   chance  ├──○────┤ 18% (9–27%)        found  ● 61%      p<0.001               │
│                                                                                │
│ Articles: [1948 Palestine war ×41] [Nakba ×22] [Zionism ×9] +20                │
│ Phrases added in 3+ articles: "expelled by Zionist forces" (6)                 │
│ How sure: 0.2% of 200 shuffled worlds made a group this large and tight.       │
│ Not shown: who these accounts are, or why they edited together.  [Details ▾]   │
└────────────────────────────────────────────────────────────────────────────────┘
```

Rules:
- **Confidence chip** (`high` / `medium` / `low`): text plus border style (solid / dashed / dotted). Never colour alone. **Low-confidence groups are shown, not hidden**, collapsed under "Groups chance also produces (low confidence)". This shows we did not cherry-pick.
- **Direction** uses the page's diff colours, as in the Zionism piece: blue `--add-bd` = adds critical terms, amber `--del-bd` = removes them, grey = mixed (insert share between 0.4 and 0.6). The mini bar is a 7-cell share bar. Text always states the percentage.
- **Both documented windows are shaded with equal weight.** The pro-Israel email-canvassing window (Oct 2023 to Jan 2024, ArbCom PIA canvassing) and the Discord window (Jan to Sep 2024) use the same neutral hatch, each labelled in words. ANGLE.md: pro-Israel organised editing "makes the piece credible". This is where it does so at no cost to the lead.
- **Window test as a dumbbell:** a hollow ring for the chance mean with its 95% CI bracket, a filled dot for the observed share, and the p value in text. Same marker grammar as the existing `.dtrack` dumbbells in `#organic`.
- **Sanction ticks** carry the `post_sanction_drop` result in the tip, or "not testable (fewer than 5 events before)" when `testable:false`.
- **Words:** "documented" only for the two ArbCom-recorded windows. For our results, say "beyond chance" or "not detected". Never "network of activists", "ring" or "operatives".

### 1.4 Second view: "Network" (graph, side by side)

```
┌ TOPIC ARTICLES ────────────────────────┐ ┌ COMPARISON ARTICLES ───────────────────┐
│   ╭─G1 (high)──╮     ╭┄G2 (medium)┄╮   │ │   ╭┄G1 (medium)┄╮                      │
│   │ ●─●  ●     │     ┆  ○─○        ┆   │ │   ┆  ●─○        ┆     ·  ·  ·          │
│   │  ╲│ ╱      │     ┆   ╲         ┆   │ │   ┆   ╲         ┆   (pairs + loners,   │
│   │   ●──●     │     ┆    ○        ┆   │ │   ╰┄┄┄┄┄┄┄┄┄┄┄┄┄╯    same scale)       │
│   ╰────────────╯     ╰┄┄┄┄┄┄┄┄┄┄┄┄┄╯   │ │                                        │
│   ·  ·   · ─ ·   (pairs, low)          │ │                                        │
└────────────────────────────────────────┘ └────────────────────────────────────────┘
 blue: mostly adds critical terms · amber: mostly removes · grey: mixed · size: edits
 line: linked beyond chance (darker = further beyond chance) · solid hull: high · dashed: medium
```

- **Fixed, deterministic layout.** No physics, no wobble, no animation on load. Each community is packed into its own cell on a grid, members on a circle or in packed circles, cells sorted like the cards. A fixed layout gives clean screenshots for TV, and the same picture for every viewer and critic.
- **Same scale on both sides:** the same node-size scale and the same cell size. If the comparison side is sparser, it looks sparser.
- **Edges:** 1px, opacity mapped to `weight`, from 0.25 to 0.9. No edge thicker than 2px. Hover or tap shows "edited different articles within 30 min **14 times; chance gives 3.1** (95% of shuffles ≤ 7); same direction 86%; e.g. *1948 Palestine war ↔ Nakba*". **Every edge tip leads with observed vs chance.**
- **Nodes:** fill = direction (blue / amber / grey), radius = √events (4–14px), and a 2px `--sheet` ring so overlapping nodes stay legible. Age bucket appears only in the tip ("account under 30 days old when first seen"). Do not encode it with shape: it is too easy to over-read.
- **Click a community hull** to jump to its card in Groups view, keeping selection state.
- **No usernames, ever.** The tip shows A-labels only. A-labels reset per network, and the legend says so.

### 1.5 Time: filter with presets, not an edge animation

**Do not animate edges appearing over 2021–2026.** An edge is a statistic over the whole period, and `time_span` only gives its first and last co-activity. Animating it invents a "moment the network formed".

Do this instead:
- **Time presets** (segmented control, one row): `All 2021–26` · `Before 7 Oct 2023` · `Email canvassing (Oct 2023–Jan 2024)` · `Discord window (Jan–Sep 2024)` · `After sanctions (Dec 2024 on)`.
- Choosing a preset **dims, never hides**. Cards and nodes fade to 25% opacity when less than X% of their activity falls in the range (needs `weekly`). Edges whose `time_span` does not overlap the range drop to 10%. The headline strip never changes, because the test was run on the whole period, and the strip says so: "the test covers 2021–2026; presets only highlight activity".
- **Optional brush** on a single shared weekly strip of all topic coordination activity. Desktop only; phones get presets.
- **Step-through** applies to the Groups view: Prev/Next moves card by card, with the same pinned control card as Zionism. No autoplay here: there is no time story to play.

### 1.6 Keeping significance in front (anti-conspiracy guardrails)

1. Headline strip: found vs chance, topic vs comparison, always on top.
2. Every number that can have a chance partner has one: edge tips, window dumbbells, group "how sure" lines.
3. Low-confidence groups are listed and openly labelled "chance also produces groups like these".
4. A fixed "What this can and cannot show" box (reuse `.caveat`):
   - shared watchlists and breaking news produce the same pattern;
   - beyond chance is not proof of coordination;
   - we do not identify accounts.
5. The comparison network is always one tap away, and side by side on desktop.
6. Copy rule: the verb is "clustered" or "moved together", never "coordinated", except for the two ArbCom-documented episodes, named as documented.
7. Show the selection-aware calibration share ("0.2% of 200 shuffled worlds") as well as p. It answers "you went looking for groups and found some".

### 1.7 Mobile (390px)

- The headline strip stacks as two rows (Topic, Comparison), and the shared scale is kept.
- **Groups is the only default view.** Cards are full width, and the activity strip is 56px tall with both windows hatched. The dumbbell takes the full width.
- The **Network** tab becomes a **mini graph per card**: a static, ≤12-node layout of that community (160px tall) in place of the global graph. The global graph on a 390px screen is noise.
- "Articles: Topic / Comparison" stays a toggle, with the same scale.
- Time presets become a horizontally scrolling chip row (44px targets), like the Zionism "Jump to" row.
- No hover anywhere. Tapping a node or edge fills a details panel under the graph, so no information lives only in a tooltip.

### 1.8 Accessible alternatives

- **Table view** (third tab): one row per community with size, articles, insert share, confidence, calibration share, Discord share vs expected (CI), email-window share vs expected, sanction-drop result. Expand a row to list its edges: A-pair, observed, chance, p, same-direction share. Sortable `<th>` buttons, as in `#ledger`.
- The graph SVG has `role="img"` and a computed summary ("Topic: 4 groups beyond chance, 0.6 expected; Comparison: 1"). Arrow keys move between nodes in community order, and a live region reads the node and edge facts.
- Confidence and direction are always in text. Colours pass the page's existing validated diff palette in light and dark.
- `prefers-reduced-motion`: no transitions. There is no animation to begin with.

---

## 2. Hamas / October 7 as a second step-through timeline: **yes**, reuse the Zionism component

### 2.1 Why
- The Zionism piece is the owner's favourite interaction. A second instance teaches the grammar once and repays it twice.
- The Hamas data has the same shape: every first-sentence revision (`ratchet.json`), with key-term flips. OCT7.md counts 114 changes since 7 Oct 2023 against 7 before, and 19 "militant" flips.
- The story is exactly what a step-through shows best: the first days (9 Oct "political" in, 12 Oct "militant" becomes "military"), then a long tug of war, then a settle.

### 2.2 Generalise the component (build note)

Factor `#zionism`'s JS into one factory, `stepTimeline(root, cfg)`, with all DOM queries scoped to `root`. That keeps each section self-contained and movable. Config:

```
cfg = {
  id: "hamas",
  changes: [...],                // [date_or_ts, from_variant, to_variant, reverted, moves[]] as in zionism_data()
  variants: Map(id -> text),
  lanes: [ {term:"militant", label:"“militant” in the definition", tone:"del"},     // a word that LEFT = amber
           {term:"pol_mil_wing", label:"“political … with a military wing”", tone:"add"},  // a word that is IN now = blue
           {term:"terrorist", kind:"blips", label:"“terrorist” added (each lasted hours)"} ],
  context: {kind:"monthly_views", series:[...] },   // Hamas: monthly pageviews in place of edits/week
  axis: {from:"2021-01-01", collapseBefore:"2023-10-01"},   // see 2.4
  phases: rule-based (see 2.3), moments: [...], keyLabel: "militant / terrorist moves"
}
```

`build_page.py`: generalise `zionism_data()` into `fs_track(title, lexicon)`, a term → regex map evaluated on `fs_variants`. Call it for Hamas, "October 7 attacks" and "Gaza genocide". `zionism_data()` keeps its own chips and paragraph diff and calls `fs_track` for the timeline part. Time precision: these articles change within hours, so durations must show hours ("lasted 2 hours", "15 minutes"). Revisions need timestamps, not day dates; `ratchet.json` must expose them or the build must join them.

### 2.3 Hamas spec

- **Title:** "Hamas: how the encyclopedia defines it, revision by revision".
- **How to read:** "Each tick is one change to the first sentence. Amber shows when 'militant' was in it. Blue shows when it read 'political organisation with a military wing'. Red-outlined dots are the five times 'terrorist' was added; none lasted a day."
- **Lanes:**
  1. "militant" in (amber, `--del-bd`, because it left);
  2. political / military-wing form in (blue);
  3. "terrorist" blips: dots sized by how long they lived, with the duration in the tip;
  4. every change (ticks, short tick = later undone).
- **Context strip:** monthly pageviews, not edits per week. Oct 2023 = 8,236,474, the record month. For an Israeli audience the question is how many readers saw which version.
- **Phases** (computed, rules stated in the note):
  1. "Stable" (Jan 2021 to 9 Oct 2023, 7 changes);
  2. "Rewrite week" (9 to 12 Oct 2023: "fundamentalist" out, "political" in, "militant" becomes "military");
  3. "Tug of war" (to 18 Feb 2025: militant in/out 19 times; first run of militant flips with no gap over 45 days, the Zionism rule);
  4. "Settled: political organisation with a military wing" (18 Feb 2025 to now; last change 2 Dec 2025).
  The analyst must confirm the boundaries from data, as I did for Zionism.
- **Jump to:**
  - 9 Oct 2023 "political" added;
  - 12 Oct 2023 "militant" becomes "military";
  - first "terrorist" insertion (10 Oct 2023, about 2 h);
  - 19 Aug 2024 "militant wing";
  - 12–18 Feb 2025 last "militant" spell;
  - settle.
- **Diff panel:** identical to Zionism (date with UTC time, "this wording lasted", "later undone?", "key word moved" in ins/del style, before/after word diff).
- **Companion card under the timeline:** "Where the terror designation sits in the lead". This is the `oct7_08` position bar: one horizontal bar per snapshot from 0 (first word) to 1 (last word), a dot where "terrorist" first appears, and a hollow dot for "supported by Israel". Static, five rows, no stepping needed. It answers the second Israeli grievance without leaving the section.

### 2.4 October 7 and Gaza genocide: same component, article tabs

Above the chart, a segmented control picks the article: **`Hamas` · `October 7` · `Gaza genocide`**. One component and one set of controls; the lanes swap per article.
- **October 7:**
  - title lane: 6 labelled steps, from "Operation Al-Aqsa Flood" to "October 7 attacks";
  - act lane: "attacks" → "armed incursions";
  - Hamas-named lane;
  - blips: "massacre" (twice, about 1 h), "terror" (3, 0.2 days), toll (1.2 days), "hostages" (never). Show the empty lane labelled "hostages: never in the first sentence". **An empty lane is the finding.**
  - Moments: 22 Oct 2023 renamed, 9 Dec 2023 "armed incursions", 26 May 2025 Hamas leaves the title, 8 Oct 2026 holiday clause removed.
- **Gaza genocide:** a "voice ladder" lane (0 alleged, 1 accused, 2 according to, 4 own voice; step line). Red ticks for the 10 reverted attribution attempts after Sep 2025. Moment: 21 Sep 2025 01:53 UTC, first own-voice version.
- **Axis:** these articles live from Oct 2023. For Hamas, collapse 2021 to Sep 2023 into a labelled stub ("2021–Sep 2023: 7 changes ▸") 8% wide, and give the rest of the width to Oct 2023 on.
- **New feature for all instances, including Zionism:** clicking a phase card **zooms the x axis to that phase**, with a "Reset to all years" chip. The tug-of-war weeks have dozens of changes per day, and at full range the playhead barely moves. The control strip (changes in order) already helps; zoom completes it.

---

## 3. Small multiple: perpetrator and charge shift (PERP.md)

**Message:** "Same share, graver charge." Israel's share as the named perpetrator barely moved (23.6% → 24.1% → 26.4%, CI crosses zero). What changed is the charge and the voice.

### 3.1 Layout

Top strip, the denominator, so nobody over-reads the grid:
```
Share of harm sentences naming the side as perpetrator   2021   2023   now
Israel / Jews (150 topic leads)                          23.6   24.1   26.4  (change +2.8, CI −1.9 to +8.3: not clear)
Comparison side A (Russia, Azerbaijan…, 50 leads)        32.9   43.5   43.2
```
Then the grid: **rows = charge, columns = side**. Each cell has three short columns (Jan 2021 · Jul 2023 · now). Dark segment = Wikipedia's own voice, pale segment = attributed. Counts sit above each column.

```
                 ISRAEL / JEWS          HAMAS / PALESTINIANS    COMPARISON SIDE A
                 '21  '23  now          '21  '23  now           '21  '23  now
Genocide          0    0  ▆8            0    0    0             ▄4   ▄5   ▄5
                            (2 own)                               (2 own each)
Apartheid         0   ▁1  ▃4            0    0    0              n/a
Ethnic cleansing ▃4  ▃4  ▅6             ·    ·    ·             (from perp_results)
Occupation      35   35   55            –    –    –              8   10   19
                own 46%  51%  80%                               own 25% 70% 74%
Massacre/killing 9   10   26            8    8   24              …
Terrorism        –    –    –            9   10    9              …
                                        own 2    3    4
```
- **Scale:** one shared y scale within each row, so cells are comparable across sides. Rows may differ (occupation counts are 10× genocide). Each row shows its max at the left: "max 55".
- **Encoding:**
  - own voice = `--ink-2` solid, attributed = the same hue at 30% plus a 45° texture, so it survives print and colour-blind viewing;
  - side identity comes from the column header, never from colour. No red-versus-blue partisanship on the page;
  - the "now" column is outlined, the one change readers should look at.
- **Selective labels:** counts on every column (three per cell, so it stays readable); own-voice share only in the occupation row, where the voice shift is the story.
- **Interaction:** tap or click a column to open the **receipts panel**: the exact sentences from `perp_codes.jsonl` for that article × date × side × charge, with the voice code and a link to the revision. Example: the Israel genocide "now" column lists the two own-voice sentences, the Israel article and Netanyahu. For newsrooms, this is the most valuable interaction on the page: every bar has a quote behind it.
- **Pageview toggle** (seg `Articles counted once | Weighted by readers`) for the top strip only. The grid stays in counts, so there is no fake precision on tiny n.
- **Mobile:** the grid transposes. One block per side with tabs `Israel / Jews · Hamas / Palestinians · Comparison`, and the charge rows below, so each cell is full width. The receipts panel opens as a bottom card in the same pinned position as the Zionism controls.
- **Caveat line under the grid** (fixed): "Counts are exact sentences in 150 leads; self-validated coding (98% precision on 100 re-checks); comparison is context, not a matched control."

---

## 4. One interaction grammar for every interactive piece

### 4.1 Controls (identical markup and CSS class names across sections)
| need | control | spec |
|---|---|---|
| move through items in order | **Prev · Play/Pause · Next** + counter "Change 92 of 292" | pinned control card (sticky top 48px and bottom 8px inside the figure). Buttons ≥40px desktop, ≥46px phone. Play only where there is a time order (step timelines). Speeds Normal 1.2 s / Slow 2.6 s. Autoplay pauses on any manual action and when the figure leaves the screen. |
| filter the set being stepped | segmented `.seg` ("Key moves / Every change", "Topic / Comparison", "Groups / Network / Table") | one-line explanation under every seg, always visible, never a tooltip |
| jump to curated moments | **"Jump to" chips**: numbered badge, short label, date | the same numbers appear on the chart as black badges; chips scroll horizontally on phones |
| understand the trend | **phase cards** computed from data, each with a date range and one plain sentence | click = jump to the phase (and zoom, see 2.4). The rule for each boundary is written in the section note. |
| time scope without animation | time-preset chips | dim, never hide; the test scope is stated |
| exact quote behind a mark | **receipts panel** | Before/After word diff, or sentence list, with a revision link |

Keyboard everywhere: ←/→ step, Home/End, Space play/pause (step timelines). Each piece has one polite live region announcing the step. `prefers-reduced-motion`: no glide; Play defaults to Slow.

### 4.2 Legend and colour semantics (site-wide, fixed)
- **Legend style:** plain sentences starting with the colour word, mono 12px, swatch first: "blue: 'colonial' is in the first sentence". Never a bare label. A one-line **"How to read this"** sits above every chart; the legend sits below it.
- **Fixed meanings:**
  - blue `--add-*` = text that is in or was added, or an account that mostly adds critical terms;
  - amber `--del-*` = text that left, or an account that mostly removes them;
  - ink = the current selection or playhead;
  - grey `--mid` = context volume (edits, views);
  - red dashed `--war` = 7 Oct 2023, and nothing else;
  - dotted ghost bar / hollow ring = **what chance gives**;
  - solid dark / pale textured = own voice / attributed;
  - solid / dashed / dotted outline = high / medium / low confidence.
- **Evidence words:** "documented" (ArbCom-recorded), "alleged", "beyond chance", "not detected (test had low power)". Use them in chips and copy exactly as ANGLE.md defines them.
- **Tooltips are optional sugar.** Every tooltip fact is also in the selected-item panel, because phones and screen readers have no hover.

### 4.3 Newsroom affordances (recommended for all pieces)
- **Permalink per state:** `#zionism?k=92`, `#hamas?k=41`, `#coord?g=1`. A "Copy link to this change" button in the diff panel lets journalists cite an exact step.
- **Screenshot-ready card:** the diff panel and receipts panel always carry date (UTC), article, revision number and "English Wikipedia", so a TV screenshot keeps its provenance.
- **Table view** behind every chart (`Show as table`). It is the accessible alternative and the fact-checker's view.

---

## Build order (when approved)
1. Extract `stepTimeline()` from `#zionism`, with no visual change (regression-test with the existing Playwright script).
2. Hamas / October 7 / Gaza genocide tabs, plus the Hamas designation-position card.
3. Perpetrator small multiple with the receipts panel.
4. Coordination: headline strip and Groups cards first (they work with today's schema), Table second, Network tab last (needs layout coordinates and `weekly`).
