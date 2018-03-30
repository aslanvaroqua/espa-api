import mock
from base64 import b64encode

import hug
import pytest
from falcon import HTTP_400, HTTP_401, HTTP_404, HTTP_200

from api.transport import http

def test_ping():
    response = hug.test.get(http, '/')
    assert response.status == HTTP_200
    assert response.data == 'Welcome to the ESPA API, please direct requests to /api'

def test_versions():
    response = hug.test.get(http, '/api/v2a')
    assert response.status == HTTP_404
    assert response.data == {'errors': {'Not found on the server': '/api/v2a'}}

def test_v2_user_not_auth():
    response = hug.test.get(http, '/api/v2a/user')
    assert response.status == HTTP_401
    assert response.data == {'errors': {'Authentication Required': 'Please provide valid Basic HTTP Authentication credentials'}}

@pytest.fixture
def auth_header():
    return {
        'Authorization': b'Basic ' + b64encode('{0}:{1}'.format('Tim Burton', 'Wrong password').encode('utf8'))
    }

@mock.patch('api.auth.ers.login', lambda x,y: x)
@mock.patch('api.auth.ers.roles', lambda x: x)
def test_v2_user(auth_header):
    response = hug.test.get(http, '/api/v2a/user', headers=auth_header)
    assert response.status == HTTP_200
    assert response.data == "hello Tim Burton!"
