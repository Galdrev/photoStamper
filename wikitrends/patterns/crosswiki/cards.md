# Cross-wiki: how the narrative travelled between language editions

Generated 2026-11-08T12:32:13Z. Data to 2026-11-08. Nulls: 1000 draws. No usernames or account hashes appear here; accounts in the network are A1, A2...

## What the cross-wiki tier covers

**Confidence:** descriptive

78 language editions of the key articles ({'en': 8, 'ar': 8, 'de': 6, 'fr': 8, 'he': 6, 'nl': 8, 'pl': 7, 'pt': 8, 'ru': 7, 'es': 7, 'it': 5}), 107141 article revisions and 87429 talk revisions since 2021; 1196 term events (1192 pinned to an exact revision). One run-wide pseudonymous ID per account across all wikis.

**Null model:** {"draws": 1000, "calibration_worlds": 200, "expected_by_chance": "n/a"}

**So what:** Everything below is measured on the opening sections of these pages.

**Caveat:** Term detection is a word list per language (attribution by marker words); it misses paraphrase.

## Who said it first: English led most often

**Confidence:** low

In 32 article-term cells where 2+ editions added the term after 2021, the first mover was English 9 (chance 6.35), French 6 (chance 5.48), Spanish 6 (chance 5.03), German 3 (chance 2.28), Dutch 3 (chance 5.01). English moved before the other edition in 69% of 103 pairs (chance 58%, p=0.019); 16% followed English within 90 days (chance 11%, p=0.0559). In 17 more cases English already had the term before 2021 and the other edition added it later.

**Null model:** {"null": "each language's entry dates permuted across the cells where it has one (keeps each edition's general timing; breaks the link to the specific article and term)", "expected_english_first_share": 0.58, "expected_follow90_share": 0.11}

**So what:** A systematic leader is the edition the others follow; a short follow lag is consistent with copying or translation.

**Caveat:** First entry only; a term can enter and leave many times. Pages created after 2021 count their creation as entry.

## From 'accused of' to fact: where the encyclopedia's own voice took over

**Confidence:** low

Article-term paths from attributed to own voice: English 12 (median 430.1 d), Hebrew 6 (median 439.7 d), Portuguese 5 (median 827.5 d), Italian 4 (median 273.2 d), Russian 4 (median 540.4 d), Dutch 3 (median 845.6 d), Arabic 3 (median 1048.5 d), Spanish 2 (median 662.3 d), French 1 (median 1242.6 d). Own-voice transitions after 7 Oct 2023 vs expected from editing activity: English 12/18 (chance 16.64, p=0.9998), German 3/3 (chance 2.87, p=0.8734), French 14/15 (chance 14.2, p=0.8119), Spanish 3/5 (chance 4.65, p=0.997), Italian 56/56 (chance 54.44, p=0.205), Dutch 7/12 (chance 11.04, p=0.9998), Russian 9/9 (chance 8.52, p=0.6118), Hebrew 5/5 (chance 4.43, p=0.5441), Arabic 3/4 (chance 3.47, p=0.9121), Polish 3/3 (chance 2.55, p=0.6119), Portuguese 10/11 (chance 10.04, p=0.7496)

**Null model:** {"null": "transitions spread like the language's revisions (binomial on the after-war share of revisions)", "expected_after_war": {"en": 16.64, "de": 2.87, "fr": 14.2, "es": 4.65, "it": 54.44, "nl": 11.04, "ru": 8.52, "he": 4.43, "ar": 3.47, "pl": 2.55, "pt": 10.04}}

**So what:** Moving a charge from someone's mouth into the encyclopedia's voice is the strongest framing change.

**Caveat:** Voice = a term sentence without an attribution word of that language (a marker heuristic, not a coded reading). English key articles from ratchet carry voice only at event revisions.

## After 7 October: which editions moved with English

**Confidence:** high

Article-term cells present on 6 Oct 2023 -> now: English 7->13, German 1->3, French 1->12, Spanish 3->10, Italian 2->6, Dutch 9->12, Russian 2->5, Hebrew 4->7, Arabic 8->15, Polish 0->4, Portuguese 6->9. Insertions after the war vs expected from editing activity: English 115 (chance 110.555), German 26 (chance 23.62), French 96 (chance 84.025), Spanish 59 (chance 56.162), Italian 75 (chance 74.205), Dutch 54 (chance 52.115), Russian 33 (chance 31.323), Hebrew 25 (chance 24.101), Arabic 22 (chance 26.801), Polish 12 (chance 10.133), Portuguese 24 (chance 23.136)

**Null model:** {"null": "each page's insertion events moved to random revisions of the same page (keeps its activity curve)", "expected_after_war": {"en": 110.555, "de": 23.62, "fr": 84.025, "es": 56.162, "it": 74.205, "nl": 52.115, "ru": 31.323, "he": 24.101, "ar": 26.801, "pl": 10.133, "pt": 23.136}}

**So what:** English gained 7 and lost 1 cells; 'net_gain_vs_english' compares each edition.

**Caveat:** Cells are article x term family; presence anywhere in the opening section.

## The same accounts across editions

**Confidence:** high

153 of 8175 accounts (2%) edited the same key article in 2+ languages; chance 106.005 (p=0.001). Accounts that inserted a term family in 2+ languages: 0 (chance 0.0, p=1.0) of 281 inserters; removed in 2+ languages: 0 (chance 0.0, p=1.0) of 284 removers.

**Null model:** {"null": "within each language, accounts shuffled among accounts with the same activity (number of articles, or families, in that language); multilingual accounts stay multilingual", "expected_same_article": 106.005, "expected_insert_same_family": 0.0, "expected_remove_same_family": 0.0}

**So what:** Above chance means multilingual editors carry the same term across editions, not just edit in several.

**Caveat:** Same username = same global (SUL) account; local accounts checked for every term-event account. 'Not detected' means our tests found nothing beyond chance; with few events the tests have little power, so it is not proof that it did not happen.

## Same-day moves in different editions

**Confidence:** high

within 1h: same account 0 pairs (chance 0.0, p=1.0), different accounts 11 (chance 5.26, p=0.031); within 1d: same account 0 pairs (chance 0.0, p=1.0), different accounts 135 (chance 104.565, p=0.014); within 1w: same account 0 pairs (chance 0.0, p=1.0), different accounts 925 (chance 579.256, p=0.001). Clusters of one term moving in 3+ editions of the same article within 48 h: 3 (chance 1.28); flagged beyond the selection-calibrated null: 0.

