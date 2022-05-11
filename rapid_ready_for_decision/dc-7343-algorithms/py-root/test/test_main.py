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
                                    "code": "363419009",
                                    "status": "active",
                                    "text": "Malignant tumor of head of pancreas (disorder)",
                                    "onset_date": "2021-11-01",
                                    "abatement_date": "2022-04-01"
                                },
                            ],
                            "medication": [{"text": "5-fluorouracil",
                                            "code": "4492",
                                            "status": "active",
                                            "date": "2022-04-01"},
                                           {"text": "Irinotecan",
                                            "code": "1726319",
                                            "status": "active",
                                            "date": "2022-04-01"}],
                            "procedure": [
                                {
                                    "code": "174710004",
                                    "code_system": "http://snomed.info/sct",
                                    "text": "(Surgery - distal subtotal pancreatectomy)",
                                    "performed_date": "2021-12-01",
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
                    "body": json.dumps(
                        {'evidence': {
                            'active_cancer_result': {
                                'active_cancer_present': True,
                                'success': True
                            },
                            'medication_match_result': {
                                'continuous_medication_required': True,
                                'success': True
                            },
                            'procedures_in_last_six_months': {
                                'procedure_within_six_months': True,
                                'success': True
                            }
                        },
                            'rrd_eligible': True}
                    )
                }
        ),
        (
                {
                    "body": json.dumps({

                        "condition": [
                            {
                                "code": "363419009",
                                "status": "active",
                                "text": "Malignant tumor of head of pancreas (disorder)",
                                "onset_date": "2021-11-01",
                                "abatement_date": "2022-04-01"
                            },
                        ],
                        "procedure": [
                            {
                                "code": "174710004",
                                "code_system": "http://snomed.info/sct",
                                "text": "(Surgery - distal subtotal pancreatectomy)",
                                "performed_date": "2021-12-01",
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
                    "body": json.dumps(
                        {
                            'evidence': {
                                'active_cancer_result': {
                                    'active_cancer_present': True,
                                    'success': True
                                },
                                'medication_match_result': {
                                    'continuous_medication_required': False,
                                    'success': True
                                },
                                'procedures_in_last_six_months': {
                                    'procedure_within_six_months': True,
                                    'success': True
                                }
                            },
                            'rrd_eligible': True
                        }
                    )
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
                    "body": json.dumps(
                        {
                            'evidence': {
                                'active_cancer_result': {
                                    'active_cancer_present': False,
                                    'success': True
                                },
                                'medication_match_result': {
                                    'continuous_medication_required': False,
                                    'success': True
                                },
                                'procedures_in_last_six_months': {
                                    'procedure_within_six_months': False,
                                    'success': True
                                }
                            },
                            'rrd_eligible': False
                        }
                    )
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
