import datetime
import jwt
import requests

from uuid import uuid1

from typing import Union

Json = Union[dict, list]

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
        "code": params["fhir_loinc_code"],
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
