import pytest
from lib.algorithms.utils import bp_readings_meet_date_specs, tally_diastolic_counts, tally_systolic_counts

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
                "less_than_one_hundred": 1
            }
        ),
    ],
)
def test_tally_diastolic_counts(bp_readings, result):
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
                "less_than_one_sixty": 2
            }
        ),
    ],
)
def test_tally_systolic_counts(bp_readings, result):
    assert tally_systolic_counts(bp_readings) == result

@pytest.mark.parametrize(
    "date_of_claim, bp_readings, result",
    [
        # Valid reading
        (
            '2021-11-09',
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
            '2021-11-09',
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
            '2021-11-09',
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
            '2021-11-09',
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
            '2021-11-09',
            [],
            False
        )
    ],
)
def test_bp_readings_meet_date_specs(date_of_claim, bp_readings, result):
    assert bp_readings_meet_date_specs(date_of_claim, bp_readings) == result