import lib.lighthouse as lighthouse

from lib.lighthouse import fetch_observation_data
from test.doubles.lighthouse import http_get_api_request_double

from test.data.lighthouse import (
    lh_observation_response
)

# TODO: Mock the API call
# TODO: Test something better than the length of the access token
def test_authenticate_to_lighthouse(lh_access_token):
    length_of_a_lh_access_token = 929
    assert len(lh_access_token) == length_of_a_lh_access_token

def test_fetch_observation_data(monkeypatch_session, config, lh_access_token):
    monkeypatch_session.setattr(lighthouse, 'http_get_api_request', http_get_api_request_double)

    observation_response = fetch_observation_data(
        config["lighthouse"]["vet_health_api_observation"], config["lighthouse"]["icn"], lh_access_token
    )

    assert lh_observation_response == observation_response
