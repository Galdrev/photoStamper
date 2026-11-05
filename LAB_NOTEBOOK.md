# Lab notebook: how this study was run

This is a log of process decisions, so you can judge later which techniques are worth adopting for real work.
Each entry gives the technique, why it was used, what it cost, and a verdict after use: **KEEP**, **ADAPT** or **DROP**.

## Decisions log

| # | Phase | Technique | Why | Cost | Verdict |
|---|-------|-----------|-----|------|---------|
| 1 | Plan | Hypothesis + explicit null + control group written before any data | Stops confirmation bias. The comparison group is what makes a result mean anything | 10 min | KEEP. Should be standard on any "is X getting worse?" question |
| 2 | Gather | Hit a network block, routed collection through GitHub Actions in the user's own repo | Legit path around the sandbox's network policy. Free tier minutes | 15 min, $0 | KEEP. A useful pattern: CI runners as a data-collection worker |
| 3 | Gather | First CI run crashed on one bad category call | No error tolerance; one failure killed the run | 1 run lost | Lesson: wrap every external call. Never let one item kill a batch. Always save partial results |
| 4 | Build | Ran the pipeline on synthetic data before real data arrived | Catches crashes without burning the slow fetch | 5 min | KEEP |
| 5 | Delegate | 4 parallel background agents: prior work, method, code review, design | Independent work. I keep the conclusions, not the file dumps | ~400k subagent tokens, ~5 min wall time each | KEEP. Prior-work gave dated validation targets I would not have had; method gave the pre-registration idea |
| 6 | Verify | Code review agent briefed with the code and no conclusions | A read that isn't anchored on mine | ~100k tokens | **KEEP, strongest single step.** It found 5 result-corrupting bugs (redirect snapshots worth 2,500/10k, back-matter counted, cache mixing, new-article distortion, non-directional lexicon). It found them before real data, so the fixes are still pre-registered |
| 7 | Plan | Pre-registration (SPEC.md) committed before data, with an amendment log | Anthropic best practice ("write the spec") plus the social-science norm. The git timestamp proves it | 15 min | KEEP. Forces a headline decision rule in advance |
| 8 | Verify | Known-answer validation targets from press coverage | Plays the role of an eval set: the instrument must recover known shifts | 5 min | pending |
| 9 | Plan | Rejected: human gold set + DSL estimator, cross-vendor grader | No human coders or OpenAI key here. Substituted: known-answer targets, 2 Claude sizes × 2 prompt wordings | — | ADAPT. For real work with stakes, pay for the human gold set |
| 11 | Build | Caught my own design flaw: the name-swap placebo gets undone by the masking | Self-review of the agent's recommendation against my implementation | 2 min | Lesson: an advisor's recommendation can be incoherent with your other choices. Replaced with an unmasked-repeat test |
| 12 | Delegate | Coding rubric packaged as a repo Skill (.claude/skills/blind-stance-coder) | Anthropic Agent Skills pattern: identical instructions for every worker, versioned in git | 10 min | pending |
| 13 | Verify | User pushback: "sampling sounds basic". Replaced the eyeball check with written acceptance tests on 100% of the data, including hash integrity against Wikipedia's own sha1 | Data QA is a contract written before looking, not an impression | 15 min | KEEP. The user's challenge improved the process. Lesson: say what "good data" means before looking at any |
| 14 | Verify | 6-article sample run in a parallel CI job, with the acceptance tests run locally | Catch defects before the 2-hour full run lands | 10 min, $0 | **KEEP.** sha1 integrity was 137/137. But an INFO-level number (14 short snapshots) revealed that the cleaner deleted wikitables, so list articles lost about 95% of their text and a validation target was invisible. Lesson: read the INFO lines, not just PASS/FAIL |
| 15 | Verify | Validation targets against press claims | Known-answer tests | — | Mixed, and informative. 2 of 3 testable targets passed. Zionism's "colonization" wording entered between Apr and Jul 2024, earlier than the press timeline. The original target is kept as a FAIL and a separate POST-HOC target is labelled as such, rather than quietly moving the goalposts |
| 16 | Explore | "Go wild" handled by labelling: 4 exploratory analyses + exact-revision tracing, all marked as not pre-registered | Freedom to explore without contaminating the confirmatory test | 30 min | KEEP. The separation between pre-registered and exploratory is what keeps exploration honest |
| 17 | Build | Named a file bisect.py, which shadowed Python's stdlib and broke `random` | Caught by a mock test before CI | 1 min | Lesson: mock-test every new script locally, even ones that need the network |
| 18 | Explore | Organic vs organised: 7 aggregate signals, each against a null model (popularity-preserving overlap, circular-shift timelines), with editors as per-run salted hashes | Answers the user's question without building a dossier on volunteers. Null models stop shared-interest editing reading as collusion | 25 min | pending |
| 19 | Plan | User reframed: Wikipedia as a crowd-built record *guarded as truth*. Restructured the thesis into content / process / epistemics, and added the strongest natural control: the same articles in 10 other-language Wikipedias | Same rules and software, different communities: isolates community from facts | 20 min | KEEP. The user's domain framing produced the best design idea of the project |
| 20 | Present | Design agent delivered an editorial scroll story, verified by my own look at the screenshots (not just its report) | Trust but verify: read the artifact, not the summary | 300k tokens, 27 min | KEEP. Strong result. Delegating design with a precise brief plus a data contract worked |
| 21b | Verify | Mass frame v2 composition: topic = Israel 1,400 / Palestine 1,400 / Judaism 1,400 / Jewish history 505; comparison = 22 projects × 260 | Composition gate passed; 10,433 articles | — | KEEP |
| 21 | Plan | User pushback: "580 I could do with chat deep research". Added a mass tier: up to 8,000 articles sampled from WikiProject importance ratings (the community's own taxonomy, not my picks), plus 10 languages for the top 1,600, fanned out over 10 parallel CI jobs | The real edge of code over chat is coverage and a sampling frame nobody hand-picked | 30 min to build, about 600 CI minutes | pending |
| 22 | Explore | User hypothesis "push, undo, push, until it slips through" turned into a measurable ratchet test: the lead of every revision (API section=0, 50 per call) for 40 key articles, with insertion/removal survival and failed attempts before sticking | A domain intuition becomes a falsifiable metric with a comparison group | 25 min | pending |
| 23 | Verify | Read the mass frame job's log before letting 10 shards spend about 600 minutes: topic side = Judaism only (Israel/Palestine categories have other names), comparison dominated by Russia/India Top/High | Kill criterion caught it only partly (counts passed!). Reading composition, not just totals, caught it | about 5 CI min lost | **KEEP.** A count gate is not enough. Check *composition*. Fixed with category discovery, per-project caps and a fail-fast frame validator |
| 24 | Verify | Method revisit #2 (builders' guidance vs the *current* design) found real flaws in my coder: examples lopsided 4–5:1 toward "less favourable" and using the study's own loaded words; single A/B order; a 5-item gate | Re-reading guidance after the design has changed surfaces things that weren't relevant at the start | 87k tokens, 2 min | **KEEP, high value.** Periodic method revisits beat a one-time playbook. My own rubric was leaking the hypothesis |
| 25 | Present | User: "lab feels like work, I meant play". Ran 3 concept agents with deliberately different personas (data journalist, interaction designer, public statistician) in parallel; brainstorm only, no code | Diversity of personas → diverse options; convergence across them is a signal (all 3 independently proposed a "shadow/ghost comparison", 2 proposed shuffle, flipbook and ratchet heartbeat) | ~190k tokens, about 1 min | **KEEP.** Cheap, fast, and the convergence made picking easy |
| 26 | Present | Written grading criteria (DESIGN_CRITERIA.md) shared by builder and critic, from Anthropic's harness-design post (evaluator needs explicit criteria or it drifts toward approval) | Makes "wow" and "honest" scorable | 10 min | pending |
| 27 | Build | Split the page into two independently owned files (report template vs lab fragment) so two builder agents can work in parallel without edit conflicts | Parallelism needs separated ownership | 5 min | pending |
| 28 | Verify | The report builder agent, while building a chart, noticed the R4 estimate sat outside its own CI: the weighted bootstrap ignored the weights | Builders who draw data honestly double as validators | — | KEEP. Fixed: weighted bootstrap; no permutation p for the reweighted test |
| 29 | Present | Creative director (evaluator agent, explicit rubric) actually *used* the page via Playwright and verdict ITERATE: report 45,000px on phone, placeholder "pending" shipped, unit mismatch (per 1k vs per 10k), a floating pill covering data. Proposed the boldest idea ("the definition breathes") | Generator/evaluator loop from Anthropic's harness post. The evaluator caught things both builders' self-checks scored as passing | 107k tokens, 4 min | **KEEP, strongest design step.** Self-evaluation by the builder was too lenient (both scored themselves ≥3 everywhere). A separate judge with a rubric was not |
| 30 | Verify | CD round 2: the lab's Galaxy shuffled single articles and claimed "beyond chance". Articles within a WikiProject are correlated, so the band was too narrow. The same flaw applies to my pre-registered article-level permutation, so I added R8 (cluster bootstrap by subgroup), reported but not counted | A design critic found a *statistics* flaw by asking why two parts of the page disagreed | — | **KEEP.** Inconsistency between views is a bug detector |
| 31 | Verify | CD round 3: the builder's "back link fixed, 58px" was tested with a hand-made intent; real taps still failed. The critic found the root cause (`from` never passed). Orchestrator applied the one-line fix and re-ran the critic's own real-tap test: 6/6 pass | Test with the user's real path, not a synthetic shortcut. An agent's "verified" claim is only as good as its test | 3 rounds | **KEEP.** Evaluator-optimizer loop: 3 rounds took the scorecard from 2s to 4s/5s. Result: SHIP |
| 32 | Process | User: "you didn't test the process". True: I ran 2 multi-hour CI jobs blind (no logs while running), then cancelled them without visibility, killing 2 nearly finished mass shards. Rebuilt for observability: shared rate-limited net layer with counters, heartbeats pushed to a status branch every 3 min, checkpointed shards that resume, hard time budgets so analysis always runs, dry-run modes on test branches, and a live monitor on my side. Unit-tested against a misbehaving fake server and a simulated kill/resume | Long-running agentic work needs telemetry and graceful degradation, not hope (the "observability" and "durable execution" lessons from Anthropic's multi-agent post) | ~45 min, ~2.5 CI-hours lost | **KEEP, top lesson.** Orchestrator accountability: test the process, not just the code; never act on a running job you can't see |
| 33 | Process | Dry run 1 caught 3 real defects before full scale: (a) mass analyze wrote into an old results.json and the commit crashed on unstaged changes; (b) **GitHub's default shell has no pipefail, so `python … | tee` hid a Python crash as a green step**; (c) silent empty outputs (trace of an unfetched article returned 0 with no warning). Also measured Wikipedia's aggregate throttle (about 1/3 of requests throttled at ~30 rps total vs 3.5% at 5 rps) and re-planned the load | Dry runs plus reading *every* log line, not the green checkmarks | 2 dry runs, ~25 CI min | **KEEP, top lesson.** A green CI run is not evidence; logs are. Always dry-run a long pipeline end to end on a tiny slice |
| 34 | Process | Full run: fetch 598/598 with 0 failures and sha1 integrity 13,498/13,498. Analysis then crashed on real data (a None at the end date in R3), and pipefail surfaced it as a red step instead of a silent green. Reading the QA log revealed a worse, silent bug: the cache held 872 files vs 598 in the manifest, and stale articles from earlier corpora would have entered the analysis with old labels. Fixed both, then stress-tested every stage on hostile synthetic data (stale files, shrinking leads, new articles, redirects, zero-hit articles) before relaunching | Real data finds the cases synthetic data didn't think of. Turn each one into a fuzz case | 1 failed run | **KEEP.** Every real failure becomes a permanent test case |
| 35 | Process | The heartbeat paid off: ratchet showed 5/40 articles after 45 min, ETA 265 min, inside a 50-min budget. The counters showed it was latency- and bandwidth-bound (2.1 s per request, 2 GB of section-0 text because leads include infoboxes), not throttled. Moved it into a dedicated workflow with per-article checkpoints, 8 threads and a 4.5 h budget, after a mock resume test | Telemetry turned a silent loss into a 10-minute fix | — | **KEEP.** Budget long tasks from measured rates, not guesses |
| 36 | Process | My own error: I committed ratchet.json to the research branch while the main run was about to commit a file at the same path. Its final step hit a rebase conflict, and 3 h of results that lived only on the ephemeral runner were lost (raw cache survived, so the rerun costs about 1 h). Fix: every CI run now pushes results to its own new branch `results/<run_id>`, so bot writes can never conflict with mine; I merge files deliberately | Two writers, one path, no lock. The classic multi-agent coordination bug (the C-compiler post's file locks) | ~3 CI-hours | **KEEP.** Give every agent or job its own output namespace; merge explicitly |
| 37 | Process | Hit GitHub's free Actions quota (private repo, 2,000 min/month) mid-pipeline. Diagnosed from the check-run annotation, not a guess. Gave the user 4 options; they chose to make the repo public (unlimited minutes). Before flipping, I scanned every branch for secrets and removed the only raw data with Wikipedia usernames (6 sample articles) from all branches. The proxy forbade the settings change, so the user flipped it. Then I re-ran only the failed job (mass merge) and relaunched main | Budget limits are real constraints. Escalate to the user with priced options; never work around a billing limit | ~15 min | **KEEP.** Estimate total CI minutes *before* fanning out; I never budgeted the parallel runs against the quota |
| 38 | Verify | **Re-identification test: 25/30 masked leads were named exactly by an AI** (4 more partly). Masking entity names does not blind a model that has read Wikipedia. My first scorer (keyword regex) undercounted this as 12/30, and reading the raw guesses caught it. Blind coding is downgraded to "masked coding, known blinding failure" and stays exploratory | The blinding check, added after the method revisit, earned its place: without it the report would have overclaimed "blind" coding | 1 agent | **KEEP, important.** Always test your blinding, and read raw outputs, not your own summary metric |
| 10 | Build | Synthetic test exposed the log1p scale blowing up for articles starting at zero | Planted-effect test: a known drift must be recovered | 5 min | KEEP. Always test the stats on data where you know the answer |

## Open questions to judge at the end
- Did the parallel agents produce anything I wouldn't have produced alone?
- Did blind coding agree with the lexicon counts?
- What would I cut if I had a tenth of the budget?

## Rabbit-hole guard: kill criteria fixed before results
Each exploratory branch goes on the page only if it passes its sanity gate. Otherwise it is cut and the cut is logged here.

| Branch | Sanity gate (instrument works) | Kill if |
|---|---|---|
| Lexicon counts | KWIC precision ≥ 60% per frame on a 40-hit sample | the frame is dropped (not the whole study) |
| Blind stance coding | ≥ 70% correct direction on known-answer changes; pairwise agreement ≥ 0.6 | reported as a failed instrument, not used for conclusions |
| Hedging (E1) | ≥ 70% of a 30-item sample correctly marked hedged/unhedged | dropped |
| Citations (E2) | "Other" class < 50% of refs (classifier covers most sources) | reported descriptively only |
| Terror labelling (E3) | ≥ 5 armed-group articles per side with mentions | dropped |
| Coordination signals | null model produces non-zero baselines; ratios stable across 2 seeds | dropped |
| Ratchet | ≥ 30 insertion events per group for critical terms | reported per article only, no group claim |
| Cross-language | ≥ 6 languages with ≥ 10 articles per group | reported per article only |
| Mass tier | ≥ 1,000 articles per group in the frame | fix category names, else report deep tier only |
| Narrative coding | coders agree on the main theme in ≥ 60% of a double-coded 30-item subset | themes shown as examples only, no shares |

## Study 2 (user insight after reading study 1)
| # | Phase | Technique | Why | Cost | Verdict |
|---|---|---|---|---|---|
| 39 | Plan | User spotted the design's blind spot: study 1 measured one direction (critical words), not **two narratives against each other** (indigeneity, ancient naming, holy-site naming order, the two displacements, 1948 agency, violence labels by perpetrator, legitimacy words, Jewish history in shared-site leads). Pre-registered as SPEC_NARRATIVE.md before computing, with comparison disputes (Kosovo, Karabakh, Cyprus, Kashmir, Northern Ireland) and planted-shift tests | A domain expert's framing beats the analyst's first operationalisation. Reusing the raw cache made a new study cost a reanalysis, not a recollection | ~1 h build | pending |

| 40 | Plan | User: "do the two narratives support each other at scale; clean irrelevant articles, but with common tools, don't fix the research". Pre-registered coherence (Spearman + PCA), an outcome-blind relevance filter (Wikidata P31 types + 2021 baseline text only), and standard OLS with cluster-robust SEs (statsmodels). Every result is reported filtered *and* unfiltered. A synthetic test exposed a bias in my own filter (comparison articles outside the disputes had no baseline and would all have been dropped); fixed before any real run | Cleaning is where researchers most often "fix" results. Fixing the rule before seeing outcomes and always showing both versions is the standard guard | ~1 h | pending |

## Final verdicts: what to adopt for real work

**Adopt (highest value per hour):**
1. **Pre-registration with a written decision rule (SPEC.md + amendment log).** The headline had to say "not supported" even though exploratory results looked more interesting. That is the whole point.
2. **A separate adversarial verifier given only the claims and the data.** It found 12 problems in my findings, several of them real overclaims, and reproduced every core number. The builders' and my own self-checks missed them.
3. **An evaluator agent with a written rubric (creative director).** It took design scores from 2 to 4–5 in 3 rounds. Builders' self-scores were always too generous.
4. **Data validator on the real page.** It found 9 contradictions between page text and data, including 2 in my own takeaway cards.
5. **Telemetry plus dry runs for long jobs.** Heartbeats, checkpoints, time budgets, pipefail, a per-run output namespace. Every serious failure in this project was a missing one of these.
6. **Known-answer tests for instruments** (synthetic edits, validation targets, planted effects). They caught the log-scale blow-up, and they let the coder be calibrated.
7. **Test your blinding.** 25/30 masked texts were re-identified. Without the test, the report would have claimed "blind" coding.

**Adapt:**
- **Parallel persona agents for brainstorming.** Cheap, and convergence across personas is a good signal. Pick 3, not 10.
- **Method revisits at checkpoints.** Valuable, but only once the design has changed.
- **Large agent fan-out for coding (≈60 coder calls).** It works with a pilot gate. But real-edit stance coding was noisy (agreement 0.50–0.70), so for real stakes, pay for a human gold set.

**Drop or avoid:**
- Acting on a long job you cannot see (I cancelled 2 nearly finished shards blind).
- Two writers to one path with no lock (one run's results lost).
- Fanning out without a compute budget (hit the GitHub minutes quota).
- Count-only gates (a 4,000-article frame that was "mostly Russia" passed).

**Answers to the open questions:**
- *Did parallel agents produce things I wouldn't have alone?* Yes. Dated validation targets, the cluster-correlation catch, the "breathing definition" opener, the re-identification idea and the 12 verifier corrections.
- *Did blind coding agree with lexicon counts?* Direction yes, significance no, and the blinding failed. It is the weakest instrument.
- *With a tenth of the budget?* Keep the pre-registered deep test, the mass tier, the adversarial verifier and the data validator. Cut the narrative coding and most design rounds.

## #41 Study 3: let the data sharpen the questions, without fooling ourselves (2026-11-05)
- **Trigger:** the owner saw the uneven picture (a few articles moved a lot) and asked for better questions, not a better-looking answer.
- **Technique:** split-sample discovery → confirmation. A deterministic 50/50 split by sha1("study3|"+title) was committed (c3a07bf) *before* any hypothesis was made. Three discovery agents (where/what, how/who, narrative) see only the discovery half. Their hypotheses get frozen in SPEC_STUDY3.md, then run once, unchanged, on the holdout half plus study 2 (unseen).
- **Honest limit:** the aggregate study 1 results were already known to everyone, so the holdout protects against article-level overfitting, not against knowing the headline.
- **Adopt at work?** Yes. It is the cheapest guard against "we found a pattern in noise". It costs half your data for discovery, so it fits best when n is in the thousands (the mass tier).

## #42 Event updates vs narrative change (2026-11-05)
- **Trigger:** the owner pointed out that the Israel article *should* gain sentences about October 7. That is coverage, not narrative.
- **Technique:** a symmetric, outcome-blind sentence filter (`event_filter.py`). Sentences naming a year ≥ 2022, a fixed list of recent events for BOTH topic and comparison conflicts, or recency wording are "event"; the rest is the "narrative residual". We report unfiltered, residual and event share side by side. The rule was frozen in SPEC_STUDY3 amendment D before any filtered number existed. It is conservative: it also drops recent-scholarship sentences.
- **Ops decision:** cancelled both runs mid-way (main at fetch 75%, mass-narr at 47%). Reason: the mass run didn't store lead text, so it could never be filtered later. The relaunch stores the lead prose (any future filter runs offline), fetches the pre-war lead too (needed for the DiD), and runs 4 shards at 2 rps instead of 2 at 3. Raw fetch is cached, so the main run loses minutes, not hours.
- **Adopt at work?** Yes: "store the raw text, compute features later" beats "compute features in the crawler" every time a new question shows up.

## #43 Qualitative close reading → frozen codebook → masked double coding (2026-11-05)
- **Pipeline:**
  1. Three close readers with different lenses (voice, historiography, editorial process) did open coding on the discovery half.
  2. A methods agent triangulated their codes into 12 KPIs and froze them in SPEC_STUDY3 Part C.
  3. Two independent LLM coders coded 205 masked holdout pairs, with randomised A/B order, a verbatim-quote check and κ per KPI.
- **Result:** the moves were real but not topic-specific. Comparison leads showed them as often or more. One move flipped direction (camp labels: 6% vs 0% in discovery, 2% vs 9% in holdout), and another vanished entirely ("Zionist militants" relabelling: 0 in both groups).
- **Lesson:** close readers who read mostly the *most-changed* topic articles see vivid, convincing patterns. The comparison group and a sealed half are what stop vivid from being mistaken for distinctive. Without the holdout we would have published 3 false content findings.
- **Process slip:** coders shared one scratchpad, so a helper file collided and two coders saw a file path from the other coder. Next time, give each coder its own working directory in the prompt.
- **Adopt at work?** Yes, the whole chain. It is the cheapest honest way to turn "I feel there's a pattern in these documents" into a number that can fail.

## #44 A green shard that was 92% errors (2026-11-05)
- **What happened:** after amendment D, mass-narr shard 0 finished "success". The heartbeat showed `article_errors: 2387`: a division by zero when a filtered part was empty. My unit test only used texts that contained an event sentence.
- **Caught by:** reading the heartbeat's error counter, not the green tick.
- **Fixes:** empty parts now return None; edge-case tests added (empty text, no events, all events); and `mass._run` now exits non-zero when more than 5% of a shard's articles fail, so a mostly-failed shard can never show green again.
- **Adopt at work?** Yes. Make the error rate a pass/fail condition, not just a log line. Test the empty case first.

## #45 Scope change: from hypothesis testing to sense-making (2026-11-05)
- **Owner's call:** stop running this as an academic study. Look at the data from many angles, find the patterns and trends, and decide what we can conclude or do.
- **Setup:** three analyst agents, each owning a set of angles: when/where/what-words; how/who; story/sources/languages. They share one brief. Every pattern comes back as a card with: what we see, chart data, confidence (STRONG / SUGGESTIVE / ANECDOTE), "so what" and a caveat. A synthesis pass follows, then the page.
- **Kept from the academic phase:** the comparison group and the confidence label. Dropped: pre-registration ceremony, BH corrections and holdout splits for new angles.
- **Adopt at work?** Yes. A card format with a forced confidence label lets you explore freely without the deck overclaiming.

## #46 The results push that said "pushed" and wasn't (2026-11-05)
- **What happened:** the main run finished, then its commit step was refused. GitHub won't let the bot create a branch whose history adds a workflow file that is new relative to the nearest ref. My echo after the retry loop still printed "pushed". The run left no artifact, so its results are gone and the run is repeated.
- **Fix:** `push_data.sh` pushes results to an orphan branch, `wikitrends-data`, whose history never contains workflow files. That is the same trick that has always worked for status heartbeats. It exits non-zero on failure. Every workflow now also uploads an artifact as a backup. A rescue workflow can pull another run's artifacts and push them, which saves the in-flight mass-narr and pilot runs that still use the old commit step.
- **Second silent-success bug today** (after #44). Pattern: any "done" message must be conditional on the thing actually happening.
- **Adopt at work?** Yes. Keep results in a separate data-only branch or bucket, decoupled from code history. And always keep a second copy until the first is verified.

## #47 Mass v2: one crawl, every shortlisted signal (2026-11-05)
- **Scope (from the pilot evaluation):** about 10.3k unique pages after resolving redirects. Each gets:
  - 3 full snapshots parsed once: short description, infobox, categories, concept links, lead citation domains, narrative and event-filter features, and the P/J displacement split;
  - revision metadata: sizes, tags and summary classes;
  - aggregated account facts;
  - talk-page data, now and history;
  - RfCs and requested moves;
  - pageviews across former titles;
  - Wikidata;
  - the protection log;
  - exact lead term events over the full history, including heavy pages.

  About 182k requests, 16 shards, about 12 h.
- **Privacy decision:** the engineer's fallback put a shared salt in a run artifact. In a public repo anyone could download it during the run and reverse the published editor hashes. Replaced with per-shard random salts that are never stored. Cost: editor hashes are only linkable within a shard. A repo secret `WT_SALT_SEED` would restore cross-shard linking safely, if the owner sets one.
- **Adopt at work?** Yes: put a privacy review before scale. The convenient design was the leaky one.
