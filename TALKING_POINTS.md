# Talking points: Wikipedia Framing Drift

Short, memorable lines for presenting this project. Findings points are filled in only from real results.

## The one-liner
"We checked how Wikipedia's articles on Israel, Jews and Zionism changed between 2021 and 2026: every edit, every quarter, thousands of articles, in eleven languages. And we checked them against articles on other countries and conflicts, so we could tell a real pattern from Wikipedia just being Wikipedia."

## Why it matters (the frame)
- **Wikipedia is not social media. It is the record.** Search engines quote it, students cite it, and AI models are trained on it. A change to a Wikipedia definition becomes what millions of people, and machines, treat as fact.
- **The question is not "is Wikipedia biased?".** That is a shouting match. The question is measurable: *did the wording move, how did it move, and was it organic or organised?*
- **Three layers:**
  1. **Content:** what the record says.
  2. **Process:** how it got there.
  3. **Epistemics:** whether it was sourced and guarded like a record should be.

## Process stories (true, and good on stage)
- **"Wikipedia was blocked, so we borrowed GitHub."** The AI's cloud sandbox couldn't reach Wikipedia. It ran the data collection as a job on GitHub's servers instead, free, inside my own repo.
- **"We wrote the rules before we saw the data."** The hypothesis, the tests and the decision rule for the headline were committed to git *before* any real data arrived. The timestamp proves it. That is how you stop yourself finding what you hoped to find.
- **"The AI hired a critic for itself."** An independent AI reviewer read the code cold. It found five bugs that would each have corrupted the result. One of them: a redirect page counted as an article showed up as 2,500 "colonial" words per 10,000.
- **"The press got the date wrong. The data didn't."** Coverage said Zionism's definition gained the word "colonization" between July and October 2024. The revision history shows it was already there by July 1st. We kept the original test as a fail rather than quietly moving the goalposts.
- **"Every number is checkable."** Every snapshot's text is checked against Wikipedia's own digital fingerprint for that exact revision. In the sample: 137 out of 137 matched.
- **"Counting wasn't enough; it nearly fooled us."** The large-scale sample had 3,253 vs 4,000 articles, so it passed the size check. But "topic" turned out to mean only Judaism articles, and "comparison" was mostly Russia. Lesson: check what is in the groups, not just how many.
- **"Blind reading."** AI coders read the before/after paragraphs with all names masked ([ENTITY-1]), in random order, not knowing which was newer. They judged the framing without knowing the topic.
- **"The ratchet test."** Our hypothesis: a change is pushed, undone, pushed again, and finally slips through. We measured it by downloading the opening paragraph of *every single revision* since 2021 and timing how long each insertion and each removal survived.
- **"Same rules, different people."** The same articles in German, French, Hebrew, Arabic and seven more languages run on the same software, rules and process, but with different editing communities. If English moved and they didn't, the change lives in the community, not in the facts.
- **"Nobody was named."** Editors appear only as anonymous codes, made with a random key that was thrown away. We measure patterns, never people.

- **"You can't blind an AI to Wikipedia."** We hid every name in the paragraphs and asked a separate AI to guess the article. It named the exact article 25 times out of 30. AI has already read Wikipedia, so our "blind" coders were only masked, and we say so.

## Honest caveats (say these: they make you more credible)
- Counting words measures **emphasis, not truth**. "Genocide" can appear more because a court case exists.
- Editing patterns that look coordinated also come from **shared watchlists and breaking news**. They are signals, not proof.
- Some changes are **legitimate updates** to the scholarship. The study shows *that* and *how* framing moved. It does not rule on who is right.

