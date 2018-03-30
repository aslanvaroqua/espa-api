""" These are extensions of the /user api """

import hug


@hug.get('/')
def get_user():
    return 'hello /user!'
