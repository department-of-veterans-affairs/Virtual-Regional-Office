from datetime import datetime

# TODO: This might be overwriting whatever data object is passed in as bp_readings (I dont know b/c I dont know how Python works). If this is happening, change this function so that it doesnt overwrite the original data anymore.
def add_proper_dates(bp_readings):
    for bp_reading in bp_readings:
        bp_reading.update({ "date_object": datetime.fromisoformat(bp_reading["date"]) })

    return bp_readings


def sufficient_to_autopopulate (bp_readings):
    # TODO: Implement algorithm
    # BP data is sufficient to run through the predominance calculation algorithm and (thus auto-populate VBMS) if there is 1 BP reading within the month before the Date of Claim and at least 1 additional BP reading within 6 months of the Date of Claim.

    return add_proper_dates(bp_readings)
