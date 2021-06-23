import os
from typing import Dict
from lib.aws_secrets_manager import get_lighthouse_rsa_key
from lib.pdf_generator import PdfGenerator

WKHTMLTOPDF_PATH = os.environ["WKHTMLTOPDF_PATH"]


def main(event: Dict):
    # TODO: WARNING!! Dont use your (or any) real private RSA key here until
    # you fix this to make it stop returning it in the response body!!
    secret = os.environ["LighthousePrivateRsaKeySecretArn"]
    lighthouse_rsa_key = get_lighthouse_rsa_key(secret)

    pdf = get_pdf(event)

    # TODO: WARNING!! Don't print sensitive data -
    # remove this when we use real data
    print(pdf)

    return {"statusCode": 200, "body": lighthouse_rsa_key}


def get_pdf(event: Dict) -> bytes:
    pdf_generator = PdfGenerator(WKHTMLTOPDF_PATH)
    return pdf_generator.generate_from_string(event.get("html"))
