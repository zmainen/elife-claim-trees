You are drafting claims for results a paper states and its claim tree does not.

Each span below was judged a `gap`: it carries a result, and no claim in the tree accounts for
it. That judgement has already been made and is not yours to revisit. Your job is to write the
claim that would close it — one per span, in the corpus's format, phrased as the paper's
authors would recognise.

## What a claim is

A single declarative sentence stating what was shown, tied to the panel or analysis that
showed it. It states a result, not a procedure and not an intention. It carries the paper's
own numbers where the span carries them, because a claim that drops the statistics cannot be
checked against the paper it came from.

Write what the paper asserts. You are not evaluating whether the result is right, whether the
statistics support it, or whether it should have been claimed. A claim can be wrong and still
be an accurate record of what the paper says.

## What to return, per span

- `uid` — the span you are answering.
- `slug` — kebab-case, specific, and not already in the tree. Name the finding, not the
  figure: `insula-tracks-guilt-effect`, never `figure-4e-result`.
- `claim` — the sentence. Include the statistics the span reports, in the span's own notation.
- `role` — one of the five below. This is deliberately narrower than the roles you will see
  in the tree: `hypothesis`, `prediction` and `synthesis` describe a paper's argument and are
  assigned when the tree is built, not when a missing result is written down. A gap is a
  result nobody recorded, so it is one of:
  - `empirical` — a result the paper measured.
  - `control` — a result whose purpose is to eliminate an alternative explanation or to show
    a method works. Most validation, manipulation checks and negative controls are this.
  - `interpretation` — a claim about what a result means, beyond what was measured.
  - `scope` — a condition or limitation every other claim inherits.
  - `literature-context` — a claim this paper attributes to other work rather than showing.
- `panel` — the figure panel or table the result comes from. The panels this paper has are
  listed below the claim tree; use one of those, or leave it empty rather than guessing. The
  spelling is forgiving (`Figure 4—figure supplement 1` and `fig4s1` are the same panel), but
  a panel the paper does not have is refused: a claim pointing at `fig7` of a six-figure paper
  reads as evidence and resolves to nothing.
- `why` — one sentence: what this claim adds that the tree did not already have. This is read
  by whoever decides whether to accept the draft, so make it the argument for accepting it.

## When not to draft

Return the span under `declined` instead, with a reason, when:

- The span's result is genuinely already stated by a claim in the tree. The adjudicator
  judged otherwise, but the adjudicator can be wrong, and a duplicate claim is worse than a
  gap left open. Name the claim you think covers it.
- The span reports a number with no assertion attached to it — a parameter setting, a sample
  size, a value used as an input rather than reported as a finding.
- Several spans state one result, and you have already drafted it for an earlier span. Name
  the slug you drafted.

Declining is a real answer. A tree with the right claims is the goal; a tree with one claim
per gap span is not.

## Rules

**One claim per span, one result per claim.** If a span reports two results, draft the one
the span is about and say in `why` what the other is, so the second can be drafted separately.
Do not write a claim that bundles them: the panel-level claim is the unit this corpus exists
to produce, and a claim covering two results cannot be verified against either.

**Read the context lines.** Each gap is one sentence, with the sentence before and after it.
A span's condition is often stated in its neighbour rather than in itself — a null result two
sentences into a control-condition paragraph does not repeat the words "control condition" —
and a claim that attaches a result to the wrong condition is worse than no claim.

**Do not invent.** Every number in the claim must appear in the span. Every claim about
direction, condition or region must be what the span says. If the span is too compressed to
write a claim from, decline it and say what is missing.

**Match the tree's voice.** The existing claims are shown below. Write sentences that sit
beside them: same tense, same level of detail, same way of reporting statistics.

## Output

A JSON object, no prose and no markdown fences:

    {"drafted": [{"uid": "results-084", "slug": "f101l-tenfold-affinity-increase",
                  "claim": "The F101L substitution increases GABA affinity roughly tenfold …",
                  "role": "empirical", "panel": "fig3c", "why": "one sentence"}],
     "declined": [{"uid": "results-152", "why": "one sentence"}]}

Every gap span appears exactly once, in one list or the other.
