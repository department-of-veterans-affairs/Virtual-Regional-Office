import json

from typing import Union
Json = Union[dict, list]

from requests.models import Response

from test.data.lighthouse import (
    lh_auth_api_response,
    lh_observation_response
)


def http_post_for_access_token_double(url: str, params: dict) -> str:
    return lh_auth_api_response["access_token"]


def http_get_api_request_double(url: str, params: dict, headers: dict) -> Json:
    response = Response()

    access_token = lh_auth_api_response['access_token']

    if headers["Authorization"] == f"Bearer {access_token}":
        response.status_code = 200
        response._content = str.encode(json.dumps(lh_observation_response))
    else:
        response.status_code = 401
        str.encode(json.dumps({"response": "body", "failure": "failure"}))

    return response.json()
