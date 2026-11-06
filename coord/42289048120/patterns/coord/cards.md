# Coordinated editing: blocs, synchrony, sweeps

Generated 2026-11-06T22:26:26Z. Nulls: 1000 draws; pipeline calibration on 200 null worlds. No usernames or account hashes appear here; blocs are lettered.

## What the coordination tier covers

**Confidence:** descriptive

4121 critical-term event revisions in 959 articles (diff status {'ok': 4121}); 3206 account events used after excluding {'anon': 902, 'bot': 51} (anonymous, hidden-user, bot, deleted). One run-wide pseudonymous ID per account.

**Null model:** {"draws": 1000, "calibration_worlds": 200}

**So what:** All tests below share these events; topic and comparison articles are tested separately.

**Caveat:** Lead events come from mass2's grid (exact events only) and the ratchet key articles; edits outside those events are invisible here. IP and temporary accounts are excluded from account-level tests.

## (a) Bloc detection: topic articles, any events

**Confidence:** medium

topic articles, any events: 14 account pairs share articles above the rewiring null (p<0.01, >=3 shared); null worlds give 1.93 such pairs on average (95th 5.0). 2 candidate groups of 3+ (null worlds: 0.3 on average, 95th 1.0); 1 pass the bloc test. Bloc A (4 accounts) [medium]: 23 articles (top: Israel, Gaza war, Hamas, Israeli bombing of the Gaza Strip); 45 insertions / 23 removals; articles touched by 3+ members 3 vs null 0.236 (95th 1.0, p=0.001); 60-min cross-article co-activity 0 vs 0.12 (p=1.000, article-shuffle p=1.000); median same-article gap 333.87 h, events with another member within 10 min 0.0; 4 significant triads; null worlds with a bloc this large and dense: 0.0; active 2021-04-16 to 2025-11-15

**Null model:** {"pairs": "degree-preserving rewiring, 1000 draws", "bloc": "articles with 3+ members vs rewiring; selection-aware share of null worlds; synchrony vs account day-shift (1-7 d) and time shuffle within article", "expected_by_chance": {"null_worlds": 200, "edges_mean": 1.93, "edges_p95": 5.0, "communities_mean": 0.3, "communities_p95": 1.0, "communities_max": 2}}

**So what:** A bloc is a set of accounts whose overlap in critical-term articles is not explained by how active each account is and how popular each article is.

**Caveat:** Shared interest (WikiProject members, watchlists, talk-page RfCs) also produces overlap beyond a degree-preserving null; synchrony and direction help separate it but do not prove coordination.

## (b) Synchrony: topic account pairs acting on different articles within 10 minutes

**Confidence:** not detected (consistent with chance)

0 pairs (0 accounts) acted on 3+ distinct article pairs within 10 min of each other more often than the account day-shift null (p<0.01); 0 also beat the within-article time-shuffle null. Null worlds give 0.05 pairs on average (95th 0.0).

**Null model:** {"null": "each account's timeline shifted by a random 1-7 days (either sign), 1000 draws; secondary: timestamps permuted within article", "expected_by_chance": {"null_worlds": 200, "edges_mean": 0.05, "edges_p95": 0.0}}

**So what:** Pairs that repeatedly move together across different articles within minutes are the classic canvassing / sockpuppet signature, if they are more than the null expects.

**Caveat:** Both accounts may react to the same external trigger (news, an RfC closing, a noticeboard thread).

## Co-activity network: topic articles (time + direction)

**Confidence:** medium

14 significant edges among 11 accounts (of 697 tested); expected by chance 2.15 (95th 5.0). 2 communities of 3+ (chance 0.34, 95th 1.0), 1 significant.

**Null model:** {"edge": "p<0.01 and observed>=3 on 30-min cross-article co-activity (account day-shift) or shared articles (rewiring)", "expected_by_chance": {"null_worlds": 200, "edges_mean": 2.15, "edges_p95": 5.0, "communities_mean": 0.34, "communities_p95": 1.0, "communities_max": 2}}

**So what:** The page's network graph; edges carry direction agreement, so insert-blocs and remove-blocs are visible.

**Caveat:** Edges are tested one by one at p<0.01; compare the edge count with the chance expectation, not with zero.

## (a) Bloc detection: topic articles, insert events

**Confidence:** medium

