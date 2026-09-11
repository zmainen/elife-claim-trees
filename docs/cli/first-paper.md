# One paper end to end

From a DOI to a claim tree with a coverage report. About ten minutes and roughly $7 in model
calls for a paper the size of a typical eLife article.

The whole walkthrough is one command repeated with a different layer name. That is the point:
you name what you want, and the runner works out what it still needs.

## Before you start

[Install and configure](/elife-claim-trees/docs/install/) the package, and check that
`pipeline.py` can read the declaration:

```bash
python3 scripts/pipeline.py graph | head -5
```

This walkthrough uses Gädeke 2026 (`10.7554/eLife.105391`), the corpus's worked example — the
one paper with a full agent trace, a coverage adjudication and a marked document.

## 1. Look before you run

```bash
python3 scripts/pipeline.py run gadeke-2026-guilt-insula claim-tree --dry-run
```

Prints the chain in dependency order and runs none of it. On a paper that has never been
through the pipeline you get eight commands; on one whose tree is already current you get one,
because the walk prunes at ancestors that are already satisfied rather than rebuilding a
subtree nothing is waiting for.

Read that list before spending anything. It is the same list the
[pipeline page](/elife-claim-trees/pipeline/) draws as a graph, because both read
`pipeline/layers.yaml`.

## 2. A paper the corpus does not have yet

The runner takes a paper's DOI from `claims/<paper>/index.md`, which a new paper does not have
until `claim-tree` has written it. So seed the first layer by hand, once:

```bash
cd extract
python3 -m elife_extract.cli prepare --paper <your-slug> --doi 10.7554/eLife.<id>
cd ..
```

That writes `runs/<your-slug>/prepared.json` — the abstract, results, captions and methods the
readers will each get, sliced from the JATS. Check the slice sizes it reports. If `results` is
a few hundred characters, the section-header detection failed and everything downstream will be
reading the wrong text; that is the moment to notice, not after three model calls.

Add the slug to `corpus.yaml` so `pipeline.py` will act on it.

## 3. Run the tree

```bash
python3 scripts/pipeline.py run gadeke-2026-guilt-insula claim-tree \
  --note "first pass, default prompts"
```

Each layer runs in turn, and each appends a record to `runs/<paper>/ledger.jsonl` naming every
input by path and content hash. `--note` is the changelog line for those records; it is the
only part of a run record a person writes, so make it say why rather than what.

What happens, in order:

1. **`prepare`** — fetch and slice, cached, no model call.
2. **the three readers** — one call each, on their own slice, under their own prompt. None sees
   another's output.
3. **`reconcile`** — one call, aligning the three lists into a draft tagged `high`,
   `contested` or `single-source`.
4. **`external-review`** — one Opus pass recovering the `prediction` and `hypothesis` roles and
   the multi-panel claims the readers under-cover.
5. **`edge-inference`** — the typed relations between claims, the deductive spine.
6. **`claim-tree`** — slugs, UUIDs, the edges from step 5 attached, one file per claim.

`claim-tree` refuses to overwrite a non-empty paper directory. Move or delete it to re-run.

## 4. See where it stands

```bash
python3 scripts/pipeline.py state
```

Your paper now has a row. A cell is `current` when the layer ran and every input still hashes
to what that run recorded. Edit a prompt and watch the cells that depended on it turn `stale` —
that is the mechanism working, and it is the reason the prompts are declared inputs.

## 5. Check the references

```bash
python3 scripts/pipeline.py run <slug> reference-check
```

Confirms the paper's own DOI and every cited DOI against CrossRef. This is the
anti-hallucination check: a literature-context claim whose DOI resolves to a different paper
than the one it names is the failure mode that matters most, because it is the one a reader
would never catch.

## 6. Ask what the tree missed

Everything so far checks the claims. Nothing yet has asked the opposite question: what does the
paper assert that no claim represents?

```bash
python3 scripts/pipeline.py run <slug> coverage
```

No model calls, so it is free. It builds the paper's own inventories — every panel, every
table, every reported statistic — then cuts the whole text into one-sentence spans and asks of
each whether a claim accounts for it.

The first run reports more gaps than are real, because a mechanical match asks "does a claim
restate this statistic or name this panel", which is a proxy for the question that matters and
wrong in both directions. Adjudicate the residue once and store it:

```bash
elife-extract coverage --paper <slug> --mapping ../mappings/<slug>.json
```

For Gädeke: 245 spans, 78 carrying a result, 64 accounted for, 15 asserting nothing, **14 real
gaps**, nothing unexamined. Two of those were Figure 2's panels C and F — a failed replication
of a risk-aversion effect that sat unrepresented in the tree while every check in the pipeline
ran green, because every check ran over the claims rather than over the paper.

`--fail-on-orphans` makes it a gate.

## 7. Put the verdicts back in the document

```bash
python3 scripts/pipeline.py run <slug> marks
```

Renders the paper with a mark on every span a claim accounts for, carrying that claim's UUID.
Spans that state no result say so; spans carrying a result that no claim states are marked as
gaps. The marks are read straight back after writing, and a mismatch is an error — a document
that cannot reproduce the assignments it was written from is not a record of anything.

## 8. Record that you read it

```bash
python3 scripts/pipeline.py approve <slug> claim-tree --by "your name" \
  --note "roles checked against figures 2-4; two interpretation claims reclassified"
```

Nothing in the pipeline requires this and nothing blocks on it. The approval names the version
it was granted to, so when `claim-tree` runs again it visibly stops applying rather than
carrying forward to text you never saw.

`runs/<paper>/approvals.jsonl` is empty for every cell in this corpus. If you run the
walkthrough and stop at step 7, it stays that way, and the site will say so.

## What you have

```
runs/<slug>/
  prepared.json                  the text the readers read
  results-reader.output.json     one file per reader
  caption-reader.output.json
  structure-reader.output.json
  reconciler.output.json         the draft
  external-review.output.json    the revised draft
  edge-inference.output.json     the typed relations
  reference-check.output.json    what each citation resolved to
  ledger.jsonl                   every run, with hashes
  approvals.jsonl                who read what — if anyone did
claims/<slug>/
  index.md                       paper metadata and the claim listing
  <claim-slug>.md                one file per claim
coverage/<slug>.json             what no claim accounts for
marked/<slug>.marked.md          the paper with the verdicts in it
```

Every one of those paths is declared in `pipeline/layers.yaml`. That is what lets the ledger
hash what a run produced rather than take its existence on trust.
