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

	session.add(StaffIT(
			username='brandon',
		).set_new_password('brandon'))

	session.add(StaffIT(
			username='russ',
		).set_new_password('russ'))

	session.add(StaffIT(
			username='ethan',
		).set_new_password('ethan'))

	session.add(StaffIT(
			username='caleb',
		).set_new_password('caleb'))

	session.add(StaffIT(
			username='travis',
		).set_new_password('travis'))

	session.commit()

