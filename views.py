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

from flask.ext.login import login_user

"""
DEFAULT VIEWS
"""

@app.errorhandler(404)
def not_found(e):
	return render_template('404.html'), 404

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
			os.path.join(app.root_path, 'static'),
			'favicon.png',
			#mimetype='image/vnd.microsoft.icon')
			mimetype='image/png')

"""
INDEX
"""

@app.route('/', methods=['GET', 'POST'])
def index():
	#if 'user' not in session:
	#	return redirect('/login')

	return redirect('/chats')

"""
LOGIN/LOGOUT
"""

@app.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm(request.form)
	user = None
	error = None
	if form.validate_on_submit():
		username = form.username.data
		try:
			user = database.session.query(User) \
				.filter_by(username=username).one()

			if user.check_password(form.password.data):
				# login and validate the user...
				login_user(user)
				flash("Logged in successfully.")
				#return redirect(request.args.get("next") or \
				#		url_for("index"))

				return redirect('/about')

		except:
			error = 'Username and/or password wrong.'

	return render_template("login2.html",
				form=form,
				error=error)


@app.route('/loginOLD', methods=['GET', 'POST'])
def loginOLD():
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

	# Create a new chatroom
	# TODO: Error handle
	if request.method == 'POST':
		name = request.form['name']

		chat = Chat(name=name)
		database.session.add(chat)
		database.session.commit()

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

		rds.publish('chatroom%d'%chat.id,
				'[%s] %s: %s' % (now.isoformat(),
					user, msg))
		return ''

	return render_template('chat.html', chat=chat)


@app.route('/chat/<id>/stream')
def chat_stream(id):

	def event_stream(id):
		pubsub = rds.pubsub()
		pubsub.subscribe('chatroom%d' % id)

		for msg in pubsub.listen():
			return 'data: %s\n\n' % msg['data']

	chat = None
	try:
		chat = database.session.query(Chat) \
				.filter_by(id=id).one()
	except:
		# FIXME: 404.html **NOT** for AJAX API.
		return render_template('404.html'), 404

	return Response(event_stream(chat.id),
			mimetype='text/event-stream')

