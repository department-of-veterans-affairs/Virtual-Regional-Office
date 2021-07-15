import argparse
import datetime
import json
import os
from pathlib import Path
from typing import Union
from uuid import uuid1

import jwt
import requests

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
    config = load_config(True)

    icn = config["lighthouse"]["icn"]

    access_token = authenticate_to_lighthouse(config["lighthouse"]["auth"], icn)

    observation_response = fetch_observation_data(config["lighthouse"]["vet_health_api_observation"], icn, access_token)

    handle_api_response(observation_response)


__VRO_CONFIG__ = None
def load_config(running_as_script: bool) -> dict:
    global __VRO_CONFIG__
    if __VRO_CONFIG__ is None:
        if running_as_script:
            cli_options = get_cli_args()

            __VRO_CONFIG__ = {
                "lighthouse": {
                    "auth": {
                        **load_json(cli_options.assertions_file),
                        "secret": load_secret(cli_options.key_loc),
                        "client_id": cli_options.client_id
                    },
                    "vet_health_api_observation": load_json(cli_options.params_file),
                    "icn": cli_options.icn
                }
            }

        else:
            __VRO_CONFIG__ = "TO BE IMPLEMENTED"

    return __VRO_CONFIG__


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


def build_token_params(data: dict, icn: str) -> dict:
    # Build the JWT and the params for posting to the token provider endpoint.
    payload = build_jwt_payload(data["jwt_aud_url"], data["client_id"])
    assertion = build_jwt(payload, data["secret"])

    return {
        "grant_type": data["grant_type"],
        "client_assertion_type": data["client_assertion_type"],
        "scope": data["scope"],
        "client_assertion": assertion,
        "launch": icn
    }


def build_jwt_payload(audience: str, client_id: str) -> dict:
    timestamp = int(datetime.datetime.now().timestamp())

    return {
        "aud": audience,
        "iss": client_id,
        "sub": client_id,
        "jti": str(uuid1()),
        "iat": timestamp,
        "exp": timestamp + 3600,
    }


def build_jwt(payload: dict, secret: str) -> str:
    return jwt.encode(payload, secret, algorithm="RS256")


def build_api_params(params: dict, icn: str) -> dict:
    return {
        "category": params["fhir_category"],
        "code": params["fhir_code"],
        "patient": icn
    }


def authenticate_to_lighthouse(lh_auth_config: dict, icn: str) -> str:
    token_params = build_token_params(lh_auth_config, icn)

    access_token = http_post_for_access_token(lh_auth_config["token_url"], token_params)

    return access_token


def http_post_for_access_token(url: str, params: dict) -> str:
    assertion_response = requests.post(url, params)
    assert assertion_response.status_code == 200

    return assertion_response.json()["access_token"]


def fetch_observation_data (lh_observation_config: dict, icn: str, access_token: str) -> str:
    fhir_observation_params = build_api_params(lh_observation_config, icn)

    observation_response = http_get_api_request(lh_observation_config["fhir_observation_endpoint"], fhir_observation_params, access_token)

    return observation_response


def http_get_api_request(url: str, params: dict, token: str) -> Json:
    headers = {"Authorization": f"Bearer {token}"}

    api_response = requests.get(url, params=params, headers=headers)
    assert api_response.status_code == 200

    return api_response.json()


def handle_api_response(api_response: Json) -> None:
    print(api_response)


def load_secret(key: Union[Path, str]) -> str:
    # Load secret from file or env var.
    if Path(key).exists():
        return load_text(key)

    if secret := os.environ.get(str(key)):
        return secret

    raise SystemError(f"{key} not found as file or environment variable")


def load_text(path: Union[Path, str]) -> str:
    return Path(path).read_text()


def load_json(path: Union[Path, str]) -> dict:
    raw = load_text(path)
    return json.loads(raw)


if __name__ == "__main__":
    cli_main()