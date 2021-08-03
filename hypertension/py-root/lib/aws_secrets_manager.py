import base64
import boto3

# AWS CLI can't (easily) take params with newlines or spaces. Thus, we base64 encode our RSA PEM
# to make it single line before we upload it to Secrets Manager. See docs/design-notes.md
def get_lighthouse_rsa_key(awsSecretArn):  # pragma: no cover
    smClient = boto3.client("secretsmanager")
    base64EncodedPem = smClient.get_secret_value(SecretId=awsSecretArn)["SecretString"]

    resultBytes = base64.b64decode(base64EncodedPem)

    return resultBytes.decode()
