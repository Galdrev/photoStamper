# Revert guarding, tag teams and voting blocs (aggregate only)

Generated 2026-11-08T19:34:58Z. No usernames, account hashes or revision ids appear here; account counts of 1-2 are shown as <3. Each card gives the observed value, what the comparison articles or the null model give, and a one-line verdict.

Scope: {'topic': 254, 'comparison': 254} articles ({'topic': {'High': 82, 'Top': 55, 'core': 117}, 'comparison': {'High': 82, 'Top': 110, 'core': 62}}); revisions (thousands) {'topic': 614.2, 'comparison': 844.0}; coord network recomputed in the same job: {'available': True, 'edges': 14, 'accounts': 11, 'articles_collected': 959, 'articles_expected': 959, 'complete': True}.

## 1. Revert guarding

Totals: {'reverts': 242632, 'reverts_by_bots': 10449, 'reverts_by_ip_or_temp': 15038, 'kinds': {'identity': 214588, 'summary': 21547, 'undo': 6446, 'restore': 51}, 'reverts_since_2021': 27327, 'direction_measured': 27220, 'direction_measured_share_of_window': 0.996, 'directions': {'topic': {'none': 9339, 'add': 274, 'remove': 233}, 'comparison': {'none': 17049, 'remove': 180, 'add': 145}}}

**Topic vs comparison, full history** (86503 vs 130642 reverts by registered accounts; concentration rarefied to 86503).
- median_h: topic 0.434 [0.34, 0.553] vs comparison 0.327 [0.26, 0.418]; difference 0.107 [-0.03, 0.246], label-permutation p 0.1089
- fast24: topic 0.93 [0.919, 0.938] vs comparison 0.938 [0.929, 0.945]; difference -0.008 [-0.02, 0.004], label-permutation p 0.1808
- top5: topic 0.101 [0.09, 0.117] vs comparison 0.041 [0.038, 0.058]; difference 0.061 [0.04, 0.073], label-permutation p 0.001
- top10: topic 0.155 [0.142, 0.175] vs comparison 0.064 [0.062, 0.09]; difference 0.091 [0.061, 0.107], label-permutation p 0.001
- gini: topic 0.786 [0.762, 0.789] vs comparison 0.731 [0.72, 0.743]; difference 0.055 [0.029, 0.058], label-permutation p 0.001

**Topic vs comparison, since 2021** (9272 vs 16406 reverts by registered accounts; concentration rarefied to 9272).
- median_h: topic 1.523 [1.08, 2.181] vs comparison 1.116 [0.845, 1.468]; difference 0.407 [-0.168, 1.069], label-permutation p 0.1279
- fast24: topic 0.859 [0.826, 0.889] vs comparison 0.871 [0.856, 0.884]; difference -0.012 [-0.048, 0.021], label-permutation p 0.4116
- top5: topic 0.102 [0.089, 0.13] vs comparison 0.083 [0.076, 0.13]; difference 0.018 [-0.028, 0.041], label-permutation p 0.1429
- top10: topic 0.165 [0.149, 0.203] vs comparison 0.142 [0.132, 0.196]; difference 0.023 [-0.031, 0.053], label-permutation p 0.1668
- gini: topic 0.687 [0.647, 0.706] vs comparison 0.639 [0.627, 0.672]; difference 0.048 [-0, 0.055], label-permutation p 0.001

**Reverts of critical-term removals vs additions, topic articles** (227 vs 260 measured reverts; accounts 91 vs 154).
- median_h: removals 1.131 [0.616, 1.694] vs additions 0.836 [0.489, 1.423]; difference 0.296 [-0.34, 1.013], direction-permutation p 0.8681
- fast24: removals 0.907 [0.853, 0.942] vs additions 0.923 [0.884, 0.959]; difference -0.016 [-0.076, 0.037], direction-permutation p 0.3117
- top5: removals 0.251 [0.247, 0.389] vs additions 0.136 [0.141, 0.243]; difference 0.115 [0.051, 0.195], direction-permutation p 0.003
- top10: removals 0.41 [0.401, 0.577] vs additions 0.229 [0.24, 0.379]; difference 0.181 [0.087, 0.269], direction-permutation p 0.001
- gini: removals 0.47 [0.384, 0.514] vs additions 0.307 [0.282, 0.411]; difference 0.163 [0.026, 0.176], direction-permutation p 0.001

