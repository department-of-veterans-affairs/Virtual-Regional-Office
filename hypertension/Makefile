.SHELLFLAGS := -eu -o pipefail -c
SHELL := bash
POETRY:=$$(which poetry || echo "install poetry. see https://python-poetry.org/")

SAM ?= sam

PYTHON_PROJECT_DIR:=py-root
AWS_LAMBDA_LAYERS_DIR:=layers
PYTHON_DEPENDENCIES_LAYER_DIR:=$(AWS_LAMBDA_LAYERS_DIR)/vro--python-dependencies-layer
STACK_DEPLOYMENT_SCRIPTS_DIR:=stack_deployment

# Based on solution here: https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html and https://news.ycombinator.com/item?id=11195539
help:  ## Prints out documentation for available commands
	@awk -F ':|##' \
		'/^[^\t].+?:.*?##/ {\
			printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF \
		}' $(MAKEFILE_LIST)

.PHONY: clean
clean: ## Deletes SAM build output
	$(info [*] Destroying environment....)
	rm -rf ./.aws-sam/

.PHONY: clean.layers
clean.layers:
	rm -rf ./$(AWS_LAMBDA_LAYERS_DIR)/.aws-sam/; \
	rm -rf ./$(AWS_LAMBDA_LAYERS_DIR)/vro--wkhtmltopdf/; \
	rm -rf ./$(PYTHON_DEPENDENCIES_LAYER_DIR); \
	rm ./$(STACK_DEPLOYMENT_SCRIPTS_DIR)/wkhtmltox*;

# Notice that when building for SAM and deploying via SAM, to get your packages right, SAM only
# depends on a proper requirements.txt; not the poetry virtual environment dir, for example.
.PHONY: build.sam
build.sam: ## `sam build`s the main SAM/CloudFormation stack and sets SAM parameter overrides in samconfig.toml
	$(SAM) build
	cd ./${PYTHON_PROJECT_DIR} ; \
	$(POETRY) run python set_parameter_overrides.py ;

.PHONY: build.stack.deployment.requirements
build.stack.deployment.requirements: ## `sam build` the Layers SAM/CloudFormation stack
	make build.requirements ; \
	cd $(STACK_DEPLOYMENT_SCRIPTS_DIR) ; \
	$(POETRY) export --without-hashes -f requirements.txt -o requirements.txt; \
	$(POETRY) install; \
	cd ..; \

.PHONY: download.wkhtmltopdf
download.wkhtmltopdf:
	cd $(STACK_DEPLOYMENT_SCRIPTS_DIR); \
	$(POETRY) run python ./download_wkhtmltopdf.py; \
	cd ..; \

.PHONY: build.sam.layers
build.sam.layers:
	cd ./$(PYTHON_DEPENDENCIES_LAYER_DIR); \
	pip install -r requirements.txt; \
	cd ..; \
	$(SAM) build; \
	cd ..; \

.PHONY: build.requirements
build.requirements:
	mkdir -p $(PYTHON_DEPENDENCIES_LAYER_DIR); \
	cd ./${PYTHON_PROJECT_DIR} ; \
	$(POETRY) export --without-hashes -f requirements.txt -o ../$(PYTHON_DEPENDENCIES_LAYER_DIR)/requirements.txt --with-credentials ; \
	cd ..; \

