import pytest
from lib.utils import sufficient_to_autopopulate, history_of_diastolic_bp

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
                'sufficient_to_autopopulate': True,
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
                'sufficient_to_autopopulate': True,
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
                'sufficient_to_autopopulate': True,
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
                'sufficient_to_autopopulate': True,
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
                'sufficient_to_autopopulate': False,
                "success": True,
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
                'sufficient_to_autopopulate': False,
                "success": True,
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
                'sufficient_to_autopopulate': False,
                "success": True,
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
                'sufficient_to_autopopulate': False,
                "success": True,
            },
        ),
    ],
)
def test_sufficient_to_autopopulate(request_data, predominance_calculation):
    assert sufficient_to_autopopulate(request_data) == predominance_calculation

@pytest.mark.parametrize(
    "request_data, diastolic_bp_predominantly_100_or_more",
    [
        # 1 reading test case that passes
        (
            {
                "bp": [
                    {
                        "diastolic": 100,
                        "systolic": 180,
                        "date": "2021-11-01"
                    },
                ],
                "medication": [],
                'date_of_claim': '2021-11-09',
            },
            {
                "diastolic_bp_predominantly_100_or_more": True,
                "success": True 
            }
        ),
        # 1 reading test case that fails
        (
            {
                "bp": [
                    {
                        "diastolic": 90,
                        "systolic": 180,
                        "date": "2021-11-01"
                    },
                ],
                "medication": [],
                'date_of_claim': '2021-11-09',
            },
            {
                "diastolic_bp_predominantly_100_or_more": False,
                "success": True 
            }
        ),
        # 2 reading test case that passes
        (
            {
                "bp": [
                    {
                        "diastolic": 100,
                        "systolic": 180,
                        "date": "2021-11-01"
                    },
                    {
                        "diastolic": 90,
                        "systolic": 200,
                        "date": "2021-09-01"
                    }
                ],
                "medication": [],
                'date_of_claim': '2021-11-09',
            },
            {
                "diastolic_bp_predominantly_100_or_more": True,
                "success": True 
            }
        ),
        # 2 reading test case that fails
        (
            {
                "bp": [
                    {
                        "diastolic": 90,
                        "systolic": 180,
                        "date": "2021-11-01"
                    },
                    {
                        "diastolic": 90,
                        "systolic": 200,
                        "date": "2021-09-01"
                    }
                ],
                "medication": [],
                'date_of_claim': '2021-11-09',
            },
            {
                "diastolic_bp_predominantly_100_or_more": False,
                "success": True 
            }
        ),
        # 3 reading test case that passes
        (
            {
                "bp": [
                    {
                        "diastolic": 101,
                        "systolic": 180,
                        "date": "2021-11-01"
                    },
                    {
                        "diastolic": 90,
                        "systolic": 200,
                        "date": "2021-09-01"
                    },
                    {
                        "diastolic": 115,
                        "systolic": 200,
                        "date": "2021-09-02"
                    }
                ],
                "medication": [],
                'date_of_claim': '2021-11-09',
            },
            {
                "diastolic_bp_predominantly_100_or_more": True,
                "success": True 
            }
        ),
        # 3 reading test case that fails
        (
            {
                "bp": [
                    {
                        "diastolic": 101,
                        "systolic": 180,
                        "date": "2021-11-01"
                    },
                    {
                        "diastolic": 90,
                        "systolic": 200,
                        "date": "2021-09-01"
                    },
                    {
                        "diastolic": 95,
                        "systolic": 200,
                        "date": "2021-09-02"
                    }
                ],
                "medication": [],
                'date_of_claim': '2021-11-09',
            },
            {
                "diastolic_bp_predominantly_100_or_more": False,
                "success": True 
            }
        ),
    ],
)
def test_history_of_diastolic_bp(request_data, diastolic_bp_predominantly_100_or_more):
    assert history_of_diastolic_bp(request_data) == diastolic_bp_predominantly_100_or_more
