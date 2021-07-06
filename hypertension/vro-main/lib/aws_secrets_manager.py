import os
import boto3
from lib.utils import fix_pem_formatting


def get_lighthouse_rsa_key(awsSecretArn):  # pragma: no cover
    if os.environ["STAGE"] == "dev":
        return "development-environment"

    # Since these are just boto3 calls, no need for us to test them, and
    # fix_pem_formatting is tested elsewhere.
    smClient = boto3.client("secretsmanager")
    result = smClient.get_secret_value(SecretId=awsSecretArn)

    return fix_pem_formatting(result["SecretString"])
