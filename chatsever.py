#!/usr/bin/env python
"""
A Server-Sent Events Chat App.
ISIS (c) Brand Thomas <bt@brand.io>
"""

import os
import time
import random
import datetime

import flask
import redis

from flask import Flask, request, session, g, app, \
	redirect, url_for, abort, render_template, flash, \
	Response

from jinja2 import evalcontextfilter, contextfilter
from jinja2 import environmentfilter

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
	if request.method == 'POST':
		session['user'] = request.form['user']
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


if __name__ == '__main__':
	port = random.randint(5000, 6000)
	print "Running server on port %d" % port

	app.run(host='0.0.0.0',
			port=port,
			debug=True,
			threaded=True)

