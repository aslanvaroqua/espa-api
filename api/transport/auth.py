""" User Authentication """

import hug

from api.auth import ers

def verify_user(user_id, key):
    """ TODO: docstring """
    token = ers.login(user_id, key)
    if token:
        return ers.roles(token)


authentication = hug.authentication.basic(verify_user=verify_user)
