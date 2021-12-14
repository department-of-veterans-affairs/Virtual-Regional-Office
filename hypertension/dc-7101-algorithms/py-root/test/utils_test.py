from datetime import datetime

from test.data.htn_data import sufficient_to_autopopulate as data_sufficient_to_autopopulate
from lib.utils import sufficient_to_autopopulate

# TODO: Completely change/update/delete this test to make it better.
def test_sufficient_to_autopopulate():
    delete_or_replace_this_test_data_when_you_write_this_test_properly = [
        {
            "diastolic": 110,
            "systolic": 200,
            "date": "2021-11-01",
            "date_object": datetime.fromisoformat("2021-11-01")
        },
        {
            "diastolic": 110,
            "systolic": 200,
            "date": "2021-09-01",
            "date_object": datetime.fromisoformat("2021-09-01")
        }
    ]

    assert sufficient_to_autopopulate(data_sufficient_to_autopopulate["bp"]) == delete_or_replace_this_test_data_when_you_write_this_test_properly
