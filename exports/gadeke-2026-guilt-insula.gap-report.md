# MIRA export — what the strict file cannot carry

**Paper:** `gadeke-2026-guilt-insula` · **Generated:** 2026-09-09

27 claims, 89 typed relations between them.

## Claims by role

- **empirical** — 11
- **control** — 5
- **prediction** — 4
- **hypothesis** — 3
- **scope** — 2
- **interpretation** — 1
- **literature-context** — 1

## Relations dropped

**50 of 89 relations (56%) have no MIRA predicate and are absent from the strict export.**

| Relation | Dropped | What is lost |
|---|---:|---|
| `scopes` | 29 | a scope constraint governs another claim's validity |
| `derived-from` | 5 | prediction derived from its hypothesis (inverse of entails) |
| `entails` | 5 | hypothesis entails its prediction — the deductive step |
| `interprets` | 5 | one claim interprets another |
| `requires` | 4 | a claim depends on another holding |
| `enables-method` | 2 | a result makes a downstream method possible |

The `entails` / `derived-from` pair is the most consequential: together they are the paper's deductive spine. Without them a reader cannot tell which prediction belongs to which hypothesis.

## Relations flattened

`tests`, `confirms`, `validates`, `extends` and `replicates` all become `mira:supports`; `contradicts`, `rules-out` and `dissociates-with` all become `mira:opposes`. Both directions of collapse lose real distinctions — most sharply, evidence *designed* to test a prediction becomes indistinguishable from evidence that merely agrees with it after the fact.

## Verification records dropped

**24 verification records across 19 claims are absent from the strict export.** MIRA has no node type for the fact that a claim was independently checked, by what code, against what data, with what result. They are carried in the extended file as `haak:VerificationRecord`.

## Questions synthesized

MIRA requires every Claim to address a `mira:Question`; a claim tree has no such node. **3 questions were derived mechanically from hypothesis text and need human review.**

- Is it the case that anterior insula is the neural substrate of interpersonal guilt: when a participant bears responsibility for a choice that yields a negative outcome for another person, anterior insula activity tracks the resulting responsibility-contingent affect?
- Is it the case that momentary happiness in social decision contexts is governed by a computational rule in which partner reward prediction errors that arise from the participant's own choices (social_pRPEs) carry an independent, non-zero weight, distinct from the weight on partner RPEs that arise without participant agency?
- Is it the case that superior temporal sulcus (STS) — a core mentalizing-network region — represents the partner's affective experience specifically when the participant is responsible for the partner's outcome?

Override any of these by adding a `question:` field to the hypothesis's frontmatter and re-running the export.
