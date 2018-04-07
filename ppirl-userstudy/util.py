#! /usr/bin/python
# encoding=utf-8

from flask import session, redirect, url_for
from functools import wraps
from collections import namedtuple
import config
import redis
import os



RET = namedtuple('RET', ['status', 'return_data'])

if config.ENV == 'production':
    r = redis.from_url(os.environ.get("REDIS_URL"))
elif config.ENV == 'development':
    r = redis.Redis(host='localhost', port=6379, db=0)


def get_sequence_for_mode():
    return config.SEQUENCE['Mode_'+r.get(str(session['user_id'])+'_ustudy_mode')]

def get_url_for_index(index):
    return get_sequence_for_mode()[int(index)]

def redirect_by_state():
    index = session['state']
    if not index:
        index = 0
    return redirect(url_for(get_url_for_index(index)))


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
                    # disable going back
                    if i != 0 and i < session['state']:
                        return redirect_by_state()
                    session['state'] = i
                    user_id = session["user_id"]
                    r.set("session_"+str(user_id)+"_state", str(session['state']))
                    break
            return f(*args, **kwargs)
        return inner_wrapper
    return wrapper
