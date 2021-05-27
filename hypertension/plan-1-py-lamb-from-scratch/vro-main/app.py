import json

from lib.get_requests import get_canned_json

def lambda_handler(event, context):

    return {
        "statusCode": 200,
        "body": get_canned_json()
    }
