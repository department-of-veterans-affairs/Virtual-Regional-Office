.SHELLFLAGS := -eu -o pipefail -c
SHELL := bash
POETRY:=$$(which poetry || echo "install poetry. see https://python-poetry.org/")

SAM ?= sam

.PHONY: build.requirements.txt
build.requirements.txt:
	cd ./lambda ; \
	$(POETRY) export --without-hashes -f requirements.txt -o requirements.txt --with-credentials ;

.PHONY: build.plan.b
build.plan.b:
	cd ./lambda ; \
	$(POETRY) install ; \
