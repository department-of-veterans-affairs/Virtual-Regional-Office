import app


def test_record_updater():
    input_payload = {
        "body": {
            "claim_status": {}
        }
    }
    data = app.lambda_handler(input_payload, "")
    assert data["statusCode"] == 200
    assert "body" in data
    body = data["body"]
    assert "claim_status" in body
