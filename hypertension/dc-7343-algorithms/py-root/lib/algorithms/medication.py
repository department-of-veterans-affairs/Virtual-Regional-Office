from datetime import datetime

pc_medications = {
    "Gemcitabine",
    "5-fluorouracil",
    "Irinotecan",
    "Oxaliplatin",
    "Albumin-bound paclitaxel",
    "Capecitabine",
    "Cisplatin",
    "Paclitaxel",
    "Docetaxel",
    "Irinotecan liposome",
    "Sunitinib",
    "Everolimus",
    "Octreotide",
    "Lanreotide",
}

pc_rx_norm = {
    1736854, 583214, 1860480, 1736776, 1726319, 4492
}


def medication_match(request_body):
    """
    Determine if there is the veteran requires continuous medication for pancreatic cancer

    :param request_body: request body
    :type request_body: dict
    :return: response body indicating success or failure with additional attributes
    :rtype: dict
    """

    medication_match_calculation = {
        "success": True
    }

    veterans_medication_list = request_body["medication"]
    date_of_claim = request_body["date_of_claim"]
    date_of_claim_date = datetime.strptime(date_of_claim, "%Y-%m-%d").date()

    vet_is_taking_pc_medication_within_six_months = False
    medication_matches = 0
    for medication in veterans_medication_list:
        if medication["text"].lower() in [x.lower() for x in pc_medications] or medication["code"] in pc_rx_norm:
            medication_date = medication["date"]
            medication_date_formatted = datetime.strptime(medication_date, "%Y-%m-%d").date()
            if (date_of_claim_date - medication_date_formatted).days <= 180:
                vet_is_taking_pc_medication_within_six_months = True
                medication_matches += 1
            else:
                continue

    medication_match_calculation["continuous_medication_required"] = vet_is_taking_pc_medication_within_six_months
    medication_match_calculation["continuous_medication_matches_count"] = medication_matches

    return medication_match_calculation

