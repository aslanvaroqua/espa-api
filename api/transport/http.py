"""First API, local access only"""
import hug

from api.transport import user


@hug.get('/', versions=(0, 1))
def echo():
    return 'Hi from root!'


api = hug.API(__name__)
api.extend(user, route='/user')
