# Gädeke, re-run — 2026-09-11

The extraction chain run end to end on one paper, with every model-answered layer answered by
a Claude Opus 5 subagent rather than by a configured backend, into a side tree. Twice: once
without `external-review`, once with it. The committed corpus was not touched.

This is the first end-to-end run of the chain that exists anywhere in this repository, and
`external-review` had never produced an artifact for any paper before it.

## Why it was run

The trace at `runs/gadeke-2026-guilt-insula/` is not the provenance of the committed claim
tree — the claim files were first committed 2026-03-30 and that trace on 2026-09-10, sharing
no claim text. How the committed trees were produced is not recorded anywhere and cannot be
recovered. So the question this answers is not "how was the corpus made" but the one still
answerable: **what does today's chain produce for a paper the corpus already has, and how does
that compare?**

## What is here

    prompts/      the exact (system, user) each layer sends, as dumped
    answers/      the raw subagent replies, before any validation
    runs/         each layer's output, at the paths layers.yaml declares
    tree-A/       claim files built from the reconciled draft — no external review
    tree-B/       claim files built from the reviewed draft — the full declared chain
    pairs.py      emit two claim sets for a matcher, and score a returned alignment
    match-*.pairs.json   the alignment a matcher subagent returned
    compare-data.json    everything above, joined, for the comparison page

The prompts and the raw answers are both kept because neither is evidence on its own: a
verdict whose prompt and output are not both recorded cannot be reproduced or disputed.

## Reproducing it

Every layer now takes `--dump-prompt` and `--answer`, so this needs no bespoke harness:

```bash
elife-extract results-reader --paper <slug> --root /tmp/side --dump-prompt /tmp/q.txt
# answer /tmp/q.txt anywhere
elife-extract results-reader --paper <slug> --root /tmp/side --answer /tmp/a.json
```

`runs/` here was produced by replaying `answers/` through the CLI that way. It differs from the
hand-driven original in exactly one field across 98 files — `extraction-path`, which the CLI
records as `jats` and the hand path recorded as `pdf`. The CLI is right; the hand path
reproduced the bug fixed in #55.

## What it measured

| | claims | edges | recovery | role | panel |
|:--|--:|--:|--:|--:|--:|
| committed | 33 | — | — | — | — |
| tree A — no review | 75 | 120 | 23/33 = 70% | 74% | 30% |
| tree B — full chain | 97 | 173 | **27/33 = 82%** | **85%** | 30% |

**External review earns its place**: +4 recovered claims and +11pp on role, recovering both
`prediction` claims and the `literature-context` one tree A missed — the roles its prompt
targets. The effect is real but much smaller than the ~65%→~96% the documentation quotes from
the May sweep.

**The six claims neither run recovered are not a pipeline failure.** Five are `alt-*` claims
carrying `stance: rejects` — the rival explanations the paper eliminates. Those are the
`stance` layer's output, and that layer declares no runner, so the extraction chain is not
meant to produce them. Against what the chain can reach, recovery is 27 of 27. The one genuine
miss is `hypothesis-insula-tracks-interpersonal-guilt`, the paper's organising hypothesis.

**The extras are largely real.** 70 claims in tree B have no committed counterpart, and 9 of
them state a span the coverage layer had independently flagged as accounted for by no claim —
two of those verbatim. The curated tree is substantially a subset. Among the extras are
methodological caveats the corpus does not carry at all, e.g.

> The BOLD analysis of computational variables uses regressors whose amplitudes come from the
> happiness model already fitted to the same participants' ratings.

**Panel agreement is 30%**, well under the ~55–61% the documentation reports.

## What to distrust

The alignment is a single matcher subagent making 33 judgements per tree, unreviewed. The same
matcher judged both trees, so **the A-to-B difference is the sound part**; the absolute rates
carry its judgement and have no second opinion behind them. An earlier string-similarity pass
scored recovery at 0% while its own near-miss list paired
`ventral-striatum-tracks-risky-choices` with `bilateral-ventral-striatum-engaged-more`, which
is why the matcher is a model.

The coverage-gap corroboration *is* a string comparison, so the two exact matches are certain
and the partial ones want a reader. The 26 unmatched gaps are not evidence the chain missed
them.

Subagents are not the configured backend, and the documented defaults (`claude-sonnet-4-6`,
`claude-opus-4-6`) were not used — they predate the current model family. This measures a run
of the chain, not the chain as it would run on Vertex.
