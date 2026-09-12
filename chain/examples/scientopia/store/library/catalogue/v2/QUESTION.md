# library · catalogue · v2

What is there to read — imported work and every journal's publications?

Read INSTRUCTIONS.md and PERSONA.md if present, then everything under in/. Write claims.json as CONTRACT.json says. Refer only to what is listed there.

## Staged

- `in/library/import`  4454832f9f0d
- `in/meridian/published`  f2c43be172f9

## Command

    python3 -m chain.agents.compose sections "Seed corpus=import;Published=journal:*:published"

reads $CHAIN_IN, writes $CHAIN_OUT.
