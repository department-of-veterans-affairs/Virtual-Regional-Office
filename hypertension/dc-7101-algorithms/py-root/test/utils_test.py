from test.data.htn_data import general_request_data
from lib.utils import sufficient_to_autopopulate, history_of_diastolic_bp

# TODO: Completely change/update/delete this test to make it better.
def test_sufficient_to_autopopulate():
    predominance_calculation = {
        'sufficient_to_autopopulate': True,
        "success": True,
        'predominant_diastolic_reading': 115,
        'predominant_systolic_reading': 180
    }

    assert sufficient_to_autopopulate(general_request_data) == predominance_calculation

def test_history_of_diastolic_bp():
    history_sufficiency_data = {
        "diastolic_bp_predominantly_100_or_more": True,
        "success": True 
    }

    assert history_of_diastolic_bp(general_request_data) == history_sufficiency_data
