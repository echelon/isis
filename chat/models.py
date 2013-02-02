"""
ISIS: A Server-Sent Events Chat App.
Copyright 2013 Brand Thomas <bt@brand.io>
"""

import datetime
import hashlib
import random
import string
import json

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

	participants = relationship('ChatParticipant')
	lines = relationship('Chatline', backref='chat')

	def get_name(self):
		title = 'Untitled' if not self.title else self.title
		return 'Chat %d: %s' % (self.id, title)

	def get_url(self):
		return '/chat/view/%d' % self.id

	def to_json(self):
		return json.dumps({
			'title': self.title,
			'issue': self.issue,
			'users': None
		})

	def serialize(self, users=True):
		if not users:
			return {
				'id': self.id,
				'title': self.title,
				'issue': self.issue,
			}

		users = []
		for p in self.participants:
			users.append({
				'id': p.user.id,
				'username': p.user.username,
			})

		return {
			'id': self.id,
			'title': self.title,
			'issue': self.issue,
			'users': users
		}

class ChatParticipant(BASE):
	__tablename__ = 'chatparticipants'

	cid = Column(Integer, ForeignKey('chats.id'),
			primary_key=True)
	uid = Column(Integer, ForeignKey('users.id'),
			primary_key=True)

	dtime_join = Column(DateTime, nullable=False,
					default=datetime.datetime.now)
	dtime_lsend = Column(DateTime)

	user = relationship('User')

	def serialize(self):
		return {
			'uid': self.uid,
			'username': self.user.username,
		}

class Chatline(BASE):
	__tablename__ = 'chatlines'
	id = Column(Integer, primary_key=True)

	cid = Column(Integer, ForeignKey('chats.id'),
			nullable=False)

	# Note: system is not a user.
	# TODO: Should system be a user in the database?
	uid = Column(Integer, ForeignKey('users.id'))

	# Whether the system sent it.
	is_sys_msg = Column(Boolean, default=False)

	dtime = Column(DateTime, nullable=False,
				default=datetime.datetime.now)

	ip = Column(String)
	text = Column(String, nullable=False)
	is_markdown = Column(Boolean, default=False)

	user = relationship('User')

	def serialize(self, users=True):
		if not users:
			return {
				'id': self.id,
				'cid': self.cid,
				'uid': self.uid,
				'is_sys_msg': self.is_sys_msg,
				'ip': self.ip,
				'text': self.text,
				'is_markdown': self.is_markdown,
			}
		return {
			'id': self.id,
			'cid': self.cid,
			'uid': self.uid,
			'is_sys_msg': self.is_sys_msg,
			'ip': self.ip,
			'text': self.text,
			'is_markdown': self.is_markdown,
			'username': self.user.username,
		}

