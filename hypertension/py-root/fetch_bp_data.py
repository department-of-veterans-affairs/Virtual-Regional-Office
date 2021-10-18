import os
import argparse

from typing import Union

from dotenv import load_dotenv

from lib.utils import load_config
from lib.lighthouse import authenticate_to_lighthouse, fetch_observation_data

load_dotenv("../.env")

Json = Union[dict, list]

"""
Usage example:
    python fetch_bp_data.py 000aaa ./private.pem \
        assertion-params.json observation-request-params.json 123456789

This script depends on the env variables you set in .env

This script expects the following arguments, in order:

    icn: the ICN of the individual to query for.

"""


def cli_main() -> None:
    cli_options = get_cli_args()
    config = load_config(
        cli_options.icn, os.environ["LighthousePrivateRsaKeyFilePath"]
    )

    icn = config["lighthouse"]["icn"]

    access_token = authenticate_to_lighthouse(
        config["lighthouse"]["auth"], icn
    )

    observation_response = fetch_observation_data(
        config["lighthouse"]["vet_health_api_observation"], icn, access_token
    )

    handle_api_response(observation_response)


def get_cli_args() -> argparse.Namespace:
    return setup_cli_parser().parse_args()


def setup_cli_parser() -> argparse.ArgumentParser:
    # Configures argument parsing. See above for expected arguments.
    parser = argparse.ArgumentParser()
    args = ["icn"]

    for arg in args:
        parser.add_argument(arg, type=str)

    return parser


def handle_api_response(api_response: Json) -> None:
    print(api_response)


if __name__ == "__main__":
    cli_main()
