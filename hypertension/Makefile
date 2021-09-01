.SHELLFLAGS := -eu -o pipefail -c
SHELL := bash
POETRY:=$$(which poetry || echo "install poetry. see https://python-poetry.org/")

SAM ?= sam

PYTHON_PROJECT_DIR:=py-root

.PHONY: clean
clean: ##=> Deletes current build environment and latest build
	$(info [*] Destroying environment....)
	rm -rf ./.aws-sam/

# Notice that when building for SAM and deploying via SAM, to get your packages right, SAM only
# depends on a proper requirements.txt; not the poetry virtual environment dir, for example.
.PHONY: build.sam
build.sam: build.requirements
	$(SAM) build
	cd ./${PYTHON_PROJECT_DIR} ; \
	$(POETRY) run python set_parameter_overrides.py ;

.PHONY: build.requirements
build.requirements:
	cd ./${PYTHON_PROJECT_DIR} ; \
	$(POETRY) export --without-hashes -f requirements.txt -o requirements.txt --with-credentials ;

.PHONY: build.local
build.local:
	cd ./${PYTHON_PROJECT_DIR} ; \
	$(POETRY) install ; \
	$(POETRY) run pylint *.py ; \
	$(POETRY) run pylint lib/*.py ; \
	$(POETRY) run pylint test/*.py ; \
	$(POETRY) run pylint test/data/*.py ; \
	$(POETRY) run pylint test/doubles/*.py ; \
	$(POETRY) run flake8 --exclude=.venv ; \
	$(POETRY) run black . --exclude=/\.venv/ ;

.PHONY: pytest
pytest: build.local
	cd ./${PYTHON_PROJECT_DIR} ; \
	$(POETRY) run ptw -c -- --capture=no ;

.PHONY: deploy.sam.guided
deploy.sam.guided: build.sam ##=> Guided deploy that is typically run for the first time only
	$(SAM) deploy --guided --capabilities CAPABILITY_NAMED_IAM

.PHONY: deploy.sam
deploy.sam: build.sam ##=> Deploy app using previously saved SAM CLI configuration
	$(SAM) deploy --no-confirm-changeset --capabilities CAPABILITY_NAMED_IAM
