import json
import os

import boto3

from src.get_requests import get_canned_json

smClient = boto3.client('secretsmanager')

def lambda_handler(event, context):

    some_canned_dict = json.loads(get_canned_json())

    some_canned_dict['rsaKey'] = get_lh_rsa_key(os.environ['LH_PRIVATE_RSA_KEY_SECRET_ARN'])

    return {
        "statusCode": 200,
        "body": json.dumps(some_canned_dict)
    }

def get_lh_rsa_key(awsSecretArn):
    result = smClient.get_secret_value(SecretId=awsSecretArn)

    # TODO: Fix this. WARNING this is not safe. Don't use this code with a real secret. It's just like this for testing purposes.
    print('## Result from secret fetch')
    print(result)
    print(result['SecretString'])

    return result['SecretString']
