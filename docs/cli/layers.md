# The layer runners

`elife-extract` is one subcommand per runnable layer. Each reads the paths its layer declares
and writes the path its layer declares, and does nothing else — no dependency resolution, no
ledger. [The runner](/elife-claim-trees/docs/runner/) does both.

Every subcommand takes `--paper <slug>` and finds its inputs from there. The DOI comes from
`claims/<paper>/index.md`; a paper not yet in the corpus has no index, so `prepare` takes an
explicit `--doi` the first time.

| Subcommand | Layer | Produces |
|:-----------|:------|:---------|
| `prepare` | [`prepare`](/elife-claim-trees/pipeline/prepare/) | `runs/<paper>/prepared.json` |
| `results-reader` | [`results-reader`](/elife-claim-trees/pipeline/results-reader/) | `runs/<paper>/results-reader.output.json` |
| `caption-reader` | [`caption-reader`](/elife-claim-trees/pipeline/caption-reader/) | `runs/<paper>/caption-reader.output.json` |
| `structure-reader` | [`structure-reader`](/elife-claim-trees/pipeline/structure-reader/) | `runs/<paper>/structure-reader.output.json` |
| `reconcile` | [`reconcile`](/elife-claim-trees/pipeline/reconcile/) | `runs/<paper>/reconciler.output.json` |
| `external-review` | [`external-review`](/elife-claim-trees/pipeline/external-review/) | `runs/<paper>/external-review.output.json` |
| `edge-inference` | [`edge-inference`](/elife-claim-trees/pipeline/edge-inference/) | `runs/<paper>/edge-inference.output.json` |
| `write` | [`claim-tree`](/elife-claim-trees/pipeline/claim-tree/) | `claims/<paper>/*.md` |
| `verify-refs` | [`reference-check`](/elife-claim-trees/pipeline/reference-check/) | `runs/<paper>/reference-check.output.json` |
| `coverage` | [`coverage`](/elife-claim-trees/pipeline/coverage/) | `coverage/<paper>.json` |
| `mark` | [`marks`](/elife-claim-trees/pipeline/marks/) | `marked/<paper>.marked.md` |

`evaluate` is the twelfth subcommand and is not a layer; it has
[a page of its own](/elife-claim-trees/docs/evaluate/).

## `prepare` — the paper the readers read

```bash
elife-extract prepare --paper gadeke-2026-guilt-insula
elife-extract prepare --paper <slug> --doi 10.7554/eLife.<id>    # a paper new to the corpus
elife-extract prepare --paper <slug> --pdf-path ./paper.pdf      # not on the eLife CDN
```

Fetches the paper — JATS XML for eLife DOIs, which gives clean section boundaries and caption
text where a PDF gives a column-order guess — and slices it into the abstract, results,
captions and methods that the three readers each get. The fetch is cached under
`~/.cache/elife-extract/`, so re-running any layer on the same paper is free and offline.

It is a layer of its own because otherwise a reader's only declared input is its prompt: the
ledger would record which prompt read a paper without recording which paper, and eLife revises
papers. `runs/<paper>/prepared.json` is the text the corpus was actually built from.

## The three readers

```bash
elife-extract results-reader   --paper <slug>
elife-extract caption-reader   --paper <slug>
elife-extract structure-reader --paper <slug>
```

Each reads one slice under one prompt and proposes candidate claims, each with a panel, a role
and the verbatim sentence it rests on.

- **`results-reader`** reads the abstract and results prose — framing, hypotheses, predictions,
  synthesis and interpretation as the prose presents them.
- **`caption-reader`** reads the figure and table captions panel by panel — the quantitative
  claims, anchored to the panel that shows them.
- **`structure-reader`** reads the methods, supplements and section structure — methodological
  capabilities, scope conditions, and what the paper frames as its own conclusions.

They are three layers rather than one because none sees another's output. They are independent
witnesses, and their agreement is the informative case; collapsing them into a single call
loses it, which is what a single agent reading the whole paper does — and it fails in
characteristic ways, inventing numbers where prose summarises and attaching claims to the wrong
panel.

Each writes the model that answered it into its own output, which is what the ledger reads to
record who wrote a claim.

## `reconcile` — which candidates survive

```bash
elife-extract reconcile --paper <slug>
elife-extract reconcile --paper <slug> --reconcile-strategy union
```

Reads the three readers' outputs from disk and aligns them into one draft claim table, tagged
`high`, `contested` or `single-source`, carrying which readers surfaced each claim and the
evidence each quoted.

Single-source is not a synonym for weak. A claim only one reading strategy surfaced may be real
but buried, or it may be an artefact of that strategy — the tag records which question is open
rather than answering it.

`--reconcile-strategy` selects how the three lists combine: `confidence-tagged` (default),
`union`, `intersection-only`, `majority-vote`.

## `external-review` — what the readers systematically miss

```bash
elife-extract external-review --paper <slug>
```

One Opus pass over the reconciled draft, recovering the structure prose-level extraction
under-covers: the `prediction` and `hypothesis` roles, and multi-panel claims collapsed to a
single panel. Roughly $2 and three minutes per paper, and it lifts role agreement from ~65% to
~96% on the Headley round-trip.

This was a flag, `--review-mode external`, and it is not review. It changes the artifact, and
it runs before the version a reviewer would read exists. It took the name of the curator's seat
in the eight-step methodology and kept it after the seat was gone.

