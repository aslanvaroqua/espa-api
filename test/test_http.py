import pytest
import hug
from falcon import HTTP_400, HTTP_404, HTTP_200

from api.transport import http

def test_ping():
    response = hug.test.get(http, '/')
    assert response.status == HTTP_200
    assert response.data == 'Welcome to the ESPA API, please direct requests to /api'

def test_versions():
    response = hug.test.get(http, '/api/v2a')
    assert response.status == HTTP_404
    assert response.data == {'errors': ['Not found on the server']}

def test_v2_user():
    response = hug.test.get(http, '/api/v2a/user')
    assert response.status == HTTP_200
    assert response.data == 'hello /user!'
