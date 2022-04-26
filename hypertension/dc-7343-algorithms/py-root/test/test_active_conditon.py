import pytest
from lib.algorithms.active_condition import active_cancer_condition


@pytest.mark.parametrize(
    "request_body, active_cancer_condition_result, errors",
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
                    "veteran_is_service_connected_for_dc7343": True
                },
                {"active_cancer_present": True,
                 "active_cancer_matches_count": 1,
                 "success": True},
                {}
        ),
    ])
def test_active_cancer(request_body, active_cancer_condition_result, errors):

    assert active_cancer_condition(request_body) == active_cancer_condition_result
