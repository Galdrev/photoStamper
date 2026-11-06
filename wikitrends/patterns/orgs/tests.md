# Tests of organisational footprints

Script: `patterns/orgs/org_tests.py`. Output: `patterns/orgs/org_tests.json`. The footprints and their predicted directions were written in `footprints.json` before the script was run. Seed 20261106; 2,000 placebo dates.

**Bottom line.** No initiative leaves a footprint in our lead data that we can tell apart from chance:
- No single date passes a 5% test in its main specification.
- The joint test of the five exposure and sanction dates is flat.
- Three results point the predicted way and are suggestive at best: the Jan 2024 pro-Israel canvassing motions (removals), PIA5 (insertions), and the Apr 2025 site bans (8-week window only). None would survive correction for the 13 primary tests.
- The data are thin, so only very large effects would show. A one-sided 5% test on 4-week topic insertions needs the topic/comparison ratio to fall to **0.20×** or rise to **4.2×**. This is a low-power design, not evidence of no effect.

The firmest result is about timing. The surge in critical-term insertions came **before** the documented and alleged campaigns. Topic insertions ran at 3.4× the comparison rate in the 16 weeks from 7 Oct 2023 to 1 Feb 2024, before the Tech for Palestine channel is reported to have begun. During the channel's reported active period the ratio was 2.0×. After its exposure it was 1.8×.

## Data and method

- **Events.** Critical-term insertions and removals in article leads, from `data/mass2_events.json.gz`, grouped as topic (4,642 articles) or comparison (5,678). That is 5,053 critical-term events. Terms: settler-colonial, apartheid, genocide, ethnic cleansing, occupation, Nakba/expulsion, war crimes.
- **Weekly edits.** Deep panel, `data/results.json`: 411 topic and 85 clean comparison articles that existed before 2021.
- **Statistic.** S = log((T_post+1)/(T_pre+1)) − log((C_post+1)/(C_pre+1)).
  - T counts topic events and C counts comparison events.
  - The pre window is the 4 weeks before the date. The post window is the date's week plus the 3 weeks after.
  - The table reports exp(S) as "ratio": below 1 means topic activity fell relative to comparison.
- **p-values.** One-sided, in the predicted direction:
  - *global*: against 2,000 random dates from Jul 2021 to Sep 2026;
  - *local*: against dates within ±26 weeks of the event.
- **Sensitivity checks.** 8-week windows, and non-reverted events only.
- **Limits of what can be seen.** Account hashes link edits only within one article. The data cannot see:
  - who an account belongs to;
  - talk-page and RfC votes, which are where canvassing is usually alleged;
  - text outside the lead.

## Results: event dates

