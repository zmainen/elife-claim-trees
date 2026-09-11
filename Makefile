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
# PYTHON: the generators here are standard library only and run under any python3. The
# verification scripts under verification/ are not — they need pandas, numpy, scipy and
# nibabel, so override PYTHON for those.

PYTHON ?= python3
CORPUS ?= elife
SITE   := site

.DEFAULT_GOAL := help

.PHONY: help data exports validate build preview check report fresh deps

help:  ## Show this help
	@grep -hE '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) \
	  | awk 'BEGIN{FS=":.*?## "}{printf "  \033[1m%-10s\033[0m %s\n", $$1, $$2}'

# `make data` used to fail here for anyone with a fresh checkout, because build-data.js
# needs the site's node modules and nothing installed them.
$(SITE)/node_modules: $(SITE)/package-lock.json
	cd $(SITE) && npm ci && touch node_modules

deps: $(SITE)/node_modules  ## Install the site's node modules

# The generators that are safe to run on every build, in dependency order.
#
# exports/ is deliberately NOT here, and that is a known hole rather than an oversight.
# export_mira.py stamps date.today() into every record's `created` and `modified`, so
# regenerating changes all 30 export files on any day but the one they were last written.
# Wiring it in would make `make fresh` fail every morning for a reason unconnected to the
# corpus, and a gate that cries wolf daily is worse than no gate.
#
# It is worse than cosmetic: corpus_facts hashes those files for pipeline state, so running
# the exporter flips every paper's mira-export cell from `current` to `stale` with the three
# export paths listed as `moved`. A timestamp carrying no information defeats the staleness
# model it feeds. `make exports` runs them by hand until the exporter is deterministic.
data: $(SITE)/node_modules  ## Regenerate every generated artifact, in dependency order
	$(PYTHON) scripts/prediction_outcome.py --write
	$(PYTHON) scripts/corpus_facts.py
	$(PYTHON) scripts/agents_report.py
	$(PYTHON) scripts/review_queue.py
	cd $(SITE) && CORPUS=$(CORPUS) node scripts/build-data.js

exports:  ## Regenerate exports/ and validate them. Not part of `data` — see the note above.
	$(PYTHON) scripts/export_mira.py --all
	$(PYTHON) scripts/formats_report.py --all
	$(MAKE) validate PYTHON=$(PYTHON)

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

# Not muted with `-`. CI marks this job continue-on-error, which already stops it blocking;
# silencing it here too would make a crash indistinguishable from the expected non-zero exit,
# and the measurements could stop being produced with no signal anywhere.
report:  ## Standing corpus measurements. Expected to be non-zero; informational.
	$(PYTHON) scripts/check_reproductions.py --corpus --strict
	$(PYTHON) scripts/audit_verifications.py

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
# The pathspec covers every directory `data` writes. site/public matters and is easy to miss:
# build-data.js copies the exports and design notes the site serves for download, so leaving
# it out means the published files can disagree with the exports they were copied from —
# exactly the drift build-data.js says in its own comments that it exists to prevent.
# exports/ is excluded because `data` does not write it — see the note above. site/public is
# included because build-data.js copies the served exports and design notes there, and a stale
# copy means the files the site offers for download disagree with the ones they came from.
GENERATED := site/src/data site/public review
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
