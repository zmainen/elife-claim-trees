# Skills

The `claim-structures` skill moved to **[`claim-graphs`](https://github.com/zmainen/claim-graphs)**,
at `skills/claim-structures/`, where it is *rendered* from the declarations rather than written
by hand — relations and their directions from `scripts/relations.py`, the enforced rules from
`scripts/check_relations.py`, roles and claim types from `vocabulary.py`, the sequence from
`pipeline/layers.yaml`, and the vocabulary a model is sent from the prompt contract. `make check`
there fails when the committed skill is not what its sources generate.

The copy that lived here was hand-written, and it had drifted: it omitted `in-tension-with`
entirely, still called `dissociates-with` an opposition after #125 moved it out, and offered an
`epistemic` value no claim file uses. That is why it is not maintained in two places.

This repository holds the corpus, the site and the collaboration record. To use the skill
against it, load it from a `claim-graphs` checkout and point `CLAIM_GRAPHS_CORPUS_DIR` at
`claims/` here.
