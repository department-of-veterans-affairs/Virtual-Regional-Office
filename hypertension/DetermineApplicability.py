import json

def lambda_handler(event, context):
    print(f"Incoming event: {event}")
    claim_type = event.get("claim_type")
    claim_subtype = event.get("claim_subtype")
    claim_status = {
        "claim_type" : claim_type,
        "claim_subtype" : claim_subtype,
        "applicable" : claim_type == "disability" and claim_subtype == "increase"
    }
    return {
        'statusCode': 200,
        'body': {"claim_status": claim_status}
    }
