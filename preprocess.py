from flask import session
from app import app

import database

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

