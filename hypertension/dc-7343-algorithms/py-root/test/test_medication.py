import pytest
from lib.algorithms.medication import medication_match


@pytest.mark.parametrize(
    "request_body, medication_match_result, errors",
    [
        (
                {
                    "condition": [
                        {
                            "code": 363419009,
                            "text": "Malignant tumor of head of pancreas (disorder)",
                            "onset_date": "2021-11-01",
                            "abatement_date": "2022-04-01"
                        },
                    ],
                    "medication": ["5-fluorouracil",
                                   "Irinotecan"],
                    "procedure": [
                        {
                            "code": 174710004,
                            "text": "(Surgery - distal subtotal pancreatectomy)",
                            "performed_date": "2021-12-01",
                            "last_update_date": "2021-12-15",
                            "status": "completed"
                        }
                    ],
                    "date_of_claim": "2021-11-09",
                },
                {"continuous_medication_required": True,
                 "continuous_medication_matches_count": 2,
                 "success": True},
                {}
        ),
    ])
def test_medication(request_body, medication_match_result, errors):

    assert medication_match(request_body) == medication_match_result
