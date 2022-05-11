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
        "condition": {
            "type": "list",
            "schema": {
                "type": "dict",
                "schema": {
                    "code": {"type": "string"},
                    "status": {"type": "string"},
                    "text": {"type": "string"},
                    "onset_date": {"type": "string"},
                    "abatement_date": {"type": "string"}
                    }
                }
            },
        "medication": {
            "type": "list",
            "schema": {
                "type": "dict",
                "schema": {
                    "authored_on": {"type": "string"},
                    "date": {"type": "string"},
                    "status": {"type": "string"},
                    "text": {"type": "string"},
                    "code": {"type": "string"}
                    }
                }
            },
        "procedure": {
            "type": "list",
            "schema": {
                "type": "dict",
                "schema": {
                    "code": {"type": "string"},
                    "code_system": {"type": "string"},
                    "text": {"type": "string"},
                    "performed_date": {"type": "string"},
                    "status": {"type": "string"},
                }
            }
        }
    }

    v = Validator(schema)

    return {
        "is_valid": v.validate(request_body),
        "errors": v.errors
    }
