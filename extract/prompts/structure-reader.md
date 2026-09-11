# Structure reader

You are reading one scientific paper to find what it claims. You are given its Methods,
its appendices and its supplementary material, and nothing else: no abstract, no results
prose, no captions. Two other readers are given those, none of you sees the others' work, and
a reconciler compares the three afterwards. Agreement between independent readings is the
signal, so read your slice on its own terms.

Your slice carries no panel inventory and no bracketed span ids, so leave `span` null, name a
`panel` only where the methods name one, and keep every `evidence` quote verbatim.

## What this slice carries

The methods say what was actually done and what it rests on. Nothing else in the paper
states the boundary conditions on its results, so this slice carries what the others cannot:

- **Scope claims.** Where the results apply: the model class, the preparation, the species,
  the population and its size, the design. "All results come from a single-cell compartmental
  model." "Study 2 excluded four participants for head motion." These usually bound every
  empirical claim in the paper.
- **Methodological claims.** A capability or analytical commitment that later results depend
  on for their meaning: the null distribution, the model comparison that licenses a model-based
  analysis, the validation of a sensor, a pre-registration and what it fixed. Write what the
  commitment is and what it licenses.
- **Controls the methods document.** Where a control condition or manipulation check is
  described, return it as a claim about what that control establishes, with role `control`.
- **Load-bearing assumptions.** A parameter taken from the literature, an initialisation not
  derived, a threshold not sensitivity-tested. These are scope or methodological claims about
  what the results are conditional on.

## What is not a claim

Procedure for its own sake. Which software ran the task, how participants were recruited,
which scanner was used: these are facts, not claims, unless a result turns on them. The test
is whether a downstream result would mean something different if this were different. If not,
leave it out.

The vocabulary's **What is not a claim** section, under the `methodological` role, works this
test on real sentences: a normalisation, a measure's definition, a seed choice, a
significance threshold, a software choice — each returned by a reader and each not a claim,
set beside the procedure that a result does turn on and so is methodological. Read it before
you return a methodological claim, and check your candidate against the negative list.

One line is easy to cross: an exclusion count, the sample size and the description of the
design are components of the paper's scope claim, not claims of their own — fold them into the
scope claim that says where the results apply rather than returning each as a separate
methodological or scope claim.

## Rules

- **Never infer a result from a method.** "We computed the correlation between X and Y" says
  nothing about whether X correlates with Y. Without the results prose you cannot know what
  was found, only what was measured; return the methodological claim, not the result you
  imagine it produced.
- `evidence` is a verbatim quote from the text you were given, at most two sentences. It is
  checked against the source.
- `panel` only where the methods name one; usually `null`.
- Where the methods describe both an experiment and a simulation, say which a claim concerns.
- This slice typically yields 5–15 claims: a few scope claims, a few methodological warrants,
  the controls the methods document. A computational paper with several models may yield more;
  more than 30 means procedure is being returned as claims.

## What to return

The JSON array described below, and nothing else: no prose before or after it, no code fence.
The vocabulary that follows defines every value you may use.
