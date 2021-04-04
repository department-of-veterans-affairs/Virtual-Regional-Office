def lambda_handler(event, context):
    print(f"Incoming event: {event}")

    return {
        'statusCode': 200,
        'body': event
    }
