from lib.lighthouse import (
    authenticate_to_lighthouse,
    fetch_observation_data
)


def main(config):
    icn = config["lighthouse"]["icn"]

    access_token = authenticate_to_lighthouse(config["lighthouse"]["auth"], icn)

    observation_response = fetch_observation_data(config["lighthouse"]["vet_health_api_observation"], icn, access_token)

    return {
        "statusCode": 200,
        "body": observation_response
    }
