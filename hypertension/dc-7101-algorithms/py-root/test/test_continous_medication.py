import pytest
from lib.algorithms.continuous_medication import continuous_medication_required
from lib.algorithms.utils import hypertension_medications 

@pytest.mark.parametrize(
    "request_data, hypertension_medications, continuous_medication_required_calculation",
    [
        # Service connected and medication used to treat hypertension
        (
            {
                "bp": [],
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
                "bp": [],
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
                "bp": [],
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
        # Service connected, multiple medications, some to treat and others not to treat hypertension
        (
            {
                "bp": [],
                "medication": ["Benazepril", "Advil"],
                'date_of_claim': '2021-11-09',
                'veteran_is_service_connected': True
            },
            hypertension_medications,
            {
                "success": True,
                "continuous_medication_required": True
            },
        ),
        # Service connected but no medication
        (
            {
                "bp": [],
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
    """
    Test the history of continuous medication required algorithm

    :param request_data: request body with blood pressure readings and other data
    :type request_data: dict
    :param hypertension_medications: set of medications that treat hypertension 
    :type hypertension_medications: set
    :param continuous_medication_required_calculation: correct return value from algorithm
    :type continuous_medication_required_calculation: dict
    """
    assert continuous_medication_required(request_data, hypertension_medications) == continuous_medication_required_calculation