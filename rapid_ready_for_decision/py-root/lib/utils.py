import json
import os
from pathlib import Path
from typing import Union, Optional

from lib.aws_secrets_manager import (
    get_lighthouse_rsa_key,
    get_secret_from_secrets_manager_by_name,
)


def load_config(
        icn,
        key_loc=None,
        client_id=None,
):

    if key_loc:
        secret = load_secret(key_loc)
    else:
        secret = get_lighthouse_rsa_key(
            os.environ["LighthousePrivateRsaKeySecretArn"]
        )

    if not client_id:
        client_id = get_secret_from_secrets_manager_by_name(
            os.environ["VroLighthouseOAuthClientIdArn"]
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
                "fhir_endpoint": os.environ[
                    "LighthouseObservationUrl"
                ],
                "fhir_category": os.environ["LighthouseObservationCategory"],
                "fhir_code": os.environ[
                    "LighthouseObservationLoincCode"
                ],
            },
            "vet_health_api_condition": {
                "fhir_endpoint": os.environ[
                    "LighthouseConditionUrl"
                ],
                "fhir_category": "encounter-diagnosis",
                "fhir_clinical_status": "active",
            },
            "vet_health_api_medication": {
                "fhir_endpoint": os.environ[
                    "LighthouseMedicationUrl"
                ],
                "fhir_category": ""
            },
            "vet_health_api_procedure": {
                "fhir_endpoint": os.environ[
                    "LighthouseProcedureUrl"
                ],
                "fhir_category": ""
            },
            "icn": icn,
        }
    }


def load_secret(key_file: Union[Path, str]) -> str:
    if Path(key_file).exists():
        return Path(key_file).read_text(encoding="utf-8")

    raise SystemError(f"Keyfile {key_file} not found")


def load_text(path: Union[Path, str]) -> str:
    return Path(path).read_text(encoding="utf-8")


def load_json(path: Union[Path, str]) -> dict:
    raw = load_text(path)
    return json.loads(raw)
