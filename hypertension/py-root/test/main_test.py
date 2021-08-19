from lib.main import main

import lib.lighthouse as lighthouse

from test.doubles.lighthouse import (
    http_post_for_access_token_double,
    http_get_api_request_double
)

from test.data.lighthouse import (
    lh_observation_response
)


def test_main(config, monkeypatch_session):
    monkeypatch_session.setattr(lighthouse, 'http_post_for_access_token', http_post_for_access_token_double)
    monkeypatch_session.setattr(lighthouse, 'http_get_api_request', http_get_api_request_double)

    expected = {
        "statusCode": 200,
        "body": lh_observation_response
    }

    assert main(config) == expected
