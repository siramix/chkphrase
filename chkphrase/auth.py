"""
This module deals with authorizing users for access via HTTP simple
authentication. When the password is received it is hashed using SHA-256 and
compared against the hash in the database for that user.
"""
from functools import wraps
import hashlib
from flask import request, Response
from chkphrase.models import User
import chkphrase.database as db


def check_auth(username, password):
    """This function is called to check if a username/password combination is
    valid."""
    result = db.db_session.query(User).filter(User.name==username)
    if result.count() != 1:
        return False
    else:
        truePass = result[0].password
        tryPass = hashlib.sha256(password).hexdigest()
        return truePass == tryPass

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
