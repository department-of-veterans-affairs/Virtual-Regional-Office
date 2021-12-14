def continuous_medication_required(request, hypertension_medications):
  """
  Determine if there is the veteran requires continuous medication for hypertension

  :param request: request body
  :type request: dict
  :param hypertension_medications: set of medications used to treat hypertension
  :type hypertension_medications: set
  :return: response body indicating success or failure with additional attributes 
  :rtype: dict
  """

  continuous_medication_required_calculation = {
        "success": True
  }

  if not request["veteran_is_service_connected"]:
    continuous_medication_required_calculation["continuous_medication_required"] = False
    return continuous_medication_required_calculation

  veterans_medication_list = request["medication"]
  veteran_medication_is_hypertension_medication = False
  for medication in veterans_medication_list:
    if (medication.lower() in hypertension_medications):
      veteran_medication_is_hypertension_medication = True
      break

  continuous_medication_required_calculation["continuous_medication_required"] = veteran_medication_is_hypertension_medication
  
  return continuous_medication_required_calculation

