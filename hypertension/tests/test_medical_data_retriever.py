from functions.medical_data_retriever import app
from tests import utils

def test_insufficient_data():
    input_payload = {
        "body": {
            "claim_status": {
                "icn": 1001096151
            }
        }
    }
    data = app.lambda_handler(input_payload, "")
    utils.confirm_response(data)
    claim_status = data["claim_status"]
    assert "medication" in claim_status
    assert "readings" in claim_status
    assert "hasEnoughData" in claim_status

def test_has_enough_data():
    insufficient_data = [{}]
    assert app.has_enough_data(insufficient_data) == False
    sufficient_data = [{}, {}]
    assert app.has_enough_data(sufficient_data) == True