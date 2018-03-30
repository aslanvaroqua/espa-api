""" Interface layer for user authentication/authorization """

import hug

from api.transport.auth import authentication


api = hug.API(__name__)


@hug.get('/', api=api, requires=authentication)
def get_user(user: hug.directives.user):
    return 'hello {}!'.format(user)
