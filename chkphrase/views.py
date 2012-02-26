from chkphrase import app
from chkphrase import auth
import json
from flask import request


@app.route('/')
@auth.requires_auth
def index():
    return 'Hello World! %s' % request.authorization.username
