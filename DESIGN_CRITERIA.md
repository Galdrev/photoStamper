# Design criteria (shared by builder and creative director)

The creative director scores every iteration 1 to 5 on each criterion, with one sentence of evidence each. A score below 3 on any criterion blocks shipping.

1. **Clarity in 5 seconds.** A smart non-specialist can say what a view shows within 5 seconds of seeing it.
2. **Touch over type.** Interaction happens on the data itself: tap a bar, drag a window, scrub time. A typed input or dropdown needs a reason.
3. **Data fidelity.** Every mark is drawn to scale from the real data. Axes are honest (bars start at zero). The war marker is at the correct position. The n and the uncertainty band are visible wherever a comparison is shown.
4. **Honest play.** Playing cannot easily mislead. Small slices are flagged (n < 30). Exploratory results are labelled. Chance is shown (shuffle or band).
5. **Delight.** At least one moment per view makes someone say "oh!" through motion, reveal or surprise. It must come from the data itself, not decoration.
6. **Coherence.** The report and the lab share one visual language, and a finding in the report can be opened in the lab.
7. **Phone.** Works at 400px with a thumb. No horizontal page scroll.
8. **Restraint.** Nothing is there just because it was possible. Each element earns its place.

## Process
- Orchestrator (main session): picks concepts, briefs the builder, decides.
- Concept agents: generate options. Their personas differ on purpose.
- Builder: implements, screenshots, self-checks against these criteria.
- Creative director: judges screenshots and the running page against these criteria. Proposes the boldest improvement. Says "ship" or "iterate".
- Data validator: recomputes the numbers shown and compares them with the rendered page.
