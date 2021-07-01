import os


def get_lighthouse_rsa_key_double(awsSecretArn):
    return os.environ["LighthousePrivateRsaKey"]
