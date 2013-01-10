from flask import Flask
import redis

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