**Null model:** {"null": "account-language timelines shifted at random (1-7 d for 1 h, 3-21 d for 1 d, 14-90 d for 1 w); clusters against the best cluster of each null world", "expected": {"1h": 5.26, "1d": 104.565, "1w": 579.256}, "expected_clusters": 1.28}

**So what:** Synchrony across editions beyond chance is what coordination would look like.

**Caveat:** News also synchronises editions (an ICJ ruling, a UN report): the time-shift null removes news timing too, so a flagged cluster is a lead to read, not proof of coordination. 'Not detected' means our tests found nothing beyond chance; with few events the tests have little power, so it is not proof that it did not happen.

## Cross-wiki blocs

**Confidence:** low

479 accounts with term events; 0 significant term co-activity edges (chance 0.0), 0 of them across languages; talk co-activity edges 8 (cross-language 8). Communities of 3+: 0, beyond chance: 0.

**Null model:** {"null": "analyze_coord engine with degree-preserving rewiring inside each language (shared article-language units) and 1-7 d timeline shifts, whole pipeline re-run on null worlds", "expected_by_chance": {"null_worlds": 200, "edges_mean": 0.0, "edges_p95": 0.0, "communities_mean": 0.0, "communities_p95": 0.0, "communities_max": 0}, "talk_expected_by_chance": {"null_worlds": 50, "edges_mean": 2.7, "edges_p95": 5.0, "communities_mean": 0.34, "communities_p95": 1.0, "communities_max": 2}}

**So what:** A bloc that spans editions is the cross-wiki form of a canvassed group.

**Caveat:** Nodes are A1, A2...; units are 'article [language]'. 'Not detected' means our tests found nothing beyond chance; with few events the tests have little power, so it is not proof that it did not happen.

## Cross-wiki activity and the documented canvassing windows

**Confidence:** low

No account set large enough to test.

**Null model:** {"null": "matched random account sets (same event counts), analyze_coord.window_alignment", "expected": {}}

**So what:** The windows are English-Wikipedia findings (ArbCom); here we ask whether cross-wiki activity clusters in them.

**Caveat:** Windows overlap the war's busiest news months; matched sets share that background. 'Not detected' means our tests found nothing beyond chance; with few events the tests have little power, so it is not proof that it did not happen.

## Hamas and 'terror': where the designation sits in each edition's opening

**Confidence:** descriptive

First sentence with a terror word, as sentence k of n (2021 -> now): Arabic none -> 6/6; German 1/13 -> 1/15; English 5/21 -> 22/23; Spanish 4/16 -> 5/18; French 8/9 -> 2/15; Italian 1/23 -> 2/10; Dutch 9/10 -> 6/9; Polish none -> 3/4; Portuguese 8/17 -> 2/28; Russian 3/5 -> 1/29.

**Null model:** {"null": "none (measurement)", "expected_by_chance": "n/a"}

**So what:** Moving the designation to the end of the opening changes what a skimming reader takes away.

**Caveat:** Sentence split on . ! ? ؟; template text removed. Terror word list: terror/terreur/террор/טרור/ارهاب.

## The hostages in the opening sections

**Confidence:** descriptive

Hostage mentions now (count, first sentence) by edition: Arabic: Gaza war 1, Hamas 0, Israel 0, October 7 attacks 0; German: Gaza war 4, Hamas 0, Israel 0, October 7 attacks 3; English: Gaza war 2, Hamas 0, Israel 0, October 7 attacks 1; Spanish: Gaza war 3, Hamas 1, Israel 0, October 7 attacks 1; French: Gaza war 4, Hamas 0, Israel 0, October 7 attacks 1; Hebrew: Gaza war 0, Israel 0, October 7 attacks 2; Italian: Gaza war 1, Hamas 1, October 7 attacks 1; Dutch: Gaza war 1, Hamas 0, Israel 0, October 7 attacks 1; Polish: Gaza war 2, Hamas 0, Israel 0; Portuguese: Gaza war 3, Hamas 1, Israel 0, October 7 attacks 2; Russian: Gaza war 3, Hamas 1, Israel 0, October 7 attacks 1.

**Null model:** {"null": "none (measurement)", "expected_by_chance": "n/a"}

**So what:** Whether the hostages appear at all, and how early, is a direct measure of whose suffering the opening foregrounds.

**Caveat:** Word list per language (hostage / Geisel / otage / rehén / חטופים / رهائن / أسرى ...); «أسرى» also means prisoners.

## How each edition names 7 October

**Confidence:** descriptive

