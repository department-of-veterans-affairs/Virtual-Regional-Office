.SHELLFLAGS := -eu -o pipefail -c  
SHELL := bash
POETRY:=$$(which poetry || echo "install poetry. see https://python-poetry.org/")

SAM ?= sam
SERVICES:= applicability_determiner claim_classifier medical_data_retriever medical_record_locator record_updater
FUNCTIONS_DIR:=functions

all: build

.PHONY: clean
clean: ##=> Deletes current build environment and latest build
	$(info [*] Destroying environment....)
	rm -rf ./.aws-sam/

.PHONY: build
build: build.requirements
	$(SAM) build

.PHONY: build.requirements
build.requirements:
	@for service in $(SERVICES) ; do \
		echo "Building requirements for $$service ..."; \
		cd ./${FUNCTIONS_DIR}/$${service} ; \
		$(POETRY) export --without-hashes -f requirements.txt -o requirements.txt --with-credentials ; \
		cd ../..; \
	done

.PHONY: build.local
build.local:
	@for service in $(SERVICES) ; do \
		echo "Installing requirements for $$service ..."; \
		cd ./${FUNCTIONS_DIR}/$${service} ; \
		$(POETRY) install ; \
		cd ../..; \
	done

.PHONY: test.local
test.local: build.local
	@for service in $(SERVICES) ; do \
		echo "Testing $$service ..."; \
		cd ./${FUNCTIONS_DIR}/$${service} ; \
		$(POETRY) run pytest --capture=no --verbose --cov=app --cov-report term-missing ; \
		cd ../..; \
	done

.PHONY: deploy.guided
deploy.guided: build ##=> Guided deploy that is typically run for the first time only
	$(SAM) deploy --guided

.PHONY: deploy
deploy: build ##=> Deploy app using previously saved SAM CLI configuration
	$(SAM) deploy
