import app


def test_insufficient_data():
    input_payload = {
        "body": {
            "claim_status": {
                "icn": 1001096151
            }
        }
    }
    data = app.lambda_handler(input_payload, "")
    assert data["statusCode"] == 200
    assert "body" in data
    body = data["body"]
    assert "claim_status" in body
    claim_status = body["claim_status"]
    assert "data" in claim_status
    data = claim_status["data"]
    assert "medication" in data
    assert "readings" in data
    assert "hasEnoughData" in claim_status


def test_has_enough_data():
    insufficient_data = [{}]
    assert app.has_enough_data(insufficient_data) == False
    sufficient_data = [{}, {}]
    assert app.has_enough_data(sufficient_data) == True
