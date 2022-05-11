import json
import pytest
from lib.main import main

@pytest.mark.parametrize(
    "request_body, response",
    [
        # All three calculator functions return valid results readings
        (
                {
                    "body": json.dumps(
                        {
                            "condition": [
                                {
                                    "code": 363419009,
                                    "status": "active",
                                    "text": "Malignant tumor of head of pancreas (disorder)",
                                    "onset_date": "2021-11-01",
                                    "abatement_date": "2022-04-01"
                                },
                            ],
                            "medication": [{"text": "5-fluorouracil",
                                            "code": 4492,
                                            "date": "2022-04-01"},
                                           {"text": "Irinotecan",
                                            "code": 1726319,
                                            "date": "2022-04-01"}],
                            "procedure": [
                                {
                                    "code": "174710004",
                                    "text": "(Surgery - distal subtotal pancreatectomy)",
                                    "performed_date": "2021-12-01",
                                    "last_update_date": "2021-12-15",
                                    "status": "completed"
                                }
                            ],
                            "date_of_claim": "2021-11-09",
                        })
                },
                {
                    "statusCode": 200,
                    "headers": {
                        "Access-Control-Allow-Headers": "Content-Type",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "OPTIONS,POST"
                    },
                    "body": json.dumps({
                        "active_cancer": {
                            "success": True,
                            "active_cancer_present": True,
                            "active_cancer_matches_count": 1
                        },
                        "requires_continuous_medication": {
                            "continuous_medication_required": True,
                            "continuous_medication_matches_count": 2,
                            "success": True
                        },
                        'procedures_in_last_six_months': {'pc_procedure_within_six_months': True,
                                                          'success': True},
                    })
                }
        ),
        (
                {
                    "body": json.dumps({

                        "condition": [
                            {
                                "code": 363419009,
                                "text": "Malignant tumor of head of pancreas (disorder)",
                                "onset_date": "2021-11-01",
                                "abatement_date": "2022-04-01"
                            },
                        ],
                        "procedure": [
                            {
                                "code": "174710004",
                                "text": "(Surgery - distal subtotal pancreatectomy)",
                                "performed_date": "2021-12-01",
                                "last_update_date": "2021-12-15",
                                "status": "completed"
                            }
                        ],
                        "medication": [],
                        "date_of_claim": "2021-11-09",
                    })
                },
                {
                    "statusCode": 209,
                    "headers": {
                        "Access-Control-Allow-Headers": "Content-Type",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "OPTIONS,POST"
                    },
                    "body": json.dumps({
                        "active_cancer": {
                            "success": True,
                            "active_cancer_present": True,
                            "active_cancer_matches_count": 1
                        },
                        "requires_continuous_medication": {
                            "continuous_medication_required": False,
                            "continuous_medication_matches_count": 0,
                            "success": True
                        },
                        'procedures_in_last_six_months': {'pc_procedure_within_six_months': True,
                                                          'success': True},
                    })
                }
        ),
        # Condition and Medication algorithms fail
        (
                {
                    "body": json.dumps({
                        "condition": [],
                        "medication": [],
                        "procedure": [],
                        "date_of_claim": "2021-11-09",
                    })
                },
                {
                    "statusCode": 400,
                    "headers": {
                        "Access-Control-Allow-Headers": "Content-Type",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "OPTIONS,POST"
                    },
                    "body": json.dumps({
                        "active_cancer": {
                            "success": True,
                            "active_cancer_present": False,
                            "active_cancer_matches_count": 0
                        },
                        "requires_continuous_medication": {
                            "continuous_medication_required": False,
                            "continuous_medication_matches_count": 0,
                            "success": True
                        },
                        'procedures_in_last_six_months': {'pc_procedure_within_six_months': False,
                                                          'success': True},
                    })
                }
        ),
    ],
)
def test_main(request_body, response):
    """
    Test the function that takes the request and returns the response

    :param request_body: request body with blood pressure readings and other data
    :type request_body: dict
    :param response: response after running data through algorithms
    :type response: dict
    """
    api_response = main(json.loads(request_body["body"]))

    assert json.loads(api_response["body"]) == json.loads(response["body"])
