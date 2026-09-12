# MIRA export — what the strict file cannot carry

**Paper:** `headley-2026-inhibitory-rhythms` · **Claims registered:** 2026-03-30 – 2026-09-12

29 claims, 88 typed relations between them.

## Claims by role

- **empirical** — 14
- **prediction** — 6
- **hypothesis** — 5
- **scope** — 2
- **interpretation** — 1
- **literature-context** — 1

## Relations dropped

**47 of 88 relations (53%) have no MIRA predicate and are absent from the strict export.**

| Relation | Dropped | What is lost |
|---|---:|---|
| `requires` | 28 | a claim depends on another holding |
| `derived-from` | 6 | a prediction derived from its hypothesis (inverse of entails) |
| `entails` | 6 | a hypothesis entails its prediction — the deductive step |
| `interprets` | 5 | one claim interprets another |
| `scopes` | 2 | a scope constraint governs another claim's validity |

The `entails` / `derived-from` pair is the most consequential: together they are the paper's deductive spine. Without them a reader cannot tell which prediction belongs to which hypothesis.

## Relations flattened

`tests`, `confirms`, `validates`, `extends` and `replicates` all become `mira:supports`; `contradicts`, `rules-out` and `dissociates-with` all become `mira:opposes`. Both directions of collapse lose real distinctions — most sharply, evidence *designed* to test a prediction becomes indistinguishable from evidence that merely agrees with it after the fact.

## Verification records dropped

**17 verification records across 17 claims are absent from the strict export.** MIRA has no node type for the fact that a claim was independently checked, by what code, against what data, with what result. They are carried in the extended file as `haak:VerificationRecord`.

## Questions synthesized

MIRA requires every Claim to address a `mira:Question`; a claim tree has no such node. **5 questions were derived mechanically from hypothesis text and need human review.**

- Is it the case that distal dendritic inhibition reduces somatic firing by directly raising the action-potential threshold — the same subtractive mechanism as perisomatic inhibition — rather than by suppressing dendritic Ca²⁺ and NMDA spikes?
- Is it the case that perisomatic and distal dendritic inhibition act through a single shared mechanism, so perisomatic inhibition also controls dendritic Ca²⁺ and NMDA spiking, rather than the perisomatic-gamma and distal-beta streams being functionally orthogonal?
- Is it the case that the phase-dependent modulation of dendritic spike probability and action-potential timing by beta and gamma bursts requires a slow buildup or evolving entrainment of an underlying process across many oscillatory cycles?
- Is it the case that perisomatic and distal dendritic inhibition serve distinct computational roles in layer 5 pyramidal neurons: perisomatic inhibition principally regulates somatic action potential generation (gain and threshold of axonal output), while distal dendritic inhibition principally regulates dendritic spike incidence and the temporal coupling of dendritic spikes to somatic APs?
- Is it the case that the optimal frequency of rhythmic inhibition for modulating a given dendritic computation is determined by matching the rhythm's cycle period to the intrinsic timescale of the spike process at the target compartment: fast (gamma) for perisomatic Na+/AP processes, slow (beta) for distal Ca²⁺/NMDA dendritic spike processes?

Override any of these by adding a `question:` field to the hypothesis's frontmatter and re-running the export.

## Stance: claims this paper does not assert

**3 of this paper's claims are not asserted by it.** They are alternative explanations it entertains, rejects, or attributes to others. MIRA has no vocabulary for that distinction: it types a node as `Claim` and says nothing about who stands behind it.

The strict export still carries the `rules-out` edge that eliminated each one, declared under `mira:opposes`, so a MIRA-only reader can see the direction of the argument. What that reader cannot see is that the paper **denies** these propositions — so it will over-read them as assertions. The stance travels in the extended file as `haak:stance`.

- `alt-distal-inhibition-raises-somatic-threshold` — rejects
- `alt-perisomatic-and-distal-share-mechanism` — rejects
- `alt-phase-modulation-requires-buildup` — rejects

## Alternatives materialised as claims

None: every relation in this paper points at a claim the tree asserts.

## Paper-level scopes with no MIRA target

**2 `scopes` relations target `*`** — the claim constrains the paper as a whole rather than another claim. `mira:scopes` has `mira:Claim` as its range and MIRA has no paper-level node to point at, so no edge is emitted and no target is invented. The constraint is real and is not in the strict export.

- `l5-model-single-cell-scope` — scopes the whole paper
- `naturalistic-drive-parameterization` — scopes the whole paper
