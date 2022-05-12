import pytest
from lib.algorithms.condition import active_cancer_condition


@pytest.mark.parametrize(
    "request_body, active_cancer_condition_result, errors",
    [
        (
                {
                    "condition": [
                        {
                            "code": "363419009",
                            "text": "Malignant tumor of head of pancreas (disorder)",
                            "status": "active",
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
                                    "status": "active"}],
                    "procedure": [
                        {
                            "code": "174710004",
                            "code_system": "http://snomed.info/sct",
                            "text": "(Surgery - distal subtotal pancreatectomy)",
                            "performed_date": "2021-12-01",
                            "last_update_date": "2021-12-15",
                            "status": "completed"
                        }
                    ],
                    "date_of_claim": "2021-11-09",
                },
                {"active_cancer_present": True,
                 "success": True},
                {}
        ),
    ])
def test_active_cancer(request_body, active_cancer_condition_result, errors):

    assert active_cancer_condition(request_body) == active_cancer_condition_result
