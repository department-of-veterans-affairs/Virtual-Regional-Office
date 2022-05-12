import os
import argparse
import json

from dotenv import load_dotenv

from lib.utils import load_config
from lib.lighthouse import authenticate_to_lighthouse, fetch_lh_data

load_dotenv("../.env")

"""
Usage example:
    python fetch_cancer_data.py 000aaa ./private.pem \
        assertion-params.json observation-request-params.json 123456789
This script depends on the env variables you set in .env
This script expects the following arguments, in order:
    icn: the ICN of the individual to query for.
"""


def cli_main():
    cli_options = get_cli_args()
    config = load_config(
        cli_options.icn
    )

    icn = config["lighthouse"]["icn"]

    access_token = authenticate_to_lighthouse(
        config["lighthouse"]["auth"], icn
    )

    condition_response = fetch_lh_data(
        config["lighthouse"]["vet_health_api_condition"], icn, access_token
    )

    medication_response = fetch_lh_data(
        config["lighthouse"]["vet_health_api_medication"], icn, access_token
    )

    procedure_response = fetch_lh_data(
        config["lighthouse"]["vet_health_api_procedure"], icn, access_token
    )

    handle_api_response(
        {
            "condition_response": condition_response,
            "medication_response": medication_response,
            "procedure_response": procedure_response
        }
    )


def get_cli_args():
    return setup_cli_parser().parse_args()


def setup_cli_parser():
    # Configures argument parsing. See above for expected arguments.
    parser = argparse.ArgumentParser()
    args = ["icn"]

    for arg in args:
        parser.add_argument(arg, type=str)

    return parser


def handle_api_response(api_response):
    print(json.dumps(api_response, indent=2))


if __name__ == "__main__":
    cli_main()
