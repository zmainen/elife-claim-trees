---
uuid: afbf7e64-20a0-4f3f-a748-8591ddc1e2d4
slug: interprets-may-wightman-1989-fscv
doi: 10.1016/0006-8993(89)90835-4
claim: >
  May & Wightman (1989, Brain Research) used fast-scan cyclic voltammetry (FSCV) in rat
  striatal slices to measure evoked extracellular dopamine transients across 10, 30, and
  60 Hz electrical stimulation in dorsal and ventral striatum, and reported that ventral
  striatum reached substantially higher peak DA concentrations than dorsal striatum across
  all three frequencies. This slice-level dataset is the canonical empirical anchor for
  regional differences in striatal DA release dynamics.
displayClaim: >
  FSCV in rat striatal slices shows that ventral striatum reaches substantially higher peak
  DA than dorsal striatum across 10, 30, and 60 Hz stimulation (May & Wightman 1989).
shortClaim: "VS peak DA exceeds DS across stimulation frequencies (May & Wightman 1989)."
claim-type: interpretive
role: literature-context
concepts:
  - FSCV
  - striatal dopamine
  - dorsal vs ventral striatum
  - stimulation frequency
  - empirical anchor
priority: 2026-04-20
epistemic: moderate
check_verification: unrecorded

belongings: []

assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: ~
    panel: fig2E (explicit replication comparison)
    figureUri: https://iiif.elifesciences.org/lax/105214%2Felife-105214-fig2-v1.tif/full/1500,/0/default.jpg
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: literature interpretation; cited as the experimental target the simulated FSCV is compared against
    confidence: moderate

reproductions: []
---

This claim registers the May & Wightman (1989) FSCV dataset as a discrete literature reference so the replication claim `fscv-matches-may-wightman-1989` has an explicit node to point at. The paper's Figure 2E is framed as a direct replication comparison: simulated FSCV traces in DS and VS at three stimulation frequencies (10, 30, 60 Hz) are placed alongside the 1989 experimental results and scored qualitatively by the same VS > DS ordering. Without this literature node, "the simulation replicates May & Wightman" would have an unnamed referent.

The epistemic caveat — species (rat vs mouse), preparation (slice vs in vivo), and volume fraction — is inherited by the downstream replication claim and is discussed there; here the role of the node is purely to register the reference. The 1989 paper is pre-transporter-era and did not parameterize DAT Vmax or Km; the Vmax parameterization used in the present model is imported separately (see `interprets-cragg-rice-vmax-ratio`).
