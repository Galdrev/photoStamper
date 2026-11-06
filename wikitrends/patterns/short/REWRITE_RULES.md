# Rewrite brief: make every sentence readable (2026-11-06)

The owner says the report's texts are not readable. The facts are right, but too many sentences are dense, nested, full of qualifiers, or packed with several numbers at once. Your job is to rewrite the TEXT so a smart, critical reader understands each sentence on the first read.

## Keep exactly
- Every fact, number, interval, date and quote. Quotes from Wikipedia stay character-for-character.
- The strength of every claim. Don't make anything stronger or weaker. Keep words like "suggestive" or "within the margin of error" where they appear, but say them simply.
- The register: academic-adjacent, calm, neutral, popular-data-science style (see /home/user/photoStamper/wikitrends/patterns/short/STYLE_GUIDE.md). No slogans, no hype, no em dashes.
- All HTML markup, classes, ids, attributes and JS logic. Change only human-readable text. Inside JS, change only string literals that are shown to readers. Never change variable names, data keys or template placeholders such as ${...}. Keep any ${...} expression exactly as it is, inside your new text.

## How to write
- One idea per sentence. Most sentences under 20 words.
- Lead with the point, then the evidence.
- At most one number per sentence, two if it's a direct comparison ("9% vs 17%").
- Use the reader's words: "opening paragraph", not "lead"; "compared with similar articles on other topics", not "DiD"; "range we're fairly sure about", not "CI".
- Cut nested clauses, parentheticals inside parentheticals, and semicolon chains.
- Headings say what the section shows, plainly.
- Keep it roughly the same length or shorter. Don't add new content.

## Output
Write a JSON file (path given in your task): a list of {"file": "...", "old": "...", "new": "...", "note": "..."}.
- "old" must be an exact substring of the current file and unique in it. Include enough context to be unique, but replace whole sentences or text nodes, not fragments of words.
- Do not overlap with other edits.
- Check every "old" with a script before you finish: each must occur exactly once in its file. Report any that don't.
- Don't edit the files yourself, and don't commit.
