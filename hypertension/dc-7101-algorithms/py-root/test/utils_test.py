import pytest
from lib.algorithms.utils import bp_readings_meet_date_specs

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