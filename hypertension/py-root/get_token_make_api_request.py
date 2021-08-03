import argparse

from typing import Union

from dotenv import load_dotenv

from lib.utils import load_config
from lib.lighthouse import (
    authenticate_to_lighthouse,
    fetch_observation_data
)

load_dotenv('../cf-template-params.env')

Json = Union[dict, list]

"""
Usage example:
    python get_token_make_api_request.py 000aaa ./private.pem \
        assertion-params.json observation-request-params.json 123456789

This script expects the following arguments, in order:

    client_id: the client_id associated with your authorization.
    key_loc: the location of a private .pem file or the name of an environment
        variable containing the key.
    assertions_file: the location of a JSON file containing a dictionary with
        the following structure:

            urls:
                audience: the aud value (a URL) for the JWT.
                token_url: the URL of the endpoint for requesting a token from.
            parameters:
                grant_type: the kind of credentials you want.
                client_assertion_type: e.g.
                    "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"
                scope: the various permisions you're requesting.

    params_file: the location of a JSON file containing the params of your
        request to the API, with the following structure:
            urls:
                endpoint: the URL of the API endpoint to query.
            parameters:
                [any keys and values here will be passed to the enpoint as
                parameters]

    icn: the ICN of the individual to query for.

The JSON files in this directory are samples and should be altered as
necessary.
"""


def cli_main() -> None:
    cli_options = get_cli_args()
    config = load_config(cli_options.icn, cli_options.key_loc)

    icn = config["lighthouse"]["icn"]

    access_token = authenticate_to_lighthouse(config["lighthouse"]["auth"], icn)

    observation_response = fetch_observation_data(config["lighthouse"]["vet_health_api_observation"], icn, access_token)

    handle_api_response(observation_response)


def get_cli_args() -> argparse.Namespace:
    return setup_cli_parser().parse_args()


def setup_cli_parser() -> argparse.ArgumentParser:
    # Configures argument parsing. See above for expected arguments.
    parser = argparse.ArgumentParser()
    args = [
        "client_id",
        "key_loc",
        "assertions_file",
        "params_file",
        "icn",
    ]

    for arg in args:
        parser.add_argument(arg, type=str)

    return parser


def handle_api_response(api_response: Json) -> None:
    print(api_response)


if __name__ == "__main__":
    cli_main()