.PHONY: lint
lint: ## Runs pylint, flake8, and black
	cd ./${PYTHON_PROJECT_DIR} ; \
	$(POETRY) run pylint *.py ; \
	$(POETRY) run pylint lib/*.py ; \
	$(POETRY) run pylint test/*.py ; \
	$(POETRY) run pylint test/data/*.py ; \
	$(POETRY) run pylint test/doubles/*.py ; \
	$(POETRY) run flake8 --exclude=.venv ; \
	$(POETRY) run black . --exclude=/\.venv/ ;
	cd .. ; \

.PHONY: install-and-lint
install-and-lint: ## Runs poetry install and Makefile lint job
	cd ./${PYTHON_PROJECT_DIR} ; \
	$(POETRY) install ; \
	cd .. ; \
	make lint; \

# TODO: The version of poetry that is a part of the Circle CI python image produces error
# "[TypeError] unhashable type: 'VersionUnion'" (in our repo, due to some code in PR #21)
# I think this error happens during our `$(POETRY) install` command.
# Notice a person on the following thread said the got around this VersionUnion problem by upgrading
# poetry:
# https://github.com/python-poetry/poetry/issues/2340
# Also, sure enough, the Circle CI python image has a bit old version of poetry.
# So, we are copying this person's workaround and by doing `$(POETRY) self update` to have the
# Circle CI python image upgrade its poetry version. It works!
# After the Circle CI people update the Circle CI python image with a newer version of poetry
# (and this problem is gone), completely get rid of our update-poetry command, and change pytest.ci to
# depend only on install-and-lint instead.
# For an example of the Circle CI people maintaining their python image to fix a different issue,
# see:
# https://github.com/circleci/circleci-images/issues/335
# https://github.com/CircleCI-Public/circleci-dockerfiles/blob/master/python/images/3.7.2-stretch/Dockerfile#L81
# https://github.com/circleci/circleci-images/pull/336
.PHONY: update-poetry
update-poetry:
	cd ./${PYTHON_PROJECT_DIR} ; \
	$(POETRY) --version ; \
	$(POETRY) self update ; \
	$(POETRY) --version ; \
	cd .. ; \

.PHONY: update.function.template.layers
update.function.template.layers:
	cd ./$(STACK_DEPLOYMENT_SCRIPTS_DIR); \
	$(POETRY) run python add_deployed_layers_to_template.py --overwrite; \
	cd ..; \

.PHONY: build.and.pytest
build.and.pytest:
	make install-and-lint ; \
	cd ./${PYTHON_PROJECT_DIR} ; \
	$(POETRY) run ptw -c -- --capture=no ;

.PHONY: pytest
pytest:
	cd ./${PYTHON_PROJECT_DIR} ; \
	$(POETRY) run ptw -c -- --capture=no ;

.PHONY: pytest.ci
pytest.ci: ## Updates poetry (see comment on update-poetry command) and runs the unit tests with no watch on the pytest. (Intended for use by CI tools.)
	make update-poetry ; \
  make install-and-lint ; \
	cd ./${PYTHON_PROJECT_DIR} ; \
	$(POETRY) run pytest --capture=no ;

# The lambda layers need to be deployed to AWS with their arns
# set in the environment file for this command to be successful
.PHONY: invoke.sam.local
invoke.sam.local:
	$(SAM) build
	$(SAM) local invoke --parameter-overrides '$(shell cat cf-template-params.env)' -e $(PYTHON_PROJECT_DIR)/pdf-event.json

.PHONY: deploy.sam.guided
deploy.sam.guided: ## Guided deploy that is typically run for the first time only
	make build.sam ; \
	$(SAM) deploy --guided --capabilities CAPABILITY_NAMED_IAM

# should only be run if the function/layers aren't already deployed to the same environment
# deploy layers first and then the lambda function - this
# should be done after setting up the KMS key for the first time
.PHONY: deploy.sam.layers.guided
deploy.sam.layers.guided:
	cd ${AWS_LAMBDA_LAYERS_DIR}; \
	$(SAM) deploy --guided; \
	cd ..; \

.PHONY: deploy.sam
deploy.sam: ## Deploy app using previously saved SAM CLI configuration
	make build.sam ; \
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
.PHONY: deploy.stack
deploy.stack:
	make build.stack.deployment.requirements; \
	make download.wkhtmltopdf; \
	make build.sam.layers; \
	make deploy.sam.layers.guided; \
	make update.function.template.layers; \
	make deploy.sam.guided; \
	make clean.layers; \
