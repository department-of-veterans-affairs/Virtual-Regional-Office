import os
from test.doubles.aws_secrets_manager import get_lighthouse_rsa_key_double
from dotenv import load_dotenv
import lib.aws_secrets_manager as aws_secrets_manager


load_dotenv("../cf-template-params.env")

os.environ[
    "LighthousePrivateRsaKeySecretArn"
] = "Fake. Not used. Doesnt Matter. Just need something. Anything."

# Mock AWS::SecretsManager::Secret fetch
aws_secrets_manager.get_lighthouse_rsa_key = get_lighthouse_rsa_key_double
