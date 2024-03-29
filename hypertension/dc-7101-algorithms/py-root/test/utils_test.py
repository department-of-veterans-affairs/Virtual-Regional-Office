import pytest
from lib.algorithms.utils import validate_request_body


@pytest.mark.parametrize(
    "request_body, result_is_valid, errors",
    [
        (
            {
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
                "veteran_is_service_connected_for_dc7101": True
            },
            True,
            {}
        ),
        (
            {
                "bp": [
                    {
                        "systolic": "180",
                        "date": "2021-11-01"
                    },
                    {
                        "diastolic": "110",
                        "systolic": 200,
                        "date": 20210901
                    }
                ],
                "medication": [123],
                "date_of_claim": 20211109,
                "veteran_is_service_connected_for_dc7101": "True"
            },
            False,
            {
                "bp": [
                    {
                        0: [
                            {
                                "systolic": ["must be of integer type"],
                                "diastolic": ["required field"]
                            }
                        ],
                        1: [
                            {
                                "date": ["must be of string type"],
                                "diastolic": ["must be of integer type"]
                            }
                        ]
                    }
                ],
                "medication": [
                    {
                        0: ["must be of string type"]
                    }
                ],
                "date_of_claim": ["must be of string type"],
                "veteran_is_service_connected_for_dc7101": ["must be of boolean type"]
            }
        ),
    ],
)
def test_validate_request_body(request_body, result_is_valid, errors):
    """
    Test function that determines if the blood pressure readings contain a readings that are within 1 month and 6 months of the date of claim

    :param date_of_claim: string representation of the date of claim
    :type date_of_claim: string
    :param bp_readings: list of blood pressure readings
    :type bp_readings: list
    :param result: boolean describing whether or not the blood pressure readings meet the specifications
    :type result: bool
    """
    result = validate_request_body(request_body)
    assert result["is_valid"] == result_is_valid
    assert result["errors"] == errors
