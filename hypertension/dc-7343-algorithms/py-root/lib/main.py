import json
from typing import Dict
from .algorithms.utils import validate_request_body
from .algorithms.active_condition import active_cancer_condition
from .algorithms.medication import medication_match


def main(event: Dict):
    """
    Take a request that includes hypertension related data, and return a response

    :param event: request body
    :type event: dict
    :return: response body
    :rtype: dict
    """
    request_body = event.json

    statusCode = 200

    validation_results = validate_request_body(request_body)
    response_body = {}

    if validation_results["is_valid"]:

        active_cancer_result = active_cancer_condition(request_body)
        medication_match_result = medication_match(request_body)
        medication_match_result_status = medication_match_result["success"]
        active_cancer_result_status = active_cancer_result["success"]

        if not all([medication_match_result_status, active_cancer_result_status]):
            statusCode = 209

    else:
        statusCode = 400
        active_cancer_result = {"success": False}
        medication_match_result = {"success": False}
        response_body["errors"] = validation_results["errors"]

    response_body.update({
        "active_cancer": active_cancer_result,
        "requires_continuous_medication": medication_match_result
    })

    return {
        "statusCode": statusCode,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST"
        },
        "body": json.dumps(response_body)
    }


