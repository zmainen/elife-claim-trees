The `pairs.py` script in this directory has been retired. Its `score` subcommand is now:

```
cd extract && python3 -m elife_extract.cli score \
  --reference ../claim-tree.v1 \
  --candidate ../../../claims/gadeke-2026-guilt-insula \
  --pairs match.v3.pairs.json
```

Accepts both `[{committed, rerun, note}]` (this directory's format) and the
matcher's own `{matches: [...]}` format. Reports recovery, precision, panel,
role, edge recovery, and role confusion.
