# Integration spec: "In their own words" inside `#crosslang`

Goal: in the report's existing `#crosslang` section, let a reader pick an article and a language and read the actual sentences, then and now. The reader sees the original next to our English translation, with the changed words marked in both, and a badge for how the claim is voiced. This sits on top of the current colour stripes, which stay as the quantitative view. No page edits have been made; this is a spec only.

Data: `patterns/langs/langs.json` (built from `data/crosslang.json`; see `LANGS.md`).

---

## 1. Data plumbing (`build_page.py`)

Load the file next to the other optional inputs and slim it. The page needs about 150 KB, not the full file.

```python
lp = os.path.join(HERE, "patterns", "langs", "langs.json")
if os.path.exists(lp):
    L = json.load(open(lp))
    keep = lambda X: {k: X[k] for k in ("title", "first", "latest", "headline_claim", "key_changes", "slots") if k in X}
    for a, AA in L["articles"].items():
        for l, X in AA.items():
            hc = X.get("headline_claim") or {}
            want = {"s1", hc.get("evidence_slot")}
            X["slots"] = {k: v for k, v in X["slots"].items() if k in want}
            X["key_changes"] = X["key_changes"][:3]
            AA[l] = keep(X)
    res["langs"] = {"meta": {k: L["meta"][k] for k in ("voice_codes", "lang_order", "translations")}, "articles": L["articles"]}
```

Shape used by the page (one article × language):

```json
{"title": "ציונות",
 "first":  {"date": "2021-01", "revid": 29828968, "term_counts_full_lead": {"colonial": 0, ...}},
 "latest": {"date": "2026-10", "revid": 43883308, ...},
 "headline_claim": {"claim": "colonization / colonial framing", "first": "absent", "latest": "absent", "evidence_slot": "s1"},
 "key_changes": [{"from_orig": "מדינה יהודית", "from_gloss": "a Jewish state", "to_orig": "בית לאומי לעם היהודי", "to_gloss": "a national home for the Jewish people", "note": "..."}],
 "slots": {"s1": {"first": {"orig": "...", "tr": "...", "voice": "none", "terms": [...], "truncated": false},
                  "latest": {...},
                  "diff": {"orig": {"removed": [{"start": 46, "end": 70, "text": "..."}], "added": [...]},
                           "tr":   {"removed": [...], "added": [...]}, "voice_change": "none -> none"}}}}
```

**Offsets.** The builder writes Python code-point offsets. JavaScript strings index by UTF-16 code units. Today's data has no characters outside the BMP, so the two agree. Add a build-time assert (`all(ord(c) < 0x10000 for c in s)`), or emit UTF-16 offsets, so a future emoji or rare CJK character cannot shift the marks.

---

## 2. Placement and order inside `#crosslang`

```
<section id="crosslang">
  header (eyebrow, h2, deck)              ← deck text updated, see §8
  #xlFind   three finding quotes            ← NEW (reuses .news-q)
  #xlWrap   picks + stripes + #xlPane       ← existing
  #xlRead   "In their own words" reader     ← NEW, directly under #xlPicks, above the stripes
</section>
```

- The existing article picks (`#xlPicks`, `.pick`) drive both the stripes and the new reader. Add `S.xlRL` (reader language) beside `S.xlL`. Picking a stripe sets both, so the views stay in sync.
- Restrict the reader's article list to the nine in `langs.json`: Zionism, Israel, Nakba, Hamas, October 7 attacks, Gaza war, Gaza genocide, Israeli apartheid, West Bank. For other picks, show `.note`: "Sentence-level reading is available for the nine key articles."

---

## 3. Language switcher

- Component: the page's `.seg` (as used by `#ziMode`, `#ziSpeed`), labelled `id="xlLangL"` "Language".
- Order is fixed: **Hebrew, Arabic**, then English, German, French, Spanish, Italian, Portuguese, Dutch, Polish, Russian (`meta.lang_order`).
- Button label: the native name plus the code, with the native name in its own script and direction:
  `<button data-l="he" aria-pressed="true"><bdi lang="he" dir="rtl">עברית</bdi> <span class="code">he</span></button>`
  Native names: עברית, العربية, English, Deutsch, Français, Español, Italiano, Português, Nederlands, Polski, Русский.
- Missing article: `disabled`, hatched like `.stripe.na`, with `title` text such as "No Hebrew article is linked to English 'Gaza genocide'". `meta.missing_articles` lists them (de/he/ru for Gaza genocide; it for Nakba is a redirect; pl for October 7; de/it for apartheid).
- Default: Hebrew. If the article has no Hebrew version, use Arabic, then English. Show a one-line `.cap` saying why.
- Keyboard: roving `tabindex` with Left/Right and Home/End, as in the `#ziChart` arrow-key pattern. `aria-pressed` on the active button.
- Each button carries a 6px dot after the code showing the latest voice (§4 colours) so that the pattern across languages shows before any click. The dot needs a text equivalent in `aria-label`: "Hebrew, terror label stated as fact".

