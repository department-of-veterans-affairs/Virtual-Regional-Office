import pytest
from lib.algorithms.utils import validate_request_body


@pytest.mark.parametrize(
    "request_body, result_is_valid, errors",
    [
        (
                {
                    "condition": [
                        {
                            "code": "363419009",
                            "status": "active",
                            "text": "Malignant tumor of head of pancreas (disorder)",
                            "onset_date": "2021-11-01",
                            "abatement_date": "2022-04-01"
                        }
                    ],
                    "medication": [{"text": "5-fluorouracil",
                                    "status": "active",
                                    "code": "4492",
                                    "date": "2022-04-01"},
                                   {"text": "Irinotecan",
                                    "status": "active",
                                    "code": "1726319",
                                    "date": "2022-04-01"}],
                    "procedure": [
                        {
                            "code": "174710004",
                            "text": "(Surgery - distal subtotal pancreatectomy)",
                            "performed_date": "2021-12-01",
                            "code_system":  "http://snomed.info/sct",
                            "status": "completed"
                        }
                    ],
                    "date_of_claim": "2021-11-09"
                },
                True,
                {}
        ),
        (
                {
                    "condition": [
                        {
                            "code": 363419009,
                            "status": "active",
                            "text": "Malignant tumor of head of pancreas (disorder)",
                            "onset_date": "2021-11-01",
                            "abatement_date": "2022-04-01"
                        }
                    ],
                    "medication": [{"text": 5,
                                    "code": "4492",
                                    "status": "active",
                                    "date": "2022-04-01"},
                                   {"text": "Irinotecan",
                                    "code": "1726319",
                                    "status": "active",
                                    "date": "2022-04-01"}],
                    "procedure": [
                        {
                            "code": 174710004,
                            "text": "(Surgery - distal subtotal pancreatectomy)",
                            "performed_date": "2021-12-01",
                            "code_system": "http://snomed.info/sct",
                            "status": "completed"
                        }
                    ],
                    "date_of_claim": 20211109,
                },
                False,
                {
                    "condition": [
                        {
                            0: [
                                {
                                    "code": ["must be of string type"],
                                }
                            ]
                        }
                    ],
                    'medication': [
                        {
                            0: [{'text': ['must be of string type']}]}],
                    "procedure": [
                        {
                            0: [
                                {
                                    "code": ["must be of string type"],
                                }
                            ]
                        }
                    ],
                    "date_of_claim": ["must be of string type"],
                }
        ),
    ],
)
def test_validate_request_body(request_body, result_is_valid, errors):
    """
    Test function

    :param date_of_claim: string representation of the date of claim
    :type date_of_claim: string
    :param result: boolean describing whether or not the blood pressure readings meet the specifications
    :type result: bool
    """
    result = validate_request_body(request_body)
    assert result["is_valid"] == result_is_valid
    assert result["errors"] == errors
