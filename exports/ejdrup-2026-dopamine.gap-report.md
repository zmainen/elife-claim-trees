# MIRA export — what the strict file cannot carry

**Paper:** `ejdrup-2026-dopamine` · **Generated:** 2026-09-10

25 claims, 95 typed relations between them.

## Claims by role

- **empirical** — 15
- **hypothesis** — 3
- **scope** — 3
- **literature-context** — 2
- **control** — 1
- **methodological** — 1

## Relations dropped

**41 of 95 relations (43%) have no MIRA predicate and are absent from the strict export.**

| Relation | Dropped | What is lost |
|---|---:|---|
| `requires` | 20 | a claim depends on another holding |
| `entails` | 11 | hypothesis entails its prediction — the deductive step |
| `scopes` | 8 | a scope constraint governs another claim's validity |
| `interprets` | 2 | one claim interprets another |

The `entails` / `derived-from` pair is the most consequential: together they are the paper's deductive spine. Without them a reader cannot tell which prediction belongs to which hypothesis.

## Relations flattened

`tests`, `confirms`, `validates`, `extends` and `replicates` all become `mira:supports`; `contradicts`, `rules-out` and `dissociates-with` all become `mira:opposes`. Both directions of collapse lose real distinctions — most sharply, evidence *designed* to test a prediction becomes indistinguishable from evidence that merely agrees with it after the fact.

## Verification records dropped

**25 verification records across 20 claims are absent from the strict export.** MIRA has no node type for the fact that a claim was independently checked, by what code, against what data, with what result. They are carried in the extended file as `haak:VerificationRecord`.

## Questions synthesized

MIRA requires every Claim to address a `mira:Question`; a claim tree has no such node. **3 questions were derived mechanically from hypothesis text and need human review.**

- Is it the case that d1 and D2 receptors encode dopamine signals on distinct temporal scales due to their different binding kinetics: D1 receptors (high EC50, fast on-rate) follow extracellular DA with millisecond delay and act as detectors of transient burst events, while D2 receptors (low EC50, slow off-rate) integrate the dopamine signal over seconds and cannot resolve brief pauses or closely spaced bursts?
- Is it the case that dAT nanoclustering acts as a possible regulator of effective DAT activity in striatum: when transporters are concentrated into dense nanoclusters rather than uniformly distributed, local depletion at the cluster surface creates a diffusion-limited bottleneck that lowers the effective Vmax even at constant total DAT expression — proposing nanoclustering as one candidate mechanism for the lower effective Vmax in VS than DS?
- Is it the case that the qualitative regional contrast in extracellular dopamine dynamics between dorsal and ventral striatum — DS producing varicosity-scale hotspots with no pervasive tonic baseline versus VS producing diffuse tonic-like coverage — is principally explained by a difference in DAT Vmax (~3:1 DS:VS), rather than by differences in release-related parameters (vesicular content, release probability, active terminal fraction, or pacemaker firing rate)?

Override any of these by adding a `question:` field to the hypothesis's frontmatter and re-running the export.
