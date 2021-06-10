# Load Env
from dotenv import load_dotenv
load_dotenv('../cf-template-params.env')

# Fake Env
import os
os.environ['LighthousePrivateRsaKeySecretArn'] = 'Fake. Not used. Doesnt Matter. Just need something. Anything.'

# Mock AWS::SecretsManager::Secret fetch
import lib.aws_secrets_manager as aws_secrets_manager
from test.doubles.aws_secrets_manager import mock_get_lighthouse_rsa_key
aws_secrets_manager.get_lighthouse_rsa_key = mock_get_lighthouse_rsa_key
