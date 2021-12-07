from typing import Dict
from .utils import sufficient_to_autopopulate, history_of_diastolic_bp

def main(event: Dict):
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST"
        },
        "body": {
            "predominance_calculation": sufficient_to_autopopulate(event),
            "diastolic_history_calculation": history_of_diastolic_bp(event)
        }
    }
