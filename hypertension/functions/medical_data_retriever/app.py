import json
import csv
from pathlib import Path
import pandas as pd
import sqlalchemy
from importlib_resources import files


def lambda_handler(event, context):
    print(f"Incoming event: {event}")
    claim_status = event["body"]["claim_status"] or {}
    icn = claim_status.get('icn')
    readings, medication = get_data(icn)
    enough_data = has_enough_data(readings)
    claim_status.update(
        {
            "data": {
                "readings": readings,
                "medication": medication
            },
            "hasEnoughData": enough_data
        }
    )
    return {
        'statusCode': 200,
        'body': {"claim_status": claim_status}
    }


def get_data(icn: str):
    print(f"Getting info for person with ICN '{icn}'")
    return get_data_dummy(icn)


def get_data_real(icn: str):
    engine = initialize_engine()
    readings = get_bloodpressure_data(engine, icn)
    medication = get_medication_data(engine, icn)


def get_data_dummy(icn: str):
    readings = []
    medication = []
    if icn == "1234567890":  # intentionally insufficient
        readings = [
            {
                "stationNumber": "689",
                "facility": "(689) Connecticut HCS (Westhaven)",
                "systolic": "105",
                "diastolic": "54",
                "datetime": "2020-11-19 01:22"
            }]
    else:
        bp_data_path = Path.cwd().joinpath("BloodPressure.csv")
        with open(bp_data_path, "r") as infile:
            reader = csv.DictReader(infile)
            readings = [row for row in reader]

    med_data_path = Path.cwd().joinpath("Meds.csv")
    with open(med_data_path, "r") as infile:
        reader = csv.DictReader(infile)
        medication = [row for row in reader]
    return (readings, medication)


def initialize_engine():
    return sqlalchemy.create_engine("mssql+pyodbc://{}/{}?driver={}".format(server, database, "SQL+Server"))


def get_bloodpressure_data(engine: sqlalchemy.engine.Engine, icn: str):
    print("Getting bloodpressure data...")
    bp_query = f"EXECUTE VBA_AVD.Dflt.IDRC_BloodPressure @Icn = N'{icn}'"
    return pd.read_sql_query(bp_query, engine)


def get_medication_data(engine: sqlalchemy.engine.Engine, icn: str):
    print("Getting medication data...")
    med_query = f"EXECUTE VBA_AVD.Dflt.IDRC_Medication @Icn = N'{icn}' @VASRDCode = N'7101'"
    return pd.read_sql_query(med_query, engine)


def has_enough_data(readings):
    enough_data = True
    readings_count = len(readings)
    if readings_count < 2:
        enough_data = False
        print("Insufficient number of readings")
    else:
        print("Claim has sufficient medical data")
    return enough_data


def main():
    input_event = {
        "statusCode": 200,
        "body": {
            "claim_status": {
                "pvid": "123",
                "claim_type": "disability",
                "claim_subtype": "increase",
                "applicable": True,
                "icn": "1001096151"
            }
        }
    }
    print(json.dumps(lambda_handler(input_event, None)))


if __name__ == "__main__":
    main()
