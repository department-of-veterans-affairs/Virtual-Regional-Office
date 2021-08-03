import pytest
import sys
import os
from dotenv import load_dotenv

from lib.utils import (
    load_config
)

from lib.lighthouse import (
    authenticate_to_lighthouse
)

from get_token_make_api_request import (
    load_config,
    setup_cli_parser,
    authenticate_to_lighthouse
)


load_dotenv("../cf-template-params.env")

os.environ[
    "LighthousePrivateRsaKeySecretArn"
] = "Fake. Not used. Doesnt Matter. Just need something. Anything."


# monkeypatch is a function-scoped fuxture. Because of this, you can't use it inside a
# session-scoped fixtures. To get around this, we create a new instance of the monkeypatch fixture
# that is session-scoped, for use in our other fixtures that need to be session scoped.
# This is subject to breaking if pytest changes, because it uses the internal _pytest API.
# See https://github.com/pytest-dev/pytest/issues/1872

# REMOVE THIS ???????????????????????????????????????????/
@pytest.fixture(scope='session')
def monkeypatch_session():
    from _pytest.monkeypatch import MonkeyPatch
    m = MonkeyPatch()
    yield m
    m.undo()


@pytest.fixture(scope="session")
def lh_access_token(config):
    icn = config["lighthouse"]["icn"]
    access_token = authenticate_to_lighthouse(config["lighthouse"]["auth"], icn)
    return access_token


@pytest.fixture(scope="session")
def config(cli_options):
    config = load_config(cli_options.icn, os.environ["LighthousePrivateRsaKeyFilePath"])
    return config


@pytest.fixture(scope="session")
def cli_options():
    cli_options = setup_cli_parser().parse_args([
        os.environ["TestVeteranIcn"]
    ])

    return cli_options
