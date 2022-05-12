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
                    "code": {
                        "type": "string",
                        "required": True
                    },
                    "status": {
                        "type": "string",
                        "required": True
                    },
                    "text": {
                        "type": "string"
                    },
                    "onset_date": {
                        "type": "string",
                        "required": True
                    },
                    "abatement_date": {
                        "type": "string"
                    }
                    }
                }
            },
        "medication": {
            "type": "list",
            "schema": {
                "type": "dict",
                "schema": {
                    "authored_on": {
                        "type": "string"
                    },
                    "status": {
                        "type": "string",
                        "required": True
                    },
                    "text": {
                        "type": "string",
                        "required": True
                    },
                    "code": {
                        "type": "string",
                        "required": True
                    }
                    }
                }
            },
        "procedure": {
            "type": "list",
            "schema": {
                "type": "dict",
                "schema": {
                    "code": {
                        "type": "string",
                        "required": True
                    },
                    "code_system": {
                        "type": "string"
                    },
                    "text": {
                        "type": "string"
                    },
                    "performed_date": {
                        "type": "string",
                        "required": True
                    },
                    "status": {
                        "type": "string",
                        "required": True
                    },
                }
            }
        }
    }

    v = Validator(schema)

    return {
        "is_valid": v.validate(request_body),
        "errors": v.errors
    }
