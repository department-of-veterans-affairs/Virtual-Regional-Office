.SHELLFLAGS := -eu -o pipefail -c
SHELL := bash
POETRY:=$$(which poetry || echo "install poetry. see https://python-poetry.org/")

SAM ?= sam

PYTHON_PROJECT_DIR:=vro-main
AWS_LAMBDA_LAYERS_DIR:=layers

.PHONY: clean
clean: ##=> Deletes current build environment and latest build
	$(info [*] Destroying environment....)
	rm -rf ./.aws-sam/

.PHONY: clean.layers
clean.layers:
	rm -rf ./layers/.aws-sam/; \
	rm -rf ./layers/vro--wkhtmltopdf/; \
	rm ./scripts/initial_deployment/wkhtmltox*;

# Notice that when building for SAM and deploying via SAM, to get your packages right, SAM only
# depends on a proper requirements.txt; not the poetry virtual environment dir, for example.
.PHONY: build.sam
build.sam:
	$(SAM) build

.PHONY: build.initial.deployment.requirements
build.initial.deployment.requirements: build.requirements
	cd ./scripts/initial_deployment ; \
	$(POETRY) export --without-hashes -f requirements.txt -o requirements.txt; \
	cd .venv ; \
	source bin/activate ; \
	cd ..; \
	$(POETRY) install; \
	cd ../..; \

.PHONY: build.sam.layers
build.sam.layers:
	cd ./${AWS_LAMBDA_LAYERS_DIR}/vro--python-dependencies-layer/; \
	pip install -r requirements.txt; \
	cd ..; \
	$(SAM) build; \
	cd ..; \


.PHONY: build.requirements
build.requirements:
	cd ./${PYTHON_PROJECT_DIR} ; \
	$(POETRY) export --without-hashes -f requirements.txt -o ../layers/vro--python-dependencies-layer/requirements.txt --with-credentials ; \
	cd ../..; \

.PHONY: build.local
build.local:
	cd ./${PYTHON_PROJECT_DIR} ; \
	$(POETRY) install ; \
	$(POETRY) run pylint *.py ; \
	$(POETRY) run pylint lib/*.py ; \
	$(POETRY) run pylint test/*.py ; \
	$(POETRY) run flake8 --exclude=.venv ; \
	$(POETRY) run black . --exclude=/\.venv/ ; \
	cd ../..; \

.PHONY: pytest
pytest: build.local
	cd ./${PYTHON_PROJECT_DIR} ; \
	$(POETRY) run ptw -c -- --capture=no ; \
	cd ../..; \

.PHONY: invoke.sam.local
invoke.sam.local: build.sam
	$(SAM) local invoke --parameter-overrides $$(cat cf-template-params.env) -e vro-main/pdf-event.json

.PHONY: deploy.sam.guided
deploy.sam.guided: build.sam ##=> Guided deploy that is typically run for the first time only
	$(SAM) deploy --guided --capabilities CAPABILITY_NAMED_IAM --parameter-overrides $$(cat cf-template-params.env)

# should only be run if the function/layers aren't already deployed to the same environment
# deploy layers first and then the lambda function - this
# should be done after setting up the KMS key for the first time
.PHONY: deploy.sam.layers.guided
deploy.sam.layers.guided:
	cd ./${AWS_LAMBDA_LAYERS_DIR}/; \
	$(SAM) deploy --guided; \
	cd ..; \

.PHONY: deploy.sam
deploy.sam: build.sam ##=> Deploy app using previously saved SAM CLI configuration
	$(SAM) deploy --no-confirm-changeset --capabilities CAPABILITY_NAMED_IAM --parameter-overrides $$(cat cf-template-params.env)

# ONLY RUN FOR INITIAL DEPLOYMENT OF THE LAMBDA STACK (INCLUDING LAYERS)
# TO A NEW ENVIRONMENT
#
# BEFORE RUNNING: ensure the manual steps have been completed for initial deployment [see README]
#
# Deploys layers first and then the lambda function
.PHONY: deploy.initial.stack
deploy.initial.stack:
	./scripts/initial_deployment/initial_deployment.sh
