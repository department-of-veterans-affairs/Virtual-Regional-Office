from datetime import datetime
import operator

def tally_diastolic_counts(bp_readings):
    """
    Give a list of blood pressure readings, determine how many of each reading are included in each diastolic BP bucket

    :param bp_readings: list of blood pressure readings
    :type bp_readings: list
    :return: dict with keys which match the diastolic BP buckets and the number of readings in the list for each diastolic bucket type
    :rtype: dict
    """

    diastolic_bucket = {
        "130": 0,
        "120": 0,
        "110": 0,
        "100": 0,
        "less_than_100": 0
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
            key = "less_than_100"

        reading["diastolic_key"] = key
        diastolic_bucket[key] += 1

    return diastolic_bucket


def tally_systolic_counts(bp_readings):
    """
    Give a list of blood pressure readings, determine how many of each reading are included in each systolic BP bucket

    :param bp_readings: list of blood pressure readings
    :type bp_readings: list
    :return: dict with keys which match the systolic BP buckets and the number of readings in the list for each systolic bucket type
    :rtype: dict
    """

    systolic_bucket = {
        "200": 0,
        "160": 0,
        "less_than_160": 0
    }

    for reading in bp_readings:
        curr = reading["systolic"]

        key = None
        if curr >= 200:
            key = "200"
        elif curr >= 160:
            key = "160"
        else:
            key = "less_than_160"

        reading["systolic_key"] = key
        systolic_bucket[key] += 1

    return systolic_bucket


def calculate_reading_from_bucket(bucket, bp_readings, filter_for_diastolic):
    """
    Determine the predominant rating from a list of BP readings

    :param bucket: dict of blood pressure buckets and how many of each bucket type there are for the given blood pressure readings
    :type bucket: dict
    :param bp_readings: list of blood pressure readings
    :type bp_readings: list
    :param filter_for_diastolic: boolean indicating whether or not reading are diastolic
    :type filter_for_diastolic: boolean
    :return: most recent predominant BP reading
    :rtype: dict
    """

    largest_count = 0
    largest_count_bucket = None

    if filter_for_diastolic:
        type = 'diastolic'
    else:
        type = 'systolic'

    for key in bucket:
        curr_count = bucket[key]
        key_and_largest_count_are_ints = (
            largest_count_bucket != None
            and key != "less_than_100"
            and key != "less_than_160"
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
    """
    Determine from a list of BP readings if there exists two readings with a 1 month and 6 month date window 

    :param date_of_claim: string of date of claim
    :type date_of_claim: string
    :param bp_readings: list of blood pressure readings
    :type bp_readings: list
    :return: boolean indicating if readings within the two date windows are present
    :rtype: boolean
    """

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

hypertension_medications = {
    "benazepril",
    "lotensin",
    "captopril",
    "capoten",
    "enalapril",
    "enalaprilat",
    "fosinopril",
    "monopril",
    "lisinopril",
    "prinivil",
    "zestril",
}
