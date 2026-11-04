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

## Honest caveats (say these: they make you more credible)
- Counting words measures **emphasis, not truth**. "Genocide" can appear more because a court case exists.
- Editing patterns that look coordinated also come from **shared watchlists and breaking news**. They are signals, not proof.
- Some changes are **legitimate updates** to the scholarship. The study shows *that* and *how* framing moved. It does not rule on who is right.

## Findings (filled from real results only)
_Pending: written once the collection and the tests are complete._

## Lines that land
- "We didn't ask whether Wikipedia is biased. We asked whether the record moved, and we measured it."
- "A definition that changes once is an edit. One that changes, gets reverted and comes back three times is persistence. Whether that persistence is unusual is what the comparison articles tell you."
- "The most important chart is the one for articles about *other* countries."
