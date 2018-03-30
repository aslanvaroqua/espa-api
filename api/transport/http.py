""" API definition and root access routing """

import hug

from api.transport import version2a


api = hug.API(__name__)
api.extend(version2a.api, route='/api/v2a')


@hug.get('/')
def ping():
    return 'Welcome to the ESPA API, please direct requests to /api'
