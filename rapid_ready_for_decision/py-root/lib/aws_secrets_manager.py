import base64
import boto3
import ast


# AWS CLI can't (easily) take params with newlines or spaces. Thus, we base64
# encode our RSA PEM to make it single line before we upload it to
# Secrets Manager. See docs/design-notes.md
def get_lighthouse_rsa_key(aws_secret_arn):  # pragma: no cover
    sm_client = boto3.client("secretsmanager", region_name="us-east-1")
    base64_encoded_pem = sm_client.get_secret_value(SecretId=aws_secret_arn)[
        "SecretString"
    ]
    base64_encoded_pem = ast.literal_eval(base64_encoded_pem)
    print(type(base64_encoded_pem))
    result_bytes = base64.b64decode(base64_encoded_pem["VroLhPrivateRsaKey"])

    return result_bytes.decode(), base64_encoded_pem["VroLighthouseOAuthClientId"]


def get_secret_from_secrets_manager_by_name(
    aws_secret_arn: str,
):  # pragma: no cover
    sm_client = boto3.client("secretsmanager")
    secret_info = sm_client.get_secret_value(SecretId=aws_secret_arn)
    secret = secret_info["SecretString"]
    return secret
