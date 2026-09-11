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

.PHONY: help data validate build preview check report fresh deps

help:  ## Show this help
	@grep -hE '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) \
	  | awk 'BEGIN{FS=":.*?## "}{printf "  \033[1m%-10s\033[0m %s\n", $$1, $$2}'

# `make data` used to fail here for anyone with a fresh checkout, because build-data.js
# needs the site's node modules and nothing installed them.
$(SITE)/node_modules:
	cd $(SITE) && npm ci

deps: $(SITE)/node_modules  ## Install the site's node modules

data: $(SITE)/node_modules  ## Regenerate everything under site/src/data and review/
	$(PYTHON) scripts/prediction_outcome.py --write
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

report:  ## Standing corpus measurements. Expected to be non-zero; informational.
	-$(PYTHON) scripts/check_reproductions.py --corpus --strict
	-$(PYTHON) scripts/audit_verifications.py

build: data  ## Regenerate data, then build the site
	cd $(SITE) && CORPUS=$(CORPUS) npx astro build

preview: build  ## Build and serve locally
	cd $(SITE) && npx astro preview

# The check that makes the rest of this file mean something. Regenerating must be a no-op on
# a clean tree; if it is not, the committed data does not match the corpus it claims to
# describe. CI runs this, so the failure surfaces in a pull request rather than on the
# published site.
fresh: data  ## Fail if regenerating changed anything that was committed
	@git diff --quiet -- site/src/data review || { \
	  echo ""; \
	  echo "Committed generated data is stale. Files that changed when regenerated:"; \
	  git diff --stat -- site/src/data review; \
	  echo ""; \
	  echo "Run 'make data' and commit the result."; \
	  exit 1; }
	@echo "Generated data matches the corpus."
