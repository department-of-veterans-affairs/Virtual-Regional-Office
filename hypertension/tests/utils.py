def confirm_response(data):
    assert data["statusCode"] == 200
    assert "body" in data
    body = data["body"]
    assert "claim_status" in body