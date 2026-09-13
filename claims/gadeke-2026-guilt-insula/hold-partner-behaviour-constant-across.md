---
uuid: d69aa510-3094-4017-930b-c7c57c98bdc5
slug: hold-partner-behaviour-constant-across
doi: null
claim: To hold the partner's behaviour constant across participants, the partner's decisions were simulated
  by an algorithm that always selected the option with the highest expected value.
claim-type: assessment
role: methodological
concepts: []
priority: '2026-09-13'
enables-method:
- when-partner-received-low-lottery
belongings: []
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: null
  readers: single-source
reproductions:
- carried_from: partner-algorithm-deception-assumption
  agent: mainen-z
  date: 2026-03-30
  status: blocked
  blocked_by: not-applicable
  notes: 'Confirmed by code inspection of Methods section (Decision task, p.15): "the partner''s decisions
    were simulated using a simple algorithm that always selected the option with the highest expected
    value". Authors acknowledge this in Discussion as a limitation and note that partner outcomes nonetheless
    influenced participant happiness, arguing the effects could be stronger with genuine interaction.'
warrant: weak
warrant_why: asserted procedure; nothing in the tree's argument bears on it
check_verification: blocked
check_verification_from:
- record:blocked
---

**Notes from extraction:** The partner was not a free agent; partner choices in the Partner condition were deterministic, which the responsibility/guilt contrasts rely on.

**Relations.** Why each outgoing edge was inferred:

- `enables-method` → `when-partner-received-low-lottery`: simulating the partner's choices holds behaviour constant, making the guilt comparison possible

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**structure-reader evidence:**
> In order to ascertain constant decisions by the partner, the partner’s decisions were simulated using a simple algorithm that always selected the option with the highest expected value
