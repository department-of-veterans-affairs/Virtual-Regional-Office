from functions.medical_record_locator import app
from tests import utils

def test_located_record():
    input_payload = {
        "body": {
            "claim_status": {
                "applicable": True,
                "pvid": 123
            }
        }
    }
    data = app.lambda_handler(input_payload, "")
    utils.confirm_response(data)
    claim_status = data["claim_status"]
    assert claim_status["icn"] == 1001096151

def test_missing_record():
    input_payload = {
        "body": {
            "claim_status": {
                "applicable": True,
                "pvid": 123
            }
        }
    }
    data = app.lambda_handler(input_payload, "")
    utils.confirm_response(data)
    claim_status = data["claim_status"]
    assert claim_status["icn"] == None

