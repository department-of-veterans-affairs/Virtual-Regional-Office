import app


def test_located_record():
    input_payload = {
        "body": {
            "claim_status": {
                "applicable": True,
                "pvid": "123"
            }
        }
    }
    data = app.lambda_handler(input_payload, "")
    assert data["statusCode"] == 200
    assert "body" in data
    body = data["body"]
    assert "claim_status" in body
    claim_status = body["claim_status"]
    assert claim_status["icn"] == "1001096151"


def test_missing_record():
    input_payload = {
        "body": {
            "claim_status": {
                "applicable": True,
                "pvid": "404"
            }
        }
    }
    data = app.lambda_handler(input_payload, "")
    assert data["statusCode"] == 200
    assert "body" in data
    body = data["body"]
    assert "claim_status" in body
    claim_status = body["claim_status"]
    assert claim_status["icn"] == None
