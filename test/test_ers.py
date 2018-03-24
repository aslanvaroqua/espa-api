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
        token = ers.login('json', 'json', secret='46b5bdef021a6d1c', url='http://ers/jsonapi')

def test_bad_url():
    with pytest.raises(ers.ErsUnavailable) as exc:
        token = ers.login('user', 'pass', url='http://isnothere/api')

@test.vcr.use_cassette(test.cassettes['ers'])
def test_roles():
    user = ers.roles('fb0fc56dd0692391', url='http://ers/api', verify=False)
    assert isinstance(user, tuple)
    assert len(user) == 4
