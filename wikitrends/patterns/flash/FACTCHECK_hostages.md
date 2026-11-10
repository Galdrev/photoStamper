# Fact check: the hostages, in every Wikipedia edition we hold (card 3 moment)

**Question from the owner:** "the hostages are missing in all languages". This file states how far our stored data supports that, with every exception named.

**Method.** Recomputed from the raw stored files by `patterns/flash/factcheck_hostages.py` (run: `cd wikitrends && python3 -I patterns/flash/factcheck_hostages.py .`; output `patterns/flash/factcheck_hostages.json`). The script does not import the build; it has its own word lists and its own sentence splitter (it strips image-caption residue at the head of a copy, and it splits after a full stop followed by a closing quote, which the Arabic copy needs). The build (`build_flash.py`, "fix log 3" block) then asserts the same facts by its own code, so a data change fails the build.

**Word lists** (stems, case-insensitive): en hostage, captive, abduct, kidnap · de Geisel, entführ, verschlepp · fr otage, enlev, kidnapp, captif · es rehén, rehenes, secuestr, cautiv · it ostagg, rapiment, rapit-, sequestr · pt refém, reféns, sequestr, rapto · nl gijzel, ontvoer, gevangengenomen · pl zakładni, porwan, uprowadz · ru заложни, похищ, пленн · he חטופ, חטיפ, בני ערובה, שבוי · ar رهائن, رهين, أسرى, أسروا, مختطف, محتجز, خطف. The crosswiki counts (below) use an older list that misses Italian "rapimento" and Arabic "أسروا"; we found and corrected for both.

**Stored data used:**
- `patterns/langs/langs.json`: each edition's curated October 7 first sentence, first copy (Jan 2024) and latest copy (Oct 2026), with revision ids, and the "hostages" sentence where we hold it.
- `data/crosslang.json`: 12 quarterly copies (Jan 2024 – Oct 2026) of each edition's October 7 opening section, and 24 quarterly copies (Jan 2021 – Oct 2026) of its Israel and Hamas opening sections. **Each copy holds only the first 1,200 characters.**
- `data/ratchet.json`: all 107 English first sentences of the October 7 article (7 Oct 2023 – 8 Oct 2026).
- `data/mass2_leads.json.gz` and `data/leads.json`: English opening sections (the 2 Nov 2026 crawl copy of October 7; five copies each of Israel and Hamas: Jan 2021, Jul 2023, 1 Oct 2026, the crawl, and the leads file).
- `patterns/crosswiki/chart_data/narrative.json`: counts from the **full** opening sections at four dates (1 Jan 2021, 6 Oct 2023, 7 Oct 2024, 8 Nov 2026). We hold the counts, not the text.

Polish Wikipedia has no article linked to the English October 7 article, so 10 of the 11 editions in our language grid can be checked.

## (a) The October 7 article's first sentence

**In our latest copies (Oct 2026; English 2 Nov 2026), the first sentence names no hostages in 9 of the 10 Wikipedias we hold with an article on the attack. Italian's does.**

| Edition | Latest copy (rev) | Hostages in the first sentence now? | Earlier quarterly copies (12, Jan 2024 – Oct 2026) |
|---|---|---|---|
| עברית (he) | Oct 2026 (44000524) | **No** | **Yes in 5 of 12**: Oct 2024, Jan 2025, Apr 2025, Jul 2025, Oct 2025 ("…תוך ביצוע טבח, אונס, … חטיפת אזרחים, …"). From Jan 2026 the phrase is in sentence 2; in Oct 2026 the abduction of 251 is later in the opening section. |
| العربية (ar) | Oct 2026 (76346544) | No | none of 12 |
| English (en) | 2 Nov 2026 crawl; Oct 2026 (1377629133) | No | none of 12; **none of all 107 versions** (7 Oct 2023 – 8 Oct 2026, `ratchet.json`) |
| Deutsch (de) | Oct 2026 (270436396) | No | none of 12 |
| Français (fr) | Oct 2026 (239902929) | No | none of 12 |
| Español (es) | Oct 2026 (175577194) | No | none of 12 |
| **Italiano (it)** | Oct 2026 (152492999) | **Yes**: "…e nel rapimento di circa 250 di questi…" ("and the kidnapping of about 250 of them") | **Yes in 11 of 12** (every copy from Apr 2024; not in Jan 2024) |
| Português (pt) | Oct 2026 (71897690) | No | none of 12 |
| Nederlands (nl) | Oct 2026 (71996559) | No | none of 12 |
| Русский (ru) | Oct 2026 (155047116) | No | none of 12 |
| Polski (pl) | — | no linked article | — |

Notes:
- The Arabic first sentence is one long sentence: the operation's names, the defining clause we quote (`langs.json` s1, marked with ellipses on the page), the date and the reason its commander gave, ending "…المحتل.»". The captives ("أسروا") are in sentence 2 of our copy.
- The Italian stored text reads "Lattacco" (the apostrophe was lost in our extraction); the page quotes it exactly as stored.
- Jan 2024 copies of Hebrew contain "בכיכר החטופים" in an image caption at the head of the text; that is not the first sentence and is excluded.

**So the owner's sentence, scoped:** "In the first sentence of the October 7 article, in 9 of the 10 Wikipedias we hold (latest copies, Oct–Nov 2026): no hostages. Italian names them. Hebrew named them from our Oct 2024 to our Oct 2025 copy." "Missing in all languages" is **not** supported.

