import pytest
import sys
import os
from test.doubles.aws_secrets_manager import get_lighthouse_rsa_key_double
from dotenv import load_dotenv
import lib.aws_secrets_manager as aws_secrets_manager
import scripts.python_get_token_make_api_request_script.get_token_make_api_request as get_token_make_api_request
from scripts.python_get_token_make_api_request_script.get_token_make_api_request import (
    load_config,
    authenticate_to_lighthouse
)
from test.doubles.get_token_make_api_request import get_cli_args_double

load_dotenv("../cf-template-params.env")

os.environ[
    "LighthousePrivateRsaKeySecretArn"
] = "Fake. Not used. Doesnt Matter. Just need something. Anything."

# Mock AWS::SecretsManager::Secret fetch
aws_secrets_manager.get_lighthouse_rsa_key = get_lighthouse_rsa_key_double

# monkeypatch is a function-scoped fuxture. Because of this, you can't use it inside a
# session-scoped fixtures. To get around this, we create a new instance of the monkeypatch fixture
# that is session-scoped, for use in our other fixtures that need to be session scoped.
# This is subject to breaking if pytest changes, because it uses the internal _pytest API.
# See https://github.com/pytest-dev/pytest/issues/1872
@pytest.fixture(scope='session')
def monkeypatch_session():
    from _pytest.monkeypatch import MonkeyPatch
    m = MonkeyPatch()
    yield m
    m.undo()


@pytest.fixture(scope="session")
def lh_access_token(config):
    icn = config["lighthouse"]["icn"]
    access_token = authenticate_to_lighthouse(config["lighthouse"]["auth"], icn)
    return access_token


@pytest.fixture(scope="session")
def config(monkeypatch_session):
    monkeypatch_session.setattr(get_token_make_api_request, 'get_cli_args', get_cli_args_double)
    config = load_config(True)
    return config
