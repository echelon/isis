"""
ISIS: A Server-Sent Events Chat App.
Copyright 2013 Brand Thomas <bt@brand.io>
"""
from flask import Flask, Response, request, session, \
	redirect, url_for, abort, render_template, flash, \
	send_from_directory

import database
from model import *

from chat import mod_chat
from chat.forms import *

"""
CHATS
"""

@mod_chat.route('/list', methods=['GET', 'POST'])
def chats():
	# TODO: FORCE LOGIN STATE 

	# Create a new chatroom
	# TODO: Error handle
	if request.method == 'POST':
		name = request.form['name']

		chat = Chat(name=name)
		database.session.add(chat)
		database.session.commit()

	chats = database.session.query(Chat).all()

	return render_template('chat/list.html', chats=chats)


@mod_chat.route('/view/<id>', methods=['GET', 'POST'])
def chat(id):
	# TODO: FORCE LOGIN STATE 

	chat = None
	try:
		chat = database.session.query(Chat) \
				.filter_by(id=id).one()
	except:
		# FIXME: 404.html **NOT** for API.
		return render_template('404.html'), 404

	if request.method == 'POST':
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


@mod_chat.route('/view/<id>/stream')
def chat_stream(id):

	def event_stream(id):
		pubsub = rds.pubsub()
		pubsub.subscribe('chatroom%d' % id)

		for msg in pubsub.listen():
			return 'data: %s\n\n' % msg['data']

	chat = None
	try:
		chat = database.session.query(Chat) \
				.filter_by(id=id).one()
	except:
		# FIXME: 404.html **NOT** for AJAX API.
		return render_template('chat/404.html'), 404

	return Response(event_stream(chat.id),
			mimetype='text/event-stream')

