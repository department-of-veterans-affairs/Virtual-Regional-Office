import os
from pathlib import Path
from typing import (
    Union,
    Optional
)

from lib.aws_secrets_manager import get_lighthouse_rsa_key

def load_config(icn: str, key_loc: Optional[str] = None) -> dict:
    return {
        "lighthouse": {
            "auth": {
                "token_url": os.environ["LighthouseTokenUrl"],
                "jwt_aud_url": os.environ["LighthouseJwtAudUrl"],
                "grant_type": os.environ["LighthouseOAuthGrantType"],
                "client_assertion_type": os.environ["LighthouseOAuthAssertionType"],
                "scope": os.environ["LighthouseJwtScope"],
                "secret": load_secret(key_loc) if key_loc else get_lighthouse_rsa_key(os.environ["LighthousePrivateRsaKeySecretArn"]),
                "client_id": os.environ["LighthouseOAuthClientId"]
            },
            "vet_health_api_observation": {
                "fhir_observation_endpoint": os.environ["LighthouseObservationUrl"],
                "fhir_category": os.environ["LighthouseObservationCategory"],
                "fhir_loinc_code": os.environ["LighthouseObservationLoincCode"],
            },
            "icn": icn
        }
    }


def load_secret(key_file: Union[Path, str]) -> str:
    if Path(key_file).exists():
        return Path(key_file).read_text()

    raise SystemError(f"Keyfile {key_file} not found")