---

## 4. Voice badge

One badge per copy, shown as **then → now** above the pair: `<span class="vb vb-attributed">attributed</span> → <span class="vb vb-fact">stated as fact</span>`. The claim it refers to comes from `headline_claim.claim` and is printed before the badges ("Genocide:", "Colonization:", "Terror label:").

| code | badge text | style (reuse existing tokens; no new colours) |
|---|---|---|
| fact | stated as fact | `background:var(--ink); color:var(--paper)` |
| attributed | attributed | `background:var(--sheet); border:1px solid var(--ink-2); color:var(--ink-2)` |
| disputed | disputed in the same sentence | same as attributed, `border-style:dashed` |
| denial | denial reported | outline `var(--muted)` |
| legal | court case only | outline `var(--muted)`, mono text |
| label | "a term in use" | outline `var(--muted)`, italic |
| self | the group's own words | outline `var(--muted)` |
| absent | not in the lead | hatched, like `.stripe.na` |
| outside | later in the lead (not quoted) | `color:var(--muted)`, dotted outline, with the count: "1 mention beyond our text" |
| not_held | not in our text | as `outside`, without the count |

- Base: the `.chip` geometry (`font:500 10.5px/1.5 var(--mono)`, radius 2px), but sentence-case text, not uppercase. Every state carries text, so colour is never the only signal.
- Don't reuse `--topic`/`--comp` (those mean topic/comparison group) or `--del-*`/`--add-*` (those mean removed/added words).
- Tooltip (`#tip`): the `meta.voice_codes` definition.

---

## 5. The pair: original and translation side by side, changes marked in both

Reuse the Zionism styling: `.wow-grid`, `.wow-col`, `.wow-col .when`, and the `del`/`ins` rules at `.wow-s del/.xl-text del` (amber struck-through = removed, blue = added). Add `.xl-read` to the selector lists at lines ~107–108 so the same marks apply.

Desktop (≥ 900px): a 2 × 2 grid.

```
              ORIGINAL (lang, dir)                 OUR TRANSLATION (en)
THEN · 2021-01 · rev ↗   <p class="xl-o"> …<del>…</del>… </p>   <p class="xl-t"> …<del>…</del>… </p>
NOW  · 2026-10 · rev ↗   <p class="xl-o"> …<ins>…</ins>… </p>   <p class="xl-t"> …<ins>…</ins>… </p>
```

- Column heads: "Original · Hebrew" and "Our translation". The translation head always carries the word **ours** (accuracy rule).
- Row heads: reuse `.wow-col .when`, with the date and a link `https://{lang}.wikipedia.org/w/index.php?oldid={revid}` (same pattern as `xlShow`).
- Marks: build the HTML from `diff.orig.removed` (THEN row, original), `diff.orig.added` (NOW row, original), `diff.tr.removed` and `diff.tr.added` (translation cells). Slice by the spans; escape every slice with `esc`. Don't re-diff in the browser, so the page shows exactly what was checked.
- When `diff.unchanged` is true, show both rows unmarked plus a `.cap`: "Same words in 2021 and 2026."
- When a copy is missing (Polish apartheid starts in 2026; the war articles start in 2024), say "First copy: 2024-01" in the row head. If there is only one copy, show one row and "Only one copy".
- When `truncated` is true, end with `…` and a `.cap`: "Cut at the 1,200 characters we hold."
- Type: original at `font:400 18px/1.6 var(--display)`. Translation at `16px/1.55 var(--body)` in `var(--ink-2)`, so it reads as secondary.
- Slot switcher: if `headline_claim.evidence_slot` is not `s1`, show a small `.seg` above the grid: "First sentence | The key sentence". The key sentence is labelled with the claim, e.g. "The 'genocide' sentence".

Under the grid:

- **Key words** chips: reuse `.zi-chips` (`<li><del>orig</del> → <ins>orig</ins></li>`). Under each chip add a second line in `.cap`: "our gloss: *a Jewish state* → *a national home for the Jewish people*", followed by `note`.
- **What the words carry**: a `details.stats` disclosure listing `terms` (original · literal gloss · connotation), e.g. «תפיסה לוחמתית» · belligerent occupation · legal term of art, avoids «כיבוש».
- **Counts**: keep the existing per-term table, but label it "Counted in the whole opening section". Flag any term counted there but absent from the quoted text.

`aria-live="polite"` on the grid container; on change, announce "Hebrew, Zionism, first sentence, 2021 and 2026".

---

## 6. RTL handling (Hebrew, Arabic)

