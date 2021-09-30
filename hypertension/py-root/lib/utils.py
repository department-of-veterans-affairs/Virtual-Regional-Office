import json
import os
from pathlib import Path
from typing import Union, Optional

from lib.aws_secrets_manager import (
    get_lighthouse_rsa_key,
    get_secret_from_secrets_manager_by_name,
)


def load_config(
    icn: str,
    key_loc: Optional[str] = None,
    client_id_loc: Optional[str] = None,
) -> dict:

    if key_loc:
        secret = load_secret(key_loc)
    else:
        secret = get_lighthouse_rsa_key(
            os.environ["LighthousePrivateRsaKeySecretArn"]
        )

    if client_id_loc:
        client_id = load_secret(client_id_loc)
    else:
        client_id = get_secret_from_secrets_manager_by_name(
            os.environ["LighthousePrivateClientIdArn"]
        )

    return {
        "lighthouse": {
            "auth": {
                "token_url": os.environ["LighthouseTokenUrl"],
                "jwt_aud_url": os.environ["LighthouseJwtAudUrl"],
                "grant_type": os.environ["LighthouseOAuthGrantType"],
                "client_assertion_type": os.environ[
                    "LighthouseOAuthAssertionType"
                ],
                "scope": os.environ["LighthouseJwtScope"],
                "secret": secret,
                "client_id": client_id,
            },
            "vet_health_api_observation": {
                "fhir_observation_endpoint": os.environ[
                    "LighthouseObservationUrl"
                ],
                "fhir_category": os.environ["LighthouseObservationCategory"],
                "fhir_loinc_code": os.environ[
                    "LighthouseObservationLoincCode"
                ],
            },
            "icn": icn,
        }
    }


def load_secret(key_file: Union[Path, str]) -> str:
    if Path(key_file).exists():
        return Path(key_file).read_text()

    raise SystemError(f"Keyfile {key_file} not found")


def load_text(path: Union[Path, str]) -> str:
    return Path(path).read_text()


def load_json(path: Union[Path, str]) -> dict:
    raw = load_text(path)
    return json.loads(raw)
