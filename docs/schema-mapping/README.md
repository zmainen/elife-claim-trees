# Schema mapping

How a claim tree maps onto each standard it can be expressed in, and what each mapping
costs. One document per target. They are comparisons, not conversions: the conversion code
lives in `scripts/` and `extract/scripts/`, and each document explains what its code does and
what it cannot do.

| Document | Target | What it covers |
|---|---|---|
| [`mira-mapping.md`](mira-mapping.md) | **MIRA** — the discourse-graph schema eLife's article platform reads | node and relation mapping, the 57% of typed relations MIRA has no predicate for, the verification records it has no node type for, and the Questions the export has to synthesise |
| [`oxa-claim-schema.md`](oxa-claim-schema.md) | **OXA** — Curvenote/Stencila/eLife document format | the proposed `Claim` block node: role, panel anchor, typed edges |
| [`cito-mapping.md`](cito-mapping.md) | **CiTO** — Citation Typing Ontology | which of our edge types map to existing CiTO properties, and which need extensions |
| [`claim-relations.ttl`](claim-relations.ttl) | — | the OWL vocabulary for those extensions, defined as CiTO subproperties so standard queries still find them |

## The shape of the comparison

The same finding recurs across all four, which is why they are kept together rather than
folded into one page. Every standard in this ecosystem represents *nodes* better than it
represents *edges*, and none of them represents *verification* at all:

- **OXA** types the document's elements — headings, figures, code — but not the propositions
  those elements argue for.
- **CiTO** types relations richly, but between *papers*, not between claims within one.
- **MIRA** has Claim, Evidence, Question and Study as first-class nodes with an explicit
  epistemic status — a real advance — but two relation predicates, `supports` and `opposes`,
  against the fourteen this corpus uses.
- **None** has a way to record that a claim was independently checked: by what code, against
  what deposited data, with what result beside the published value.

So the proposals that come out of these documents are additive rather than competing. A
relation vocabulary and a verification node could be added to MIRA without changing anything
MIRA already does, and the argument for both is a corpus of 1,096 hand-drawn typed relations
rather than an opinion about what ought to be expressible.

## Keeping them honest

The numbers in `mira-mapping.md` are produced by the exporter, not written by hand:
`python3 scripts/export_mira.py --all` regenerates every file in `exports/`, including a
per-paper gap report, and the output is byte-stable across runs so "run it and diff" is a
real check. If the corpus changes and the document does not, the gap reports will disagree
with it.