**Reverts of critical-term removals vs additions, comparison articles** (172 vs 135 measured reverts; accounts 120 vs 87).
- median_h: removals 0.084 [0.037, 0.242] vs additions 0.357 [0.211, 1.805]; difference -0.273 [-1.605, -0.138], direction-permutation p 0.005
- fast24: removals 0.942 [0.888, 0.975] vs additions 0.874 [0.791, 0.939]; difference 0.068 [-0.002, 0.14], direction-permutation p 0.022
- top5: removals 0.169 [0.15, 0.344] vs additions 0.193 [0.195, 0.385]; difference -0.024 [-0.164, 0.059], direction-permutation p 0.6164
- top10: removals 0.263 [0.259, 0.496] vs additions 0.304 [0.328, 0.554]; difference -0.04 [-0.196, 0.044], direction-permutation p 0.4016
- gini: removals 0.227 [0.216, 0.431] vs additions 0.285 [0.283, 0.437]; difference -0.058 [-0.136, 0.043], direction-permutation p 0.2398

**Difference in differences (topic minus comparison, removal minus addition):** median_h 0.569 [-0.069, 2.074]; fast24 -0.084 [-0.183, 0.006]; top5 0.139 [0.038, 0.303]; top10 0.221 [0.094, 0.403]; gini 0.221 [0.029, 0.264]

**Verdict:** inconclusive: one guarding signature (speed or concentration) beyond chance, not both

## 2. Tag-team reverting

a tag-team sequence = 2+ reverts toward the same version (same sha1 restored) of one article by 2+ different registered non-bot accounts, consecutive reverts no more than W hours apart. Null: reverter labels shuffled among the reverts of the same article and calendar month (who reverts in that article-month is kept; who reverts toward which version is broken), 500 draws.

**Window 24 h.** Sequences: topic 9663, comparison 15668. Per article: {'topic': 39.602, 'comparison': 65.556, 'difference': -25.954, 'difference_ci95': [-46.83, -7.379], 'p_label_permutation': 0.023}. Per 1,000 reverts: {'topic': 111.707, 'comparison': 119.931, 'difference': -8.224, 'difference_ci95': [-20.195, 3.17], 'p_label_permutation': 0.1758}.
- topic: sequences 9663 (shuffle 11940.0); pairs on 3+ articles {'observed': 430.0, 'null_mean': 580.694, 'null_p95': 608.0, 'p_upper': 1.0, 'excess_over_null': -150.694}; pairs on 2+ articles {'observed': 1385.0, 'null_mean': 1948.318, 'null_p95': 2003.05, 'p_upper': 1.0, 'excess_over_null': -563.318}; accounts in 3+-article pairs {'observed': 202, 'null_mean': 237.148, 'null_p95': 251.05, 'p_upper': 1.0, 'excess_over_null': -35.148}; pairs recurring beyond their own shuffle distribution {'rule': "pair shares sequences on 3+ distinct articles and p<0.01 against that pair's own shuffle distribution", 'observed': 19, 'expected_by_chance_mean': 9.64, 'expected_p95': 15.0, 'accounts': 31, 'groups_3plus_accounts': {'count': 2, 'sizes': [8, 3]}}
- comparison: sequences 15668 (shuffle 19149.1); pairs on 3+ articles {'observed': 323.0, 'null_mean': 358.08, 'null_p95': 385.0, 'p_upper': 0.996, 'excess_over_null': -35.08}; pairs on 2+ articles {'observed': 1507.0, 'null_mean': 1806.548, 'null_p95': 1866.05, 'p_upper': 1.0, 'excess_over_null': -299.548}; accounts in 3+-article pairs {'observed': 233, 'null_mean': 236.852, 'null_p95': 253.0, 'p_upper': 0.6667, 'excess_over_null': -3.852}; pairs recurring beyond their own shuffle distribution {'rule': "pair shares sequences on 3+ distinct articles and p<0.01 against that pair's own shuffle distribution", 'observed': 25, 'expected_by_chance_mean': 11.96, 'expected_p95': 19.0, 'accounts': 47, 'groups_3plus_accounts': {'count': 2, 'sizes': [4, 3]}}

