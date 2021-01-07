from functions.applicability_determiner import app

def test_disability_increase():
    input_payload = {
        "claim_type": "disability",
        "claim_subtype": "increase",
        "pvid": "123"
    }
    data = app.lambda_handler(input_payload, "")
    confirm_response(data)
    claim_status = body["claim_status"]
    assert "claim_type" in claim_status
    assert "claim_subtype" in claim_status
    assert claim_status["applicable"] == True

def test_disability_new():
    input_payload = {
        "claim_type": "disability",
        "claim_subtype": "new"
    }
    data = app.lambda_handler(input_payload, "")
    confirm_response(data)
    assert "claim_type" in claim_status
    assert "claim_subtype" in claim_status
    assert claim_status["applicable"] == False

def confirm_response(data):
    assert data["statusCode"] == 200
    assert "body" in data
    body = data["body"]
    assert "claim_status" in body