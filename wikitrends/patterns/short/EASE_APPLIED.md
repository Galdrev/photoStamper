# Ease-text edits: applied log

Source: `EASE_TEXTS.md` (25 edits, priority order). Target: `page_template.html` (text only; no chart code, layout, colours or scrolly mechanics changed).
Date: 2026-11-05. Result: **25 applied, 0 skipped.**

| # | Where | Status | Note |
|---|---|---|---|
| 1 | Scrolly heading `#keyH` | Applied | |
| 2 | Scrolly deck | Applied | Step-card text and the chart's own title inside `drawKey()` left as is (chart). |
| 3 | "The twist" deck | Applied | |
| 4 | "The twist" heading | Applied | |
| 5 | Reach deck | Applied | |
| 6 | Reach "What this means" (`drawReach()`) | Applied | Only the `#mReach` string; the bars and legend are untouched. |
| 7 | Israel quote label (`drawNews()`) | Applied | Label text only. |
| 8 | Nakba quote label (`drawNews()`) | Applied | Label text only. |
| 9 | EPISTEMICS chip + description | Applied | All 5 chips (`#chance`, `#board`, `#sourcing`, `#checks`, layer key) now read SOURCES; the CSS class `layer epistemics` (dashed border) is unchanged. |
| 10 | "What this study can tell you", item 1 | Applied | |
| 11 | "When it happened" heading `#whenH` | Applied | |
| 12 | "When it happened" deck | Applied | |
| 13 | Half-year bars title and note | Applied | HTML caption only; the SVG and its aria-label are unchanged. |
| 14 | `#mWhen` | Applied | |
| 15 | "News or narrative?" deck | Applied | |
| 16 | "News or narrative?" figure labels | Applied | Title, note and the two labels under the bar; the 89/11 bar itself is unchanged. |
| 17 | "News or narrative?" caption | Applied | |
| 18 | `#mNews` caution | Applied | |
| 19 | "How it spread" heading `#spreadH` | Applied | |
| 20 | "Established editors" panel text | Applied | |
| 21 | "Links come before words" panel + RfC heading | Applied | `+5.6 points` / `with the same amount of editing`; RfC tile heading. Tile charts unchanged. |
| 22 | `#mSpread` | Applied | |
| 23 | "What we checked and dropped", newcomer item | Applied | |
| 24 | Ratchet heading + vocabulary deck | Applied | |
| 25 | Article table caption + sourcing deck | Applied | Also renamed the two table headers ("Loaded words, first" -> "Critical vocabulary, first"; "History words, first" -> "Jewish-history vocabulary, first") so the caption's definitions still match the column names. |

## Consistency edits outside EASE_TEXTS (task step 3)

- `notes/takeaways.json` (the "60-second version" cards): headlines shortened so they no longer repeat the new top section word for word; "loaded words" -> "critical vocabulary", "lead" -> "opening paragraph". Numbers, bars and anchors unchanged.
- `findings.html`: "narrow, heavily read core" -> "small set of heavily read pages", "crawled" -> "collected every article", "leads" -> "opening paragraphs"; "The picture in five sentences" renamed "The longer version" and its items trimmed where they repeated the top cards. The statistics toggle is unchanged.

## Not changed on purpose

- Chart-internal text drawn in SVG (axis labels, aria-labels, the scrolly chart title "Loaded words per 10,000 words", the cross-language and ratchet chart captions), because they belong to the charts.
- `#breathe` and `#crosslang` headings/decks (as EASE_TEXTS says).
