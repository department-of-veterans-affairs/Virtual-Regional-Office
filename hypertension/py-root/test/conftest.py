import sys
import os
from test.doubles.aws_secrets_manager import get_lighthouse_rsa_key_double
from dotenv import load_dotenv
import lib.aws_secrets_manager as aws_secrets_manager
from test.doubles.filesystem_operations import (
    load_text_double,
    load_secret_double,
)
import scripts.python_get_token_make_api_request_script.get_token_make_api_request as get_token_make_api_request

load_dotenv("../cf-template-params.env")

os.environ[
    "LighthousePrivateRsaKeySecretArn"
] = "Fake. Not used. Doesnt Matter. Just need something. Anything."

# Mock AWS::SecretsManager::Secret fetch
aws_secrets_manager.get_lighthouse_rsa_key = get_lighthouse_rsa_key_double

# Mock read files from filesystem
get_token_make_api_request.load_text = load_text_double
get_token_make_api_request.load_secret = load_secret_double

sys.argv = [
    "scripts/python_get_token_make_api_request_script/get_token_make_api_request.py",
    "FakeLighthouseClientCredentialsOAuthClientId",
    "FakePathToLighthouseRsaPrivateKeyPemFile",
    "FakePathToLighthouseAuthAssertionsFile",
    "FakePathToLighthouseHealthApiObservationRequestParamsFile",
    "FakeVeteranIcn",
]
