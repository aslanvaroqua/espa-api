import os
import mock

import pytest

from api.db import psql
from api.config import cfg


def test_param_fmt():
    assert "name = %(name)s" == psql._fmt('name', 'yogi')
    assert  "id >= %(id)d" == psql._fmt('id >=', 10)

def test_base_sql():
    assert "SELECT name FROM tomato" == psql.get("name", table="tomato")
    assert "SELECT hello, moto FROM tomato" == psql.get(("hello", "moto"), table="tomato")

def test_filter_sql():
    assert "" == psql.filter_sql()
    assert " WHERE username = %(username)s" == psql.filter_sql(username="eleven")
    assert " WHERE user = %(user)d AND roles in %(roles)s" == psql.filter_sql(user=10, roles=(10, 11))

def test_insert():
    sql = "INSERT INTO egg (roll) VALUES (%(roll)s)"
    assert sql == psql.insert(table='egg', values={'roll': 'spring'})
    sql = ("INSERT INTO users (username, contactid) VALUES (%(username)s, "
           "%(contactid)s) ON CONFLICT (username) DO UPDATE SET (contactid) = "
           "(%(contactid)s) WHERE username = %(username)s RETURNING (id)")
    assert sql == psql.insert("users", {"username": "greg", "contactid": 10},
                              col_conflict='username', updates='contactid',
                              where={'username': 'greg'}, returning='id')

def test_update():
    sql = "UPDATE bigtable SET (level) = (%(level)s)"
    assert sql == psql.update('bigtable', {"level": 9000})
    sql = ("UPDATE otherone SET (yolo) = (%(yolo)s) WHERE level = %(level)s "
           "RETURNING (id)")
    assert sql == psql.update('otherone', {"yolo": "once"}, {"level": "9000"}, 'id')

@mock.patch.dict(os.environ, {'ESPA_API_CONFIG_PATH': './run/config.ini'})
@pytest.fixture(scope='module')
def db():
    db = psql.connection(**cfg.get('db', lower=True))
    db.query("set search_path = espa_unit_test;")
    return db

@pytest.mark.integration
def test_query(db):
    sql = psql.get('value', table='ordering_configuration')
    params = dict(key='landsatds.host')
    sql += psql.filter_sql(**params)
    assert "dummy_host" == db.query(sql, params)[0]['value']
