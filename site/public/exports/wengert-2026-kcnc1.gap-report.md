# MIRA export — what the strict file cannot carry

**Paper:** `wengert-2026-kcnc1` · **Generated:** 2026-09-10

31 claims, 122 typed relations between them.

## Claims by role

- **empirical** — 14
- **prediction** — 9
- **hypothesis** — 3
- **control** — 2
- **methodological** — 1
- **scope** — 1
- **synthesis** — 1

## Relations dropped

**58 of 122 relations (48%) have no MIRA predicate and are absent from the strict export.**

| Relation | Dropped | What is lost |
|---|---:|---|
| `scopes` | 18 | a scope constraint governs another claim's validity |
| `enables-method` | 16 | a result makes a downstream method possible |
| `derived-from` | 9 | prediction derived from its hypothesis (inverse of entails) |
| `entails` | 9 | hypothesis entails its prediction — the deductive step |
| `interprets` | 4 | one claim interprets another |
| `requires` | 2 | a claim depends on another holding |

The `entails` / `derived-from` pair is the most consequential: together they are the paper's deductive spine. Without them a reader cannot tell which prediction belongs to which hypothesis.

## Relations flattened

`tests`, `confirms`, `validates`, `extends` and `replicates` all become `mira:supports`; `contradicts`, `rules-out` and `dissociates-with` all become `mira:opposes`. Both directions of collapse lose real distinctions — most sharply, evidence *designed* to test a prediction becomes indistinguishable from evidence that merely agrees with it after the fact.

## Verification records dropped

**18 verification records across 18 claims are absent from the strict export.** MIRA has no node type for the fact that a claim was independently checked, by what code, against what data, with what result. They are carried in the extended file as `haak:VerificationRecord`.

## Questions synthesized

MIRA requires every Claim to address a `mira:Question`; a claim tree has no such node. **3 questions were derived mechanically from hypothesis text and need human review.**

- Is it the case that the recurrent missense variant KCNC1-p.Ala421Val (A421V) in the Kv3.1 voltage-gated potassium channel causes a loss of channel function via impaired delivery of channel protein to the plasma membrane (a trafficking defect), rather than via altered gating or conductance of channels that do reach the surface?
- Is it the case that cell-autonomous loss of Kv3.1 function in PV-INs is sufficient to drive the network-level developmental and epileptic encephalopathy phenotype of KCNC1 disease?
- Is it the case that because Kv3.1 is strongly and selectively expressed in fast-spiking neurons that rely on rapid action-potential repolarization to sustain high firing rates, haploinsufficient or dominant-negative loss of Kv3.1 should produce a cell-type- specific impairment that targets parvalbumin-positive (PV+) GABAergic interneurons while leaving excitatory neurons (which do not express Kv3.1 at functionally relevant levels) intact?

Override any of these by adding a `question:` field to the hypothesis's frontmatter and re-running the export.

## Alternatives materialised as claims

None: every relation in this paper points at a claim the tree asserts.

## Paper-level scopes with no MIRA target

None.