**Window 72 h.** Sequences: topic 11223, comparison 18140. Per article: {'topic': 45.996, 'comparison': 75.9, 'difference': -29.904, 'difference_ci95': [-51.893, -6.548], 'p_label_permutation': 0.009}. Per 1,000 reverts: {'topic': 129.741, 'comparison': 138.853, 'difference': -9.112, 'difference_ci95': [-18.77, 0.881], 'p_label_permutation': 0.0799}.
- topic: sequences 11223 (shuffle 13477.3); pairs on 3+ articles {'observed': 557.0, 'null_mean': 765.946, 'null_p95': 796.05, 'p_upper': 1.0, 'excess_over_null': -208.946}; pairs on 2+ articles {'observed': 1857.0, 'null_mean': 2489.446, 'null_p95': 2544.0, 'p_upper': 1.0, 'excess_over_null': -632.446}; accounts in 3+-article pairs {'observed': 253, 'null_mean': 290.346, 'null_p95': 305.0, 'p_upper': 1.0, 'excess_over_null': -37.346}; pairs recurring beyond their own shuffle distribution {'rule': "pair shares sequences on 3+ distinct articles and p<0.01 against that pair's own shuffle distribution", 'observed': 21, 'expected_by_chance_mean': 11.12, 'expected_p95': 17.0, 'accounts': 32, 'groups_3plus_accounts': {'count': 4, 'sizes': [9, 3, 3, 3]}}
- comparison: sequences 18140 (shuffle 21517.7); pairs on 3+ articles {'observed': 422.0, 'null_mean': 473.276, 'null_p95': 501.0, 'p_upper': 0.998, 'excess_over_null': -51.276}; pairs on 2+ articles {'observed': 1938.0, 'null_mean': 2284.236, 'null_p95': 2343.05, 'p_upper': 1.0, 'excess_over_null': -346.236}; accounts in 3+-article pairs {'observed': 282, 'null_mean': 294.608, 'null_p95': 312.0, 'p_upper': 0.8862, 'excess_over_null': -12.608}; pairs recurring beyond their own shuffle distribution {'rule': "pair shares sequences on 3+ distinct articles and p<0.01 against that pair's own shuffle distribution", 'observed': 25, 'expected_by_chance_mean': 12.76, 'expected_p95': 19.0, 'accounts': 45, 'groups_3plus_accounts': {'count': 5, 'sizes': [3, 3, 3, 3, 3]}}

**Verdict:** no evidence of topic-specific tag-teaming: some pairs recur beyond the shuffle null, but the excess is no larger than on the comparison articles

## 3. Voting blocs on talk pages

!votes (support / oppose / include / exclude / keep / delete / option X...) in RfC, requested-move and AfD discussions on the talk pages (and archives) of the scoped articles; one stance per account per discussion; accounts with 3+ votes in the group, discussions with 3+ such voters. Null: stances permuted among the voters of each discussion, 1000 draws; significant pair: p<0.01 and 3+ agreements; blocs: Louvain on significant pairs, 3+ accounts; 100 calibration worlds.

