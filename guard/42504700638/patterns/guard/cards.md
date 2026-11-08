# Revert guarding, tag teams and voting blocs (aggregate only)

Generated 2026-11-08T18:21:34Z. No usernames, account hashes or revision ids appear here; account counts of 1-2 are shown as <3. Each card gives the observed value, what the comparison articles or the null model give, and a one-line verdict.

Scope: {'topic': 254, 'comparison': 254} articles ({'topic': {'High': 82, 'Top': 55, 'core': 117}, 'comparison': {'High': 82, 'Top': 110, 'core': 62}}); revisions (thousands) {'topic': 614.2, 'comparison': 843.8}; coord network recomputed in the same job: {'available': True, 'edges': 16, 'accounts': 13, 'articles_collected': 959, 'articles_expected': 959, 'complete': True}.

## 1. Revert guarding

Totals: {'reverts': 242619, 'reverts_by_bots': 10410, 'reverts_by_ip_or_temp': 15045, 'kinds': {'identity': 214555, 'summary': 21565, 'undo': 6448, 'restore': 51}, 'reverts_since_2021': 27417, 'direction_measured': 27307, 'direction_measured_share_of_window': 0.996, 'directions': {'topic': {'none': 9339, 'add': 274, 'remove': 233}, 'comparison': {'none': 17136, 'remove': 180, 'add': 145}}}

**Topic vs comparison, full history** (86503 vs 130661 reverts by registered accounts; concentration rarefied to 86503).
- median_h: topic 0.434 [0.34, 0.547] vs comparison 0.329 [0.259, 0.419]; difference 0.105 [-0.028, 0.241], label-permutation p 0.1329
- fast24: topic 0.93 [0.92, 0.938] vs comparison 0.938 [0.929, 0.945]; difference -0.008 [-0.021, 0.004], label-permutation p 0.2058
- top5: topic 0.101 [0.09, 0.117] vs comparison 0.04 [0.038, 0.058]; difference 0.061 [0.038, 0.074], label-permutation p 0.001
- top10: topic 0.155 [0.141, 0.174] vs comparison 0.064 [0.062, 0.09]; difference 0.091 [0.06, 0.104], label-permutation p 0.001
- gini: topic 0.786 [0.762, 0.787] vs comparison 0.731 [0.719, 0.743]; difference 0.055 [0.028, 0.057], label-permutation p 0.001

**Topic vs comparison, since 2021** (9272 vs 16484 reverts by registered accounts; concentration rarefied to 9272).
- median_h: topic 1.523 [1.084, 2.141] vs comparison 1.13 [0.842, 1.427]; difference 0.393 [-0.162, 1.096], label-permutation p 0.1578
- fast24: topic 0.859 [0.826, 0.888] vs comparison 0.871 [0.856, 0.884]; difference -0.011 [-0.047, 0.023], label-permutation p 0.4476
- top5: topic 0.102 [0.089, 0.132] vs comparison 0.084 [0.077, 0.133]; difference 0.017 [-0.028, 0.04], label-permutation p 0.1728
- top10: topic 0.165 [0.149, 0.204] vs comparison 0.142 [0.133, 0.198]; difference 0.022 [-0.031, 0.053], label-permutation p 0.1998
- gini: topic 0.687 [0.645, 0.703] vs comparison 0.639 [0.625, 0.673]; difference 0.048 [-0.001, 0.053], label-permutation p 0.002

**Reverts of critical-term removals vs additions, topic articles** (227 vs 260 measured reverts; accounts 91 vs 154).
- median_h: removals 1.131 [0.616, 1.694] vs additions 0.836 [0.489, 1.443]; difference 0.296 [-0.413, 1.05], direction-permutation p 0.9331
- fast24: removals 0.907 [0.854, 0.944] vs additions 0.923 [0.878, 0.955]; difference -0.016 [-0.075, 0.04], direction-permutation p 0.2787
- top5: removals 0.251 [0.243, 0.388] vs additions 0.136 [0.137, 0.251]; difference 0.115 [0.044, 0.193], direction-permutation p 0.005
- top10: removals 0.41 [0.403, 0.569] vs additions 0.232 [0.233, 0.387]; difference 0.178 [0.077, 0.264], direction-permutation p 0.001
- gini: removals 0.47 [0.382, 0.518] vs additions 0.309 [0.282, 0.417]; difference 0.161 [0.024, 0.177], direction-permutation p 0.001

