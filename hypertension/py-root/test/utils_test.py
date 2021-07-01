from pathlib import Path
from lib.utils import fix_pem_formatting

from lib.utils import load_config

CURRENT_DIR = Path(__file__).parent
NORMAL_RSA_KEY_PATH = CURRENT_DIR / "fake-realistic-rsa-key.txt"
CUSTOM_RSA_KEY_PATH = CURRENT_DIR / "fake-custom-rsa-key.txt"


def test_fix_pem_formatting():
    normal_rsa_key = NORMAL_RSA_KEY_PATH.read_text().strip()
    key_in_our_custom_format = CUSTOM_RSA_KEY_PATH.read_text().strip()

    assert fix_pem_formatting(key_in_our_custom_format) == normal_rsa_key

def test_load_config():
    assert load_config(True) == "TO BE IMPLEMENTED"
