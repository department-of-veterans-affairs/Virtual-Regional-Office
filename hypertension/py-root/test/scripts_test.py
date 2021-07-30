import os
import re
from pathlib import Path
from unittest import mock
from set_parameter_overrides import set_parameter_overrides 

# TODO: Figure out where to put this. Make a const?
fake_env = {
    "LighthouseTokenUrl": "DUMMY_DONT_CARE",
    "LighthouseJwtAudUrl": "DUMMY_DONT_CARE",
    "LighthouseJwtScope": "DUMMY_DONT_CARE",
    "LighthouseOAuthClientId": "DUMMY_DONT_CARE",
    "LighthouseOAuthGrantType": "DUMMY_DONT_CARE",
    "LighthouseOAuthAssertionType": "DUMMY_DONT_CARE",
    "KmsCmkId": "DUMMY_DONT_CARE",
    "LighthouseObservationUrl": "DUMMY_DONT_CARE",
    "LighthouseObservationCategory": "DUMMY_DONT_CARE",
    "LighthouseObservationLoincCode": "DUMMY_DONT_CARE"
}

# TODO: Parametrize this test?
# TODO: Break this out into test_update_file() and take that part out of test_set_parameter_overrides()? Or just keep it like it is because that's simpler?
@mock.patch.dict(os.environ, fake_env)
def test_set_parameter_overrides():
    # Get actual
    samconfig_file_path = './samconfig-default.toml'
    set_parameter_overrides(samconfig_file_path)
    actual = Path(samconfig_file_path).read_text()

    # Construct expected
    # TODO: Instead of this should we do the following?
    # - filesystem cp the root dir samconfig-default.toml into your test dir,
    # - then read it into here
    # - then do your operations on the copied version of the samconfig-default.toml
    # - then finish this test
    # - thenn delete the copied version of samconfig-default.toml
    samconfig_default_content = """version = 0.1
[default]
[default.deploy]
[default.deploy.parameters]
parameter_overrides = "DUMMY_VALUE___OVERWRITE_THIS_BEFORE_YOU_DEPLOY"
"""

    parameter_overrides = f'parameter_overrides = \"LighthouseTokenUrl=\\"{fake_env["LighthouseTokenUrl"]}\\" LighthouseJwtAudUrl=\\"{fake_env["LighthouseJwtAudUrl"]}\\" LighthouseJwtScope=\\"{fake_env["LighthouseJwtScope"]}\\" LighthouseOAuthClientId=\\"{fake_env["LighthouseOAuthClientId"]}\\" LighthouseOAuthGrantType=\\"{fake_env["LighthouseOAuthGrantType"]}\\" LighthouseOAuthAssertionType=\\"{fake_env["LighthouseOAuthAssertionType"]}\\" KmsCmkId=\\"{fake_env["KmsCmkId"]}\\" LighthouseObservationUrl=\\"{fake_env["LighthouseObservationUrl"]}\\" LighthouseObservationCategory=\\"{fake_env["LighthouseObservationCategory"]}\\" LighthouseObservationLoincCode=\\"{fake_env["LighthouseObservationLoincCode"]}\\"\"'

    regex = 'parameter_overrides = "DUMMY_VALUE___OVERWRITE_THIS_BEFORE_YOU_DEPLOY"'
    p = re.compile(regex)
    expected = p.sub(parameter_overrides, samconfig_default_content)

    assert actual == expected

    # Cleanup
    Path(samconfig_file_path).write_text(samconfig_default_content)

# TODO: Add test for present and absent newline character after the `parameter_overrides` line
# TODO: Add test for when there's a line in the samconfig.toml file that is _after_ the parameter_overrides line
