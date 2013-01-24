"""
ISIS: A Server-Sent Events Chat App.
Copyright 2013 Brand Thomas <bt@brand.io>
"""

from flask import Blueprint

mod_userext = Blueprint('userext', __name__)

from userext import models
from userext import records

def install():
	print '>>>>> INIT USEREXT RECORDS <<<<<'
	records.insert_key_records()
	records.insert_test_records()

mod_userext.install = install

