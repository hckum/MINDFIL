#! /usr/bin/python
# encoding=utf-8

from flask import session
from functools import wraps
from collections import namedtuple
import config



RET = namedtuple('RET', ['status', 'return_data'])


def state_machine(function_name):
    def wrapper(f):
        @wraps(f)
        def inner_wrapper(*args, **kwargs):
            sequence = config.SEQUENCE['Mode_' + session[session['user_id'] + '_mode']]
            for i in range(len(sequence)):
                current = sequence[i]
                # handle the flask blueprint
                if '.' in current:
                    current = current.split('.')[1]
                if current == function_name:
                    session['state'] = i
                    break
            return f(*args, **kwargs)
        return inner_wrapper
    return wrapper
