# Configuration

Every flag and environment variable, in one place. Resolution order is CLI argument, then
environment variable, then default.

## `scripts/pipeline.py`

Needs only PyYAML. It holds no credentials and calls no model — it reads the declaration, reads
the ledger, and shells out to the commands the declaration names.

| Subcommand | Arguments |
|:-----------|:----------|
| `graph` | — |
| `state` | `--json`, `--fail-on-stale` |
| `run` | `<paper> <layer>`, `--dry-run`, `--no-deps`, `--note TEXT` |
| `approve` | `<paper> <layer>`, `--by NAME` (required), `--v N`, `--note TEXT` |
| `backfill` | `--force` |

Paths come from the repository it lives in. There is nothing to configure.

## `elife-extract`

### Shared by every layer runner

| Flag | Env | Default | Purpose |
|:-----|:----|:--------|:--------|
| `--paper` | — | required | The paper slug |
| `--root` | `ELIFE_CLAIM_TREES_ROOT` | the directory the package ships in | The corpus repository, which `pipeline/layers.yaml` resolves its paths against |
| `--corpus-dir` | `ELIFE_CORPUS_DIR` | `<root>/claims` | Where claim files are read and written |
| `--prompts-dir` | — | package-local `prompts/` | Override the prompt directory |
| `--prompt-variant` | — | `default` | A named directory under `prompts/<variant>/` |
| `--backend` | `ELIFE_EXTRACT_BACKEND` | `vertex` | `vertex`, `anthropic`, or anything litellm routes |
| `--api-key` | that backend's key variable | — | Not needed for Vertex |
| `-v`, `--verbose` | — | off | Per-chunk DEBUG logging |

### Model routing

Carried by every runner that calls a model.

| Flag | Env | Default |
|:-----|:----|:--------|
| `--model-results` | `ELIFE_EXTRACT_MODEL_RESULTS` | `claude-sonnet-4-6` |
| `--model-caption` | `ELIFE_EXTRACT_MODEL_CAPTION` | `claude-sonnet-4-6` |
| `--model-structure` | `ELIFE_EXTRACT_MODEL_STRUCTURE` | `claude-sonnet-4-6` |
| `--model-reconcile` | `ELIFE_EXTRACT_MODEL_RECONCILE` | `claude-opus-4-6` |
| `--vertex-project` | `VERTEX_PROJECT_ID` | `cr-mainen` |
| `--vertex-region` | `VERTEX_REGION` | `europe-west1` |

`--model-reconcile` covers reconciliation, external review and edge inference — the three steps
that reason over the whole draft rather than over a slice.

### Per-subcommand

| Subcommand | Flags beyond the shared set |
|:-----------|:----------------------------|
| `prepare` | `--doi`, `--pdf-path`, `--input-format {auto,jats,pdf}` |
| `reconcile` | `--reconcile-strategy {confidence-tagged,union,intersection-only,majority-vote}` |
| `edge-inference` | `--dump-prompt PATH`, `--edges-json PATH` |
| `write` | `--format {yaml,oxa}` |
| `verify-refs` | `--paper` optional (omit to sweep), `--dry-run` |
| `coverage` | `--claims-dir`, `--include-methods`, `--mapping`, `--json`, `--fail-on-orphans` |
| `mark` | `--claims-dir`, `--mapping`, `--include-methods`, `--author`, `-o/--out` |
| `evaluate` | `--reference-dir`, `--work-dir`, `--paper`/`--papers`/`--all`, `--no-external-review`, `--skip-existing` |

### Backends

`vertex` and `anthropic` call the Anthropic SDK directly. Every other value is routed through
litellm and needs no code of its own, reading its conventional key from the environment:

| `--backend` | Key |
|:------------|:----|
| `anthropic` | `ANTHROPIC_API_KEY` |
| `openrouter` | `OPENROUTER_API_KEY` |
| `openai` | `OPENAI_API_KEY` |
| `google` | `GEMINI_API_KEY` |
| `groq` | `GROQ_API_KEY` |
| `together` | `TOGETHER_API_KEY` |
| `deepseek` | `DEEPSEEK_API_KEY` |

The published corpus was extracted on `deepseek/deepseek-chat`, which is what the ledger
records for Gädeke's reader layers — not the Vertex default. A run records the model that
answered it, so the defaults documented here are not a claim about what produced any particular
claim file.

## What is not configurable

**Where a layer writes.** That comes from `pipeline/layers.yaml`, and a runner that wrote
somewhere else would produce artifacts the ledger could not hash. `--root` moves the whole tree;
nothing moves one layer's output within it.

**Whether a run is recorded.** `scripts/pipeline.py run` always appends to the ledger. There is
no quiet mode, because a run nobody can account for is the thing the ledger exists to prevent.

**The review gate.** There isn't one. `--review-mode` used to take `interactive`, `external`,
`auto-approve` and `dry-run`; `external` is now the `external-review` layer and `interactive` is
`pipeline.py approve`, which acts on a version after it exists. See
[the runner](/elife-claim-trees/docs/runner/#approve--record-that-a-person-read-a-version).
