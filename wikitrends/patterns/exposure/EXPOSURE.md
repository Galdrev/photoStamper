# View-weighted exposure: what share of readers met the more critical wording?

Data: `exposure.json` (this folder), built by `exposure.py` from GitHub Actions run 42651558741
(`wikitrends-data:views/42651558741/views/`). Window end: 8 Nov 2026 (last full day of pageviews).

## The result, one line per hero row

Each line gives the share of page views, then the share of time ("time share") in brackets.

- **Israel**: since 7 Oct 2023, **35%** of views of Israel met "genocide" in the opening section (time share 52%). That is
  9.7M views. Only 17% (4.7M views) met the hero phrase "began committing genocide" (time share 29%); the rest met
  "accusations that it has committed … genocide". Last 12 months: 100% (5.1M views), 93% of them with "began committing
  genocide". During the Oct–Dec 2023 surge 99% of 9.3M views met no genocide charge.
- **Zionism**: since 7 Oct 2023, **53%** of views met "colonization"/"colonial" in the first sentence (time share 78%).
  That is 6.3M views. 14% (1.6M) met the exact hero phrase "a Jewish homeland through colonization". "re-establishment"
  reached 0.1% (it left in June 2021). The other 47% met the plain "establishment of a homeland" wording. Last 12 months:
  100% (2.1M views). Since 2021: 41% (time share 41%), with 8% for "re-establishment".
- **Nakba**: since 7 Oct 2023, **5%** of views met "the ethnic cleansing of Palestinian Arabs by Zionists" (time share
  11%), which is 0.19M views. "Ethnic cleansing" with another agent or none ("by Israel", "Israeli", no agent) reached
  58% (time share 75%). The earlier "destruction of Palestinian society" reached 6%, and the "violent displacement and
  dispossession" wording, with no ethnic cleansing, reached 31%. Last 12 months: 30% for "by Zionists" and 70% for other
  ethnic-cleansing wordings. Since 2021, "destruction of Palestinian society" was live 42% of the time but met only 15%
  of views.
- **October 7 attacks**: over the article's life (since Oct 2023), **84%** of views met "coordinated armed incursions"
  (time share 95%), which is 7.0M views. 15% (1.2M) met the earlier "coordinated attacks" wording, which was live only
  5% of the time. Last 12 months: 100% (2.0M).
- **Hamas**: since 7 Oct 2023, **29%** of views met "political organisation with a military wing" (time share 68%), which
  is 5.3M views. 22% (4.1M) met "militant" (time share 2%). 49% (9.2M) met "political and military movement /
  organisation", the wording that held from 12 Oct 2023 to Aug 2024. Last 12 months: 95% (1.4M views). Since 2021:
  23% political organisation, 37% militant and 40% other.
- **Gaza genocide**: over the article's life (since 29 Dec 2023), **53%** of views met genocide stated in Wikipedia's own
  voice (time share 40%), which is 2.3M views; 52% met the hero phrase "carried out by Israel". 47% met an attributed
  first sentence ("has been accused of", "according to …"), and 0.4% met "Allegations" (time share 1%). Last 12 months:
  99% own voice (1.7M views).

## Where the view share and the time share differ by more than 10 points

The owner's "tricky" point holds. The October 2023 surge was very large: Hamas had 10.2M views between 7 Oct and
31 Dec 2023, against 1.5M in the last 12 months. So whatever wording was live in October 2023 dominates every window
that includes it, even when it was live only briefly.

