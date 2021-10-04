.SHELLFLAGS := -eu -o pipefail -c
SHELL := bash
POETRY:=$$(which poetry || echo "install poetry. see https://python-poetry.org/")

SAM ?= sam

PYTHON_PROJECT_DIR:=py-root
AWS_LAMBDA_LAYERS_DIR:=layers
PYTHON_DEPENDENCIES_LAYER_DIR:=$(AWS_LAMBDA_LAYERS_DIR)/vro--python-dependencies-layer
STACK_DEPLOYMENT_SCRIPTS_DIR:=stack_deployment

.PHONY: clean
clean: ##=> Deletes current build environment and latest build
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
build.sam:
	$(SAM) build
	cd ./${PYTHON_PROJECT_DIR} ; \
	$(POETRY) run python set_parameter_overrides.py ;

.PHONY: build.stack.deployment.requirements
build.stack.deployment.requirements: build.requirements
	cd $(STACK_DEPLOYMENT_SCRIPTS_DIR) ; \
	$(POETRY) export --without-hashes -f requirements.txt -o requirements.txt; \
	$(POETRY) install; \
	cd ..; \

.PHONY: download.wkhtmltopdf
download.wkhtmltopdf:
	cd $(STACK_DEPLOYMENT_SCRIPTS_DIR); \
	$(POETRY) run python ./download_wkhtmltopdf.py; \
	cd ..; \

.PHONY: create.directory
create.directory:
	mkdir -p $(PYTHON_DEPENDENCIES_LAYER_DIR); \

.PHONY: build.sam.layers
build.sam.layers:
	cd ./$(PYTHON_DEPENDENCIES_LAYER_DIR); \
	pip install -r requirements.txt; \
	cd ..; \
	$(SAM) build; \
	cd ..; \

.PHONY: build.requirements
build.requirements:
	make create.directory; \
	cd ./${PYTHON_PROJECT_DIR} ; \
	$(POETRY) export --without-hashes -f requirements.txt -o ../$(PYTHON_DEPENDENCIES_LAYER_DIR)/requirements.txt --with-credentials ; \
	cd ..; \

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

.PHONY: update.function.template.layers
update.function.template.layers:
	cd ./$(STACK_DEPLOYMENT_SCRIPTS_DIR); \
	$(POETRY) run python add_deployed_layers_to_template.py --overwrite; \
	cd ..; \

.PHONY: pytest
pytest: build.local
	cd ./${PYTHON_PROJECT_DIR} ; \
	$(POETRY) run ptw -c -- --capture=no ;

# The lambda layers need to be deployed to AWS with their arns
# set in the environment file for this command to be successful
.PHONY: invoke.sam.local
invoke.sam.local:
	$(SAM) build
	$(SAM) local invoke --parameter-overrides '$(shell cat cf-template-params.env)' -e $(PYTHON_PROJECT_DIR)/pdf-event.json

.PHONY: deploy.sam.guided
deploy.sam.guided: build.sam ##=> Guided deploy that is typically run for the first time only
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
deploy.sam: build.sam ##=> Deploy app using previously saved SAM CLI configuration
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
deploy.stack: build.stack.deployment.requirements
	make download.wkhtmltopdf; \
	make build.sam.layers; \
	make deploy.sam.layers.guided; \
	make update.function.template.layers; \
	make deploy.sam.guided; \
	make clean.layers; \
