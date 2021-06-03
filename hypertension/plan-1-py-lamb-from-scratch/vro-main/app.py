from src.main import main

def lambda_handler(event, context):

    result = main()

    return {
        "statusCode": 200,
        "body": result
    }
