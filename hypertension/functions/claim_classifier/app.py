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
    hypertension_identified = number_of_readings_sufficient and number_of_days_sufficient and number_of_abnormal_readings_sufficient
    return hypertension_identified

def assess_medication(medication):
    # TODO: Implement better medication logic
    return len(medication) > 0