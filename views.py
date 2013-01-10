import os
import sys
import time
import random
import argparse
import datetime

import flask
import redis

from flask import Flask, request, session, app, \
	redirect, url_for, abort, render_template, flash, \
	Response

from jinja2 import evalcontextfilter, contextfilter
from jinja2 import environmentfilter

import database
from model import *

from app import app
from app import rds

"""
DEFAULT VIEWS
"""

@app.errorhandler(404)
def not_found(e):
	return render_template('404.html'), 404

"""
AJAX GATEWAY
"""

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
INDEX
"""

@app.route('/', methods=['GET', 'POST'])
def index():
	if 'user' not in session:
		return redirect('/login')

	return redirect('/chats')

"""
LOGIN/LOGOUT
"""

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

		return redirect('/chats')

	return render_template('login.html')

@app.route('/logout')
def logout():
	del session['user']
	return redirect('/')

"""
CHATS
"""

@app.route('/chats', methods=['GET', 'POST'])
def chats():
	if 'user' not in session:
		return redirect('/')

	chats = database.session.query(Chat).all()

	return render_template('chats.html', chats=chats)


@app.route('/chat/<id>', methods=['GET', 'POST'])
def chat(id):
	if 'user' not in session:
		return redirect('/')

	chat = None
	try:
		chat = database.session.query(Chat) \
				.filter_by(id=id).one()
	except:
		# FIXME: 404.html **NOT** for API.
		return render_template('404.html'), 404

	if request.method == 'POST':
		user = session['user']
		msg = request.form['message']

		# TODO: No. 
		now = datetime.datetime.now() \
				.replace(microsecond=0).time()

		rds.publish('chatroom',
				'[%s] %s: %s' % (now.isoformat(),
					user, msg))
		return ''

	return render_template('chat.html', chat=chat)

