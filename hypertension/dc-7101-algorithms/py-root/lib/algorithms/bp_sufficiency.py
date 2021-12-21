from datetime import datetime
from dateutil.relativedelta import relativedelta

from .utils import (
    tally_diastolic_counts,
    tally_systolic_counts,
    calculate_reading_from_buckets,
    bp_readings_meet_date_specs
)

def sufficient_to_autopopulate (request_body):
    """
    Determine if there is enough BP data to calculate a predominant reading,
    and if so return the predominant rating

    :param request_body: request body
    :type request_body: dict
    :return: response body indicating success or failure with additional attributes
    :rtype: dict
    """

    predominance_calculation = {
        "success": True,
    }
    date_of_claim = request_body["date_of_claim"]
    valid_bp_readings = []
    date_of_claim_date = datetime.strptime(date_of_claim, "%Y-%m-%d").date()

    for reading in request_body["bp"]:
        bp_reading_date = datetime.strptime(reading["date"], "%Y-%m-%d").date()
        if bp_reading_date >= date_of_claim_date - relativedelta(years=1):
            valid_bp_readings.append(reading)

    if len(valid_bp_readings) <= 1 or not bp_readings_meet_date_specs(date_of_claim, valid_bp_readings):
        predominance_calculation["success"] = False
        return predominance_calculation

    elif len(valid_bp_readings) > 1 and bp_readings_meet_date_specs(date_of_claim, valid_bp_readings):

        if len(valid_bp_readings) == 2:
            most_recent_reading = sorted(valid_bp_readings, key=lambda d: d["date"])[-1]
            predominance_calculation["predominant_diastolic_reading"] = most_recent_reading["diastolic"]
            predominance_calculation["predominant_systolic_reading"] = most_recent_reading["systolic"]
        elif len(valid_bp_readings) > 2:
            bucketed_diastolic_readings = tally_diastolic_counts(valid_bp_readings)
            predominance_calculation["predominant_diastolic_reading"] = calculate_reading_from_buckets(bucketed_diastolic_readings, valid_bp_readings, True)
            bucketed_systolic_readings = tally_systolic_counts(valid_bp_readings)
            predominance_calculation["predominant_systolic_reading"] = calculate_reading_from_buckets(bucketed_systolic_readings, valid_bp_readings, False)

    return predominance_calculation
