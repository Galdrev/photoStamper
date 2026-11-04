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
| 10 | Build | Synthetic test exposed the log1p scale blowing up for articles starting at zero | Planted-effect test: a known drift must be recovered | 5 min | KEEP. Always test the stats on data where you know the answer |

## Open questions to judge at the end
- Did the parallel agents produce anything I wouldn't have produced alone?
- Did blind coding agree with the lexicon counts?
- What would I cut if I had a tenth of the budget?
