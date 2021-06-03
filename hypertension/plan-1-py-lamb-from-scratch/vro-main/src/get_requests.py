import requests

from src.aws_secrets_manager import get_lh_rsa_key

def get_canned_json():
  return requests.get('http://echo.jsontest.com/key/value/one/two').text

def get_lh_token(awsSecretArn):
  rsa_key = get_lh_rsa_key(awsSecretArn)

  return 'THE REAL get_lh_token (...after I finish implementing this function). And, I throw in the secretArn here just for fun for now: {}'.format(awsSecretArn)