First-sentence naming now: Arabic attack, incursion, operation; German attack, terror; English incursion; Spanish attack, operation; French attack, terror; Hebrew attack, massacre, terror; Italian attack, operation, terror; Dutch attack, terror; Portuguese attack; Russian incursion, operation. Renames: Arabic 2023-10-07 'معركة طوفان الأقصى' -> 'عملية طوفان الأقصى'; German 2023-10-07 'Angriff der Hamas auf Israel 2023' -> 'Oktober 2023 Gaza-Israel-Konflikt'; German 2023-10-07 'Oktober 2023 Gaza-Israel-Konflikt' -> 'Angriff der Hamas auf Israel 2023'; German 2023-10-08 'Angriff der Hamas auf Israel 2023' -> 'Gaza-Israel-Konflikt (Oktober 2023)'; German 2023-10-08 'Gaza-Israel-Konflikt (Oktober 2023)' -> 'Angriff der Hamas auf Israel 2023)'; German 2023-10-08 'Angriff der Hamas auf Israel 2023)' -> 'Angriff der Hamas auf Israel 2023'; German 2023-10-15 'Angriff der Hamas auf Israel 2023' -> 'Terror-Angriff der Hamas auf Israel 2023'; German 2023-10-17 'Terror-Angriff der Hamas auf Israel 2023' -> 'Terrorangriff der Hamas auf Israel 2023'; German 2023-10-17 'Hamas-Israel-Krieg 2023' -> 'Terrorangriff der Hamas auf Israel 2023'; English 2023-10-07 '2023 Hamas attack on Israel' -> 'October 2023 Hamas attack on Israel'; English 2023-10-10 'October 2023 Gaza−Israel conflict' -> 'October 2023 Gaza–Israel conflict'; English 2023-10-12 'Operation Al-Aqsa Flood' -> '2023 Hamas attacks on Israel'; English 2023-10-12 '2023 Hamas attacks on Israel' -> 'Operation Al-Aqsa Flood'; English 2023-10-22 '2023 Hamas attack on Israel' -> '2023 Hamas terrorist attack on Israel'; English 2023-10-22 'Operation Al-Aqsa Flood' -> '2023 Hamas attack on Israel'; English 2023-10-30 '2023 Hamas attack on Israel' -> 'October 7 Hamas attack on Israel'; English 2023-10-30 'October 7 Hamas attack on Israel' -> '2023 Hamas attack on Israel'; English 2023-11-28 '2023 Hamas attack on Israel' -> '2023 Hamas-led attack on Israel'; English 2024-06-22 '2023 Hamas-led attack on Israel' -> '7 October attacks'; English 2024-07-09 '7 October attacks' -> '2023 Hamas-led attack on Israel'; English 2024-10-10 '2023 Hamas-led attack on Israel' -> '7 October Hamas-led attack on Israel'; English 2024-12-30 '7 October Hamas-led attack on Israel' -> 'October 7 Hamas-led attack on Israel'; English 2025-05-26 'October 7 Hamas-led attack on Israel' -> 'October 7 Attacks'; English 2025-05-26 'October 7 Attacks' -> 'October 7 attacks'; Spanish 2025-01-31 'Operación Inundación de Al-Aqsa' -> 'Ataques del 7 de octubre'; Spanish 2025-09-22 'Operación Inundación de Al-Aqsa' -> 'Ataques de Hamás a Israel del 7 de octubre'; Spanish 2026-04-22 'Ataques de Hamás a Israel del 7 de octubre' -> 'Ataques del 7 de octubre'; French 2023-10-10 'Attaque du Hamas contre Israël' -> 'Attaque palestinienne contre Israël en 2023'; French 2023-10-10 'Attaque du Hamas contre Israël' -> 'Conflit israélo-palestinien de 2023'; French 2023-10-14 'Attaque du Hamas contre Israël' -> 'Guerre entre Israël et le Hamas'; French 2023-11-05 'Attaque du Hamas contre Israël' -> 'Attaque du Hamas contre Israël de 2023'; French 2023-11-05 'Attaque du Hamas contre Israël de 2023' -> 'Attaque du Hamas contre Israël'; French 2023-11-13 'Attaque du Hamas contre Israël' -> 'Attaque du Hamas contre Israël du 7 octobre 2023'; French 2023-11-14 'Attaque du Hamas contre Israël du 7 octobre 2023' -> 'Attaque du Hamas contre Israël'; French 2024-01-05 'Attaque du Hamas contre Israël' -> 'Attaque du Hamas contre Israël (octobre 2023)'; French 2024-01-05 'Attaque du Hamas contre Israël (octobre 2023)' -> 'Attaque du Hamas contre Israël de 2023'; French 2024-06-26 'Attaque du Hamas contre Israël de 2023' -> 'Attaque du Hamas contre Israël d'octobre 2023'; French 2026-10-16 'Attaque du Hamas contre Israël d'octobre 2023' -> 'Attaques du 7 octobre 2023'; Hebrew 2023-10-07 'מתקפת שמחת תורה' -> 'מתקפת פתע על ישראל (2023)'; Hebrew 2023-10-07 'מתקפת פתע על ישראל (2023)' -> 'מתקפת הפתע על ישראל (2023)'; Hebrew 2024-11-20 'מתקפת הפתע על ישראל (2023)' -> 'טבח שבעה באוקטובר'; Italian 2025-02-03 'Pogrom di Hamas in Israele del 2023' -> 'Attacco di Hamas a Israele del 2023'; Russian 2023-10-07 'Столкновения на границе Израиля с сектором Газа (2023)' -> 'Нападение ХАМАС на Израиль (2023)'; Russian 2023-10-07 'Нападение ХАМАС на Израиль (2023)' -> 'Нападение сектора Газа на Израиль (2023)'; Russian 2023-10-07 'Нападение сектора Газа на Израиль (2023)' -> 'Нападение ХАМАС на Израиль (2023)'; Russian 2023-10-08 'Нападение ХАМАС на Израиль (2023)' -> 'Вторжение ХАМАС в Израиль (2023)'; Russian 2023-10-08 'Вторжение ХАМАС в Израиль (2023)' -> 'Вторжение ХАМАСа в Израиль (2023)'; Russian 2023-10-08 'Вторжение ХАМАСа в Израиль (2023)' -> 'Вторжение ХАМАС в Израиль (2023)'; Russian 2023-10-12 'Вторжение ХАМАС в Израиль (2023)' -> 'Война Израиля с ХАМАС (2023)'; Russian 2023-10-12 'Война Израиля с ХАМАС (2023)' -> 'Вторжение ХАМАС в Израиль (2023)'; Russian 2025-05-08 'Вторжение ХАМАС в Израиль (2023)' -> 'Вторжение ХАМАС в Израиль'.

**Null model:** {"null": "none (measurement)", "expected_by_chance": "n/a"}

**So what:** 'Massacre', 'attack' and 'operation' tell three different stories of the same day.

**Caveat:** Classes from a multilingual word list on the first sentence; the title comes from the move log.

## Court rulings said more than the courts did

**Confidence:** descriptive

Arabic: icj_found_plausible_intent (Gaza genocide; 2024-04-17 -> 2026-10-10, still in the lead); English: icj_found_plausible_intent (Gaza genocide; 2024-03-17 -> 2024-05-05); French: icj_recognised_apartheid (Israeli apartheid; 2025-10-26 -> 2026-11-05, still in the lead); Italian: icj_plausibly_genocidal (Gaza genocide, Gaza war; 2025-03-09 -> 2026-10-28, still in the lead); Russian: court_found_israel_guilty (Israeli apartheid; 2025-03-31 -> 2026-09-24, still in the lead) What the courts said: icj_found_plausible_intent: ICJ order of 26 Jan 2024: found some of the rights South Africa claimed plausible; it made no finding of intent | icj_plausibly_genocidal: No ICJ ruling uses the phrase 'plausibly genocidal' | court_found_israel_guilty: ICJ advisory opinion of 19 Jul 2024 is non-binding and gives no verdict of guilt | icj_recognised_apartheid: ICJ advisory opinion of 19 Jul 2024 found a breach of CERD Article 3 without saying whether it was segregation or apartheid | icj_ruled_genocide: No ICJ judgment has found that Israel is committing genocide (merits pending)

**Null model:** {"null": "none (pattern flags)", "expected_by_chance": "n/a"}

