import boto3

def get_lighthouse_rsa_key(awsSecretArn):
    smClient = boto3.client('secretsmanager')
    result = smClient.get_secret_value(SecretId=awsSecretArn)
    return result['SecretString']
