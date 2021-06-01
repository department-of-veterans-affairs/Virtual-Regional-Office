import requests

def get_canned_json():
  return requests.get('http://echo.jsontest.com/key/value/one/two').text
