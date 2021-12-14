.SHELLFLAGS := -eu -o pipefail -c
SHELL := bash
POETRY ?= poetry
SAM ?= sam

PYTHON_PROJECT_DIR := py-root

# Based on solution here: https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html and https://news.ycombinator.com/item?id=11195539
help: ## Print out documentation for available commands.
	@awk -F ':|##' \
		'/^[^\t].+?:.*?##/ {\
			printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF \
		}' $(MAKEFILE_LIST)

.PHONY: poetry-install
poetry-install: ## Run poetry install in the `py-root/` directory.
	cd ./$(PYTHON_PROJECT_DIR); \
	$(POETRY) install; \
	cd ..; \

.PHONY: test
test: ## Pytest with watch enabled. No other steps.
	cd ./$(PYTHON_PROJECT_DIR); \
	$(POETRY) run ptw -c -- --capture=no;

.PHONY: build
build: ## Poetry install and sam build.
	make poetry-install
	$(SAM) build

.PHONY: deploy-guided
deploy-guided: ## Build and sam deploy --guided.
	make build
	$(SAM) deploy --guided --capabilities CAPABILITY_NAMED_IAM

.PHONY: deploy
deploy: ## Build and sam deploy.
	make build
	$(SAM) deploy