**topic:** {"discussions_with_3plus_regular_voters": 217, "discussion_kinds": {"afd": 9, "rm": 115, "rfc": 93}, "regular_voters": 351, "pairs_with_3plus_shared_discussions": 1520, "significant_agreement_pairs": {"observed": 26, "expected_by_chance_mean": 0.44, "expected_p95": 2.0, "calibration_worlds": 100}, "share_of_pairs_agreeing_80pct_plus": {"observed": 0.287, "null_mean": 0.116, "null_ci95": [0.102, 0.133], "p_upper": 0.001}, "mean_pair_agreement": {"observed": 0.512, "null_mean": 0.506}, "blocs": {"count": 4, "sizes": [6, 6, 4, 3], "expected_by_chance_mean": 0.01, "expected_p95": 0.0, "detail": [{"size": 6, "within_bloc_agreement": 0.97, "null_mean": 0.528, "null_ci95": [0.436, 0.634], "p_upper": 0.001}, {"size": 6, "within_bloc_agreement": 0.892, "null_mean": 0.527, "null_ci95": [0.459, 0.599], "p_upper": 0.001}, {"size": 4, "within_bloc_agreement": 1.0, "null_mean": 0.476, "null_ci95": [0.324, 0.647], "p_upper": 0.001}, {"size": 3, "within_bloc_agreement": 0.933, "null_mean": 0.465, "null_ci95": [0.2, 0.667], "p_upper": 0.001}]}}

**comparison:** {"discussions_with_3plus_regular_voters": 92, "discussion_kinds": {"rm": 65, "rfc": 24, "afd": 3}, "regular_voters": 128, "pairs_with_3plus_shared_discussions": 46, "significant_agreement_pairs": {"observed": 0, "expected_by_chance_mean": 0.0, "expected_p95": 0.0, "calibration_worlds": 100}, "share_of_pairs_agreeing_80pct_plus": {"observed": 0.348, "null_mean": 0.261, "null_ci95": [0.152, 0.391], "p_upper": 0.1069}, "mean_pair_agreement": {"observed": 0.618, "null_mean": 0.656}, "blocs": {"count": 0, "sizes": [], "expected_by_chance_mean": 0.0, "expected_p95": 0.0, "detail": []}}

**Overlap with the recomputed coord edges:** {'coord_edges': 14, 'coord_edges_that_are_voting_pairs_with_3plus_shared': 4, 'of_which_significant_agreement_pairs': 0, 'expected_significant_by_chance': 0.07, 'coord_accounts_among_regular_voters': 6, 'coord_accounts_in_voting_blocs': 3, 'expected_in_blocs_by_chance': 0.32, 'expected_p95': 1.0, 'p_upper': 0.003}

**Verdict:** supports bloc voting: more high-agreement pairs and voting blocs than the stance permutation produces (consistent co-voting; on its own this is also what two honest camps produce, it is not proof of off-wiki coordination)

## 4. Are the fast reverters the same accounts?

fast reverter = registered non-bot account with 2+ reverts, within 24 h, of topic-article edits that removed (or, as contrast, added) lead critical terms (measured sample since 2021)

{"null": "1000 random sets of the same size from all registered topic reverters, matched on revert-count decile", "remove": {"fast_reverters": 33, "coord_edge_accounts": {"set_size": 11, "overlap": 5, "expected_mean": 0.24, "expected_p95": 1.0, "p_upper": 0.001}, "voting_bloc_members": {"set_size": 19, "overlap": 8, "expected_mean": 0.36, "expected_p95": 1.0, "p_upper": 0.001}, "recurrent_tag_team_accounts": {"set_size": 31, "overlap": "<3", "expected_mean": 0.81, "expected_p95": 2.0, "p_upper": 0.1858}}, "add": {"fast_reverters": 44, "coord_edge_accounts": {"set_size": 11, "overlap": 7, "expected_mean": 0.29, "expected_p95": 1.0, "p_upper": 0.001}, "voting_bloc_members": {"set_size": 19, "overlap": 8, "expected_mean": 0.42, "expected_p95": 2.0, "p_upper": 0.001}, "recurrent_tag_team_accounts": {"set_size": 31, "overlap": "<3", "expected_mean": 0.9, "expected_p95": 3.0, "p_upper": 0.2278}}}

**Verdict:** inconclusive: fast reverters of critical-term removals overlap coord_edge_accounts, voting_bloc_members beyond matched random sets, but so do fast reverters of critical-term additions: a shared core of very active topic-area accounts, not removal-specific guarding

## 5. ArbCom primary source

See arbcom.md. primary source: 4 findings / remedies mention off-wiki coordination, canvassing, Discord, email or proxying (see arbcom.md)
