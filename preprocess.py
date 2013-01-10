"""
Request and Context Preprocessors.
"""

import flask

from flask import Flask, request, session, \
	redirect, url_for, abort, render_template, flash, \
	Response

from jinja2 import evalcontextfilter, contextfilter
from jinja2 import environmentfilter

from app import app
import database


"""
REQUEST PREPROCESSORS
"""

@app.before_request
def before_request():
	print 'before_request'
	pass

@app.teardown_request
def teardown_request(exception):
	print 'teardown_request'
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



