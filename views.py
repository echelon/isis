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

"""
REGISTER/LOGIN/LOGOUT
"""

@app.route("/register", methods=['GET', 'POST'])
def register():
	"""
	Register a new user account.
	"""
	form = RegisterForm(request.form)
	user = None
	error = None
	if form.validate_on_submit():
		user = User(
			username=form.username.data,
			email=form.email.data
		)
		user.set_new_password(form.password.data)

		database.session.add(user)
		database.session.commit()

		login_user(user)
		flash("Logged in successfully.")

		return redirect('/nothing')

		error = 'There was an error creating the account.'

	return render_template('register.html',
			form=form,
			error=error)

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
				print "logging in..."

				login_user(user)
				flash("Logged in successfully.")

				#return redirect(request.args.get("next") or \
				#		url_for("index"))

				user.dtime_llogin = datetime.datetime.now()
				database.session.commit()

				return redirect('/nothing')

		except:
			error = 'Username and/or password wrong.'

	return render_template("login.html",
				form=form,
				error=error)

@app.route('/logout')
def logout():
	logout_user()
	return redirect('/')

"""
PROFILES
"""

def user_profile_view(username=None, userid=None):
	"""
	Construct a profile view from either username or userid.
	"""
	user = None
	if username == 'Anonymous' or userid == -1:
		user = Anonymous()
	else:
		try:
			if username:
				user = database.session.query(User) \
					.filter_by(username=username).one()

			elif userid != None:
				user = database.session.query(User) \
					.filter_by(id=userid).one()
		except:
			return render_template('404.html'), 404

	return render_template('profile.html', user=user)


@app.route('/user/<username>')
def user(username):
	return user_profile_view(username=username)

@app.route('/userid/<uid>')
def userid(uid):
	return user_profile_view(userid=int(uid))

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

