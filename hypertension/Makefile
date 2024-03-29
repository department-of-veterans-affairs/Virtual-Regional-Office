.SHELLFLAGS := -eu -o pipefail -c
SHELL := bash
POETRY:=$$(which poetry || echo "install poetry. see https://python-poetry.org/")

SAM ?= sam

PYTHON_PROJECT_DIR:=py-root
AWS_LAMBDA_LAYERS_DIR:=layers
PYTHON_DEPENDENCIES_LAYER_DIR:=$(AWS_LAMBDA_LAYERS_DIR)/vro--python-dependencies-layer
STACK_DEPLOYMENT_SCRIPTS_DIR:=stack_deployment

# Based on solution here: https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html and https://news.ycombinator.com/item?id=11195539
help: ## Print out documentation for available commands
	@awk -F ':|##' \
		'/^[^\t].+?:.*?##/ {\
			printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF \
		}' $(MAKEFILE_LIST)

.PHONY: clean-main
clean-main: ## Delete SAM build output of main SAM/CF stack.
	$(info [*] Destroying environment....)
	rm -rf ./.aws-sam/

.PHONY: clean-layers
clean-layers: ## Delete SAM build output and miscellaneous files of layers SAM/CF stack.
	rm -rf ./$(AWS_LAMBDA_LAYERS_DIR)/.aws-sam/; \
	rm -rf ./$(AWS_LAMBDA_LAYERS_DIR)/vro--wkhtmltopdf/; \
	rm -rf ./$(PYTHON_DEPENDENCIES_LAYER_DIR); \
	rm ./$(STACK_DEPLOYMENT_SCRIPTS_DIR)/wkhtmltox*;

.PHONY: build-main
build-main: ## `sam build` the main SAM/CloudFormation stack and set SAM parameter overrides in samconfig.toml.
	make set-layer-env-vars; \
	$(SAM) build
	make set-parameter-overrides;

.PHONY: poetry-install-deploy-tool
poetry-install-deploy-tool: ## Run poetry install for the deployment tools' dependencies.
	cd $(STACK_DEPLOYMENT_SCRIPTS_DIR); \
	$(POETRY) install; \
	cd ..; \

.PHONY: set-parameter-overrides
set-parameter-overrides: # Uses your env vars to set the parameter_overrides value in the main SAM/CF stack's samconfig.toml
	make poetry-install-py-root; \
	cd ./$(PYTHON_PROJECT_DIR); \
	$(POETRY) run python set_parameter_overrides.py;
	cd ..; \

.PHONY: download-wkhtmltopdf
download-wkhtmltopdf: ## Download the wkhtmltopdf binary, for later upload to Lambda Layer.
	cd $(STACK_DEPLOYMENT_SCRIPTS_DIR); \
	$(POETRY) run python ./download_wkhtmltopdf.py; \
	cd ..; \

.PHONY: build-layers
build-layers: ## Build the layers SAM/CF stack (the content and `sam build`)
	make create-requirements.txt; \
	make download-wkhtmltopdf; \
	cd $(AWS_LAMBDA_LAYERS_DIR); \
	$(SAM) build; \
	cd ..; \

.PHONY: create-requirements.txt
create-requirements.txt: ## Create requirements.txt file in python dependencies layer, from `py-root/` Poetry dependencies.
	mkdir -p $(PYTHON_DEPENDENCIES_LAYER_DIR); \
	cd ./$(PYTHON_PROJECT_DIR); \
	$(POETRY) export --without-hashes -f requirements.txt -o ../$(PYTHON_DEPENDENCIES_LAYER_DIR)/requirements.txt --with-credentials; \
	cd ..; \

