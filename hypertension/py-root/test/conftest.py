import sys
import os
from test.doubles.aws_secrets_manager import get_lighthouse_rsa_key_double
from dotenv import load_dotenv
import lib.aws_secrets_manager as aws_secrets_manager
import scripts.python_get_token_make_api_request_script.get_token_make_api_request as get_token_make_api_request

load_dotenv("../cf-template-params.env")

os.environ[
    "LighthousePrivateRsaKeySecretArn"
] = "Fake. Not used. Doesnt Matter. Just need something. Anything."

# Mock AWS::SecretsManager::Secret fetch
aws_secrets_manager.get_lighthouse_rsa_key = get_lighthouse_rsa_key_double

sys.argv = [
    "scripts/python_get_token_make_api_request_script/get_token_make_api_request.py",
    os.environ["LighthouseClientId"],
    os.environ["LighthousePrivateRsaKeyFilePath"],
    "./scripts/python_get_token_make_api_request_script/assertion-params-example.json",
    "./scripts/python_get_token_make_api_request_script/observation-request-params-example.json",
    os.environ["TestVeteranIcn"],
]
