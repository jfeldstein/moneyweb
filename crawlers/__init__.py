from __future__ import with_statement
from contextlib import closing
from flask import Flask

#configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

import moneyweb.views


@app.teardown_request
def teardown_request(exception):
    pass