.PHONY: lint
lint: ## Run pylint, flake8, and black.
	cd ./$(PYTHON_PROJECT_DIR); \
	$(POETRY) run pylint *.py; \
	$(POETRY) run pylint lib/*.py; \
	$(POETRY) run pylint test/*.py; \
	$(POETRY) run pylint test/data/*.py; \
	$(POETRY) run pylint test/doubles/*.py; \
	$(POETRY) run flake8 --exclude=.venv; \
	$(POETRY) run black . --exclude=/\.venv/;
	cd ..; \

.PHONY: poetry-install-py-root
poetry-install-py-root: ## Run poetry install in the `py-root/` directory.
	cd ./$(PYTHON_PROJECT_DIR); \
	$(POETRY) install; \
	cd ..; \

# TODO: The version of poetry that is a part of the Circle CI python image produces error
# "[TypeError] unhashable type: 'VersionUnion'" (in our repo, due to some code in PR #21)
# I think this error happens during our `$(POETRY) install` command.
# Notice a person on the following thread said the got around this VersionUnion problem by upgrading
# poetry:
# https://github.com/python-poetry/poetry/issues/2340
# Also, sure enough, the Circle CI python image cimg/python:3.8.6 has an old version of poetry.
# So, we are copying this person's workaround and by doing `$(POETRY) self update` to have the
# Circle CI python image upgrade its poetry version. It works!
# After our repo upgrades from Python 3.8.6 to 3.9.7, the problem
# will be gone (because cimg/python:3.9.7 has a version of Poetry that doesn't have this bug),
# completely get rid of our update-poetry command, and change test-ci to depend only on
# poetry-install-py-root and lint instead.
.PHONY: update-poetry
update-poetry: ## Update Poetry version, as workaround for VersionUnion bug. See comment in Makefile.
	cd ./$(PYTHON_PROJECT_DIR); \
	$(POETRY) --version; \
	$(POETRY) self update; \
	$(POETRY) --version; \
	cd ..; \

.PHONY: set-layer-env-vars
set-layer-env-vars: ## Set Lambda Layer ARNs env vars based on the ARNs of the layers deployed in the layers stack.
	cd ./$(STACK_DEPLOYMENT_SCRIPTS_DIR); \
	$(POETRY) run python set_layer_env_vars.py --overwrite; \
	cd ..; \

.PHONY: test
test: ## Poetry install `py-root/`, lint, and pytest with watch enabled.
	make poetry-install-py-root; \
	make lint; \
	make test-only; \

.PHONY: test-only
test-only: ## Pytest with watch enabled. No other steps.
	cd ./$(PYTHON_PROJECT_DIR); \
	$(POETRY) run ptw -c -- --capture=no;

.PHONY: test-ci
test-ci: ## Update poetry (see comment on update-poetry command) and run the unit tests with no watch on the pytest. (Intended for use by CI tools.)
	make update-poetry; \
  make poetry-install-py-root; \
	make lint; \
	cd ./$(PYTHON_PROJECT_DIR); \
	$(POETRY) run pytest --capture=no;

# The lambda layers need to be deployed to AWS (with their ARNs set, of course), for this to be successful
.PHONY: invoke-sam-local
invoke-sam-local: ## `sam local invoke`, for testing.
	$(SAM) build
	$(SAM) local invoke --parameter-overrides '$(shell cat .env)' -e $(PYTHON_PROJECT_DIR)/pdf-event.json

.PHONY: deploy-main-guided
deploy-main-guided: ## Build and `sam deploy --guided` the main SAM/CF stack.
	make build-main; \
	$(SAM) deploy --guided --capabilities CAPABILITY_NAMED_IAM

.PHONY: deploy-layers-guided
deploy-layers-guided: ## Build and `sam deploy --guided` the layers SAM/CF stack.
	make build-layers; \
	cd $(AWS_LAMBDA_LAYERS_DIR); \
	$(SAM) deploy --guided; \
	cd ..; \

.PHONY: deploy-main
deploy-main: ## Build and `sam deploy` (not guided) the main SAM/CF stack.
	make build-main; \
	$(SAM) deploy --no-confirm-changeset --capabilities CAPABILITY_NAMED_IAM

.PHONY: deploy-all-guided
deploy-all-guided: ## Build everything and `sam deploy --guided` both SAM/CF stacks. (Use this for your initial deployment of both stacks.)
	make poetry-install-deploy-tool; \
	make deploy-layers-guided; \
	make deploy-main-guided; \
