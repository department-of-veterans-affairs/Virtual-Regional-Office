from scripts.python_get_token_make_api_request_script.get_token_make_api_request import (
    cli_main,
)


def test_get_token_make_api_request():
    result = cli_main()
    print("result is -------------------------------------------------")
    print(result)
    assert 1 == 1
