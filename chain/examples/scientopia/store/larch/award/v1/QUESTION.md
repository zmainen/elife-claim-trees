# larch · award · v1

What did the funders decide about this team's proposal?

Read INSTRUCTIONS.md and PERSONA.md if present, then everything under in/. Write claims.json as CONTRACT.json says. Refer only to what is listed there.

## Staged

- `in/aurora/select`  0aaa15ad3f7b
- `in/personas/larch.md`  0fdf02606c41

## Command

    python3 -m chain.agents.compose about-me "Decisions=funder:*:select"

reads $CHAIN_IN, writes $CHAIN_OUT.
