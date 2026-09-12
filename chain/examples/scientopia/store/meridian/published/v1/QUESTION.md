# meridian · published · v1

The published record: each accepted article with its reviews and decision.

Read INSTRUCTIONS.md and PERSONA.md if present, then everything under in/. Write claims.json as CONTRACT.json says. Refer only to what is listed there.

## Staged

- `in/meridian/decision`  d255d945a86a
- `in/meridian/review`  a17fc296ebee
- `in/meridian/submissions`  4554b6b33f28
- `in/juniper/paper`  5308b445293a
- `in/larch/paper`  e06410c98c42
- `in/personas/meridian.md`  3094b1f597f3

## Command

    python3 -m chain.agents.compose accepted decision review submissions

reads $CHAIN_IN, writes $CHAIN_OUT.
