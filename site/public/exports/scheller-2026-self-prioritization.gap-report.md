# MIRA export — what the strict file cannot carry

**Paper:** `scheller-2026-self-prioritization` · **Generated:** 2026-09-09

23 claims, 90 typed relations between them.

## Claims by role

- **empirical** — 8
- **prediction** — 4
- **hypothesis** — 3
- **control** — 2
- **interpretation** — 2
- **literature-context** — 1
- **methodological** — 1
- **scope** — 1
- **synthesis** — 1

## Relations dropped

**54 of 90 relations (60%) have no MIRA predicate and are absent from the strict export.**

| Relation | Dropped | What is lost |
|---|---:|---|
| `requires` | 15 | a claim depends on another holding |
| `scopes` | 14 | a scope constraint governs another claim's validity |
| `interprets` | 10 | one claim interprets another |
| `enables-method` | 7 | a result makes a downstream method possible |
| `derived-from` | 4 | prediction derived from its hypothesis (inverse of entails) |
| `entails` | 4 | hypothesis entails its prediction — the deductive step |

The `entails` / `derived-from` pair is the most consequential: together they are the paper's deductive spine. Without them a reader cannot tell which prediction belongs to which hypothesis.

## Relations flattened

`tests`, `confirms`, `validates`, `extends` and `replicates` all become `mira:supports`; `contradicts`, `rules-out` and `dissociates-with` all become `mira:opposes`. Both directions of collapse lose real distinctions — most sharply, evidence *designed* to test a prediction becomes indistinguishable from evidence that merely agrees with it after the fact.

## Verification records dropped

**14 verification records across 14 claims are absent from the strict export.** MIRA has no node type for the fact that a claim was independently checked, by what code, against what data, with what result. They are carried in the extended file as `haak:VerificationRecord`.

## Questions synthesized

MIRA requires every Claim to address a `mira:Question`; a claim tree has no such node. **3 questions were derived mechanically from hypothesis text and need human review.**

- Is it the case that the mechanism by which self-association enhances perceptual processing is a change in the absolute Theory-of-Visual-Attention processing capacity (the C parameter, which governs total resources available for encoding into aware short-term memory) rather than a pure redistribution of fixed attentional weights (the w parameter) between the two competing stimuli?
- Is it the case that mere arbitrary association of an otherwise neutral perceptual feature (a shape) with the self alters early attentional selection of that feature into aware short-term memory: the self-association acts as an attentional salience signal that shifts processing rates in the Theory of Visual Attention framework?
- Is it the case that social salience (driven by self-association or other-association) and perceptual salience (driven by physical properties such as local colour contrast) capture attention via largely independent mechanisms?

Override any of these by adding a `question:` field to the hypothesis's frontmatter and re-running the export.
