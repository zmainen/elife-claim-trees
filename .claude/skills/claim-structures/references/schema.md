# Claim schema

One file per claim: YAML frontmatter over an optional markdown body. The body carries what does
not compress into fields — caveats, boundary conditions, why one edge and not another.

Canonical path in a corpus: `claims/<paper-slug>/<claim-slug>.md`, with an `index.md` per paper.

## Required fields

| Field | Value |
|:------|:------|
| `uuid` | UUID4, generated once at creation, immutable. `python3 -c "import uuid; print(uuid.uuid4())"` |
| `slug` | filename slug: lowercase, hyphenated, 3–6 words, a verb phrase naming the proposition |
| `doi` | `~` — claims are not yet citable units. Exception: a `literature-context` claim puts the *cited paper's* DOI here |
| `claim` | one declarative sentence, active voice, quantitative where the result is quantitative |
| `claim-type` | `empirical` / `interpretive` / `existence` / `synthesis` / `assessment` / `hypothesis` / `prediction` |
| `role` | one of the nine below |
| `concepts` | domain terms the claim touches; the handle for cross-paper retrieval |
| `priority` | date the claim was first registered (ISO) |
| `epistemic` | `strong` / `moderate` / `weak` / `contested` — support across *all* assertions, not this paper's confidence |
| `assertions` | list of blocks tying the claim to paper / panel / analysis / data |
| `reproductions` | list of verification attempts; `[]` when none |

`epistemic` is the analyst's standing assessment and gets revised: a claim asserted `strong` by
one paper and failing reproduction in another moves to `contested`. It is bounded by the weakest
claim it `requires` — that is the point of registering assumptions as claims.

## Claim types

| Type | Definition |
|:-----|:-----------|
| `empirical` | a directly observed or computed result |
| `interpretive` | an inference drawn from one or more empirical claims |
| `existence` | an assertion that a phenomenon or entity exists |
| `synthesis` | a proposition integrating results across analyses, papers or datasets |
| `assessment` | a methodological or quality claim — a parameter, an assumption, a capability |
| `hypothesis` | a proposition bet on, not yet evidenced by this work's results |
| `prediction` | a deduced expectation, to be tested by an empirical claim |

## Roles

Role governs which edges a claim may carry and how a reader reconstructs the argument from the
graph alone. It is the most consequential field after `claim`.

| Role | What it marks | Signals in prose | Typical type |
|:-----|:--------------|:-----------------|:-------------|
| `hypothesis` | the organising bet the rest defends | "we hypothesize", "we asked whether", "we sought to test" | `hypothesis` |
| `prediction` | the deductive consequence under stated conditions | "if X then we should observe Y", "the model predicts" | `prediction` |
| `empirical` | a measured or computed result, panel-grounded | "we found", "we measured", "Figure N shows" | `empirical` |
| `control` | a result whose work is to eliminate a rival | "rules out", "excludes", "not due to", "no effect of [confound]" | `empirical` |
| `scope` | a boundary condition on the empirical claims | "all results come from", "the model assumes", "restricted to" | `assessment` |
| `methodological` | a procedural capability that warrants an interpretation | "sorting uses Kilosort 2.5", "modeled as sinusoidal modulation" | `assessment` |
| `synthesis` | several results integrated, staying inside this work's evidence | "taken together", "these results show", "this dissociation establishes" | `synthesis` |
| `interpretation` | a reframing through a theoretical lens, reaching outside | "may provide a functional interpretation", "suggests a role for" | `interpretive` |
| `literature-context` | a cited prior result as a first-class node | "as shown by Author (Year)", "previous work established" | `interpretive` |

Notes that matter in practice:

- A **hypothesis** holds no empirical content and does not `requires` empirical claims —
  its predictions do that. Its panel is normally null; a hypothesis is paper-level.
- An **empirical** claim is panel-grounded by definition. If you cannot name the panel, table or
  analysis block, it is probably a synthesis or an interpretation.
- **control** vs **empirical** is functional, not contentful: the same proposition is `control`
  here and `empirical` in a paper that reports it as a finding.
- **scope** is often global: `scopes: ["*"]` qualifies every empirical claim in the paper.
- **synthesis** stays inside the paper's own evidence; **interpretation** maps onto outside
  theory. Reading an interpretation as a derivation is the commonest way a reconstruction
  overstates what the work showed.
- **literature-context** exists so eliminative and interpretive moves have an explicit referent.
  Without a node for "multiplicative gain control", `rules-out: multiplicative-gain-control` is
  an eliminative move against an unnamed alternative.

## Questions

A question is not a claim — a claim is a declarative sentence — so it is not a node. It lives in
the paper's `index.md` frontmatter:

```yaml
questions:
  - id: q1
    text: "Does the anterior insula encode responsibility-contingent interpersonal guilt?"
```

A `hypothesis` names the question it answers via top-level `addresses: q1`; so does a rejected
alternative, which is one of the *other* answers to the same question. Every other role omits
the field. A hypothesis and the alternatives it competes with normally share one `addresses` —
that shared id is what makes them rivals rather than unrelated propositions.

## Assertions

