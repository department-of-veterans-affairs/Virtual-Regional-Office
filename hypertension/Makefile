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
clean-main: ## Delete SAM build output of main SAM/CF stack
	$(info [*] Destroying environment....)
	rm -rf ./.aws-sam/

.PHONY: clean-layers
clean-layers: ## Delete SAM build output and misc files of layers SAM/CF stack
	rm -rf ./$(AWS_LAMBDA_LAYERS_DIR)/.aws-sam/; \
	rm -rf ./$(AWS_LAMBDA_LAYERS_DIR)/vro--wkhtmltopdf/; \
	rm -rf ./$(PYTHON_DEPENDENCIES_LAYER_DIR); \
	rm ./$(STACK_DEPLOYMENT_SCRIPTS_DIR)/wkhtmltox*;

# Notice that when building for SAM and deploying via SAM, to get your packages right, SAM only
# depends on a proper requirements.txt; not the poetry virtual environment dir, for example.
.PHONY: build-main
build-main: ## `sam build` the main SAM/CloudFormation stack and sets SAM parameter overrides in samconfig.toml
	$(SAM) build
	cd ./$(PYTHON_PROJECT_DIR) ; \
	$(POETRY) run python set_parameter_overrides.py ;

.PHONY: poetry-install-deploy-tool
poetry-install-deploy-tool: ## Run poetry install for the deployment tools' dependencies
	cd $(STACK_DEPLOYMENT_SCRIPTS_DIR) ; \
	$(POETRY) install; \
	cd ..; \

.PHONY: download-wkhtmltopdf
download-wkhtmltopdf: ## Download the wkhtmltopdf binary, for later upload to Lambda Layer
	cd $(STACK_DEPLOYMENT_SCRIPTS_DIR); \
	$(POETRY) run python ./download_wkhtmltopdf.py; \
	cd ..; \

.PHONY: build-layers
build-layers: ## `sam build` the layers SAM/CF stack
	cd $(AWS_LAMBDA_LAYERS_DIR); \
	$(SAM) build; \
	cd ..; \

.PHONY: create-requirements.txt
create-requirements.txt: ## Create requirements.txt file in python dependencies layer, from py-root/ Poetry dependencies
	mkdir -p $(PYTHON_DEPENDENCIES_LAYER_DIR); \
	cd ./$(PYTHON_PROJECT_DIR) ; \
	$(POETRY) export --without-hashes -f requirements.txt -o ../$(PYTHON_DEPENDENCIES_LAYER_DIR)/requirements.txt --with-credentials ; \
	cd ..; \

.PHONY: lint
lint: ## Run pylint, flake8, and black
	cd ./$(PYTHON_PROJECT_DIR) ; \
	$(POETRY) run pylint *.py ; \
	$(POETRY) run pylint lib/*.py ; \
	$(POETRY) run pylint test/*.py ; \
	$(POETRY) run pylint test/data/*.py ; \
	$(POETRY) run pylint test/doubles/*.py ; \
	$(POETRY) run flake8 --exclude=.venv ; \
	$(POETRY) run black . --exclude=/\.venv/ ;
	cd .. ; \

.PHONY: poetry-install-py-root
poetry-install-py-root: ## Run poetry install in py-root/ directory
	cd ./$(PYTHON_PROJECT_DIR) ; \
	$(POETRY) install ; \
	cd .. ; \

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
update-poetry: ## Update Poetry version (as workaround for VersionUnion bug. See comment in Makefile.)
	cd ./$(PYTHON_PROJECT_DIR) ; \
	$(POETRY) --version ; \
	$(POETRY) self update ; \
	$(POETRY) --version ; \
	cd .. ; \

.PHONY: add-layers-to-main-template
add-layers-to-main-template:
	cd ./$(STACK_DEPLOYMENT_SCRIPTS_DIR); \
	$(POETRY) run python add_deployed_layers_to_template.py --overwrite; \
	cd ..; \

.PHONY: test
test: ## Poetry install py-root/, link, and pytest with watch enabled
	make poetry-install-py-root ; \
	make lint ; \
	make test-only ; \

.PHONY: test-only
test-only: ## Pytest with watch enabled. No other steps.
	cd ./$(PYTHON_PROJECT_DIR) ; \
	$(POETRY) run ptw -c -- --capture=no ;

.PHONY: test-ci
test-ci: ## Update poetry (see comment on update-poetry command) and run the unit tests with no watch on the pytest. (Intended for use by CI tools.)
	make update-poetry ; \
  make poetry-install-py-root ; \
	make lint ; \
	cd ./$(PYTHON_PROJECT_DIR) ; \
	$(POETRY) run pytest --capture=no ;

# The lambda layers need to be deployed to AWS with their arns
# set in the environment file for this command to be successful
.PHONY: invoke-sam-local
invoke-sam-local: ## `sam local invoke`, for testing.
	$(SAM) build
	$(SAM) local invoke --parameter-overrides '$(shell cat cf-template-params.env)' -e $(PYTHON_PROJECT_DIR)/pdf-event.json

.PHONY: deploy-main-guided
deploy-main-guided: ## Build and `sam deploy --guided` the main SAM/CF stack.
	make build-main ; \
	$(SAM) deploy --guided --capabilities CAPABILITY_NAMED_IAM

# should only be run if the function/layers aren't already deployed to the same environment
# deploy layers first and then the lambda function - this
# should be done after setting up the KMS key for the first time
.PHONY: deploy-layers-guided
deploy-layers-guided: ## `sam deploy --guided` the layers SAM/CF stack.
	cd $(AWS_LAMBDA_LAYERS_DIR); \
	$(SAM) deploy --guided; \
	cd ..; \

.PHONY: deploy-main
deploy-main: ## Build and `sam deploy` (not guided) the main SAM/CF stack
	make build-main ; \
	$(SAM) deploy --no-confirm-changeset --capabilities CAPABILITY_NAMED_IAM

# SHOULD BE RUN FOR DEPLOYMENT OF THE LAMBDA STACK (INCLUDING LAYERS)
# TO A NEW ENVIRONMENT.
#
# Can also be run if updates to the layers have been made and are
# ready to be used in the lambda function - this will deploy those updates
# and update the layer versions within the function's template.yml
#
# BEFORE RUNNING: ensure the manual steps have been completed for initial deployment [see README]
#
# Deploys layers first and then the lambda function
.PHONY: deploy-all-guided
deploy-all-guided: ## Build everything and `sam deploy --guided` both SAM/CF stacks.
	make create-requirements.txt; \
	make poetry-install-deploy-tool; \
	make download-wkhtmltopdf; \
	make build-layers; \
	make deploy-layers-guided; \
	make add-layers-to-main-template; \
	make deploy-main-guided; \
	make clean-layers; \
