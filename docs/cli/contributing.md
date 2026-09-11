# For contributors

## Where things are

```
pipeline/layers.yaml          the graph — the only place it is written down
scripts/
  pipeline.py                 the runner: graph, state, run, approve, backfill
  corpus_facts.py             counts the corpus, so no page has to
  agents_report.py            what the agents did, for the site to render
  export_mira.py              …and the other layer commands that are plain scripts
extract/
  prompts/                    seven prompts, one per model-calling layer
  elife_extract/
    cli.py                    argument parsing and dispatch — one subcommand per layer
    layers.py                 the layer runners: read declared inputs, write declared outputs
    config.py                 the CLI-arg / env / default contract
    schema.py                 the pydantic wire format
    prepare.py  agents.py  reconcile.py  external_review.py  edges.py  write.py
    coverage.py  marks.py  verify_refs.py  evaluate.py
  tests/                      layer-contract tests, and the round-trip harness
runs/<paper>/                 what each layer produced, plus ledger.jsonl and approvals.jsonl
claims/<paper>/               the corpus
docs/                         this prose, and the methodology
site/                         the Astro site
```

The split that matters: `cli.py` parses and prints, `layers.py` does the reading and writing,
and the modules beside it do the work. A layer runner in `layers.py` is usually five lines —
read the declared inputs, call the module, write the declared output — and that is deliberate.
When a runner grows logic, the logic belongs in a module where it can be tested without an
argument parser.

## Reading order

If you are new to it, read in this order and each piece explains the next:

1. **`pipeline/layers.yaml`** — the header comment is the design in about sixty lines. What a
   layer is, the five kinds, and why approval is not one of them.
2. **`scripts/pipeline.py`** — `state()` is the whole staleness model in forty lines, and the
   comment above the `upstream` / `unrecorded` split is the subtlest decision in the system.
3. **`extract/elife_extract/layers.py`** — what a layer runner is obliged to do.
4. **One module** — `coverage.py` if you want the most interesting algorithm, `agents.py` if
   you want the model plumbing.

## The tests

`extract/tests/test_layer_contract.py` pins the contract between the CLI and the declaration.
No LLM and no network; it runs in under a second.

```bash
cd extract && pytest tests/ -q
python3 tests/test_layer_contract.py      # or standalone, no pytest
```

What it holds in place:

- Every `command:` in the declaration names a subcommand that exists. Nothing checks this at
  run time — `pipeline.py run` shells out to the string — so a renamed subcommand would
  otherwise surface as a layer that fails at the moment someone needs it.
- Each runner writes the path its layer declares. This is the invariant the whole ledger rests
  on, and it is exactly what the previous design got wrong.
- Every model-answered layer declares `by_from`, so the ledger records the model rather than
  the runner.
- `claim-tree` reads the edges `edge-inference` wrote instead of re-inferring them.
- The retired subcommands stay retired.

If you add a layer, the first two of those will fail until the declaration and the CLI agree,
which is the intent.

## Adding a layer

1. **Declare it** in `pipeline/layers.yaml`. `question:` is the field that matters — a layer
   whose question is a restatement of what it does is probably a step inside another layer
   rather than a layer. Give it `needs`, `reads`, `produces`, and a `command` if something can
   run it.
2. **Write the runner** in `layers.py`, and the subcommand in `cli.py`.
3. If a model answers it, have its output carry `model` at the top level and declare
   `by_from: model`.
4. `python3 scripts/pipeline.py graph` — an unknown dependency or a cycle fails here.
5. `pytest tests/` — the contract tests will tell you if the two halves disagree.

A layer with no runner is legitimate. `replication` has none: it asks whether an independent
study found the same thing, which this corpus has never asked, and it is declared so that the
gap is a column rather than an omission.

## Adding a prompt variant

See [the prompts](/elife-claim-trees/docs/prompts/). Briefly: a variant is a directory under
`extract/prompts/`, it may contain one file, and anything it omits falls back to the default —
so the diff is the experiment. Measure it with
[`evaluate`](/elife-claim-trees/docs/evaluate/) before keeping it.

## What is deliberately not abstracted

**The three readers are three layers.** They could be one function over a config table. Keeping
them apart is the point: none sees another's output, their agreement is the signal, and a table
that collapsed them would make it easy to accidentally share state between them.

**The runner shells out.** `pipeline.py run` executes the `command:` string rather than
importing and calling. That is what lets a layer be a Python module, a shell script, or nothing
at all, and it is why the layer graph is not tied to this CLI.

**Nothing caches a prompt across a run.** Prompts are read from disk when used, so the hash the
ledger records is the hash of the file that was actually sent.

## Conventions

Conventional commits. Prose in `docs/`, rendered by the site rather than duplicated into it —
if you write documentation as an Astro page you have created a second place for it to be wrong.
Figures in prose are `\{{token}}`s filled from `corpus-facts.json` at build, and an unknown token
fails the build, because a page that quietly shows its own placeholder is one nobody notices.
