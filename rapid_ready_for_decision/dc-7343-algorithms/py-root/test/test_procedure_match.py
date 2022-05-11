import pytest
from lib.algorithms.procedure import procedure_match


@pytest.mark.parametrize(
    "request_body, procedure_match_result, errors",
    [
        (
                {
                    "condition": [
                        {
                            "code": 363419009,
                            "status": "active",
                            "text": "Malignant tumor of head of pancreas (disorder)",
                            "onset_date": "2021-11-01",
                            "abatement_date": "2022-04-01"
                        },
                    ],
                    "medication": [{"text": "5-fluorouracil",
                                    "code": 4492,
                                    "date": "2022-04-01"},
                                   {"text": "Irinotecan",
                                    "code": 1726319,
                                    "date": "2022-04-01"}],
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
                {"pc_procedure_within_six_months": True,
                 "success": True},
                {}
        ),
    ])
def test_procedure(request_body, procedure_match_result, errors):

    assert procedure_match(request_body) == procedure_match_result