**So what:** Turning a provisional order or a non-binding opinion into a finding is a factual error, not a framing choice.

**Caveat:** Flags are the patterns in LANGS.md finding 7 plus an English equivalent; each hit needs a human read.

## What sources came in with the term

**Confidence:** high

622 insertions with section-0 references at both revisions; 35% brought a new domain. Arriving classes: {'Other': 1254, 'Western wire & papers': 298, 'Rights orgs & UN': 221, 'Arab & Palestinian press, pro-Palestinian outlets': 101, 'Israeli press': 92, 'Scholarly (books, journals)': 73, 'Pro-Israel advocacy': 8}. Insertions that stuck brought a new source 50% of the time vs 28% for reverted ones (difference 0.22, chance 0.001, p=0.0005).

**Null model:** {"null": "stuck / reverted labels permuted across insertions", "expected_difference": 0.001, "expected_stuck_with_new_source": 71.0}

**So what:** Whether a framing sticks because it is sourced, or because it is pushed, is the core fairness question.

**Caveat:** Domains only (explore.SOURCE_CLASSES); citation templates without URLs count as no domain.

## Settled by a formal discussion, or by attrition?

**Confidence:** low

Of 26 English wordings that stuck (term entered or left and stayed 90+ days), 6 settled within 30 days after an RfC / move-request close (chance 2.3, p=0.0202); 9 stuck after failed attempts with no close nearby. Other editions changed the same term within 30 days after an English close 154 times (chance 192.33).

**Null model:** {"null": "stick dates uniform over 2021 -> now-90 d; each page's own close dates", "expected_by_chance": 2.3}

**So what:** A wording that settles right after a close was decided by the community's formal process.

**Caveat:** Close date = first signature after the close template; undated or unclosed items are counted but not aligned.

## When each edition opened a 'Gaza genocide' article

**Confidence:** descriptive

Gaza genocide: English 2023-12-29, French 2024-01-02 (+5 d), Arabic 2024-04-17 (+110 d), Portuguese 2024-05-01 (+124 d), Spanish 2024-10-24 (+301 d), Italian 2024-11-14 (+322 d), Polish 2025-01-11 (+380 d), Dutch 2025-05-11 (+500 d). Editions without one have no page in the data.

**Null model:** {"null": "none (dates)", "expected_by_chance": "n/a"}

**So what:** Opening a dedicated article is itself a framing decision.

**Caveat:** Creation = first revision of the current page (its history follows renames).

## Renames and protection

**Confidence:** descriptive

