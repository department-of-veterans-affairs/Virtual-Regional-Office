import subprocess
from pathlib import Path

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

# Set the wkhtmltopdf path environment variable by finding the local binary

which_wkhtmltopdf = subprocess.run(
    "which wkhtmltopdf", shell=True, capture_output=True
)

wkhtmltopdf_path = Path(which_wkhtmltopdf.stdout.decode().strip()).resolve()
assert wkhtmltopdf_path.exists()
os.environ["WKHTMLTOPDF_PATH"] = str(wkhtmltopdf_path)

# Mock AWS::SecretsManager::Secret fetch

aws_secrets_manager.get_lighthouse_rsa_key = mock_get_lighthouse_rsa_key
