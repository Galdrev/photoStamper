# Flash edition, English: follow-ups found by the Hebrew proofs

These are for the next merge into `page_flash_template.html`. They are not applied yet, because another agent is editing the template in a separate worktree.

## 1. "In short": name the source of the Zionism quote

- **Found by:** Hebrew proof 1 (#3). The weakness is in the English too.
- **Current English** (`p.fl-dinner`): "…now the article on Israel says, in Wikipedia’s voice, that Israel “began committing genocide,” Zionism is “a Jewish homeland through colonization,” and, in every copy we hold, the Israel and Hamas opening sections do not mention the hostages."
- **The problem:** "the article on Israel says … that" governs the whole list, so the Zionism quote reads as part of the Israel article. It comes from the Zionism article.
- **Proposed English** (exact):

  > Before the war, none of the most-read Wikipedia openings on the subject charged Israel with genocide; now the article on Israel says, in Wikipedia’s voice, that Israel “began committing genocide”; the Zionism article calls Zionism “a Jewish homeland through colonization”; and, in every copy we hold, the Israel and Hamas opening sections do not mention the hostages.

- **Checks:**
  - Both quotes are unchanged, so the English quote check still passes.
  - There are no new numbers.
- **Hebrew follow-up in the same merge:** the `template` pair whose English key is the old "In short" line must take the new English key. The Hebrew side already carries the fix: «…שישראל ״החלה לבצע רצח עם״; לפי הערך על הציונות, הציונות היא ״מולדת יהודית באמצעות קולוניזציה״; ובכל עותק…». If the key is not updated, the Hebrew build fails with "English text not found". It cannot fail silently.
