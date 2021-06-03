import json
import os

from src.get_requests import get_canned_json
from src.aws_secrets_manager import get_lh_rsa_key

def main():

    some_canned_dict = json.loads(get_canned_json())

    some_canned_dict['rsaKey'] = get_lh_rsa_key(os.environ['LighthousePrivateRsaKeySecretArn'])

    return json.dumps(some_canned_dict)
