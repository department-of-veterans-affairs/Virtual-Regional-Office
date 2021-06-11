import os
from lib.aws_secrets_manager import get_lighthouse_rsa_key


def main():
    # TODO: WARNING!! Dont use your (or any) real private RSA key here until
    # you fix this to make it stop returning it in the response body!!
    secret = os.environ["LighthousePrivateRsaKeySecretArn"]
    lighthouse_rsa_key = get_lighthouse_rsa_key(secret)
    return {"statusCode": 200, "body": lighthouse_rsa_key}
