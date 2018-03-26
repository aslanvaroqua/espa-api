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
    return ''.join([
        ' WHERE ',
        ' {} '.format(compare).join(_fmt(key, value)
                                    for key, value in kwargs.items())
    ])


def get(columns, table):
    """ Format SQL to get columns from table

    Args:
        columns (tuple): column names
        table (str): table name to fetch from

    Returns:
        str: sql string
    """
    columns = tuple([columns]) if isinstance(columns, str) else columns
    return "SELECT {c} FROM {t}".format(c=', '.join(columns), t=table)


def _named_vals_fmt(values, template='%({})s'):
    """ Helper fuction to format insert statements """
    return (', '.join(values), ', '.join(map(template.format, values)))


def conflict(col_conflict, values, updates, template='%({})s',
             where=None):
    """ Column conflict formatting, see `insert` for arg descriptions """
    if not col_conflict:
        return ""
    if isinstance(col_conflict, str):
        col_conflict = tuple([col_conflict])
    return ''.join([
        " ON CONFLICT ({c})".format(c=', '.join(col_conflict)),
        " DO UPDATE SET ({0}) = ({1})".format(*_named_vals_fmt(updates)),
        filter_sql(**where)
    ])


def insert_into(values, table, template='%({})s'):
    """ Insert formatting, see `insert` for arg descriptions """
    c, n =_named_vals_fmt(values.keys(), template)
    sql = ("INSERT INTO {t} ({c}) VALUES ({n})".format(t=table, c=c, n=n))
    return sql


def returner(column):
    """ Helper to create sql of column to return on updates/inserts """
    if isinstance(column, str):
        column = tuple([column])
    return (" RETURNING ({r})"
            .format(r=', '.join(column)) if column else '')


def insert(table, values, template='%({})s', col_conflict=None,
           update_all=False, updates=None, where=None, returning=None):
    """ Insert new values, with optional column conflict handling

    Args:
        table (str): database schema table to insert data into
        values (dict): parameters to insert into table
        template (str): format templating for keys as values
        col_conflict (tuple): column to detect conflicts, to allow updates
        update_all (bool): update all `values` on conflict
        updates (tuple): columns to update on conflict
        where (dict): filters for subsetting update on conflict
        returning (str): value to return from modified/created rows

    Returns:
        str: full sql statement

    Examples:
        >>> insert("ordering_order", {"orderid": 1, "status": "ready"})
        "INSERT INTO ordering_order (orderid, status) VALUES (%(orderid)s,
        %(status)s)"
        >>> insert("users", {"username": "greg", "contactid": 10},
                   col_conflict='username', updates='contactid',
                   where={'username': 'greg'}, returning='id')
        "INSERT INTO users (username, contactid) VALUES (%(username)s, "
        "%(contactid)s) ON CONFLICT (username) DO UPDATE SET (contactid) = "
        "(%(contactid)s) WHERE username = %(username)s RETURNING (id)"
    """
    updates = tuple(k for k in values.keys() if (update_all or (updates is not None and k in updates)))
    return ''.join([
        insert_into(values=values, table=table, template=template),
        conflict(col_conflict=col_conflict, values=values, template=template,
                 updates=updates, where=where),
        returner(returning)
    ])


def update(table, values, where=None, returning=None, template='%({})s'):
    """ Format statement to update columns in a table

    Args:
        table (str): database schema table of columns to update
        values (dict): key/values of columns/values to update
        where (dict): column filters to restrict update
        returning (str): value to return from modified/created rows
        template (str): format templating for keys as values

    Returns:
        str: sql statement

    Examples:
        >>> update('bigtable', {"level": 9000})
        "UPDATE bigtable SET (level) = (%(level)s)"
        >>> update('otherone', {"yolo": "once"}, {"level": "9000"}, 'id')
        "UPDATE otherone SET (yolo) = (%(yolo)s) WHERE level = %(level)s "
        "RETURNING (id)"
    """
    return ''.join([
        "UPDATE {t} SET ".format(t=table),
        "({0}) = ({1})".format(*_named_vals_fmt(values)),
        filter_sql(**where or {}),
        returner(returning),
    ])
