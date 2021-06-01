import pytest

from src.get_requests import get_canned_json

def test_something(get_fake_canned_json):
  assert get_canned_json() == get_fake_canned_json
