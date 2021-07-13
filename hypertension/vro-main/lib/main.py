import os
from typing import Dict
from lib.aws_secrets_manager import get_lighthouse_rsa_key
from lib.pdf_generator import generate_pdf_from_string


def main(event: Dict):
    # TODO: WARNING!! Dont use your (or any) real private RSA key here until
    # you fix this to make it stop returning it in the response body!!
    secret = os.environ["LighthousePrivateRsaKeySecretArn"]
    lighthouse_rsa_key = get_lighthouse_rsa_key(secret)

    assert "html" in event
    pdf = generate_pdf_from_string(event.get("html"))

    # TODO: WARNING!! Don't print sensitive data -
    # remove this when we use real data
    print(pdf)

    return {"statusCode": 200, "body": lighthouse_rsa_key}
