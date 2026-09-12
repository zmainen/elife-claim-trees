# chain

The referee for a game of players who interact only through artifacts, where every artifact
is a claim set. Design: `docs/design/2026-09-12-the-core.md`. The game: `docs/scientopia/`.
Worked round: `examples/scientopia/board.html`.

**Five nouns.** A *player* is what a process runs against (a team, a funder, a journal, the
library, the process itself): a persona file plus whatever answers its requests — a person, a
model, a group. A *step* is a question asked of a player; a step with a command is run by the
referee, any other waits for its player. A *claim* is the atom of every answer. A *version* is
one immutable directory. A *run* is the record of one answer: inputs by hash, who, when.

**Five verbs.**

```bash
python3 -m chain ask     <player> <step> [--again]           # stage the request; commands run at once; players wait
python3 -m chain answer  <player> <step> <claims.json> --by WHO
python3 -m chain status  [player] [--json]
python3 -m chain board   [--out board.html]
python3 -m chain export  <player> <step> [--v N]            # JSON-LD with the standards mapping
```

**One rule.** A step reads `$CHAIN_IN` and writes `$CHAIN_OUT`. The request directory holds
`INSTRUCTIONS.md`, `PERSONA.md`, a copy of every input under `in/`, `CONTRACT.json`,
`QUESTION.md`, and for a judging step `skeleton.json`. An answer may refer only to what was
staged.

**Inputs.** `step` (same player), `player:step`, `type:*:step` (every player of a type's latest;
goes stale when the field changes, never blocks, never orders the graph — this is how the loop
closes), or a path.

**One schema.** `claims.json`: `claims` (id, type, text, by; `about` and `verdict` for
assessments and decisions), `edges` (from, to, rel), `sections` (compositions only). Types and
relations are listed in `claims.py` and mapped to standards in `standards.yaml`.

```
store/<player>/<step>/request/     the open question
store/<player>/<step>/v<N>/        claims.json · run.json · QUESTION.md · INSTRUCTIONS.md · PERSONA.md
store/<player>/ledger.jsonl
```

```bash
python3 -m pytest chain/tests -q                      # runs the whole demo round
python3 -m chain.examples.scientopia.demo             # regenerate examples/scientopia/{store,board.html}
python3 -m chain --root chain/examples/scientopia status
```

`agents/stub.py` is the smallest black box that answers a request (from fixtures);
`agents/compose.py` composes documents from staged claims; `agents/seed.py` imports a corpus
into the library. Replace the stub with a real player and nothing else changes.
