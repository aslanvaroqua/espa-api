""" TODO: DOCSTRING """
import datetime


from api.db import psql
from api.schema.user import UserEntrySchema


def insert_sql(user, table='auth_user'):
    """ Format the insert statement to create/update a user

    Args:
        user (dict): a valid user entry schema
        table (str): database schema table to insert into

    Returns:
        str: sql insert statement
        dict: parametrized column values
    """
    params = UserEntrySchema().dump(UserEntrySchema().load(user))
    return psql.insert(table=table, values=params,
                       col_conflict='username', update_all=True,
                       returning='id'), params


def insert(user, db):
    """ Push a user object to a database

    Args:
        user (dict): user information to be inserted/updated in the db
        db (method): callable which takes (str, dict) parameterized sql

    Returns:
        list: the created user objects
    """
    return db(*insert_sql(user))


def where_sql(filters=None, table='auth_user', compare='AND'):
    """ SQL formatting for a user

    Args:
        table (str): database schema table to query from
        filters (dict): sql where filters
        compare (str): sql where combination AND/OR

    Returns:
        str: sql query string

    Examples:
        >>> where_sql('auth_user', {'username': 'davyjones'})
        "SELECT id, username, email, contactid, date_joined FROM auth_user "
        "WHERE username = %(username)s"
    """
    columns = ('id', 'username', 'email', 'contactid', 'date_joined')
    return ''.join([
        psql.get(columns, table=table),
        psql.filter_sql(compare=compare, **filters) if filters else ''
    ])


def where(filters, db):
    """ Pull matching user objects from a database

    Args:
        filters (dict): db schema table columns to use as filters
        db (method): callable which takes (str, dict) parameterized sql

    Returns:
        list: matching results of the query
    """
    return UserEntrySchema(many=True).load(
        db(where_sql(filters), filters)
    )
