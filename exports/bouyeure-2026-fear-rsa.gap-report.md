# MIRA export — what the strict file cannot carry

**Paper:** `bouyeure-2026-fear-rsa` · **Generated:** 2026-09-09

30 claims, 83 typed relations between them.

## Claims by role

- **empirical** — 15
- **prediction** — 5
- **hypothesis** — 3
- **control** — 2
- **methodological** — 2
- **interpretation** — 1
- **scope** — 1
- **synthesis** — 1

## Relations dropped

**44 of 83 relations (53%) have no MIRA predicate and are absent from the strict export.**

| Relation | Dropped | What is lost |
|---|---:|---|
| `requires` | 13 | a claim depends on another holding |
| `scopes` | 11 | a scope constraint governs another claim's validity |
| `derived-from` | 6 | prediction derived from its hypothesis (inverse of entails) |
| `entails` | 6 | hypothesis entails its prediction — the deductive step |
| `interprets` | 5 | one claim interprets another |
| `enables-method` | 3 | a result makes a downstream method possible |

The `entails` / `derived-from` pair is the most consequential: together they are the paper's deductive spine. Without them a reader cannot tell which prediction belongs to which hypothesis.

## Relations flattened

`tests`, `confirms`, `validates`, `extends` and `replicates` all become `mira:supports`; `contradicts`, `rules-out` and `dissociates-with` all become `mira:opposes`. Both directions of collapse lose real distinctions — most sharply, evidence *designed* to test a prediction becomes indistinguishable from evidence that merely agrees with it after the fact.

## Verification records dropped

**22 verification records across 22 claims are absent from the strict export.** MIRA has no node type for the fact that a claim was independently checked, by what code, against what data, with what result. They are carried in the extended file as `haak:VerificationRecord`.

## Questions synthesized

MIRA requires every Claim to address a `mira:Question`; a claim tree has no such node. **3 questions were derived mechanically from hypothesis text and need human review.**

- Is it the case that prefrontal cortex represents fear-relevant contexts as distinct multivoxel patterns (context-specific coding), and this representational distinctness is the neural substrate that enables context-dependent fear renewal: participants whose PFC encodes contexts more distinctly during reversal will show stronger reinstatement of acquisition-phase fear memory traces when later tested in the original acquisition context?
- Is it the case that reversal learning recruits two simultaneous representational strategies in different brain regions: generalization (treating newly dangerous CS-+ like CS++ in fear-network territory) for cues that share their current threat status with established cue classes, and item-specific updating (distinguishing changing-valence cues such as CS+- from stable cues) in higher-order cortex?
- Is it the case that fear learning produces generalized (cross-item) neural representations of threatening cues in the canonical fear network: when an animal learns that a stimulus class is dangerous, the brain represents members of the class with overlapping multivoxel patterns rather than preserving item-specific patterns, so that any new exemplar of the class inherits the threat representation?

Override any of these by adding a `question:` field to the hypothesis's frontmatter and re-running the export.