topic articles, insert events: 5 account pairs share articles above the rewiring null (p<0.01, >=3 shared); null worlds give 0.85 such pairs on average (95th 3.0). 1 candidate groups of 3+ (null worlds: 0.12 on average, 95th 1.0); 1 pass the bloc test. Bloc B (4 accounts) [medium]: 53 articles (top: Israel, Gaza war, Ariel Sharon, Hamas); 114 insertions / 0 removals; articles touched by 3+ members 3 vs null 0.56 (95th 2.0, p=0.006); 60-min cross-article co-activity 0 vs 0.309 (p=1.000, article-shuffle p=1.000); median same-article gap 1574.42 h, events with another member within 10 min 0.0; 0 significant triads; null worlds with a bloc this large and dense: 0.005; active 2021-04-16 to 2025-08-10

**Null model:** {"pairs": "degree-preserving rewiring, 1000 draws", "bloc": "articles with 3+ members vs rewiring; selection-aware share of null worlds; synchrony vs account day-shift (1-7 d) and time shuffle within article", "expected_by_chance": {"null_worlds": 200, "edges_mean": 0.85, "edges_p95": 3.0, "communities_mean": 0.12, "communities_p95": 1.0, "communities_max": 1}}

**So what:** A bloc is a set of accounts whose overlap in critical-term articles is not explained by how active each account is and how popular each article is.

**Caveat:** Shared interest (WikiProject members, watchlists, talk-page RfCs) also produces overlap beyond a degree-preserving null; synchrony and direction help separate it but do not prove coordination.

## (a) Bloc detection: topic articles, remove events

**Confidence:** not detected

topic articles, remove events: 2 account pairs share articles above the rewiring null (p<0.01, >=3 shared); null worlds give 0.19 such pairs on average (95th 1.0). 1 candidate groups of 3+ (null worlds: 0.02 on average, 95th 0.0); 0 pass the bloc test. No bloc detected.

**Null model:** {"pairs": "degree-preserving rewiring, 1000 draws", "bloc": "articles with 3+ members vs rewiring; selection-aware share of null worlds; synchrony vs account day-shift (1-7 d) and time shuffle within article", "expected_by_chance": {"null_worlds": 200, "edges_mean": 0.19, "edges_p95": 1.0, "communities_mean": 0.02, "communities_p95": 0.0, "communities_max": 1}}

**So what:** Account overlap is what the rewiring null predicts from activity and article popularity alone.

**Caveat:** Shared interest (WikiProject members, watchlists, talk-page RfCs) also produces overlap beyond a degree-preserving null; synchrony and direction help separate it but do not prove coordination.

## (a) Bloc detection: comparison articles, any events

**Confidence:** not detected

comparison articles, any events: 3 account pairs share articles above the rewiring null (p<0.01, >=3 shared); null worlds give 0.27 such pairs on average (95th 1.0). 0 candidate groups of 3+ (null worlds: 0.03 on average, 95th 0.0); 0 pass the bloc test. No bloc detected.

**Null model:** {"pairs": "degree-preserving rewiring, 1000 draws", "bloc": "articles with 3+ members vs rewiring; selection-aware share of null worlds; synchrony vs account day-shift (1-7 d) and time shuffle within article", "expected_by_chance": {"null_worlds": 200, "edges_mean": 0.27, "edges_p95": 1.0, "communities_mean": 0.03, "communities_p95": 0.0, "communities_max": 1}}

**So what:** Account overlap is what the rewiring null predicts from activity and article popularity alone.

**Caveat:** Shared interest (WikiProject members, watchlists, talk-page RfCs) also produces overlap beyond a degree-preserving null; synchrony and direction help separate it but do not prove coordination.

## (b) Synchrony: comparison account pairs acting on different articles within 10 minutes

**Confidence:** not detected (consistent with chance)

0 pairs (0 accounts) acted on 3+ distinct article pairs within 10 min of each other more often than the account day-shift null (p<0.01); 0 also beat the within-article time-shuffle null. Null worlds give 0.0 pairs on average (95th 0.0).

**Null model:** {"null": "each account's timeline shifted by a random 1-7 days (either sign), 1000 draws; secondary: timestamps permuted within article", "expected_by_chance": {"null_worlds": 200, "edges_mean": 0.0, "edges_p95": 0.0}}

**So what:** Pairs that repeatedly move together across different articles within minutes are the classic canvassing / sockpuppet signature, if they are more than the null expects.

**Caveat:** Both accounts may react to the same external trigger (news, an RfC closing, a noticeboard thread).

## Co-activity network: comparison articles (time + direction)

**Confidence:** not detected (consistent with chance)

