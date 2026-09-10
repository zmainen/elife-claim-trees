# MIRA export — what the strict file cannot carry

**Paper:** `rozak-2026-neurovascular-dl` · **Generated:** 2026-09-10

23 claims, 130 typed relations between them.

## Claims by role

- **empirical** — 8
- **control** — 4
- **scope** — 4
- **hypothesis** — 2
- **methodological** — 2
- **prediction** — 2
- **synthesis** — 1

## Relations dropped

**69 of 130 relations (53%) have no MIRA predicate and are absent from the strict export.**

| Relation | Dropped | What is lost |
|---|---:|---|
| `scopes` | 42 | a scope constraint governs another claim's validity |
| `requires` | 10 | a claim depends on another holding |
| `enables-method` | 9 | a result makes a downstream method possible |
| `derived-from` | 4 | prediction derived from its hypothesis (inverse of entails) |
| `entails` | 4 | hypothesis entails its prediction — the deductive step |

The `entails` / `derived-from` pair is the most consequential: together they are the paper's deductive spine. Without them a reader cannot tell which prediction belongs to which hypothesis.

## Relations flattened

`tests`, `confirms`, `validates`, `extends` and `replicates` all become `mira:supports`; `contradicts`, `rules-out` and `dissociates-with` all become `mira:opposes`. Both directions of collapse lose real distinctions — most sharply, evidence *designed* to test a prediction becomes indistinguishable from evidence that merely agrees with it after the fact.

## Verification records dropped

**19 verification records across 19 claims are absent from the strict export.** MIRA has no node type for the fact that a claim was independently checked, by what code, against what data, with what result. They are carried in the extended file as `haak:VerificationRecord`.

## Questions synthesized

MIRA requires every Claim to address a `mira:Question`; a claim tree has no such node. **2 questions were derived mechanically from hypothesis text and need human review.**

- Is it the case that a deep-learning segmentation pipeline (UNet/UNETR ensemble) coupled with cross-time-point registration, vertex-wise radius estimation, and graph-theoretic network analysis can produce reliable, automated, network-level measurements of neurovascular coupling in volumetric two-photon fluorescence microscopy of cerebral microcirculation — measurements that prior point-measurement and manual-segmentation approaches could not yield at the scale of hundreds of interconnected vessels per FOV?
- Is it the case that optogenetic activation of cortical pyramidal neurons elicits coordinated, network-level vascular responses that cannot be predicted from individual-vessel measurements alone: dilations and constrictions are spatially organised relative to active neurons, capillary responses correlate with their network neighbours' responses, and overall capillary network efficiency is modulated by stimulation?

Override any of these by adding a `question:` field to the hypothesis's frontmatter and re-running the export.

## Alternatives materialised as claims

None: every relation in this paper points at a claim the tree asserts.

## Paper-level scopes with no MIRA target

None.
