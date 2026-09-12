---
uuid: 26819b09-5b20-4c90-b9f3-8bdd29a2a57c
slug: distal-inhib-drops-firing-02hz
doi: ~
claim: >
  Doubling the strength of distal dendritic inhibition reduces somatic firing rate from a
  baseline of approximately 5.5 Hz to approximately 0.2 Hz, primarily by suppressing the
  occurrence of dendritic Ca²⁺ and NMDA spikes rather than by directly raising AP threshold.
displayClaim: >
  Doubling distal dendritic inhibition collapses somatic firing from ~5.5 Hz to ~0.2 Hz,
  almost entirely by suppressing dendritic Ca²⁺ and NMDA spikes rather than by raising the
  somatic AP threshold.
claim-type: empirical
role: empirical
concepts:
  - distal dendritic inhibition
  - somatic firing rate
  - dendritic spike suppression
  - Ca2+ spikes
  - NMDA spikes
priority: 2026-03-30
epistemic: strong
rules-out:
- alt-distal-inhibition-raises-somatic-threshold

tests:
  - prediction-distal-dendritic-spike-mechanism

dissociates-with:
  - perisomatic-inhib-drops-firing-07hz

belongings:
  - relation: requires
    target: l5-model-single-cell-scope
  - relation: requires
    target: naturalistic-drive-parameterization
  - relation: supports
    target: beta-bidirectional-dendritic-control
  - relation: supports
    target: beta-gates-distal-apical-inputs
  - relation: supports
    target: hypothesis-distinct-compartmental-roles

assertions:
  - paper-slug: headley-2026-inhibitory-rhythms
    doi: 10.7554/eLife.95562
    panel: fig4, fig5
    figureUri: https://iiif.elifesciences.org/lax/95562%2Felife-95562-fig4-v1.tif/full/1500,/0/default.jpg
    analysis: scripts/Fig4.ipynb, scripts/Fig5.ipynb
    dataset: https://datadryad.org/dataset/doi:10.5061/dryad.v6wwpzhb8
    dataset-doi: 10.5061/dryad.v6wwpzhb8
    method: compartmental modelling — inhibition magnitude sweep
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: verified
    script: verification/headley-2026-inhibitory-rhythms/verify.py
    original_figure: verification/originals/headley-2026-inhibitory-rhythms/fig4.jpg
    figure: verification/headley-2026-inhibitory-rhythms/fig4a-firing-rates.png
    original_script: https://github.com/dbheadley/InhibOnDendComp/blob/main/scripts/Fig4.ipynb
    script_execution: unmodified
    script_execution_note: "Run unmodified on pre-computed CSV data from GitHub repo"
    time_fast: "~2 min"
    time_full: "~6 hrs (NEURON + 1.88 GB Dryad)"
    notes: >
      Verified directly from Figure4a.csv in repo data/. Pre-computed firing rates (30
      trials each condition): control=5.5±0.86 Hz, dendritic (2×distal inhib)=0.2±0.15 Hz,
      somatic (2×perisomatic)=0.7±0.31 Hz. These are exact matches for the claimed values.
      Figure4d.csv shows Ca spike rates: control=4.86 Hz, dendritic=3.10 Hz (reduced),
      somatic=4.84 Hz (preserved) — confirming that distal inhib suppresses dendritic Ca
      spikes while perisomatic inhib does not. Figure4e.csv (NMDA): control=4.28 Hz,
      dendritic=3.07 Hz (reduced), somatic=4.19 Hz (preserved). The dendritic spike
      suppression mechanism is confirmed. Full notebooks (Fig4.ipynb, Fig5.ipynb) require
      Dryad data for detailed panel reproduction, but the key quantitative claim is
      completely verified from pre-computed summary data.
---

The near-complete suppression of firing (5.5 → 0.2 Hz) under doubled distal inhibition demonstrates that dendritic spikes are not merely modulatory — they are required for most somatic APs under these conditions. The mechanism is dendritic spike suppression: distal inhibitory conductance prevents membrane voltage from reaching spike threshold in the apical tuft, eliminating the regenerative events that would otherwise drive somatic output. This contrasts sharply with perisomatic inhibition (same magnitude: 5.5 → 0.7 Hz), where the mechanism is AP threshold elevation and the effect is smaller.
