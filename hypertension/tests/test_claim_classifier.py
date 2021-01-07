from functions.claim_classifier import app
from tests import utils

def test_function():
    input_payload = {
        "claim_type": "disability",
        "medication": [],
        "readings": []
    }
    data = app.lambda_handler(input_payload, "")
    utils.confirm_response(data)
    claim_status = body["claim_status"]

def test_assess_criteria():
    # TODO: Add various test cases for classifier logic
    pass