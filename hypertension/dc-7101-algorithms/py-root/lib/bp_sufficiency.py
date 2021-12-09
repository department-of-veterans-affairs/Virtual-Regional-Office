from datetime import datetime
from dateutil.relativedelta import relativedelta

from .utils import tally_diastolic_counts, tally_systolic_counts, calculate_reading_from_bucket_count, bp_readings_meet_date_specs

def sufficient_to_autopopulate (request):
    predominance_calculation = {
        "success": True,
    }
    date_of_claim = request["date_of_claim"]
    filter_bp_readings = []
    date_of_claim_date = datetime.strptime(date_of_claim, "%Y-%m-%d").date()

    if len(request["bp"]) < 1:
        predominance_calculation["success"] = False
        return predominance_calculation

    for reading in request["bp"]:
        bp_reading_date = datetime.strptime(reading["date"], "%Y-%m-%d").date()
        if bp_reading_date >= date_of_claim_date - relativedelta(years=1):
            filter_bp_readings.append(reading)

    if len(filter_bp_readings) <= 1 or not bp_readings_meet_date_specs(date_of_claim, filter_bp_readings):
        predominance_calculation["success"] = False
        return predominance_calculation

    elif len(filter_bp_readings) > 1 and bp_readings_meet_date_specs(date_of_claim, filter_bp_readings):

        if len(filter_bp_readings) == 2:
            most_recent_reading = sorted(filter_bp_readings, key=lambda d: d["date"])[-1]
            predominance_calculation["predominant_diastolic_reading"] = most_recent_reading["diastolic"]
            predominance_calculation["predominant_systolic_reading"] = most_recent_reading["systolic"]
        elif len(filter_bp_readings) > 2:
            diastolic_bucket_count = tally_diastolic_counts(filter_bp_readings)
            predominance_calculation["predominant_diastolic_reading"] = calculate_reading_from_bucket_count(diastolic_bucket_count, filter_bp_readings, 'diastolic')
            systolic_bucket_count = tally_systolic_counts(filter_bp_readings)
            predominance_calculation["predominant_systolic_reading"] = calculate_reading_from_bucket_count(systolic_bucket_count, filter_bp_readings, 'systolic')

    return predominance_calculation
