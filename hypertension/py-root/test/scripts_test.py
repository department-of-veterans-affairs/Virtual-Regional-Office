import os
import re
from pathlib import Path
from unittest import mock
from test.data.env import fake_env
from set_parameter_overrides import set_parameter_overrides


# TODO: Add more tests of set_parameter_overrides()
# - Add test for present and absent newline character after the
# `parameter_overrides` line
# - Add test for when there's a line in the samconfig.toml file that is
# *after* the parameter_overrides line
@mock.patch.dict(os.environ, fake_env)
def test_set_parameter_overrides():
    # Get actual
    samconfig_file_path = "./test/data/samconfig-default.toml"
    set_parameter_overrides(samconfig_file_path)
    actual = Path(samconfig_file_path).read_text()

    # Construct expected
    samconfig_default_content = """version = 0.1
[default]
[default.deploy]
[default.deploy.parameters]
parameter_overrides = "DUMMY_VALUE___OVERWRITE_BEFORE_YOU_DEPLOY"
"""

    keys = [
        "LighthouseTokenUrl",
        "LighthouseJwtAudUrl",
        "LighthouseJwtScope",
        "LighthouseOAuthClientId",
        "LighthouseOAuthGrantType",
        "LighthouseOAuthAssertionType",
        "KmsCmkId",
        "LighthouseObservationUrl",
        "LighthouseObservationCategory",
        "LighthouseObservationLoincCode",
    ]

    strings = []

    for key in keys:
        strings.append(f'{key}=\\"{os.environ[key]}\\"')

    params = " ".join(strings)

    # fmt: off
    parameter_overrides = 'parameter_overrides = \"' + params + '\"'
    # fmt: on

    regex = 'parameter_overrides = "DUMMY_VALUE___OVERWRITE_BEFORE_YOU_DEPLOY"'
    p = re.compile(regex)
    expected = p.sub(parameter_overrides, samconfig_default_content)

    assert actual == expected

    # Cleanup
    Path(samconfig_file_path).write_text(samconfig_default_content)
