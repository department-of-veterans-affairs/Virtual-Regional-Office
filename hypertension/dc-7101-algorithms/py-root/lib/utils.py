from datetime import datetime
from dateutil.relativedelta import relativedelta
import operator

def tally_diastolic_counts(bp_readings):
    diastolic_bucket_count = {
        "130": 0,
        "120": 0,
        "110": 0,
        "100": 0,
        "less_than_one_hundred": 0
    }

    for reading in bp_readings:
        curr = reading["diastolic"]

        key = None
        if curr >= 130:
            key = "130"
        elif curr >= 120 and curr < 130:
            key = "120"
        elif curr >= 110 and curr < 120:
            key = "110"
        elif curr >= 100 and curr < 110:
            key = "100"
        else:
            key = "less_than_one_hundred"

        reading["diastolic_key"] = key
        diastolic_bucket_count[key] += 1

    return diastolic_bucket_count


def tally_systolic_counts(bp_readings):
    systolic_bucket_count = {
        "200": 0,
        "160": 0,
        "less_than_one_sixty": 0
    }

    for reading in bp_readings:
        curr = reading["systolic"]

        key = None
        if curr >= 200:
            key = "200"
        elif curr >= 160:
            key = "160"
        else:
            key = "less_than_one_sixty"

        reading["systolic_key"] = key
        systolic_bucket_count[key] += 1

    return systolic_bucket_count


def calculate_reading_from_bucket_count(bucket_count, bp_readings, type):
    largest_count = 0
    largest_count_bucket = None

    for key in bucket_count:
        curr_count = bucket_count[key]
        key_and_largest_count_are_ints = (
            largest_count_bucket != None
            and key != "less_than_one_hundred"
            and key != "less_than_one_sixty"
            )

        if curr_count > largest_count:
            largest_count = curr_count
            largest_count_bucket = key
        if (
            curr_count == largest_count
            and key_and_largest_count_are_ints
            and int(key) > int(largest_count_bucket)
        ):
            largest_count_bucket = key

    bucketed_bp_readings = list(filter(lambda d: d[f"{type}_key"] == largest_count_bucket, bp_readings))
    bucketed_bp_readings.sort(key=operator.itemgetter("date"))
    most_recent_reading_of_selected_type = bucketed_bp_readings[-1][type]

    return most_recent_reading_of_selected_type

def bp_readings_meet_date_specs(date_of_claim, bp_readings):
    claim_within_six_months = False
    claim_within_one_month = False
    date_of_claim_date = datetime.strptime(date_of_claim, "%Y-%m-%d").date()

    for reading in bp_readings:
        bp_reading_date = datetime.strptime(reading["date"], "%Y-%m-%d").date()
        within_thirty_days = (date_of_claim_date - bp_reading_date).days <= 30

        if (within_thirty_days and not claim_within_one_month):
            claim_within_one_month = True
        elif (within_thirty_days and claim_within_one_month):
            claim_within_six_months = True
        elif ((date_of_claim_date - bp_reading_date).days <= 180 and not claim_within_six_months):
            claim_within_six_months = True

    return claim_within_one_month and claim_within_six_months


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
