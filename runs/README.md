# Runs — the prompts and model output behind the corpus

Every claim in this repository was written by a language model. This directory is what makes
that checkable rather than merely disclosed: for each paper, the prompt given to each agent
and the raw output it returned.

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

Gädeke only, so far. The other nine papers were extracted before runs were recorded, so their
agent-level history does not exist and would have to be regenerated. Until then this directory
is honest about covering one paper rather than implying ten.
