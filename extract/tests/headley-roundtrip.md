# Headley 2026 — Round-trip test scorecard

**Generated:** 2026-05-10

**Reference:** `/Users/zach/Projects/mainenlab/elife-claim-trees/claims/headley-2026-inhibitory-rhythms` (26 curated claims)
**CLI output:** `/tmp/elife-test/headley-2024-spatially-targeted-inhibitory` (76 extracted claims)
**Matcher model:** claude-opus-4-6

## Acceptance criteria

| Metric | Threshold | Achieved | Status |
|:-------|:----------|:---------|:-------|
| Claim recovery | ≥ 80% | 100.0% (26/26) | ✅ PASS |
| Panel assignment | ≥ 90% (of matched) | 53.8% (14/26) | ❌ FAIL |
| Role classification | ≥ 75% (of matched) | 61.5% (16/26) | ❌ FAIL |

## Match-quality breakdown

- Exact matches: 10
- Partial matches: 16
- No match: 0
- Total recovered (exact + partial): 26 of 26

## Findings — systematic biases for prompt iteration

The CLI achieves **perfect recall** (every curated claim has a corresponding extraction) but the panel and role thresholds fail. The mismatches cluster into a small number of systematic biases the Results-reader and reconciler prompts should address:

### Bias 1 — Under-use of the `prediction` role

The reference has 6 `prediction-*` claims; the CLI matches 0 of them with role=prediction. The CLI consistently maps prediction claims to `empirical` (the observed test) or `synthesis` (the conclusion), missing the deductive layer the paper explicitly establishes.

Affected reference claims (all matched but role-mismatched):
- `prediction-beta-optimal-distal` → CLI marked as `interpretation`
- `prediction-distal-dendritic-spike-mechanism` → CLI marked as `empirical`
- `prediction-gamma-optimal-perisomatic` → CLI marked as `empirical`
- `prediction-orthogonal-input-gating` → CLI marked as `synthesis`
- `prediction-perisomatic-input-output-shaping` → CLI marked as `empirical`
- `prediction-perisomatic-threshold-mechanism` → CLI marked as `empirical`

**Fix candidate:** the Results-reader prompt should explicitly call out the hypothesis→prediction→test structure the methodology section 4.4.1 (deductive reasoning) describes, and instruct the agent to surface predictions as separate claims from their empirical tests.

### Bias 2 — Under-use of the `hypothesis` role

The reference has 2 `hypothesis-*` claims at the top of the dependency graph. The CLI matched both, but classified them as `empirical` (one) and `prediction` (the other) — the organising hypothesis itself is not being surfaced as a top-level claim.

Affected reference claims:
- `hypothesis-distinct-compartmental-roles` → CLI marked as `empirical`
- `hypothesis-frequency-compartment-matching` → CLI marked as `prediction`

**Fix candidate:** the Results-reader prompt should emphasize that hypotheses are typically introduced in the abstract or first paragraph of results and carry `entails:` edges to subsequent predictions; if the paper frames a claim as the organising bet rather than a result, it is a hypothesis.

### Bias 3 — Multi-panel claims collapsed to single-panel

Several reference claims span multiple panels (e.g., `distal-inhib-drops-firing-02hz` lists `panel: fig4, fig5`). The CLI consistently picks one panel even when the caption assigns the claim to multiple. This produces panel mismatches that aren't truly wrong — just less complete.

