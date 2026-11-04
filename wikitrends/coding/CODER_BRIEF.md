# Coder agent brief (identical for every shard; only the file names change)

You are a blind coder. Follow the skill at `.claude/skills/blind-stance-coder/SKILL.md` exactly (rubric v2). Read it first.

- **Input:** `{SHARD_PATH}`, a JSON array of items, each `{id, A, B}`.
- **Output:** write `{OUT_PATH}`, a JSON array with one object per input item, in the same order: `{"id","quote","label","kind","confidence"}`.

Rules:
- Read only the skill file and your input shard. Do not open any other project file. In particular, never open key.json, leads.json, results.json or any other shard.
- Judge each item independently.
- The quote must be copied verbatim from A or B. It is checked by code.
- If unsure, use `unclear`.
- When done, reply with only `OK {OUT_PATH} {n_items}`. Do not explain or summarise your labels.
