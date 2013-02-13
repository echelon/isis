"""
ISIS: A Server-Sent Events Chat App.
Copyright 2013 Brand Thomas <bt@brand.io>
"""

from flask import Flask, Response, request, session, \
	redirect, url_for, abort, render_template, flash, \
	send_from_directory, json, jsonify

from flask.ext.login import LoginManager, login_user, \
		logout_user, login_required, current_user, \
		AnonymousUser

import database
from model import *

from chat import mod_chat
from chat.forms import *
from chat.models import *

from core.models import *

from app import rds

@mod_chat.route('/start', methods=['GET', 'POST'])
def start():
	"""
	Person to be helped initiates a new chat.

			!!!!!

	There is no Chat Queue implemented yet in order to
	manage how these users are served. The Chat Queue
	may not even make it into the alpha/MVP.

			!!!!!
	"""
	form = ChatInitForm(request.form)

	# TODO: Really no need to validate
	if form.validate_on_submit():
		chat = Chat(
			issue=form.issue.data
		)

		database.session.add(chat)
		database.session.commit() # Only to get id.

		partip = ChatParticipant(
			cid = chat.id,
			uid = current_user.id
		)

		database.session.add(partip)
		database.session.commit()

		# TODO: Use Json from Chatline.
		rds.publish('newchat',
				json.dumps(chat.serialize(users=False)))


		return redirect(url_for('chat.view', id=chat.id))

	return render_template('chat/initiate.html', form=form)

"""
# TODO: Rename to something epic since this will compose a
# giant ajaxy app.
@mod_chat.route('/view/<id>', methods=['GET', 'POST'])
def view(id):
	chat = None
	try:
		chat = database.session.query(Chat) \
				.filter_by(id=id).one()
	except:
		# FIXME: 404.html **NOT** for API.
		return render_template('404.html'), 404

	# TODO: When permissions exist, disallow users to join
	# chats that they wouldn't be allowed to.

	partip = None
	try:
		partip = database.session.query(ChatParticipant) \
			.filter_by(cid=id, uid=current_user.id).one()
	except:
		pass

	if not partip:
		partip = ChatParticipant(
			cid = chat.id,
			uid = current_user.id
		)

		database.session.add(partip)
		database.session.commit()

	if request.method == 'POST':
		print 'POSTING TO DEPRECATED THING'
		print 'POSTING TO DEPRECATED THING'
		print 'POSTING TO DEPRECATED THING'
		user = session['user']
		msg = request.form['message']

		# TODO: No. 
		now = datetime.datetime.now() \
				.replace(microsecond=0).time()

		rds.publish('chatroom%d'%chat.id,
				'[%s] %s: %s' % (now.isoformat(),
					user, msg))
		return ''

	return render_template('chat/chat.html', chat=chat)
"""

@mod_chat.route('/view/<id>', methods=['GET', 'POST'])
def view(id):
	"""
	Compose the chat view.

	A lot of this will be Ajax, so this won't handle all
	functionality. This brings it all together and handles
	some of the more mundane stuff.
	"""

	chat = None
	try:
		chat = database.session.query(Chat) \
				.filter_by(id=id).one()
	except:
		# FIXME: 404.html **NOT** for API.
		return render_template('404.html'), 404

	# TODO: When permissions exist, disallow users to join
	# chats that they wouldn't be allowed to.

	partip = None
	try:
		partip = database.session.query(ChatParticipant) \
			.filter_by(cid=id, uid=current_user.id).one()
	except:
		pass

	if not partip:
		partip = ChatParticipant(
			cid = chat.id,
			uid = current_user.id
		)

		database.session.add(partip)
		database.session.commit()

	return render_template('chat/chatapp.html', chat=chat)

# TODO: What module does this belong in?
@mod_chat.route('/list')
def list():
	chats = database.session.query(Chat).all()
	return render_template('chat/list.html', chats=chats)

