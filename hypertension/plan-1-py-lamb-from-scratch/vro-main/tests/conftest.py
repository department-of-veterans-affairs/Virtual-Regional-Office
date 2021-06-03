import pytest
import sys
import os

from dotenv import load_dotenv

load_dotenv('../cf-template-params.env')

@pytest.fixture()
def get_fake_canned_json():
  with open('tests/fixtures/echo.jsontest.com.key.value.one.two.json', 'r') as f:
    return f.read()
