import os
from getpass import getpass
import boto3

pick = lambda keep, d: {k: d[k] for k in keep if k in d}


def establish_aws_mfa_session_main() -> None:
    # This main function serves the purpose of providing AWS session
    # credentials to a wrapper shell script which will be able to
    # export the credentials to the parent shell. We need it to
    # pass the credentials to the wrapper shell script because
    # python won't export env variables to parent processes
    serial_number, token_code = load_credentials_from_user()
    credentials = load_credentials_from_sts(serial_number, token_code)

    aws_map = {
        "AccessKeyId": "AWS_ACCESS_KEY_ID",
        "SessionToken": "AWS_SESSION_TOKEN",
        "SecretAccessKey": "AWS_SECRET_ACCESS_KEY",
    }

    output_lines = [
        make_output_line(aws_map, credentials, key) for key in aws_map
    ]

    print("\n".join(output_lines))


def make_output_line(aws_map: dict, credentials: dict, key: str) -> str:
    var_name, var_value = aws_map[key], credentials[key]
    # Escape symbols commonly used by Bash.
    escape_pairs = (('"', '\\"'), ("$", "\\$"), ("`", "\\`"))
    for pair in escape_pairs:
        var_value = var_value.replace(*pair)

    return f'export {var_name}="{var_value}"'


def load_credentials_from_user():
    # path for when the session has already been set up in parent shell
    # If AWS_ACCESS_KEY_ID starts with ASIA, it's a temporary credential
    # and needs to be unset in order to be able to call
    # aws sts get-session-token; so we unset the aws credentials environment variables
    if os.environ.get("AWS_ACCESS_KEY_ID", "").startswith("ASIA"):
        keys = (
            "AWS_ACCESS_KEY_ID",
            "AWS_SESSION_TOKEN",
            "AWS_SECRET_ACCESS_KEY",
        )
        for key in keys:
            del os.environ[key]

    arn_q = (
        "Establishing temporary AWS session. "
        "Enter your AWS IAM user's virtual device_arn: "
    )
    token_q = "Enter the six-digit token code from your MFA device: "
    serial_number = getpass(arn_q)
    token_code = getpass(token_q)
    return (serial_number, token_code)


def load_credentials_from_sts(serial_number, token_code):
    sts = boto3.client("sts")
    session_token = sts.get_session_token(
        SerialNumber=serial_number, TokenCode=token_code
    )
    relevant_credentials = pick(
        ("AccessKeyId", "SecretAccessKey", "SessionToken"),
        session_token["Credentials"],
    )
    return relevant_credentials


if __name__ == "__main__":
    establish_aws_mfa_session_main()
