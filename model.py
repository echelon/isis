import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import Table, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

# XXX: 'Base' configured in 'database' module
from database import Base

Participant = Table('participants',
	Base.metadata,
	Column('uid', Integer, ForeignKey('users.id')),
	Column('cid', Integer, ForeignKey('chats.id')),
	Column('dtime_join', DateTime, nullable=False)
)

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)

	username = Column(String, nullable=False)
	dtime_create = Column(DateTime, nullable=False,
			default=datetime.datetime.now)

	chats = relationship('Chat', secondary=Participant,
			backref='users')

	lines = relationship('Chatline', backref='user')

class Chat(Base):
	__tablename__ = 'chats'
	id = Column(Integer, primary_key=True)

	dtime_start = Column(DateTime, nullable=False,
			default=datetime.datetime.now)
	dtime_end = Column(DateTime)

	# Already exists -- 
	#users = relationship('User', secondary=Participant,
	#		backref='chats')

	lines = relationship('Chatline', backref='chat')

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

