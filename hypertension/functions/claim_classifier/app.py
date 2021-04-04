import csv
import json
import base64
from datetime import datetime


def lambda_handler(event, context):
    print(f"Incoming event: {event}")
    claim_status = event["body"]["claim_status"]
    data = claim_status.get('data')
    has_hypertension = assess_criteria(data)
    print(f"Patient has hypertension? {has_hypertension}")
    claim_status.update({"has_hypertension": has_hypertension})
    return {
        'statusCode': 200,
        'body': {"claim_status": claim_status}
    }


def assess_criteria(data):
    '''
    From Business Rule Description:
    Blood Pressure Readings at required levels, taken at least 2 times on at least 3 different days.
        Diastolic blood pressure is predominantly 90mm or greater; or
        Systolic blood pressure is predominantly 160mm or greater with a diastolic blood pressure of less than 90mm.
    '''
    hypertension_identified = False

    reading_assessment = assess_blood_pressure(data.get('readings'))
    medication_assessment = assess_medication(data.get('medication'))
    return reading_assessment and medication_assessment


def assess_blood_pressure(readings):
    abnormal_count = 0
    seen_dates = set()
    number_of_readings_sufficient = (len(readings) >= 2)

    for reading in readings:
        systolic = int(str(reading.get("systolic")))
        diastolic = int(str(reading.get("diastolic")))
        date_string = str(reading.get("datetime"))
        date_taken = datetime.strptime(date_string, '%Y-%m-%d %H:%M').date()

        if date_taken not in seen_dates:
            if systolic >= 190 and diastolic <= 90:
                print(
                    f"> 190 Systolic ({systolic}) found on {str(date_taken)}")
                abnormal_count += 1
                seen_dates.add(date_taken)
            elif diastolic >= 90:
                print(
                    f"> 90 Diastolic ({diastolic}) found on {str(date_taken)}")
                abnormal_count += 1
                seen_dates.add(date_taken)
    number_of_days = len(seen_dates)
    number_of_days_sufficient = (number_of_days >= 3)
    number_of_abnormal_readings_sufficient = (abnormal_count >= 2)

    print(
        f"Number of abnormal readings: {abnormal_count}, number of days these readings were taken:{number_of_days}")
    hypertension_identified = number_of_readings_sufficient and number_of_days_sufficient and number_of_abnormal_readings_sufficient
    return hypertension_identified


def assess_medication(medication):
    # TODO: Implement better medication logic
    return len(medication) > 0


def main():
    input_event = {
        "statusCode": 200,
        "body": {
            "claim_status": {
                "pvid": "123",
                "claim_type": "disability",
                "claim_subtype": "increase",
                "applicable": True,
                "icn": "3456789101",
                "data": {
                    "readings": [
                        {
                            "stationNumber": "123",
                            "facility": "(123) Connecticut HCS (Westhaven)",
                            "systolic": "180",
                            "diastolic": "90",
                            "datetime": "2020-11-19 01:22"
                        },
                        {
                            "stationNumber": "123",
                            "facility": "(123) Connecticut HCS (Westhaven)",
                            "systolic": "190",
                            "diastolic": "99",
                            "datetime": "2020-11-18 11:40"
                        },
                        {
                            "stationNumber": "123",
                            "facility": "(123) Connecticut HCS (Westhaven)",
                            "systolic": "190",
                            "diastolic": "99",
                            "datetime": "2020-11-20 11:40"
                        }
                    ],
                    "medication": [
                        {
                            "\ufeffgenericName": "FUROSEMIDE",
                            "datetime": "2020-12-07",
                            "route": "ORAL",
                            "schedule": "QAM",
                            "doseOrdered": "40",
                            "unit": "MG",
                            "sig": " TAKE ONE TABLET BY MOUTH EVERY MORNING TO REMOVE FLUID/CONTROL BLOOD  PRESSURE",
                            "stationNumber": "689",
                            "facility": "(689) Connecticut HCS (Westhaven)"
                        },
                        {
                            "\ufeffgenericName": "LOSARTAN",
                            "datetime": "2020-07-20",
                            "route": "ORAL",
                            "schedule": "DAILY",
                            "doseOrdered": "25",
                            "unit": "MG",
                            "sig": " TAKE ONE TABLET BY MOUTH ONCE DAILY (30 DAYS SUPPLY D/T BACKORDER)",
                            "stationNumber": "689",
                            "facility": "(689) Connecticut HCS (Westhaven)"
                        }
                    ]
                },
                "hasEnoughData": True
            }
        }
    }
    print(json.dumps(lambda_handler(input_event, None)))


if __name__ == "__main__":
    main()
