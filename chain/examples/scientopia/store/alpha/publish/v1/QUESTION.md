# alpha · publish · v1

The published record: the article, its reviews, and the decision.

Answered by: code. Read INSTRUCTIONS.md, then everything under in/. Write claims.json as CONTRACT.json says. Refer only to what is listed there.

## Staged

- `in/alpha/paper`  c0418142b0a7
- `in/alpha/peer-review`  900b3d942849
- `in/alpha/editorial`  1eecaf95a483

## Command

    python3 -m chain.agents.compose "Article=paper;Reviews=peer-review;Decision=editorial"

reads $CHAIN_IN, writes $CHAIN_OUT.
