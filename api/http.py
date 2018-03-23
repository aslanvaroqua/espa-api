import os

print('hello world')

def application(*args, **kwargs):
    print('args: {}'.format(args))
    print('kwargs: {}'.format(kwargs))
    return b'Hi'
