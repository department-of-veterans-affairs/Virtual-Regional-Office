# pylint: disable=redefined-outer-name,wrong-import-order,wrong-import-position

import os
from pathlib import Path
import pytest
import subprocess

from _pytest.monkeypatch import MonkeyPatch
from dotenv import load_dotenv

load_dotenv("../.env.test.env")

import lib.lighthouse as lighthouse  # noqa: E402
from lib.utils import load_config, load_secret  # noqa: E402
from test.doubles.lighthouse import (  # noqa: E402
    http_post_for_access_token_double,
)

os.environ[
    "LighthousePrivateRsaKeySecretArn"
] = "Fake. Not used. Doesnt Matter. Just need something. Anything."


# monkeypatch is a function-scoped fixture. Because of this, you can't use it
# inside session-scoped fixtures. To get around this, we create a new
# instance of the monkeypatch fixture that is session-scoped, for use in our
# other fixtures that need to be session scoped. This is subject to breaking if
# pytest changes, because it uses the internal _pytest API.
# See https://github.com/pytest-dev/pytest/issues/1872
@pytest.fixture(scope="session")
def monkeypatch_session():
    m = MonkeyPatch()
    yield m
    m.undo()


@pytest.fixture(scope="session")
def lh_access_token(config, monkeypatch_session):
    icn = config["lighthouse"]["icn"]
    monkeypatch_session.setattr(
        lighthouse,
        "http_post_for_access_token",
        http_post_for_access_token_double,
    )
    access_token = lighthouse.authenticate_to_lighthouse(
        config["lighthouse"]["auth"], icn
    )
    return access_token


@pytest.fixture(scope="session")
def config():
    config = load_config(
        os.environ["TestVeteranIcn"],
        os.environ["LighthousePrivateRsaKeyFilePath"],
        os.environ["TestClientId"],
    )
    config["html"] = "<html><body>Hello World!</body></html>"
    return config


@pytest.fixture(scope="session")
def public_rsa_key():
    return load_secret(os.environ["LighthousePublicRsaKeyFilePath"])


# Set the wkhtmltopdf path environment variable by finding the local binary
which_wkhtmltopdf = subprocess.run(
    "which wkhtmltopdf", shell=True, capture_output=True
)

wkhtmltopdf_path = Path(which_wkhtmltopdf.stdout.decode().strip()).resolve()
assert wkhtmltopdf_path.exists()
os.environ["WKHTMLTOPDF_PATH"] = str(wkhtmltopdf_path)
