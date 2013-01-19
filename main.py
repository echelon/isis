#!/usr/bin/env python
"""
ISIS: A Server-Sent Events Chat App.
Copyright 2013 Brand Thomas <bt@brand.io>
"""

import argparse

"""
APPLICATION COMPONENTS
"""

import database

from app import app
from preprocess import *
from model import *
from views import *

from user import mod_user
from chat import mod_chat

app.register_blueprint(mod_user, url_prefix='/user')
app.register_blueprint(mod_chat, url_prefix='/chat')

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