**Fix candidate:** the Caption-reader prompt should preserve the comma-separated panel list when a single claim spans multiple panels (already in the prompt; the agent isn't following it strictly enough). The reconciler prompt could also be revised to preserve multi-panel assignments.

### Cost-benefit on iteration

At this point the CLI is recoverable — the human review gate at Step 5 catches role mismatches and panel collapses cheaply (the analyst skims and adjusts before write). The prompt iteration would shift work from human review into the prompts themselves. Recommended order:

1. **Land the scorecard as the first measurement.** This file is the baseline.
2. **Iterate Bias 1 (prediction role)** — single prompt change in the Results-reader, re-run scorecard, measure delta.
3. **Iterate Bias 2 (hypothesis role)** — same, isolated.
4. **Bias 3 (multi-panel)** — already in the prompt; skip iteration unless other biases are addressed and this remains the bottleneck.

Each iteration is one full pipeline run (~5 min, ~$3-5). Not free, but cheap relative to the per-paper review savings.

## Per-reference detail

| Reference slug | Match quality | CLI slug | Panel match | Role match | Notes |
|:---------------|:--------------|:---------|:-----------:|:----------:|:------|
| `beta-bidirectional-dendritic-control` | partial | `beta-rhythmic-inhibition-hz-depth` | ✓ | ✓ | CLI claim captures beta distal inhibition modulating dendritic spikes but doe... |
| `beta-gates-distal-apical-inputs` | exact | `beta-rhythms-enhanced-transmission-distal` | ✓ | ✓ | Both describe beta rhythms gating distal inputs: enhanced during trough, supp... |
| `beta-optimal-distal-dendritic-entrainment` | partial | `increasing-inhibition-frequency-above-hz` | ✓ | ✓ | CLI claim captures that 20 Hz is peak for distal dendritic spike entrainment ... |
| `burst-effects-emerge-first-cycles` | exact | `burst-regime-modulations-evident-within-first` | ✓ | ✓ |  |
| `ca-spikes-couple-20ms-before-ap` | exact | `spike-occurrence-increased-within-ms` | ✗ | ✓ | CLI says Ca2+ spike occurrence increased within 20 ms of somatic APs; panel i... |
| `distal-inhib-drops-firing-02hz` | partial | `both-doubling-distal-perisomatic-inhibitory` | ✓ | ✓ | CLI claim includes both distal and perisomatic; captures distal dropping to 0... |
| `ei-lag-sensitivity-firing-rate` | partial | `increasing-lag-perisomatic-inhibition-lowered` | ✓ | ✓ | CLI captures lag effects on firing rate but doesn't emphasize the key point a... |
| `gamma-gates-proximal-basal-inputs` | exact | `gamma-rhythms-barely-affected-moderately` | ✓ | ✓ | CLI describes gamma gating proximal inputs (enhanced trough, suppressed peak)... |
| `gamma-optimal-perisomatic-ap-modulation` | partial | `perisomatic-inhibition-frequency-increased-bias` | ✓ | ✓ | CLI claim describes gamma-range peaking at 50 Hz for membrane potential fluct... |
| `gamma-perisomatic-no-dendritic-spike-change` | exact | `gamma-rhythmic-inhibition-hz-depth` | ✓ | ✓ | Both state gamma perisomatic inhibition had virtually no effect on dendritic ... |
| `hypothesis-distinct-compartmental-roles` | partial | `perisomatic-inhibition-principally-regulated-action` | ✗ | ✗ | CLI captures only the perisomatic half of the hypothesis; the distal part is ... |
| `hypothesis-frequency-compartment-matching` | partial | `perisomatic-inhibition-most-effective-when` | ✗ | ✗ | CLI captures the conclusion (gamma optimal perisomatic, beta optimal distal) ... |
| `interprets-pv-gamma-sst-beta-associations` | partial | `results-may-provide-functional-interpretation` | ✗ | ✗ | CLI mentions the association of PV+ with gamma and SST+ with beta but doesn't... |
| `l5-model-single-cell-scope` | exact | `all-results-derive-single-cell-compartmental` | ✓ | ✓ |  |
| `na-spikes-couple-2to3ms-before-ap` | exact | `dendritic-na-spikes-increased-ms` | ✓ | ✓ | Both describe Na+ spikes peaking 2-3 ms before somatic APs with coupling decl... |
| `naturalistic-drive-parameterization` | partial | `naturalistic-presynaptic-drive-elicited-median` | ✓ | ✗ | CLI captures the 5.3 Hz firing rate matching in vivo but doesn't mention ~26,... |
| `nmda-spikes-couple-25ms-before-ap` | exact | `incidence-nmda-spikes-increased-ms` | ✓ | ✓ | Both describe NMDA spikes increasing ~25 ms before somatic APs. |
| `perisomatic-inhib-drops-firing-07hz` | partial | `both-doubling-distal-perisomatic-inhibitory` | ✓ | ✓ | CLI includes perisomatic dropping to 0.70 Hz but doesn't explicitly state mec... |
| `perisomatic-inhib-subtractive-divisive` | exact | `both-perisomatic-distal-dendritic-inhibition` | ✗ | ✓ | CLI captures both subtractive and divisive effects of perisomatic inhibition,... |
| `prediction-beta-optimal-distal` | partial | `slow-timescale-nmda-spikes-ms` | ✗ | ✗ | CLI mentions the ~50 ms timescale matching but frames it as interpretation ab... |
| `prediction-distal-dendritic-spike-mechanism` | partial | `distal-dendritic-inhibition-decreased-nmda` | ✗ | ✗ | CLI states the result (distal inhibition decreases NMDA/Ca2+ spikes) but fram... |
| `prediction-gamma-optimal-perisomatic` | partial | `perisomatic-inhibition-most-effective-when` | ✗ | ✗ | CLI captures that perisomatic inhibition is most effective at gamma but doesn... |
| `prediction-orthogonal-input-gating` | partial | `somatic-spiking-driven-clustered-proximal` | ✗ | ✗ | CLI captures the bidirectional gating result but frames it as synthesis rathe... |
| `prediction-perisomatic-input-output-shaping` | partial | `both-perisomatic-distal-dendritic-inhibition` | ✗ | ✗ | CLI captures subtractive+divisive effects empirically rather than as a predic... |
| `prediction-perisomatic-threshold-mechanism` | partial | `perisomatic-inhibition-not-affect-rate` | ✗ | ✗ | CLI captures that perisomatic inhibition doesn't affect dendritic spike rates... |
| `pv-gamma-sst-beta-correspondence` | exact | `results-may-provide-functional-interpretation` | ✗ | ✓ | Both describe the model providing mechanistic grounding for PV+/gamma and SST... |

## Unmatched CLI claims

The CLI produced 76 claims; 26 of them aligned to a reference.
The remaining 50 did not. (The reference is curated tighter than the
CLI's extraction; over-extraction is the CLI's expected failure mode at this stage.)

Selected unmatched CLI claims (first 10) for prompt iteration:

- `action-potentials-preceded-spike-up` [panel=fig3d, role=empirical]: Action potentials preceded by a Ca2+ spike (by up to 20 ms) had increased coupling with apical NMDA spikes, but no such 
- `apical-nexus-may-serve-thresholded` [panel=fig3d, role=interpretation]: The apical nexus may serve as a thresholded nonlinearity for NMDA spikes in the apical tuft to drive action potentials i
- `beta-band-frequencies-exhibit-unique` [panel=fig7c, role=synthesis]: Beta band frequencies exhibit unique coordination with dendritic spikes: they are the fastest rhythm capable of entraini
- `beta-modulated-responsiveness-distal-inputs` [panel=None, role=synthesis]: Beta modulated responsiveness to distal inputs in a phase-dependent manner, while gamma did so for proximal inputs.
- `beta-rhythmic-inhibition-delivered-distal` [panel=fig5e, role=empirical]: Beta rhythmic inhibition delivered to distal dendrites had an unexpected impact on Na+ spikes, since delivery of the sam
- `beta-rhythmic-inhibition-distal-dendrites` [panel=fig11b, role=synthesis]: Beta rhythmic inhibition to the distal dendrites modulated dendritic spikes (Ca2+, NMDA, and Na+ spikes) in a phase-depe
- `beta-rhythms-either-not-affect` [panel=fig10b, role=empirical]: Beta rhythms either did not affect or moderately suppressed proximal inputs during the trough phase and suppressed them 
- `beta-rhythms-emulated-modulating-distal` [panel=fig5, role=methodological]: Beta rhythms are emulated by modulating distal (SOM+) inhibitory synapses at 16 Hz with 20% depth, and gamma rhythms by 
- `both-beta-gamma-rhythms-regulate` [panel=fig10c, role=synthesis]: Both beta and gamma rhythms regulate the sensitivity of pyramidal neurons to afferents throughout the dendritic tree, bu
- `bursty-inhibition-simulations-apply-gaussian` [panel=fig9, role=methodological]: Bursty inhibition simulations apply a Gaussian envelope with a standard deviation of two oscillatory cycles to the rhyth
