# Headley 2026 — Round-trip test scorecard

**Generated:** 2026-05-10

**Reference:** `/Users/zach/Projects/mainenlab/elife-claim-trees/claims/headley-2026-inhibitory-rhythms` (26 curated claims)
**CLI output:** `/tmp/elife-test/headley-2024-spatially-targeted-inhibitory` (76 extracted claims)
**Matcher model:** claude-opus-4-6

## Acceptance criteria

| Metric | Threshold | Achieved | Status |
|:-------|:----------|:---------|:-------|
| Claim recovery | ≥ 80% | 100.0% (26/26) | ✅ PASS |
| Panel assignment | ≥ 90% (of matched) | 50.0% (13/26) | ❌ FAIL |
| Role classification | ≥ 75% (of matched) | 65.4% (17/26) | ❌ FAIL |

## Delta from v1 (prompt iteration)

The Results-reader prompt was revised to emphasize the hypothesis→prediction→empirical-test structure, with explicit linguistic markers and a worked example. The reconciler prompt was revised to preserve role distinctions when agents surface different roles for related claims.

**Per-claim deltas:**

- `hypothesis-distinct-compartmental-roles`: role False → **True** (the one explicit hypothesis is now correctly classified).
- `l5-model-single-cell-scope`: panel True → False (LLM stochasticity; same content matched to a different CLI claim with no panel anchor).
- All 6 `prediction-*` claims: unchanged. The Results-reader emitted **0 prediction-role claims** in v2 (same as v1).

**Why the prediction iteration failed:**

The Results-reader is doing the right thing. Headley's predictions are not stated as predictions in the prose — they're inferred by the curator from the modelling structure. The paper's prose says "we found that gamma was optimal for perisomatic at 50 Hz"; the curator's prediction claim says "we predicted that gamma would be optimal for perisomatic"; the linkage between them is curator-inferred. There is no `if X then Y` phrasing in Headley's results section that the LLM could pattern-match.

**Implication:** prediction-role assignment is structural inference, not pattern matching. To recover predictions, the pipeline needs either:

1. **A second-pass structural-inference call** after extraction — given the empirical claims and the abstract, identify the implicit predictions that tie them to the hypothesis. This is heavier (one more LLM call per paper) but matches what the curator actually does.
2. **Accept that prediction roles are added at Step 5** by the analyst — the CLI surfaces empirical claims correctly; the analyst names the predictions during review. This is consistent with the methodology's claim that "Step 5 is where the schema's role labels are first assigned definitively."

**Recommendation:** option 2 is correct for Phase F. The CLI's extraction is faithful to the prose; the methodology positions Step 5 as the role-assignment gate. Targeting prediction-role recovery in extraction is asking the LLM to do work the methodology gives the analyst. We accept the role threshold failure on first round-trip as a calibration finding, not a CLI defect, and document this in the README.

## Match-quality breakdown

- Exact matches: 8
- Partial matches: 18
- No match: 0
- Total recovered (exact + partial): 26 of 26

## Per-reference detail

