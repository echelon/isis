"""
ISIS: A Server-Sent Events Chat App.
Copyright 2013 Brand Thomas <bt@brand.io>
"""

import datetime
import hashlib
import random
import string

from sqlalchemy import Column, Integer, String, DateTime,\
						Boolean, Table, Text, ForeignKey

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from flask.ext.login import UserMixin, AnonymousUser

# XXX: 'BASE' configured in 'database' module
from core.database import BASE

class Chat(BASE):
	__tablename__ = 'chats'
	id = Column(Integer, primary_key=True)

	# Optional identifier set by our staff
	title = Column(String(255))

	# Categories (later) for analytics
	#topic = Column(String)

	# An initial, optional user-set issue
	issue = Column(String)

	# Should I cache whom the chat is for?
	#for = Column(String)

	dtime_start = Column(DateTime, nullable=False,
					default=datetime.datetime.now)
	dtime_end = Column(DateTime)

	users = relationship('ChatParticipant')
	lines = relationship('Chatline', backref='chat')

	def get_name(self):
		title = 'Untitled' if not self.title else self.title
		return 'Chat %d: %s' % (self.id, title)

	def get_url(self):
		return '/chat/view/%d' % self.id

class ChatParticipant(BASE):
	__tablename__ = 'chatparticipants'

	cid = Column(Integer, ForeignKey('chats.id'),
			primary_key=True)
	uid = Column(Integer, ForeignKey('users.id'),
			primary_key=True)

	dtime_join = Column(DateTime, nullable=False,
					default=datetime.datetime.now)
	dtime_lsend = Column(DateTime)

class Chatline(BASE):
	__tablename__ = 'chatlines'
	id = Column(Integer, primary_key=True)

	cid = Column(Integer, ForeignKey('chats.id'),
			nullable=False)

	# Note: system is not a user.
	# TODO: Should system be a user in the database?
	uid = Column(Integer, ForeignKey('users.id'))

	# Whether the system sent it.
	sysmessage = Column(Boolean,  default=False)

	dtime = Column(DateTime, nullable=False)

	ip = Column(String, nullable=False)
	text = Column(String, nullable=False)

