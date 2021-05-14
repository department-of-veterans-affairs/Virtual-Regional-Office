import argparse
import datetime
import json
import os
import pdb
from pathlib import Path
from typing import Union
from uuid import uuid1

import jwt
import requests


"""
Usage example:
    python get_token_make_api_request.py 000aaa ./private.pem \
        assertion-params.json observation-request-params.json 123456789

This script expects the following arguments, in order:

    client_id: the client_id associated with your authorization.
    key_loc: the location of a private .pem file or the name of an environment
        variable containing the key.
    assertions_file: the location of a JSON file containing a dictionary with
        the following fields:

            audience: the aud value (a URL) for the JWT.
            token_url: the URL of the endpoint for requesting a token from.
            grant_type: the kind of credentials you want.
            client_assertion_type: e.g.
                "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"
            scope: the various permisions you're requesting.

    params_file: the location of a JSON file containing the params of your
        request to the API. Must include the url of the API endpoint to query
        in the api_url field.  Other fields will be passed as parameters to
        that endpoint with a GET request.

    icn: the ICN of the individual to query for.

The JSON files in this directory are samples and should be altered as
necessary.
"""


def cli_main() -> None:
    opts = get_cli_args()
    auth_params = load_json(opts.assertions_file)
    base_params = load_json(opts.params_file)
    secret = load_secret(opts.key_loc)

    token_url, api_url = auth_params["token_url"], base_params["api_url"]
    client_id, icn = opts.client_id, opts.icn

    token_params = build_token_params(auth_params, client_id, icn, secret)
    api_params = build_api_params(base_params, icn)

    access_token = http_post_for_access_token(token_url, token_params)

    api_response = http_get_api_request(api_url, api_params, access_token)

    handle_api_response(api_response)


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


def get_cli_args() -> argparse.Namespace:
    return setup_cli_parser().parse_args()


def build_jwt(payload: dict, secret: str) -> str:
    return jwt.encode(payload, secret, algorithm="RS256")


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


def build_form_params(params: dict, assertion: str, icn: str) -> dict:
    # Add: client_assertion and launch. Remove: token_url and audience.
    full_params = params | {"client_assertion": assertion, "launch": icn}
    return omit(["token_url", "audience"], full_params)


def build_token_params(
    params: dict, client_id: str, icn: str, secret: str
) -> dict:
    # Build the JWT and the params for posting to the token provider endpoint.
    payload = build_jwt_payload(params["audience"], client_id)
    assertion = build_jwt(payload, secret)
    return build_form_params(params, assertion, icn)


def http_post_for_access_token(url: str, params: dict) -> str:
    assertion_response = requests.post(url, params)
    assert assertion_response.status_code == 200

    return assertion_response.json()["access_token"]


def build_api_params(params: dict, icn: str) -> dict:
    # Add: patient. Remove: api_url.
    full_params = params | {"patient": icn}
    return omit(["api_url"], full_params)


def http_get_api_request(url: str, params: dict, token: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}

    api_response = requests.get(url, params=params, headers=headers)
    if api_response.status_code != 200:
        pdb.set_trace()

    return api_response.json()


def load_secret(key: Union[Path, str]) -> str:
    # Load secret from file or env var.
    if Path(key).exists():
        return load_text(key)

    if secret := os.environ.get(key):
        return secret

    raise SystemError(f"{key} not found as file or environment variable")


def handle_api_response(api_response: Union[dict, list]) -> None:
    print(api_response)


def omit(keys_to_remove: list, d: dict) -> dict:
    return {k: d[k] for k in d if k not in keys_to_remove}


def load_text(path: Union[Path, str]) -> str:
    return Path(path).read_text()


def load_json(path: Union[Path, str]) -> dict:
    raw = load_text(path)
    return json.loads(raw)


if __name__ == "__main__":
    cli_main()
