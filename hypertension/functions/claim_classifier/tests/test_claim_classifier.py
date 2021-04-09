import app


def test_function():
    input_payload = {
        "body": {
            "claim_status": {
                "claim_type": "disability",
                "data": {
                    "medication": [1, 2, 3],
                    "readings": [{
                        "stationNumber": "689",
                        "facility": "(689) Connecticut HCS (Westhaven)",
                        "systolic": "105",
                        "diastolic": "54",
                        "datetime": "2020-11-19 01:22"
                    },
                        {
                        "stationNumber": "689",
                        "facility": "(689) Connecticut HCS (Westhaven)",
                        "systolic": "106",
                        "diastolic": "54",
                        "datetime": "2020-11-18 11:40"
                    }]
                }
            }
        }
    }
    data = app.lambda_handler(input_payload, "")
    assert data["statusCode"] == 200
    assert "body" in data
    body = data["body"]
    assert "claim_status" in body
    claim_status = body["claim_status"]


def test_assess_criteria():
    # TODO: Add various test cases for classifier logic
    pass