- Every original cell: `lang="{l}" dir="rtl"` for he/ar (else `dir="ltr"`), plus `unicode-bidi:isolate` and `text-align:start`. Don't use `unicode-bidi:plaintext` here. The direction is known, and plaintext can flip a cell whose first strong character is Latin (e.g. a sentence that opens with "ICJ").
- Translation cells stay `lang="en" dir="ltr"`.
- Keep the grid's column order fixed (Original | Translation) for every language, so switching never moves the layout. RTL text right-aligns inside its cell.
- Inline Hebrew or Arabic inside English text (chips, deck, finding quotes): wrap it in `<bdi lang="he">…</bdi>` so neighbouring punctuation and numbers stay in place.
- Quotation marks: don't wrap RTL originals in English quote characters. The cell is the quote. In chips use `«…»` inside the `bdi`.
- `del`/`ins` in RTL: the struck-through line works for Hebrew. For Arabic, it can cut through dots and diacritics, so set `[lang=ar] del{text-decoration-thickness:1px; text-decoration-skip-ink:none}` and keep the amber background as the main cue. `padding:0 .08em` is fine, because inline padding is symmetric.
- Fonts: extend `--display` with `"Noto Serif Hebrew","Frank Ruhl Libre"` and `"Noto Naskh Arabic","Amiri"` fallbacks, with system serif last. Give Arabic `line-height:1.8`, because vowel marks (e.g. «الصِّهْيَوْنِيَّة») need the room.
- Numbers and Latin runs inside RTL (dates, "ICJ", "Human Rights Watch") need no markup when the cell has `dir="rtl"`. Spot-check the Hebrew Gaza-war ICJ sentence and the Arabic Gaza-genocide numbers.
- Test in Chrome, Safari iOS and Firefox, in light and dark themes.

---

## 7. Mobile (< 640px, `isPhone()`)

- The language `.seg` becomes one horizontally scrolling row (`overflow-x:auto; scroll-snap-type:x mandatory; flex-wrap:nowrap`), with `min-height:40px` buttons (as `.zi-opts .seg button`). Fade the right edge to show the row scrolls (the page is LTR, so no mirroring is needed). Hebrew and Arabic are first, so they show without scrolling.
- The 2 × 2 grid stacks into one column, in the same order as the Zionism pair on phones (lines ~631–632): **Then: original → Then: our translation → Now: original → Now: our translation**. Add `border-top:1px solid var(--rule)` between the Then and Now blocks. Each cell keeps a small label ("Then · original · עברית").
- Collapse the translation behind "Show our translation" (`details`), open by default for he/ar (so a non-reader is never stuck) and closed for Latin-script languages.
- Voice badges sit on their own line under the language row, wrapping if needed.
- The reader is visible by default on phones. The existing rule that hides `#xlPane` until a stripe is tapped stays as it is.
- `max-height` with internal scroll is only for the stripe pane (`.xl-text`). Let reader cells grow, because the quotes are a sentence or two.

---

## 8. Copy for the section

Deck (replace the current one). Every clause is checked in `LANGS.md`:

> Mostly not in vocabulary counts, but the words tell a sharper story. Spanish, Portuguese and Arabic now define the "Gaza genocide" in their own voice, as English does. Dutch and Polish pulled back, and Hebrew mentions only South Africa's court case. "Colonization" entered the Zionism definition in English, Arabic, Portuguese, Italian and Dutch. Hebrew, German, French, Spanish, Polish and Russian kept it out. Arabic turned apartheid from "an accusation" into "a confirmed fact". Pick an article and a language to read the sentences, then and now, in the original and in our translation.

`#xlFind`: three `.news-q` blockquotes, original plus translation, each with its date. Use the es Gaza war "genocide" sentence, the ar apartheid "confirmed fact" pair and the he October 7 retitling («מתקפת הפתע» → «טבח»). Label them "Spanish · Gaza war · 2026" etc., and put the native script in `<bdi>`.

Method line (`.means`), under the reader:

> **How to read this:** the sentences are quoted exactly from each Wikipedia's opening section at the first and latest quarterly copy. We hold the first 1,200 characters; words beyond that are counted but not quoted. Translations are ours, kept close to literal. Amber struck-through = words removed; blue = words added, marked in the original and in the translation.

---

## 9. Checks before shipping

1. For each displayed `orig`, `latest.lead.includes(orig)` against `crosslang.json`. The builder already asserts this (333/333), so re-run it on rebuild.
2. Spans: `orig.slice(start, end) === text` for every span in both strings.
3. RTL: screenshots of he and ar at 360px and 1280px, light and dark.
4. Keyboard only: picks → language seg (arrows) → slot seg → links.
5. Screen reader: `del`/`ins` get visually hidden prefixes "removed:" / "added:" (`.sr` class with `::before`), as browsers do not announce them by default.
6. The deck's claims match the badges shown, for the default state and for each of the nine articles.
