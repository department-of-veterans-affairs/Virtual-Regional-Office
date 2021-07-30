from lib.main import main

def test_main(config):
    assert main(config) == {
        "statusCode": 200,
        "body": config
    }
