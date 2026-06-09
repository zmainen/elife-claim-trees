# Integration recipe — running elife-extract on your eLife papers

This guide is for the eLife technical team and any external collaborator who wants to run the claim-extraction pipeline on their own eLife papers, with their own Claude / Vertex credentials, on their own machine.

It walks through one full deployment cycle: install → first paper → batch operation → reviewing the output. Each step links to the relevant section of the [README](README.md) for detail.

## Prerequisites

- **Python 3.10 or later.** Check with `python3 --version`.
- **Vertex AI access.** This pipeline runs Anthropic's Claude models via Google Cloud Vertex AI — you'll need a GCP project with the Anthropic models enabled (`claude-opus-4-6`, `claude-sonnet-4-6`, `claude-haiku-4-5`) in the Anthropic Model Garden, plus a service account JSON for authentication.
  - Alternative: the Anthropic SDK supports direct API access via `ANTHROPIC_API_KEY`. Set the env var and the SDK will route there. This requires the same level of model access from Anthropic directly.
- **`pdftotext` is not required** — pdfplumber is the Python library used; it ships with the package.
- **An eLife paper DOI.** This guide uses Headley 2026 (`10.7554/eLife.95562`) as the example.

## 1. Install

Clone the elife-claim-trees repo (when published) or the haak repo, navigate to `extract/`:

```bash
cd home/collabs/elife/claim-trees/extract
pip install -e .
```

Verify:

```bash
elife-extract --version
elife-extract --help
```

You should see the version string and the four subcommands listed: `extract`, `write`, `verify-refs`, `run`, `evaluate`.

## 2. Configure credentials

