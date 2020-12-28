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
    event.update({"has_hypertension": has_hypertension})
    return {
        'statusCode': 200,
        'body': {"claim_status": claim_status}
    }

def assess_criteria(readings):
    '''
    From Business Rule Description:
    Blood Pressure Readings at required levels, taken at least 2 times on at least 3 different days.
        Diastolic blood pressure is predominantly 90mm or greater; or
        Systolic blood pressure is predominantly 160mm or greater with a diastolic blood pressure of less than 90mm.
    '''
    hypertension_identified = False

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
                print(f"> 190 Systolic ({systolic}) found on {str(date_taken)}")
                abnormal_count += 1
                seen_dates.add(date_taken)
            elif diastolic >= 90:
                print(f"> 90 Diastolic ({diastolic}) found on {str(date_taken)}")
                abnormal_count += 1
                seen_dates.add(date_taken)
    number_of_days = len(seen_dates)
    number_of_days_sufficient = (number_of_days >= 3)
    number_of_abnormal_readings_sufficient = (abnormal_count >= 2)

    print(f"Number of abnormal readings: {abnormal_count}, number of days these readings were taken:{number_of_days}")

    if number_of_readings_sufficient and number_of_days_sufficient and number_of_abnormal_readings_sufficient:
        hypertension_identified = True
    return hypertension_identified


