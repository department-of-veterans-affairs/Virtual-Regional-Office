hypertension_medications = {
    "benazepril",
    "lotensin",
    "captopril",
    "capoten",
    "enalapril",
    "enalaprilat",
    "fosinopril",
    "monopril",
    "lisinopril",
    "prinivil",
    "zestril",
}

def continuous_medication_required(request_body):
  """
  Determine if there is the veteran requires continuous medication for hypertension

  :param request_body: request body
  :type request_body: dict
  :return: response body indicating success or failure with additional attributes 
  :rtype: dict
  """

  continuous_medication_required_calculation = {
        "success": True
  }

  if not request_body["veteran_is_service_connected_for_dc7101"]:
    continuous_medication_required_calculation["continuous_medication_required"] = False
    return continuous_medication_required_calculation

  veterans_medication_list = request_body["medication"]
  vet_is_taking_htn_medication = False
  for medication in veterans_medication_list:
    if (medication.lower() in hypertension_medications):
      vet_is_taking_htn_medication = True
      break

  continuous_medication_required_calculation["continuous_medication_required"] = vet_is_taking_htn_medication

  return continuous_medication_required_calculation

