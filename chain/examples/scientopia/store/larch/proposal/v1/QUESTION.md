# larch · proposal · v1

The proposal, composed.

Read INSTRUCTIONS.md and PERSONA.md if present, then everything under in/. Write claims.json as CONTRACT.json says. Refer only to what is listed there.

## Staged

- `in/larch/question`  8e7c60f19c2b
- `in/larch/hypotheses`  ef167e3404e5
- `in/larch/design`  3c975c9dfd08
- `in/personas/larch.md`  0fdf02606c41

## Command

    python3 -m chain.agents.compose sections "Question=question;Hypotheses and predictions=hypotheses;Design=design"

reads $CHAIN_IN, writes $CHAIN_OUT.
