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

## Findings (verified against the data and by an adversarial review)
- **The headline:** "We wrote the test down before looking. By our own rule, the answer was *not supported*: the 'colonial / apartheid / genocide' vocabulary did not grow more in these articles than in articles about other countries and conflicts."
- **But not nothing:** "In a sample 20 times bigger, about 10,000 articles, there is a small, real rise. It appears only *after* October 7, sits mostly in articles tagged Palestine and Israel, and is about the same size as in articles on other wars: Armenia, Russia, Ukraine. Articles about Judaism barely moved."
- **The scale:** "One extra such word per 20,000 words. Real, measurable, small."
- **The definition moment:** "The opening sentence of 'Zionism' went through 169 different versions since 2021. It moved from 'a movement among the Jewish people… re-establishment of a Jewish state' to 'an ethnic nationalist movement… through colonization'. That word entered in spring 2024, months earlier than the press reported."
- **Edit wars, not a ratchet:** "Our hypothesis was 'push, get reverted, push again, until it sticks'. The data says loaded words are pushed and pulled more often here, but they don't stick *more* than elsewhere."
- **Co-editing:** "The same pairs of editors repeatedly edit right after each other about twice as often per edit on these articles. That's a signal worth watching, not proof of a campaign: shared watchlists during a war look exactly the same."
- **Languages:** "On 16 key articles, English openings picked up these words more often than German, French, Hebrew, Arabic and the others. Across 500 articles per language, English looks like everyone else. Scale changes the answer, and that's worth saying."
- **What the words did:** "When an opening paragraph shifted, the typical move was turning 'X is accused of…' into 'X did…'. 'Israeli apartheid' went from a contested analogy to stated fact. It happened in both directions, and in other topics too."
- **The honest limit:** "Word counts can't tell you who a word is aimed at, or whether it's true. 'Not supported' means 'not shown', not 'nothing happened'."

## Lines that land
- "We didn't ask whether Wikipedia is biased. We asked whether the record moved, and we measured it."
- "A definition that changes once is an edit. One that changes, gets reverted and comes back three times is persistence. Whether that persistence is unusual is what the comparison articles tell you."
- "The most important chart is the one for articles about *other* countries."
