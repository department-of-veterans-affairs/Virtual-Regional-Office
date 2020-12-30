import json
import csv
from pathlib import Path

def lambda_handler(event, context):
    print(f"Incoming event: {event}")
    claim_status = event["body"]["claim_status"] or {}
    icn = claim_status.get('icn')
    readings = get_data(icn)
    enough_data = has_enough_data(readings)
    claim_status.update({"data": readings, "hasEnoughData": enough_data})
    return {
        'statusCode': 200,
        'body': {"claim_status": claim_status}
    }
    
def get_data(icn):
    print(f"Getting info for person with ICN '{icn}'")
    """
    import pandas as pd  # pandas==1.0.3
    import sqlalchemy as sql  # SQLAlchemy==1.3.16
    bp_query = f"EXECUTE VBA_AVD.Dflt.IDRC_BloodPressure @Icn = N'{icn}'"
    engine = sql.create_engine("mssql+pyodbc://{}/{}?driver={}".format(server, database, "SQL+Server"))
    readings = pd.read_sql_query(bp_query, engine)
    med_query = f"EXECUTE VBA_AVD.Dflt.IDRC_Medication @Icn = N'{icn}' @VASRDCode = N'7101'"
    medication = pd.read_sql_query(med_query, engine)
    return (readings, medication)
    """
    readings = []
    if icn == "1234567890": # intentionally insufficient
        readings = [
                    {
                        "stationNumber": "689",
                        "facility" : "(689) Connecticut HCS (Westhaven)",
                        "systolic" : "105",
                        "diastolic" : "54",
                        "datetime" : "2020-11-19 01:22"
                    }]
    else:
        data_path=Path.cwd().joinpath("BloodPressure.csv")
        with open(data_path, "r") as infile:
            reader = csv.DictReader(infile)
            readings = [row for row in reader]
    return readings
    

def has_enough_data(readings):
    enough_data = True
    readings_count = len(readings)
    if readings_count < 2:
        enough_data = False
        print("Insufficient number of readings")
    else:
        print("Claim has sufficient medical data")
    return enough_data