One block per paper that asserts the claim. The panel is a property of the assertion, not of the
claim: `fig2a` says how *this* paper chose to show the proposition.

```yaml
assertions:
  - paper-slug: headley-2026-inhibitory-rhythms
    doi: 10.7554/eLife.95562
    panel: fig4, fig5              # publisher's own figure id where available
    figureUri: https://…           # optional, for rendering
    scope: tissue-scale            # varicosity-scale | tissue-scale | in-vivo | ex-vivo | in-vitro
    analysis: scripts/Fig4.ipynb
    dataset: https://datadryad.org/dataset/doi:10.5061/dryad.v6wwpzhb8
    dataset-doi: 10.5061/dryad.v6wwpzhb8
    method: compartmental modelling — inhibition magnitude sweep
    confidence: strong             # this paper's own confidence
    stance: asserts                # asserts | entertains | rejects | attributes
    source: "Servan-Schreiber et al. 1990"   # required when stance is `attributes`
```

### Stance

| Value | Meaning |
|:------|:--------|
| `asserts` | the paper claims the proposition is true — **default** when absent |
| `entertains` | it is raised as a candidate and not asserted |
| `rejects` | the paper argues it is false |
| `attributes` | someone else asserts it; this paper reports that. Requires `source` |

There is no "rejected" value. A claim asserted with `entertains` and an incoming `rules-out`
**is** a rejected alternative; with `entertains` and no such edge it is an *open* alternative —
a rival raised and not settled, which is a finding about the paper worth keeping.

### Alternatives are claims

When a paper rules out a confound, a rival mechanism, or a competing account, the thing ruled
out gets a file like any other. Its role is whatever it functionally is (usually `hypothesis`);
what marks it as a rival is the stance on its assertion.

```yaml
uuid: …
slug: alt-social-context-shifts-risk-attitude
claim: >
  The happiness difference between Social and Partner conditions reflects a social-context-driven
  shift in risk attitude rather than responsibility-contingent guilt.
role: hypothesis
epistemic: weak
addresses: q2
assertions:
  - paper-slug: gadeke-2026-guilt-insula
    stance: rejects
    method: agent extraction from the paper's control analyses
```

and the control that kills it carries `rules-out: [alt-social-context-shifts-risk-attitude]`.

## Reproductions

```yaml
reproductions:
  - agent: mainen-z                # the identity that ran it — not a person who read it
    date: 2026-03-30
    status: verified
    script: verification/<paper>/verify.py
    original_script: https://github.com/…/Fig4.ipynb
    script_execution: unmodified   # unmodified | patched | from-notes
    figure: verification/<paper>/fig4a-firing-rates.png
    time_fast: "~2 min"
    time_full: "~6 hrs (NEURON + 1.88 GB Dryad)"
    notes: >
      Pre-computed firing rates (30 trials/condition): control 5.5±0.86 Hz, dendritic
      0.2±0.15 Hz, somatic 0.7±0.31 Hz — exact matches for the claimed values.
```

| Status | Meaning |
|:-------|:--------|
| `verified` | ran it; output matches within tolerance |
| `verified:partial` | ran a defined subset; matched portion named in `notes` |
| `failed:mismatch` | ran it; output does not match — discrepancy diagnosed in `notes` |
| `unverified` | not attempted |
| `unverified:no-data` / `unverified:no-code` | deposit not accessible |
| `unverified:code-error` | errors before producing output; record the exact error |
| `unverified:compute-infeasible` | would need compute beyond available resources |

`notes` carries the evidentiary weight. "Numbers differ" is not a record. "Clearance rate
constant 0.31 s⁻¹ in reproduction vs 0.18 s⁻¹ in paper; suspect different initial conditions"
is. A status written from what the analysis was *expected* to show is the one failure mode a
later reader cannot detect — record what the code actually opened and actually returned.

## Auxiliary fields

- `displayClaim` — one to two sentences, the form rendered in body text and cards. Softens the
  formal sentence without changing the proposition.
- `shortClaim` — a single clause, ≤90 characters, for graph nodes and tooltips. Required for
  synthesis, interpretation and literature-context nodes, which must read at a glance.
- `number` / `numberParts` — **computed at build** from role and graph position (`H1.P2.E1`).
  Never author these by hand.

## Conditionality is graph structure

When a result depends on an assumed parameter, a methodological choice, or an untested
boundary, do not annotate it — register it as an `assessment` claim with its value, its source
and whether it was sensitivity-tested, and point a `requires` edge at it.

```yaml
slug: d2r-initialization-unjustified
claim: >
  D2 receptor occupancy is initialized at 0.4 without derivation from steady state; at
  EC50 = 7 nM and tonic [DA] ~10 nM, equilibrium occupancy would be ≈0.59. No sensitivity
  analysis over this parameter is reported.
claim-type: assessment
role: scope
epistemic: weak
```

Three kinds always deserve this treatment: model-parameter assumptions taken from literature
rather than measured; scope separations where a simulation runs at a different scale from the
paper's primary model; and untested methodological choices (initialization, thresholds,
boundary conditions). The weakness then propagates by traversal instead of by footnote.
