# Questions

You are reading one scientific paper to recover the **questions** it set out to answer, and to
say which of its claims answers each. A question is not a claim — a claim is a declarative
sentence — so it is recorded on the paper, not as a node in the graph. The vocabulary that
follows this task defines what a question is and how a hypothesis relates to it.

## What you are given

- **The abstract**, and the **Introduction** when it is available. (The prepared paper does not
  always carry an Introduction; when it is absent, read the questions off the abstract, which
  states them for an eLife paper.)
- **The paper's hypotheses and its rejected alternatives**, each as a slug and a sentence. The
  hypotheses are the answers the paper commits to; the `alt-` claims are the rivals it argues
  against. Both answer questions, and those are the only claims you may attach to a question.

## What to find

Find the questions the paper states — what it asked, in the abstract or the opening of the
Introduction. A paper usually asks one to three. State each as a question, in the paper's own
terms where it gives them, in one sentence. Then say, for each hypothesis and each rejected
alternative, which question it answers.

- A hypothesis is the answer the paper **commits to**; the alternatives it rules out are the
  **other answers** to the same question. So a hypothesis and the alternatives it competes with
  usually address the *same* question.
- Do not manufacture a question by hollowing out a hypothesis — "X involves neural mechanisms"
  is not a question the paper asked. Return the question it actually posed, or leave a claim
  unaddressed if none fits.
- Every `addresses` value must be one of the `id`s you returned, and every slug must be one you
  were given. Do not invent slugs or questions.

## What to return

A single JSON object and nothing else — no prose before or after, no code fence:

```json
{
  "questions": [
    {"id": "q1", "text": "Does the anterior insula encode responsibility-contingent guilt?"}
  ],
  "addresses": {
    "hypothesis-insula-tracks-interpersonal-guilt": "q1",
    "alt-agency-aversion-not-guilt": "q1"
  }
}
```

Number the questions `q1`, `q2`, … in the order you would present them. A claim that answers no
stated question is simply left out of `addresses`.
