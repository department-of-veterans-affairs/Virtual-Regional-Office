import re
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv("../.env")


def update_file(path, search_regex, new_string):
    orig = Path(path).read_text(encoding="utf-8")

    p = re.compile(search_regex)
    new_file_contents = p.sub(new_string, orig)

    Path(path).write_text(new_file_contents, encoding="utf-8")


def set_parameter_overrides(samconfig_file_path):
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
        "PdfGeneratorLayerArn",
        "PythonDependenciesLayerArn",
    ]

    strings = []

    for key in keys:
        strings.append(f'{key}=\\"{os.environ[key]}\\"')

    params = " ".join(strings)

    # fmt: off
    parameter_overrides = 'parameter_overrides = \"' + params + '\"'
    # fmt: on

    samconfig_po_regex = r"parameter_overrides\s=\s.*"

    update_file(samconfig_file_path, samconfig_po_regex, parameter_overrides)


if __name__ == "__main__":
    set_parameter_overrides("../samconfig.toml")
