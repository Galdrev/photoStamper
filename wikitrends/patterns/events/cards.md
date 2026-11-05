# Events and timing: pattern cards

Do real-world events line up with peaks in the editing data? Event calendar: `calendar.json` (87 events, committed before looking at the series). Script: `wikitrends/event_timing.py`. Chart data: `chart_data/`.

**Method in one line.** For each event, excess = mean of weeks +0..+2 over mean of weeks -6..-1, compared with 2,000 random dates; type-level p compares the mean log-excess with random date sets of the same size.

## Type x outcome (all events; geometric-mean excess, permutation p)

| type | n | topic edits | articles edited | other conflicts' pages | lead term insertions | durable insertions (7d) | insertions per edit | pageviews (monthly) |
|---|---|---|---|---|---|---|---|---|
| military_escalation | 24 | 1.17 (p=0.001) | 1.06 (p=0.001) | 0.84 (p=0.926) | 1.19 (p=0.086) | 1.14 (p=0.098) | 0.96 (p=0.472) | 1.28 (p=0.007) |
| ceasefire_deal | 9 | 0.97 (p=0.511) | 0.95 (p=0.893) | 0.87 (p=0.716) | 0.80 (p=0.696) | 0.87 (p=0.636) | 0.92 (p=0.503) | 0.83 (p=0.583) |
| legal_institutional | 25 | 0.94 (p=0.795) | 0.94 (p=1.000) | 1.00 (p=0.276) | 0.82 (p=0.756) | 0.98 (p=0.394) | 0.85 (p=0.723) | 0.73 (p=0.955) |
| humanitarian_media | 10 | 1.08 (p=0.077) | 1.04 (p=0.094) | 0.79 (p=0.917) | 1.15 (p=0.221) | 1.55 (p=0.019) | 1.13 (p=0.294) | 0.90 (p=0.419) |
| social_global | 8 | 0.91 (p=0.848) | 0.95 (p=0.872) | 1.01 (p=0.383) | 0.73 (p=0.774) | 0.57 (p=0.979) | 0.80 (p=0.708) | 0.68 (p=0.928) |
| comparison | 10 | 0.90 (p=0.905) | 0.94 (p=0.975) | 1.36 (p=0.005) | 0.68 (p=0.871) | 0.62 (p=0.970) | 0.77 (p=0.762) | 1.15 (p=0.102) |

## Same, dropping events within 3 weeks of a stronger one

| type | n | topic edits | articles edited | other conflicts' pages | lead term insertions | durable insertions (7d) | insertions per edit | pageviews (monthly) |
|---|---|---|---|---|---|---|---|---|
| military_escalation | 8 | 1.32 (p=0.001) | 1.12 (p=0.001) | 0.79 (p=0.898) | 0.94 (p=0.493) | 0.84 (p=0.648) | 0.54 (p=0.963) | 1.42 (p=0.034) |
| ceasefire_deal | 5 | 0.98 (p=0.466) | 0.96 (p=0.804) | 0.84 (p=0.726) | 0.54 (p=0.915) | 0.58 (p=0.927) | 0.70 (p=0.772) | 0.82 (p=0.581) |
| legal_institutional | 7 | 0.98 (p=0.454) | 0.97 (p=0.731) | 1.29 (p=0.035) | 0.59 (p=0.892) | 0.75 (p=0.801) | 0.64 (p=0.868) | 0.68 (p=0.911) |
| humanitarian_media | 3 | 1.02 (p=0.317) | 0.97 (p=0.641) | 0.66 (p=0.925) | 2.03 (p=0.070) | 1.44 (p=0.165) | 1.78 (p=0.118) | 0.72 (p=0.765) |
| social_global | 1 | 0.83 (p=0.846) | 0.92 (p=0.808) | 1.21 (p=0.259) | 0.79 (p=0.534) | 1.22 (p=0.335) | 1.62 (p=0.293) | 0.58 (p=0.810) |
| comparison | 6 | 0.85 (p=0.958) | 0.92 (p=0.978) | 1.23 (p=0.077) | 0.45 (p=0.975) | 0.48 (p=0.993) | 0.54 (p=0.941) | 0.91 (p=0.387) |

6 types x 7 outcomes x 3 event sets; at p<0.05 about 2 cells per table would light up by chance. Only military -> edits/articles edited (p<=0.001) clears a Bonferroni bar. RfC starts are not testable with current data (no dates in pilot.json); `--mass2` adds them.

