from lib.main import main  # pragma: no cover (main is tested elsewhere)


def lambda_handler(event, context):  # pragma: no cover
    return main()
