# Runs — recorded runs of the pipeline

What each layer read and produced, per paper: the run ledger, and where a model answered, the
prompt it was given and the raw output it returned.

**This is not the provenance of the committed claim files.** For Gädeke, the one paper with a
full agent trace, the claim files were first committed 2026-03-30 and the trace on 2026-09-10
— five months later, 47 drafted claims against 33 committed ones, and no committed claim has
so much as a 0.80 textual match anywhere in the trace. It is a recorded run of the pipeline on
that paper, which is a worked example of what the agents do. How the committed tree was
actually produced is not recorded anywhere and cannot be recovered.

A verdict whose prompt and output are not both recorded cannot be reproduced or disputed. That
had already gone wrong once — the coverage verdicts in `mappings/` were produced by a prompt
written ad hoc during the run and never committed, so for a day the corpus carried judgements
nobody could regenerate.

## Layout

    runs/<paper-slug>/
      manifest.json                     which prompt, which model, which output, with hashes
      results-reader.output.json        raw output, one file per agent
      caption-reader.output.json
      structure-reader.output.json
      reconciler.output.json
      edge-inference.output.json
      coverage-adjudicator.output.json

The prompts themselves live in `extract/prompts/` and are referenced by path and hash from the
manifest, so a run records *which version* of a prompt produced it. Prompts change; a run does
not.

## Reading a manifest

Each role records `prompt`, `prompt_sha256_12`, `model`, `output` and `output_sha256_12`. If
the hash of a prompt file no longer matches what a run recorded, that run was produced by a
different prompt than the one now in the tree — which is a fact worth seeing rather than
discovering.

Note the `model` field distinguishes the configured backend from an agent that answered the
same prompt outside it. Both happen: the reader agents ran on the pipeline's backend, while
edge inference and coverage adjudication were answered by a reasoning agent when the backend
was unavailable. That difference belongs in the provenance, not in a footnote.

## Coverage

Every paper has a `ledger.jsonl`. Only Gädeke has an agent trace, and that trace is a re-run
rather than the run its claim files came from — so no paper in this corpus has a recorded
provenance for its claim tree, and one has a recorded example of the pipeline producing one.

Most ledger entries are `backfilled: true`, written from artifacts that predate the ledger.
A backfilled entry records that a layer produced something and when, and deliberately records
no inputs: it cannot know what was read, and a guess in the shape of a measurement is what
this directory exists to avoid. `pipeline.py state` reports those cells `unrecorded`, not
`current`.
