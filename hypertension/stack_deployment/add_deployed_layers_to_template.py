import argparse
import os
from pathlib import Path
from typing import Optional
import boto3

ENV_FILE_LOCATION = "../.env"
RELEVANT_LAMBDA_LAYERS = {
    "vro--pdf-generator-layer": "PdfGeneratorLayerArn",
    "vro--python-dependencies-layer": "PythonDependenciesLayerArn",
}


# This is run as part of stack deployments in order to update the SAM lambda
# function's template with the newly-deployed layer ARNs.
# This function assumes that you've already established an
# AWS MFA session (See README for instructions on doing that).
def add_deployed_layers_to_template_main(
    args: Optional[list],
    env_file_location: str,
    relevant_lambda_layers: dict,
) -> None:
    options = setup_cli_parser().parse_args(args)
    env_file = Path(env_file_location).read_text()
    env_info = make_env_dict(env_file)
    current_layers = get_current_layers(env_info)

    if current_layers and not (options.keep_current_layer_arns or options.overwrite):
        write_existing_layers_error(current_layers)
        return

    if current_layers and options.keep_current_layer_arns:
        print("Keeping ARNs as set in current env file.")
        return

    credentials = load_credentials_from_env()
    layer_arns = fetch_layer_arns(credentials, relevant_lambda_layers)

    write_new_layer_arns_to_env(env_file_location, env_info, layer_arns)


def write_new_layer_arns_to_env(env_file_location: str, env_info: dict, layer_arns: dict):
    updated_env_info = {**env_info, **layer_arns}
    env_string = make_env_string(updated_env_info)
    Path(env_file_location).write_text(env_string)


def make_env_dict(env_contents: str) -> dict:
    def remove_quotes(value):
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        return value

    kv_lists = [_.split("=") for _ in env_contents.splitlines()]
    return {k: remove_quotes(v) for k, v in kv_lists}


def make_env_string(env_info: dict) -> str:
    lines = [f'{key}="{value}"' for key, value in env_info.items()]
    return "\n".join(lines)


def load_credentials_from_env() -> dict:
    return {
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY"),
        "aws_session_token": os.environ.get("AWS_SESSION_TOKEN"),
    }


def setup_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--keep_current_layer_arns", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser


def get_current_layers(env: dict) -> dict:
    layer_keys = (
        "PythonDependenciesLayerArn",
        "PdfGeneratorLayerArn",
    )
    arn_start_text = "arn:aws:lambda:"
    check = lambda v: v and v.startswith(arn_start_text)

    candidates = {k: env.get(k) for k in layer_keys if check(env.get(k, ""))}
    return candidates if (len(candidates) == len(layer_keys)) else {}


def write_existing_layers_error(existing_layers: dict) -> None:
    error_lines = [
        "The Layers property is already present in the lambda's SAM template.",
        "No further action is needed. If you've encountered this result",
        "by mistake, either pass in the --keep_current_layer_arns option, or",
        "pass in the --overwrite option",
        "Existing layers: ",
        str(existing_layers),
    ]
    error_message = "\n".join(error_lines)

    raise UserWarning(error_message)


def load_layer_arns(credentials, relevant_lambda_layers: dict) -> dict:
    lambda_client = boto3.client("lambda", **credentials)
    layers = lambda_client.list_layers().get("Layers")

    layer_arns = {}

    for layer in layers:
        if layer["LayerName"] in relevant_lambda_layers:
            key = relevant_lambda_layers[layer["LayerName"]]
            layer_arns[key] = layer["LatestMatchingVersion"]["LayerVersionArn"]

    return layer_arns


if __name__ == "__main__":
    add_deployed_layers_to_template_main(
        None, ENV_FILE_LOCATION, RELEVANT_LAMBDA_LAYERS
    )
