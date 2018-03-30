import mock

import pytest

from api.domain import user
from api.db import psql
from api.config import cfg


def test_where_sql():
    sql = "SELECT id, username, email, contactid, date_joined FROM auth_user"
    assert sql == user.where_sql()
    sql = ("SELECT id, username, email, contactid, date_joined FROM auth_user "
           "WHERE username = %(username)s")
    assert sql == user.where_sql({'username': 'davyjones'}, 'auth_user')


@mock.patch.dict('os.environ', {'ESPA_API_CONFIG_PATH': './run/config.ini'})
@pytest.fixture(scope='module')
def db():
    db = psql.connection(**cfg.get('db', lower=True))
    db.query("set search_path = espa_unit_test;")
    return db

@pytest.fixture
def user1():
    return {"username": "dave", "email": "y@xyz.com", "contactid": "1"}

def test_insert_user(user1):
    sql, params = user.insert_sql(user1)
    assert set(params) - set(user1) == {'date_joined', 'last_login'}
    assert sql.startswith('INSERT INTO auth_user')
    assert 'ON CONFLICT (username) DO UPDATE SET' in sql
    assert sql.endswith('RETURNING (id)')

@pytest.mark.integration
def test_db_make_user(db, user1):
    user_id = user.insert(user1, db.query)
    assert isinstance(user_id[0]['id'], int)
    filters = {'id': user_id[0]['id']}
    user2 = user.where(filters, db.query)
    assert {'contactid', 'username', 'email', 'id', 'last_login', 'date_joined'} == set(user2[0])
