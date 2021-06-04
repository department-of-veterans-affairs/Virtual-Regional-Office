import re

# AWS SAM CLI can't take multi-line parameters or spaces. Thus, our private RSA key for Lighthouse
# must be ingested as a single line with no spaces, and converted back to normal, multi-line PEM
# format via fix_pem_formatting().
# We chose & to substitute for newline characters and _ to substitute for space characters because
# - These are not possible PEM body characters (because they're not valid base64 characters)
# - Regex doesn't treat them as special characters
# - SAM CLI doesn't choke on them
def fix_pem_formatting(custom_format_rsa_key):
  return re.sub('_',' ' , re.sub('&', '\n', custom_format_rsa_key))
