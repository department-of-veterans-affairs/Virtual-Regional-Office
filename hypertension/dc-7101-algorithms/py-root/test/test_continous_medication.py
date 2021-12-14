import pytest
from lib.algorithms.continuous_medication import continuous_medication_required
from lib.algorithms.utils import hypertension_medications 

@pytest.mark.parametrize(
    "request_data, hypertension_medications, continuous_medication_required_calculation",
    [
        # Service connected and medication used to treat hypertension
        (
            {
                "bp": [
                    {
                        "diastolic": 115,
                        "systolic": 180,
                        "date": "2021-11-01"
                    },
                    {
                        "diastolic": 110,
                        "systolic": 200,
                        "date": "2021-09-01"
                    }
                ],
                "medication": ["Benazepril"],
                'date_of_claim': '2021-11-09',
                'veteran_is_service_connected': True
            },
            hypertension_medications,
            {
                "success": True,
                "continuous_medication_required": True
            },
        ),
        # Not service connected but uses medication used to treat hypertension
        (
            {
                "bp": [
                    {
                        "diastolic": 115,
                        "systolic": 180,
                        "date": "2021-11-01"
                    },
                    {
                        "diastolic": 110,
                        "systolic": 200,
                        "date": "2021-09-01"
                    }
                ],
                "medication": ["Benazepril"],
                'date_of_claim': '2021-11-09',
                'veteran_is_service_connected': False
            },
            hypertension_medications,
            {
                "success": True,
                "continuous_medication_required": False
            },
        ),
        # Service connected but doesn't use medication used to treat hypertension
        (
            {
                "bp": [
                    {
                        "diastolic": 115,
                        "systolic": 180,
                        "date": "2021-11-01"
                    },
                    {
                        "diastolic": 110,
                        "systolic": 200,
                        "date": "2021-09-01"
                    }
                ],
                "medication": ["Advil"],
                'date_of_claim': '2021-11-09',
                'veteran_is_service_connected': True
            },
            hypertension_medications,
            {
                "success": True,
                "continuous_medication_required": False
            },
        ),
        # Service connected but no medication
        (
            {
                "bp": [
                    {
                        "diastolic": 115,
                        "systolic": 180,
                        "date": "2021-11-01"
                    },
                    {
                        "diastolic": 110,
                        "systolic": 200,
                        "date": "2021-09-01"
                    }
                ],
                "medication": [],
                'date_of_claim': '2021-11-09',
                'veteran_is_service_connected': True
            },
            hypertension_medications,
            {
                "success": True,
                "continuous_medication_required": False
            },
        ),
    ],
)
def test_continuous_medication_required(request_data, hypertension_medications, continuous_medication_required_calculation):
    assert continuous_medication_required(request_data, hypertension_medications) == continuous_medication_required_calculation