For Vertex (recommended, since the CLI's defaults target Vertex):

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-service-account.json
export VERTEX_PROJECT_ID=your-gcp-project-id
export VERTEX_REGION=us-central1   # or wherever Anthropic models are enabled
```

Or, if you've configured `gcloud` auth and your project has the models enabled, omit `GOOGLE_APPLICATION_CREDENTIALS` — the SDK will use Application Default Credentials.

For direct Anthropic API:

```bash
export ANTHROPIC_API_KEY=your-anthropic-key
```

Verify the auth path works (a smoke test that calls Vertex once):

```bash
elife-extract extract --doi 10.7554/eLife.95562 \
  --corpus-dir /tmp/test-corpus
```

If this prints a step-by-step extraction trace and ends with `draft saved`, your auth works. If it fails on `403 Permission denied` or `404 Publisher Model not found`, the model isn't enabled in your project / region — check the Vertex AI console.

## 3. Run on your first paper

Pick an eLife paper. The pipeline needs only the DOI; everything else is fetched.

```bash
mkdir -p /tmp/my-corpus

elife-extract extract \
  --doi 10.7554/eLife.<your-paper-id> \
  --corpus-dir /tmp/my-corpus
```

Expect ~5 minutes wall time and ~$5 in API cost. Output:

```
=== Step 1 — Prepare ===
  doi    = 10.7554/eLife.<id>
  slug   = <author>-<year>-<title-keywords>
  ...
  slices = abstract:<size>c results:<size>c captions:<size>c methods:<size>c
  panels = <N> detected

=== Steps 2-3 — Three-agent extraction ===
  ...

=== Step 4 — Reconciliation ===
  draft has <N> claim(s)

=== Output ===
  draft  → /your/output/draft-<slug>.json
  Next: elife-extract write ...
```

The draft JSON is the reconciled claim list. **No claim files have been written yet** — the pipeline waits for the review step.

## 4. Review and write

You have three review modes. Pick the one that fits your operational shape.

### Mode A — Interactive review (curator-quality, single paper)

```bash
elife-extract write \
  --draft <path-from-extract>/draft-<slug>.json \
  --corpus-dir /tmp/my-corpus \
  --review-mode interactive
```

Opens the draft in your `$EDITOR` as a YAML file you can revise. Save and exit to commit. The schema is validated on re-read; parse errors preserve your edits to a `.rescue.yaml` for retry.

### Mode B — External Opus review (recommended for batch)

```bash
elife-extract write \
  --draft <path>/draft-<slug>.json \
  --corpus-dir /tmp/my-corpus \
  --review-mode external
```

An Opus pass reads the paper plus the draft and revises it for the systematic biases prose-level extraction misses (under-coverage of `prediction` and `hypothesis` roles). Adds ~$2 and ~3 minutes per paper. Verified to lift role-classification accuracy from ~65% (auto-approve) to ~96% (external) on the Headley round-trip — output approaches curator quality without curator time.

### Mode C — Auto-approve (tests, demos)

```bash
elife-extract write \
  --draft <path>/draft-<slug>.json \
  --corpus-dir /tmp/my-corpus \
  --review-mode auto-approve
```

Skips review entirely. Use only when you intend to manually review the resulting `.md` files afterwards, or for tests where speed matters more than quality.

## 5. Verify literature-context references

```bash
elife-extract verify-refs \
  --paper <slug> \
  --corpus-dir /tmp/my-corpus \
  --dry-run   # remove --dry-run to write back resolved DOIs
```

For each `role: literature-context` claim, queries CrossRef. Confirms existing DOIs resolve to real papers (anti-hallucination check) and resolves missing DOIs from `Author (Year)` patterns in the claim body.

## 6. Inspect the output

The CLI writes:

```
/tmp/my-corpus/
└── <paper-slug>/
    ├── index.md                   # paper metadata + claims listing
    ├── <claim-slug-1>.md          # one file per claim
    ├── <claim-slug-2>.md
    └── ...
```

Each claim file follows the elife-claim-trees § 4 schema:

```yaml
---
uuid: <uuid4>
slug: <claim-slug>
doi: ~                              # placeholder for non-lit-context claims
claim: |
  Doubling distal dendritic inhibition reduces somatic firing rate from
  approximately 5.5 Hz to approximately 0.2 Hz.
claim-type: empirical
role: empirical
concepts: []                        # analyst fills in at review
priority: 2026-05-10
epistemic: tentative                # default; analyst sets
belongings: []                      # edge mappings; Step 6 (deferred)
assertions:
- paper-slug: <paper-slug>
  doi: 10.7554/eLife.<id>
  panel: fig4
  confidence: tentative
reproductions: []                   # populated by Step 8 (per-paper verify.py)
---

(body prose: extraction notes + per-agent evidence quotes)
```

Open a few claim files and skim. Common things to watch for:

- **Roles look reasonable.** Most claims should be `empirical`. Predictions and hypotheses cluster near the top of the dependency graph; check that they exist if your paper has a clear deductive structure.
- **Panels are anchored.** Empirical claims should have a `panel:` value matching the paper's figure structure. `panel: null` is correct for synthesis or scope claims.
- **Evidence quotes are real.** The body should contain verbatim quotes from the paper grounding each claim. If a quote looks invented, the prompt may need adjustment.

## 7. Batch operation across multiple papers

For more than ~5 papers, run them through `extract` then `write` separately:

```bash
# Extract drafts for many papers in parallel (or sequence) — outputs to /tmp/drafts/
for doi in 10.7554/eLife.95562 10.7554/eLife.<other> ...; do
  elife-extract extract --doi $doi --corpus-dir /tmp/my-corpus --output-dir /tmp/drafts
done

# Then write claim files with external review for each
for draft in /tmp/drafts/draft-*.json; do
  elife-extract write --draft $draft --corpus-dir /tmp/my-corpus --review-mode external
done
```

Or, if you have a curated reference corpus to validate against (e.g., the 12-paper public eLife set), use `evaluate`:

```bash
elife-extract evaluate \
  --reference-dir /path/to/curated-reference/ \
  --work-dir /tmp/eval \
  --all \
  --review-mode external
```

Produces an aggregate scorecard at `<work-dir>/aggregate-scorecard.md` with per-paper recovery / panel / role metrics and means/medians.

## 8. Cost budget for planning

Approximate per-paper cost (10-page eLife paper, ~30-50 claims):

| Operation | Cost (Sonnet 4.6 + Opus 4.6 mix) | Wall time |
|:----------|:-----:|:---------:|
| extract | ~$5 | ~5 min |
| write (interactive) | $0 (your time) | varies |
| write (external Opus review) | ~$2 | ~3 min |
| write (auto-approve) | $0 | <1s |
| verify-refs | $0 (CrossRef is free) | ~1s per cited paper |
| **Total: extract + external review + verify-refs** | **~$7** | **~10 min** |

A 100-paper corpus with external review: ~$700, ~17 hours sequential. Parallelization is straightforward at the shell level (limit by your Vertex rate quota).

## 9. Troubleshooting

| Symptom | Likely cause | Fix |
|:--------|:-------------|:----|
| `404 Publisher Model not found` | Anthropic model not enabled in your Vertex region | Enable in the GCP console or change `--vertex-region` |
| `[Errno 8] nodename nor servname` | DNS / network failure | Check connectivity to `cdn.elifesciences.org` and `*-aiplatform.googleapis.com` |
| Extract hangs > 15 minutes | Vertex API stalled mid-stream | Kill with Ctrl-C; the cached PDF persists, re-run will start from extract step |
| `Streaming required for operations longer than 10 minutes` | max_tokens too high for non-streaming | Already handled in the CLI; report this as a bug if you see it |
| Schema validation error | Reviewer or extraction agent emitted an invalid value | Likely a prompt-output mismatch; report with the full draft JSON for diagnosis |
| Recovery is < 80% on a paper | Paper layout doesn't match eLife conventions | Check the prepare step's slice sizes; the section-header detection may have failed |
| Role classification looks wrong | Auto-approve mode | Use `--review-mode external` or `--review-mode interactive` |

## 10. Where to escalate

- Bugs in the CLI: file an issue in the elife-claim-trees repo (when published) or contact Zach (zmainen@neuro.fchampalimaud.org)
- Methodology questions (when does claim X get role Y?): consult `docs/method.md` § 3.3 and § 4.2 in the elife-claim-trees repo
- Cost optimization questions: see [`README.md` § Empirical-test knobs](README.md#empirical-test-knobs) — `--max-claims`, per-agent model overrides, and `--prompt-variant` give cost levers
