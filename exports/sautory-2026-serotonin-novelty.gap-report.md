# MIRA export — what the strict file cannot carry

**Paper:** `sautory-2026-serotonin-novelty` · **Generated:** 2026-09-09

31 claims, 38 typed relations between them.

## Claims by role

- **empirical** — 31

## Relations dropped

**31 of 38 relations (82%) have no MIRA predicate and are absent from the strict export.**

| Relation | Dropped | What is lost |
|---|---:|---|
| `requires` | 30 | a claim depends on another holding |
| `derived-from` | 1 | prediction derived from its hypothesis (inverse of entails) |

The `entails` / `derived-from` pair is the most consequential: together they are the paper's deductive spine. Without them a reader cannot tell which prediction belongs to which hypothesis.

## Relations flattened

`tests`, `confirms`, `validates`, `extends` and `replicates` all become `mira:supports`; `contradicts`, `rules-out` and `dissociates-with` all become `mira:opposes`. Both directions of collapse lose real distinctions — most sharply, evidence *designed* to test a prediction becomes indistinguishable from evidence that merely agrees with it after the fact.

## Verification records dropped

**0 verification records across 0 claims are absent from the strict export.** MIRA has no node type for the fact that a claim was independently checked, by what code, against what data, with what result. They are carried in the extended file as `haak:VerificationRecord`.

## Questions synthesized

MIRA requires every Claim to address a `mira:Question`; a claim tree has no such node. **0 questions were derived mechanically from hypothesis text and need human review.**


Override any of these by adding a `question:` field to the hypothesis's frontmatter and re-running the export.