| Article | Window | Wording | View share | Time share | Gap (points) |
|---|---|---|---|---|---|
| Hamas | since 7 Oct 2023 | political organisation (critical) | 29% | 68% | **−39.5** |
| Hamas | since 7 Oct 2023 | "militant" (softer) | 22% | 2% | **+20.0** |
| Hamas | since 7 Oct 2023 | political and military movement (other) | 49% | 30% | +19.6 |
| Zionism | since 7 Oct 2023 | colonization (critical) | 53% | 78% | **−24.8** |
| Nakba | 2021 to now | destruction of Palestinian society (softer) | 15% | 42% | −26.5 |
| Nakba | 2021 to now / since Oct 2023 | displacement wording, no ethnic cleansing (other) | 30% / 31% | 11% / 13% | +19.6 / +18.7 |
| Nakba | since 7 Oct 2023 | ethnic cleansing, other agent | 58% | 75% | −17.9 |
| Israel | since 7 Oct 2023 | genocide in the opening (critical) | 35% | 52% | **−17.3** |
| Hamas | 2021 to now | political organisation (critical) | 23% | 36% | −13.0 |
| Gaza genocide | article life | own voice (critical) | 53% | 40% | **+13.1** |
| Gaza genocide | article life | attributed | 47% | 59% | −12.3 |
| October 7 attacks | article life | armed incursions (critical) | 84% | 95% | −10.5 |
| October 7 attacks | article life | "coordinated attacks" (softer) | 15% | 5% | +10.1 |

What drives the gaps:

- **Hamas.** "Militant" was the first-sentence wording until 10–12 Oct 2023. It flipped back and forth with "political
  and military movement" in those three days. On 11–12 Oct 2023 alone, "militant" was live for about 0.9 days and met
  about 0.57M views. In the surge window (7 Oct–31 Dec 2023), "militant" was live 5% of the time but met 38% of views
  (3.9M).
- **Zionism, Israel and Hamas.** In each, the critical wording arrived after the surge: Zionism in mid-2024 (stable from
  late 2024), Israel in Apr–May 2025 and Hamas in Aug 2024 to Mar 2025. So since 7 Oct 2023 the critical wording holds
  most of the time but well under half of the readers.
- **Gaza genocide** is the one case where the critical wording met more readers than its time share. Its own-voice
  sentence (since late Sep 2025) coincides with the article's heaviest traffic.
- **October 7 attacks.** "Coordinated attacks" held from 12 Oct to late Nov 2023, about 44 days at peak interest, and met
  1.1M views.
- In the **last 12 months** no gap exceeds 5 points (largest: Nakba "by Zionists", 30% of views against 34% of time). Traffic is flat and the wordings are mostly settled.

## Run 2: Benjamin Netanyahu and Palestine (the other two flash reach bars)

Data: GitHub Actions run 42704500939 (`wikitrends-data:views/42704500939/views/`), the same workflow, endpoint
(agent=user daily pageviews), window and method as run 1; the workflow takes the titles from `WT_TITLES`. `exposure.py`
now reads both runs (`python exposure.py <run 1 dir> <run 2 dir>`); the six hero articles' entries are unchanged
(checked equal to the run-1 file). The critical wording for both is "genocide" anywhere in the opening section, the
test used for Israel.

- **Benjamin Netanyahu**: last 12 months (9 Nov 2025 – 8 Nov 2026), **7.9M views (7,940,343), 100%** met "genocide" in
  the opening section; 13.6% met the own-voice sentence "orchestrating the Gaza genocide", live since 29 Sep 2026.
  "Genocide" has been in the opening section since 21 Mar 2024. Surge (7 Oct – 31 Dec 2023): 3.5M views, none with
  "genocide". No page moves.
- **Palestine**: last 12 months, **2.6M views (2,641,678), 100%** met "genocide" in the opening section; 41.0% met
  "recognised as constituting genocide", live since 3 Jun 2026. "Genocide" entered the opening on 23 Dec 2024. The
  article was "State of Palestine" until 7 Jan 2025 (views of that title count from the start, views of "Palestine"
  from the move). Since 7 Oct 2023 the view share is 35% against a time share of 61% (the surge again).
- The old flash bars (mass2 crawl, monthly) gave Netanyahu 7.0M and Palestine 2.4M; the daily sums are larger, as for
  the six hero articles (see the caveat above).

## Method

- **Views**: daily Wikimedia REST pageviews, `per-article/en.wikipedia/all-access/user/<Title>/daily/20210101/20261108`
  (agent=user, which excludes self-identified bots and spiders). They were fetched by
  `.github/workflows/wikitrends-views.yml`, with no email address in the User-Agent.
