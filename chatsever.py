#!/usr/bin/env python
"""
A Server-Sent Events Chat App.
ISIS (c) Brand Thomas <bt@brand.io>
"""

import os
import sys
import time
import random
import argparse
import datetime

import flask
import redis

from flask import Flask, request, session, g, app, \
	redirect, url_for, abort, render_template, flash, \
	Response

from jinja2 import evalcontextfilter, contextfilter
from jinja2 import environmentfilter

import database
from model import *

"""
CONFIGURATION
"""

DEBUG = True
SECRET_KEY = 'not a secret'

"""
GLOBALS
"""

app = Flask(__name__)
app.config.from_object(__name__)

rds = redis.Redis()

"""
REQUEST PREPROCESSORS
"""

@app.before_request
def before_request():
	pass

@app.teardown_request
def teardown_request(exception):
	pass

@app.teardown_request
def shutdown_session(exception=None):
	pass

"""
BROWSER GATEWAY
"""

@app.errorhandler(404)
def not_found(e):
	return render_template('404.html'), 404

@app.route('/', methods=['GET', 'POST'])
def index():
	if 'user' not in session:
		return redirect('/login')

	return redirect('/chat')

@app.route('/login', methods=['GET', 'POST'])
def login():
	def user_sync(username):
		"""Make or query a user. Temporary."""
		user = None

		try:
			user = database.session.query(User) \
				.filter_by(username=username).one()
		except:
			user = User(
				username=username
			)
			database.session.add(user)
			database.session.commit()

		return user

	if request.method == 'POST':
		username = request.form['user']

		user_sync(username)

		session['user'] = username

		return redirect('/chat')

	return render_template('login.html')

@app.route('/logout')
def logout():
	del session['user']
	return redirect('/')

@app.route('/chat')
def chat():
	if 'user' not in session:
		return redirect('/')

	return render_template('chat.html',
			user=session['user'])

@app.route('/initdb')
def initdb():
	database.init_db()
	return 'Database installed'

"""
AJAX GATEWAY
"""

@app.route('/send', methods=['POST'])
def send():
	user = session['user']
	msg = request.form['message']

	# TODO: No. 
	now = datetime.datetime.now().replace(microsecond=0).time()

	rds.publish('chatroom', '[%s] %s: %s' % (now.isoformat(), user, msg))

	return ''


@app.route('/stream')
def stream():

	def event_stream():
		pubsub = rds.pubsub()
		pubsub.subscribe('chatroom')
		for msg in pubsub.listen():
			return 'data: %s\n\n' % msg['data']

	return Response(event_stream(),
			mimetype='text/event-stream')

"""
COMMANDLINE / MAIN
"""

def get_args():
	"""
	Install and parse commandline arguments.
	"""
	parser = argparse.ArgumentParser(
			description='Chat Server.')

	parser.add_argument('port',
			nargs='?',
			default=5000,
			type=int, help='Port number')

	parser.add_argument('--reinstall',
			action='store_const', const=True,
			default=False,
			help='Drop and reset database')

	return parser.parse_args()

def main():
	args = get_args()

	if args.reinstall:
		print "Reinstalling database"
		database.drop_db()
		database.init_db()

	port = args.port

	print "Running server on port %d" % port

	app.run(host='0.0.0.0',
			port=port,
			debug=True,
			threaded=True)

if __name__ == '__main__':
	main()

