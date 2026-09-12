# chain

A versioned processing graph with people in it, where every artifact is a claim set.
Design: `docs/design/2026-09-12-the-core.md`. Worked cycle: `examples/scientopia/board.html`.

**Five nouns.** A *subject* is what a process instance runs against (a project, a manuscript,
the corpus, the process itself). A *step* is a question asked of a subject, answered by code, a
model or a person. A *claim* is the atom of every answer. A *version* is one immutable
directory. A *run* is the record of one answer: inputs by hash, who, when.

**Five verbs.**

```bash
python3 -m chain ask     <subject> <step> [--again]          # stage the request; code answers itself; people and models wait
python3 -m chain answer  <subject> <step> <claims.json> --by WHO
python3 -m chain status  [subject] [--json]
python3 -m chain board   [--out board.html]
python3 -m chain export  <subject> <step> [--v N]           # JSON-LD with the standards mapping
```

**One rule.** A step reads `$CHAIN_IN` and writes `$CHAIN_OUT`. The request directory holds
`INSTRUCTIONS.md`, a copy of every input under `in/`, `CONTRACT.json`, `QUESTION.md`, and for a
judging step `skeleton.json`. An answer may refer only to what was staged.

**One schema.** `claims.json`: `claims` (id, type, text, by; `about` and `verdict` for
assessments and decisions), `edges` (from, to, rel), `sections` (compositions only). Types and
relations are listed in `claims.py` and mapped to standards in `standards.yaml`.

```
store/<subject>/<step>/request/     the open question
store/<subject>/<step>/v<N>/        claims.json · run.json · QUESTION.md · INSTRUCTIONS.md
store/<subject>/ledger.jsonl
```

```bash
python3 -m pytest chain/tests -q                      # 7 tests, runs the whole demo cycle
python3 -m chain.examples.scientopia.demo             # regenerate examples/scientopia/{store,board.html}
python3 -m chain --root chain/examples/scientopia status
```

`agents/stub.py` is the smallest black box that answers a request (from fixtures);
`agents/compose.py` composes a document from staged claims. Replace the stub with a real agent
and nothing else changes.