**Reverts of critical-term removals vs additions, comparison articles** (172 vs 135 measured reverts; accounts 120 vs 87).
- median_h: removals 0.084 [0.033, 0.269] vs additions 0.357 [0.178, 1.805]; difference -0.273 [-1.568, -0.128], direction-permutation p 0.004
- fast24: removals 0.942 [0.886, 0.977] vs additions 0.874 [0.788, 0.936]; difference 0.068 [0.001, 0.146], direction-permutation p 0.03
- top5: removals 0.173 [0.156, 0.341] vs additions 0.193 [0.19, 0.402]; difference -0.02 [-0.173, 0.059], direction-permutation p 0.8062
- top10: removals 0.268 [0.26, 0.489] vs additions 0.304 [0.326, 0.575]; difference -0.035 [-0.193, 0.039], direction-permutation p 0.4585
- gini: removals 0.232 [0.22, 0.423] vs additions 0.285 [0.28, 0.44]; difference -0.053 [-0.134, 0.043], direction-permutation p 0.2987

**Difference in differences (topic minus comparison, removal minus addition):** median_h 0.569 [-0.128, 2.051]; fast24 -0.084 [-0.184, -0.001]; top5 0.135 [0.032, 0.3]; top10 0.213 [0.095, 0.388]; gini 0.214 [0.028, 0.265]

**Verdict:** inconclusive: one guarding signature (speed or concentration) beyond chance, not both

## 2. Tag-team reverting

a tag-team sequence = 2+ reverts toward the same version (same sha1 restored) of one article by 2+ different registered non-bot accounts, consecutive reverts no more than W hours apart. Null: reverter labels shuffled among the reverts of the same article and calendar month (who reverts in that article-month is kept; who reverts toward which version is broken), 500 draws.

**Window 24 h.** Sequences: topic 9663, comparison 15641. Per article: {'topic': 39.602, 'comparison': 65.444, 'difference': -25.841, 'difference_ci95': [-46.972, -5.313], 'p_label_permutation': 0.021}. Per 1,000 reverts: {'topic': 111.707, 'comparison': 119.707, 'difference': -8.0, 'difference_ci95': [-18.879, 3.359], 'p_label_permutation': 0.2038}.
- topic: sequences 9663 (shuffle 11941.0); pairs on 3+ articles {'observed': 430.0, 'null_mean': 579.634, 'null_p95': 605.0, 'p_upper': 1.0, 'excess_over_null': -149.634}; pairs on 2+ articles {'observed': 1385.0, 'null_mean': 1948.314, 'null_p95': 2001.0, 'p_upper': 1.0, 'excess_over_null': -563.314}; accounts in 3+-article pairs {'observed': 202, 'null_mean': 236.414, 'null_p95': 250.0, 'p_upper': 1.0, 'excess_over_null': -34.414}; pairs recurring beyond their own shuffle distribution {'rule': "pair shares sequences on 3+ distinct articles and p<0.01 against that pair's own shuffle distribution", 'observed': 19, 'expected_by_chance_mean': 9.89, 'expected_p95': 15.0, 'accounts': 30, 'groups_3plus_accounts': {'count': 3, 'sizes': [8, 3, 3]}}
- comparison: sequences 15641 (shuffle 19130.7); pairs on 3+ articles {'observed': 323.0, 'null_mean': 358.44, 'null_p95': 382.0, 'p_upper': 0.998, 'excess_over_null': -35.44}; pairs on 2+ articles {'observed': 1508.0, 'null_mean': 1804.93, 'null_p95': 1868.0, 'p_upper': 1.0, 'excess_over_null': -296.93}; accounts in 3+-article pairs {'observed': 233, 'null_mean': 237.442, 'null_p95': 253.0, 'p_upper': 0.7146, 'excess_over_null': -4.442}; pairs recurring beyond their own shuffle distribution {'rule': "pair shares sequences on 3+ distinct articles and p<0.01 against that pair's own shuffle distribution", 'observed': 21, 'expected_by_chance_mean': 11.46, 'expected_p95': 18.0, 'accounts': 36, 'groups_3plus_accounts': {'count': 4, 'sizes': [3, 3, 3, 3]}}

