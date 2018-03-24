"""This is the interface module to the EROS registration service"""
import json
import logging

import requests


def json_request(resource='login', data=None, headers=None,
                 verify=True, verb='get'):
    """ Common upstream api call """
    kwargs = dict(data=data, headers=headers, verify=verify)
    resp = getattr(requests, verb)(resource, **kwargs)
    return resp.json()


class ErsInvalidLogin(Exception):
    """ Raised on invalid credentials """
    pass


class ErsInvalidResponse(Exception):
    """ Raised on unexpected responses from ERS """
    pass


class ErsUnavailable(Exception):
    """ Raised on inability to connect to ERS """
    pass


def ers_api(url='', data=None, headers=None, verify=True, verb='get'):
    """ Interface layer to raise errors on ERS behavior """
    try:
        response = json_request(resource=url, data=data, headers=headers,
                                verify=verify, verb=verb)
    except json.decoder.JSONDecodeError as exc:
        raise ErsInvalidLogin('Invalid login response')
    except requests.exceptions.RequestException as exc:
        raise ErsUnavailable()
    if response.get('errors'):
        raise ErsInvalidLogin(response['errors'])
    if 'data' not in response.keys():
        raise ErsInvalidResponse()
    return response.get('data')


def login(username, password, secret='', url='', resource='auth', verify=True):
    """ If user login is successful, an auth token is returned

    Args:
        username (str): external user authentication id
        password (str): password for user authentication
        secret (str): principal authorization secret for ERS environment
        url (str): full resource path to running ERS application
        resource (str): api endpoint for the ERS application
        verify (bool): flag to enforce ssl certificate verification

    Returns:
        str: auth token

    Example:
        >>> ers.login('username', 'password', '46b5bdef021a6d1c')
        'fb0fc56dd0692391'
    """
    if not all((username, password)):
        raise ErsInvalidLogin('Invalid username/password pair')
    url = '{}/{}'.format(url, resource)
    request = {
        'username': username,
        'password': password,
        'client_secret': secret
    }
    response = ers_api(url, data=request, verb='post', verify=verify)
    if 'authToken' not in response.keys():
        raise ErsInvalidResponse()
    return response.get('authToken')


def roles(token, url='', resource='me', verify=True):
    """ For a valid authentication token, returns the demographics of the user

    Args:
        token (str): a recent and valid login token from ERS
        url (str): full resource path to running ERS application
        resource (str): api endpoint for the ERS application
        verify (bool): flag to enforce ssl certificate verification

    Returns:
        str: username
        str: email
        int: contact_id
        tuple: roles

    Example:
        >>> ers.roles('fb0fc56dd0692391')
        ('username', 'password', (,))
    """
    url = '{}/{}'.format(url, resource)
    header = {
        'X-AuthToken': token
    }
    response = ers_api(url, headers=header, verify=verify)
    keys = ('username', 'email', 'contact_id', 'roles')
    if not all(x in response for x in keys):
        raise ErsInvalidResponse()
    return (
        response['username'],
        response['email'],
        response['contact_id'],
        response['roles'],
    )
