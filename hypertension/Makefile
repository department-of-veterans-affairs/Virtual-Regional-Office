CODE_COVERAGE = 75
POETRY ?= poetry 
SAM ?= sam
DOCKER ?= docker
BREW ?= brew
PYENV ?= pyenv
POETRY_VERSION := 1.1.4

target:
	$(info ${HELP_MESSAGE})
	@exit 0

clean: ##=> Deletes current build environment and latest build
	$(info [*] Destroying environment....)
	rm -rf ./.aws-sam/

Darwin:
	$(info [*] Installing necessary packages...)
	$(BREW) update 
	$(BREW) install pyenv
	curl -sSL https://raw.githubusercontent.com/sdispater/poetry/${POETRY_VERSION}/get-poetry.py | python
	$(PYENV) install

all: clean build

install:
	$(info [*] Installing pyenv (assumes MacOS))
	$(MAKE) Darwin
	$(MAKE) dev

dev:
	$(info [*] Installing poetry project dependencies)
	$(POETRY) install

shell:
	$(POETRY) shell

build: ##=> Same as package except that we don't create a ZIP
	$(SAM) build --use-container

deploy.guided: ##=> Guided deploy that is typically run for the first time only
	$(SAM) deploy --guided

deploy: ##=> Deploy app using previously saved SAM CLI configuration
	$(SAM) deploy

test:
	$(POETRY) run pytest --capture=no --verbose --cov=functions --cov-report=xml --junitxml=test.xml --cov-report term-missing --cov-fail-under $(CODE_COVERAGE) 

local:
	$(DOCKER) pull amazon/aws-stepfunctions-local
	$(DOCKER) run -p 8083:8083 amazon/aws-stepfunctions-local

ci: ##=> Run full workflow - Install deps, build deps, and deploy
	$(MAKE) dev
	$(MAKE) test
	$(MAKE) build
	$(MAKE) deploy

define HELP_MESSAGE
	Environment variables to be aware of or to hardcode depending on your use case:

	NETWORK
		Default: ""
		Info: Docker Network to connect to when running Lambda function locally

	Common usage:

	...::: Installs poetry, application and dev dependencies defined in pyproject.toml :::...
	$ make install

	...::: Builds Lambda function dependencies:::...
	$ make build

	...::: Deploy for the first time :::...
	$ make deploy.guided

	...::: Deploy subsequent changes :::...
	$ make deploy

	...::: Run Pytest under tests/ with poetry :::...
	$ make test

	...::: Spawn a virtual environment shell :::...
	$ make shell

	...::: Cleans up the environment - Deletes Virtualenv, ZIP builds and Dev env :::...
	$ make clean

endef