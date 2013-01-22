"""
ISIS: A Server-Sent Events Chat App.
Copyright 2013 Brand Thomas <bt@brand.io>
"""

import redis

from flask import Flask

from core.models import Anonymous

"""
CONFIGURATION
"""

DEBUG = True
SECRET_KEY = 'not a secret'

"""
APPLICATION CREATION
"""

app = Flask(__name__)
app.config.from_object(__name__)

rds = redis.Redis()

from core import login_manager

login_manager.setup_app(app)
