from datetime import datetime

pc_procedure = {
    "(Surgery - distal subtotal pancreatectomy)",
    #703423002
}


def procedure_match(request_body):
    """
    Determine if there is the veteran requires continuous medication for pancreatic cancer

    :param request_body: request body
    :type request_body: dict
    :return: response body indicating success or failure with additional attributes
    :rtype: dict
    """
    procedure_match_calculation = {
        "success": True
    }

    veterans_procedure_list = request_body["procedure"]

    date_of_claim = request_body["date_of_claim"]
    date_of_claim_date = datetime.strptime(date_of_claim, "%Y-%m-%d").date()
    pc_procedure_within_six_months = False

    for procedure in veterans_procedure_list:
        if procedure["text"].lower() in [x.lower() for x in pc_procedure]:
            procedure_date = procedure["performed_date"]
            procedure_date_formatted = datetime.strptime(procedure_date, "%Y-%m-%d").date()
            if (date_of_claim_date - procedure_date_formatted).days <= 180:
                pc_procedure_within_six_months = True
            else:
                continue

    procedure_match_calculation["pc_procedure_within_six_months"] = pc_procedure_within_six_months

    return procedure_match_calculation
