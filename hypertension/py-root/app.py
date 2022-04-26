from lib.main import main  # pragma: no cover (main is tested elsewhere)
from lib.utils import load_config


# pylint: disable=unused-argument
def lambda_handler(event, context):  # pragma: no cover
    config = load_config(event["icn"])
    # add VASRD code
    return main(config, event)


# TODO: (Optional) Figure out a way to unit test this?
# Background: If you try to do a pytest unitest on lambda_handler, then
# load_config(event["icn"]) will fail.
# This is because the load_config is called this way (without a key_loc param),
# because the lambda_handler is supposed to run in lambda.
# And so, if you run this with pytest, key_loc is not defined, and so
# load_config tries to fetch the Lighthouse RSA key from AWS SecretsManager
# using boto3. And this fails of course.