3 significant edges among 6 accounts (of 847 tested); expected by chance 0.28 (95th 1.0). 0 communities of 3+ (chance 0.03, 95th 0.0), 0 significant.

**Null model:** {"edge": "p<0.01 and observed>=3 on 30-min cross-article co-activity (account day-shift) or shared articles (rewiring)", "expected_by_chance": {"null_worlds": 200, "edges_mean": 0.28, "edges_p95": 1.0, "communities_mean": 0.03, "communities_p95": 0.0, "communities_max": 1}}

**So what:** The page's network graph; edges carry direction agreement, so insert-blocs and remove-blocs are visible.

**Caveat:** Edges are tested one by one at p<0.01; compare the edge count with the chance expectation, not with zero.

## (a) Bloc detection: comparison articles, insert events

**Confidence:** not detected

comparison articles, insert events: 2 account pairs share articles above the rewiring null (p<0.01, >=3 shared); null worlds give 0.0 such pairs on average (95th 0.0). 0 candidate groups of 3+ (null worlds: 0.0 on average, 95th 0.0); 0 pass the bloc test. No bloc detected.

**Null model:** {"pairs": "degree-preserving rewiring, 1000 draws", "bloc": "articles with 3+ members vs rewiring; selection-aware share of null worlds; synchrony vs account day-shift (1-7 d) and time shuffle within article", "expected_by_chance": {"null_worlds": 200, "edges_mean": 0.0, "edges_p95": 0.0, "communities_mean": 0.0, "communities_p95": 0.0, "communities_max": 0}}

**So what:** Account overlap is what the rewiring null predicts from activity and article popularity alone.

**Caveat:** Shared interest (WikiProject members, watchlists, talk-page RfCs) also produces overlap beyond a degree-preserving null; synchrony and direction help separate it but do not prove coordination.

## (a) Bloc detection: comparison articles, remove events

**Confidence:** not detected

comparison articles, remove events: 1 account pairs share articles above the rewiring null (p<0.01, >=3 shared); null worlds give 0.04 such pairs on average (95th 0.0). 0 candidate groups of 3+ (null worlds: 0.0 on average, 95th 0.0); 0 pass the bloc test. No bloc detected.

**Null model:** {"pairs": "degree-preserving rewiring, 1000 draws", "bloc": "articles with 3+ members vs rewiring; selection-aware share of null worlds; synchrony vs account day-shift (1-7 d) and time shuffle within article", "expected_by_chance": {"null_worlds": 200, "edges_mean": 0.04, "edges_p95": 0.0, "communities_mean": 0.0, "communities_p95": 0.0, "communities_max": 0}}

**So what:** Account overlap is what the rewiring null predicts from activity and article popularity alone.

**Caveat:** Shared interest (WikiProject members, watchlists, talk-page RfCs) also produces overlap beyond a degree-preserving null; synchrony and direction help separate it but do not prove coordination.

## (c) Copy-paste sweeps: topic articles

**Confidence:** n/a (none found)

0 near-identical inserted sentences (5-word shingle Jaccard >= 0.7) appear in 5+ articles. 

**Null model:** {"null": "same number of insertion times drawn from all term insertions in the group, 1000 draws; statistic: shortest span covering 5 distinct articles"}

**So what:** A sweep is the same wording placed into many articles; a short span and few accounts point to a campaign, a long span and many accounts to a shared standard phrase.

