---
uuid: 49eb1a86-3a61-4e0f-aa8e-f5c225b9df09
slug: hypothesis-vmax-explains-regional-difference
doi: ~
claim: >
  The qualitative regional contrast in extracellular dopamine dynamics between dorsal and
  ventral striatum — DS producing varicosity-scale hotspots with no pervasive tonic baseline
  versus VS producing diffuse tonic-like coverage — is principally explained by a difference
  in DAT Vmax (~3:1 DS:VS), rather than by differences in release-related parameters
  (vesicular content, release probability, active terminal fraction, or pacemaker firing rate).
displayClaim: >
  Regional differences in striatal DA dynamics (DS hotspots vs VS pervasive tonic coverage) are
  driven principally by DAT Vmax differences, not by release-side parameters.
shortClaim: "DAT Vmax differences, not release parameters, drive striatal regional dopamine dynamics."
claim-type: hypothesis
role: hypothesis
concepts:
  - DAT Vmax
  - regional contrast
  - dorsal striatum
  - ventral striatum
  - tonic dopamine
priority: 2026-04-19
epistemic: hypothesis
check_verification: unrecorded
status: N/A
panel: hypothesis

entails:
  - ds-lacks-pervasive-tonic-da
  - vs-maintains-pervasive-tonic-da
  - vmax-only-parameter-driving-regional-difference
  - vmax-modulation-larger-impact-in-vs
  - vs-low-active-fraction-resembles-ds-distribution
  - fscv-matches-may-wightman-1989

belongings: []

assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: 10.7554/eLife.105214
    panel: hypothesis
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: hypothesis stated in abstract and developed in Results sections 1–3
    confidence: N/A

reproductions: []
---

The Vmax-explains-regional-difference hypothesis is the central organising claim of the paper. It is stated in the abstract ("These regional differences do not reflect release-related phenomena but rather differential dopamine transporter (DAT) activity") and the entire Figure 3 parameter sweep is constructed to falsify it: had any of the release-related parameters generated a regional contrast comparable to Vmax, the hypothesis would be undermined. The sweep instead shows only Vmax produces a differential response between DS and VS, while every other parameter shifts both regions proportionally. The hypothesis is supported by external corroboration (DAT immunostaining gradient, FSCV match to May & Wightman 1989) and is the inferential bridge from the Vmax assumption to the observed regional dynamics.
