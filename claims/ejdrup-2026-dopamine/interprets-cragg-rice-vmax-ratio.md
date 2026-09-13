---
uuid: 39079ccf-d87a-4e0b-83a9-a01369e54836
slug: interprets-cragg-rice-vmax-ratio
doi: 10.1016/j.tins.2004.03.011
claim: >
  Prior voltammetry and DAT-binding literature — notably Cragg & Rice (2004, TINS) and
  Kennedy and colleagues on in vivo fast-scan measurements — established a roughly 3:1
  ratio of dopamine transporter Vmax between dorsal and ventral striatum, with DS at
  approximately 4–6 µM·s⁻¹ and VS at approximately 1.5–2 µM·s⁻¹. This Vmax asymmetry is
  the functional correlate of the DAT protein gradient seen across the dorsoventral
  striatal axis and has been treated as an empirical given in computational models of
  striatal DA dynamics.
displayClaim: >
  Prior voltammetry literature established a roughly 3:1 DS:VS DAT Vmax ratio (DS ~6, VS
  ~2 µM·s⁻¹) — treated as a numerical anchor for striatal DA models (Cragg & Rice 2004;
  Kennedy et al.).
shortClaim: "Prior voltammetry sets a 3:1 DS:VS DAT Vmax ratio used as a model parameter."
claim-type: interpretive
role: literature-context
concepts:
  - DAT Vmax
  - dorsoventral gradient
  - voltammetry literature
  - model parameterization
priority: 2026-04-20
epistemic: moderate
check_verification: unrecorded

belongings: []

assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: ~
    panel: fig2A (implied parameterization)
    figureUri: https://iiif.elifesciences.org/lax/105214%2Felife-105214-fig2-v1.tif/full/1500,/0/default.jpg
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: literature interpretation; cited as the source of the 3:1 DS:VS Vmax ratio imported into the model
    confidence: moderate

reproductions: []
---

This claim registers the voltammetry-literature Vmax ratio as a discrete node so that the scope claim `ds-vs-vmax-ratio-assumed` has an explicit referent for the "published literature" phrase. The 3:1 ratio is the structural load-bearing parameter of the entire model — every claim about regional differences in DA dynamics in DS versus VS flows from it, either directly (the tonic-DA-accumulation contrast) or indirectly (the Vmax-sweep parameter-sensitivity finding).

The epistemic status is moderate because the Vmax ratio is well-supported across multiple in vitro and ex vivo preparations but has not been directly measured in the specific brain state and species the simulated tissue represents (awake mouse with pacemaker-firing DA neurons). The functional Vmax additionally depends on DAT trafficking dynamics and effective surface density, both of which the paper later argues can be modulated by nanoclustering — so the 3:1 number is best understood as a parameterization anchor rather than a fixed biological constant.
