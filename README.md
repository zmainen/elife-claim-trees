# elife-claim-trees

Open claim-panel infrastructure for scientific papers. A prototype built in collaboration with eLife.

## What this is

Scientific papers make claims. Those claims are currently embedded in prose, attached to figures that bundle multiple results, and severed from the code and data that produced them. This project builds infrastructure to extract, represent, and link claims at the panel level — where a claim is a single analysis generating a single result, tied directly to the underlying code and data.

The prototype focuses on eLife neuroscience papers, spanning a range of data quality from exemplary to average. The goal is to demonstrate that panel-level claim extraction is tractable, auditable, and useful — and to build the open infrastructure for doing it at scale.

## The claim unit

A paper contains approximately 10–20 claims. Each claim is:

- A single declarative sentence stating what was shown
- A panel — one figure panel or analysis block — that generated the result
- A data source (raw or processed)
- An analysis script that transforms data into the result
- A set of upstream claims it depends on (e.g. a calibration result that the main finding requires)

This maps to the `ms_mat` format: a structured text file per claim, human-readable, machine-parseable, version-controllable.

Kenneth's formulation from our initial meeting: **the unit of publication is not a figure or a statistic — it is a computer program**. A claim is a computation: inputs (data, parameters), transformation (analysis code), output (result). A paper that cannot express its claims in this form is making assertions that cannot be independently verified.

## Why panel-level

Figures are too coarse: a single figure panel contains multiple sub-results, and the figure caption conflates them. Statistics are too granular: a p-value has no interpretive context on its own. The panel — one analysis producing one result — is the natural unit of reproducible science.

Existing claim-extraction approaches tend toward either sentence-level NLP (too granular, loses causal structure) or paper-level labeling (too coarse, misses the verification problem). Panel-level is the level at which reproducibility actually operates.

## No human checks this corpus

**Every claim here was produced by a language model, and no person has verified any of it.**
The claims are found by three model calls and reconciled by a fourth; the relations between
them are inferred by a fifth; the review gate the methodology specifies is passed either by
another model or not at all. The `agent:` field on a verification record names the agent that
ran the script, not a person who checked the result.

Read this as a draft annotation layer, not as adjudicated output. A human-review step is
compatible with the format and is **not implemented**. See
[`docs/method.md`](docs/method.md) § 3 for exactly which steps are model calls.

## The claim graph

Claims relate to each other via directed belongings: `supports`, `requires`, `contradicts`, `extends`. The graph is stored as plain text files — no database, no neural network required for the core structure. Each node is a claim file; each edge is a typed relation in the frontmatter. The graph is human-auditable at every level.

## Status

Working prototype. The published corpus is **10 eLife papers, 254 claims (wholes; parts are
counted separately), 919 typed relations**; two further claim trees are versions of one
bioRxiv preprint, kept as method
examples and never folded into the corpus totals. Public site at
https://zmainen.github.io/elife-claim-trees/ (eLife papers only).

Figures on the site are generated — `scripts/corpus_facts.py` counts the claim files and the
pages substitute `{{token}}`, so a number in prose cannot drift from the corpus because it is
not in the prose. This README is not built that way, so treat it as the one place a count can
go stale; `python3 scripts/corpus_facts.py --print` is authoritative.

Full methodology at `docs/method.md`, claim format at `docs/claim-format.md`, cost estimate
for 3000-paper scaling at `docs/cost-estimate.md`.

## Producing and exporting a claim tree

The code that produces the corpus is in the repository alongside the corpus it produces.

A layer is run by `scripts/pipeline.py`, which walks the declaration in
`pipeline/layers.yaml` to find what the layer you asked for still needs, runs each one, and
records every run in `runs/<paper>/ledger.jsonl` with the content hash of what it read. Run
the layers by hand and nothing records it; there is no second path that produces the corpus.

```bash
# induce a claim tree, running whatever it still needs first
python3 scripts/pipeline.py run gadeke-2026-guilt-insula claim-tree

# what would that do? — the commands, in dependency order, running none of them
python3 scripts/pipeline.py run gadeke-2026-guilt-insula claim-tree --dry-run

# what does the paper assert that no claim accounts for? (no model calls)
python3 scripts/pipeline.py run gadeke-2026-guilt-insula coverage

# record that a person read a version and approved it
python3 scripts/pipeline.py approve gadeke-2026-guilt-insula claim-tree --by "your name"

# where every paper stands against every layer
python3 scripts/pipeline.py state

# export every paper to MIRA JSON-LD, with a gap report per paper
python3 scripts/export_mira.py --all
```

`mappings/` holds the adjudicated coverage verdicts per paper. The mechanical match answers
"does a claim restate this statistic or name this panel", which is a proxy for the question
that matters and wrong in both directions; the residue is judged once and stored, so it can
be audited rather than silently recomputed. For Gädeke: 245 spans, 78 carrying a result, 64
accounted for, 15 asserting nothing, 14 real gaps, nothing unexamined.

`exports/` holds the result for every paper: a strict `.mira.jsonld`, an
`.mira-extended.jsonld` carrying what MIRA has no vocabulary for, and a `.gap-report.md`
saying exactly what the strict file dropped. The export is byte-stable, so regenerating it
and diffing is a real check. What each standard can and cannot represent is documented in
[`docs/schema-mapping/`](docs/schema-mapping/README.md).

## Running the site locally

```bash
cd site
npm install
npm run dev          # eLife papers only (public)
npm run dev:all      # all papers including private lab papers
```

### Sharing a review build

To produce a portable static build (no dev environment needed to view):

```bash
cd site
npm run build:share
# dist/ is now a self-contained static site
# Zip and send, or serve locally:
cd dist
python3 -m http.server 8000
# Open http://localhost:8000
```

See `site/SHARE-README.md` for reviewer instructions.

## Collaboration

- Zach Mainen — Mainen Lab, Champalimaud Research, Lisbon
- Tim Behrens — Oxford
- Damian Pattinson, Andy Collings — eLife

## Related work

- Shadow Scientific Ecosystem paper (preprint forthcoming) — the theoretical argument for open, adversarial, panel-level claim infrastructure
- [Library Theorem (arXiv:2603.21272)](https://arxiv.org/abs/2603.21272) — formal grounding for the claim graph structure
- Leo Pucter's group — complementary open approach at finer claim granularity