- **Titles and moves**: page moves come from revision comments ("moved page [[A]] to [[B]]"). Each title's views count from
  the moment it became the article's title. Before a move, the current title was a redirect to something else, so its
  views are not counted then. After a move, views of the old title (now a redirect) still count.
  - Nakba: An Nakba → Nakba, 3 Apr 2021.
  - October 7 attacks: ten titles, from Operation Al-Aqsa Flood through 2023 Hamas-led attack on Israel to October 7
    attacks (26 May 2025).
  - Gaza genocide: Allegations of genocide in the 2023 Israeli attack on Gaza → Gaza genocide (3 Jul 2024); this includes
    a 4-minute vandal move.
  - A sensitivity variant adds every current redirect to the article at all dates (`view_share_incl_redirects`). It moves
    no headline share by more than 1 point.
- **Wording per version**: the section 0 of every revision since 1 Jan 2021 was fetched again with exact timestamps, as
  ratchet.py does (`analyze.prose`, first sentence by `analyze.sentences`). Phrases are tested after the flash edition's
  `norm()`, which normalises whitespace and folds curly apostrophes.
  - The categories (ordered, first match wins) are listed in `exposure.json` → `categories`.
  - Besides the categories, the exact hero now/then phrases from `page_flash_template.html` #flRw are tested
    case-sensitively, as build_flash.py does (`hero_exact_phrase`).
  - Israel is tested on the whole opening section; the other five on the first sentence.
- **Day resolution**: each day's views (UTC days) are split across the versions live that day in proportion to the
  seconds each was live, using the revision timestamps. No equal-split fallback was needed.
- **Time share**: seconds live within the window, over the covered seconds.
- **Gaps in coverage**:
  - Days before an article's first revision since 2021, and days when the page was a redirect, are excluded from both
    shares. The excluded views are listed as `views_excluded_no_state`: at most 31k, for October 7 attacks, which was a
    redirect to the war article from 7 to 12 Oct 2023.
  - For Israel, Zionism and Hamas, the hours from 1 Jan 2021 to the first 2021 edit use the Jan 2021 lead in
    `leads.json`.
  - Hidden revisions carry the previous state forward.
- **Windows**:
  - 2021 to now: 1 Jan 2021 – 8 Nov 2026.
  - Since 7 Oct 2023.
  - Last 12 months: 10 Nov 2025 – 8 Nov 2026.
  - An extra window for the surge: 7 Oct – 31 Dec 2023.
  - For October 7 attacks and Gaza genocide, the "2021" window equals the article's life.

## Caveats

- **Pageviews are not readers.** One person reloading or returning counts again. agent=user still contains some
  undeclared automated traffic, especially on spike days. Views do not show whether anyone read the first sentence.
- **Mobile and previews**: all-access includes mobile web and the apps, which show the same lead. Hover previews, search
  snippets and knowledge panels are not pageviews and often show the first sentence too, so the first sentence's real
  reach is larger than this count and is not measured here.
- **Opening section vs first sentence**: the Israel row tests the whole section 0. The opening section is long, and
  "genocide" there is not in the first sentence. Before Sep 2026 the word came mainly as an accusation, and
  "began committing genocide" was live from 11 Dec 2025, with short gaps. The other rows test only the first sentence.
- **Renames**: views follow titles. A view of an old title after a move is a redirect hit that showed the same article.
  Views before an article existed under any of its titles are not counted (October 7 attacks before 7 Oct 2023;
  Gaza genocide before 29 Dec 2023).
- **The current history**: revision text comes from the page history as it stands on 9 Nov 2026. Suppressed revisions
  (rare) carry the previous state.
- **The flash's 12-month view bars do not match these totals.** The flash shows Israel 4.6M, Zionism 1.8M and Hamas
  1.3M; these are from the mass2 crawl. Daily sums here are 5.1M, 2.1M and 1.5M for 10 Nov 2025 – 8 Nov 2026. I did not
  reconcile the difference (it may be a window or aggregation difference) and leave the flash numbers unchanged.
- **Category edges**: "other" covers neutral rewordings and parse artefacts, such as a map caption parsed as the first
  sentence of Nakba in Nov 2022 – Jan 2023 (72 days, 0.11M views).
