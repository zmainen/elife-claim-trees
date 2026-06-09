# Headley 2026 — Round-trip test scorecard

**Generated:** 2026-05-10

**Reference:** `/Users/zach/Projects/mainenlab/elife-claim-trees/claims/headley-2026-inhibitory-rhythms` (26 curated claims)
**CLI output:** `/tmp/elife-test/headley-2024-spatially-targeted-inhibitory` (86 extracted claims)
**Matcher model:** claude-opus-4-6

## Acceptance criteria

| Metric | Threshold | Achieved | Status |
|:-------|:----------|:---------|:-------|
| Claim recovery | ≥ 80% | 100.0% (26/26) | ✅ PASS |
| Panel assignment | ≥ 90% (of matched) | 50.0% (13/26) | ❌ FAIL |
| Role classification | ≥ 75% (of matched) | 96.2% (25/26) | ✅ PASS |

## Match-quality breakdown

- Exact matches: 13
- Partial matches: 13
- No match: 0
- Total recovered (exact + partial): 26 of 26

## Per-reference detail

| Reference slug | Match quality | CLI slug | Panel match | Role match | Notes |
|:---------------|:--------------|:---------|:-----------:|:----------:|:------|
| `beta-bidirectional-dendritic-control` | partial | `beta-rhythmic-inhibition-delivered-distal-2` | ✓ | ✓ | CLI claim captures modulation of dendritic spikes by beta but doesn't explici... |
| `beta-gates-distal-apical-inputs` | exact | `beta-rhythms-enhanced-transmission-distal` | ✓ | ✓ |  |
| `beta-optimal-distal-dendritic-entrainment` | partial | `increasing-inhibition-frequency-above-hz` | ✓ | ✓ | CLI says entrainment diminishes above 20 Hz, which partially captures beta op... |
| `burst-effects-emerge-first-cycles` | exact | `under-oscillatory-burst-conditions-beta` | ✓ | ✓ | CLI mentions modulations evident within first few cycles of a burst |
| `ca-spikes-couple-20ms-before-ap` | exact | `spike-occurrence-increased-within-ms` | ✗ | ✓ | CLI says Ca2+ spike occurrence increased within 20 ms of somatic APs; panel d... |
| `distal-inhib-drops-firing-02hz` | partial | `both-doubling-distal-perisomatic-inhibitory` | ✓ | ✓ | CLI captures the firing rate drop to 0.2 Hz but doesn't explicitly state mech... |
| `ei-lag-sensitivity-firing-rate` | partial | `increasing-lag-perisomatic-inhibition-monotonically` | ✓ | ✓ | CLI captures lag effects on firing rate but doesn't state the key point about... |
| `gamma-gates-proximal-basal-inputs` | exact | `gamma-barely-affected-moderately-suppressed` | ✓ | ✓ | CLI captures gamma gating proximal inputs phase-dependently while leaving dis... |
| `gamma-optimal-perisomatic-ap-modulation` | partial | `perisomatic-inhibition-frequency-increased-bias` | ✓ | ✓ | CLI captures gamma uniqueness in perisomatic modulation but doesn't directly ... |
| `gamma-perisomatic-no-dendritic-spike-change` | exact | `gamma-rhythmic-inhibition-delivered-perisomatically` | ✓ | ✓ |  |
| `hypothesis-distinct-compartmental-roles` | exact | `rhythmic-inhibition-different-spatial-locations` | ✗ | ✓ | Both state the hypothesis that perisomatic/distal inhibition serve distinct r... |
| `hypothesis-frequency-compartment-matching` | partial | `beta-frequency-inhibition-optimally-matched-timescale` | ✗ | ✓ | CLI captures the beta-dendrite matching but not the general principle includi... |
| `interprets-pv-gamma-sst-beta-associations` | partial | `results-may-provide-functional-interpretation` | ✗ | ✗ | CLI acknowledges the PV/gamma and SOM/beta association but doesn't elaborate ... |
| `l5-model-single-cell-scope` | exact | `all-results-derive-single-compartmental` | ✗ | ✓ | Both describe single-cell scope with no network dynamics |
| `na-spikes-couple-2to3ms-before-ap` | exact | `dendritic-na-spikes-increased-ms` | ✓ | ✓ | CLI says Na+ spikes increased 2-3 ms prior to somatic APs with coupling decli... |
| `naturalistic-drive-parameterization` | partial | `model-pyramidal-neuron-driven-naturalistic` | ✓ | ✓ | CLI captures baseline firing rate matching in vivo but not synapse counts or ... |
| `nmda-spikes-couple-25ms-before-ap` | exact | `nmda-spike-incidence-increased-ms` | ✓ | ✓ | CLI says NMDA spike incidence increased ~25 ms prior to somatic APs |
| `perisomatic-inhib-drops-firing-07hz` | partial | `both-doubling-distal-perisomatic-inhibitory` | ✓ | ✓ | CLI captures firing rate drop to 0.7 Hz but doesn't explicitly state AP thres... |
| `perisomatic-inhib-subtractive-divisive` | partial | `both-perisomatic-distal-dendritic-inhibition` | ✗ | ✓ | CLI captures subtractive+divisive for perisomatic but panel is fig4b vs fig5/... |
| `prediction-beta-optimal-distal` | exact | `beta-frequency-inhibition-optimally-matched-timescale` | ✗ | ✓ | Both predict beta optimality for distal dendrites based on timescale matching |
| `prediction-distal-dendritic-spike-mechanism` | partial | `perisomatic-distal-dendritic-inhibition-serve` | ✗ | ✓ | CLI captures prediction about distinct roles but less specific about dendriti... |
| `prediction-gamma-optimal-perisomatic` | exact | `gamma-frequency-inhibition-optimally-matched-fast` | ✗ | ✓ | Both predict gamma optimality for perisomatic based on fast Na+ dynamics |
| `prediction-orthogonal-input-gating` | exact | `beta-gamma-regulate-different-spatial` | ✗ | ✓ | Both predict beta gates distal and gamma gates proximal inputs independently |
| `prediction-perisomatic-input-output-shaping` | partial | `perisomatic-distal-dendritic-inhibition-serve` | ✗ | ✓ | CLI predicts perisomatic affects somatic excitability but doesn't specificall... |
| `prediction-perisomatic-threshold-mechanism` | partial | `perisomatic-distal-dendritic-inhibition-serve` | ✗ | ✓ | CLI captures distinct roles prediction but not specific prediction about AP t... |
| `pv-gamma-sst-beta-correspondence` | exact | `results-may-provide-functional-interpretation` | ✗ | ✓ | Both state model provides functional interpretation for PV/gamma and SOM/beta... |

