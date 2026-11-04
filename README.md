# WikiTrends: framing drift in Wikipedia articles on Judaism, Israel and Zionism

## Hypothesis
**H1.** Since 2021, and faster since October 2023, English Wikipedia articles on Judaism, Israel and Zionism
have shifted toward an anti-colonial framing: more "settler-colonial", "apartheid", "genocide",
"ethnic cleansing", "occupation" and "Nakba/expulsion" language, and less language about Jewish
indigeneity, homeland, self-determination and antisemitism. The shift is larger than in comparable
articles, and it shows most in the lead sections.

**H0 (null).** Changes in these articles match those in comparable articles about other nations,
national movements, religions and conflicts, or they follow real-world events
(the 2023–present Gaza war, ICJ proceedings) that every encyclopedia would cover.

## Method
1. **Corpus**: about 150 hand-picked treatment articles plus up to 350 more sampled from Zionism,
   antisemitism, conflict and Jewish-history categories. About 80 control articles cover other
   nationalisms, states, conflicts, genocides and religions.
2. **Data** (Wikipedia API plus Wikimedia pageviews): every revision since 2021-01-01, with time,
   editor, size, tags and reverts; quarterly full-text snapshots; talk-page activity; monthly views.
3. **Measures**: frame-term rates per 10k words, counted in the full text and in the lead;
   the first sentence (the definition) over time; lead diffs; edit, revert and talk volume;
   how concentrated the editing is.
4. **Test**: difference-in-differences (treatment change minus control change), with bootstrap 95% CIs,
   for the whole window, before the war and after it.

Term frequency is a proxy. It is not a verdict on accuracy or bias. Editor data is reported only in aggregate.

## Run
```
cd wikitrends && pip install requests && python fetch.py && python analyze.py
```