## Findings (verified against the data and by an adversarial review; numbers as in wikitrends/patterns/SYNTHESIS.md)
- **The headline:** "The core, most-read Israel articles shifted. The long tail did not. Across the full population of 49,000 articles, the average change was no larger than in articles on other conflicts."
- **The core:** "We drew a random sample from every article Wikipedia's Israel, Palestine, Judaism and Jewish history projects assess, 48,974 of them, and from 141,356 articles on other conflict regions: Ukraine, Armenia, Azerbaijan, Kosovo and others. Among the articles the projects rate Top importance, 10.3% gained critical vocabulary in their opening paragraph since July 2023. In the other conflicts' Top articles: 4.4%. At Mid importance: 1.5% against none."
- **The long tail:** "The Low-importance and ungraded pages, about 80% of the topic, moved exactly like other conflicts' pages. Across all 49,000 articles the gap is 0.4 points, within the margin of error. Still, that is about 446 articles whose opening paragraph gained these terms."
- **Not Wikipedia-wide:** "We also checked 2,466 random Wikipedia articles. No drift at all: virtually none gained these terms. Contested subjects moved; the encyclopedia at large did not."
- **What we wrote down first:** "We wrote the test down before looking. By our own rule, the answer was *not supported*: on average, the vocabulary did not grow more in these articles than in comparison articles. The full-population sample now says the same about the average. The change is in the core."
- **The sealed half, precisely:** "On our first crawl of Top, High and Mid articles, the half we sealed until the end replicated the gap: +3.6 points. That holds for those articles. It is not a claim about all 49,000."
- **Readers:** "In the core crawl, the 3.9% of articles that gained carry 15% of reading (comparison 1.5% and 5%). Across the whole population the share of reading on changed pages is the same as for other conflicts, 4.8% against 4.6%. 83% of core topic reading still lands on opening paragraphs that didn't change."
- **One wave, now over:** "New critical terms per 1,000 topic edits: about 7 before the war, about 16 through 2024, back to 5 or 6 in 2026. This was a time-limited reframing, not a continuing slide."
- **Where it went:** "The change sits in Israel and Palestine pages, in leads and first sentences, in a few hundred core articles. Israel and Palestine articles gained at 1.2%, Judaism at 0.3%. Articles on Judaism moved no more than other conflicts' articles (−0.2 points). At equal editing activity, topic articles gained 2 to 4 times as often as the pooled comparison; against other live conflicts the gap is smaller (Palestine 57%, Israel 44%, Ukraine 30%, Armenia 30% in the busiest fifth)."
- **The definition moment:** "Zionism's opening sentence moved from 'a movement among the Jewish people… re-establishment of a Jewish state' to 'an ethnic nationalist movement… through colonization'. 'Colonization' first entered on 5 June 2024 and was undone. It went in and out 44 times, and the wording locked in only on 27 August 2026. That's a tug-of-war over one word."
- **Edit wars on a few pages, not a ratchet for the topic:** "On the key battleground leads, added terms survive less well (36% vs 56% at 30 days) and need more tries. Across all 4,642 topic articles that gap disappears: 47.3% vs 42.9%. The famous fights are a few pages; most change landed on quiet pages nobody reverted."
- **Organised or organic?** "Off-wiki canvassing is documented by Wikipedia's arbitration committee on both sides. In our data, 14 pairs of accounts kept returning to the same articles beyond chance, where chance gives about 2. They form two small blocs of four long-standing accounts each: one that adds and removes, one found when we test insertions alone (114 insertions across 53 articles). None edited in step, no wording was pasted across articles, and no bloc of removers showed up. On comparison pages: 3 pairs against 0.28 by chance, no bloc."
- **Timing, said carefully:** "One bloc made 41% of its edits in the window of the pro-Israel email canvassing ArbCom found, against 18% for random accounts. That's low confidence: it fails our strict test, and the window is also the war's first months. In the Discord window: 21% against 23%. Being active in a window doesn't make a group part of it."
- **Languages:** "English and Portuguese leads moved (+0.24 and +0.27 per 1,000 words). The other nine languages did not detectably. So it's not 'Wikipedia everywhere'."
- **What the words did:** "Most new labels came in attributed: 'X states that…'. In a few flagship leads, Gaza genocide, Israel, Israeli apartheid, Nakba, Zionism, the attribution was later removed and the label now stands in Wikipedia's own voice. Wikipedia as a whole did not move into its own voice."
- **The honest limit:** "Word counts can't tell you who a word is aimed at, or whether it's true. 'Not supported' means 'not shown', not 'nothing happened'."

### New: when, why and how it spread
- **Battles, not courts:** "In the three weeks after a military escalation, topic editing rose 17%. After ICJ orders, ICC warrants, UN votes and rights reports, it was 0.94 times normal, and those legal events show no effect on new terms at full scale. Don't write 'after the ICJ ruling, Wikipedia changed.' The war brings the editors; the courts don't."
- **News or narrative?** "Strip out every lead sentence about recent events, and 89% of the extra change is still there. The war didn't mainly produce war coverage. It sent editors back to retell 1897 to 1948 and to rename the land, and they did it by adding sentences: leads that gained terms grew in 78.2% of cases."
- **Experienced hands, formal process:** "Only 9.1% of war-window edits on topic pages came from accounts with under 500 edits, against 17.2% on comparison pages. Protection went from 11% to 31% of topic pages; requests for comment nearly tripled, on a few pages: Gaza genocide alone had 21. This wasn't a flood of newcomers. It was regulars, settling things formally."
- **The structure moved too:** "Framing categories were added to 7.2% of topic articles vs 2.2% of comparison articles. And links come first: articles already linking to a core concept like the Nakba picked up its vocabulary 5.6 points more often at the same editing level. New links are an early warning signal."

### What we checked and dropped (say this; it builds trust)
- "We withdrew our own result on how 1948 departures are described, 'forced out vs fled'. The measure scored 53% on a hand-checked precision test, under our 60% bar. Two other measures failed too."
- "A pilot said blocked accounts made more of the loaded-word edits. At full scale they didn't: 13.7% of insertions against a 12.3% base rate on the same pages."
- "The 'four pages hold most of the fighting' line is true inside the 25 key articles, not across the topic (9%). The 'words stick here' line holds only on the battlegrounds."

## Lines that land
- "We didn't ask whether Wikipedia is biased. We asked whether the record moved, and we measured it."
- "A definition that changes once is an edit. One that changes, gets reverted and comes back three times is persistence. Whether that persistence is unusual is what the comparison articles tell you."
- "The most important chart is the one for articles about *other* countries."
