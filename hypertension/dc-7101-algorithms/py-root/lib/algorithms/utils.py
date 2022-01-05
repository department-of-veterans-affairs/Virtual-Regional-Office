from datetime import datetime
import operator
from cerberus import Validator

def tally_diastolic_counts(bp_readings):
    """
    Give a list of blood pressure readings, determine how many of each reading are included in each of the diastolic BP buckets created by the 38 CFR 4.104 DC 7101 rating percentages.

    :param bp_readings: list of blood pressure readings
    :type bp_readings: list
    :return: dict with keys which match the diastolic BP buckets and the number of readings in the list for each diastolic bucket type
    :rtype: dict
    """

    diastolic_buckets = {
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
        diastolic_buckets[key] += 1

    return diastolic_buckets


def tally_systolic_counts(bp_readings):
    """
    Give a list of blood pressure readings, determine how many of each reading are included in each of the systolic BP buckets created by the 38 CFR 4.104 DC 7101 rating percentages.

    :param bp_readings: list of blood pressure readings
    :type bp_readings: list
    :return: dict with keys which match the systolic BP buckets and the number of readings in the list for each systolic bucket type
    :rtype: dict
    """

    systolic_buckets = {
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
        systolic_buckets[key] += 1

    return systolic_buckets


def calculate_reading_from_buckets(buckets, bp_readings, filter_for_diastolic):
    """
    Determine the predominant rating from a list of BP readings

    :param buckets: dict of blood pressure buckets and how many of each bucket type there are for the given blood pressure readings
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
        type = "diastolic"
    else:
        type = "systolic"

    for key in buckets:
        curr_count = buckets[key]
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

    reading_within_one_month = False
    reading_within_six_months = False
    date_of_claim_date = datetime.strptime(date_of_claim, "%Y-%m-%d").date()

    for reading in bp_readings:
        bp_reading_date = datetime.strptime(reading["date"], "%Y-%m-%d").date()
        one_month_difference = (date_of_claim_date - bp_reading_date).days <= 30
        six_month_difference = (date_of_claim_date - bp_reading_date).days <= 180

        if (one_month_difference and not reading_within_one_month):
            reading_within_one_month = True
        elif (one_month_difference and reading_within_one_month):
            reading_within_six_months = True
        elif (six_month_difference and not reading_within_six_months):
            reading_within_six_months = True

    return reading_within_one_month and reading_within_six_months

def validate_request_body(request_body):
    schema = {
        "body": {
            "type": "dict",
            "schema": {
                "date_of_claim": {"type": "string"},
                "veteran_is_service_connected": {"type": "boolean"},
                "bp": {
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "allow_unknown": True,
                        "schema": {
                            "diastolic": {"type": "integer"},
                            "systolic": {"type": "integer"},
                            "date": {"type": "string"}
                        }
                    }
                },
                "medication": {
                    "type": "list",
                    "schema": {
                        "type": "string",
                    }
                }
            }
        }
    }
    v = Validator(schema)

    return v.validate(request_body)

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

