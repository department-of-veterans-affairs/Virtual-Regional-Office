import json
from typing import Dict
from .algorithms.utils import validate_request_body
from .algorithms.active_condition import active_cancer_condition
from .algorithms.medication import medication_match
from .algorithms.procedure import procedure_match


def main(event: Dict):
    """
    Take a request that includes hypertension related data, and return a response

    :param event: request body
    :type event: dict
    :return: response body
    :rtype: dict
    """
    request_body = event
    # JB: If running with lambda app, change line 18 to: request_body = json.loads(event["body"])

    statusCode = 200

    validation_results = validate_request_body(request_body)
    response_body = {}
    rrd_eligible = False

    if validation_results["is_valid"]:

        active_cancer_result = active_cancer_condition(request_body)
        medication_match_result = medication_match(request_body)
        procedure_match_result = procedure_match(request_body)

        if active_cancer_result["active_cancer_present"] or \
                medication_match_result["continuous_medication_required"] or \
                medication_match_result["procedure_within_six_months"]:
            rrd_eligible = True

    else:
        statusCode = 400
        active_cancer_result = {"success": False}
        medication_match_result = {"success": False}
        procedure_match_result = {"success": False}
        response_body["errors"] = validation_results["errors"]

    response_body.update({
        "rrd_eligible": rrd_eligible,
        "evidence": {
            "active_cancer_result": active_cancer_result,
            "medication_match_result": medication_match_result,
            "procedures_in_last_six_months": procedure_match_result,
        }
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
