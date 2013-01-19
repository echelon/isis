"""
ISIS: A Server-Sent Events Chat App.
Copyright 2013 Brand Thomas <bt@brand.io>
"""

from flask import session
import jinja2

from app import app
from app import login_manager

import database

from model import User

"""
USER
"""

# FIXME: Move to user module??
@login_manager.user_loader
def load_user(uid):
	"""
	Callback loads the User from uid managed by session.
	"""
	print type(uid)
	print "load user %d, %s" % (int(uid), uid)

	user = None
	try:
		user = database.session.query(User) \
			.filter_by(id=int(uid)).one()
	except:
		pass

	print user
	return user

"""
REQUEST PREPROCESSORS
"""

@app.before_request
def before_request():
	pass

@app.teardown_request
def teardown_request(exception):
	pass

#@app.teardown_request
#def shutdown_session(exception=None):
#	pass

"""
CONTEXT PREPROCESSORS, FILTERS, ETC.
"""

@app.context_processor
def inject_something():
	"""
	Insert something into template.
	This is for reference, for when I need it.
	"""
	return dict(something='something')

@app.template_filter('datetime')
def format_datetime(value, format='medium'):
	# This is here for when I need it...
	return value