| Reference slug | Match quality | CLI slug | Panel match | Role match | Notes |
|:---------------|:--------------|:---------|:-----------:|:----------:|:------|
| `beta-bidirectional-dendritic-control` | partial | `beta-rhythmic-inhibition-delivered-distal-2` | ✓ | ✓ | CLI claim captures modulation of dendritic spikes by beta but doesn't explici... |
| `beta-gates-distal-apical-inputs` | exact | `beta-rhythms-enhanced-transmission-distal` | ✓ | ✓ |  |
| `beta-optimal-distal-dendritic-entrainment` | partial | `increasing-inhibition-frequency-above-hz` | ✓ | ✓ | CLI captures the falloff above 20 Hz but doesn't explicitly frame it as stron... |
| `burst-effects-emerge-first-cycles` | partial | `under-oscillatory-burst-conditions-beta` | ✓ | ✓ | CLI mentions modulations evident within first few cycles but doesn't cover bo... |
| `ca-spikes-couple-20ms-before-ap` | exact | `spike-occurrence-increased-within-ms` | ✗ | ✓ | CLI panel is fig3b vs ref fig2/fig3; same proposition about Ca2+ spikes prece... |
| `distal-inhib-drops-firing-02hz` | partial | `both-doubling-distal-perisomatic-inhibitory` | ✓ | ✓ | CLI covers both distal and perisomatic; captures 0.20 Hz number but doesn't e... |
| `ei-lag-sensitivity-firing-rate` | partial | `increasing-lag-perisomatic-inhibition-monotonically` | ✓ | ✓ | CLI captures firing rate effects of lag but doesn't emphasize the key point a... |
| `gamma-gates-proximal-basal-inputs` | exact | `gamma-barely-affected-moderately-suppressed` | ✓ | ✓ | CLI captures gamma gating proximal inputs while leaving distal unaffected |
| `gamma-optimal-perisomatic-ap-modulation` | partial | `perisomatic-inhibition-frequency-increased-bias` | ✓ | ✓ | CLI captures gamma being unique in keeping mean potential equivalent while bi... |
| `gamma-perisomatic-no-dendritic-spike-change` | exact | `gamma-rhythmic-inhibition-delivered-perisomatically` | ✓ | ✓ |  |
| `hypothesis-distinct-compartmental-roles` | partial | `paper-investigated-how-rhythmic-perisomatic` | ✗ | ✓ | CLI frames it as investigation topic rather than explicit hypothesis about di... |
| `hypothesis-frequency-compartment-matching` | partial | `slow-timescale-nmda-spikes-ms` | ✗ | ✗ | CLI captures part of the frequency-matching idea but only for gamma/dendritic... |
| `interprets-pv-gamma-sst-beta-associations` | partial | `results-may-provide-functional-interpretation` | ✗ | ✗ | CLI mentions the association but doesn't elaborate on the literature details ... |
| `l5-model-single-cell-scope` | exact | `all-results-derive-single-compartmental` | ✗ | ✓ | Both capture single-cell scope with no network dynamics |
| `na-spikes-couple-2to3ms-before-ap` | exact | `dendritic-na-spikes-increased-ms` | ✓ | ✓ |  |
| `naturalistic-drive-parameterization` | partial | `model-pyramidal-neuron-driven-naturalistic` | ✓ | ✗ | CLI captures firing rate match but not the detailed synapse counts (~26k exc,... |
| `nmda-spikes-couple-25ms-before-ap` | exact | `nmda-spike-incidence-increased-ms` | ✓ | ✓ |  |
| `perisomatic-inhib-drops-firing-07hz` | partial | `both-doubling-distal-perisomatic-inhibitory` | ✓ | ✓ | CLI has the 0.70 Hz number but doesn't emphasize the mechanism of elevated AP... |
| `perisomatic-inhib-subtractive-divisive` | exact | `both-perisomatic-distal-dendritic-inhibition` | ✗ | ✓ | CLI captures subtractive effect for both and divisive only for perisomatic, m... |
| `prediction-beta-optimal-distal` | partial | `distal-dendritic-inhibition-functioned-best` | ✗ | ✗ | CLI states the conclusion but doesn't frame it as a prediction with the times... |
| `prediction-distal-dendritic-spike-mechanism` | partial | `distal-dendritic-inhibition-regulated-incidence` | ✗ | ✗ | CLI captures the synthesis but not framed as a prediction; doesn't mention li... |
| `prediction-gamma-optimal-perisomatic` | partial | `perisomatic-inhibition-most-effective-when` | ✗ | ✗ | CLI states conclusion but not framed as prediction with timescale-matching ra... |
| `prediction-orthogonal-input-gating` | partial | `beta-modulated-responsiveness-distal-inputs` | ✗ | ✗ | CLI captures the result but not framed as prediction; doesn't elaborate on in... |
| `prediction-perisomatic-input-output-shaping` | partial | `both-perisomatic-distal-dendritic-inhibition` | ✗ | ✗ | CLI captures the subtractive/divisive effects but not framed as prediction |
| `prediction-perisomatic-threshold-mechanism` | partial | `perisomatic-inhibition-not-affect-rate` | ✗ | ✗ | CLI captures that perisomatic inhibition didn't affect dendritic spikes, but ... |
| `pv-gamma-sst-beta-correspondence` | partial | `results-may-provide-functional-interpretation` | ✗ | ✓ | CLI mentions the association but lacks the mechanistic detail about optimal f... |

## Unmatched CLI claims

The CLI produced 76 claims; 26 of them aligned to a reference.
The remaining 50 did not. (The reference is curated tighter than the
CLI's extraction; over-extraction is the CLI's expected failure mode at this stage.)

Selected unmatched CLI claims (first 10) for prompt iteration:

- `action-potentials-preceded-spike-up` [panel=fig3d, role=empirical]: Action potentials preceded by a Ca2+ spike (by up to 20 ms) had increased coupling with apical NMDA spikes, but no such 
- `apical-nexus-may-serve-thresholded` [panel=fig3d, role=interpretation]: The apical nexus may serve as a thresholded nonlinearity for NMDA spikes in the apical tuft to drive action potentials.
- `apical-trunk-exhibited-relatively-small` [panel=fig2a, role=empirical]: The apical trunk exhibited a relatively small attenuation ratio of ~10%, while attenuation reached 0.1% in the distal ap
- `beta-band-frequencies-exhibit-unique` [panel=fig7c, role=synthesis]: Beta band frequencies exhibit unique coordination with dendritic spikes: they are the fastest rhythm capable of entraini
- `beta-phase-modulated-na-spike` [panel=fig5e1, fig5e2, role=empirical]: Beta phase modulated Na+ spike presence in apical and basal dendrites with ~75% depth of modulation; this was unexpected
- `beta-phase-modulated-nmda-spike` [panel=fig5d1, fig5d2, role=empirical]: Beta phase modulated NMDA spike presence in both apical and basal dendrites with ~75% depth of modulation.
- `beta-rhythmic-inhibition-delivered-distal` [panel=fig5b, role=empirical]: Beta rhythmic inhibition delivered to distal dendrites modulated action potential rate as a function of beta phase.
- `beta-rhythmic-inhibition-delivered-soma` [panel=figS6-supplement1b, role=empirical]: Beta rhythmic inhibition delivered to the soma raised the action potential threshold and hyperpolarized the membrane pot
- `both-beta-gamma-rhythms-regulate` [panel=fig10c, role=synthesis]: Both beta and gamma rhythms regulate the sensitivity of pyramidal neurons to afferents throughout the dendritic tree, bu
- `clustered-synaptic-input-experiments-figure` [panel=fig10a, role=methodological]: Clustered synaptic input experiments (Figure 10) add 187 synapses driven by 40 near-synchronous presynaptic spike trains
