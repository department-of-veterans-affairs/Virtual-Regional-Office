from cerberus import Validator


def validate_request_body(request_body):
    """
    Validates that the request body conforms to the expected data format

    :param request_body: request body converted from json
    :type request_body: dict
    :return: dict with boolean result showing if request is valid and if not, any applicable errors
    :rtype: dict
    """
    schema = {
        "date_of_claim": {"type": "string"},
        "veteran_is_service_connected_for_dc7101": {"type": "boolean"},
        "bp": {
            "type": "list",
            "schema": {
                "type": "dict",
                "require_all": True,
                "schema": {
                    "diastolic": {"type": "integer"},
                    "systolic": {"type": "integer"},
                    "date": {"type": "string"}
                }
            }
        },
        "medication": {
            "type": "list",
            "schema": {
                "type": "string",
            }
        }
    }
    v = Validator(schema)

    return {
        "is_valid": v.validate(request_body),
        "errors": v.errors
    }
