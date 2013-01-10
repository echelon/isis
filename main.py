#!/usr/bin/env python
"""
A Server-Sent Events Chat App.
ISIS (c) Brand Thomas <bt@brand.io>
"""

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

"""
GLOBALS
"""

from app import app
from preprocess import *
from views import *

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

