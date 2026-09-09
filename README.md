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

## The claim graph

Claims relate to each other via directed belongings: `supports`, `requires`, `contradicts`, `extends`. The graph is stored as plain text files — no database, no neural network required for the core structure. Each node is a claim file; each edge is a typed relation in the frontmatter. The graph is human-auditable at every level.

## Status

Working prototype. 13 papers (10 eLife + 3 lab), 341 claims, 939 verified references. Public site at https://zmainen.github.io/elife-claim-trees/ (eLife papers only). Full methodology at `docs/method.md`, claim format at `docs/claim-format.md`, cost estimate for 3000-paper scaling at `docs/cost-estimate.md`.

## Producing and exporting a claim tree

The code that produces the corpus is in the repository alongside the corpus it produces.

```bash
# induce a claim tree from a paper (extract -> reconcile -> review -> write)
cd extract && python3 -m elife_extract.cli run --doi 10.7554/eLife.105391 --corpus-dir ../claims

# what does the paper assert that no claim accounts for? (no model calls)
python3 -m elife_extract.cli coverage --doi 10.7554/eLife.105391 \
    --claims-dir ../claims/gadeke-2026-guilt-insula

# export every paper to MIRA JSON-LD, with a gap report per paper
cd .. && python3 scripts/export_mira.py --all
```

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
