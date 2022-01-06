import json
import pytest
from lib.main import main

@pytest.mark.parametrize(
    "request_body, response",
    [
        # All three calculator functions return valid results readings
        (
            {
                "body": json.dumps({
                    "bp": [
                        {
                            "diastolic": 115,
                            "systolic": 180,
                            "date": "2021-11-01"
                        },
                        {
                            "diastolic": 110,
                            "systolic": 200,
                            "date": "2021-09-01"
                        }
                    ],
                    "medication": ["Capoten"],
                    "date_of_claim": "2021-11-09",
                    "veteran_is_service_connected": True
                })
            },
            {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Headers" : "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST"
                },
                "body": json.dumps({
                    "predominance_calculation": {
                        "success": True,
                        "predominant_diastolic_reading": 115,
                        "predominant_systolic_reading": 180
                    },
                    "diastolic_history_calculation": {
                        "diastolic_bp_predominantly_100_or_more": True,
                        "success": True
                    },
                    "requires_continuous_medication": {
                        "continuous_medication_required": True,
                        "success": True
                    }
                })
            }
        ),
        # sufficient_to_autopopulate returns "success": False, but history_of_diastolic_bp doesn"t
        # Note that the inverse can"t happen (where history_of_diastolic_bp fails while sufficient_to_autopopulate doesn"t)
        # because the only way history_of_diastolic_bp can fail is if there are no bp readings, which would cause
        # sufficient_to_autopopulate to fail as well 
        (
            {
                "body": json.dumps({
                    "bp": [
                        {
                            "diastolic": 115,
                            "systolic": 180,
                            "date": "2020-11-01"
                        },
                        {
                            "diastolic": 110,
                            "systolic": 200,
                            "date": "2020-09-01"
                        }
                    ],
                    "medication": [],
                    "date_of_claim": "2021-11-09",
                    "veteran_is_service_connected": True
                })
            },
            {
                "statusCode": 209,
                "headers": {
                    "Access-Control-Allow-Headers" : "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST"
                },
                "body": json.dumps({
                    "predominance_calculation": {
                        "success": False,
                    },
                    "diastolic_history_calculation": {
                        "diastolic_bp_predominantly_100_or_more": True,
                        "success": True
                    },
                    "requires_continuous_medication": {
                        "continuous_medication_required": False,
                        "success": True
                    }
                })
            }
        ),
        # sufficiency and history algos fail
        (
            {
                "body": json.dumps({
                    "bp": [],
                    "medication": [],
                    "date_of_claim": "2021-11-09",
                    "veteran_is_service_connected": True
                })
            },
            {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Headers" : "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST"
                },
                "body": json.dumps({
                    "predominance_calculation": {
                        "success": False,
                    },
                    "diastolic_history_calculation": {
                        "success": False
                    },
                    "requires_continuous_medication": {
                        "continuous_medication_required": False,
                        "success": True
                    }
                })
            }
        ),
        # # Bad data - "diastolic" key is missing in second reading
        (
            {
                "body": json.dumps({
                    "bp": [
                        {
                            "diastolic": 111,
                            "systolic": 200,
                            "date": "2021-09-01"
                        },
                        {
                            "systolic": 180,
                            "date": "2021-11-01"
                        }
                    ],
                    "date_of_claim": "2021-11-09",
                })
            },
            {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Headers" : "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST"
                },
                "body": json.dumps({
                    "predominance_calculation": {
                        "success": False,
                    },
                    "diastolic_history_calculation": {
                        "success": False
                    },
                    "requires_continuous_medication": {
                        "success": False
                    },
                    "errors": {"bp": [{"1": [{"diastolic": ["required field"]}]}]}
                })
            }
        ),
        # # Bad data - "diastolic" value is string instead of int, medication is an int, veteran_is... is a string
        (
            {
                "body": json.dumps({
                    "bp": [
                        {
                            "diastolic": "180",
                            "systolic": 200,
                            "date": "2021-09-01"
                        },
                        {
                            "diastolic": 120,
                            "systolic": 180,
                            "date": "2021-11-01"
                        }
                    ],
                    "date_of_claim": "2021-11-09",
                    "medication": [11],
                    "veteran_is_service_connected": "True"
                })
            },
            {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Headers" : "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST"
                },
                "body": json.dumps({
                    "predominance_calculation": {
                        "success": False,
                    },
                    "diastolic_history_calculation": {
                        "success": False
                    },
                    "requires_continuous_medication": {
                        "success": False
                    },
                    "errors": {
                        "bp": [{"0": [{"diastolic": ["must be of integer type"]}]}],
                        "medication": [{"0": ["must be of string type"]}],
                        "veteran_is_service_connected": ["must be of boolean type"]
                    }
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
    api_response = main(request_body)

    assert json.loads(api_response["body"]) == json.loads(response["body"])
