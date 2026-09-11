# Integration recipe — running elife-extract on your eLife papers

This guide is for the eLife technical team and any external collaborator who wants to run the claim-extraction pipeline on their own eLife papers, with their own Claude / Vertex credentials, on their own machine.

It walks through one full deployment cycle: install → first paper → batch operation → reviewing the output. Each step links to the relevant section of the [README](README.md) for detail.

**The unit of work is a layer.** `pipeline/layers.yaml` declares the processing graph — what
each layer asks, what it reads, what it produces — and `scripts/pipeline.py` is what runs one,
after running whatever it still needs. Every run is recorded in `runs/<paper>/ledger.jsonl`
with the content hash of each input, so whether a result is still current is asked of the files
rather than of anyone's memory. The `elife-extract` subcommands below are the layer runners
themselves; you can call them directly, but nothing then records that you did.

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

You should see the version string and one subcommand per runnable layer: `prepare`,
`results-reader`, `caption-reader`, `structure-reader`, `reconcile`, `external-review`,
`edge-inference`, `write`, `verify-refs`, `coverage`, `mark` — plus `evaluate`, which is a
tool rather than a layer.

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

Verify the auth path works. `prepare` fetches and slices the paper without calling a model,
so run it first to separate a network problem from a credentials one, then one reader:

```bash
elife-extract prepare --paper headley-2026-inhibitory-rhythms --doi 10.7554/eLife.95562
elife-extract results-reader --paper headley-2026-inhibitory-rhythms
```

If the first prints slice sizes and the second prints a candidate-claim count, your auth works.
If the second fails on `403 Permission denied` or `404 Publisher Model not found`, the model
isn't enabled in your project / region — check the Vertex AI console.

## 3. Run on your first paper

Pick an eLife paper. Ask for the layer you want and let the runner work out what it needs:

```bash
python3 scripts/pipeline.py run <paper-slug> claim-tree --dry-run   # what would run
python3 scripts/pipeline.py run <paper-slug> claim-tree             # run it
```

Expect ~5 minutes wall time and ~$7 in API cost. The dry run prints the chain in dependency
order — `prepare`, the three readers, `reconcile`, `external-review`, `edge-inference`, then
`claim-tree` — which is the same list the site's pipeline page shows, because both read the
same declaration.

A paper that is not yet in the corpus has no `claims/<slug>/index.md` for the runner to take
the DOI from, so seed it once by hand and then use the runner for everything after:

```bash
elife-extract prepare --paper <paper-slug> --doi 10.7554/eLife.<id>
python3 scripts/pipeline.py run <paper-slug> claim-tree
```

Each layer writes to the path its declaration names, under `runs/<paper>/`, and the claim files
land in `claims/<paper>/`. Nothing is written outside those paths, which is what lets the ledger
hash a run's outputs rather than take their existence on trust.

## 4. Review

There are no review modes. There used to be a `--review-mode` flag, and it bundled two
different things.

The first was `external` — an Opus pass that reads the paper plus the draft and revises it for
the biases prose-level extraction misses, chiefly under-coverage of the `prediction` and
`hypothesis` roles. That is not review; it changes the artifact, and it happens before the
version a reviewer would read exists. It is now the `external-review` layer, which runs in the
chain above. Adds ~$2 and ~3 minutes per paper, and lifts role agreement from ~65% to ~96% on
the Headley round-trip. Because it is declared, editing `extract/prompts/external-reviewer.md`
now makes every claim tree built on it stale, which the flag could never express.

The second was `interactive`, an editor opened on the draft before anything was written. That
reviewed the wrong object: what you edited was a draft table, while the version that reached
the corpus was whatever `write` then made of it, and your edits left no record that anyone had
looked. Approval is now an operation on a version that exists:

```bash
python3 scripts/pipeline.py approve <paper-slug> claim-tree \
  --by "your name" --note "roles checked against figures 2-4"
```

The record names the version. Re-run the layer and the approval does not follow it — it was
granted to text that no longer exists, and `pipeline.py state` shows it as no longer applying
rather than silently carrying it forward. To correct a claim, edit the file; that makes the
layer stale against its own ledger entry, which is true, and visible.

## 5. Verify literature-context references

```bash
python3 scripts/pipeline.py run <paper-slug> reference-check
```

For each `role: literature-context` claim, queries CrossRef: confirms existing DOIs resolve to
real papers (the anti-hallucination check) and resolves missing ones from `Author (Year)`
patterns in the claim body. It also confirms the paper's own DOI from its `index.md`. The
verdicts are kept at `runs/<paper>/reference-check.output.json` rather than printed and lost.

