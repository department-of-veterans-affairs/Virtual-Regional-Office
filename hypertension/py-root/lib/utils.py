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
