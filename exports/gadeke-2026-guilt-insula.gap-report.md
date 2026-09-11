# MIRA export — what the strict file cannot carry

**Paper:** `gadeke-2026-guilt-insula` · **Claims registered:** 2026-09-10 – 2026-09-11

74 claims, 91 typed relations between them.

## Claims by role

- **empirical** — 23
- **methodological** — 12
- **control** — 11
- **hypothesis** — 10
- **prediction** — 5
- **interpretation** — 4
- **scope** — 4
- **literature-context** — 3
- **synthesis** — 2

## Relations dropped

**59 of 91 relations (65%) have no MIRA predicate and are absent from the strict export.**

| Relation | Dropped | What is lost |
|---|---:|---|
| `requires` | 24 | a claim depends on another holding |
| `part-of` | 10 | a component of another claim — one comparison, condition, measure or study of a proposition the target states whole; the target is weakened but not falsified by the source alone |
| `scopes` | 10 | a scope constraint governs another claim's validity |
| `derived-from` | 5 | a prediction derived from its hypothesis (inverse of entails) |
| `entails` | 5 | a hypothesis entails its prediction — the deductive step |
| `interprets` | 4 | one claim interprets another |
| `enables-method` | 1 | a result makes a downstream method possible |

The `entails` / `derived-from` pair is the most consequential: together they are the paper's deductive spine. Without them a reader cannot tell which prediction belongs to which hypothesis.

## Relations flattened

`tests`, `confirms`, `validates`, `extends` and `replicates` all become `mira:supports`; `contradicts`, `rules-out` and `dissociates-with` all become `mira:opposes`. Both directions of collapse lose real distinctions — most sharply, evidence *designed* to test a prediction becomes indistinguishable from evidence that merely agrees with it after the fact.

## Verification records dropped

**34 verification records across 19 claims are absent from the strict export.** MIRA has no node type for the fact that a claim was independently checked, by what code, against what data, with what result. They are carried in the extended file as `haak:VerificationRecord`.

## Questions stated by the paper

**3 question(s) are stated on the paper** (in `index.md`) and answered by the hypotheses and rejected alternatives that `addresses` them. These are emitted as real `mira:Question` nodes, not derived.

- Does the larger decrease in momentary happiness after a low outcome for the partner when the participant made the choice reflect responsibility-contingent interpersonal guilt, rather than general agency aversion, disappointment over the participant's own outcome, a social shift in risk attitude, or inattentive task engagement?
- Is the anterior insula, together with its condition- and choice-dependent connectivity to prefrontal cortex, the neural substrate of this interpersonal guilt, responding more when the participant is responsible for a partner's low outcome?
- Does a neural substrate track the participant's responsibility for the partner's outcomes, representing partner reward prediction errors more strongly when they arise from the participant's own choice than from the partner's choice?

## Questions synthesized

MIRA requires every Claim to address a `mira:Question`; a claim tree has no such node. **0 questions were derived mechanically from hypothesis text and need human review.**


Override any of these by adding a `question:` field to the hypothesis's frontmatter and re-running the export.

## Stance: claims this paper does not assert

**6 of this paper's claims are not asserted by it.** They are alternative explanations it entertains, rejects, or attributes to others. MIRA has no vocabulary for that distinction: it types a node as `Claim` and says nothing about who stands behind it.

The strict export still carries the `rules-out` edge that eliminated each one, declared under `mira:opposes`, so a MIRA-only reader can see the direction of the argument. What that reader cannot see is that the paper **denies** these propositions — so it will over-read them as assertions. The stance travels in the extended file as `haak:stance`.

- `alt-agency-aversion-not-guilt` — rejects
- `alt-guilt-effect-driven-by-own-outcome` — rejects
- `alt-imaging-contrast-invalid` — rejects
- `alt-model-based-glm-invalid` — rejects
- `alt-participants-insensitive-to-value` — rejects
- `alt-social-context-shifts-risk-attitude` — rejects

## Alternatives materialised as claims

None: every relation in this paper points at a claim the tree asserts.

## Paper-level scopes with no MIRA target

None.
