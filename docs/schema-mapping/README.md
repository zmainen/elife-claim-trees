# Schema mapping

How a claim tree maps onto each standard it can be expressed in, and what each mapping
costs. One document per target. They are comparisons, not conversions: the conversion code
lives in `scripts/` and `extract/scripts/`, and each document explains what its code does and
what it cannot do.

| Document | Target | What it covers |
|---|---|---|
| [`mira-guide.md`](mira-guide.md) | **MIRA** — the discourse-graph schema eLife's platform reads | what the schema actually is, how its data is shaped, how we convert, how to validate, and what is still wrong |
| [`oxa-claim-schema.md`](oxa-claim-schema.md) | **OXA** — Curvenote/Stencila/eLife document format | the proposed `Claim` block node: role, panel anchor, typed edges |
| [`cito-mapping.md`](cito-mapping.md) | **CiTO** — Citation Typing Ontology | which of our edge types map to existing CiTO properties, and which need extensions |
| [`claim-relations.ttl`](claim-relations.ttl) | — | the OWL vocabulary for those extensions, defined as CiTO subproperties so standard queries still find them |

## The shape of the comparison

Every standard here represents *nodes* better than it represents *edges*, and none of them
represents *verification* at all:

- **OXA** types the document's elements — headings, figures, code — but not the propositions
  those elements argue for.
- **CiTO** types relations richly, but between *papers*, not between claims within one.
- **MIRA** has Claim, Evidence, Question and Study as first-class nodes with an explicit
  epistemic status, and — contrary to what this file said for a week — its relation
  vocabulary is *extensible*: `AbstractRelationDef` lets a relation MIRA does not name be
  declared rather than dropped or flattened. What it does not have is any way to say a claim
  was independently recomputed.
- **None** has a node for verification: which code, which deposited data, which commit, the
  reproduced value beside the published one.

So the proposal that comes out of these is additive rather than competing: a `Verification`
node, motivated by a corpus rather than by an opinion about what ought to be expressible.

## A correction worth keeping

This directory previously argued that MIRA drops 57% of what a claim tree holds. That was a
fact about our exporter, not about MIRA, and it came from reading our own mapping table
instead of the schema. The number is now zero. The real gap is narrower, and different in
kind: our export uses inline predicates where MIRA reifies relations as nodes, so it does not
validate. `mira-guide.md` records what the schema actually requires, with the source quoted.
