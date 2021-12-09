import pytest
from lib.bp_sufficiency import sufficient_to_autopopulate

@pytest.mark.parametrize(
    "request_data, predominance_calculation",
    [
        # 2 reading test case with no out of range dates
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
                "medication": [],
                'date_of_claim': '2021-11-09',
            },
            {
                "success": True,
                'predominant_diastolic_reading': 115,
                'predominant_systolic_reading': 180
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
                "medication": [],
                'date_of_claim': '2021-11-09',
            },
            {
                "success": True,
                'predominant_diastolic_reading': 115,
                'predominant_systolic_reading': 180
            },
        ),
        # +2 reading test case with no out of range dates
        # this also validates that given an equal number of two categories
        # the algorithm chooses the higher rating for both categories
        (
            {
                "bp": [
                    {
                        'systolic': 181,
                        'diastolic': 109,
                        'date': '2021-10-10'
                    },
                    {
                        'systolic': 131,
                        'diastolic': 113,
                        'date': '2021-05-13'
                    },
                    {
                        'systolic': 160,
                        'diastolic': 101,
                        'date': '2021-09-13'
                    },
                    {
                        'systolic': 120,
                        'diastolic': 104,
                        'date': '2021-09-13'
                    },
                    {
                        'systolic': 180,
                        'diastolic': 116,
                        'date': '2021-10-13'
                    },
                    {
                        'systolic': 155,
                        'diastolic': 111,
                        'date': '2021-10-14'
                    }
                ],
                "medication": [],
                'date_of_claim': '2021-11-09',
            },
            {
                "success": True,
                'predominant_diastolic_reading': 111,
                'predominant_systolic_reading': 180
            },
        ),
        # +2 reading test case with 1 out of range date (which would change the results if included)
        (
            {
                "bp": [
                    {
                        'systolic': 181,
                        'diastolic': 109,
                        'date': '2021-10-10'
                    },
                    {
                        'systolic': 131,
                        'diastolic': 113,
                        'date': '2021-05-13'
                    },
                    {
                        'systolic': 160,
                        'diastolic': 101,
                        'date': '2021-09-13'
                    },
                    {
                        'systolic': 120,
                        'diastolic': 104,
                        'date': '2021-09-13'
                    },
                    {
                        'systolic': 180,
                        'diastolic': 116,
                        'date': '2021-10-13'
                    },
                    {
                        'systolic': 155,
                        'diastolic': 111,
                        'date': '2021-10-14'
                    },
                    {
                        'systolic': 154,
                        'diastolic': 105,
                        'date': '2020-11-08'
                    }
                ],
                "medication": [],
                'date_of_claim': '2021-11-09',
            },
            {
                "success": True,
                'predominant_diastolic_reading': 111,
                'predominant_systolic_reading': 180
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
                "medication": [],
                'date_of_claim': '2021-11-09',
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
                "medication": [],
                'date_of_claim': '2021-11-09',
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
                "medication": [],
                'date_of_claim': '2021-11-09',
            },
            {
                "success": False,
            },
        ),
        # 0 readings
        (
            {
                "bp": [
                ],
                "medication": [],
                'date_of_claim': '2021-11-09',
            },
            {
                "success": False,
            }
        ),
    ],
)
def test_sufficient_to_autopopulate(request_data, predominance_calculation):
    assert sufficient_to_autopopulate(request_data) == predominance_calculation

