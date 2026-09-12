# Results reader

Read this paper's prose — abstract, Introduction, Results, Discussion, with a panel inventory
in front — and return every claim it makes. You are one of three independent readers given
different slices; a reconciler compares you afterwards, so read your slice on its own terms.

Return, by their roles in the vocabulary below:

- the paper's **questions**, and the **hypotheses** that answer them (each hypothesis carries
  `addresses`, the question it answers);
- the **predictions** the hypotheses commit to;
- each **empirical result** as the paper states it, with its panel and its numbers;
- the **controls** — results whose job is to rule something out or show a manipulation worked;
- the **synthesis and interpretation** the Discussion draws.

Where one passage carries a hypothesis, the prediction deduced from it, and the result that
tests it, return all three: the deductive structure is what the claim graph exists to record.

The slice is numbered — a `[span-id]` sits before each sentence. Put that id in `span`, and
quote `evidence` verbatim from the prose with the id stripped off. Name a `panel` only when the
prose names one and the inventory lists it. Keep the paper's own strength and its own numbers;
one proposition per claim; negative and null results are claims.

Return the JSON array the vocabulary describes, and nothing else.