Declared as a layer it earns what the flag could not: edit
`extract/prompts/external-reviewer.md` and every claim tree built on it goes stale, computed
rather than remembered. As a flag, you could rewrite that prompt and nothing anywhere could
detect that the corpus had been built by a different reviewer.

`claim-tree` builds on this layer's output where it has run and on the reconciled draft where it
has not, so a paper without it is the ordinary case rather than a failure.

## `edge-inference` — which claims depend on which

```bash
elife-extract edge-inference --paper <slug>
elife-extract edge-inference --paper <slug> --dump-prompt /tmp/edges.txt
elife-extract edge-inference --paper <slug> --edges-json /tmp/answer.json
```

Infers typed relations between the draft's claims — the deductive spine, `entails` from
hypothesis to prediction and `tests` back from the empirical result.

`--dump-prompt` writes the exact request and exits, so that whatever answers it — an analyst, a
reasoning agent, a different provider — answers the same question the layer would have asked
rather than a paraphrase of it written from memory. `--edges-json` records that answer, and it
goes through exactly the same validation an inferred one gets: edges naming an unknown slug, or
pointing at themselves, are dropped either way. An invented target is worse than a missing edge,
and that has to hold no matter who produced the answer.

This exists because the spine is the part of a claim tree that matters most and the part most
easily lost to a provider outage. On one live Gädeke run every other stage succeeded and the
edges were gone — HTTP 402, a token budget the account could not afford.

## `write` — the claim tree

```bash
elife-extract write --paper <slug>
elife-extract write --paper <slug> --format oxa    # one OXA JSON Document instead
```

Assigns slugs and UUIDs, attaches the edges `edge-inference` produced, and writes one file per
claim into `<corpus-dir>/<paper>/` plus the paper's `index.md`.

It reads those edges rather than inferring them again. It used to do the latter — a second paid
Opus call, per paper, for an answer already sitting on disk.

Refuses to overwrite a non-empty paper directory. Move or delete it to re-run.

## `verify-refs` — the reference check

```bash
elife-extract verify-refs --paper <slug>
elife-extract verify-refs --paper <slug> --dry-run   # resolve, write nothing
elife-extract verify-refs                            # sweep the corpus, write no report
```

Confirms the paper's own DOI from its `index.md`, then for each `role: literature-context`
claim takes one of two paths:

- **confirm** — the claim already has a top-level `doi:`; CrossRef confirms it resolves to a
  real paper. This is the anti-hallucination check, and it is the one that matters.
- **found** — no DOI yet; hints are extracted from the claim text and slug, CrossRef is
  queried, and the highest-scoring match above a confidence threshold is written back.

All {{literature_context_doi_top_level}} of the {{literature_context_claims}}
literature-context claims in the published corpus carry the cited DOI at top-level `doi:`,
where the schema puts it, and {{literature_context_doi_in_assertions}} carry it at
`assertions[0].doi`. Those counts are generated rather than asserted, because they are what a
second implementation of this check got wrong: `scripts/verify-references.py` read
`assertions[0].doi`, so its confirm path never fired for any claim and every verdict it
recorded came from a fuzzy title search instead. One entered the record as a confirmed match
titled "NEEDLE TINS", for a claim whose own file already carried the right DOI. That script is
gone; this is the only implementation.

Omitting `--paper` sweeps the corpus but writes no report, because a version belongs to one
paper.

## `coverage` and `mark`

```bash
elife-extract coverage --paper <slug> --json ../coverage/<slug>.json
elife-extract coverage --paper <slug> --mapping ../mappings/<slug>.json
elife-extract coverage --paper <slug> --fail-on-orphans
elife-extract mark --paper <slug> --mapping ../mappings/<slug>.json -o ../marked/<slug>.marked.md
```

Neither calls a model, so both are free and fast enough to run over the whole corpus.

`coverage` takes its denominator **from the paper** rather than from the claim set. It builds
the paper's own inventories — every panel, every table, every reported statistic — then cuts
the whole text into one-sentence spans and asks of each whether any claim accounts for it. That
is what lets it see what a comparison between two claim sets cannot: you can score 100%
agreement on a third of a paper.

`--mapping` folds in the adjudicated verdicts from `mappings/<paper>.json`, so the report shows
real gaps rather than everything a string comparison could not match. Without it, Gädeke reports
36 unaccounted spans; with it, 22 were the matcher being wrong and 14 were real.

`mark` writes those verdicts into the document itself, as tika marks carrying each claim's
UUID. A span that states no result says so; a span carrying a result that no claim states is
marked as a gap, so it is visible by looking rather than only countable in a report. The marks
are read straight back after writing — a document that cannot reproduce the assignments it was
written from is not a record of anything.

## Flags every runner takes

| Flag | Purpose |
|:-----|:--------|
| `--paper` | The paper slug. Every runner needs it |
| `--root` | The corpus repository, which `pipeline/layers.yaml` resolves paths against. Defaults to where the package ships |
| `--corpus-dir` | Where claim files are read and written (default: `<root>/claims`) |
| `--prompts-dir`, `--prompt-variant` | Override the prompt directory, or select a named variant |
| `--backend`, `--api-key` | `vertex` (default), `anthropic`, or anything litellm routes |
| `--model-{results,caption,structure,reconcile}` | Per-layer model selection |
| `-v`, `--verbose` | Per-chunk DEBUG logging |