**Window 72 h.** Sequences: topic 11223, comparison 18115. Per article: {'topic': 45.996, 'comparison': 75.795, 'difference': -29.799, 'difference_ci95': [-53.884, -7.769], 'p_label_permutation': 0.013}. Per 1,000 reverts: {'topic': 129.741, 'comparison': 138.641, 'difference': -8.9, 'difference_ci95': [-18.306, 0.754], 'p_label_permutation': 0.0869}.
- topic: sequences 11223 (shuffle 13474.4); pairs on 3+ articles {'observed': 557.0, 'null_mean': 764.784, 'null_p95': 796.0, 'p_upper': 1.0, 'excess_over_null': -207.784}; pairs on 2+ articles {'observed': 1857.0, 'null_mean': 2489.26, 'null_p95': 2544.1, 'p_upper': 1.0, 'excess_over_null': -632.26}; accounts in 3+-article pairs {'observed': 253, 'null_mean': 289.338, 'null_p95': 303.0, 'p_upper': 1.0, 'excess_over_null': -36.338}; pairs recurring beyond their own shuffle distribution {'rule': "pair shares sequences on 3+ distinct articles and p<0.01 against that pair's own shuffle distribution", 'observed': 22, 'expected_by_chance_mean': 10.2, 'expected_p95': 15.0, 'accounts': 32, 'groups_3plus_accounts': {'count': 4, 'sizes': [8, 4, 3, 3]}}
- comparison: sequences 18115 (shuffle 21504.8); pairs on 3+ articles {'observed': 422.0, 'null_mean': 472.164, 'null_p95': 499.0, 'p_upper': 1.0, 'excess_over_null': -50.164}; pairs on 2+ articles {'observed': 1935.0, 'null_mean': 2274.44, 'null_p95': 2335.0, 'p_upper': 1.0, 'excess_over_null': -339.44}; accounts in 3+-article pairs {'observed': 282, 'null_mean': 294.096, 'null_p95': 309.05, 'p_upper': 0.9102, 'excess_over_null': -12.096}; pairs recurring beyond their own shuffle distribution {'rule': "pair shares sequences on 3+ distinct articles and p<0.01 against that pair's own shuffle distribution", 'observed': 22, 'expected_by_chance_mean': 12.76, 'expected_p95': 19.0, 'accounts': 40, 'groups_3plus_accounts': {'count': 4, 'sizes': [3, 3, 3, 3]}}

**Verdict:** inconclusive: recurrent pairs above the shuffle null, but few or not above the comparison articles

## 3. Voting blocs on talk pages

!votes (support / oppose / include / exclude / keep / delete / option X...) in RfC, requested-move and AfD discussions on the talk pages (and archives) of the scoped articles; one stance per account per discussion; accounts with 3+ votes in the group, discussions with 3+ such voters. Null: stances permuted among the voters of each discussion, 1000 draws; significant pair: p<0.01 and 3+ agreements; blocs: Louvain on significant pairs, 3+ accounts; 100 calibration worlds.

