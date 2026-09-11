# MIRA export — what the strict file cannot carry

**Paper:** `meijer-2025-serotonin-orthogonal` · **Claims registered:** 2026-04-19 – 2026-09-10

25 claims, 63 typed relations between them.

## Claims by role

- **empirical** — 9
- **control** — 4
- **hypothesis** — 4
- **prediction** — 4
- **scope** — 2
- **literature-context** — 1
- **methodological** — 1

## Relations dropped

**39 of 63 relations (62%) have no MIRA predicate and are absent from the strict export.**

| Relation | Dropped | What is lost |
|---|---:|---|
| `requires` | 18 | a claim depends on another holding |
| `scopes` | 10 | a scope constraint governs another claim's validity |
| `derived-from` | 4 | a prediction derived from its hypothesis (inverse of entails) |
| `entails` | 4 | a hypothesis entails its prediction — the deductive step |
| `enables-method` | 2 | a result makes a downstream method possible |
| `interprets` | 1 | one claim interprets another |

The `entails` / `derived-from` pair is the most consequential: together they are the paper's deductive spine. Without them a reader cannot tell which prediction belongs to which hypothesis.

## Relations flattened

`tests`, `confirms`, `validates`, `extends` and `replicates` all become `mira:supports`; `contradicts`, `rules-out` and `dissociates-with` all become `mira:opposes`. Both directions of collapse lose real distinctions — most sharply, evidence *designed* to test a prediction becomes indistinguishable from evidence that merely agrees with it after the fact.

## Verification records dropped

**16 verification records across 16 claims are absent from the strict export.** MIRA has no node type for the fact that a claim was independently checked, by what code, against what data, with what result. They are carried in the extended file as `haak:VerificationRecord`.

## Questions synthesized

MIRA requires every Claim to address a `mira:Question`; a claim tree has no such node. **4 questions were derived mechanically from hypothesis text and need human review.**

- Is it the case that the rapid inhibition observed after dorsal-raphe stimulation is produced by preferential, fast recruitment of fast-spiking inhibitory interneurons, which are engaged by 5-HT more readily than other cell types and impose inhibition at short latency?
- Is it the case that phasic dorsal-raphe serotonin release functions as a surprise / belief-updating signal — therefore, optogenetically driven 5-HT release during a perceptual decision-making task should accelerate the rate at which the animal updates its prior, increase behavioral flexibility, and/or measurably alter the trade-off between sensory evidence and prior expectation in the choice computation?
- Is it the case that a neuromodulatory signal can produce strong, brain-wide single-neuron modulation while leaving ongoing task-driven behavior unaffected if the modulation is geometrically confined to a population subspace orthogonal to the readout dimensions used by downstream circuits to extract task variables (here, the upcoming choice)?
- Is it the case that a phasic burst of serotonin release from the dorsal raphe nucleus drives a rapid switch in internal arousal/behavioral state in the awake quiescent animal — from an "offline" state characterized by low arousal, hippocampal sharp-wave ripples, and minimal exploratory movement, to an "online" state characterized by pupil dilation, ripple suppression, and active exploration (whisking, sniffing)?

Override any of these by adding a `question:` field to the hypothesis's frontmatter and re-running the export.

## Stance: claims this paper does not assert

**1 of this paper's claims are not asserted by it.** They are alternative explanations it entertains, rejects, or attributes to others. MIRA has no vocabulary for that distinction: it types a node as `Claim` and says nothing about who stands behind it.

The strict export still carries the `rules-out` edge that eliminated each one, declared under `mira:opposes`, so a MIRA-only reader can see the direction of the argument. What that reader cannot see is that the paper **denies** these propositions — so it will over-read them as assertions. The stance travels in the extended file as `haak:stance`.

- `alt-rapid-fs-interneuron-recruitment` — rejects

## Alternatives materialised as claims

**1 relation targets name something no claim file asserts.** They are alternative explanations the paper argues against, so the target exists only as the thing being excluded. Each is minted as a `mira:Claim` so the edge has a destination, and flagged `haak:materialisedFrom: relation-target` in the extended file. **None of these is an authored claim.**

- light-or-heat-mediated-modulation

## Paper-level scopes with no MIRA target

None.
