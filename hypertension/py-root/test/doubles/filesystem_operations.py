from pathlib import Path
from typing import Union


def load_text_double(path: Union[Path, str]) -> str:
    if path == "FakePathToLighthouseAuthAssertionsFile":
        return """{
    "urls": {
        "audience": "https://fake-lighthouse-aud-url",
        "token": "https://fake-lighthouse-client-credentials-jwt-request-url"
    },
    "parameters": {
        "grant_type": "client_credentials",
        "client_assertion_type": "fake lighthouse client assertion type",
        "scope": "fake lighthouse scopes"
    }
}"""
    elif path == "FakePathToLighthouseHealthApiObservationRequestParamsFile":
        return """{
    "urls": {
        "endpoint": "https://fake-lighthouse-veterans-health-api-endpoint-for-fhir-observations"
    },
    "parameters": {
        "category": "vital-signs",
        "code": "fake loinc code for blood pressure readings"
    }
}"""
    else:
        return "ERROR"


def load_secret_double(key: Union[Path, str]) -> str:
    if key == "FakePathToLighthouseRsaPrivateKeyPemFile":
        return """-----BEGIN RSA PRIVATE KEY-----
This is fake
-----END RSA PRIVATE KEY-----
"""
    else:
        return "ERROR"
