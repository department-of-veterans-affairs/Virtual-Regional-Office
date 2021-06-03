import os

import src.get_requests as get_requests

from tests.doubles.aws_secrets_manager import mock_get_lh_rsa_key

from src.main import main

def test_something(get_fake_canned_json):
  assert get_requests.get_canned_json() == get_fake_canned_json

def test_get_lh_token(monkeypatch):
  monkeypatch.setattr(get_requests, 'get_lh_token', mock_get_lh_rsa_key)

  fake_arn = 'some fake arn (not used anyway)'

  assert get_requests.get_lh_token(fake_arn) == os.environ['LighthousePrivateRsaKey']
