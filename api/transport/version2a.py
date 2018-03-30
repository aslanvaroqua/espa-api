""" API interface layer for the Version 2a route """

import hug

from api.transport import user

api = hug.API(__name__)
api.extend(user.api, route='/user')
