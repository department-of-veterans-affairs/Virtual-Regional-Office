from functions.record_uploader import app
from tests import utils

def test_record_uploader():
    input_payload = {
        "body": {
            "claim_status": {}
        }
    }
    data = app.lambda_handler(input_payload, "")
    utils.confirm_response(data)