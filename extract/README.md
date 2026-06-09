# elife-extract

Eight-step claim induction pipeline for eLife papers. Three-agent extraction (Results, Caption, Structure readers reading partitioned slices), Opus reconciliation, optional Opus review pass, claim file writing per the elife-claim-trees § 4 schema, CrossRef DOI verification, and round-trip evaluation against a curated reference corpus.

**Status: working.** All eight phases of the job spec are implemented. Verified end-to-end on Headley 2026 with 100% claim recovery against the curated reference and 96% role agreement when run in `--review-mode external`. See `tests/headley-roundtrip-v3-external.md` for the per-claim scorecard.

**Methodology authority:** `~/Projects/mainenlab/elife-claim-trees/docs/method.md` § 3 (Claim induction — the eight-step process), § 4 (Schema). The CLI implements that methodology; when a behavior decision isn't anticipated by the doc, the CLI's behavior is the decision and the doc is updated in the same commit.

## Install

```bash
cd home/collabs/elife/claim-trees/extract
pip install -e .
```

Requires Python 3.10+, the Anthropic SDK with Vertex backend (`anthropic[vertex]`), pdfplumber, httpx, pyyaml, pydantic. All installed automatically.

You also need Vertex AI credentials. The CLI defaults to `cr-mainen` / `europe-west1` (HAAK's Vertex project); override with `--vertex-project` / `--vertex-region` or env vars.

## Configure

The CLI reads from CLI args first, then environment variables, then defaults.

| Variable | CLI flag | Required? | Purpose |
|:---------|:---------|:----------|:--------|
| `ELIFE_CORPUS_DIR` | `--corpus-dir` | yes (for write/run/verify-refs) | Where claim files are read/written |
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

The CLI is two-phase per the methodology's Step 5 review gate (no claim files written until the draft is reviewed).

### `extract` — steps 1-4

```bash
elife-extract extract \
  --doi 10.7554/eLife.95562 \
  --corpus-dir /path/to/corpus
```

Fetches the paper PDF from the eLife CDN (cached at `~/.cache/elife-extract/`), slices into abstract/results/captions/methods, runs three Sonnet agents independently, reconciles with Opus, writes a draft JSON to `<output-dir>/draft-<slug>.json`. **No claim files are written.**

### `write` — steps 5-7

```bash
elife-extract write \
  --draft <output-dir>/draft-<slug>.json \
  --corpus-dir /path/to/corpus \
  --review-mode interactive
```

Loads the draft, runs the chosen review mode, then writes per-claim `.md` files into `<corpus-dir>/<slug>/`.

**Review modes:**

| Mode | What happens | Use case |
|:-----|:-------------|:---------|
| `interactive` | Opens the draft in `$EDITOR` for you to revise; saves and re-parses on exit | Production single-paper runs where curator-quality output matters |
| `external` | Runs an Opus review pass that addresses the auto-approve role-classification gap (see [Phase F findings](#empirical-results)); writes the revised draft directly | Batch runs where human review isn't feasible; **recommended default for unattended operation** |
| `auto-approve` | Skips review; writes the reconciled draft as-is | Tests, demos, when you intend to review the resulting claim files manually after |
| `dry-run` | Prints the draft, writes nothing | Inspecting the extraction without committing |

### `verify-refs` — CrossRef DOI resolution

```bash
elife-extract verify-refs \
  --paper <slug> \
  --corpus-dir /path/to/corpus \
  --dry-run    # omit to write back resolved DOIs
```

For each `role: literature-context` claim in `<corpus-dir>/<slug>/`, queries CrossRef. Two paths:

- **confirm**: claim already has a top-level `doi:` (per the schema); CrossRef confirms it resolves to a real paper (anti-hallucination check)
- **found**: no DOI yet; extracts Author (Year) hints from claim text and slug, queries CrossRef, writes the highest-scoring match (score > 15) back to top-level `doi:`

Omit `--paper` to sweep the whole corpus. Use `--dry-run` to inspect resolutions before committing.

### `run` — composed shorthand

```bash
elife-extract run \
  --doi 10.7554/eLife.95562 \
  --corpus-dir /tmp/test-corpus
```

End-to-end: extract + write (auto-approve) + verify-refs. Useful for tests and demos. **Implies `--review-mode auto-approve` — does not run external review by default.** For production batch runs, use `extract` and `write --review-mode external` separately, or invoke the per-paper helper through `evaluate`.

### `evaluate` — round-trip scoring against a reference corpus

```bash
elife-extract evaluate \
  --reference-dir ~/Projects/mainenlab/elife-claim-trees/claims \
  --work-dir /tmp/elife-eval \
  --paper headley-2026-inhibitory-rhythms \
  --review-mode external

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
2. Runs the full pipeline (`extract` → `reconcile` → optional `external_review` → `write`)
3. Calls Opus matcher to align CLI claims with reference claims
4. Saves per-paper scorecard at `<work-dir>/<paper-slug>/scorecard.json`

After all papers, renders an aggregate scorecard at `<work-dir>/aggregate-scorecard.md` with mean / median per-paper metrics and a comparison table. `--skip-existing` reuses prior scorecards (resumable sweeps).

Use `evaluate` to validate prompt iterations, model changes, or new review modes — produces the same scorecard format as the manual round-trip in `tests/headley_roundtrip.py`.

## Empirical-test knobs

The CLI exposes the knobs future experiments will sweep:

| Flag | Purpose |
|:-----|:--------|
| `--model-{results,caption,structure,reconcile}` | Per-agent model selection |
| `--prompt-variant` | A/B test prompt revisions; named directory under `prompts/<variant>/` |
| `--reconcile-strategy` | `confidence-tagged` (default) \| `union` \| `intersection-only` \| `majority-vote` |
| `--review-mode` | `interactive` \| `external` \| `auto-approve` \| `dry-run` |
| `--max-claims` | Hard cap on per-paper claim count |
| `--no-retry-on-thin` | Disable retrying agents whose output looks thin |

## Empirical results

Round-trip scoring on Headley 2026 (DOI 10.7554/eLife.95562) against the 26-claim curated reference at `~/Projects/mainenlab/elife-claim-trees/claims/headley-2026-inhibitory-rhythms/`. Three review modes:

| Metric | Threshold | `auto-approve` | `interactive` | **`external`** |
|:-------|:----------|:--------------:|:-------------:|:--------------:|
| Claim recovery | ≥ 80% | 100% | 100% | **100%** |
| Panel agreement | ≥ 90% | 50% | depends on reviewer | 50-54% |
| Role classification | ≥ 75% | 65% | depends on reviewer | **96%** ✅ |
| Match quality (exact / partial) | — | 8 / 16 | — | 13 / 13 |
| Per-paper cost | — | ~$5 | ~$5 + analyst time | ~$7 |
| Per-paper wall time | — | ~5 min | ~5 min + review | ~15 min |

`--review-mode external` is the recommended unattended setting. The Opus reviewer addresses the systematic biases that prose-level extraction misses (under-coverage of `prediction` and `hypothesis` roles), at a $2 / paper cost premium. See `tests/headley-roundtrip-v3-external.md` for the per-claim scorecard.

CrossRef DOI verification (verify-refs): 12/12 literature-context claims across the 6-paper public-eLife subset of the curated corpus resolved correctly via CrossRef — 100% anti-hallucination check.

## Known limitations

- **Panel agreement at 50%** — papers with multi-panel claims (e.g., reference cites `panel: fig4, fig5`) are extracted as single-panel claims by the Caption-reader. The reconciler and external reviewer prompts don't aggressively expand to multi-panel lists. Targeted prompt iteration is the next polish round.
- **Step 6 (dependency mapping) is scaffolded** — claim files emit with empty `belongings:` / edge sections. The methodology calls for analyst judgment at edge mapping; a future LLM-suggestion pass can populate edges when adoption justifies it.
- **PDF metadata extraction is heuristic** — title may truncate (eLife title spans two lines), year may catch a citation rather than the publication year, author affiliation superscripts may leak into the names. Override slug via `--paper-slug` if the auto-derived form is wrong.
- **Methodology fallback chain not implemented** — `prepare()` raises on PDF fetch failure rather than degrading to GitHub README / API / web fetch per `docs/method.md` § 3.3. Add when papers in the wild break the PDF path.
- **Schema bug in canonical script** — `~/Projects/mainenlab/elife-claim-trees/scripts/verify-references.py` checks `assertions[0].doi`, but the schema actually puts cited DOIs at top-level `doi:` for literature-context claims. This CLI's `verify-refs` reads from the right field; the canonical script is in latent disagreement with the data.

## Directory layout

```
extract/
├── pyproject.toml               # package config, entry point: elife-extract
├── README.md                    # this file
├── prompts/
│   ├── results-reader.md        # Agent A — abstract + results prose
│   ├── caption-reader.md        # Agent B — figure captions, panel-by-panel
│   ├── structure-reader.md      # Agent C — methods + supplements + code
│   ├── reconciler.md            # Step 4 — Opus reconciliation
│   └── external-reviewer.md     # Step 4.5 — Opus structural-inference pass
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
