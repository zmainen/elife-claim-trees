# Claim trees → MIRA

MIRA (Modular Interoperable Research Attribution) is the discourse-graph schema eLife's
article platform reads. This document says exactly how a claim tree maps onto it, what
survives the conversion, and what does not — with numbers measured over the whole corpus
rather than estimated.

Everything here is produced by `scripts/export_mira.py`, which writes three files per paper
into `exports/`:

| File | What it is |
|---|---|
| `<slug>.mira.jsonld` | strict MIRA core — only MIRA and schema.org terms, safe for any MIRA reader |
| `<slug>.mira-extended.jsonld` | the same graph plus a `haak:` namespace carrying what MIRA has no vocabulary for |
| `<slug>.gap-report.md` | what the strict file could not carry, and why |

Two files rather than one is a deliberate choice. MIRA can express roughly half of what a
claim tree holds. A single "converted" file either silently drops the rest — leaving a reader
with no way to know something was lost — or emits extension terms that a strict reader
chokes on. Two files keeps both promises: the strict one is honestly strict, the extended one
is honestly lossless, and the gap report makes the difference legible without reading either.

Reproduce all of it with `python3 scripts/export_mira.py --all`. The output is byte-stable
across runs, so "run it and diff" is a real check rather than a figure of speech.

## What maps cleanly

**Nodes.** A claim's `role` decides its MIRA type. This is the mapping, and it is data in
`ROLE_TO_TYPE` rather than logic buried in a function, because every row is a decision
someone should be able to disagree with:

| Claim role | MIRA type |
|---|---|
| `hypothesis`, `prediction`, `interpretation`, `synthesis`, `assessment`, `scope` | `mira:Claim` |
| `empirical`, `control` | `mira:Evidence` |
| `methodological` | `mira:Protocol` |
| `literature-context` | `dg:SourceDocument` |

**Epistemic status.** MIRA carries the hypothesis/established distinction on
`mira:EpistemicStatus` rather than in the node type, so a hypothesis or prediction becomes
`mira:Hypothesis`, a scope constraint or weakly-held claim becomes `mira:Assumption`, and the
rest become `mira:Claim`.

**Observation base.** An Evidence node whose assertion names a dataset gets a `mira:Study`
with that identifier, and the method it followed becomes a `mira:Protocol`.

**Two relation families.** `tests`, `confirms`, `validates`, `supports`, `extends` and
`replicates` all become `mira:supports`. `contradicts`, `opposes`, `dissociates-with` and
`rules-out` all become `mira:opposes`.

## What is flattened

That last row is the first real cost, and it runs in both directions. Evidence *designed in
advance* to test a prediction becomes indistinguishable from evidence that merely agrees with
it after the fact — a distinction that is close to the whole point of pre-registration.
`replicates` and `extends` collapse together, so a direct replication reads the same as a
generalisation to a new condition. On the opposing side, `rules-out` — which asserts that a
result eliminates an alternative — reads the same as `dissociates-with`, which only says two
things came apart.

Nothing is lost from the file, in the sense that the relation still exists and still points
where it pointed. What is lost is the reason it was drawn.

## What is dropped entirely

Seven relations have no MIRA predicate at all and are simply absent from the strict export.
Six of them occur in this corpus (`qualifies` is defined but unused), and across all 13
papers **623 of 1,096 typed relations (57%) fall in this category**:

| Relation | Dropped | What it says |
|---|---:|---|
| `scopes` | 197 | a scope constraint governs another claim's validity |
| `requires` | 178 | a claim depends on another holding |
| `enables-method` | 79 | a result makes a downstream method possible |
| `entails` | 65 | a hypothesis entails its prediction — the deductive step |
| `derived-from` | 62 | a prediction derived from its hypothesis (the inverse) |
| `interprets` | 42 | one claim interprets another |

The `entails` / `derived-from` pair is the most consequential of the six. Together they are
the paper's deductive spine: they are what lets a reader see which prediction belongs to
which hypothesis, and therefore what would have counted as the hypothesis being wrong. A
strict MIRA export of a paper still contains every hypothesis and every prediction, and gives
no way to tell which goes with which.

`scopes` and `requires` are the two largest, and they matter for a quieter reason. A claim
that holds only under a stated condition, exported without that condition, does not read as
narrower than it is — it reads as unconditional. The export makes claims *look stronger* than
the corpus records them.

## What has no node type at all

**Verification records — 225 across the corpus.** MIRA has no way to say that a claim was
independently checked: by what code, at which line, against which deposited file, at which
commit of the authors' repository, with what result beside the published value. This is the
part of the corpus that took the most work to produce and the part MIRA can carry least of.
It survives only in the extended file, as `haak:VerificationRecord`.

For Gädeke that means the entire verification chain — the peak MNI coordinate re-derived from
the authors' deposited contrast map, the logistic regression re-run on their deposited
choice data — is absent from the strict export. What arrives is a claim that says the insula
tracks guilt, with no record that anyone checked.

## What is synthesised, and therefore needs a human

MIRA requires every `mira:Claim` to address a `mira:Question`. A claim tree has no such node:
it records what a paper asserts, not what it asked. The export derives a question mechanically
from each hypothesis — literally "Is it the case that ⟨hypothesis text⟩?" — which produces
something structurally valid and rhetorically wrong. **31 questions were synthesised this
way across the corpus.**

They are flagged as synthesised rather than presented as ours. Override any of them by adding
a `question:` field to the hypothesis's frontmatter and re-running the export.

## How this compares to the formats we proposed

The repo already argues, on the [standards page](../../site/src/pages/standards.astro), that
OXA, CiTO and Discourse Graphs each stop short of representing the individual claims a paper
makes: OXA types the document's *elements*, CiTO types relations between *papers*, and
Discourse Graphs types Claims and Evidence but as a note-taking ontology rather than as
something embedded in a published article.

MIRA is a real advance on all three for this purpose — it has Claim, Evidence, Question and
Study as first-class nodes, and an explicit epistemic status. The gap is narrower and more
specific than the gap in the other three:

| | Claims as nodes | Typed claim→claim relations | Epistemic status | Verification provenance |
|---|:--:|:--:|:--:|:--:|
| OXA | no | no | no | no |
| CiTO | no (papers only) | 40+ types, between documents | no | no |
| Discourse Graphs | yes | few | partial | no |
| MIRA | yes | 2 (`supports`, `opposes`) | yes | no |
| claim trees | yes | 17 | yes | yes |

So the honest summary is not "MIRA cannot represent claim trees". It is that MIRA represents
the *nodes* well and the *edges* thinly, and has no vocabulary for the fact that a claim was
checked. Two of those three are additive rather than contradictory — they could be proposed
as MIRA extensions without changing anything MIRA already does:

1. **A relation vocabulary.** `supports` and `opposes` are a two-value collapse of what CiTO
   already types richly between documents. The six dropped relations, plus the distinctions
   flattened into `supports`, are a concrete proposal with a corpus behind it: 1,096 typed
   relations across 13 papers, drawn by hand, showing which distinctions people actually use.
2. **A verification node.** A `Verification` node pointing at a Claim, carrying code
   location, data identifier, data commit, and reproduced-versus-published values. This is
   what makes a claim graph checkable rather than merely assertable, and it is the piece
   nothing in the ecosystem has.
3. **Question as optional, or derivable.** Requiring a Question per Claim is reasonable for
   graphs built by hand from reading. For graphs induced from a finished paper there is often
   no question in the text to point at, and forcing one manufactures rhetoric.

The gap reports are the evidence for all three, and they are generated, not written — which
means the argument can be re-checked against a changed corpus by re-running one command.
