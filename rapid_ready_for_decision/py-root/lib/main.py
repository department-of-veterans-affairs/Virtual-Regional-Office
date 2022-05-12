from typing import Dict
from lib.lighthouse import authenticate_to_lighthouse, fetch_observation_data
from lib.pdf_generator import generate_template_file, generate_pdf_from_string


def main(config: Dict, event):
    icn = config["lighthouse"]["icn"]

    access_token = authenticate_to_lighthouse(
        config["lighthouse"]["auth"], icn
    )

    observation_response = fetch_observation_data(
        config["lighthouse"]["vet_health_api_observation"], icn, access_token
    )

    assert "html" in event

    pdf_data = {"test": "test"}

    template = generate_template_file("hypertension", pdf_data)

    # pdf = generate_pdf_from_string(event.get("html"))
    pdf = generate_pdf_from_string(template)

    # TODO: WARNING!! Don't print sensitive data -
    # remove this when we use real data
    print(pdf)

    return {"statusCode": 200, "body": observation_response}
