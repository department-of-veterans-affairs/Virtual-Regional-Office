import pytest
from lib.algorithms.bp_history import history_of_diastolic_bp

@pytest.mark.parametrize(
    "request_data, diastolic_bp_predominantly_100_or_more",
    [
        # 0 readings
        (
            {
                "bp": [
                ],
                "medication": [],
                'date_of_claim': '2021-11-09',
            },
            {
                "success": False
            }
        ),
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
