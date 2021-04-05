.SHELLFLAGS := -eu -o pipefail -c
SHELL := bash
POETRY:=$$(which poetry || echo "install poetry. see https://python-poetry.org/")

SAM ?= sam

.PHONY: build.plan.b
build.plan.b:
	cd ./lambda ; \
	$(POETRY) install ; \

.PHONY: build.requirements.txt
build.requirements.txt: build.plan.b
	cd ./lambda ; \
	$(POETRY) export --without-hashes -f requirements.txt -o requirements.txt --with-credentials ;

.PHONY: build.sam.local
build.sam.local: build.requirements.txt
	$(SAM) build --template template-local.yaml

.PHONY: build.sam.cloud
build.sam.cloud: build.requirements.txt
	$(SAM) build
