import pytest

from api.db import psql


@pytest.fixture(scope='module')
def db():
    return {}

def test_param_fmt():
    assert "name = %(name)s" == psql._fmt('name', 'yogi')
    assert  "id >= %(id)d" == psql._fmt('id >=', 10)

def test_base_sql():
    assert "SELECT name FROM tomato" == psql.get("name", table="tomato")
    assert "SELECT hello, moto FROM tomato" == psql.get("hello", "moto", table="tomato")

def test_filter_sql():
    assert "" == psql.filter_sql()
    assert " WHERE username = %(username)s" == psql.filter_sql(username="eleven")
    assert " WHERE user = %(user)d AND roles in %(roles)s" == psql.filter_sql(user=10, roles=(10, 11))
