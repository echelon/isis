import datetime
import hashlib
import random
import string

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import Table, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from flask.ext.login import UserMixin, AnonymousUser

# XXX: 'BASE' configured in 'database' module
from core.database import BASE
from core.models import User

class Teacher(User):
	__mapper_args__ = { 'polymorphic_identity': 'teacher' }

	name_first = Column(String)
	name_last = Column(String)

class StaffIT(User):
	__mapper_args__ = { 'polymorphic_identity': 'staffit' }

	name_first_RENAME = Column(String)
	name_last_RENAME = Column(String)

