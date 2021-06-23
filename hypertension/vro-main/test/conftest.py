import subprocess

# Load Env
from dotenv import load_dotenv

import lib.aws_secrets_manager as aws_secrets_manager  # noqa

load_dotenv("../cf-template-params.env")

from test.doubles.aws_secrets_manager import (  # noqa
    mock_get_lighthouse_rsa_key,
)

# Fake Env
import os  # noqa

os.environ[
    "LighthousePrivateRsaKeySecretArn"
] = "Fake. Not used. Doesnt Matter. Just need something. Anything."
wkhtmltopdf_path = subprocess.run(
    "which wkhtmltopdf", shell=True, capture_output=True
)
os.environ["WKHTMLTOPDF_PATH"] = wkhtmltopdf_path.stdout.decode(
    "utf-8"
).rstrip("\n")

# Mock AWS::SecretsManager::Secret fetch

aws_secrets_manager.get_lighthouse_rsa_key = mock_get_lighthouse_rsa_key
