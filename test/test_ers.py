import pytest

from api import ers
import test


@test.vcr.use_cassette(test.cassettes['ers'])
def test_bad_creds():
    with pytest.raises(ers.ErsInvalidLogin) as exc:
        token = ers.login('', '')

@test.vcr.use_cassette(test.cassettes['ers'])
def test_login():
    token = ers.login('username', 'password', secret='46b5bdef021a6d1c',
                      url='http://ers/api')
    assert isinstance(token, str)

@test.vcr.use_cassette(test.cassettes['ers'])
def test_bad_login():
    with pytest.raises(ers.ErsInvalidLogin):
        token = ers.login('json', 'json', secret='46b5bdef021a6d1c', url='http://ers/noauth')

def test_bad_url():
    with pytest.raises(ers.ErsUnavailable) as exc:
        token = ers.login('user', 'pass', url='http://isnothere/api')

@test.vcr.use_cassette(test.cassettes['ers'])
def test_roles():
    user = ers.roles('fb0fc56dd0692391', url='http://ers/api', verify=False)
    assert isinstance(user, tuple)
    assert len(user) == 4

@test.vcr.use_cassette(test.cassettes['ers.bad'])
def test_bad_login_response_format():
    with pytest.raises(ers.ErsInvalidLogin):
        token = ers.login('json', 'json', secret='46b5bdef021a6d1c', url='http://ers/xmlapi')

@test.vcr.use_cassette(test.cassettes['ers.bad'])
def test_bad_login_missing_response_data():
    with pytest.raises(ers.ErsInvalidResponse):
        token = ers.login('json', 'json', secret='46b5bdef021a6d1c', url='http://ers/json4api')

@test.vcr.use_cassette(test.cassettes['ers.bad'])
def test_bad_login_response_data():
    with pytest.raises(ers.ErsInvalidResponse):
        token = ers.login('json2', 'json2', secret='46b5bdef021a6d1c', url='http://ers/json2api')

@test.vcr.use_cassette(test.cassettes['ers.bad'])
def test_bad_role_response_data():
    with pytest.raises(ers.ErsInvalidResponse):
        token = ers.roles('fb0fc56dd0692391', url='http://ers/json2api')

@test.vcr.use_cassette(test.cassettes['ers.bad'])
def test_bad_role_missing_response_data():
    with pytest.raises(ers.ErsInvalidResponse):
        token = ers.roles('fb0fc56dd0692391', url='http://ers/json3api')
