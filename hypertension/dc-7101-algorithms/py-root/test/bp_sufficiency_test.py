import pytest
from lib.algorithms.predominant_bp import sufficient_to_autopopulate, bp_readings_meet_date_specs, calculate_predominant_readings

@pytest.mark.parametrize(
    "date_of_claim, bp_readings, result",
    [
        # Date requirements met (1x within 30 days + 1x within 180 days).
        # This also tests the edge cases in that 10/10 is exactly 30 days before 11/9
        # and 5/13 is exactly 180 days before 11/9
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
                    "date": "2021-05-13"
                }
            ],
            True
        ),
        # Yes reading within 30 days, but no reading within 180 days.
        # This also tests the edge case in that 5/12 is *181* days before 11/9
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
        # Yes reading within 180 days, but no reading within 30 days
        # This also tests the edge case in that 10/9 is *31* days before 11/9
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
        # Date specs not met because 1 reading is insufficient data.
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
        # Date specs not met because 0 readings is insufficient data.
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
    "bp_readings, result",
    [
        (
            [
                {
                    "diastolic": 115,
                    "systolic": 180,
                    "date": "2021-10-10",
                },
                {
                    "diastolic": 110,
                    "systolic": 210,
                    "date": "2021-09-01",
                },
                {
                    "diastolic": 105,
                    "systolic": 180,
                    "date": "2021-10-10",
                },
                {
                    "diastolic": 121,
                    "systolic": 200,
                    "date": "2021-09-01",
                },
                {
                    "diastolic": 91,
                    "systolic": 200,
                    "date": "2021-09-01",
                },
                {
                    "diastolic": 95,
                    "systolic": 180,
                    "date": "2021-10-01",
                },
                # Per the algorithm, when the total number of BP readings is 3 or greater, if there
                # are multiple values within the Predominant Percent Range of Diastolic Readings
                # (PPRDR) (see algorithm document for definition) then *most recent* reading in the
                # PPRDR is the predominant reading (i.e. not neccessarily the *highest* reading
                # reading within the PPRDR).
                # The following two readings are ordered specifically this way in this Python list
                # to exercise and test the date sorting portion of the algorithm.
                {
                    "diastolic": 135,
                    "systolic": 155,
                    "date": "2021-09-05",
                },
                {
                    "diastolic": 140,
                    "systolic": 150,
                    "date": "2021-09-01",
                },
            ],
            {
                "diastolic_value": 135,
                "systolic_value": 200
            }
        )
    ],
)
def test_calculate_predominant_readings(bp_readings, result):
    """
    Test calculating the predominant blood pressure reading from a list of bp readings

    :param bp_readings: list of blood pressure readings
    :type bp_readings: list
    :param result: int value showing the predominant rating
    :type result: int
    """
    assert calculate_predominant_readings(bp_readings) == result


