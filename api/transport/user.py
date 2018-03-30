""" Interface layer for user authentication/authorization """

import hug


api = hug.API(__name__)


@hug.get('/', api=api)
def get_user():
    return 'hello /user!'
