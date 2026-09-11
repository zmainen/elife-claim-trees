# elife-extract

Layer runners for the claim-trees pipeline. Three-agent extraction (Results, Caption and
Structure readers on partitioned slices), Opus reconciliation, an Opus review pass, claim file
writing per the elife-claim-trees § 4 schema, CrossRef DOI verification, coverage measurement,
and round-trip evaluation against a curated reference corpus.

**This is not the pipeline.** The pipeline is `pipeline/layers.yaml` plus
`scripts/pipeline.py`, which walks the graph, runs what a layer still needs, and records every
run in `runs/<paper>/ledger.jsonl` with the content hash of what it read. Each subcommand here
is one layer's runner: it reads the paths its layer declares and writes the path its layer
declares, and nothing more. Call them directly and nothing records that you did — which is why
`extract` and `run`, the two subcommands that chained several layers together and wrote to a
directory no layer declares, are gone.

**Status: working.** Verified end-to-end on Headley 2026 with 100% claim recovery against the
curated reference and 96% role agreement with `external-review` in the chain. See
`tests/headley-roundtrip-v3-external.md` for the per-claim scorecard.

**Methodology authority:** `~/Projects/mainenlab/elife-claim-trees/docs/method.md` § 3 (Claim induction — the ten-step process), § 4 (Schema). The CLI implements that methodology; when a behavior decision isn't anticipated by the doc, the CLI's behavior is the decision and the doc is updated in the same commit.

## Install

```bash
cd home/collabs/elife/claim-trees/extract
pip install -e .
```

Requires Python 3.10+, the Anthropic SDK with Vertex backend (`anthropic[vertex]`), pdfplumber, httpx, pyyaml, pydantic. All installed automatically.

