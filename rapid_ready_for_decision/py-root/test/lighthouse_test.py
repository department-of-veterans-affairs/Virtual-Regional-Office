from test.doubles.lighthouse import http_get_api_request_double

from test.data.lighthouse import (
    lh_auth_api_response,
    lh_observation_success_response,
    lh_observation_failure_response,
)

import jwt

from lib import lighthouse

from lib.lighthouse import fetch_observation_data, build_token_params


def test_authenticate_to_lighthouse(lh_access_token):
    assert lh_auth_api_response["access_token"] == lh_access_token


def test_fetch_observation_data_success(
    monkeypatch_session, config, lh_access_token
):
    monkeypatch_session.setattr(
        lighthouse, "http_get_api_request", http_get_api_request_double
    )

    observation_response = fetch_observation_data(
        config["lighthouse"]["vet_health_api_observation"],
        config["lighthouse"]["icn"],
        lh_access_token,
    )

    assert lh_observation_success_response == observation_response


def test_fetch_observation_data_failure(monkeypatch_session, config):
    monkeypatch_session.setattr(
        lighthouse, "http_get_api_request", http_get_api_request_double
    )

    observation_response = fetch_observation_data(
        config["lighthouse"]["vet_health_api_observation"],
        config["lighthouse"]["icn"],
        "This is an invalid access token",
    )

    assert lh_observation_failure_response == observation_response


def test_build_token_params(config, public_rsa_key):
    lh_auth_config = config["lighthouse"]["auth"]
    audience = lh_auth_config["jwt_aud_url"]
    client_id = lh_auth_config["client_id"]
    secret = lh_auth_config["secret"]
    icn = config["lighthouse"]["icn"]

    actual = build_token_params(lh_auth_config, icn)

    just_for_a_timestamp_and_uuid = jwt.decode(
        actual["client_assertion"],
        public_rsa_key,
        audience=audience,
        algorithms="RS256",
    )

    expected_payload = {
        "aud": audience,
        "iss": client_id,
        "sub": client_id,
        "jti": just_for_a_timestamp_and_uuid["jti"],
        "iat": just_for_a_timestamp_and_uuid["iat"],
        "exp": just_for_a_timestamp_and_uuid["iat"] + 3600,
    }

    expected_assertion = jwt.encode(
        expected_payload, secret, algorithm="RS256"
    )

    expected_token_params = {
        "grant_type": lh_auth_config["grant_type"],
        "client_assertion_type": lh_auth_config["client_assertion_type"],
        "scope": lh_auth_config["scope"],
        "client_assertion": expected_assertion,
        "launch": icn,
    }

    assert expected_token_params == actual
