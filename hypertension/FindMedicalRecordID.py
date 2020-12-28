import json

def lambda_handler(event, context):
    print(f"Incoming event: {event}")
    claim_status = event["body"]["claim_status"]
    pvid_to_icn = {
        123 : 1001096151,
        666 : 1234567890
    }
    pvid = claim_status.get('pvid')
    icn = pvid_to_icn.get(pvid)
    claim_status.update({"icn" : icn})
    return {
        'statusCode': 200,
        'body': {"claim_status": claim_status}
    }