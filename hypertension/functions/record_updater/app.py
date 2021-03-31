import json


def lambda_handler(event, context):
    print(f"Incoming event: {event}")
    claim_status = event["body"]["claim_status"]
    print(f"Updating VMBS with data {claim_status}")
    return {
        'statusCode': 200,
        'body': {"claim_status": claim_status}
    }


def main():
    input_event = {
        "statusCode": 200,
        "body": {
            "claim_status": {
                "pvid": "123",
                "claim_type": "disability",
                "claim_subtype": "increase",
                "applicable": True,
                "icn": "1001096151",
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
                "hasEnoughData": True,
                "has_hypertension": True
            }
        }
    }

    print(json.dumps(lambda_handler(input_event, None)))


if __name__ == "__main__":
    main()
