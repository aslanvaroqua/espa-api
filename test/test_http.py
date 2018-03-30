import pytest
import hug
from falcon import HTTP_400, HTTP_404, HTTP_200

from api.transport import http, user

def test_root():
    response = hug.test.get(http, '/')
    assert response.status == HTTP_200
    assert response.data == 'Hi from root!'

def test_user():
    response = hug.test.get(user, '/')
    assert response.status == HTTP_200
    assert response.data == 'hello /user!'
    response = hug.test.get(http, '/user')
    assert response.data == 'hello /user!'
