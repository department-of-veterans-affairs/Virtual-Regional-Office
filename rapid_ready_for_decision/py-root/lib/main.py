from typing import Dict
from lib.lighthouse import authenticate_to_lighthouse, fetch_observation_data
from lib.pdf_generator import generate_pdf_from_string


def main(config: Dict, event):
    icn = config["lighthouse"]["icn"]

    access_token = authenticate_to_lighthouse(
        config["lighthouse"]["auth"], icn
    )

    observation_response = fetch_observation_data(
        config["lighthouse"]["vet_health_api_observation"], icn, access_token
    )

    assert "html" in event

    pdf = generate_pdf_from_string(event.get("html"))

    # TODO: WARNING!! Don't print sensitive data -
    # remove this when we use real data
    print(pdf)

    return {"statusCode": 200, "body": observation_response}
