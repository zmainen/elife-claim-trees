# MIRA export — what the strict file cannot carry

**Paper:** `gadeke-2026-guilt-insula` · **Claims registered:** 2026-03-30 – 2026-09-10

33 claims, 93 typed relations between them.

## Claims by role

- **empirical** — 11
- **hypothesis** — 9
- **control** — 5
- **prediction** — 4
- **scope** — 2
- **interpretation** — 1
- **literature-context** — 1

## Relations dropped

**51 of 93 relations (55%) have no MIRA predicate and are absent from the strict export.**

| Relation | Dropped | What is lost |
|---|---:|---|
| `scopes` | 29 | a scope constraint governs another claim's validity |
| `derived-from` | 5 | a prediction derived from its hypothesis (inverse of entails) |
| `entails` | 5 | a hypothesis entails its prediction — the deductive step |
| `interprets` | 5 | one claim interprets another |
| `requires` | 4 | a claim depends on another holding |
| `enables-method` | 2 | a result makes a downstream method possible |
| `qualifies` | 1 | a claim narrows another's applicability |

The `entails` / `derived-from` pair is the most consequential: together they are the paper's deductive spine. Without them a reader cannot tell which prediction belongs to which hypothesis.

## Relations flattened

`tests`, `confirms`, `validates`, `extends` and `replicates` all become `mira:supports`; `contradicts`, `rules-out` and `dissociates-with` all become `mira:opposes`. Both directions of collapse lose real distinctions — most sharply, evidence *designed* to test a prediction becomes indistinguishable from evidence that merely agrees with it after the fact.

## Verification records dropped

**34 verification records across 19 claims are absent from the strict export.** MIRA has no node type for the fact that a claim was independently checked, by what code, against what data, with what result. They are carried in the extended file as `haak:VerificationRecord`.

## Questions stated by the paper

**3 question(s) are stated on the paper** (in `index.md`) and answered by the hypotheses and rejected alternatives that `addresses` them. These are emitted as real `mira:Question` nodes, not derived.

- Does the anterior insula encode interpersonal guilt — the responsibility-contingent affect that arises specifically when a participant's own choice causes a negative outcome for their partner, as distinct from empathy for partner loss or regret over one's own loss?
- Is momentary happiness during social decisions under risk governed by a responsibility-weighted rule in which partner reward prediction errors caused by the participant's own choice carry an independent, non-zero weight — so that the larger happiness drop after low partner outcomes when the participant chose reflects interpersonal guilt rather than another cause?
- Does the superior temporal sulcus represent the partner's affective state — tracking partner reward prediction errors — specifically when the participant is responsible for the partner's outcome?

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
