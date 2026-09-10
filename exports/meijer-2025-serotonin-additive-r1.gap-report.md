# MIRA export — what the strict file cannot carry

**Paper:** `meijer-2025-serotonin-additive-r1` · **Generated:** 2026-09-10

41 claims, 84 typed relations between them.

## Claims by role

- **empirical** — 17
- **prediction** — 6
- **literature-context** — 5
- **hypothesis** — 4
- **control** — 3
- **synthesis** — 3
- **scope** — 2
- **methodological** — 1

## Relations dropped

**70 of 84 relations (83%) have no MIRA predicate and are absent from the strict export.**

| Relation | Dropped | What is lost |
|---|---:|---|
| `requires` | 31 | a claim depends on another holding |
| `scopes` | 17 | a scope constraint governs another claim's validity |
| `derived-from` | 9 | prediction derived from its hypothesis (inverse of entails) |
| `entails` | 7 | hypothesis entails its prediction — the deductive step |
| `interprets` | 4 | one claim interprets another |
| `enables-method` | 2 | a result makes a downstream method possible |

The `entails` / `derived-from` pair is the most consequential: together they are the paper's deductive spine. Without them a reader cannot tell which prediction belongs to which hypothesis.

## Relations flattened

`tests`, `confirms`, `validates`, `extends` and `replicates` all become `mira:supports`; `contradicts`, `rules-out` and `dissociates-with` all become `mira:opposes`. Both directions of collapse lose real distinctions — most sharply, evidence *designed* to test a prediction becomes indistinguishable from evidence that merely agrees with it after the fact.

## Verification records dropped

**22 verification records across 22 claims are absent from the strict export.** MIRA has no node type for the fact that a claim was independently checked, by what code, against what data, with what result. They are carried in the extended file as `haak:VerificationRecord`.

## Questions synthesized

MIRA requires every Claim to address a `mira:Question`; a claim tree has no such node. **4 questions were derived mechanically from hypothesis text and need human review.**

- Is it the case that phasic dorsal-raphe serotonin release functions as a surprise / belief-updating signal — therefore, optogenetically driven 5-HT release during a perceptual decision-making task should accelerate the rate at which the animal updates its prior, increase behavioral flexibility, and/or measurably alter the trade-off between sensory evidence and prior expectation in the choice computation?
- Is it the case that optogenetic activation of dorsal-raphe serotonergic neurons modulates downstream single-neuron spiking activity additively rather than multiplicatively — that is, the 5-HT effect on a neuron's firing rate is well approximated by a constant additive offset that is independent of the choice-related component of activity, rather than by a gain factor that scales the choice-related component?
- Is it the case that a neuromodulatory signal can produce strong, brain-wide single-neuron modulation while leaving ongoing task-driven behavior unaffected if the modulation is geometrically confined to a population subspace orthogonal to the readout dimensions used by downstream circuits to extract task variables?
- Is it the case that phasic dorsal-raphe serotonin release drives a rapid switch in internal state in the awake quiescent animal, from an "offline" to a more "online" state, manifest as pupil dilation, suppression of hippocampal sharp wave ripples, and increased exploratory behaviors (whisking, sniffing) at short latency?

Override any of these by adding a `question:` field to the hypothesis's frontmatter and re-running the export.

## Alternatives materialised as claims

**1 relation targets name something no claim file asserts.** They are alternative explanations the paper argues against, so the target exists only as the thing being excluded. Each is minted as a `mira:Claim` so the edge has a destination, and flagged `haak:materialisedFrom: relation-target` in the extended file. **None of these is an authored claim.**

- inhibition-fast-excitation-slow

## Paper-level scopes with no MIRA target

None.
