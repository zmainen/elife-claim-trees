# Stance, and alternative explanations as claims

**Status:** accepted, implemented for Gädeke
**Issue:** [#3](https://github.com/zmainen/elife-claim-trees/issues/3)
**Supersedes nothing. Depends on:** `docs/claim-format.md` §1–2

A claim tree can record what a result supports. It cannot record what a result *rules out*,
because an alternative explanation that nobody asserts has nowhere in the format to be. This
note argues that the fix is one field in the right place, shows why the format's own ontology
picks that place for us, and records what the fix costs.

## The problem, from the corpus

Gädeke has five claims with role `control`. A control exists to eliminate an alternative
explanation; that is what the role means. And each of the five states its target explicitly,
in a closing clause, in the same grammatical position:

| Control | Closing clause | The rival it eliminates |
|---|---|---|
| `risk-premiums-null-social-solo` | "evidence against social-context-driven changes in risk aversion" | the effect is a shift in risk attitude |
| `guilt-effect-independent-of-own-outcome` | "regardless of whether the participant received the high or low outcome" | the effect is about the participant's own loss |
| `lottery-choice-increases-with-ev` | "confirming participants were sensitive to expected value" | participants were not engaged with the task |
| `ventral-striatum-tracks-computational-reward` | "validating the model-based fMRI approach as a manipulation check" | the model-based GLM does not work |
| `ventral-striatum-tracks-risky-choices` | "replicating established striatal responses" | the imaging contrast is invalid |

Plus `agency-reduces-happiness`, which establishes that being the chooser depresses happiness
*independently of outcome*, addressing the sharpest rival of all: that the whole phenomenon is
general agency aversion rather than guilt.

Six rivals, named in prose, none of them a node. The `validates:` edges these controls carry
point at the claim they defend, never at the rival they kill — so the graph records that
`lottery-choice-increases-with-ev` supports the hypothesis, but not *why*: that the behavioural
data means anything at all.

This is not a Gädeke peculiarity. Across the corpus, 39 claims in 11 of 12 papers use
eliminative language and only 5 carry a corresponding edge. Ejdrup enumerates five candidate
mechanisms for a regional dopamine difference and kills four; all four eliminations point into
text, and the immunostaining control that kills the fifth has no incoming edge at all, so the
graph cannot say what it is for.

### The absence does not merely lose information — it manufactures errors

Fifteen `rules-out` relations exist. Eleven target prose, which resolves to nothing. The other
four target real claims, and **all four are wrong** ([#4]). The mechanism is identical in each:
the paper says "this rules out explanation X of finding Y", X has no node, so the edge was
wired to Y — the nearest thing that did.

In Gädeke this produced something worse than a dangling edge. `risk-premiums-null-social-solo`
and `solo-vs-social-choice-difference` are wired as mutually `contradicts`, when in fact one is
about choice frequency and the other about the risk premium implied by those choices; both are
asserted, both are true, and they are compatible. What the extraction meant is that both bear
on the same confound. With no node for the confound, that shared bearing was expressed as the
two claims attacking each other, and **the graph now asserts an internal contradiction in a
paper that has none** ([#5]).

For a claim graph this is the maximally bad failure: a false contradiction is precisely what an
automated reader is built to surface.

### And the loss is argumentative, not just structural

Eliminative arguments carry their warrant in the elimination. "DAT Vmax explains the regional
difference" is only as strong as the enumeration of alternatives is complete — and an
enumeration that lives in prose cannot be audited, disputed, or extended by a later paper. The
part of a paper most exposed to challenge is the part the format currently cannot hold.

## Where the fix belongs

The obvious move is a new `role: alternative`. It is wrong, and the format says why.

`role` classifies a claim's *function in an argument* — hypothesis, prediction, empirical,
control. An alternative explanation is, functionally, a hypothesis. Making "alternative" a role
would conflate what a claim *is* with what a paper *thinks of it*, and would lose the
distinction between a rival the paper invented (Ejdrup's parameter sweep) and one the field
proposed (Kammer's "FEF as candidate driver", which needs a citation).

`docs/claim-format.md` §1 already settles this:

> A claim is an entity — a proposition that exists independently of any particular paper. […]
> Papers make assertions about claims.

If the claim is paper-independent, then "does this paper assert this proposition, or merely
entertain it?" is not a fact about the claim at all. It is a fact about the *assertion* — the
situation of a paper relating to a proposition at a moment in time. The format already models
that situation as a first-class thing with its own fields, one of which (`confidence`) is
already the paper's own epistemic posture.

So the fix is one field on the assertion block. The ontology chose the location; we only have
to name the values.

## The design

**`stance`** on each assertion block. Four values:

| Value | Meaning |
|---|---|
| `asserts` | The paper claims the proposition is true. **Default** — every existing assertion. |
| `entertains` | The paper raises it as a candidate and does not assert it. |
| `rejects` | The paper argues it is false. |
| `attributes` | Someone else asserts it; this paper reports that. Requires a citation. |

A ruled-out alternative is then: a normal claim entity, with an assertion block carrying
`stance: rejects`, and incoming `rules-out` edges from the evidence that did the rejecting.

Three things follow, and they are the reason this shape is worth preferring to the alternatives.

**Stance and edges do different jobs, so keep both.** `stance: rejects` is the paper's
*conclusion*; the incoming `rules-out` edge is its *warrant*. A paper can reject something by
dismissal, with no evidence offered — stance records that, and no edge would. Conversely the
edge says *which* control did the work, which stance cannot.

**The outcome is not a fifth value.** A claim with `stance: entertains` and an incoming
`rules-out` is a rejected alternative. One with `stance: entertains` and no such edge is an
*open* alternative — a rival the paper raised and did not settle. That second case is real,
common, and currently inexpressible; it falls out of this design for free rather than needing
its own vocabulary.

**Stance is per-paper, which is the point.** Today each claim lives in one paper's directory
with one assertion, so stance-on-assertion and stance-on-claim look identical. They come apart
exactly when the corpus does what it is designed to do: when paper B asserts the proposition
paper A rejected, the shared claim entity carries two assertion blocks with opposing stances,
and that disagreement becomes queryable instead of being two unrelated nodes. Putting stance on
the claim would foreclose this.

## Validation that falls out

Once stance exists, three rules become checkable, and each catches a class of error already in
the corpus:

1. **`rules-out` and `contradicts` must not target an assertion with `stance: asserts` from the
   same paper.** A paper does not rule out what it claims. This catches all four miswired
   relations in [#4] and the false Gädeke contradiction in [#5].
2. **A claim must not both support and oppose the same target.** Fourteen pairs currently do
   ([#6]).
3. **`stance: attributes` requires a citation.** Otherwise an attributed rival is
   indistinguishable from an invented one.

Implemented in `scripts/check_relations.py`.

## What MIRA does with it

Nothing, and that is worth stating plainly rather than papering over.

MIRA has `Claim`, `Evidence`, `Question`, `supports` and `opposes`. It has no way to say that a
paper considered a proposition and rejected it. A rejected alternative exported as a plain
`mira:Claim` reads as something this paper asserts — the exact inversion of its meaning.

So: `stance` travels in the extended file as `haak:stance`, the strict export emits the
`rules-out` edge (declared under `mira:opposes`, which gives a MIRA-only reader the direction if
not the posture), and each paper's `gap-report.md` states that a MIRA-only reader will
**over-read these nodes as assertions**. This is the second thing our corpus motivates that
MIRA lacks a vocabulary for, alongside verification, and both are worth putting to the MIRA
authors as questions rather than complaints.

## Migration

Creating an alternative claim means *writing* it — the proposition has to be stated, and no
claim file contains it. That is authorship, done here by an agent from the control claim's own
closing clause, with no human check, exactly as with every other claim in this corpus. The
provenance is recorded and the alternatives are marked so nobody mistakes them for propositions
the paper asserted.

Gädeke first, six alternatives. Ejdrup, Kammer and Meijer hold the remaining known cases. The
39 claims carrying unencoded eliminative language are a re-extraction question, not a migration
one, and stay open under [#3].

## Open questions

- **Does `rejects` need a strength?** "Ruled out decisively" and "argued against weakly" are
  different, and `epistemic` is the natural home — but `epistemic` currently carries two
  vocabularies and never records `contested` ([#8]). Deferred until that is settled.
- **Are validity checks rivals at all?** Two of Gädeke's six — "the GLM does not work", "the
  imaging contrast is invalid" — are preconditions rather than competing explanations of the
  phenomenon. They may want `requires` against an assessment claim (`docs/claim-format.md` §5)
  rather than `rules-out` against an alternative. Implemented here as alternatives, flagged for
  review.
- **Who authors an attributed rival?** `attributes` needs the citation to point somewhere. The
  corpus has a `literature-context` role that may already be the right target.

[#4]: https://github.com/zmainen/elife-claim-trees/issues/4
[#5]: https://github.com/zmainen/elife-claim-trees/issues/5
[#6]: https://github.com/zmainen/elife-claim-trees/issues/6
[#3]: https://github.com/zmainen/elife-claim-trees/issues/3
[#8]: https://github.com/zmainen/elife-claim-trees/issues/8
