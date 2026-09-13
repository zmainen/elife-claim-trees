# MIRA export — what the strict file cannot carry

**Paper:** `gadeke-2026-guilt-insula` · **Claims registered:** 2026-09-10 – 2026-09-13

68 claims, 82 typed relations between them.

## Claims by role

- **empirical** — 23
- **control** — 11
- **hypothesis** — 10
- **methodological** — 7
- **prediction** — 5
- **interpretation** — 4
- **literature-context** — 3
- **scope** — 3
- **synthesis** — 2

## Relations dropped

**34 of 82 relations (41%) have no MIRA predicate and are absent from the strict export.**

| Relation | Dropped | What is lost |
|---|---:|---|
| `requires` | 9 | a claim depends on another holding |
| `derived-from` | 5 | a prediction derived from its hypothesis (inverse of entails) |
| `entails` | 5 | a hypothesis entails its prediction — the deductive step |
| `interprets` | 4 | one claim interprets another |
| `part-of` | 4 | a component of another claim — one comparison, condition, measure or study of a proposition the target states whole; the target is weakened but not falsified by the source alone |
| `enables-method` | 3 | a result makes a downstream method possible |
| `scopes` | 3 | a scope constraint governs another claim's validity |
| `dissociates-with` | 1 | the source and target jointly establish a dissociation — two claims whose difference across a condition, region, population or measure is itself the finding, neither bearing on the other's truth (symmetric) |

The `entails` / `derived-from` pair is the most consequential: together they are the paper's deductive spine. Without them a reader cannot tell which prediction belongs to which hypothesis.

## Relations flattened

`tests`, `confirms`, `validates`, `extends` and `replicates` all become `mira:supports`; `contradicts`, `rules-out` and `in-tension-with` all become `mira:opposes`. Both directions of collapse lose real distinctions — most sharply, evidence *designed* to test a prediction becomes indistinguishable from evidence that merely agrees with it after the fact. `in-tension-with` under `mira:opposes` says more than the relation means: a tension holds between two claims the paper *asserts*, both of which stand, so `mira:opposes` overstates it as one claim standing against the other. `dissociates-with` is no longer flattened here — it is a neutral contrast with no MIRA predicate and is dropped instead (see above).

## Verification records dropped

**34 verification records across 19 claims are absent from the strict export.** MIRA has no node type for the fact that a claim was independently checked, by what code, against what data, with what result. They are carried in the extended file as `cg:VerificationRecord`.

## Questions synthesized

MIRA requires every Claim to address a `mira:Question`; a claim tree has no such node. **10 questions were derived mechanically from hypothesis text and need human review.**

- Is it the case that the happiness cost observed in the Social condition is general agency aversion — the unpleasantness of being the decision-maker as such — and is not contingent on responsibility for a negative outcome befalling the partner?
- Is it the case that the happiness decrease following negative partner outcomes under participant choice is driven by the participant's own lottery outcome rather than by the partner's, and so reflects self-directed disappointment rather than interpersonal guilt?
- Is it the case that the imaging pipeline and condition contrasts do not recover established effects, so differences reported between Social and Partner conditions cannot be attributed to the experimental manipulation?
- Is it the case that the model-based fMRI approach does not recover known neural signals, so parametric modulators derived from the computational model — including the partner reward prediction error regressors — cannot be trusted?
- Is it the case that participants did not engage with the lottery task in a value-sensitive way — choices were inattentive or random — so the behavioural measures carry no information about preference or affect?
- Is it the case that the happiness and choice differences between Social and Partner conditions reflect a social-context-driven shift in risk attitude — participants become more or less risk averse when choosing on another person's behalf — rather than responsibility-contingent interpersonal guilt?
- Is it the case that the anterior insula is the neural substrate of the guilt effect, increasing its BOLD response when participants are responsible for low outcomes affecting their partner?
- Is it the case that functional connectivity between guilt- and responsibility-related outcome-phase regions and prefrontal cortex changes depending on whether participants decide for themselves alone or also for their partner, and on the type of choice (Safe or Risky)?
- Is it the case that a neural substrate tracks the participant's responsibility for the partner's outcomes: within regions sensitive to choice outcomes, the partner's reward prediction errors are represented more strongly when they arise from the participant's own choice than from the partner's choice?
- Is it the case that responsibility for a social choice that yields a low outcome for a partner produces interpersonal guilt, experienced by the decision-maker as a larger decrease in momentary happiness than when the partner made the same choice?

Override any of these by adding a `question:` field to the hypothesis's frontmatter and re-running the export.

## Stance: claims this paper does not assert

**6 of this paper's claims are not asserted by it.** They are alternative explanations it entertains, rejects, or attributes to others. MIRA has no vocabulary for that distinction: it types a node as `Claim` and says nothing about who stands behind it.

The strict export still carries the `rules-out` edge that eliminated each one, declared under `mira:opposes`, so a MIRA-only reader can see the direction of the argument. What that reader cannot see is that the paper **denies** these propositions — so it will over-read them as assertions. The stance travels in the extended file as `cg:stance`.

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
