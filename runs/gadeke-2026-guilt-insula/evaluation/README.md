The `pairs.py` script in this directory has been retired. Its `score` subcommand is now:

```
cd extract && python3 -m elife_extract.cli score \
  --reference ../claim-tree.v1 \
  --candidate ../../../claims/gadeke-2026-guilt-insula \
  --pairs match.v3.pairs.json
```

Accepts both `[{committed, rerun, note}]` (this directory's format) and the
matcher's own `{matches: [...]}` format. Reports recovery, precision, panel,
role, edge recovery, and role confusion.

## The model sweep's scorecards (#85)

`evaluate score --out <profile>.scorecard.json --profile <name>` writes a scorecard here in
the scorer's own format; the corpus-scope `evaluation` layer
(`scripts/evaluation_report.py --write`) gathers every `*.scorecard.json` under
`runs/<paper>/evaluation/` into `review/evaluation.json`, which the site renders at
`/pipeline/evaluation/` and on the claim-tree cell. Rows here, all scored against
`claim-tree.v1` (the committed tree; no version is approved yet):

- **`subagent.scorecard.json`** — the three-reader chain, subagent-answered, as the current
  committed tree (`claims/gadeke-2026-guilt-insula`, aligned by `match.v3.pairs.json`).
- **`fourth-reading.{answer,output,pairs,scorecard}.json`, `fourth-reading.tree/`** — the
  experiment the design note left open: one whole-paper reading in a single pass. The prompt
  gave one reader the whole prepared paper (abstract, introduction, results, discussion,
  captions, tables, methods, the panel inventory and span ids) and asked for every claim; the
  answer was validated through `reader_from_raw`, built into a tree, and scored with a
  matcher alignment produced by hand.
- **`{frontier,standard}-tasks.*`** — scaffolding versus model, as far as the subagent path
  allows: the frontier lean reader task and the standard reader task, both answered by the
  same subagent on the results slice, scored side by side.

The paid profiles (`frontier`, `standard`, `open` through real model calls) have no scorecard
and appear in `review/evaluation.json` as `not run: no backend credit`.
