# This script isn't meant to be run ad hoc because it isn't idempotent.  It's
# part of the initial deployment process for the lambda layers + the lambda
# function If you run this multiple times, it will add duplicate layer arns to
# the lambda function's template.yaml file
import argparse
from pathlib import Path
from typing import Optional
import boto3
import ruamel.yaml
from establish_aws_mfa_session import load_credentials_from_sts, load_credentials_from_user

MAIN_LAMBDA_TEMPLATE_LOCATION = "../../template.yaml"
RELEVANT_LAMBDA_LAYERS = [
    "vro--pdf-generator-layer",
    "vro--python-dependencies-layer",
]


def add_deployed_layers_to_template_main(
    args: Optional[list],
    main_lambda_template_location: str,
    relevant_lambda_layers: list,
) -> None:
    options = setup_cli_parser().parse_args(args)
    template_yaml = load_yaml_from_file(main_lambda_template_location)

    current_layers = get_current_layers(template_yaml)
    if current_layers and not options.overwrite:
        write_existing_layers_error(current_layers)
        return

    serial_number, token_code = load_credentials_from_user()
    credentials = load_credentials_from_sts(serial_number, token_code)
    layer_arns = load_layer_arns(credentials, relevant_lambda_layers)

    template_yaml["Resources"]["VroMainFunction"]["Properties"][
        "Layers"
    ] = layer_arns

    write_template_yaml(main_lambda_template_location, template_yaml)


def setup_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--overwrite", action="store_true")
    return parser


def load_yaml_from_file(location):
    template_file = Path(location)
    template_yaml = ruamel.yaml.YAML().load(template_file.read_text())
    return template_yaml


def get_current_layers(template: dict) -> list:
    try:
        current_layers = template["Resources"]["VroMainFunction"][
            "Properties"
        ]["Layers"]
    except KeyError:
        # We expect the key to be absent but have to test for its presence.
        current_layers = []
    return current_layers


def write_existing_layers_error(existing_layers: list) -> None:
    error_lines = [
        "The Layers property is already present in the lambda's SAM template.",
        "No further action is needed. If you've encountered this result",
        "by mistake, delete the Layers property from the template and retry.",
        "Existing layers: ",
        str(existing_layers),
    ]
    error_message = "\n".join(error_lines)

    raise UserWarning(error_message)


def load_layer_arns(credentials, relevant_lambda_layers: list) -> list:
    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=credentials.get("AccessKeyId"),
        aws_secret_access_key=credentials.get("SecretAccessKey"),
        aws_session_token=credentials.get("SessionToken"),
    )
    layers = lambda_client.list_layers().get("Layers")
    return [
        layer["LatestMatchingVersion"]["LayerVersionArn"]
        for layer in layers
        if layer["LayerName"] in relevant_lambda_layers
    ]


def write_template_yaml(template_location: str, template_yaml: dict) -> None:
    template_file = Path(template_location)
    ruamel.yaml.YAML().dump(template_yaml, template_file)


if __name__ == "__main__":
    add_deployed_layers_to_template_main(
        None, MAIN_LAMBDA_TEMPLATE_LOCATION, RELEVANT_LAMBDA_LAYERS
    )
