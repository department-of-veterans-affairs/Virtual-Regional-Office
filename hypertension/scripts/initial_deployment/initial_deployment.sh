#!/usr/bin/env bash

# This script is intended to be used for the initial deployment
# of the lambda stack, including layers, into a new AWS environment.
#
# BEFORE YOU RUN: ensure you've followed all initial deployment manual steps
# referenced in the README before running. SEE BELOW for how to run this script.
#
# HOW TO RUN: enter `make deploy.initial` on the command line
# from the root directory containing the Makefile [currently, 'hypertension']

INITIAL_DEPLOYMENT_PATH=scripts/initial_deployment

make build.initial.deployment.requirements
cd $INITIAL_DEPLOYMENT_PATH
python ./download_wkhtmltopdf.py
eval `python establish_aws_mfa_session.py`
make -C ../.. build.sam.layers
make -C ../.. deploy.sam.layers.guided
cd .venv
source bin/activate
cd ..
python add_deployed_layers_to_template.py --overwrite
make -C ../.. deploy.sam.guided
