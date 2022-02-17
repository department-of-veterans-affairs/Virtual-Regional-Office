import pytest
from lib.algorithms.utils import (
    bp_readings_meet_date_specs, 
    tally_diastolic_counts, 
    tally_systolic_counts, 
    calculate_reading_from_buckets, 
    validate_request_body
)

@pytest.mark.parametrize(
    "bp_readings, result",
    [
        (
            [
                {
                    "diastolic": 115,
                    "systolic": 180,
                    "date": "2021-10-10"
                },
                {
                    "diastolic": 110,
                    "systolic": 200,
                    "date": "2021-09-01"
                },
                {
                    "diastolic": 105,
                    "systolic": 180,
                    "date": "2021-10-10"
                },
                {
                    "diastolic": 121,
                    "systolic": 200,
                    "date": "2021-09-01"
                },
                {
                    "diastolic": 91,
                    "systolic": 200,
                    "date": "2021-09-01"
                },
                {
                    "diastolic": 135,
                    "systolic": 200,
                    "date": "2021-09-01"
                }
            ],
            {
                "130": 1,
                "120": 1,
                "110": 2,
                "100": 1,
                "less_than_100": 1
            }
        ),
    ],
)
def test_tally_diastolic_counts(bp_readings, result):
    """
    Test counting the number of diastolic readings for each blood pressure "bucket"

    :param bp_readings: list of blood pressure readings
    :type bp_readings: list
    :param result: dict of blood pressure buckets with the number of counts of each bucket
    :type result: dict
    """
    assert tally_diastolic_counts(bp_readings) == result

@pytest.mark.parametrize(
    "bp_readings, result",
    [
        (
            [
                {
                    "diastolic": 115,
                    "systolic": 150,
                    "date": "2021-10-10"
                },
                {
                    "diastolic": 110,
                    "systolic": 159,
                    "date": "2021-09-01"
                },
                {
                    "diastolic": 105,
                    "systolic": 160,
                    "date": "2021-10-10"
                },
                {
                    "diastolic": 121,
                    "systolic": 170,
                    "date": "2021-09-01"
                },
                {
                    "diastolic": 91,
                    "systolic": 201,
                    "date": "2021-09-01"
                },
                {
                    "diastolic": 135,
                    "systolic": 200,
                    "date": "2021-09-01"
                }
            ],
            {
                "200": 2,
                "160": 2,
                "less_than_160": 2
            }
        ),
    ],
)
def test_tally_systolic_counts(bp_readings, result):
    """
    Test counting the number of systolic readings for each blood pressure "bucket"

    :param bp_readings: list of blood pressure readings
    :type bp_readings: list
    :param result: dict of blood pressure buckets with the number of counts of each bucket
    :type result: dict
    """
    assert tally_systolic_counts(bp_readings) == result

