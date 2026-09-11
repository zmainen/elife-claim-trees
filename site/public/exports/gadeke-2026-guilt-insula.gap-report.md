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

## Questions synthesized

MIRA requires every Claim to address a `mira:Question`; a claim tree has no such node. **9 questions were derived mechanically from hypothesis text and need human review.**

- Is it the case that the happiness cost observed in the Social condition is general agency aversion — the unpleasantness of being the decision-maker as such — and is not contingent on responsibility for a negative outcome befalling the partner?
- Is it the case that the happiness decrease following negative partner outcomes under participant choice is driven by the participant's own lottery outcome rather than by the partner's, and so reflects self-directed disappointment rather than interpersonal guilt?
- Is it the case that the imaging pipeline and condition contrasts do not recover established effects, so differences reported between Social and Partner conditions cannot be attributed to the experimental manipulation?
- Is it the case that the model-based fMRI approach does not recover known neural signals, so parametric modulators derived from the computational model — including the partner reward prediction error regressors — cannot be trusted?
- Is it the case that participants did not engage with the lottery task in a value-sensitive way — choices were inattentive or random — so the behavioural measures carry no information about preference or affect?
- Is it the case that the happiness and choice differences between Social and Partner conditions reflect a social-context-driven shift in risk attitude — participants become more or less risk averse when choosing on another person's behalf — rather than responsibility-contingent interpersonal guilt?
- Is it the case that anterior insula is the neural substrate of interpersonal guilt: when a participant bears responsibility for a choice that yields a negative outcome for another person, anterior insula activity tracks the resulting responsibility-contingent affect?
- Is it the case that momentary happiness in social decision contexts is governed by a computational rule in which partner reward prediction errors that arise from the participant's own choices (social_pRPEs) carry an independent, non-zero weight, distinct from the weight on partner RPEs that arise without participant agency?
- Is it the case that superior temporal sulcus (STS) — a core mentalizing-network region — represents the partner's affective experience specifically when the participant is responsible for the partner's outcome?

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
