# Fact check: the new numbers and quotes since the last checked build (merge round and final round)

**Method:** every number was recomputed from the raw sources with code written for this check (`scratchpad/s5/fc.py`, `tm.py`, `fb.py`). That code does not read `exposure.json` or the build. The recomputed values were then compared with what the page prints, in English and in Hebrew.

**Sources:**
- daily views and revision histories: `wikitrends-data:views/42651558741/views/` (the six hero articles) and `views/42704500939/views/` (Benjamin Netanyahu, Palestine);
- `data/leads.json` (the Jan 2021 leads);
- `data/mass2.json` and `data/mass2_leads.json.gz` (the treemap);
- `patterns/angle/perp_codes.jsonl` (the charge per opening);
- the research data `res["ratchet"]` (the Zionism sentence history behind the fight lanes).

**Result:** every number matches. Nothing was wrong, so nothing on the page was corrected. Two new build assertions now pin the numbers the page computes at run time (§4).

## 1. Reach bars and shares (window 9 Nov 2025 – 8 Nov 2026, daily sums, agent=user)

| Article | Recomputed views | Page | Recomputed share | Page | Bar width (views ÷ Netanyahu) |
|---|---|---|---|---|---|
| Benjamin Netanyahu (new) | 7,940,343 | 7.9 million | 100% ("genocide" in the opening section) | 100% | 100.0% |
| Israel | 5.056M | 5.1 million | 100% | 100% | 63.7% |
| Palestine (new) | 2,641,678 | 2.6 million | 100% | 100% | 33.3% |
| Zionism | 2.098M | 2.1 million | 99.88% | 99.9% | 26.4% |
| October 7 attacks | 2.008M | 2.0 million | 100% | 100% | 25.3% |
| Gaza genocide | 1.682M | 1.7 million | 99.34% (own voice) | 99.3% | 21.2% |
| Hamas | 1.463M | 1.5 million | 95.10% | 95.1% | 18.4% |
| Nakba | 0.616M | 0.6 million | 30.34% | 30.3% | 7.8% |

**Key figures:**

| Figure | Recomputed | Page |
|---|---|---|
| Israel, share with "began committing genocide" | 92.59% | 92.6% |
| Netanyahu, share with "orchestrating the Gaza genocide" (live since 29 Sep 2026) | 13.61% | 13.6% |
| Palestine, share with "recognised as constituting genocide" (live since 3 Jun 2026) | 40.97% | 41.0% |
| Nakba, share with another "ethnic cleansing" wording | 69.65% | 69.7% |

**Two notes:**
- **Palestine.** The views count "State of Palestine" from the start and "Palestine" from the move on 7 Jan 2025 20:06. Before the move, "Palestine" was a different page. This is the same rule as for the hero articles' moves, and the build asserts it.
- **"Nearly every view … except Nakba".** Seven of the eight bars are at or above 95%. Nakba is below 50%. The build asserts both.

## 2. The surge line (7 Oct – 31 Dec 2023)

| Article | Recomputed | Page |
|---|---|---|
| Israel | 9.319M views, 99.09% with no "genocide" in the opening section | "9.3 million views, 99.1% with no genocide charge" |
| Hamas | 10.222M views, 0.000% with "political organisation with a military wing" | "10.2 million, none with “political organisation”" |
| Netanyahu, Palestine (not on the page) | 3.46M and 8.75M views, 0% with "genocide" | (not on the page) |

**Placement:** in the final round the surge line moved into the collapsed key ("What counts as the critical wording · the October 2023 surge"). Its text is unchanged.

## 3. The treemap

| Claim on the page | Recomputed | OK |
|---|---|---|
| The 150 most-read topic openings with a lead at all three dates | 150. Israel's views since 2021 are 42,920,851, as in PERP.md | yes |
| Area = views Nov 2025 – Oct 2026 (monthly sums) | The last 12 of the 70 monthly values (Jan 2021 – Oct 2026) are Nov 2025 – Oct 2026 | yes |
| "Jan 2021 and Jul 2023: none charged Israel with genocide" | No charge clause (Israel, genocide, not a denial) is dated 2021-01 or 2023-07 | yes |
| "Now 7 of 150 do" | 7: Israel, Benjamin Netanyahu, Palestine, Gaza Strip, Israeli–Palestinian conflict, Israel Defense Forces, Gaza–Israel conflict | yes |
| "two as fact" | Israel and Benjamin Netanyahu (`wikipedia_voice`) | yes |
| "12% of the views of all 150" | 16.79M of 135.34M = **12.41%**, printed as 12% | yes |

**Different sources for the same article:** the treemap's Netanyahu tile (monthly sums, Nov–Oct) and the Netanyahu reach bar (daily sums, 9 Nov – 8 Nov) use different sources and windows, as the key says. They are not meant to match.

## 4. The fight lanes (#flFb, the Zionism first sentence)

The page computes these at run time (`fbBuild`). They were reimplemented in Python from the same stored history: 293 steps, 264 fought-over phrases.

| On the page | Recomputed |
|---|---|
| "100 words fought over since Jan 2021" | 100 single words fought over |
| "colonization" ⇄81 | 81 |
| "land outside" (of) Europe ⇄54 | 54 |
| "Palestine, a region" ⇄40 | 40 |
| "Land of Israel" ⇄40 | 40 |
| "Jewish history" ⇄37 | 37 |
| "homeland" ⇄35 | 35 |
| "Jewish people" ⇄35 | 35 |
| "Jewish state" ⇄29 | 29 |

**The lane states match the legend:**
- added since 2021: colonization, Jewish history, homeland;
- not in Jan 2021 and not now, fought over in between: land outside, Palestine, a region;
- as in Jan 2021: Land of Israel;
- removed: Jewish people, Jewish state.

**New build assertions (`build_flash.py`, step 5 block):**
- the Python recount must give exactly these 100 words and these 8 lanes and counts;
- the treemap share must round to 12.4%.

The smoke test separately recounts the lanes on the rendered page, at rest and at three sweep dates.

## 5. Quotes added since the last checked build

| Quote | Source checked | OK |
|---|---|---|
| “orchestrating the Gaza genocide” (reach key) | Netanyahu opening section, stored lead (`data-q` en:Benjamin Netanyahu). The build's quote check passes | yes |
| “recognised as constituting genocide” (reach key) | Palestine opening section, stored lead. The build's quote check passes | yes |
| The seven treemap charge sentences | Each is asserted to be a substring of the stored lead (`norm(s) in norm(M2[k][2])`) | yes |
| The Hebrew translations of the treemap sentences | Checked for fidelity in `HE_FIXLOG2.md` §2. Three corrected: agency in Palestine, "as constituting" in Gaza Strip, "abuses" and "multiple" in IDF | yes |

## 6. The Data lab

The lab prints only data that the research edition's lab prints, unchanged: per-wording live days and views, change counts, and loaded-word rates. It uses the same code (`lab_flash.py` only patches the chrome and the missing-data notes) on a subset of the same data.
- The slim set has 15 flipbook articles and 12 prism articles.
- It holds only the flash's own articles: the six hero articles and the treemap's 150.
- `lab_flash.data()` asserts both.
