# Stance

You are reading one paper to recover the **alternatives it argues against** — the rival
explanations, confounds and competing accounts it raises in order to reject, together with the
controls or results that eliminate each. An alternative explanation is a proposition, so it
gets a claim of its own; what marks it as a rival is its **stance**, not its role. The
vocabulary that follows this task defines stance, and the `rules-out` relation that points from
a control to the rival it kills.

Why this matters. A claim tree records what a paper's results *support*. Its eliminative
arguments — "this rules out explanation X of finding Y" — carry their warrant in the
elimination, and an elimination whose target is not a node in the graph has nowhere to point:
it gets wired to the nearest claim that does exist, which is usually one the paper asserts, and
then the graph says the paper contradicts itself. The rule the format enforces is that a
`rules-out` edge is **never** aimed at a claim the paper asserts. This layer gives each ruled-out
rival a node of its own so the edge has something true to point at.

## What you are given

- **The paper's controls and empirical claims** — each as a slug, its role, the panel it rests
  on, and its sentence. These are the claims that do the eliminating: a control exists to rule
  an alternative out, and an empirical result often does too. A control's sentence usually names
  its target in a closing clause — "evidence against …", "confirming …", "validating … as a
  manipulation check", "regardless of whether …".
- **The paper's research questions**, each with an id. An alternative is one of the *other
  answers* to a question the paper's own hypothesis answers.
- **Alternatives already recorded**, when the paper has any — each as its slug and its sentence.
  If you raise the same proposition again, reuse its slug so the existing claim is refined
  rather than duplicated.
- **The Results prose**, one sentence per line, each prefixed with the span id you cite in
  `span`.

## What to find

Every alternative the paper raises in order to reject, or raises and leaves open. State each as
the paper would have stated the proposition it argues against — the rival's own claim, the one
the paper is saying is false — not the paper's refutation of it.

- `stance` is `rejects` when the paper argues the alternative is false, and `entertains` when it
  raises the rival and does not settle it.
- `ruled_out_by` names the control or empirical claims — by slug, from the list you were given —
  whose result eliminates the alternative. A rejected alternative normally has at least one.
  Name only claims that do the eliminating, and only slugs you were given; do not invent them.
- `addresses` names the question the alternative answers, by id. Leave it out when none of the
  stated questions fits, or when the paper states no questions.
- `span` cites the Results sentence that states or names the alternative.
- `slug` is optional. Give one to reuse an alternative already recorded; otherwise it is derived
  from the proposition. It is written with an `alt-` prefix either way.
- Do **not** raise an alternative the paper actually asserts. A proposition the paper concludes
  is true is one of its claims with the default stance, not an alternative — and aiming an
  elimination at it is the one error the format forbids.

## What to return

A single JSON object and nothing else — no prose before or after, no code fence:

```json
{
  "alternatives": [
    {
      "slug": "alt-agency-aversion-not-guilt",
      "claim": "The happiness cost in the Social condition is general agency aversion — the unpleasantness of being the chooser as such — and is not contingent on responsibility for the partner's outcome.",
      "role": "hypothesis",
      "stance": "rejects",
      "addresses": "q1",
      "ruled_out_by": ["participant-happiness-lower-when-participant"],
      "span": "results-041",
      "why": "one sentence: how the named control or result eliminates this rival"
    }
  ]
}
```

Return only the alternatives you find. A paper that raises none returns `{"alternatives": []}`.
