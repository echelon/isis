#!/usr/bin/env python
"""
ISIS: A Server-Sent Events Chat App.
Copyright 2013 Brand Thomas <bt@brand.io>
"""

import argparse
import threading

"""
APPLICATION COMPONENTS
"""

import database

from app import app
#from preprocess import *
from model import *
from views import *

# XXX: Import order matters!
from core import mod_core
from userext import mod_userext
from chat import mod_chat

app.register_blueprint(mod_core, url_prefix='')
app.register_blueprint(mod_userext, url_prefix='/userext')
app.register_blueprint(mod_chat, url_prefix='/chat')

from core import preprocess

preprocess.install(app)

"""
COMMANDLINE / MAIN
"""

from core import common

if __name__ == '__main__':
	common.main(app)

