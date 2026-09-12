# juniper · paper · v1

The paper, composed.

Read INSTRUCTIONS.md and PERSONA.md if present, then everything under in/. Write claims.json as CONTRACT.json says. Refer only to what is listed there.

## Staged

- `in/juniper/question`  c846ad7fb877
- `in/juniper/hypotheses`  ce23e05e08bc
- `in/juniper/design`  48d7000b80b7
- `in/juniper/study`  f1ff24882072
- `in/personas/juniper.md`  b03af50c8a27

## Command

    python3 -m chain.agents.compose sections "Introduction=question,hypotheses;Methods=design;Results=study"

reads $CHAIN_IN, writes $CHAIN_OUT.
