# TODO: Mock the API call
# TODO: Test something better than the length of the access token
def test_authenticate_to_lighthouse(lh_access_token):
    assert len(lh_access_token) == 929
