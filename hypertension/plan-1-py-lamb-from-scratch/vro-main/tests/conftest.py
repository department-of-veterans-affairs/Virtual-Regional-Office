import pytest

@pytest.fixture()
def get_fake_canned_json():
  with open('tests/fixtures/echo.jsontest.com.key.value.one.two.json', 'r') as fn:
    return fn.read()
