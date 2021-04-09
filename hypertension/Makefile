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
	$(MAKE) clean.sam
	$(MAKE) clean.asl

.PHONY: clean.sam
clean.sam:
	rm -rf ./.aws-sam/

.PHONY: clean.asl
clean.asl:
	rm -f build/hypertension.asl.json

.PHONY: build.sam
build.sam: build.requirements
	$(SAM) build

.PHONE: build.asl
build.asl: clean.asl ##=> Build the ASL file for Step Functions Local
	cp statemachine/hypertension.asl.json build/hypertension.asl.json
	# Interestingly, AWS_REGION can be null/empty string and everything works anyway.
	sed -i .tmp 's/$${ApplicabilityDeterminerFunctionArn}/arn:aws:lambda:$(AWS_REGION):012345678901:function:ApplicabilityDeterminerFunction/' build/hypertension.asl.json
	sed -i .tmp 's/$${MedicalRecordLocatorFunctionArn}/arn:aws:lambda:$(AWS_REGION):012345678901:function:MedicalRecordLocatorFunction/' build/hypertension.asl.json
	sed -i .tmp 's/$${MedicalDataRetrieverFunctionArn}/arn:aws:lambda:$(AWS_REGION):012345678901:function:MedicalDataRetrieverFunction/' build/hypertension.asl.json
	sed -i .tmp 's/$${ClaimClassifierFunctionArn}/arn:aws:lambda:$(AWS_REGION):012345678901:function:ClaimClassifierFunction/' build/hypertension.asl.json
	sed -i .tmp 's/$${RecordUpdaterFunctionArn}/arn:aws:lambda:$(AWS_REGION):012345678901:function:RecordUpdaterFunction/' build/hypertension.asl.json
	rm build/hypertension.asl.json.tmp

.PHONY: build.requirements
build.requirements:
	@for service in $(SERVICES) ; do \
		echo "Building requirements for $$service ..."; \
		cd ./${FUNCTIONS_DIR}/$${service} ; \
		$(POETRY) export --without-hashes -f requirements.txt -o requirements.txt --with-credentials ; \
		cd ../..; \
	done

.PHONY: build.python
build.python:
	@for service in $(SERVICES) ; do \
		echo "Installing requirements for $$service ..."; \
		cd ./${FUNCTIONS_DIR}/$${service} ; \
		$(POETRY) install ; \
		cd ../..; \
	done

.PHONY: test.python
test.python: build.python
	@for service in $(SERVICES) ; do \
		echo "Testing $$service ..."; \
		cd ./${FUNCTIONS_DIR}/$${service} ; \
		$(POETRY) run pytest --capture=no --verbose --cov=app --cov-report term-missing ; \
		cd ../..; \
	done

.PHONY: deploy.sam.guided
deploy.sam.guided: build.sam ##=> Guided deploy that is typically run for the first time only
	$(SAM) deploy --guided

.PHONY: deploy.sam
deploy.sam: build.sam ##=> Deploy app using previously saved SAM CLI configuration
	$(SAM) deploy
