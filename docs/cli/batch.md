# Batch operation

Running a layer across the corpus is the same command in a loop. What makes it workable is that
the runner knows what has already been done: a layer whose cell is `current` is skipped, so
re-running a sweep costs nothing for the papers that have not changed.

```bash
for paper in $(python3 -c "import yaml;print(' '.join(
    yaml.safe_load(open('corpus.yaml'))['corpora']['elife']['papers']))"); do
  python3 scripts/pipeline.py run "$paper" claim-tree --note "sweep $(date +%F)"
done
```

Then look at what happened:

```bash
python3 scripts/pipeline.py state
```

## Re-running after a prompt change

This is the case the ledger exists for. Edit `extract/prompts/caption-reader.md` and every run
that read it becomes `stale`, because the run recorded the hash of the prompt it used. Staleness
propagates along `needs`, so the reconciliation, the review, the edges and the tree downstream
of it go `blocked` — not wrong, but not to be trusted until the thing above them is rebuilt.

`state` will show you exactly which cells. The sweep above then rebuilds only those.

Before spending anything on a corpus-wide re-run, measure the change on one paper:
[`evaluate`](/elife-claim-trees/docs/evaluate/) scores a re-extraction against the committed
corpus, so you find out whether the prompt is better before you rebuild ten papers with it.

## As a gate

```bash
python3 scripts/pipeline.py state --fail-on-stale
```

Exits non-zero if any cell is stale — a prompt or a script changed and the artifacts built from
it have not been rebuilt. Suitable for CI.

Note what it does *not* fail on: `absent`, and `unrecorded`. A jagged edge in the matrix is the
normal condition of this corpus rather than a defect, and a gate that treated an un-run layer as
a failure would be red permanently and read by nobody.

## Cost

Per paper, for a typical eLife article:

| Layer | Cost | Wall time |
|:------|-----:|:----------|
| `prepare` | $0 — fetch and slice, cached after the first | ~2 s |
| the three readers | ~$4 | ~4 min |
| `reconcile` | ~$1 | ~1 min |
| `external-review` | ~$2 | ~3 min |
| `edge-inference` | ~$0.20 | ~30 s |
| `claim-tree` | $0 — reads the edges the layer wrote | <1 s |
| `reference-check` | $0 — CrossRef is free | ~1 s per citation |
| `coverage`, `marks` | $0 — no model calls | ~5 s |
| **end to end** | **~$7** | **~10 min** |

A hundred-paper corpus with external review is roughly $700 and seventeen hours run
sequentially. Parallelising across papers is safe — the layers for one paper never read another
paper's files — and the practical limit is your provider's rate quota, not the pipeline.

`claim-tree` costing nothing is recent. It used to call edge inference itself, paying a second
time per paper for an answer the `edge-inference` layer had already written to disk.

## Cutting the cost

- **Skip external review** where role accuracy matters less than throughput: $2 and three
  minutes per paper. It is the difference between ~65% and ~96% role agreement, so this is a
  real trade rather than a free saving.
- **`--model-{results,caption,structure}`** sends the readers to a cheaper model. They read a
  slice and emit structured claims, which is the least demanding work in the chain.
- **`--max-claims`** caps per-paper output, for smoke tests.
- **`prepare` is cached** under `~/.cache/elife-extract/`, so re-running any layer on a paper
  costs no fetch and works offline.

## Papers outside the corpus

The runner acts on papers listed in `corpus.yaml`, and takes their DOIs from
`claims/<paper>/index.md` — which a new paper does not have until `claim-tree` has run. So the
first layer is seeded by hand:

```bash
cd extract && python3 -m elife_extract.cli prepare --paper <slug> --doi 10.7554/eLife.<id>
```

Add the slug to `corpus.yaml` and the rest of the chain runs normally. For a paper that is not
an eLife DOI at all, `--pdf-path` takes a local file; expect worse slicing, since a PDF gives a
column-order guess where JATS gives real section boundaries.
