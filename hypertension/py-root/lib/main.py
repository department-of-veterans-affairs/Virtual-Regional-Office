def main(config):
    # TODO: WARNING!! Dont use your (or any) real private RSA key in your env vars until
    # you fix this to make it stop returning it in the response body!!
    return {"statusCode": 200, "body": config}
