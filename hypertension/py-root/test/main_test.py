from lib.main import main

from test.doubles.aws_secrets_manager import get_lighthouse_rsa_key_double


def test_main():
    assert main() == {
        "statusCode": 200,
        "body": get_lighthouse_rsa_key_double(
            "Fake. Doesnt Matter. Just need something here."
        ),
    }