To see what it would write without writing it:

```bash
elife-extract verify-refs --paper <paper-slug> --dry-run
```

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

Ask for the same layer once per paper. The runner skips what is already current, so a
re-run costs nothing for the papers that have not changed:

```bash
for paper in $(python3 -c "import yaml;print(' '.join(yaml.safe_load(open('corpus.yaml'))['corpora']['elife']['papers']))"); do
  python3 scripts/pipeline.py run $paper claim-tree --note "batch $(date +%F)"
done
```

Then see where the corpus stands:

```bash
python3 scripts/pipeline.py state
python3 scripts/pipeline.py state --fail-on-stale   # as a CI gate
```

A jagged edge in that matrix is the normal condition, not a defect: a blank means the layer
has not been run for that paper, not that it ran and found nothing.

### Validating a prompt change

`evaluate` is the one subcommand that is not a layer, and it is deliberately outside the
graph: it re-runs the chain into a temp tree and scores the result against the committed claim
files, so it asks about the prompts rather than about a paper, and produces nothing any layer
consumes.

```bash
elife-extract evaluate \
  --reference-dir ../claims/ \
  --work-dir /tmp/eval \
  --all
```

Produces an aggregate scorecard at `<work-dir>/aggregate-scorecard.md` with per-paper recovery
/ panel / role metrics and means/medians. Change a prompt, re-run, diff the aggregate, decide —
which is what makes prompt iteration a discipline rather than an impression. Pass
`--no-external-review` to score the chain without the Opus pass.

## 8. Cost budget for planning

Approximate per-paper cost (10-page eLife paper, ~30-50 claims):

| Layer | Cost (Sonnet 4.6 + Opus 4.6 mix) | Wall time |
|:------|:-----:|:---------:|
| `prepare` | $0 (fetch + slice, cached) | ~2 s |
| the three readers | ~$4 | ~4 min |
| `reconcile` | ~$1 | ~1 min |
| `external-review` | ~$2 | ~3 min |
| `edge-inference` | ~$0.20 | ~30 s |
| `claim-tree` | $0 (reads the edges the layer wrote) | <1 s |
| `reference-check` | $0 (CrossRef is free) | ~1 s per cited paper |
| `coverage`, `mark` | $0 (no model calls) | ~5 s |
| **Total, one paper end to end** | **~$7** | **~10 min** |

`claim-tree` used to call edge inference a second time itself, paying twice for an answer the
`edge-inference` layer had already written to disk.

A 100-paper corpus with external review: ~$700, ~17 hours sequential. Parallelization is straightforward at the shell level (limit by your Vertex rate quota).

## 9. Troubleshooting

| Symptom | Likely cause | Fix |
|:--------|:-------------|:----|
| `404 Publisher Model not found` | Anthropic model not enabled in your Vertex region | Enable in the GCP console or change `--vertex-region` |
| `[Errno 8] nodename nor servname` | DNS / network failure | Check connectivity to `cdn.elifesciences.org` and `*-aiplatform.googleapis.com` |
| A reader hangs > 15 minutes | Vertex API stalled mid-stream | Kill with Ctrl-C. The fetched paper is cached and `prepare`'s output is on disk, so the re-run resumes at the layer that failed rather than at the beginning |
| `Streaming required for operations longer than 10 minutes` | max_tokens too high for non-streaming | Already handled in the CLI; report this as a bug if you see it |
| Schema validation error | Reviewer or extraction agent emitted an invalid value | Likely a prompt-output mismatch; report with the full draft JSON for diagnosis |
| Recovery is < 80% on a paper | Paper layout doesn't match eLife conventions | Check the slice sizes `prepare` reported, or read `runs/<paper>/prepared.json` directly; the section-header detection may have failed |
| Role classification looks wrong | `external-review` has not run for that paper | `python3 scripts/pipeline.py run <paper> external-review`, then re-run `claim-tree`. `pipeline.py state` shows which papers have been through it |

## 10. Where to escalate

- Bugs in the CLI: file an issue in the elife-claim-trees repo (when published) or contact Zach (zmainen@neuro.fchampalimaud.org)
- Methodology questions (when does claim X get role Y?): consult `docs/method.md` § 3.3 and § 4.2 in the elife-claim-trees repo
- Cost optimization questions: see [`README.md` § Empirical-test knobs](README.md#empirical-test-knobs) — `--max-claims`, per-agent model overrides, and `--prompt-variant` give cost levers
