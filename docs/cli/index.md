# Docs

This is the reference for the two command-line tools that produce this corpus. It documents
what you type. What the resulting graph then knows — what a layer is, why staleness is
computed rather than remembered, what an approval attaches to — is on
[the pipeline pages](/elife-claim-trees/pipeline/), where every figure is generated from the
corpus rather than written down.

The division is not editorial. These pages describe commands, which change when the code
changes; those pages describe a model, which changes when a decision changes. Keeping them
apart is what stopped this section describing a system that no longer existed.

## The two tools

**`scripts/pipeline.py`** is the pipeline. It reads `pipeline/layers.yaml`, works out what the
layer you asked for still needs, runs each one, and appends a record to
`runs/<paper>/ledger.jsonl` naming every input by path and content hash. It is the only thing
that writes a ledger, which is what makes "is this result still current" a question about
files rather than about anyone's memory.

**`elife-extract`** is a set of layer runners — one subcommand per node in the graph that a
model or a script can execute. Each reads the paths its layer declares and writes the path its
layer declares. You can run them directly; nothing then records that you did.

That asymmetry is the whole reason to prefer the first. There is no second path that produces
the corpus.

```bash
python3 scripts/pipeline.py run gadeke-2026-guilt-insula claim-tree --dry-run
```
```
prepare          cd extract && python3 -m elife_extract.cli prepare --paper gadeke-2026-guilt-insula …
results-reader   cd extract && python3 -m elife_extract.cli results-reader --paper gadeke-2026-guilt-insula
caption-reader   …
structure-reader …
reconcile        …
external-review  …
edge-inference   …
claim-tree       …
```

Eight commands, in dependency order, none of them run. Every one of them is a layer with a
page of its own.

## Where to start

- **[Install and configure](/elife-claim-trees/docs/install/)** — Python, credentials, the
  environment-variable contract.
- **[One paper end to end](/elife-claim-trees/docs/first-paper/)** — the walkthrough, from a
  DOI to a claim tree with a coverage report.
- **[The runner](/elife-claim-trees/docs/runner/)** — `pipeline.py`: `graph`, `backfill`,
  `state`, `run`, `approve`.
- **[The layer runners](/elife-claim-trees/docs/layers/)** — `elife-extract`, one subcommand
  per layer.
- **[Batch operation](/elife-claim-trees/docs/batch/)** — running the corpus, and what it
  costs.
- **[Measuring a prompt change](/elife-claim-trees/docs/evaluate/)** — `evaluate`, the one
  subcommand that is not a layer.
- **[Configuration](/elife-claim-trees/docs/config/)** and
  **[the prompts](/elife-claim-trees/docs/prompts/)** — the reference tables.
- **[For contributors](/elife-claim-trees/docs/contributing/)** — code structure, adding a
  prompt variant, what the tests pin.

## Coming from the old CLI

The command surface changed. If you have older notes or scripts:

| If you used | Use now |
|:------------|:--------|
| `elife-extract extract --doi <doi>` | `pipeline.py run <paper> claim-tree`, or `prepare` then each reader |
| `elife-extract run` | `pipeline.py run <paper> claim-tree` |
| `write --draft out/draft-<slug>.json` | `write --paper <slug>` |
| `write --review-mode external` | the `external-review` layer, which runs in the chain |
| `write --review-mode interactive` | `pipeline.py approve <paper> <layer> --by NAME`, after the write |
| `write --review-mode auto-approve` | nothing — there is no gate to bypass |
| `coverage --doi <doi> --claims-dir <dir>` | `coverage --paper <slug>` |
| `mark --doi <doi> …` | `mark --paper <slug>` |
| `scripts/verify-references.py` | `pipeline.py run <paper> reference-check` |

## Elsewhere on this site

| | |
|:--|:--|
| [Papers](/elife-claim-trees/papers/) | the claim graphs themselves |
| [Pipeline](/elife-claim-trees/pipeline/) | the layer graph, and which papers have been through each layer |
| [Roles and relations](/elife-claim-trees/pipeline/vocabulary/) | what a claim can be, and what can hold between two |
| [Methodology](/elife-claim-trees/method/) | the procedure the corpus follows |
| [Design note](/elife-claim-trees/design/2026-09-11-layers-as-pipeline.html) | why the system is shaped this way |