You also need Vertex AI credentials. The CLI defaults to `cr-mainen` / `europe-west1` (HaaK's Vertex project); override with `--vertex-project` / `--vertex-region` or env vars.

## Configure

The CLI reads from CLI args first, then environment variables, then defaults.

| Variable | CLI flag | Required? | Purpose |
|:---------|:---------|:----------|:--------|
| `ELIFE_CLAIM_TREES_ROOT` | `--root` | no | The corpus repository — what `pipeline/layers.yaml` resolves its paths against. Defaults to the directory this package ships in |
| `ELIFE_CORPUS_DIR` | `--corpus-dir` | no | Where claim files are read/written (default: `<root>/claims`) |
| `VERTEX_PROJECT_ID` | `--vertex-project` | uses default | GCP project for Vertex AI Claude (default: `cr-mainen`) |
| `VERTEX_REGION` | `--vertex-region` | uses default | Vertex region (default: `europe-west1`) |
| `GOOGLE_APPLICATION_CREDENTIALS` | n/a | yes | Service account JSON for Vertex auth |
| `ELIFE_EXTRACT_MODEL_RESULTS` | `--model-results` | optional | Override Results-reader model |
| `ELIFE_EXTRACT_MODEL_CAPTION` | `--model-caption` | optional | Override Caption-reader model |
| `ELIFE_EXTRACT_MODEL_STRUCTURE` | `--model-structure` | optional | Override Structure-reader model |
| `ELIFE_EXTRACT_MODEL_RECONCILE` | `--model-reconcile` | optional | Override reconciliation + reviewer model |
| `ELIFE_EXTRACT_OUTPUT` | `--output-dir` | optional | Where draft tables and intermediates are written |

Default model routing (cost-balanced, validated empirically):

- Three extraction agents: **claude-sonnet-4-6**
- Reconciliation + external review: **claude-opus-4-6**

## Subcommands

One per runnable layer, named for the layer it runs. To run a layer *and whatever it still
needs*, and to have the run recorded, go through the runner instead:

```bash
python3 scripts/pipeline.py run <paper> <layer>            # run it
python3 scripts/pipeline.py run <paper> <layer> --dry-run  # print the chain, run nothing
python3 scripts/pipeline.py state                          # where every paper stands
python3 scripts/pipeline.py approve <paper> <layer> --by NAME
```

| Subcommand | Layer | Produces |
|:-----------|:------|:---------|
| `prepare` | `prepare` | `runs/<paper>/prepared.json` |
| `results-reader` | `results-reader` | `runs/<paper>/results-reader.output.json` |
| `caption-reader` | `caption-reader` | `runs/<paper>/caption-reader.output.json` |
| `structure-reader` | `structure-reader` | `runs/<paper>/structure-reader.output.json` |
| `reconcile` | `reconcile` | `runs/<paper>/reconciler.output.json` |
| `external-review` | `external-review` | `runs/<paper>/external-review.output.json` |
| `edge-inference` | `edge-inference` | `runs/<paper>/edge-inference.output.json` |
| `write` | `claim-tree` | `claims/<paper>/*.md` |
| `verify-refs` | `reference-check` | `runs/<paper>/reference-check.output.json` |
| `coverage` | `coverage` | `coverage/<paper>.json` |
| `mark` | `marks` | `marked/<paper>.marked.md` |
| `evaluate` | — not a layer | scorecards under `--work-dir` |

Every subcommand takes `--paper <slug>` and finds its inputs from there. The DOI comes from
`claims/<paper>/index.md`; a paper not yet in the corpus has no index, so `prepare` takes an
explicit `--doi` the first time.

### `prepare` — the paper the readers read

```bash
elife-extract prepare --paper gadeke-2026-guilt-insula
```

Fetches the paper from the eLife CDN (cached at `~/.cache/elife-extract/`), slices it into
abstract / results / captions / methods, and writes the result where the readers will find it.

A layer of its own because otherwise a reader's only declared input is its prompt: the ledger
would record which prompt read a paper without recording which paper, and eLife papers get
revised.

### the three readers

```bash
elife-extract results-reader   --paper gadeke-2026-guilt-insula
elife-extract caption-reader   --paper gadeke-2026-guilt-insula
elife-extract structure-reader --paper gadeke-2026-guilt-insula
```

Each reads its own slice under its own prompt. None sees another's output — they are
independent witnesses, and their agreement is the signal, which is why they are three layers
rather than one.

### `reconcile` — which candidates survive

```bash
elife-extract reconcile --paper gadeke-2026-guilt-insula
```

Reads the three readers' outputs from disk and aligns them into one draft claim table, tagged
`high` / `contested` / `single-source` and carrying which readers surfaced each claim.

### `external-review` — what the readers systematically miss

```bash
elife-extract external-review --paper gadeke-2026-guilt-insula
```

One Opus pass over the reconciled draft, recovering the `prediction` and `hypothesis` roles and
the multi-panel claims prose-level extraction under-covers. ~$2 and ~3 minutes per paper; lifts
role agreement from ~65% to ~96% on the Headley round-trip.

This was `--review-mode external`. It is a step, not review: it changes the artifact, and it
runs before the version it would have approved exists. Declared as a layer, editing
`prompts/external-reviewer.md` makes every claim tree built on it stale.

`claim-tree` builds on this layer's output where it has run and on the reconciled draft where
it has not, so a paper without it is the ordinary case rather than a failure.

### `edge-inference` — which claims depend on which

```bash
elife-extract edge-inference --paper gadeke-2026-guilt-insula
elife-extract edge-inference --paper <slug> --dump-prompt /tmp/edges.txt
elife-extract edge-inference --paper <slug> --edges-json /tmp/answer.json
```

`--dump-prompt` writes the exact request and exits, so an analyst or a reasoning agent answers
the same question the layer would have asked rather than a paraphrase written from memory.
`--edges-json` records that answer, through the same validation an inferred one gets — edges
naming an unknown slug, or pointing at themselves, are dropped either way.

### `write` — the claim tree

```bash
elife-extract write --paper gadeke-2026-guilt-insula
```

Assigns slugs and UUIDs, attaches the edges `edge-inference` produced, and writes one file per
claim into `<corpus-dir>/<paper>/`. It reads those edges rather than inferring them again,
which it used to do — a second paid Opus call for an answer already on disk.

Refuses to overwrite a non-empty paper directory; move or delete it to re-run.

### `verify-refs` — CrossRef DOI resolution

```bash
elife-extract verify-refs --paper <slug>
elife-extract verify-refs --paper <slug> --dry-run   # resolve, write nothing
```

Confirms the paper's own DOI from its `index.md`, then for each `role: literature-context`
claim takes one of two paths:

- **confirm**: the claim already has a top-level `doi:` (per the schema); CrossRef confirms it
  resolves to a real paper — the anti-hallucination check
- **found**: no DOI yet; extracts Author (Year) hints from the claim text and slug, queries
  CrossRef, and writes the highest-scoring match (score > 15) back to top-level `doi:`

The verdicts are kept as the layer's output rather than printed and lost. Omit `--paper` to
sweep the corpus, which writes no report — a version belongs to one paper.

### `coverage` and `mark`

```bash
elife-extract coverage --paper <slug> --json ../coverage/<slug>.json
elife-extract mark     --paper <slug> --mapping ../mappings/<slug>.json -o ../marked/<slug>.marked.md
```

No model calls, so both are free and fast enough to run over the whole corpus; `coverage
--fail-on-orphans` makes it a gate. `coverage` takes its denominator from the paper rather than
from the claim set, which is what lets it see what both the tree and any comparison missed.

### `evaluate` — round-trip scoring against a reference corpus

```bash
elife-extract evaluate \
  --reference-dir ~/Projects/mainenlab/elife-claim-trees/claims \
  --work-dir /tmp/elife-eval \
  --paper headley-2026-inhibitory-rhythms

elife-extract evaluate \
  --reference-dir ... \
  --work-dir ... \
  --all              # all paper-dirs under reference
elife-extract evaluate \
  --reference-dir ... \
  --work-dir ... \
  --papers slug1,slug2,slug3
```

For each named paper:

1. Reads the reference paper's `index.md` to get the DOI
2. Runs the chain into that temp tree — prepare, the three readers, reconcile, optional
   external review, write
3. Calls Opus matcher to align CLI claims with reference claims
4. Saves per-paper scorecard at `<work-dir>/<paper-slug>/scorecard.json`

After all papers, renders an aggregate scorecard at `<work-dir>/aggregate-scorecard.md` with mean / median per-paper metrics and a comparison table. `--skip-existing` reuses prior scorecards (resumable sweeps).

Use `evaluate` to validate a prompt iteration or a model change before keeping it — same
scorecard format as the manual round-trip in `tests/headley_roundtrip.py`. `--no-external-review`
scores the chain without the Opus pass.

It is the one subcommand that is not a layer, and deliberately so: it re-runs the chain into a
temp tree and scores the result against the committed claim files, so its subject is the prompt
set rather than any paper, and it produces nothing another layer consumes. That also makes it
the last caller of the run-the-whole-chain-in-one-process path, which the layer runners
otherwise replaced.

## Prompts

A prompt is two things. The **task** is a page per role, written by hand, saying what that
role reads and what to look for. The **contract** is what every role shares — the vocabulary
of roles, claim types, relations and confidence with one corpus example each and the pairs a
reader confuses, and the exact output schema — and it is generated from the code that already
defines it: `elife_extract/vocabulary.py`, `scripts/relations.py`, `elife_extract/schema.py`.
Edit those and run `make contract`; `make check` fails when the committed contract is not what
the sources generate.

`prompts.py` composes task and contract for a role, and `pipeline/layers.yaml` declares the
same files as the layer's inputs, so a prompt file cannot be sent without being hashed into
the run. A `--prompt-variant` directory overrides any file and inherits the rest.

## Empirical-test knobs

The CLI exposes the knobs future experiments will sweep:

| Flag | Purpose |
|:-----|:--------|
| `--model-{results,caption,structure,reconcile}` | Per-agent model selection |
| `--prompt-variant` | A/B test prompt revisions; named directory under `prompts/<variant>/` |
| `--reconcile-strategy` | `confidence-tagged` (default) \| `union` \| `intersection-only` \| `majority-vote` |
| `--max-claims` | Hard cap on per-paper claim count |
| `--no-retry-on-thin` | Disable retrying agents whose output looks thin |

## Empirical results

Round-trip scoring on Headley 2026 (DOI 10.7554/eLife.95562) against the 26-claim curated
reference at `claims/headley-2026-inhibitory-rhythms/`, with and without the `external-review`
layer in the chain. These were measured when the two were settings of `--review-mode`; the
numbers are of the chain, which is unchanged, but the third column was a curator editing a
draft table and there is no longer any way to do that:

| Metric | Threshold | chain without `external-review` | curator edit (retired) | **with `external-review`** |
|:-------|:----------|:--------------:|:-------------:|:--------------:|
| Claim recovery | ≥ 80% | 100% | 100% | **100%** |
| Panel agreement | ≥ 90% | 50% | depends on reviewer | 50-54% |
| Role classification | ≥ 75% | 65% | depends on reviewer | **96%** ✅ |
| Match quality (exact / partial) | — | 8 / 16 | — | 13 / 13 |
| Per-paper cost | — | ~$5 | ~$5 + analyst time | ~$7 |
| Per-paper wall time | — | ~5 min | ~5 min + review | ~15 min |

Running `external-review` is the recommended default. The Opus reviewer addresses the
systematic biases prose-level extraction misses — under-coverage of the `prediction` and
`hypothesis` roles — at a $2 / paper premium. See `tests/headley-roundtrip-v3-external.md` for
the per-claim scorecard.

Reference check: 12 of 12 literature-context claims in the corpus resolve correctly via
CrossRef, and all 12 carry the cited DOI at top-level `doi:` — the field the schema specifies,
and the one the retired `scripts/verify-references.py` did not read.

## Known limitations

- **Panel agreement at 50%** — papers with multi-panel claims (e.g., reference cites `panel: fig4, fig5`) are extracted as single-panel claims by the Caption-reader. The reconciler and external reviewer prompts don't aggressively expand to multi-panel lists. Targeted prompt iteration is the next polish round.
- **Step 6 (dependency mapping) is scaffolded** — claim files emit with empty `belongings:` / edge sections. The methodology calls for analyst judgment at edge mapping; a future LLM-suggestion pass can populate edges when adoption justifies it.
- **PDF metadata extraction is heuristic** — title may truncate (eLife title spans two lines), year may catch a citation rather than the publication year, author affiliation superscripts may leak into the names. Override slug via `--paper-slug` if the auto-derived form is wrong.
- **Methodology fallback chain not implemented** — `prepare()` raises on PDF fetch failure rather than degrading to GitHub README / API / web fetch per `docs/method.md` § 3.3. Add when papers in the wild break the PDF path.
- **The duplicate reference checker is gone** — `scripts/verify-references.py` checked `assertions[0].doi`, a field no claim in the corpus uses (the schema puts cited DOIs at top-level `doi:`), so every verdict it recorded came from a fuzzy title search. `verify-refs` is now the `reference-check` layer and the only implementation; it absorbed the paper-level DOI check the old script alone performed.

## Directory layout

```
extract/
├── pyproject.toml               # package config, entry point: elife-extract
├── README.md                    # this file
├── prompts/
│   ├── results-reader.md        # each role's task: what it reads and what to look for
│   ├── caption-reader.md
│   ├── structure-reader.md
│   ├── reconciler.md
│   ├── external-reviewer.md
│   ├── edge-inference.md
│   ├── coverage-adjudicator.md
│   └── contract/                # GENERATED — `elife-extract contract --write`
│       ├── vocabulary.md        # roles, claim types, relations, confidence, corpus examples
│       ├── schema-candidate.md  # what a reader returns, from schema.py
│       └── schema-draft.md      # what the reconciler and reviewer return, from schema.py
├── elife_extract/
│   ├── __init__.py
│   ├── cli.py                   # argparse CLI, subcommand dispatch
│   ├── config.py                # Config dataclass, env-var resolution
│   ├── schema.py                # Pydantic models for the wire format
│   ├── prepare.py               # Step 1 — paper fetch + slice
│   ├── agents.py                # Steps 2-3 — three-agent extraction
│   ├── reconcile.py             # Step 4 — reconciliation
│   ├── external_review.py       # Step 4.5 — Opus reviewer pass
│   ├── review.py                # Step 5 — interactive review gate
│   ├── write.py                 # Steps 6-7 — edges + claim files
│   ├── verify_refs.py           # CrossRef DOI resolution
│   └── evaluate.py              # round-trip scoring helpers
└── tests/
    ├── headley_roundtrip.py     # standalone Headley scorer (pre-evaluate)
    ├── headley-roundtrip.md           # v1 scorecard (auto-approve baseline)
    ├── headley-roundtrip-v2.md        # v2 (revised prompts, still auto-approve)
    └── headley-roundtrip-v3-external.md  # v3 (external review)
```

## Where this lives

The Python package develops here in haak (`home/collabs/elife/claim-trees/extract/`) where iteration happens with full agent context. When the CLI is published to the shared eLife repo at `~/Projects/mainenlab/elife-claim-trees`, that's a separate sub-deliverable (publication step of `production:release`); not part of this CLI's job.

## See also

- [`../jobs/extract-cli.md`](../jobs/extract-cli.md) — phase plan, acceptance criteria, full worklog
- [`../briefing.md`](../briefing.md) — claim-trees scope orientation
- [`../../analysis/`](../../analysis/) — peer-review behavior analysis (sibling deliverable)
- `~/Projects/mainenlab/elife-claim-trees/docs/method.md` — full methodology
- `home/projects/inscription/jobs/panel-claim-unification.md` — parent Phase 5 job
