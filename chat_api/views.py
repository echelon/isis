"""
ISIS: A Server-Sent Events Chat App.
Copyright 2013 Brand Thomas <bt@brand.io>
"""

from flask import Flask, Response, request, session, \
	redirect, url_for, abort, render_template, flash, \
	send_from_directory, json, jsonify #, stream_with_context

from flask.ext.login import LoginManager, login_user, \
		logout_user, login_required, current_user, \
		AnonymousUser

import database
from model import *

from chat_api import mod_chat_api
from chat.forms import *
from chat.models import *
from core.models import *

from app import rds

# XXX: Index will get out of date when coding...
@mod_chat_api.route('/')
def index():
	"""Documentation of API features"""
	return jsonify(
			README='API features (perhaps out of date).',
			uris = {
				'/chats': 'List of all chatrooms',
				'/chat/<id>': 'POST messages to chat',
				'/messages/<id>': 'List of all messages said',
				'/participants/<id>': 'List all users in room',
				'/stream/<id>': 'Stream REDIS chatlines',
			}
		)

@mod_chat_api.route('/chat/<id>', methods=['GET', 'POST'])
def chat(id):
	"""Post messages to the chat"""
	# TODO: Permissions -- don't let anyone join any chat
	# TODO: API ERROR HANDLING
	print '/chat_api/chat/id'
	print id
	user = current_user
	chat = None
	try:
		chat = database.session.query(Chat) \
				.filter_by(id=id).one()
	except:
		print '>> chat DNE'
		return '404'

	if request.method == 'POST':
		try:
			msg = request.form['message']
			line = Chatline(
				cid = chat.id,
				uid = user.id,
				text = msg,
				ip = request.remote_addr
			)
			database.session.add(line)
			database.session.commit()
			print '>> chatline added'

			# TODO: No. Yucky. 
			now = datetime.datetime.now() \
					.replace(microsecond=0).time()

			# TODO: Use Json from Chatline.
			rds.publish('chatroom%d'%chat.id,
					'[%s] %s: %s' % (now.isoformat(),
						user.username, msg))

			print '>> redis published'
			return 'OK'
		except:
			print '>> fail to add chatline'
			return 'FAIL'

	print chat
	#lines = database.session.query(Chatline).all()
	#return jsonify(lines = [x.serialize() for x in chats])
	return jsonify(chat.serialize())

@mod_chat_api.route('/chat_chatlines/<id>')
def chat_chatlines(id):
	"""All messages in a chatroom"""
	chat = None
	try:
		chat = database.session.query(Chat) \
				.filter_by(id=id).one()
	except:
		return '404'

	lines = database.session.query(Chatline) \
				.filter_by(cid=id).all()

	# TODO: Return mimetype not same as with jsonify
	return json.dumps([x.serialize() for x in lines])

@mod_chat_api.route('/chats')
def chats():
	"""List of all chatrooms"""
	chats = database.session.query(Chat).all()
	return jsonify(chats = [x.serialize() for x in chats])

@mod_chat_api.route('/messages/<id>')
def messages(id):
	"""All messages in a chatroom"""
	# TODO: Permissions -- don't let anyone join any chat
	# TODO: API ERROR HANDLING

	chat = None
	try:
		chat = database.session.query(Chat) \
				.filter_by(id=id).one()
	except:
		return '404'

	lines = database.session.query(Chatline) \
				.filter_by(cid=id).all()
	return jsonify(lines = [x.serialize() for x in lines])

@mod_chat_api.route('/participants/<id>')
def participants(id):
	"""All participants in a chatroom"""
	chat = None
	try:
		chat = database.session.query(Chat) \
				.filter_by(id=id).one()
	except:
		return '404'

	users = database.session.query(ChatParticipant) \
				.filter_by(cid=id).all()
	return jsonify(users = [x.serialize() for x in users])

@mod_chat_api.route('/stream/<id>')
def stream(id):
	"""Stream messages from a chatroom"""
	# TODO: Check out :
	# http://flask.pocoo.org/docs/api/#stream-helpers
	#@stream_with_context
	# TODO: Upgrade Flask to 0.9 for context
	def event_stream(id):
		pubsub = rds.pubsub()
		pubsub.subscribe('chatroom%d' % id)

		for msg in pubsub.listen():
			print '>> event streamed'
			yield 'data: %s\n\n' % msg['data']

	chat = None
	try:
		chat = database.session.query(Chat) \
				.filter_by(id=id).one()
	except:
		return 'FAIL'

	return Response(event_stream(chat.id),
			mimetype='text/event-stream')

