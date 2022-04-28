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
    1736854, 583214, 1860480, 1736776
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

    vet_is_taking_pc_medication = False
    medication_matches = 0
    for medication in veterans_medication_list:
        if medication.lower() in [x.lower() for x in pc_medications]:
            vet_is_taking_pc_medication = True
            medication_matches += 1

    medication_match_calculation["continuous_medication_required"] = vet_is_taking_pc_medication
    medication_match_calculation["continuous_medication_matches_count"] = medication_matches

    return medication_match_calculation