## 1. Battles drive editing and reading; courts, reports and ceasefires do not
*EVENTS · STRONG*

**What we see.** In the three weeks after the 24 military escalations in our calendar, topic articles got 17% more edits than in the six weeks before (geometric mean; p=0.001 against 2,000 random dates), 6% more articles were touched (p=0.001), and topic pageviews were 28% higher (p=0.007). The 25 legal and institutional events (ICJ orders, ICC, UN votes, rights-group reports, recognitions) came with 6% fewer edits and 27% fewer pageviews than usual; the 9 ceasefires and deals showed nothing (0.97). Legal events drew 19% fewer edits than military ones (p=0.005). The edit effect survives dropping events within 3 weeks of a stronger one (8 military events left: 1.32x, p=0.001), capping each article at 10 edits a week, and a local placebo that removes the 2023-24 rise and decay (1.20x, p=0.011).

**Chart.** heatmap: rows = event type (n), columns = outcome (topic edits, articles edited, other conflicts' pages, lead term insertions, durable insertions, insertions per edit, pageviews); cell = geometric-mean excess (weeks +0..+2 over -6..-1), shaded by p (`chart_data/02_type_by_outcome.json`)

**So what.** Wikipedia's editing tracks the shooting war, not the courtroom. The size is modest except for October 7 (3.0x edits, 13x pageviews over October-November against the six months before) - most escalations add a sixth more editing, not a flood. Anyone expecting a surge of edits after the next ICJ or ICC ruling should not.

**Caveat.** Weekly resolution with 86 events, many of them within days of each other; the military result leans on two clusters (Oct 2023 and Sep-Oct 2024), and only 2 military events are fully isolated (1.09x, not significant).

**Examples.**
- October 7 attacks: 283 to 936 topic edits a week; 1.45x as many articles edited.
- ICJ provisional measures order, 26 Jan 2024: topic edits flat (482 to 466 a week), pageviews 0.39x of the previous six months.
- ICC arrest warrants, 21 Nov 2024: edits 0.70x.

## 2. The idea that legal rulings drove the vocabulary change does not hold up at the scale of weeks
*EVENTS · SUGGESTIVE*

**What we see.** We tested whether legal and institutional events are followed by more critical terms (colonial, apartheid, genocide, occupation, ethnic cleansing, Nakba/expulsion, war crimes) entering the leads of 60 topic articles. They are not: insertions were 0.82x their pre-event level in the 3 weeks after (p=0.76), durable insertions 0.98x (p=0.39), and insertions per edit 0.85x. With a slower window (13 weeks after vs 13 before) durable insertions were 0.92x (p=0.90). After the ICJ order of 26 Jan 2024, lead insertions fell from 2.8 to 1.0 a week. In 2024-H1, the half-year of the vocabulary wave, legal-event windows covered 58% of weeks and got 52% of the durable insertions: no concentration. Legal and military events do not differ on insertions per edit (ratio 0.89, p=0.62).

**Chart.** dot plot: one dot per legal/institutional event, x = date, y = excess durable term insertions (log scale), grey band = 10th-90th percentile of 2,000 placebo dates (`chart_data/05_event_scatter.json`)

**So what.** The 2024 wave cannot be pinned on the ICJ, the ICC or the rights-group reports by timing. The most likely reading is that the post-October 7 editing simply took months to settle (card EV3), with institutional findings used as sources along the way rather than as triggers. A journalist should not write 'after the ICJ ruling, Wikipedia changed'.

**Caveat.** Low power: durable lead insertions run at about 1 a week on 60 leads, so a real but small legal effect could be missed; mass v2 (about 10k leads, --mass2) will test this properly.

**Examples.**
- Spain, Ireland and Norway recognise Palestine / ICJ Rafah order (late May 2024): one of the few legal windows with a rise (3.8x durable insertions, from 0.17 to 1.33 a week), shared with the Tel al-Sultan strike the same week.
- UN Commission of Inquiry genocide finding, 16 Sep 2025: durable insertions unchanged (0.33 a week before and after).

## 3. The first rush of new words after October 7 mostly bounced; what stuck arrived in 2024
*EVENTS · SUGGESTIVE*

**What we see.** In the second half of 2023 there were 75 insertions of critical terms into the 60 topic leads, four times the previous half-year, but only 23% were still there a week later. In 2024-H1 there were fewer insertions (46) but 54% stuck (Fisher exact p=0.0007). Durable insertions peaked in 2024-H1 (25) and 2024-H2 (20), against 9 in 2023-H1. Removals tracked insertions almost one for one (71 vs 75 in 2023-H2). So the 'wave months after the news peak' is the same contest being settled, not a new response to later events.

**Chart.** stacked bars by half-year: durable insertions (dark) and insertions removed within 7 days (light), with a line for the share that stuck (`chart_data/06_bounce_then_stick.json`)

**So what.** This explains the delay between the news peak and the vocabulary wave without needing a legal trigger. The October 2023 edits were attempts; consensus, talk-page work and repeated tries turned some of them into standing text over the following months. For monitoring, the number to watch is insertions that survive a week, not raw insertions.

**Caveat.** 60 leads only (25 key articles with every revision, 35 from the pilot); the 7-day survival rule is a simple proxy for 'stuck'.

**Examples.**
- Zionism as settler colonialism, 23 Oct 2023: 'Zionism and the Israeli-Palestinian conflict have been described as a form of settler colonialism.' (lived 131 days)
- Nakba, 6 Jun 2024: 'The Nakba is the ethnic cleansing of Palestinians through their violent displacement and dispossession of land, property, and belongings...' (first sentence, lived 93 days)

## 4. The method passes its placebo test: other wars move their own pages, not these
*EVENTS · STRONG*

**What we see.** The 10 comparison events (Russia's invasion of Ukraine, the Kursk incursion, Nagorno-Karabakh, Assad's fall, El Fasher and others) were followed by 1.36x the usual edits on the shocked comparison articles (Ukraine, Russia, Armenia and similar; p=0.005) and 0.90x on the topic articles. Russia's invasion: 3.2x; Kursk: 3.0x; Karabakh: 2.1x on those pages. In the other direction, Israel-Palestine military events left the clean comparison articles flat (1.01x).

**Chart.** paired bars per comparison event: excess edits on shocked comparison pages vs topic pages, reference line at 1 (`chart_data/05_event_scatter.json`)

**So what.** The event-study picks up real editing responses where they should be and not where they should not, so the nulls in EV2 are not just a blunt tool. It also shows that the edit-follows-war pattern is ordinary Wikipedia behaviour, the same for Ukraine as for Gaza.

**Caveat.** The shocked comparison set is only 6 articles, so single events swing it.

**Examples.**
- Russia's invasion of Ukraine, 24 Feb 2022: shocked-page edits 3.2x (p=0.005).
- Fall of Assad, 8 Dec 2024: topic edits 0.93x.

## 5. Edits and new words move in the same week; neither leads the other
*EVENTS · SUGGESTIVE*

**What we see.** Across 304 weeks, weekly topic edits and weekly critical-term insertions correlate most at lag 0 (r=0.517; after first-differencing logs r=0.214, 95% noise band +-0.115). No other lag from -8 to +8 weeks stands out after differencing, except a small negative value at -2 (-0.207). Monthly series show the same peak at lag 0 (r=0.621 for durable insertions) with a weak shoulder at 3 months (0.448).

**Chart.** bar chart of cross-correlation by lag (-8..+8 weeks), raw and differenced, with the +-2/sqrt(n) band (`chart_data/03_lag_xcorr.json`)

**So what.** Vocabulary change happens inside edit surges, not as a slow echo weeks later. If there is a delayed effect, it works over months (attempts settling, card EV3) and is too smeared to see in weekly data.

**Caveat.** Both series share the October 2023 spike; the differenced estimate is the honest one and it is small.

## 6. Where institutions do leave a mark: the Gaza genocide lead names each new finding within days
*EVENTS · ANECDOTE*

**What we see.** The first sentence of the Gaza genocide article added each institution as its finding appeared: Amnesty's report (5 Dec 2024) was named on 12 Dec, Human Rights Watch (19 Dec) on 31 Dec, B'Tselem (28 Jul 2025) the same day, the International Association of Genocide Scholars (31 Aug) the next day, and the UN Commission of Inquiry (16 Sep) the same day. On 5 Oct 2025 the attribution list was replaced by Wikipedia's own voice: 'The Gaza genocide is the ongoing, intentional, and systematic destruction of the Palestinian people in the Gaza Strip carried out by Israel during the Gaza war.'

**Chart.** timeline: one row per institution, dot at publication date and at first appearance in the first sentence, joined by a line; vertical marker at 5 Oct 2025 (voice step) (`chart_data/07_gaza_genocide_attribution.json`)

**So what.** Legal and institutional events do shape wording, but narrowly and fast: as named sources in the one article about the accusation, building a stack of attributions that later justified dropping attribution. That is a traceable mechanism a reader or editor can audit in the page history.

**Caveat.** One article; the voice step also followed months of talk-page discussion, so the last findings were not the only cause.

**Examples.**
- Gaza genocide, 1 Sep 2025: 'According to a United Nations special committee, Amnesty International, Medecins Sans Frontieres, B'Tselem, Physicians for Human Rights-Israel, ... (including the International Association of Genocide Scholars) ...'
- Gaza genocide, 2 Apr 2025, edit summary 'add "acts of genocide" clarification'.

## 7. The windows with the most new words are mostly war weeks, but the words are not about the war
*EVENTS · ANECDOTE*

**What we see.** Ranking event weeks by durable critical-term insertions, the top five are: Nasrallah's killing and the Lebanon invasion (late Sep 2024, 4.6x, 0.17 to 1.67 a week), the Al-Ahli hospital explosion (Oct 2023, 4.4x), the US strikes on Iran and the June 2025 ceasefire (3.9x), the ICJ Rafah order with the recognitions and the Tel al-Sultan strike (late May 2024, 3.8x), and the killing of the Rafah paramedics (Mar 2025, 3.7x). None of them beats the placebo dates by much (p 0.02 to 0.06) and the placebo event Nagorno-Karabakh ranks 9th. The terms going in were mostly about history and the land: 'Nakba' into the Israel and Hezbollah leads and 'occupation' into the Hamas lead in the Lebanon weeks; 'settler colonial' into the Israel lead during the Iran war.

**Chart.** ranked horizontal bars: top 10 event weeks by excess durable insertions, coloured by type, with the placebo 90th percentile marked (`chart_data/04_left_a_mark.json`)

**So what.** Big news weeks bring editors in, and some of them then work on old contested wording. This fits the event-filter finding that the lead change sits in history sentences: the war supplies the people and the attention, not the content.

**Caveat.** Each top window has only 2 to 5 durable insertions; with 86 events, about 4 would reach p<0.05 by chance and 8 did.

**Examples.**
- Zionism, 2 Oct 2024 (Lebanon window), edit summary 'Per talk, simplify description to ethnocultural': 'Zionism is an ethnocultural nationalist movement that emerged in Europe in the late 19th century and aimed for the establishment of a Jewish state through the colonization of a land outside Europe.' (lived 47 days)
- Israeli apartheid, 29 Sep 2024: 'Israeli apartheid is a system of institutionalized segregation and discrimination in the Israeli-occupied Palestinian territories and to a lesser extent in Israel.' (lived 40 days)
- Zionism, 22 Jun 2025 (Iran war): '... to establish and maintain a Jewish homeland through the colonization of Palestine, a region corresponding to the Land of Israel in Judaism and central to Jewish history.'

## 8. Each new war moved the editing less, and one edit war can fake an event effect
*EVENTS · SUGGESTIVE*

**What we see.** Topic edits were 3.0x in the weeks after October 7, 2.0x after Nasrallah's killing (Sep 2024), 1.06x after Israel attacked Iran (Jun 2025) and 1.09x when the 2026 Iran war began. Pageviews still rose 1.57x in June 2025. But the Sep 2024 peak (1,008 edits in one week, as high as October 2023) is mostly not Lebanon: 218 edits were on 'Antisemitic trope' and 76 on 'Society for Crypto-Judaic Studies'; Hezbollah had 104. Counted as articles edited, the Lebanon week was only 1.10x, against 1.45x after October 7.

**Chart.** line: weekly topic edits, capped edits (10 per article-week) and articles edited, 2021-2026, with event markers coloured by type (`chart_data/01_weekly_timeline_events.json`)

**So what.** After 2024 the topic's editors no longer surged with each new war, even when readers did. Raw weekly edit totals can be driven by a single unrelated dispute, so event claims should use article counts or capped edits.

**Caveat.** The deep panel's topic articles are not war articles (most are history, people, places), so later wars may mostly be edited on new war pages outside the panel.

**Examples.**
- Week of 13 Oct 2023: Hamas 122, Demographic history of Palestine (region) 101, Gaza Strip 98 edits.
- Week of 27 Sep 2024: Antisemitic trope 218, Zionism 115, Hezbollah 104 edits.

