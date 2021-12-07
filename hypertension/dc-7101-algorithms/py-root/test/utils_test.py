from test.data.htn_data import sufficient_to_autopopulate as data_sufficient_to_autopopulate
from test.data.htn_data import data_to_affirm_history
from lib.utils import sufficient_to_autopopulate, history_of_diastolic_bp

# TODO: Completely change/update/delete this test to make it better.
def test_sufficient_to_autopopulate():
    bp_sufficiency_data = {
        'sufficient_to_autopopulate': True,
        "success": True,
        'predominant_diastolic_reading': 115,
        'predominant_systolic_reading': 180
    }

    assert sufficient_to_autopopulate(data_sufficient_to_autopopulate) == bp_sufficiency_data

def test_history_of_diastolic_bp():
    history_sufficiency_data = {
        "diastolic_bp_predominantly_100_or_more": True,
        "success": True 
    }

    assert history_of_diastolic_bp(data_to_affirm_history) == history_sufficiency_data
