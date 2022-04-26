from lib.main import main  # pragma: no cover (main is tested elsewhere)


# pylint: disable=unused-argument
def lambda_handler(event, context):  # pragma: no cover
    return main(event)
