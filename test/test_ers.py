import pytest

from api import ers
import test


@test.vcr.use_cassette(test.cassettes['ers'])
def test_login():
    token = ers.login('username', 'password', secret='46b5bdef021a6d1c',
                      url='http://ers/api')
    assert isinstance(token, str)
