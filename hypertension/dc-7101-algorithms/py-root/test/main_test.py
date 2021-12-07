from lib.main import main
from test.data.htn_data import general_request_data

def test_main():
    assert main(general_request_data) == {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST"
        },
        "body": {
            "predominance_calculation": {
                'sufficient_to_autopopulate': True,
                "success": True,
                'predominant_diastolic_reading': 115,
                'predominant_systolic_reading': 180
            },
            "diastolic_history_calculation": {
                "diastolic_bp_predominantly_100_or_more": True,
                "success": True 
            }
        }
    }