| Test | Date | Predicted | Topic pre→post | Comp. pre→post | Ratio (4w) | p global / local | 8w ratio (p g/l) | Non-reverted 4w (p g/l) |
|---|---|---|---|---|---|---|---|---|
| F1a TfP channel created (Jan 2024; month only) | 2024-01-15 | ↑ ins | 39→46 | 12→19 | 0.76 | 0.64 / 0.74 | 0.72 (0.68/0.84) | 1.11 (0.47/0.44) |
| F1a sensitivity | 2024-01-01 | ↑ ins | 39→57 | 9→19 | 0.72 | 0.67 / 0.72 | 0.69 | 1.06 |
| F1a sensitivity | 2024-02-01 | ↑ ins | 57→28 | 19→13 | 0.71 | 0.67 / 0.76 | 0.71 | 1.42 (0.33/0.33) |
| F1b Pirate Wires exposé | 2024-10-24 | ↓ ins | 35→32 | 19→28 | 0.63 | 0.24 / 0.28 | 0.65 (0.25/0.29) | 0.96 |
| F1c first ArbCom sanctions tied to the channel | 2024-12-09 | ↓ ins | 24→53 | 13→11 | **2.52 (wrong way)** | 0.88 / 0.89 | 3.36 | 2.12 |
| F2 ArbCom "PIA canvassing" motions (pro-Israel email canvassing) | 2024-01-20 | ↓ rem | 39→28 | 12→18 | 0.50 | 0.16 / **0.065** | 0.58 (0.20/**0.026**) | 0.35 (0.12/0.065) |
| F3a PIA5 closed: insertions | 2025-01-23 | ↓ ins | 44→18 | 6→7 | 0.37 | 0.105 / **0.065** | 0.46 (0.15/0.16) | 0.55 (0.23/0.17) |
| F3a PIA5: removals | 2025-01-23 | ↓ rem | 34→17 | 6→4 | 0.72 | 0.34 / 0.28 | 0.48 (0.13/0.105) | 1.09 |
| F3a PIA5: all flips | 2025-01-23 | ↓ | 78→35 | 12→11 | 0.49 | 0.18 / 0.17 | 0.46 (0.11/0.08) | 0.74 |
| F3a PIA5: deep-panel weekly edits | 2025-01-23 | ↓ edits | 2120→1976 | 892→999 | 0.83 | 0.26 / 0.20 | 0.79 (0.26/0.13) | n/a |
| F4a ADL "Editing for Hate" | 2025-03-18 | ↓ ins | 22→32 | 20→11 | **2.51 (wrong way)** | 0.88 / 0.85 | 1.11 | 3.94 |
| F4b private-case site bans | 2025-04-25 | ↓ ins | 10→10 | 11→16 | 0.71 | 0.33 / 0.30 | 0.32 (**0.051/0.026**) | 0.43 (0.15/0.22) |
| F5b Euro-Med WikiRights round 2 | 2021-11-01 | ↑ ins | 6→2 | 21→12 | 0.73 | 0.64 / 0.74 | 0.75 | 1.08 |
| F5a Euro-Med WikiRights round 3: "genocide" insertions | 2026-02-16 | ↑ | 1→1 | 2→4 | 0.60 | 0.71 / 0.63 | 1.71 (0.30/0.21) | n/a |
| Deep-panel edits at the exposé | 2024-10-24 | ↓ edits | 3004→1919 | 1384→1068 | 0.83 | 0.24 / 0.17 | n/a | n/a |
| Deep-panel edits at the channel start | 2024-01-15 | ↑ edits | 1903→2010 | 1103→1076 | 1.08 | 0.43 / 0.35 | n/a | n/a |

**Joint test.** We averaged S over the five exposure and sanction dates (F1b, F1c, F3a, F4a, F4b) and compared that mean with 2,000 random sets of five dates. Mean ratio 1.01, p = 0.53. There is no common footprint.

**F5a, non-extended-confirmed (EC) inserters.** On topic leads, in the 12 weeks before and the 12 weeks after 16 Feb 2026, 2 of 18 and 2 of 23 insertions came from non-EC accounts. That share did not change. The extended-confirmed restriction (ECR) bars non-EC accounts from these pages, and trainees in a 2026 course would almost all be new accounts. A footprint, if there is one, would be in article creation or in edits outside our set.

## Results: periods and concentration

**F1d. Topic/comparison insertion ratio by period.** Descriptive, and confounded by the war's tempo.

| Period | Weeks | Topic/wk | Comp/wk | Ratio |
|---|---|---|---|---|
| 2023-01-01 to 7 Oct 2023 | 40 | 2.5 | 4.9 | 0.51 |
| 7 Oct 2023 to 1 Feb 2024 (before the channel) | 16 | 11.2 | 3.3 | **3.44** |
| Feb to Sep 2024 (channel reported active) | 35 | 6.3 | 3.1 | 2.01 |
| Oct 2024 to May 2025 (exposure, sanctions, PIA5) | 35 | 6.4 | 3.5 | 1.84 |
| Jun 2025 to Nov 2026 | 74 | 2.1 | 2.6 | 0.82 |

The channel period does not stand out. The step from 2.0 to 1.8 is small next to the fall from the war-onset peak.

**F4c. ADL's claim that coordinated activity fell 95%.**
- The topic/comparison ratio fell from 2.10 in 2024 to 1.32 in 2025. Topic insertions per week halved (7.5 to 3.8).
- The fall is consistent with ADL's claim, and equally with saturation (the terms were already in the leads) and with the war's tempo. Our data cannot attribute it.
- Share of topic insertions made by accounts with 3 or more flips on the same article: 26% in 2023, 11% in 2024, 31% in 2025. Comparison articles: 27%, 20%, 23%.
- So 2024 was the year of **many one-off inserters**, not of repeat inserters. Because hashes do not link across articles, this cannot rule out a group spread thinly across pages.

**F3b. Concentration and carry-over around PIA5.** Only 3 to 10 articles have enough flips in both 12-month windows, so this is LOW confidence.
- With ≥3 flips in each window, the share of post-window flips made by accounts that had also flipped the same article in the prior year was:
  - topic articles, at PIA5 (23 Jan 2025): **3%** (5 articles);
  - topic articles, at a placebo date one year earlier: 19% (10 articles);
  - comparison articles, at the PIA5 date: 19% (5 articles).
- This is consistent with turnover of the active set after PIA5. The topic bans would produce it, but so would burnout. The top-1 account share did not change (0.37 to 0.35).

**F6. Zionism first sentence, after the Sept 2024 petition and press campaign.**
- In the 42 days from 14 Sep 2024 there were 7 removals of "coloni-" and 7 re-insertions.
- Random 42-day windows over 2021–26 average 0.8 removals (p = 0.03), but random windows within 2024 average 3.8 (p = 0.23).
- The month with the most removals was **June 2024 (10)**, before the petition and the press wave.
- So the petition period was busy but not unusual for 2024, and every removal in it was reverted. The press wave and the petition share dates and cannot be separated.

## Confidence

| Footprint | Verdict | Confidence |
|---|---|---|
| Tech for Palestine channel start, exposure and sanctions (F1a–d) | No footprint. The surge came before the channel; F1c points the wrong way | MODERATE that no large lead-level effect is visible; LOW on smaller effects |
| Pro-Israel email canvassing motions (F2) | Removals fell relative to comparison (local p 0.03–0.07); global p not significant | LOW (suggestive) |
| PIA5 (F3a, F3b) | Insertions and edits fell in the predicted direction; not significant; turnover is suggestive | LOW |
| ADL report (F4a) | Wrong direction | LOW (null) |
| Site bans (F4b) | 8-week window only | LOW |
| Euro-Med WikiRights (F5a, F5b) | Nothing visible; ECR would block trainees anyway | LOW (underpowered) |
| Zionism petition (F6) | Busy but typical for 2024 | LOW |

## What would make these tests stronger

1. **Talk-page and RfC participation by date.** Canvassing is alleged mainly in votes, not article edits. `discussions` in mass2 has dates and class labels but no participants.
2. **Page histories for named targets.** These pages are not in our set:
   - Azrieli Group and David Azrieli, for the Toronto edit-a-thons (Apr 2025 and 22 Oct 2025);
   - Palestinian artist biographies, for the Art+Feminism/Iniva event (20 May 2024).

   Fetching them needs en.wikipedia.org, which this session could not reach.
3. **Exact dates** for the Tech for Palestine channel start and the Dec 2024 sanctions, from the ArbCom noticeboard.
4. **Article-creation counts by week** in the topic area, for the WikiRights and edit-a-thon footprints.
