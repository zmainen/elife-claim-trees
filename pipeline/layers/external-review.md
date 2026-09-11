**This step is specified but not implemented as written.** As specified: present the draft
claim table for review before any files are written; the reviewer corrects claim sentences,
reclassifies roles and types, adds missing claims, removes spurious ones, revises slugs, and
adjudicates single-source candidates. Nothing reaches disk until the table is approved. It is
the intellectual gate — the claim graph should be right before it is made permanent.

As it runs today the gate does not exist. Two things stand in its place, and neither of them is
a person reading the corpus.

A model's pass over the draft is the `external-review` layer, declared like any other and
versioned and hashed with the rest. A person's approval is a separate operation, performed on a
version that already exists: `scripts/pipeline.py approve <paper> <layer> --by NAME` records who
read which version of what. Because the record names the version, re-running the layer does not
carry the approval forward — it was granted to text that no longer exists.

Nothing forces an approval and none has been granted. The corpus is unreviewed, and the
approval ledger says so for every cell in it. The step is documented in full because it is what
the method requires, and its absence is the largest gap between the method and the artefact. The review gate is where the schema's role labels (`hypothesis`, `prediction`, `empirical`, `control`, `scope`, `methodological`, `synthesis`, `interpretation`, `literature-context`) are first assigned definitively, because role-assignment requires the analyst's judgment about what kind of work each claim is doing in the paper's argument.