**topic:** {"discussions_with_3plus_regular_voters": 217, "discussion_kinds": {"afd": 9, "rm": 115, "rfc": 93}, "regular_voters": 351, "pairs_with_3plus_shared_discussions": 1520, "significant_agreement_pairs": {"observed": 30, "expected_by_chance_mean": 0.53, "expected_p95": 2.0, "calibration_worlds": 100}, "share_of_pairs_agreeing_80pct_plus": {"observed": 0.287, "null_mean": 0.117, "null_ci95": [0.101, 0.132], "p_upper": 0.001}, "mean_pair_agreement": {"observed": 0.512, "null_mean": 0.506}, "blocs": {"count": 3, "sizes": [9, 7, 4], "expected_by_chance_mean": 0.0, "expected_p95": 0.0, "detail": [{"size": 9, "within_bloc_agreement": 0.891, "null_mean": 0.524, "null_ci95": [0.461, 0.592], "p_upper": 0.001}, {"size": 7, "within_bloc_agreement": 0.955, "null_mean": 0.525, "null_ci95": [0.451, 0.617], "p_upper": 0.001}, {"size": 4, "within_bloc_agreement": 1.0, "null_mean": 0.479, "null_ci95": [0.324, 0.647], "p_upper": 0.001}]}}

**comparison:** {"discussions_with_3plus_regular_voters": 92, "discussion_kinds": {"rm": 65, "rfc": 24, "afd": 3}, "regular_voters": 128, "pairs_with_3plus_shared_discussions": 46, "significant_agreement_pairs": {"observed": 0, "expected_by_chance_mean": 0.0, "expected_p95": 0.0, "calibration_worlds": 100}, "share_of_pairs_agreeing_80pct_plus": {"observed": 0.348, "null_mean": 0.263, "null_ci95": [0.152, 0.391], "p_upper": 0.1119}, "mean_pair_agreement": {"observed": 0.618, "null_mean": 0.656}, "blocs": {"count": 0, "sizes": [], "expected_by_chance_mean": 0.0, "expected_p95": 0.0, "detail": []}}

**Overlap with the recomputed coord edges:** {'coord_edges': 16, 'coord_edges_that_are_voting_pairs_with_3plus_shared': 4, 'of_which_significant_agreement_pairs': 0, 'expected_significant_by_chance': 0.08, 'coord_accounts_among_regular_voters': 7, 'coord_accounts_in_voting_blocs': 3, 'expected_in_blocs_by_chance': 0.4, 'expected_p95': 2.0, 'p_upper': 0.007}

**Verdict:** supports organised guarding: more high-agreement pairs and voting blocs than the stance permutation produces

## 4. Are the fast reverters the same accounts?

fast reverter = registered non-bot account with 2+ reverts, within 24 h, of topic-article edits that removed (or, as contrast, added) lead critical terms (measured sample since 2021)

{"null": "1000 random sets of the same size from all registered topic reverters, matched on revert-count decile", "remove": {"fast_reverters": 33, "coord_edge_accounts": {"set_size": 13, "overlap": 6, "expected_mean": 0.25, "expected_p95": 1.0, "p_upper": 0.001}, "voting_bloc_members": {"set_size": 20, "overlap": 8, "expected_mean": 0.41, "expected_p95": 2.0, "p_upper": 0.001}, "recurrent_tag_team_accounts": {"set_size": 30, "overlap": 4, "expected_mean": 0.69, "expected_p95": 2.0, "p_upper": 0.006}}, "add": {"fast_reverters": 44, "coord_edge_accounts": {"set_size": 13, "overlap": 8, "expected_mean": 0.33, "expected_p95": 1.0, "p_upper": 0.001}, "voting_bloc_members": {"set_size": 20, "overlap": 8, "expected_mean": 0.42, "expected_p95": 2.0, "p_upper": 0.001}, "recurrent_tag_team_accounts": {"set_size": 30, "overlap": 4, "expected_mean": 0.87, "expected_p95": 3.0, "p_upper": 0.006}}}

**Verdict:** supports organised guarding: fast reverters of critical-term removals overlap coord_edge_accounts, voting_bloc_members, recurrent_tag_team_accounts beyond matched random sets

## 5. ArbCom primary source

See arbcom.md. primary source: 4 findings / remedies mention off-wiki coordination, canvassing, Discord, email or proxying (see arbcom.md)
