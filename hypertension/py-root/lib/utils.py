from scripts.python_get_token_make_api_request_script.get_token_make_api_request import (
    get_cli_args,
)

# AWS SAM CLI can't (easily) take parameters that are multi-line or have
# spaces. Thus, any private RSA key we need must be ingested as a single line
# with no spaces, and converted back to normal, multi-line PEM format via
# fix_pem_formatting().
# For our custom "PEM" file format, we chose to use ampersand to substitute for
# newline characters and underscore to substitute for space characters because:
#     - These are not possible PEM body characters
#       (because they're not valid base64 characters)
#     - Regex doesn't treat them as special characters
#     - SAM CLI doesn't choke on them


def fix_pem_formatting(custom_format_rsa_key):
    return custom_format_rsa_key.replace("_", " ").replace("&", "\n")


def load_config(running_as_script) -> dict:
    if running_as_script:
        config = "TO BE IMPLEMENTED"
        opts = get_cli_args(
            [
                "myClientId",
                "myKeyLoc",
                "myAssertionsFile",
                "myParamsFile",
                "myIcn",
            ]
        )
        # config["auth_data"] = load_json(opts.assertions_file)
        # config["api_data"] = load_json(opts.params_file)
        # config["auth_data"]["secret"] = load_secret(opts.key_loc)
    else:
        config = "TO BE IMPLEMENTED"
    #     config = {
    #         "auth_data": {
    #             "urls": {
    #                 "audience": os.environ["LighthouseJwtAudUrl"],
    #                 "token": os.environ["LighthouseTokenUrl"]
    #             },
    #             "parameters": {
    #                 "grant_type": os.environ["LighthouseOauthGrantType"],
    #                 "client_assertion_type": os.environ["LighthouseOauthClientAssertionType"],
    #                 "scope": "launch/patient patient/Patient.read patient/Observation.read patient/Medication.read"
    #             }
    #         }
    #     }
    # }
    return config
