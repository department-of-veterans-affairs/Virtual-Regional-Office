import argparse
import os

from scripts.python_get_token_make_api_request_script.get_token_make_api_request import (
    setup_cli_parser,
)

def get_cli_args_double() -> argparse.Namespace:
    return setup_cli_parser().parse_args([
        # "scripts/python_get_token_make_api_request_script/get_token_make_api_request.py",
        os.environ["LighthouseClientId"],
        os.environ["LighthousePrivateRsaKeyFilePath"],
        "./scripts/python_get_token_make_api_request_script/assertion-params-example.json",
        "./scripts/python_get_token_make_api_request_script/observation-request-params-example.json",
        os.environ["TestVeteranIcn"],
    ])