@pytest.mark.parametrize(
    "request_body, predominance_calculation",
    [
        # Two readings. No out of range dates.
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
                "date_of_claim": "2021-11-09",
            },
            {
                "success": True,
                "predominant_diastolic_reading": 115,
                "predominant_systolic_reading": 200
            },
        ),
        # 2 reading test case with one out of range date
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
                    },
                    {
                        "diastolic": 120,
                        "systolic": 210,
                        "date": "2020-11-08"
                    }
                ],
                "date_of_claim": "2021-11-09",
            },
            {
                "success": True,
                "predominant_diastolic_reading": 115,
                "predominant_systolic_reading": 200
            },
        ),
        # +2 reading test case with no out of range dates
        # Total number of readings is odd
        (
            {
                "bp": [
                    {
                        "systolic": 181,
                        "diastolic": 112,
                        "date": "2021-10-09"
                    },
                    {
                        "systolic": 181,
                        "diastolic": 109,
                        "date": "2021-10-10"
                    },
                    {
                        "systolic": 131,
                        "diastolic": 113,
                        "date": "2021-05-13"
                    },
                    {
                        "systolic": 160,
                        "diastolic": 101,
                        "date": "2021-09-13"
                    },
                    {
                        "systolic": 120,
                        "diastolic": 104,
                        "date": "2021-09-13"
                    },
                    {
                        "systolic": 180,
                        "diastolic": 116,
                        "date": "2021-10-13"
                    },
                    {
                        "systolic": 155,
                        "diastolic": 111,
                        "date": "2021-10-14"
                    },
                ],
                "date_of_claim": "2021-11-09",
            },
            {
                "success": True,
                "predominant_diastolic_reading": 111,
                "predominant_systolic_reading": 180
            },
        ),
        # +2 reading test case with no out of range dates
        # This also validates that given an equal number of two categories
        # the algorithm chooses the higher rating for both categories
        (
            {
                "bp": [
                    {
                        "systolic": 181,
                        "diastolic": 109,
                        "date": "2021-10-10"
                    },
                    {
                        "systolic": 131,
                        "diastolic": 113,
                        "date": "2021-05-13"
                    },
                    {
                        "systolic": 160,
                        "diastolic": 101,
                        "date": "2021-09-13"
                    },
                    {
                        "systolic": 120,
                        "diastolic": 104,
                        "date": "2021-09-13"
                    },
                    {
                        "systolic": 180,
                        "diastolic": 116,
                        "date": "2021-10-13"
                    },
                    {
                        "systolic": 155,
                        "diastolic": 111,
                        "date": "2021-10-14"
                    }
                ],
                "date_of_claim": "2021-11-09",
            },
            {
                "success": True,
                "predominant_diastolic_reading": 111,
                "predominant_systolic_reading": 180
            },
        ),
        # +2 reading test case with 1 out of range date (which would change the results if included)
        (
            {
                "bp": [
                    {
                        "systolic": 181,
                        "diastolic": 109,
                        "date": "2021-10-10"
                    },
                    {
                        "systolic": 131,
                        "diastolic": 113,
                        "date": "2021-05-13"
                    },
                    {
                        "systolic": 160,
                        "diastolic": 101,
                        "date": "2021-09-13"
                    },
                    {
                        "systolic": 120,
                        "diastolic": 104,
                        "date": "2021-09-13"
                    },
                    {
                        "systolic": 180,
                        "diastolic": 116,
                        "date": "2021-10-13"
                    },
                    {
                        "systolic": 155,
                        "diastolic": 111,
                        "date": "2021-10-14"
                    },
                    {
                        "systolic": 154,
                        "diastolic": 105,
                        "date": "2020-11-08"
                    }
                ],
                "date_of_claim": "2021-11-09",
            },
            {
                "success": True,
                "predominant_diastolic_reading": 111,
                "predominant_systolic_reading": 180
            },
        ),
        # 2 readings, but no reading within 30 days
        (
            {
                "bp": [
                    {
                        "diastolic": 115,
                        "systolic": 180,
                        "date": "2021-10-01"
                    },
                    {
                        "diastolic": 110,
                        "systolic": 200,
                        "date": "2021-09-01"
                    }
                ],
                "date_of_claim": "2021-11-09",
            },
            {
                "success": False,
            },
        ),
        # 2 readings, but no second reading within 180 days
        (
            {
                "bp": [
                    {
                        "diastolic": 115,
                        "systolic": 180,
                        "date": "2021-04-01"
                    },
                    {
                        "diastolic": 110,
                        "systolic": 200,
                        "date": "2021-10-10"
                    }
                ],
                "date_of_claim": "2021-11-09",
            },
            {
                "success": False,
            },
        ),
        # 1 reading
        (
            {
                "bp": [
                    {
                        "diastolic": 110,
                        "systolic": 200,
                        "date": "2021-10-10"
                    }
                ],
                "date_of_claim": "2021-11-09",
            },
            {
                "success": False,
            },
        ),
        # 0 readings
        (
            {
                "bp": [],
                "date_of_claim": "2021-11-09",
            },
            {
                "success": False,
            }
        ),
    ],
)
def test_sufficient_to_autopopulate(request_body, predominance_calculation):
    """
    Test the history of blood pressure sufficiency algorithm

    :param request_body: request body with blood pressure readings and other data
    :type request_body: dict
    :param predominance_calculation: correct return value from algorithm
    :type predominance_calculation: dict
    """
    assert sufficient_to_autopopulate(request_body) == predominance_calculation

