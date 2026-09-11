# Measuring a prompt change

`evaluate` is the one subcommand that is not a layer, and it is outside the graph deliberately.
It re-runs the chain into a temporary tree and scores the result against the committed claim
files, so its subject is the prompt set rather than any paper, and it produces nothing another
layer consumes. There is no version of a paper here to be current or stale.

```bash
elife-extract evaluate --reference-dir ../claims/ --work-dir /tmp/eval --all
elife-extract evaluate --reference-dir ../claims/ --work-dir /tmp/eval --paper kammer-2026-foveal-feedback
elife-extract evaluate --reference-dir ../claims/ --work-dir /tmp/eval --papers a,b,c
```

| Flag | Purpose |
|:-----|:--------|
| `--reference-dir` | The corpus to score against — normally `claims/` |
| `--work-dir` | Where the temp extraction and the scorecards go |
| `--paper` / `--papers` / `--all` | Which papers |
| `--no-external-review` | Score the chain without the Opus pass |
| `--skip-existing` | Reuse scorecards already under `--work-dir`, so a sweep is resumable |

## The round-trip

For each paper: read the reference `index.md` for the DOI, run prepare → the three readers →
reconcile → optionally external-review → write into the temp tree, then align the fresh claims
against the committed ones and score.

The alignment is the part that needs explaining. Two claim sets about the same paper will not
share wording, so the matcher is itself a model call: it pairs claims by content and reports
each pair as exact or partial. That means **the scores are measured by the same kind of system
being measured**, which is a real limitation and the reason recovery is the metric to trust —
it asks whether a reference claim was found at all, which is the least model-dependent judgement
in the set.

Four numbers come out:

| Metric | What it asks | Threshold |
|:-------|:-------------|----------:|
| **Claim recovery** | Does every reference claim have a corresponding extraction? | ≥ 80% |
| **Role agreement** | Do the two agree on what the claim is doing in the argument? | ≥ 75% |
| **Panel agreement** | Do they anchor it to the same panel? | ≥ 90% |
| Match quality | Exact versus partial content pairing | — |

Per-paper scorecards land at `<work-dir>/<paper>/scorecard.json`, and an aggregate at
`<work-dir>/aggregate-scorecard.md`.

## What the sweep found

These are measurements of a run, not counts of the corpus, so they are written down here rather
than generated — with the date and configuration that produced them, because that is what makes
a measurement readable later.

**Sweep of 2026-05-11.** Three Sonnet 4.6 readers, Opus 4.6 reconciler, Opus 4.6 external
reviewer on the seven-bias prompt, against the ten public eLife papers.

| Metric | Mean | Median | Threshold | |
|:-------|-----:|-------:|----------:|:--|
| **Claim recovery** | **96.9%** | 100.0% | ≥ 80% | pass |
| **Role classification** | **83.1%** | 84.3% | ≥ 75% | pass |
| Panel assignment | 60.9% | 58.6% | ≥ 90% | fail |

Recovery passes by a wide margin and its median is 100% — on half the corpus, every reference
claim has a corresponding extraction, and the worst paper still reaches 87%.

This ran when external review was `--review-mode external` rather than a layer. The chain it
measured is unchanged, so the numbers still describe what runs today; what changed is that the
reviewer prompt is now a hashed input, so a sweep and the corpus it scores can no longer
silently disagree about which prompt produced them.

### Panel agreement is the standing failure

It is also the one whose failure is least what it looks like. The Caption-reader extracts one
claim per panel. The curator often anchors one claim to several — `panel: fig4, fig5`. When the
matcher pairs a single-panel extraction against a multi-panel reference it scores a panel
mismatch even where the content is identical.

So the CLI is not putting claims at the wrong panel. The disagreement is about granularity, and
the metric cannot see the difference. Two prompt changes would lift it — instructing the
Caption-reader to preserve multi-panel anchors where the caption spans panels, or instructing
the reconciler to consolidate per-panel emissions that share content — and neither has been
tried, because both are testable here first and neither has been.

### Three papers lag on role, for three different reasons

| Paper | Role | What is hard about it |
|:------|-----:|:----------------------|
| kammer (foveal feedback) | 57% | Heavy `control` usage the reviewer prompt did not recognise |
| rozak (neurovascular DL) | 65% | A methods paper, where prompts calibrated on biology findings fit badly |
| scheller (self-prioritization) | 70% | `interpretation` versus `synthesis` is judgment-heavy in cognitive papers |

These are not one problem with three instances. Only the first is a prompt bug.

## The iteration discipline

This is what the tool is for. Change one thing, re-run, diff the aggregate, decide — so that a
prompt revision is a measurement rather than an impression.

The worked example is kammer. Role agreement sat at 57%, the lowest in the corpus, and the
scorecard said why: claims the reference marked `control` were coming back as `empirical`. One
addition to the external-reviewer prompt, teaching it to recognise implicit controls, moved
kammer from **57% to 71%** — and, re-run across the corpus, moved the aggregate role mean from
78.1% to 83.1% without costing anything on recovery.

Two things in that are worth keeping:

The change was **targeted at a diagnosis**, not at the number. The scorecard named a role
confusion on a specific paper; the prompt edit addressed that confusion. Editing prompts until
an aggregate rises is how you fit the prompt to the reference corpus rather than to the task,
and the corpus is ten papers.

And it was **re-run corpus-wide before being kept**. A change that lifts one paper and costs
three is common, and only visible at the aggregate. 71% is still below the 75% threshold;
kammer was kept as a known miss rather than iterated at until it passed.

## What it cannot tell you

`evaluate` scores agreement between two claim sets. It is silent about anything neither set
contains — you can score 100% agreement on a third of a paper.

That is a different question, and [`coverage`](/elife-claim-trees/docs/layers/) is what asks
it: it takes its denominator from the paper rather than from the claim set. The two are
complementary and neither substitutes for the other. Gädeke's Figure 2 panels C and F — a
failed replication that no claim represented — would have scored perfectly here, because
neither set mentioned them.

## Cost

A full ten-paper sweep with external review is roughly $70 and two to three hours sequentially.
`--skip-existing` makes it resumable, which matters more than it sounds: a sweep that dies on
paper eight should not have to redo the first seven.
