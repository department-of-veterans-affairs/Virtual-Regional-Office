import json


def lambda_handler(event, context):
    print(f"Incoming event: {event}")
    claim_status = event["body"]["claim_status"]
    pvid_to_icn = {
        "123": "1001096151",
        "666": "1234567890"
    }
    pvid = claim_status.get('pvid')
    icn = pvid_to_icn.get(pvid)
    claim_status.update({"icn": icn})
    return {
        'statusCode': 200,
        'body': {"claim_status": claim_status}
    }


def main():
    input_event = {
        "statusCode": "200",
        "body":
        {
            "claim_status":
                {
                    "pvid": "123",
                    "claim_type": "disability",
                    "claim_subtype": "increase",
                    "applicable": True
                }
        }
    }
    print(json.dumps(lambda_handler(input_event, None)))


if __name__ == "__main__":
    main()
