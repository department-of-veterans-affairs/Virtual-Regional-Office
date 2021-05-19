import os

import boto3

smClient = boto3.client('secretsmanager')

def lambda_handler(event, context):
    print(f"Incoming event: {event}")

    print('## ENVIRONMENT VARIABLES')
    print(os.environ['LH_CLIENT_ID'])

    rsaKey = get_lh_rsa_key()

    return {
        'statusCode': 200,
        # TODO: Fix this. WARNING this is not safe. Don't use this code with a real secret. It's just like this for testing purposes.
        'body': rsaKey
    }

def get_lh_rsa_key():
    result = smClient.get_secret_value(SecretId=os.environ['LH_PRIVATE_RSA_KEY_SECRET_ARN'])

    # TODO: Fix this. WARNING this is not safe. Don't use this code with a real secret. It's just like this for testing purposes.
    print('## Result from secret fetch')
    print(result)
    print(result['SecretString'])

    return result['SecretString']
