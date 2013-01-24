from core.database import session
from .models import *

def insert_key_records():
	pass

def insert_test_records():

	session.add(StaffIT(
			username='staff',
		).set_new_password('staff'))

	session.add(Teacher(
			username='teacher',
		).set_new_password('teacher'))

	session.commit()

