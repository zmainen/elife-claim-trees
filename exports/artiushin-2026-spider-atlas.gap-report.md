# MIRA export — what the strict file cannot carry

**Paper:** `artiushin-2026-spider-atlas` · **Claims registered:** 2026-03-30

17 claims, 67 typed relations between them.

## Claims by role

- **empirical** — 13
- **methodological** — 2
- **interpretation** — 1
- **scope** — 1

## Relations dropped

**35 of 67 relations (52%) have no MIRA predicate and are absent from the strict export.**

| Relation | Dropped | What is lost |
|---|---:|---|
| `scopes` | 15 | a scope constraint governs another claim's validity |
| `enables-method` | 14 | a result makes a downstream method possible |
| `derived-from` | 2 | a prediction derived from its hypothesis (inverse of entails) |
| `interprets` | 2 | one claim interprets another |
| `requires` | 2 | a claim depends on another holding |

The `entails` / `derived-from` pair is the most consequential: together they are the paper's deductive spine. Without them a reader cannot tell which prediction belongs to which hypothesis.

## Relations flattened

`tests`, `confirms`, `validates`, `extends` and `replicates` all become `mira:supports`; `contradicts`, `rules-out` and `dissociates-with` all become `mira:opposes`. Both directions of collapse lose real distinctions — most sharply, evidence *designed* to test a prediction becomes indistinguishable from evidence that merely agrees with it after the fact.

## Verification records dropped

**17 verification records across 17 claims are absent from the strict export.** MIRA has no node type for the fact that a claim was independently checked, by what code, against what data, with what result. They are carried in the extended file as `haak:VerificationRecord`.

## Questions synthesized

MIRA requires every Claim to address a `mira:Question`; a claim tree has no such node. **0 questions were derived mechanically from hypothesis text and need human review.**


Override any of these by adding a `question:` field to the hypothesis's frontmatter and re-running the export.

## Stance: claims this paper does not assert

Every claim in this paper is asserted by it.

## Alternatives materialised as claims

None: every relation in this paper points at a claim the tree asserts.

## Paper-level scopes with no MIRA target

None.
