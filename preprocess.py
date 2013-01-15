from flask import session

from app import app
from app import login_manager

import database

"""
USER
"""

@login_manager.user_loader
def load_user(uid):
	"""
	Callback loads the User from uid managed by session.
	"""
	print "load user"
    #return User.get(uid)
	if not True:
		return None


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
CONTEXT PREPROCESSORS
"""

@app.context_processor
def inject_user():
	"""Insert username into templates."""
	user = session['user'] if 'user' in session else None
	return dict(username=user)

