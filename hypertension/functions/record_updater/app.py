def lambda_handler(event, context):
    print(f"Incoming event: {event}")
    claim_status = event["body"]["claim_status"]
    print(f"Updating VMBS with data {claim_status}")
    return {
        'statusCode': 200,
        'body': {"claim_status": claim_status}
    }