@pytest.mark.parametrize(
    "bucket, bp_readings, filter_for_diastolic, result",
    [
        # Test diastolic readings
        (
            {
                "130": 2,
                "120": 1,
                "110": 2,
                "100": 1,
                "less_than_100": 2
            },
            [
                {
                    "diastolic": 115,
                    "systolic": 180,
                    "date": "2021-10-10",
                    "diastolic_key": "110"
                },
                {
                    "diastolic": 110,
                    "systolic": 200,
                    "date": "2021-09-01",
                    "diastolic_key": "110"
                },
                {
                    "diastolic": 105,
                    "systolic": 180,
                    "date": "2021-10-10",
                    "diastolic_key": "100"
                },
                {
                    "diastolic": 121,
                    "systolic": 200,
                    "date": "2021-09-01",
                    "diastolic_key": "120"
                },
                {
                    "diastolic": 91,
                    "systolic": 200,
                    "date": "2021-09-01",
                    "diastolic_key": "less_than_100"
                },
                {
                    "diastolic": 95,
                    "systolic": 180,
                    "date": "2021-10-01",
                    "diastolic_key": "less_than_100"
                },
                {
                    "diastolic": 135,
                    "systolic": 190,
                    "date": "2021-09-01",
                    "diastolic_key": "130"
                },
                {
                    "diastolic": 140,
                    "systolic": 200,
                    "date": "2021-09-05",
                    "diastolic_key": "130"
                }
            ],
            True,
            140
        ),
        # Test systolic readings
        (
            {
                "200": 2,
                "160": 2,
                "less_than_160": 2
            },
            [
                {
                    "diastolic": 115,
                    "systolic": 180,
                    "date": "2021-10-10",
                    "systolic_key": "160"
                },
                {
                    "diastolic": 110,
                    "systolic": 210,
                    "date": "2021-09-01",
                    "systolic_key": "200"
                },
                {
                    "diastolic": 105,
                    "systolic": 180,
                    "date": "2021-10-10",
                    "systolic_key": "160"
                },
                {
                    "diastolic": 121,
                    "systolic": 200,
                    "date": "2021-09-02",
                    "systolic_key": "200"
                },
                {
                    "diastolic": 91,
                    "systolic": 150,
                    "date": "2021-09-01",
                    "systolic_key": "less_than_160"
                },
                {
                    "diastolic": 95,
                    "systolic": 155,
                    "date": "2021-10-01",
                    "systolic_key": "less_than_160"
                },
            ],
            False,
            200
        ),
    ],
)
def test_calculate_reading_from_buckets(bucket, bp_readings, filter_for_diastolic, result):
    """
    Test calculating the predominant blood pressure reading from a list of bp readings and a bucket count

    :param bucket: dict of blood pressure buckets with the number of counts of each bucket
    :type bucket: dict
    :param bp_readings: list of blood pressure readings
    :type bp_readings: list
    :param filter_for_diastolic: boolean indicating if we are looking for diastolic or systolic
    :type filter_for_diastolic: boolean
    :param result: int value showing the predominant rating
    :type result: int
    """
    assert calculate_reading_from_buckets(bucket, bp_readings, filter_for_diastolic) == result

@pytest.mark.parametrize(
    "date_of_claim, bp_readings, result",
    [
        # Valid reading
        (
            "2021-11-09",
            [
                {
                    "diastolic": 115,
                    "systolic": 180,
                    "date": "2021-10-10"
                },
                {
                    "diastolic": 110,
                    "systolic": 200,
                    "date": "2021-09-01"
                }
            ],
            True
        ),
        # Reading within 30 days, no reading within 180 days (181 days)
        (
            "2021-11-09",
            [
                {
                    "diastolic": 115,
                    "systolic": 180,
                    "date": "2021-10-10"
                },
                {
                    "diastolic": 110,
                    "systolic": 200,
                    "date": "2021-05-12"
                }
            ],
            False
        ),
        # Reading within 180 days, no reading within 30 days (reading has 31 days)
        (
            "2021-11-09",
            [
                {
                    "diastolic": 115,
                    "systolic": 180,
                    "date": "2021-10-09"
                },
                {
                    "diastolic": 110,
                    "systolic": 200,
                    "date": "2021-09-01"
                }
            ],
            False
        ),
        # 1 reading
        (
            "2021-11-09",
            [
                {
                    "diastolic": 115,
                    "systolic": 180,
                    "date": "2021-10-10"
                }
            ],
            False
        ),
        # 0 readings
        (
            "2021-11-09",
            [],
            False
        )
    ],
)
def test_bp_readings_meet_date_specs(date_of_claim, bp_readings, result):
    """
    Test function that determines if the blood pressure readings contain a readings that are within 1 month and 6 months of the date of claim

    :param date_of_claim: string representation of the date of claim
    :type date_of_claim: string
    :param bp_readings: list of blood pressure readings
    :type bp_readings: list
    :param result: boolean describing whether or not the blood pressure readings meet the specifications
    :type result: bool
    """
    assert bp_readings_meet_date_specs(date_of_claim, bp_readings) == result

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
                        "diastolic": 115,
                        "systolic": "180",
                        "date": "2021-11-01"
                    },
                    {
                        "diastolic": 110,
                        "systolic": 200,
                        "date": "2021-09-01"
                    }
                ],
                "medication": [1],
                "date_of_claim": "2021-11-09",
                "veteran_is_service_connected_for_dc7101": "True"
            },
            False,
            {"bp": [
                {0: [{"systolic": ["must be of integer type"]}]}
                ],
                "medication": [{0: ["must be of string type"]}],
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