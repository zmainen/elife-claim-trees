A claim tree is stored as Markdown files with YAML frontmatter, which is a good format for
authoring and review and no format at all for exchange. `python3 scripts/export_mira.py --all`
converts every paper to MIRA JSON-LD — strict and extended — with a per-paper gap report
saying what the strict file could not carry. What each standard can and cannot represent is
documented in [`schema-mapping/`](schema-mapping/README.md).

The export is byte-stable across runs, deliberately: these files are published as artifacts
anyone can regenerate and diff, and that check is meaningless if a re-run reshuffles them.
