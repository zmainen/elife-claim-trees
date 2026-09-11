# MIRA export — what the strict file cannot carry

**Paper:** `kammer-2026-foveal-feedback` · **Generated:** 2026-09-11

23 claims, 65 typed relations between them.

## Claims by role

- **empirical** — 6
- **prediction** — 4
- **control** — 3
- **hypothesis** — 3
- **methodological** — 2
- **scope** — 2
- **synthesis** — 2
- **literature-context** — 1

## Relations dropped

**39 of 65 relations (60%) have no MIRA predicate and are absent from the strict export.**

| Relation | Dropped | What is lost |
|---|---:|---|
| `enables-method` | 17 | a result makes a downstream method possible |
| `derived-from` | 9 | a prediction derived from its hypothesis (inverse of entails) |
| `entails` | 4 | a hypothesis entails its prediction — the deductive step |
| `scopes` | 4 | a scope constraint governs another claim's validity |
| `interprets` | 3 | one claim interprets another |
| `requires` | 2 | a claim depends on another holding |

The `entails` / `derived-from` pair is the most consequential: together they are the paper's deductive spine. Without them a reader cannot tell which prediction belongs to which hypothesis.

## Relations flattened

`tests`, `confirms`, `validates`, `extends` and `replicates` all become `mira:supports`; `contradicts`, `rules-out` and `dissociates-with` all become `mira:opposes`. Both directions of collapse lose real distinctions — most sharply, evidence *designed* to test a prediction becomes indistinguishable from evidence that merely agrees with it after the fact.

## Verification records dropped

**15 verification records across 15 claims are absent from the strict export.** MIRA has no node type for the fact that a claim was independently checked, by what code, against what data, with what result. They are carried in the extended file as `haak:VerificationRecord`.

## Questions synthesized

MIRA requires every Claim to address a `mira:Question`; a claim tree has no such node. **3 questions were derived mechanically from hypothesis text and need human review.**

- Is it the case that foveal feedback to early visual cortex carries low-to-mid-level visual feature information (shape) rather than high-level semantic category information about the saccade target, reflecting the representational level appropriate to early visual cortex rather than to ventral object-selective cortex?
- Is it the case that foveal V1 decoding of peripheral saccade targets reflects genuine top-down feedback from higher cortical areas, not passive spillover from large peripheral receptive fields whose tails extend into the foveal representation?
- Is it the case that foveal feedback during saccade preparation uses a representational format shared with bottom-up sensory drive — that is, the population code carrying the predicted peripheral target in foveal V1 lies in the same representational space as the code evoked by direct foveal stimulation by the same image?

Override any of these by adding a `question:` field to the hypothesis's frontmatter and re-running the export.

## Stance: claims this paper does not assert

Every claim in this paper is asserted by it.

## Alternatives materialised as claims

**4 relation targets name something no claim file asserts.** They are alternative explanations the paper argues against, so the target exists only as the thing being excluded. Each is minted as a `mira:Claim` so the edge has a destination, and flagged `haak:materialisedFrom: relation-target` in the extended file. **None of these is an authored claim.**

- FEF as candidate driver of foveal feedback
- LO as candidate driver of foveal feedback
- generic brain-state or arousal explanation of IPS-foveal-decoding coupling
- passive spillover from large peripheral receptive fields

## Paper-level scopes with no MIRA target

None.
