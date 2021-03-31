import json


def lambda_handler(event, context):
    print(f"Incoming event: {event}")
    claim_type = event.get("claim_type")
    claim_subtype = event.get("claim_subtype")
    pvid = event.get("pvid")
    claim_status = {
        "pvid": str(pvid),
        "claim_type": claim_type,
        "claim_subtype": claim_subtype,
        "applicable": claim_type == "disability" and claim_subtype == "increase"
    }
    return {
        'statusCode': 200,
        'body': {"claim_status": claim_status}
    }


def main():
    input_event = {
        "claim_type": "disability",
        "claim_subtype": "increase",
        "pvid": "123"
    }
    print(json.dumps(lambda_handler(input_event, None)))


if __name__ == "__main__":
    main()
