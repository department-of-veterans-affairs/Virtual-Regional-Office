import boto3

from lib.utils import fix_pem_formatting

def get_lighthouse_rsa_key(awsSecretArn):
    smClient = boto3.client('secretsmanager')
    result = smClient.get_secret_value(SecretId=awsSecretArn)

    return fix_pem_formatting(result['SecretString'])
