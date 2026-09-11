# Everything the site is built from, in the order it has to run.
#
# Until now there was no root build file of any kind. `site/package.json` ran
# `build-data.js`, which shells out to no Python, so every generator that fills
# `site/src/data/` was an out-of-band manual step whose output was committed by hand. The
# published numbers stayed true to the corpus for exactly as long as somebody remembered to
# run four scripts before building — and the deploy workflow never ran them at all, so
# GitHub Pages has been serving whatever was last committed.
#
# The order below is not alphabetical and not arbitrary:
#   prediction-outcome writes review/prediction-outcome.json
#   corpus_facts       reads it, and writes site/src/data/corpus-facts.json
#   the rest are independent of each other
#   build-data.js      runs last; it is the only step `npm run build` knows about
#
# PYTHON: requirements.txt is what these need — PyYAML, and pyshacl for validation. They were
# described as standard-library-only when this was first written, which CI disproved on the
# first run. The verification scripts under verification/ need more still (pandas, numpy,
# scipy, nibabel), so override PYTHON for those.

PYTHON ?= python3
CORPUS ?= elife
SITE   := site

.DEFAULT_GOAL := help

.PHONY: help data validate build preview check contract report fresh deps

help:  ## Show this help
	@grep -hE '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) \
	  | awk 'BEGIN{FS=":.*?## "}{printf "  \033[1m%-10s\033[0m %s\n", $$1, $$2}'

# `make data` used to fail here for anyone with a fresh checkout, because build-data.js
# needs the site's node modules and nothing installed them.
$(SITE)/node_modules: $(SITE)/package-lock.json
	cd $(SITE) && npm ci && touch node_modules

deps: $(SITE)/node_modules  ## Install the site's node modules

# Every generator, in dependency order.
#
# exports/ used to be excluded, because export_mira.py stamped date.today() into every
# record's `created` and `modified` and so rewrote all 30 export files on any day but the one
# they were last written. That defeated the thing it fed: corpus_facts hashes those files for
# pipeline state, so running the exporter flipped every paper's mira-export cell from
# `current` to `stale` with the three export paths under `moved`. The dates now come from the
# claims' own `priority` fields, so the export is a function of its inputs and running it
# twice is a no-op — which is what lets it live here instead of in a target run by hand.
#
# Order is dependency order, and four edges in it are real:
#   prediction_outcome writes review/prediction-outcome.json, which corpus_facts reads
#   export_mira        writes the .mira.jsonld files formats_report and validate_mira read
#   formats_report     writes the .formats.json files corpus_facts reads
#   validate_mira      writes site/src/data/mira-validation.json, which corpus_facts reads
# corpus_facts therefore runs after all four, not second.
#
# Still NOT regenerated here: exports/{paper}.oxa.json and exports/{paper}.dg.jsonld, which
# come from extract/scripts/migrate_to_oxa.py and export_discourse_graphs.py, run per paper.
# formats_report reads both, so after a claim change its report is computed partly from stale
# inputs. The pipeline state flags oxa and dg as stale, so it surfaces rather than hiding.
data: $(SITE)/node_modules  ## Regenerate every artifact the site is built from
	$(PYTHON) scripts/prediction_outcome.py --write
	$(PYTHON) scripts/export_mira.py --all
	$(PYTHON) scripts/formats_report.py --all
	$(MAKE) validate PYTHON=$(PYTHON)
	$(PYTHON) scripts/corpus_facts.py
	$(PYTHON) scripts/agents_report.py
	$(PYTHON) scripts/review_queue.py
	cd $(SITE) && CORPUS=$(CORPUS) node scripts/build-data.js

validate:  ## SHACL-validate the MIRA exports (needs pyshacl)
	@command -v pyshacl >/dev/null 2>&1 || { \
	  echo "pyshacl not found — pip install pyshacl"; exit 1; }
	$(PYTHON) scripts/validate_mira.py

# Split by whether a non-zero exit should stop a merge.
#
# `check` is clean on main today, so a failure means this change broke something.
# `report` is not: audit_verifications finds 16 records asserting more than their run
# supports, and check_reproductions surfaces the corpus-wide status spread. Those are real
# and they predate this file. Gating on them would make every pull request red for reasons
# the pull request did not cause, so they run for their numbers and do not block.
check:  ## Gates that are clean on main. A failure here is this change's fault.
	$(PYTHON) scripts/check_relations.py
	cd extract && $(PYTHON) -m elife_extract.cli contract
	$(PYTHON) scripts/audit_layers.py

contract:  ## Regenerate the prompt contract from vocabulary.py, relations.py and schema.py
	cd extract && $(PYTHON) -m elife_extract.cli contract --write

# Both run, and the target still exits non-zero.
#
# Neither `-` prefixes nor plain recipe lines work here. Muting both with `-` makes a crash
# indistinguishable from the expected non-zero exit. Leaving them bare aborts the target on the
# first command — check_reproductions exits 1 today, so audit_verifications never ran at all
# and the "records asserting more than their run supports" count this job exists to surface was
# never printed. Collect the worst status, run everything, then fail with it.
report:  ## Standing corpus measurements. Expected to be non-zero; informational.
	@s=0; \
	$(PYTHON) scripts/check_reproductions.py --corpus --strict || s=$$?; \
	$(PYTHON) scripts/audit_verifications.py || s=$$?; \
	exit $$s

build: data  ## Regenerate data, then build the site
	cd $(SITE) && CORPUS=$(CORPUS) npx astro build

preview: build  ## Build and serve locally
	cd $(SITE) && npx astro preview

# The check that makes the rest of this file mean something. Regenerating must be a no-op on
# a clean tree; if it is not, the committed data does not match the corpus it claims to
# describe. CI runs this, so the failure surfaces in a pull request rather than on the
# published site.
# `git status --porcelain`, not `git diff`: a generator that writes a file nobody has added
# yet produces no diff at all, so a new review topic or a new export could appear, be
# untracked, and the gate would still call the tree clean.
#
# The pathspec covers every directory `data` writes. Two of them are easy to miss:
# exports/, now that the exporter is deterministic enough to run on every build — without it,
# editing a claim's relations leaves exports/ and everything downstream describing the old
# claim while the gate stays green; and site/public, because build-data.js copies the exports
# and design notes the site serves for download there, so leaving it out means the published
# files can disagree with the exports they were copied from — exactly the drift build-data.js
# says in its own comments that it exists to prevent.
GENERATED := site/src/data site/public review exports
fresh: data  ## Fail if regenerating changed anything that was committed
	@if [ -n "$$(git status --porcelain -- $(GENERATED))" ]; then \
	  echo ""; \
	  echo "Committed generated data is stale. What changed when regenerated:"; \
	  git status --porcelain -- $(GENERATED); \
	  echo ""; \
	  echo "Run 'make data' and commit the result."; \
	  exit 1; \
	fi
	@echo "Generated data matches the corpus."
