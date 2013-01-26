"""
ISIS: A Server-Sent Events Chat App.
Copyright 2013 Brand Thomas <bt@brand.io>
"""
import os
import sys
import time
import random
import argparse
import datetime

import flask
import redis

from flask import Flask, Response, request, session, app, \
	redirect, url_for, abort, render_template, flash, \
	send_from_directory

from jinja2 import evalcontextfilter, contextfilter
from jinja2 import environmentfilter

import database
from model import *
from forms import *

from app import app
from app import rds

from flask.ext.login import login_user, logout_user

"""
DEFAULT VIEWS
"""

@app.errorhandler(404)
def not_found(e):
	import urlparse
	# TODO: Way to handle inside of Blueprint?
	url = urlparse.urlparse(request.url)
	part = filter(lambda x: x, url.path.split('/'))[0]
	if part == 'chat_api':
		return '404', 404

	return render_template('404.html'), 404

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
			os.path.join(app.root_path, 'static'),
			'favicon.png',
			#mimetype='image/vnd.microsoft.icon')
			mimetype='image/png')

@app.route('/nothing')
def nothing():
	"""This static page is just for debug."""
	return render_template('nothing.html')

"""
INDEX
"""

@app.route('/', methods=['GET', 'POST'])
def index():
	#if 'user' not in session:
	#	return redirect('/login')

	return redirect('/nothing')

