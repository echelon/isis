import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import Table, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

# XXX: 'Base' configured in 'database' module
from database import Base

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)

	username = Column(String, nullable=False)
	dtime_create = Column(DateTime, nullable=False,
			default=datetime.datetime.now)

	chats = relationship('Participant')
	lines = relationship('Chatline', backref='user')

	def get_url(self):
		return '/user/%d' % self.id

class Chat(Base):
	__tablename__ = 'chats'
	id = Column(Integer, primary_key=True)

	# Name can be optional identifier for personal use
	name = Column(String)

	dtime_start = Column(DateTime, nullable=False,
			default=datetime.datetime.now)
	dtime_end = Column(DateTime)

	users = relationship('Participant')
	lines = relationship('Chatline', backref='chat')

	def get_url(self):
		return '/chat/%d' % self.id

class Participant(Base):
	__tablename__ = 'participants'

	cid = Column(Integer, ForeignKey('chats.id'),
			primary_key=True)
	uid = Column(Integer, ForeignKey('users.id'),
			primary_key=True)

	dtime_join = Column(DateTime, nullable=False)

class Chatline(Base):
	__tablename__ = 'chatlines'
	id = Column(Integer, primary_key=True)

	cid = Column(Integer, ForeignKey('chats.id'),
			nullable=False)
	uid = Column(Integer, ForeignKey('users.id'),
			nullable=False)

	dtime = Column(DateTime, nullable=False)

	ip = Column(String, nullable=False)
	text = Column(String, nullable=False)

