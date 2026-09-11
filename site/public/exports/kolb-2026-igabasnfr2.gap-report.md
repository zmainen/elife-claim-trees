# MIRA export — what the strict file cannot carry

**Paper:** `kolb-2026-igabasnfr2` · **Generated:** 2026-09-11

21 claims, 90 typed relations between them.

## Claims by role

- **empirical** — 9
- **hypothesis** — 3
- **methodological** — 3
- **prediction** — 2
- **scope** — 2
- **control** — 1
- **interpretation** — 1

## Relations dropped

**46 of 90 relations (51%) have no MIRA predicate and are absent from the strict export.**

| Relation | Dropped | What is lost |
|---|---:|---|
| `scopes` | 27 | a scope constraint governs another claim's validity |
| `enables-method` | 7 | a result makes a downstream method possible |
| `entails` | 5 | a hypothesis entails its prediction — the deductive step |
| `derived-from` | 3 | a prediction derived from its hypothesis (inverse of entails) |
| `requires` | 3 | a claim depends on another holding |
| `interprets` | 1 | one claim interprets another |

The `entails` / `derived-from` pair is the most consequential: together they are the paper's deductive spine. Without them a reader cannot tell which prediction belongs to which hypothesis.

## Relations flattened

`tests`, `confirms`, `validates`, `extends` and `replicates` all become `mira:supports`; `contradicts`, `rules-out` and `dissociates-with` all become `mira:opposes`. Both directions of collapse lose real distinctions — most sharply, evidence *designed* to test a prediction becomes indistinguishable from evidence that merely agrees with it after the fact.

## Verification records dropped

**16 verification records across 16 claims are absent from the strict export.** MIRA has no node type for the fact that a claim was independently checked, by what code, against what data, with what result. They are carried in the extended file as `haak:VerificationRecord`.

## Questions synthesized

MIRA requires every Claim to address a `mira:Question`; a claim tree has no such node. **3 questions were derived mechanically from hypothesis text and need human review.**

- Is it the case that the fluorescence response attributed to iGABASnFR2 reflects binding of, or interference by, compounds structurally related to GABA rather than GABA itself, so the reported sensitivity is not a measure of GABA detection?
- Is it the case that a GABA sensor with sufficiently improved sensitivity, kinetics, and affinity will cross qualitative capability thresholds — not merely improve signal-to-noise on measurements iGABASnFR1 could already make, but enable measurements that iGABASnFR1 cannot make at all?
- Is it the case that targeted near-saturation mutagenesis at sites in and around the Pf622 GABA-binding pocket and the cpGFP-linker interfaces can yield a successor to iGABASnFR1 with substantially improved sensitivity (ΔF/F), increased on-cell affinity within the physiologically relevant range, faster binding kinetics, and improved expression / membrane trafficking — without sacrificing GABA selectivity?

Override any of these by adding a `question:` field to the hypothesis's frontmatter and re-running the export.

## Stance: claims this paper does not assert

**1 of this paper's claims are not asserted by it.** They are alternative explanations it entertains, rejects, or attributes to others. MIRA has no vocabulary for that distinction: it types a node as `Claim` and says nothing about who stands behind it.

The strict export still carries the `rules-out` edge that eliminated each one, declared under `mira:opposes`, so a MIRA-only reader can see the direction of the argument. What that reader cannot see is that the paper **denies** these propositions — so it will over-read them as assertions. The stance travels in the extended file as `haak:stance`.

- `alt-signal-from-cross-reactivity` — rejects

## Alternatives materialised as claims

None: every relation in this paper points at a claim the tree asserts.

## Paper-level scopes with no MIRA target

None.