## (b) The October 7 opening section

**All 10 opening sections mention the hostages** (latest copies):

| Edition | Where | Source |
|---|---|---|
| en | sentence 9 only (of 16 by our split; 9 of 14 by the crosswiki split): "251 Israeli and non-Israeli civilians and soldiers were taken as hostages to the Gaza Strip." | 2 Nov 2026 crawl copy (full text) |
| he | "…וחטיפת 251 אזרחים וחיילים – ביניהם קשישים, נשים, ילדים ותינוקות." (sentence 7 of our held text) | held text, Oct 2026 |
| ar | "كما أسروا عددًا من الجنود والمدنيين واقتادوهم لغَزَّة" ("they captured a number of soldiers and civilians and led them to Gaza"): captives, not the word for hostages | held text, Oct 2026 |
| it | sentence 1 | held text |
| nl | "Naar schatting 250-255 personen werden gevangengenomen en als gijzelaars naar Gaza overgebracht." | held text |
| ru | "…ещё 251 были взяты в заложники." (sentence 3) | held text |
| de | first at sentence 9 of 19 (3 mentions) | full-section count, 8 Nov 2026 (beyond our 1,200 characters) |
| fr | sentence 9 of 14 (1) | same |
| es | sentence 6 of 11 (1) | same |
| pt | sentence 8 of 10 (2) | same |

For de, fr, es and pt we hold the count, not the sentence; the page says "beyond the 1,200 characters we hold … (our count, 8 Nov 2026)".

## (c) The Israel and Hamas opening sections

**Israel: no hostage word in any copy we hold, in any edition.** 11 editions × 24 quarterly copies (held text), the 5 English full copies, and the full-section counts at 4 dates for 10 editions (Italian Israel is not in the crosswiki counts).

**Hamas: not "none in every copy".** Exceptions, all named:

| Edition | What we hold |
|---|---|
| **en** | **Our April 2024 (rev 1215960969) and July 2024 (rev 1231763808) copies said "The ongoing 2023 war began after Hamas launched [a surprise] attack …, and taking hostages back to Gaza."** Not in Jan 2021, Jul 2023, Oct 2024 onward, 1 Oct 2026 or the crawl copy. |
| it | Jan 2025 copy: "…e il rapimento di 254 civili, tenuti poi in ostaggio nella striscia di Gaza." Full-section count: 1 mention at 7 Oct 2024 and 8 Nov 2026 (sentence 9 of 10 now). |
| he | From the Jul 2025 copy: "…מבצע פיגועים, ירי רקטות, חטיפות ופעולות טרור אחרות…" (kidnappings as one of Hamas's methods; not the October 7 hostages specifically). |
| es | Full-section count: 1 mention at all four dates, from 2021 (beyond our text; content not held, so not attributable to October 7). |
| pt, ru | Full-section count: 1 mention from 7 Oct 2024 (beyond our text). |
| ar, de, fr, nl, pl | none |

**Consequence for the flash page (fixed in step 2):**
- The card 3 caption said "Israel and Hamas opening sections: none, in every copy we hold since 2021", and "In short" said "in every copy we hold, the Israel and Hamas opening sections do not mention the hostages". **Both overstated for Hamas** (`messaging_check.md` F3 scoped this to four snapshots; the page's wording claimed every copy, and our quarterly copies include April and July 2024).
- Now: "In short" says "in our latest copies"; the English panel of the moment says "Israel’s opening section: none, in every copy we hold since 2021. Hamas’s: none now; our April and July 2024 copies said “taking hostages back to Gaza”."
- **The research edition is unchanged (byte-identical, as required)** and still says, for example, "Neither the Hamas nor the Israel opening section mentions the hostages." That is true of the four snapshots it reads (Jan 2021, Jul 2023, 1 Oct 2026, now) but not of our April and July 2024 Hamas copies. The owner should decide whether to add the 2024 exception there.

## Numbers on the page, checked

| On the page | Recomputed | Source |
|---|---|---|
| 251 (huge numeral; sentence 9) | sentence 9 of the 2 Nov 2026 copy, the only one with a hostage word | mass2_leads |
| 9 of 10 | 9 editions without, 1 (it) with, of 10 with an article | langs.json latest s1 |
| Hebrew Oct 2024 – Oct 2025 | 5 quarterly copies with "חטיפת אזרחים" in sentence 1; none from Jan 2026 | crosslang.json |
| 107 versions (H2) | 107 variants, none with a hostage word | ratchet.json |
| sentence 9 of 19 / 9 of 14 / 6 of 11 / 8 of 10 | de / fr / es / pt | crosswiki narrative.json, 8 Nov 2026 |
| April and July 2024 Hamas copies | revs 1215960969, 1231763808 | crosslang.json |

All match. Build assertions added (`build_flash.py`, "fix log 3"): the ten editions and their order; only Italian filled; each panel quotes the stored first sentence whole; the Hebrew 2024–25 window; Italian since Apr 2024; no hostage word in any quarterly first sentence of the other eight; English sentence 9; the English Israel and Hamas copies (Hamas exactly Apr and Jul 2024); the four full-section positions; every opening section mentions them; the old overstated lines are absent. The smoke suite adds an in-page recount: only the Italian panel's sentence matches the hostage words.
