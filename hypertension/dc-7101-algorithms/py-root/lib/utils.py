from datetime import datetime
from dateutil.relativedelta import relativedelta
import operator

def calculate_correct_bp_reading(bp_readings, use_diastolic):
    # Break this into two functions that share another helper?
    diastolic_bucket_count = {
        "130": 0,
        "120": 0,
        "110": 0,
        "100": 0,
        "less_than_one_hundred": 0
    }

    systolic_bucket_count = {
        "200": 0,
        "160": 0,
        "less_than_one_sixty": 0
    }

    if use_diastolic:
        type = "diastolic"
        bucket_count = diastolic_bucket_count
    else:
        type = "systolic"
        bucket_count = systolic_bucket_count

    for reading in bp_readings:
        curr = reading[type]

        key = None
        if use_diastolic:
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
        else:
            if curr >= 200:
                key = "200"
            elif curr >= 160:
                key = "160"
            else:
                key = "less_than_one_sixty"

        reading[f"{type}_key"] = key
        bucket_count[key] += 1

    largest_count = 0
    largest_count_bucket = None

    for key in bucket_count:
        curr_count = bucket_count[key]
        if curr_count > largest_count:
            largest_count = curr_count
            largest_count_bucket = key
        if (
            curr_count == largest_count
            and largest_count_bucket != None
            and key != "less_than_one_hundred"
            and key != "less_than_one_sixty"
            and int(key) > int(largest_count_bucket)
        ):
            largest_count_bucket = key

    bucketed_bp_readings = list(filter(lambda d: d[f"{type}_key"] == largest_count_bucket, bp_readings))
    bucketed_bp_readings.sort(key=operator.itemgetter("date"))

    return bucketed_bp_readings[-1][type]

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

    # where to add this? When there’s an internal server error, the algorithm CANNOT “run”.

def history_of_diastolic_bp(request):
    diastolic_history_calculation = {
        "success": True
    }
    bp_readings = request["bp"]
    bp_readings_length = len(bp_readings)
    readings_greater_or_equal_to_one_hundred = 0
    
    if bp_readings_length > 0:
        for reading in bp_readings:
            if reading["diastolic"] >= 100:
                readings_greater_or_equal_to_one_hundred += 1
        diastolic_history_calculation["diastolic_bp_predominantly_100_or_more"] = True if readings_greater_or_equal_to_one_hundred / bp_readings_length >=.5 else False
    else:
        diastolic_history_calculation["sufficient_to_autopopulate"] = False

    return diastolic_history_calculation

def sufficient_to_autopopulate (request):
    predominance_calculation = {
        "sufficient_to_autopopulate": False,
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
        # should this include the same day a year ago?
        if bp_reading_date >= date_of_claim_date - relativedelta(years=1):
            filter_bp_readings.append(reading)

    if bp_readings_meet_date_specs(date_of_claim, filter_bp_readings) and len(filter_bp_readings) > 1:
        predominance_calculation["sufficient_to_autopopulate"] = True

        if len(filter_bp_readings) == 2:
            most_recent_reading = sorted(filter_bp_readings, key=lambda d: d["date"])[-1]
            predominance_calculation["predominant_diastolic_reading"] = most_recent_reading["diastolic"]
            predominance_calculation["predominant_systolic_reading"] = most_recent_reading["systolic"]
        elif len(filter_bp_readings) > 2:
            predominance_calculation["predominant_diastolic_reading"] = calculate_correct_bp_reading(filter_bp_readings, True)
            predominance_calculation["predominant_systolic_reading"] = calculate_correct_bp_reading(filter_bp_readings, False)

    return predominance_calculation
