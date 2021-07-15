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


# TODO: Scope this to the session.
# You'll have to deal with the problem of trying to use monkey patch in a thing that's not function scoped
# https://github.com/pytest-dev/pytest/issues/1872
@pytest.fixture()
def lh_access_token(monkeypatch):
    monkeypatch.setattr(get_token_make_api_request, 'get_cli_args', get_cli_args_double)

    config = load_config(True)

    icn = config["lighthouse"]["icn"]

    access_token = authenticate_to_lighthouse(config["lighthouse"]["auth"], icn)

    return access_token