**Caveat:** Standard wording (WikiProject templates, a source's stock phrase) also repeats; the temporal null separates bursts from slow diffusion, not intent.

## (c) Copy-paste sweeps: comparison articles

**Confidence:** n/a (none found)

0 near-identical inserted sentences (5-word shingle Jaccard >= 0.7) appear in 5+ articles. 

**Null model:** {"null": "same number of insertion times drawn from all term insertions in the group, 1000 draws; statistic: shortest span covering 5 distinct articles"}

**So what:** A sweep is the same wording placed into many articles; a short span and few accounts point to a campaign, a long span and many accounts to a shared standard phrase.

**Caveat:** Standard wording (WikiProject templates, a source's stock phrase) also repeats; the temporal null separates bursts from slow diffusion, not intent.

## (c) Nakba wording on Palestinian village pages

**Confidence:** n/a (no sweep)

25 inserted Nakba / expulsion sentences on 17 village pages by 15 registered accounts. Sweeps (5+ village articles, same wording): 0. 

**Null model:** {"null": "as for (c)"}

**So what:** Flags whether the village-page Nakba wording arrived as one sweep or piecemeal.

**Caveat:** Village articles share a WikiProject structure (Khalidi / Morris sourcing), so similar wording is expected; only a short-span, few-account cluster suggests a sweep.

## (e) Do detected blocs line up with the documented canvassing windows and sanctions?

**Confidence:** low

Sets tested: 3 (insert-direction blocs 1, remove-direction 0, any-direction blocs and communities 2). 0 show window concentration or a post-sanction drop beyond matched random sets (p<0.01). Bloc A (4 accounts) [topic/any]: email_canvassing: 41% of events in window [CI 17%-74%] vs matched sets 18% [0%-44%], own-span 0.149, others 0.169, p_high 0.042; tfp_discord: 21% of events in window [CI 12%-44%] vs matched sets 23% [4%-49%], own-span 0.226, others 0.253, p_high 0.5385. after 2024-12-09: drop ratio 0.392 [CI 0.028-1.104] vs matched 1.917, p_drop 0.1968; after 2025-04-25: drop ratio 0.597 [CI 0.118-0.887] vs matched 0.835, p_drop 0.5435 | topic network community 1 (4 accounts) [topic/any]: email_canvassing: 41% of events in window [CI 17%-74%] vs matched sets 18% [0%-40%], own-span 0.149, others 0.169, p_high 0.02; tfp_discord: 21% of events in window [CI 12%-44%] vs matched sets 23% [2%-47%], own-span 0.226, others 0.253, p_high 0.5325. after 2024-12-09: drop ratio 0.392 [CI 0.028-1.104] vs matched 2.238, p_drop 0.1818; after 2025-04-25: drop ratio 0.597 [CI 0.118-0.887] vs matched 0.877, p_drop 0.5335 | Bloc B (4 accounts) [topic/insert]: email_canvassing: 34% of events in window [CI 24%-42%] vs matched sets 15% [0%-38%], own-span 0.115, others 0.154, p_high 0.0509; tfp_discord: 29% of events in window [CI 12%-37%] vs matched sets 24% [3%-44%], own-span 0.231, others 0.246, p_high 0.3157. after 2024-12-09: drop ratio 0.224 [CI 0.032-1.8] vs matched 2.052, p_drop 0.0539; after 2025-04-25: drop ratio 0.218 [CI 0.02-1.072] vs matched 0.703, p_drop 0.3636

**Null model:** {"window_share": "matched random account sets (member-by-member on event count), 1,000 draws; CI = bootstrap over members", "post_sanction_drop": "365 d after vs before each date, relative to all other accounts; same matched-set null", "windows": {"email_canvassing": ["2023-10-01", "2024-01-21", "ArbCom 'PIA canvassing' motions, 4-20 Jan 2024: email canvassing and proxying for a banned editor (pro-Israel), dated from about Oct 2023"], "tfp_discord": ["2024-01-01", "2024-10-01", "Tech for Palestine Discord Wikipedia channel: created Jan 2024, public until about Sep 2024; ArbCom sanctioned editing after off-wiki canvassing requests there (Dec 2024)"]}, "sanctions": {"2024-12-09": "ArbCom private-case sanctions for off-wiki canvassing (date approximate, ~9 Dec 2024)", "2025-04-25": "ArbCom site bans on further off-wiki coordination evidence"}}

**So what:** Alignment in time is not attribution: a set active during the Discord months is not shown to be the Discord group. It is a test of whether the documented windows left a footprint in who edited these terms.

**Caveat:** Dates come from ORGS.md snippets (marked there as needing verification); only critical-term lead events are counted; a drop after a sanction can also reflect the war-news cycle, which the comparison with all other accounts only partly removes.

## (d) Account profiles of the blocs (aggregate)

**Confidence:** medium

Bloc A (4 accounts) topic/any: median age 1071.0 d (base 1298.5), editcount<500 0.0 (base 0.222), blocked now 0.25 (base 0.151, random-set 95th 0.5) | Bloc B (4 accounts) topic/insert: median age 2204.0 d (base 1322.0), editcount<500 0.0 (base 0.217), blocked now 0.25 (base 0.163, random-set 95th 0.5)

**Null model:** {"null": "1,000 random account sets of the same size from accounts with 2+ articles in the same scope; base rate = all accounts in scope"}

**So what:** Young, low-editcount or since-blocked blocs are the sockpuppet profile; veteran blocs look like WikiProject regulars.

**Caveat:** Block status is as of collection, not as of the edit.
