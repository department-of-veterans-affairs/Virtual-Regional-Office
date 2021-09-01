import re
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv("../cf-template-params.env")


def update_file(path, search_regex, new_string):
    orig = Path(path).read_text()

    p = re.compile(search_regex)
    new_file_contents = p.sub(new_string, orig)

    Path(path).write_text(new_file_contents)


def set_parameter_overrides(samconfig_file_path):
    # TODO: Put this into its own function?
    params = " ".join(
        [
            f'LighthouseTokenUrl=\\"{os.environ["LighthouseTokenUrl"]}\\"',
            f'LighthouseJwtAudUrl=\\"{os.environ["LighthouseJwtAudUrl"]}\\"',
            f'LighthouseJwtScope=\\"{os.environ["LighthouseJwtScope"]}\\"',
            f'LighthouseOAuthClientId=\\"{os.environ["LighthouseOAuthClientId"]}\\"',
            f'LighthouseOAuthGrantType=\\"{os.environ["LighthouseOAuthGrantType"]}\\"',
            f'LighthouseOAuthAssertionType=\\"{os.environ["LighthouseOAuthAssertionType"]}\\"',
            f'KmsCmkId=\\"{os.environ["KmsCmkId"]}\\"',
            f'LighthouseObservationUrl=\\"{os.environ["LighthouseObservationUrl"]}\\"',
            f'LighthouseObservationCategory=\\"{os.environ["LighthouseObservationCategory"]}\\"',
            f'LighthouseObservationLoincCode=\\"{os.environ["LighthouseObservationLoincCode"]}\\"',
        ]
    )

    # fmt: off
    parameter_overrides = 'parameter_overrides = \"' + params + '\"'
    # fmt: on

    samconfig_po_regex = r"parameter_overrides\s=\s.*"

    update_file(samconfig_file_path, samconfig_po_regex, parameter_overrides)


if __name__ == "__main__":
    set_parameter_overrides("../samconfig.toml")
