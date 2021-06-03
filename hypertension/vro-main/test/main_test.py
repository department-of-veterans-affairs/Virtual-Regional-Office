from lib.main import main

def test_main():
  assert main() == {
    "statusCode": 200,
    "body": "Hello world!"
  }
