from datetime import datetime

pc_procedure_cpt = {
    "1007926",
    "48153",
    "48154",
    "48140",
    "1007923",
    "48152",
    "00794",
    "48150",
    "1007918",
    "48146",
    "48155",
    "48160",
    "1010904",
    "1010905",
    "77014",
    "4164F",
    "32701",
    "77399",
    "01922",
    "77469",
    "1010921",
    "1010843",
    "1010919",
    "77799",
    "77789",
    "77750",
    "1010895",
    "77423",
    "1015093",
    "1015092",
    "1014921",
    "77372",
    "77371",
    "77373",
    "77295",
    "77301",
    "77386",
    "77385",
    "1022243",
    "4165F",
    "77338",
}

pc_procedure_snomed = {
    116031009,
    401004,
    174710004,
    235468001,
    235469009,
    235470005,
    265461002,
    60194009,
    91516004,
    33479006,
    9524002,
    287846000,
    174697009,
    69036001,
    76077004,
    10611004,
    1156529004,
    1156528007,
    33356009,
    80347004,
    312248006,
    33195004,
    50632006,
    1156525005,
    77613002,
    228676000,
    45643008,
    1156506007,
    1156526006,
    1162782007,
    169336005,
    228672003,
    228667007,
    1204242009,
    38104006,
    228671005,
    228666003,
    24689001,
    74023000,
    228675001,
    395096001,
    446504008,
    448461009,
    115959002,
    441799006,
    11331000224100,
    1156530009,
    1156524009,
    169314007
}


def match_codes(procedure):
    match = False
    code = str(procedure["code"])
    if code in [str(x) for x in pc_procedure_snomed]:  # assume snomed code system for now
        match = True

    if procedure["code_system"]:
        if procedure["code_system"] == "http://www.ama-assn.org/go/cpt" and code in pc_procedure_cpt:
            match = True

    return match


def procedure_match(request_body):
    """
    Determine if there is the veteran requires continuous medication for pancreatic cancer

    :param request_body: request body
    :type request_body: dict
    :return: response body indicating success or failure with additional attributes
    :rtype: dict
    """
    procedure_match_calculation = {
        "success": True,
        "procedure_within_six_months": False
    }

    date_of_claim = request_body["date_of_claim"]
    date_of_claim_datetime = datetime.strptime(date_of_claim, "%Y-%m-%d").date()

    for procedure in request_body["procedure"]:
        match = match_codes(procedure)
        status = procedure["status"].lower()
        if match and status == "active":
            procedure_match_calculation["procedure_within_six_months"] = True
        elif match and status != "active":
            procedure_date = procedure["performed_date"]
            procedure_date_formatted = datetime.strptime(procedure_date, "%Y-%m-%d").date()
            if (date_of_claim_datetime - procedure_date_formatted).days <= 180:
                procedure_match_calculation["procedure_within_six_months"] = True

    return procedure_match_calculation
