from functools import wraps

from flask import request
from flask.ext.restful import abort

from tsserver import app


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_credentials(auth.username, auth.password):
            abort(401)
        return f(*args, **kwargs)

    return decorated


def check_credentials(username, password):
    """
    Check whether username/password combination is valid
    :type username: str
    :type password: str
    :return: True if credentials are valid, False otherwise
    """
    return (username == app.config['USERNAME']
            and password == app.config['PASSWORD'])
