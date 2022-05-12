#!/usr/bin/env bash

# this is nothing but a wrapper around our python script which will export the AWS session credentials to the environment
# We need this because python won't export env variables to parent processes
# We can run this script as source to export the variables to the current shell
eval $(poetry run python establish_aws_mfa_session.py)
