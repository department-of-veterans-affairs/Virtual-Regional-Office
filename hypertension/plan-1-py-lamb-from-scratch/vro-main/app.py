import json

import requests

def lambda_handler(event, context):

    res = requests.get('https://httpbin.org/get')

    print('res.text is')
    print(res.text)

    return {
        "statusCode": 200,
        "body": res.text
    }
