import os

def mock_get_lh_rsa_key(awsSecretArn):
  return os.environ['LighthousePrivateRsaKey']
