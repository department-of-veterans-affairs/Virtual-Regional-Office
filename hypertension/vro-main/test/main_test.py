from lib.main import main
from test.doubles.aws_secrets_manager import mock_get_lighthouse_rsa_key


test_event = {"html": "<html><body>Hello World!</body></html>"}


def test_main():
    assert main(test_event) == {
        "statusCode": 200,
        "body": mock_get_lighthouse_rsa_key(
            "Fake. Doesnt Matter. Just need something here."
        ),
    }
