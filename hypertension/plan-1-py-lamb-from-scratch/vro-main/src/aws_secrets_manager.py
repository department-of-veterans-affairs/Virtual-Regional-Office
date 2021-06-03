import boto3

def get_lh_rsa_key(awsSecretArn):
    smClient = boto3.client('secretsmanager')
    result = smClient.get_secret_value(SecretId=awsSecretArn)

    # TODO: Fix this. WARNING this is not safe. Don't use this code with a real secret. It's just like this for testing purposes.
    # print('## Result from secret fetch')
    # print(result)
    # print(result['SecretString'])

    return result['SecretString']
