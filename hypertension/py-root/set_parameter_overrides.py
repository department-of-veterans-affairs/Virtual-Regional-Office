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
    # TODO: Determine a more elegant syntax for this.
    parameter_overrides = f'parameter_overrides = \"LighthouseTokenUrl=\\"{os.environ["LighthouseTokenUrl"]}\\" LighthouseJwtAudUrl=\\"{os.environ["LighthouseJwtAudUrl"]}\\" LighthouseJwtScope=\\"{os.environ["LighthouseJwtScope"]}\\" LighthouseOAuthClientId=\\"{os.environ["LighthouseOAuthClientId"]}\\" LighthouseOAuthGrantType=\\"{os.environ["LighthouseOAuthGrantType"]}\\" LighthouseOAuthAssertionType=\\"{os.environ["LighthouseOAuthAssertionType"]}\\" KmsCmkId=\\"{os.environ["KmsCmkId"]}\\" LighthouseObservationUrl=\\"{os.environ["LighthouseObservationUrl"]}\\" LighthouseObservationCategory=\\"{os.environ["LighthouseObservationCategory"]}\\" LighthouseObservationLoincCode=\\"{os.environ["LighthouseObservationLoincCode"]}\\"\"'

    samconfig_po_regex = r'parameter_overrides\s=\s.*'

    update_file(samconfig_file_path, samconfig_po_regex, parameter_overrides)

set_parameter_overrides('../samconfig.toml')