## Unmatched CLI claims

The CLI produced 86 claims; 26 of them aligned to a reference.
The remaining 60 did not. (The reference is curated tighter than the
CLI's extraction; over-extraction is the CLI's expected failure mode at this stage.)

Selected unmatched CLI claims (first 10) for prompt iteration:

- `action-potentials-preceded-spike-up` [panel=fig3d, role=empirical]: Action potentials preceded by a Ca2+ spike (by up to 20 ms) had increased coupling with apical NMDA spikes, but no such 
- `although-perisomatic-inhibition-produced-strongest` [panel=fig4a, fig4b, fig4d, fig4e, role=synthesis]: Although perisomatic inhibition produced the strongest subtractive effect on f-I curves, distal dendritic inhibition red
- `apical-nexus-may-serve-thresholded` [panel=fig3c, fig3d, role=interpretation]: The apical nexus may serve as a thresholded nonlinearity for NMDA spikes in the apical tuft to drive action potentials.
- `apical-trunk-exhibited-relatively-small` [panel=fig2a, role=empirical]: The apical trunk exhibited a relatively small attenuation ratio of ~10%, while attenuation reached 0.1% in the distal ap
- `beta-band-frequencies-exhibit-unique` [panel=fig7a, fig7c, role=synthesis]: Beta band frequencies exhibit unique coordination with dendritic spikes: they are the fastest rhythm capable of entraini
- `beta-gamma-modulate-somatic-excitability` [panel=fig6a1, fig6a2, fig6b1, fig6b2, role=synthesis]: Beta and gamma modulate somatic excitability through distinct mechanisms: gamma shifts action potential threshold via pe
- `beta-modulated-responsiveness-distal-inputs` [panel=None, role=synthesis]: Beta modulated responsiveness to distal inputs in a phase-dependent manner, while gamma did so for proximal inputs.
- `beta-phase-modulated-na-spike` [panel=fig5e1, fig5e2, role=empirical]: Beta phase modulated Na+ spike presence in apical and basal dendrites with ~75% depth of modulation; this was unexpected
- `beta-phase-modulated-nmda-spike` [panel=fig5d1, fig5d2, role=empirical]: Beta phase modulated NMDA spike presence in both apical and basal dendrites with ~75% depth of modulation.
- `beta-rhythmic-inhibition-delivered-distal` [panel=fig5b, role=empirical]: Beta rhythmic inhibition delivered to distal dendrites modulated action potential rate as a function of beta phase.
