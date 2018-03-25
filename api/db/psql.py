""" Connection layer to PostgreSQL """

import queries


def connection(host='localhost', port=5432, dbname='postgres',
               user='postgres', password=None):
    """ Create a new Database connection

    Args:
        host (str): ip address or hostname of running postgres process
        port (int): port the running postgres is listening on
        dbname (str): name of database to connect to
        user (str): credentials username authorized to connect to db
        password (str): credentials password to authenticate user

    Returns:
        queries.Session: new database connection
    """
    connection_string = queries.uri(host, port, dbname, user, password)
    return queries.Session(connection_string)


def _fmt(key, value):
    """ Helper SQL formatting to feed parametrized queries

    Examples:
        >>> _fmt('name', 'yogi')
        "name = %(name)s"
        >>> _fmt('id >=', 10)
        "id >= %(id)d"
    """
    ctypes = {tuple: 'in'}
    stypes = {int: 'd', float: 'f'}
    if ' ' in key:
        key, compare = key.split()
    else:
        compare = ctypes.get(type(value), '=')
    stype = stypes.get(type(value), 's')
    fmtd_string = '{k} {c} %({k}){t}'.format(k=key, c=compare, t=stype)
    return fmtd_string


def filter_sql(compare='AND', **kwargs):
    """ Create WHERE clause for kwargs, formatted for parameterization

    Args:
        compare (str): AND/OR to compare all arguments
        kwargs (dict): key/value pairs that will be used in parameterized query

    Returns:
        str: where clause

    Examples:
        >>> filter_sql(username="eleven")
        " WHERE username = %(username)s"
        >>> filter_sql(user=10, roles=(10, 11))
        " WHERE user = %(user)d AND roles in %(roles)s"
    """
    if not kwargs:
        return ""
    sql = ' WHERE '
    sql += ' {} '.format(compare).join(_fmt(key, value)
                                       for key, value in kwargs.items())
    return sql


def get(*columns, table):
    """ Format SQL to get columns from table

    Args:
        columns (tuple): column names
        table (str): table name to fetch from

    Returns:
        str: sql string
    """
    return "SELECT {c} FROM {t}".format(c=', '.join(columns), t=table)
