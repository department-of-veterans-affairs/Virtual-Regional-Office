import pytest
from lib.algorithms.medication import medication_match


@pytest.mark.parametrize(
    "request_body, medication_match_result, errors",
    [
        (
                {
                    "condition": [
                        {
                            "code": "363419009",
                            "status": "active",
                            "text": "Malignant tumor of head of pancreas (disorder)",
                            "onset_date": "2021-11-01",
                            "abatement_date": "2022-04-01"
                        },
                    ],
                    "medication": [{"text": "5-fluorouracil",
                                    "code": "4492",
                                    "authored_on": "2022-04-01",
                                    "status": "completed"},
                                   {"text": "Irinotecan",
                                    "code": "1726319",
                                    "authored_on": "2022-04-01",
                                    "status": "completed"}
                                   ],
                    "procedure": [
                        {
                            "code": "174710004",
                            "text": "(Surgery - distal subtotal pancreatectomy)",
                            "performed_date": "2021-12-01",
                            "last_update_date": "2021-12-15",
                            "status": "completed"
                        }
                    ],
                    "date_of_claim": "2022-11-09",
                },
                {"continuous_medication_required": False,
                 "success": True},
                {}
        ),
        (
                {
                    "condition": [
                        {
                            "code": "363419009",
                            "status": "active",
                            "text": "Malignant tumor of head of pancreas (disorder)",
                            "onset_date": "2021-11-01",
                            "abatement_date": "2022-04-01"
                        },
                    ],
                    "medication": [{"text": "5-fluorouracil",
                                    "code": "4492",
                                    "authored_on": "2022-04-01",
                                    "status": "active"},
                                   {"text": "Irinotecan",
                                    "code": "1726319",
                                    "authored_on": "2022-04-01",
                                    "status": "active"}
                                   ],
                    "procedure": [
                        {
                            "code": "174710004",
                            "text": "(Surgery - distal subtotal pancreatectomy)",
                            "performed_date": "2021-12-01",
                            "last_update_date": "2021-12-15",
                            "status": "completed"
                        }
                    ],
                    "date_of_claim": "2022-01-09",
                },
                {"continuous_medication_required": True,
                 "success": True},
                {}
        )
    ])
def test_medication(request_body, medication_match_result, errors):

    assert medication_match(request_body) == medication_match_result
