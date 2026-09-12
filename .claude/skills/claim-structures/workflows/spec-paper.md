# Spec a paper from its claims

Forward construction: the argument is built as a graph first, and the prose is written from it.
Use this when the results exist (or are nearly in) and the paper has to be structured, when a
draft has lost its spine, or when deciding what still has to be done before a paper is possible.

The graph is not a summary of the paper. It is the paper's skeleton, and it is cheap to
rearrange while it is still a graph.

## 1. State the questions

Two to four at most, each one sentence, each answerable. Write them into the paper's `index.md`
frontmatter with `q1`, `q2` ids. A question you cannot state without naming your result is not a
question — it is a finding looking for a frame.

## 2. Commit to an answer, and name the rivals

For each question, write the `hypothesis` claim: the answer this paper commits to, `addresses`
naming its question. Then write the *other* answers — the rivals a sceptical reader holds —
each as its own claim with `addresses` pointing at the same question and stance `entertains`.

This is the step that makes the spec worth doing. A paper is persuasive in proportion to how
credible the alternatives were before it eliminated them, and the alternatives are almost never
written down until a reviewer supplies them. Writing them first turns review into something you
run against yourself.

Rivals worth enumerating: the null; the confound (a trivial mechanism that would produce the
same observation); the scope objection (true, but only in this preparation); the prior framework
your result is being read against.

## 3. Derive the predictions

For each hypothesis, `entails` the predictions that follow *if it holds* — and, for each rival,
what that rival predicts instead. State them as conditionals with the conditions attached:
"if the optimal frequency is set by matching the rhythm period to the local spike timescale,
then distal inhibition should be maximally effective near 20 Hz."

Predictions shared by your hypothesis and a rival are not evidence, however well they come out.
The predictions that discriminate are the paper.

## 4. Attach the results

For each prediction, the empirical claim that tests it: one proposition, panel-grounded,
quantitative. `tests` up to the prediction, `supports` up to the hypothesis.

**This is the figure plan.** One panel per empirical claim, one figure per group of claims that
share a prediction. A figure whose panels belong to unrelated claims is a layout decision
masquerading as an argument; a claim with no panel is either a synthesis or a result you do not
actually have.

Results in hand that test no prediction are the diagnostic: either they belong to a hypothesis
you have not written down, or they are not part of this paper. Both are useful to learn before
drafting.

## 5. Kill the rivals, bound the whole

- For each rival, the `control` claim whose result eliminates it, carrying `rules-out`. A rival
  with no incoming `rules-out` survives into the reviews — decide now whether to run the
  control, argue it away in the discussion, or keep it as an open alternative and say so.
- Every `scope` claim: the population, the preparation, the stimulation regime, the model's
  boundary, the untested parameter. Point them at what they bound, `scopes: ["*"]` where global.
  Written now they shape the claims; written at the end they become a limitations paragraph.
- Every `methodological` claim a result leans on, with `enables-method` to the results it
  warrants. Where the method is assumed rather than validated here, that is an `assessment`
  claim with `epistemic: weak`, and everything requiring it inherits the weakness.
- Every `literature-context` premise the argument inherits — especially any framework you
  position against, which needs a node for the eliminative move to reach.

## 6. Read the top of the graph — that is the abstract

The synthesis and interpretation claims are what the paper concludes. Drafting the abstract from
them, rather than from the figures, is what keeps the abstract honest: abstracts systematically
scrub the eliminative moves (`rules-out`, `refutes`) and absorb controls into the main result.
The structure records what the prose drops.

Section order falls out too: results follow the hypothesis-prediction-test arcs in dependency
order; the methods section is the methodological and scope claims made continuous; the
discussion is the interpretation claims plus the scope claims turned outward.

## 7. Audit the spec before drafting

Run [references/checks.md](../references/checks.md), then read the graph for these:

| Symptom | What it means |
|:--------|:--------------|
| a rival with no incoming `rules-out` | an unanswered objection — run the control or concede it |
| a prediction with no `tests` | an untested commitment; drop it or do the experiment |
| an empirical claim testing nothing | an orphan result, or a hypothesis you have not stated |
| a synthesis with one `supports` | an overreach: one result is not an integration |
| no `scope` claims | the boundaries are unexamined, not absent |
| every edge is `supports` | the argument has no deductive spine — nothing entails, nothing tests |
| a hypothesis with one prediction | the design has one point of contact with the world |

## 8. Keep the graph alive while drafting

When a reviewer objects, the objection is a rival: add the node, and either the control that
kills it or the scope claim that concedes it. When a result changes, the claim sentence changes
and everything that `requires` it is flagged for re-reading. When a figure is cut, the claims it
carried are visibly orphaned rather than quietly lost.

The version of the tree that ships alongside the paper is what lets a reader check the argument
rather than reconstruct it — which is the thing the corpus this skill comes from exists to test.
