from lib.main import main

def test_main():
    test_event = {"irrelevant": "value"}
    assert main(test_event) == {"statusCode": 200, "body": "test body"}
