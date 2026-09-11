# Install and configure

From a clean Python environment to a working pipeline in under ten minutes.

## Prerequisites

- **Python 3.10 or later.** Check with `python3 --version`.
- **A clone of this repository.** The extraction package ships inside it, at `extract/`, and
  the layer declaration it works against is at `pipeline/layers.yaml`. The two are not
  separable: a layer runner writes the paths the declaration names.
- **Vertex AI access, or a direct Anthropic API key.** Vertex is the canonical configuration.
- **A budget.** Roughly $7 per paper with external review, so a hundred-paper corpus is about
  $700 and seventeen hours run sequentially.

`pipeline.py` itself needs only PyYAML. You can read the graph, the state matrix and the whole
ledger without installing the extraction package or holding any credentials at all:

```bash
pip install pyyaml
python3 scripts/pipeline.py state
```

## Install the package

```bash
cd extract
pip install -e .
```

This installs the `elife-extract` console script with its dependencies — `anthropic[vertex]`,
`httpx`, `pdfplumber`, `pyyaml`, `pydantic`.

```bash
elife-extract --version
elife-extract --help
```

You should see one subcommand per runnable layer — `prepare`, the three readers, `reconcile`,
`external-review`, `edge-inference`, `write`, `verify-refs`, `coverage`, `mark` — plus
`evaluate`, which is a tool rather than a layer.

## Configure Vertex AI

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-service-account.json
export VERTEX_PROJECT_ID=your-gcp-project-id
export VERTEX_REGION=us-central1   # or wherever Anthropic models are enabled
```

Anthropic's models must be enabled in your project's Model Garden subscription for the regions
you target. The defaults are `claude-sonnet-4-6` for the three readers and `claude-opus-4-6`
for reconciliation, external review and edge inference.

`404 Publisher Model not found` means the model is not enabled in that project and region.
Enable it in the Vertex console, or point elsewhere with `--vertex-region`.

Without `GOOGLE_APPLICATION_CREDENTIALS` the SDK falls back to Application Default Credentials;
`gcloud auth application-default login` sets those up.

## Or configure a direct API

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export ELIFE_EXTRACT_BACKEND=anthropic
```

Any backend other than `vertex` or `anthropic` — `openrouter`, `openai`, `google`, `groq`,
`together`, `deepseek` — is routed through litellm and needs no code of its own. Each reads its
own conventional key from the environment.

## The environment contract

Configuration resolves CLI args first, then environment, then defaults.

| Variable | Flag | Purpose |
|:---------|:-----|:--------|
| `ELIFE_CLAIM_TREES_ROOT` | `--root` | The corpus repository, which `pipeline/layers.yaml` resolves its paths against. Defaults to the directory the package ships in |
| `ELIFE_CORPUS_DIR` | `--corpus-dir` | Where claim files are read and written (default: `<root>/claims`) |
| `VERTEX_PROJECT_ID` | `--vertex-project` | GCP project (default: `cr-mainen`) |
| `VERTEX_REGION` | `--vertex-region` | Vertex region (default: `europe-west1`) |
| `GOOGLE_APPLICATION_CREDENTIALS` | — | Service account JSON, for Vertex |
| `ANTHROPIC_API_KEY` | `--api-key` | Direct Anthropic auth |
| `ELIFE_EXTRACT_BACKEND` | `--backend` | Which provider to route to |
| `ELIFE_EXTRACT_MODEL_RESULTS` | `--model-results` | Override the Results-reader model |
| `ELIFE_EXTRACT_MODEL_CAPTION` | `--model-caption` | Override the Caption-reader model |
| `ELIFE_EXTRACT_MODEL_STRUCTURE` | `--model-structure` | Override the Structure-reader model |
| `ELIFE_EXTRACT_MODEL_RECONCILE` | `--model-reconcile` | Override the model for reconciliation, external review and edge inference |

`--root` is the one worth understanding. Everything a layer writes lands under it, because a
run is only recordable if its outputs are where the declaration says they are. The default —
two directories above the package — is right whenever the package sits in the repository it
produces.

## Smoke test

Check the parts separately, so a failure tells you which one broke. `prepare` calls no model,
so if it works and a reader does not, the problem is credentials rather than network:

```bash
cd extract
python3 -m elife_extract.cli prepare --paper headley-2026-inhibitory-rhythms \
  --doi 10.7554/eLife.95562
python3 -m elife_extract.cli results-reader --paper headley-2026-inhibitory-rhythms
```

The first prints slice sizes and writes `runs/<paper>/prepared.json` in a couple of seconds.
The second prints a candidate-claim count and costs a few cents.

| Symptom | Cause | Fix |
|:--------|:------|:----|
| `404 Publisher Model not found` | Model not enabled in that Vertex region | Enable it, or change `--vertex-region` |
| `[Errno 8] nodename nor servname` | DNS or network | Check reachability of `cdn.elifesciences.org` and `*-aiplatform.googleapis.com` |
| `root not found` | `--root` points somewhere that is not the repository | Pass `--root`, or set `ELIFE_CLAIM_TREES_ROOT` |
| `needs prepared.json, which prepare has not produced` | You skipped a layer | Run the layer it names, or use `pipeline.py run`, which does that for you |
| `pdfplumber import error` | Dependency missing | `pip install -e .` again, in the environment you are actually using |

## Next

- [One paper end to end](/elife-claim-trees/docs/first-paper/)
- [The runner](/elife-claim-trees/docs/runner/) — what `pipeline.py` does with all this
- [Configuration](/elife-claim-trees/docs/config/) — every flag in detail