Renames since 2021: Arabic 2024-01-06 'الحرب الفلسطينية الإسرائيلية 2023' -> 'الحرب الفلسطينية الإسرائيلية 2023-2024'; Arabic 2024-01-07 'الحرب الفلسطينية الإسرائيلية 2023-2024' -> 'الحرب الفلسطينية الإسرائيلية 2023'; Arabic 2024-05-11 'الحرب الفلسطينية الإسرائيلية 2023' -> 'الحرب الفلسطينية الإسرائيلية'; Arabic 2024-05-18 'الحرب الفلسطينية الإسرائيلية' -> 'الحرب الفلسطينية الإسرائيلية 2023'; Arabic 2024-10-03 'الحرب الفلسطينية الإسرائيلية 2023' -> 'الحرب الفلسطينية الإسرائيلية'; Arabic 2024-10-04 'الحرب الفلسطينية الإسرائيلية' -> 'الحرب الفلسطينية الإسرائيلية 2023'; Arabic 2024-10-13 'الحرب الفلسطينية الإسرائيلية 2023' -> 'الحرب الفلسطينية الإسرائيلية (2023 – الآن)'; Arabic 2025-02-16 'الحرب الفلسطينية الإسرائيلية (2023 – الآن)' -> 'الحرب الفلسطينية الإسرائيلية (2023 – 2025)'; Arabic 2025-02-16 'الحرب الفلسطينية الإسرائيلية (2023 – 2025)' -> 'الحرب الفلسطينية الإسرائيلية (2023 – الآن)'; Arabic 2025-03-22 'الحرب الفلسطينية الإسرائيلية (2023 – الآن)' -> 'الحرب الفلسطينية الإسرائيلية (2023)'; Arabic 2025-03-22 'الحرب الفلسطينية الإسرائيلية (2023 – الآن)' -> 'الحرب الفلسطينية الإسرائيلية (2023)'; Arabic 2025-03-22 'الحرب الفلسطينية الإسرائيلية (2023)' -> 'الحرب الفلسطينية الإسرائيلية (2023 – الآن)'; Arabic 2025-09-10 'الحرب الفلسطينية الإسرائيلية (2023 – الآن)' -> 'الحرب الفلسطينية الإسرائيلية (2023 – 2027)'; Arabic 2025-09-10 'الحرب الفلسطينية الإسرائيلية (2023 – 2027)' -> 'الحرب الفلسطينية الإسرائيلية (2023 – الآن)'; Arabic 2025-10-09 'الحرب الفلسطينية الإسرائيلية (2023 – الآن)' -> 'الحرب الفلسطينية الإسرائيلية (2023 – 2025)'; Arabic 2025-10-09 'الحرب الفلسطينية الإسرائيلية (2023 – 2025)' -> 'الحرب الفلسطينية الإسرائيلية (2023–الآن)'; Arabic 2024-06-26 'مزاعم الإبادة الجماعية في هجوم إسرائيل على غزة عام 2023' -> 'الإبادة الجماعية في الحرب الفلسطينية الإسرائيلية 2023'; Arabic 2024-08-21 'الإبادة الجماعية في الحرب الفلسطينية الإسرائيلية 2023' -> 'الإبادة الجماعية لغزة'; Arabic 2023-04-01 'مؤسسو حركة حماس' -> 'حركة حماس'; Arabic 2023-10-07 'معركة طوفان الأقصى' -> 'عملية طوفان الأقصى'; German 2023-10-07 'Angriff der Hamas auf Israel 2023' -> 'Oktober 2023 Gaza-Israel-Konflikt'; German 2023-10-07 'Oktober 2023 Gaza-Israel-Konflikt' -> 'Angriff der Hamas auf Israel 2023'; German 2023-10-08 'Angriff der Hamas auf Israel 2023' -> 'Gaza-Israel-Konflikt (Oktober 2023)'; German 2023-10-08 'Gaza-Israel-Konflikt (Oktober 2023)' -> 'Angriff der Hamas auf Israel 2023)'; German 2023-10-08 'Angriff der Hamas auf Israel 2023)' -> 'Angriff der Hamas auf Israel 2023'; German 2023-10-15 'Angriff der Hamas auf Israel 2023' -> 'Terror-Angriff der Hamas auf Israel 2023'; German 2023-10-17 'Terror-Angriff der Hamas auf Israel 2023' -> 'Terrorangriff der Hamas auf Israel 2023'; German 2023-10-17 'Terrorangriff der Hamas auf Israel 2023' -> 'Hamas-Israel-Krieg 2023'; German 2023-10-17 'Hamas-Israel-Krieg 2023' -> 'Terrorangriff der Hamas auf Israel 2023'; German 2024-01-07 'Krieg in Israel und Gaza 2023' -> 'Krieg in Israel und Gaza seit 2023'; German 2025-01-19 'Krieg in Israel und Gaza (2023 bis 2025)' -> 'Krieg in Israel und Gaza seit 2023'; German 2023-10-07 'Angriff der Hamas auf Israel 2023' -> 'Oktober 2023 Gaza-Israel-Konflikt'; German 2023-10-07 'Oktober 2023 Gaza-Israel-Konflikt' -> 'Angriff der Hamas auf Israel 2023'; German 2023-10-08 'Angriff der Hamas auf Israel 2023' -> 'Gaza-Israel-Konflikt (Oktober 2023)'; German 2023-10-08 'Gaza-Israel-Konflikt (Oktober 2023)' -> 'Angriff der Hamas auf Israel 2023)'; German 2023-10-08 'Angriff der Hamas auf Israel 2023)' -> 'Angriff der Hamas auf Israel 2023'; German 2023-10-15 'Angriff der Hamas auf Israel 2023' -> 'Terror-Angriff der Hamas auf Israel 2023'; German 2023-10-17 'Terror-Angriff der Hamas auf Israel 2023' -> 'Terrorangriff der Hamas auf Israel 2023'; German 2023-10-17 'Hamas-Israel-Krieg 2023' -> 'Terrorangriff der Hamas auf Israel 2023'; English 2023-10-07 '2023 Hamas attack on Israel' -> 'October 2023 Hamas attack on Israel'; English 2023-10-07 'October 2023 Hamas attack on Israel' -> 'October 2023 Gaza−Israel conflict'; English 2023-10-10 'October 2023 Gaza−Israel conflict' -> 'October 2023 Gaza–Israel conflict'; English 2023-10-10 'October 2023 Gaza–Israel conflict' -> '2023 Israel–Hamas war'; English 2023-10-22 '2023 Hamas attack on Israel' -> '2023 Hamas terrorist attack on Israel'; English 2023-10-30 '2023 Hamas attack on Israel' -> 'October 7 Hamas attack on Israel'; English 2023-11-28 '2023 Hamas attack on Israel' -> '2023 Hamas-led attack on Israel'; English 2024-01-20 '2023 Israel–Hamas war' -> 'Israel–Hamas war'; English 2025-01-27 'Israel–Hamas war' -> 'Gaza war'; English 2025-05-01 'Gaza genocide' -> 'Make Israel Great Again'; English 2024-02-29 'Allegations of genocide in the 2023 Israeli attack on Gaza' -> 'Attempted genocide by Israel in their 2023 attack on Gaza'; English 2024-02-29 'Attempted genocide by Israel in their 2023 attack on Gaza' -> 'Allegations of genocide in the 2023 Israeli attack on Gaza'; English 2024-07-03 'Allegations of genocide in the 2023 Israeli attack on Gaza' -> 'Gaza genocide'; English 2025-05-01 'Make Israel Great Again' -> 'Gaza genocide'; English 2021-04-03 'An Nakba' -> 'Nakba'; English 2023-10-07 '2023 Hamas attack on Israel' -> 'October 2023 Hamas attack on Israel'; English 2023-10-10 'October 2023 Gaza−Israel conflict' -> 'October 2023 Gaza–Israel conflict'; English 2023-10-12 'Operation Al-Aqsa Flood' -> '2023 Hamas attacks on Israel'; English 2023-10-12 '2023 Hamas attacks on Israel' -> 'Operation Al-Aqsa Flood'; English 2023-10-22 '2023 Hamas attack on Israel' -> '2023 Hamas terrorist attack on Israel'; English 2023-10-22 'Operation Al-Aqsa Flood' -> '2023 Hamas attack on Israel'; English 2023-10-30 '2023 Hamas attack on Israel' -> 'October 7 Hamas attack on Israel'; English 2023-10-30 'October 7 Hamas attack on Israel' -> '2023 Hamas attack on Israel'; English 2023-11-28 '2023 Hamas attack on Israel' -> '2023 Hamas-led attack on Israel'; English 2024-06-22 '2023 Hamas-led attack on Israel' -> '7 October attacks'; English 2024-07-09 '7 October attacks' -> '2023 Hamas-led attack on Israel'; English 2024-10-10 '2023 Hamas-led attack on Israel' -> '7 October Hamas-led attack on Israel'; English 2024-12-30 '7 October Hamas-led attack on Israel' -> 'October 7 Hamas-led attack on Israel'; English 2025-05-26 'October 7 Hamas-led attack on Israel' -> 'October 7 Attacks'; English 2025-05-26 'October 7 Attacks' -> 'October 7 attacks'; English 2022-09-12 'Israel and the apartheid analogy' -> 'Israel and apartheid'; English 2024-08-05 'Israel and apartheid' -> 'Israeli apartheid'; English 2025-07-07 'Felix Klein (German antisemitism commmisioner)' -> 'Felix Klein (German Antisemitism Commissioner)'; Spanish 2023-10-07 'Ataque de Hamás a Israel de 2023' -> 'Conflicto israelí-palestino de 2023'; Spanish 2023-10-08 'Conflicto israelí-palestino de 2023' -> 'Conflicto israelí-gaza de 2023'; Spanish 2023-10-08 'Conflicto israelí-gaza de 2023' -> 'Conflicto israelí-palestino de 2023'; Spanish 2023-10-09 'Conflicto israelí-palestino de 2023' -> 'Conflicto israelí-palestino de octubre 2023'; Spanish 2023-10-09 'Conflicto israelí-palestino de octubre 2023' -> 'Conflicto israelí-palestino de octubre de 2023'; Spanish 2023-11-02 'Conflicto israelí-palestino de octubre de 2023' -> 'Conflicto israelí-palestino de octubre y noviembre de 2023'; Spanish 2023-11-02 'Conflicto israelí-palestino de octubre y noviembre de 2023' -> 'Conflicto israelí-palestino de octubre de 2023'; Spanish 2023-11-02 'Conflicto israelí-palestino de octubre de 2023' -> 'Guerra Israel-Gaza de 2023'; Spanish 2024-01-01 'Guerra Israel-Gaza de 2023' -> 'Guerra Israel-Gaza (2023-presente)'; Spanish 2024-02-12 'Guerra Israel-Gaza (2023-presente)' -> 'Guerra entre Israel y Gaza (2023-presente)'; Spanish 2024-02-12 'Guerra entre Israel y Gaza (2023-presente)' -> 'Guerra Israel-Gaza (2023-presente)'; Spanish 2024-06-19 'Guerra Israel-Gaza (2023-presente)' -> 'Guerra entre Israel y Gaza (2023-presente)'; Spanish 2024-06-19 'Guerra entre Israel y Gaza (2023-presente)' -> 'Guerra Israel-Gaza (2023-presente)'; Spanish 2025-06-23 'Guerra Israel-Gaza (2023-presente)' -> 'Guerra de Gaza'; Spanish 2025-09-29 'Genocidio en Gaza' -> 'Genocidio palestino en Gaza'; Spanish 2025-01-31 'Operación Inundación de Al-Aqsa' -> 'Ataques del 7 de octubre'; Spanish 2025-09-22 'Operación Inundación de Al-Aqsa' -> 'Ataques de Hamás a Israel del 7 de octubre'; Spanish 2026-04-22 'Ataques de Hamás a Israel del 7 de octubre' -> 'Ataques del 7 de octubre'; Spanish 2024-05-17 'Israel y la analogía del apartheid' -> 'Apartheid israelí'; French 2026-06-05 'L’etat terroriste Israël' -> 'Israël'; French 2023-10-07 'Opération Inondation d'Al-Aqsa' -> 'Conflit israélo-palestinien d'octobre 2023'; French 2023-10-07 'Conflit israélo-palestinien d'octobre 2023' -> 'Opération Déluge d'al-Aqsa'; French 2023-10-09 'Opération Déluge d'al-Aqsa' -> 'Attaque du Hamas contre Israël'; French 2023-10-10 'Attaque du Hamas contre Israël' -> 'Attaque palestinienne contre Israël en 2023'; French 2023-10-10 'Attaque palestinienne contre Israël en 2023' -> 'Attaque du Hamas contre Israël'; French 2023-10-10 'Attaque du Hamas contre Israël' -> 'Conflit israélo-palestinien de 2023'; French 2023-10-10 'Conflit israélo-palestinien de 2023' -> 'Attaque du Hamas contre Israël'; French 2023-10-14 'Attaque du Hamas contre Israël' -> 'Guerre entre Israël et le Hamas'; French 2023-10-16 'Guerre entre Israël et le Hamas' -> 'Guerre entre Israël et le Hamas de 2023'; French 2023-10-20 'Guerre entre Israël et le Hamas de 2023' -> 'Guerre Israël-Hamas de 2023'; French 2023-11-05 'Attaque du Hamas contre Israël' -> 'Attaque du Hamas contre Israël de 2023'; French 2023-11-11 'Guerre Israël-Hamas de 2023' -> 'Guerre Israël-Gaza de 2023'; French 2023-11-11 'Guerre Israël-Gaza de 2023' -> 'Guerre Israël-Hamas de 2023'; French 2023-11-13 'Attaque du Hamas contre Israël' -> 'Attaque du Hamas contre Israël du 7 octobre 2023'; French 2023-12-11 'Guerre Israël-Hamas de 2023' -> 'Guerre Israëlo-palestinienne de 2023'; French 2023-12-11 'Guerre Israëlo-palestinienne de 2023' -> 'Guerre Israël-Hamas de 2023'; French 2024-01-04 'Guerre Israël-Hamas de 2023' -> 'Guerre Israël-Hamas de 2023 - 2024'; French 2024-01-04 'Guerre Israël-Hamas de 2023 - 2024' -> 'Guerre Israël-Hamas de 2023-2024'; French 2024-01-05 'Attaque du Hamas contre Israël' -> 'Attaque du Hamas contre Israël (octobre 2023)'; French 2024-03-11 'Guerre Israël-Hamas de 2023-2024' -> 'Affrontements Israël-Hamas de 2023-2024'; French 2024-03-11 'Affrontements Israël-Hamas de 2023-2024' -> 'Guerre Israël-Hamas de 2023-2024'; French 2024-04-08 'Guerre Israël-Hamas de 2023-2024' -> 'Guerre Israël-Gaza depuis 2023'; French 2024-04-08 'Guerre Israël-Gaza depuis 2023' -> 'Guerre Israël-Hamas de 2023-2024'; French 2024-05-29 'Guerre Israël-Hamas de 2023-2024' -> 'Guerre Israël-Hamas (depuis 2023)'; French 2024-07-11 'Guerre Israël-Hamas (depuis 2023)' -> 'Guerre Israël-Hamas (depuis octobre 2023)'; French 2024-07-11 'Guerre Israël-Hamas (depuis octobre 2023)' -> 'Guerre Israël-Hamas (depuis 2023)'; French 2024-07-11 'Guerre Israël-Hamas (depuis 2023)' -> 'Guerre Israël-Hamas (depuis le 7 octobre 2023)'; French 2024-07-11 'Guerre Israël-Hamas (depuis le 7 octobre 2023)' -> 'Guerre Israël-Hamas (depuis 2023)'; French 2025-01-15 'Guerre Israël-Hamas (depuis 2023)' -> 'Guerre Israël-Hamas (2023-2025)'; French 2025-01-16 'Guerre Israël-Hamas (2023-2025)' -> 'Guerre Israël-Hamas (depuis 2023)'; French 2025-04-05 'Guerre Israël-Hamas (depuis 2023)' -> 'Guerre à Gaza depuis 2023'; French 2025-06-17 'Guerre à Gaza depuis 2023' -> 'Guerre de Gaza depuis 2023'; French 2024-08-08 'Allégations de génocide lors de l’attaque israélienne sur Gaza en 2023' -> 'Génocide de Gaza'; French 2024-08-08 'Génocide de Gaza' -> 'Allégations de génocide lors de l’attaque israélienne sur Gaza en 2023'; French 2024-08-27 'Allégations de génocide lors de l’attaque israélienne sur Gaza en 2023' -> 'Risque de génocide à Gaza depuis 2023'; French 2024-11-08 'Risque de génocide à Gaza depuis 2023' -> 'Génocide à Gaza'; French 2024-11-09 'Risque de génocide à Gaza depuis 2023' -> 'Génocide à Gaza'; French 2024-11-09 'Risque de génocide à Gaza depuis 2023' -> 'Génocide à Gaza'; French 2025-06-16 'Risque de génocide à Gaza depuis 2023' -> 'Génocide à Gaza'; French 2023-10-10 'Attaque du Hamas contre Israël' -> 'Attaque palestinienne contre Israël en 2023'; French 2023-10-10 'Attaque du Hamas contre Israël' -> 'Conflit israélo-palestinien de 2023'; French 2023-10-14 'Attaque du Hamas contre Israël' -> 'Guerre entre Israël et le Hamas'; French 2023-11-05 'Attaque du Hamas contre Israël' -> 'Attaque du Hamas contre Israël de 2023'; French 2023-11-05 'Attaque du Hamas contre Israël de 2023' -> 'Attaque du Hamas contre Israël'; French 2023-11-13 'Attaque du Hamas contre Israël' -> 'Attaque du Hamas contre Israël du 7 octobre 2023'; French 2023-11-14 'Attaque du Hamas contre Israël du 7 octobre 2023' -> 'Attaque du Hamas contre Israël'; French 2024-01-05 'Attaque du Hamas contre Israël' -> 'Attaque du Hamas contre Israël (octobre 2023)'; French 2024-01-05 'Attaque du Hamas contre Israël (octobre 2023)' -> 'Attaque du Hamas contre Israël de 2023'; French 2024-06-26 'Attaque du Hamas contre Israël de 2023' -> 'Attaque du Hamas contre Israël d'octobre 2023'; French 2026-10-16 'Attaque du Hamas contre Israël d'octobre 2023' -> 'Attaques du 7 octobre 2023'; French 2024-10-26 'Israël et l'analogie de l'apartheid' -> 'Apartheid israélien'; Hebrew 2023-10-29 'הלחימה ברצועת עזה במלחמת חרבות ברזל' -> 'הלחימה הקרקעית ברצועת עזה במלחמת חרבות ברזל'; Hebrew 2023-10-29 'הלחימה הקרקעית ברצועת עזה במלחמת חרבות ברזל' -> 'הלחימה ברצועת עזה במלחמת חרבות ברזל'; Hebrew 2025-07-13 'הלחימה ברצועת עזה במלחמת חרבות ברזל' -> 'זירת עזה במלחמת חרבות ברזל'; Hebrew 2025-08-16 'זירת עזה במלחמת חרבות ברזל' -> 'זירת רצועת עזה במלחמת חרבות ברזל'; Hebrew 2023-10-07 'מתקפת שמחת תורה' -> 'מתקפת פתע על ישראל (2023)'; Hebrew 2023-10-07 'מתקפת פתע על ישראל (2023)' -> 'מתקפת הפתע על ישראל (2023)'; Hebrew 2024-11-20 'מתקפת הפתע על ישראל (2023)' -> 'טבח שבעה באוקטובר'; Hebrew 2021-05-22 'השוואה בין ישראל לאפרטהייד' -> 'טענות למדיניות אפרטהייד בישראל'; Hebrew 2021-08-24 'טענות למדיניות אפרטהייד בישראל' -> 'טענות למדיניות אפרטהייד על ידי ישראל'; Italian 2023-11-27 'Conflitto Gaza-Israele del 2023' -> 'Guerra Hamas-Israele del 2023'; Italian 2024-03-29 'Guerra Hamas-Israele del 2023' -> 'Guerra di Gaza'; Italian 2024-09-12 'Guerra di Gaza' -> 'Guerra Israele-Hamas'; Italian 2024-11-14 'Genocidio di Gaza' -> 'Genocidio nella Striscia di Gaza'; Italian 2025-03-13 'Accuse di genocidio nella Striscia di Gaza' -> 'Genocidio nella Striscia di Gaza'; Italian 2025-03-14 'Accuse di genocidio nella Striscia di Gaza' -> 'Genocidio nella Striscia di Gaza'; Italian 2025-03-25 'Accuse di genocidio nella Striscia di Gaza' -> 'Genocidio nella Striscia di Gaza'; Italian 2025-05-20 'Accuse di genocidio nella Striscia di Gaza' -> 'Genocidio nella Striscia di Gaza'; Italian 2025-08-06 'Accuse di genocidio nella Striscia di Gaza' -> 'Genocidio nella Striscia di Gaza'; Italian 2025-02-03 'Pogrom di Hamas in Israele del 2023' -> 'Attacco di Hamas a Israele del 2023'; Dutch 2023-10-07 'Gaza-oorlog' -> 'Israëlisch-Palestijns conflict (2023)'; Dutch 2023-10-13 'Israëlisch-Palestijns conflict (2023)' -> 'Hamas-Israël oorlog (2023)'; Dutch 2023-10-13 'Hamas-Israël oorlog (2023)' -> 'Israëlisch-Palestijns conflict (2023)'; Dutch 2024-01-10 'Israëlisch-Palestijns conflict (2023)' -> 'Oorlog Hamas-Israël (2023-2024)'; Dutch 2024-01-10 'Oorlog Hamas-Israël (2023-2024)' -> 'Oorlog Hamas-Israël'; Dutch 2025-06-09 'Oorlog Hamas-Israël' -> 'Oorlog in Gaza vanaf 2023'; Dutch 2025-12-20 'Oorlog in Israël vanaf 2023' -> 'Oorlog in Gaza vanaf 2023'; Dutch 2025-12-18 'Verdenking van genocide in Gaza' -> 'Genocide in Gaza'; Dutch 2022-06-19 'Israëlische apartheid' -> 'Israel en apartheid'; Dutch 2022-06-20 'Israel en apartheid' -> 'Israël en apartheid'; Polish 2023-10-11 'Atak Hamasu na Izrael (2023)' -> 'Wojna Izraela z Hamasem (2023)'; Polish 2023-10-11 'Wojna Izraela z Hamasem (2023)' -> 'Wojna Izraela z Hamasem'; Polish 2023-11-02 'Wojna Izraela z Hamasem (2023)' -> 'Wojna Izraela z Hamasem'; Polish 2026-04-26 'Zarzuty ludobójstwa w Strefie Gazy' -> 'Ludobójstwo w Strefie Gazy'; Portuguese 2023-10-07 'Ataque do Hamas a Israel em 2023' -> 'Conflito israelo-palestino de outubro de 2023'; Portuguese 2023-10-07 'Conflito israelo-palestino de outubro de 2023' -> 'Conflito israelo-palestino de 2023'; Portuguese 2024-01-01 'Conflito israelo-palestino de 2023' -> 'Conflito israelo-palestino (2023 - Presente)'; Portuguese 2024-01-01 'Conflito israelo-palestino (2023 - Presente)' -> 'Conflito israelo-palestino (2023-presente)'; Portuguese 2024-01-02 'Conflito israelo-palestino (2023-presente)' -> 'Conflito israelo-palestino (2023–presente)'; Portuguese 2024-01-09 'Conflito israelo-palestino (2023–presente)' -> 'Guerra Israel-Hamas de 2023'; Portuguese 2024-01-09 'Guerra Israel-Hamas de 2023' -> 'Guerra Israel-Hamas'; Portuguese 2025-06-18 'Guerra Israel-Hamas' -> 'Guerra de Gaza (2023-presente)'; Portuguese 2025-08-24 'Guerra de Gaza (2023-presente)' -> 'Guerra de Gaza (2023–presente)'; Portuguese 2025-10-10 'Guerra de Gaza (2023–presente)' -> 'Guerra de Gaza'; Portuguese 2026-10-13 'Guerra de Gaza (2023–presente)' -> 'Guerra de Gaza'; Portuguese 2026-10-14 'Guerra de Gaza (2023–presente)' -> 'Guerra de Gaza'; Portuguese 2026-10-14 'Guerra de Gaza (2023–presente)' -> 'Guerra de Gaza'; Portuguese 2024-07-14 'Alegações de genocídio no ataque israelita de 2023 a Gaza' -> 'Genocídio em a Gaza'; Portuguese 2024-07-14 'Genocídio em a Gaza' -> 'Genocídio em Gaza'; Portuguese 2024-08-10 'Genocídio em Gaza' -> 'Genocídio na Faixa de Gaza'; Portuguese 2025-05-03 'Analogia Israel-Apartheid' -> 'Apartheid israelense'; Russian 2023-10-08 'Контртеррористическая операция в Секторе Газа (2023)' -> 'Операция «Железные мечи»'; Russian 2023-11-10 'Операция «Железные мечи»' -> 'Война в Газе (2023)'; Russian 2023-11-13 'Война в Газе (2023)' -> 'Война Израиля с ХАМАСом (2023)'; Russian 2023-11-14 'Война Израиля с ХАМАСом (2023)' -> 'Война в Газе (2023)'; Russian 2024-01-01 'Война в Газе (2023)' -> 'Война в Газе (с 2023)'; Russian 2024-07-25 'Война в Газе (с 2023)' -> 'Война в секторе Га́за ( с 2023)'; Russian 2024-07-25 'Война в секторе Га́за ( с 2023)' -> 'Война в Газе (с 2023)'; Russian 2025-01-19 'Война в Газе (с 2023)' -> 'Война в Газе (2023—2025)'; Russian 2025-01-19 'Война в Газе (2023—2025)' -> 'Война в Газе (с 2023)'; Russian 2025-10-10 'Война в Газе (с 2023)' -> 'Война в Газе (2023—2025)'; Russian 2025-10-10 'Война в Газе (2023—2025)' -> 'Война в Газе (с 2023)'; Russian 2025-10-13 'Война в Газе (с 2023)' -> 'Война в Газе (2023-2025)'; Russian 2025-10-13 'Война в Газе (2023-2025)' -> 'Война в Газе (с 2023)'; Russian 2025-10-13 'Война в Газе (с 2023)' -> 'Война в Газе'; Russian 2023-10-07 'Столкновения на границе Израиля с сектором Газа (2023)' -> 'Нападение ХАМАС на Израиль (2023)'; Russian 2023-10-07 'Нападение ХАМАС на Израиль (2023)' -> 'Нападение сектора Газа на Израиль (2023)'; Russian 2023-10-07 'Нападение сектора Газа на Израиль (2023)' -> 'Нападение ХАМАС на Израиль (2023)'; Russian 2023-10-08 'Нападение ХАМАС на Израиль (2023)' -> 'Вторжение ХАМАС в Израиль (2023)'; Russian 2023-10-08 'Вторжение ХАМАС в Израиль (2023)' -> 'Вторжение ХАМАСа в Израиль (2023)'; Russian 2023-10-08 'Вторжение ХАМАСа в Израиль (2023)' -> 'Вторжение ХАМАС в Израиль (2023)'; Russian 2023-10-12 'Вторжение ХАМАС в Израиль (2023)' -> 'Война Израиля с ХАМАС (2023)'; Russian 2023-10-12 'Война Израиля с ХАМАС (2023)' -> 'Вторжение ХАМАС в Израиль (2023)'; Russian 2025-05-08 'Вторжение ХАМАС в Израиль (2023)' -> 'Вторжение ХАМАС в Израиль'. Protection actions since 2021 per edition: Arabic 13, German 45, English 46, Spanish 35, French 49, Hebrew 28, Italian 29, Dutch 17, Polish 15, Portuguese 11, Russian 47.

**Null model:** {"null": "none (log records)", "expected_by_chance": "n/a"}

**So what:** A title is the first framing a reader sees; protection decides who may change the text.

**Caveat:** Renames are moves confirmed in the move log; protection levels are each wiki's own names.

## How many readers met each framing

**Confidence:** descriptive

Share of key-article views after 7 Oct 2023 whose opening stated 'genocide' in the encyclopedia's own voice: English 11%, German n/a, French 9%, Spanish 10%, Italian 5%, Dutch 7%, Russian 1%, Hebrew 4%, Arabic 3%, Polish 2%, Portuguese 1%.

**Null model:** {"null": "none (exposure measurement)", "expected_by_chance": "n/a"}

**So what:** Exposure turns a wording into an audience: what millions actually read.

**Caveat:** Monthly user views (all access) summed over current and former titles; framing at mid-month.

## The one-line descriptions search engines show

**Confidence:** descriptive

Wikidata description changes since 2021 (after the war): .

**Null model:** {"null": "none (change records)", "expected_by_chance": "n/a"}

**So what:** These short lines appear under search results and in AI answers.

**Caveat:** Values come from edit summaries; bulk edits are counted without values.
