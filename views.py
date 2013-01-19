"""
ISIS: A Server-Sent Events Chat App.
Copyright 2013 Brand Thomas <bt@brand.io>
"""
from flask import Flask, Response, request, session, \
	redirect, url_for, abort, render_template, flash, \
	send_from_directory

from flask.ext.login import login_user, logout_user

import database

from user import mod_user
from user.forms import *
from user.models import *

"""
REGISTER/LOGIN/LOGOUT
"""

@mod_user.route("/register", methods=['GET', 'POST'])
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

	return render_template('user/register.html',
			form=form,
			error=error)

@mod_user.route("/login", methods=["GET", "POST"])
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

	return render_template('user/login.html',
				form=form,
				error=error)

@mod_user.route('/logout')
def logout():
	logout_user()
	return redirect('/')

"""
USER LIST
"""

@mod_user.route('/') # XXX: Disable if I drop /user/ prefix.
@mod_user.route('/list')
def userlist():
	users = database.session.query(User).all()
	return render_template('user/list.html', users=users)

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

	return render_template('user/profile.html', user=user)

@mod_user.route('/view/<username>')
def user(username):
	return user_profile_view(username=username)

@mod_user.route('/viewid/<uid>')
def userid(uid):
	return user_profile_view(userid=int(uid))

