import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

"""
DB configuration.
"""

DATABASE_FILE = 'sqlite.db'

engine = create_engine('sqlite:///%s' % DATABASE_FILE, convert_unicode=True)

session = scoped_session(sessionmaker(autocommit=False,
	autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

"""
Helper functions to create and drop database.
"""

def drop_db():
	os.remove(DATABASE_FILE) # XXX: Careful!

def init_db():
	import model
	Base.metadata.create_all(bind=engine)

	# Default records.
	session.add(model.Chat(name='Default Chatroom.'))

	session.add(model.User(
		username='admin',
		passsalt='NONE',
		passhash=model.User.hash_password('admin', 'NONE')
	))

	session.add(model.User(
		username='joe',
		passsalt='NONE',
		passhash=model.User.hash_password('joe', 'NONE')
	))
	session.add(model.User(
			username='bill'
		).set_new_password('bill'))

	session.commit()

