import os

from lib.aws_secrets_manager import get_lighthouse_rsa_key

def main():
  return {
    "statusCode": 200,
    # TODO: WARNING!! Dont use your (or any) real private RSA key here until you fix this to make it stop returning it in the response body!!
    "body": get_lighthouse_rsa_key(os.environ['LighthousePrivateRsaKeySecretArn'])
  }
