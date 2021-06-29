import os


def mock_get_lighthouse_rsa_key(awsSecretArn):
    return os.environ["LighthousePrivateRsaKey"]
