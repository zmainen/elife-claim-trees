# Design an experiment from its claim structure

Before data. The graph you build here is a design document and, if you fix it before running, a
preregistration: the same claims, with `stance` and `epistemic` unset and every panel marked
planned.

The organising idea: **a design is defined by what it can eliminate.** An experiment that would
produce an interesting result under every hypothesis on the table has not been designed, it has
been scheduled.

## 1. The question

One sentence, answerable, not naming your preferred answer. Write it as `q1` on the study.

## 2. Enumerate the answers — all of them

Write every answer a competent sceptic would hold, one claim each, `addresses: q1`, stance
`entertains`:

- **the null** — the effect does not exist;
- **the confound** — something uninteresting produces the same observation (task difficulty,
  arousal, motion, expression level, sampling bias);
- **the rival mechanism** — a different process producing the same phenomenon;
- **the scope objection** — it is real but confined to this preparation, species, or regime;
- **the prior framework** — the account the field currently defaults to.

Then mark one as yours: `role: hypothesis`, stance `asserts` when the study asserts it.

Do this before thinking about methods. Enumerating the rivals first is what separates a design
from a protocol, and it is the only part of this workflow that cannot be recovered afterwards —
once you have data, the rivals you did not name look like objections rather than options.

## 3. Derive what each answer predicts

For each answer, including the rivals, write the predictions it `entails` under the conditions
you can actually create. Then build the table that is the heart of the design:

| Prediction | Your hypothesis | Null | Confound | Rival mechanism |
|:-----------|:----------------|:-----|:---------|:----------------|
| P1 dose-response is monotonic | yes | no | yes | yes |
| P2 effect survives the confound control | yes | no | **no** | yes |
| P3 effect reverses under manipulation M | yes | no | no | **no** |

A row where every column agrees buys nothing. The design is the set of rows where columns
disagree, and if there are none, the experiment cannot settle the question — change the design
now rather than discovering it in analysis.

## 4. Plan the measurements as claims

For each discriminating prediction, write the empirical claim you expect to be able to make,
in full, before collecting anything:

```yaml
slug: distal-inhibition-suppresses-firing
claim: >
  Doubling distal dendritic inhibition reduces somatic firing rate relative to baseline,
  with the reduction larger than for matched perisomatic inhibition.
claim-type: empirical
role: empirical
epistemic: ~                      # unset until data
tests: [prediction-distal-dendritic-spike-mechanism]
requires: [single-cell-model-scope, drive-parameterization]
assertions:
  - paper-slug: <study>
    panel: planned-fig2a
    analysis: analysis/firing_rate_sweep.py
    method: compartmental modelling — inhibition magnitude sweep
    stance: entertains            # nothing is asserted before data
```

Writing the sentence first forces the design decisions that are otherwise deferred: what is
measured, in what units, against what comparison, with what effect direction. **If you cannot
write the sentence without the data, you do not yet know what the experiment measures.** Leave
the magnitude as a blank to be filled — never as a guessed number, which becomes a fabricated
result the moment the file is read by anyone else.

Name the analysis path in the claim. A planned claim whose analysis is unnamed is a hope.

## 5. Controls, one per rival

Every rival from step 2 needs a planned control claim carrying `rules-out` to it. Write what
result would eliminate it — specifically, including the direction and the threshold. A control
whose outcome you cannot state in advance is not a control.

Two cases to handle explicitly:

- A rival you cannot eliminate with this design. Keep the node, leave it with no incoming
  `rules-out`, and write the `scope` claim that concedes it. That is an honest design; silence
  is not.
- A control that would only be informative if it comes out null. Say so — `validates` is for
  exactly this, a check whose specific outcome strengthens a warrant.

## 6. Scope and method, written before data

Scope claims: population, preparation, stimulation regime, dose range, model architecture, the
parameters assumed rather than measured. Point them at the empirical claims they bound, or
`scopes: ["*"]`.

Methodological claims: every capability the planned interpretation depends on — the sorting
pipeline, the decoder, the null model, the registration. Where a capability is assumed rather
than validated in this study, register it as an `assessment` claim with `epistemic: weak` and
let everything that `requires` it inherit that.

Feasibility belongs here too, as claims with the numbers in them: the sample size the design
needs for the effect it expects, the runtime, the n per group. A power calculation that lives
only in a grant is not attached to the claim it constrains.

## 7. Audit the design

Run [references/checks.md](../references/checks.md), then check the design-specific properties:

| Check | Failure means |
|:------|:--------------|
| every rival has an incoming `rules-out`, or a scope claim conceding it | an objection the study cannot answer and does not admit |
| at least one prediction discriminates your hypothesis from each rival | the experiment cannot settle the question |
| every planned empirical claim names an analysis | a measurement without a method |
| every claim sentence is writable without the data | the measurement is underspecified |
| each dissociation has both arms planned | half a contrast establishes nothing |
| no claim carries a number that does not exist yet | a fabricated result waiting to be quoted |
| scope claims exist and are pointed at something | the boundaries are unexamined |

## 8. After the data

The graph becomes the record rather than the plan:

- Fill the numbers into the claim sentences, verbatim from the analysis output.
- Set `stance`: `asserts` for what held, `rejects` for rivals the controls killed, and leave
  `entertains` on rivals that survived — an open alternative is a finding.
- Where a prediction came out against you, add `refutes` from the result to the prediction and
  keep both. A paper refuting its own prediction is the loop closing correctly, and it is the
  part of the record that is worth the most and gets dropped the most.
- Set `epistemic` from what the data actually support, bounded by the weakest claim each result
  `requires`.
- Add `reproductions` blocks as analyses are run, recording what the code actually opened and
  actually returned rather than what it was expected to show.

Diffing the pre-data graph against the post-data one gives, exactly: what was predicted, what
held, what did not, and what was added afterwards. That diff is the thing a preregistration is
supposed to make possible and usually does not.
