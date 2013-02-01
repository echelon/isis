// XXX: No 'views' in models! BAD FORM.
// Models can have multiple views.

/**
 * Chat
 */

var Chat = Backbone.Model.extend({
	urlRoot: '/chat_api/chat',
	defaults: {
		id: null,
		title: '',
		issue: '', 
		dtime_start: 0,
		dtime_end: 0,
		//participants: [],
		//lines: [], // Chatlines
	},

	getName: function() {
		var t = this.get('title'),
			n = t ? t : 'Untitled';
		return 'Chat ' + this.get('id') + ': ' + t;
	},
});

var Chats = Backbone.Collection.extend({
	model: Chat,
	url: '/chat_api/chat',
});


/**
 * Chatline
 */

var Chatline = Backbone.Model.extend({
	defaults: {
		id: null,
		cid: null,
		uid: null,
		is_sys_msg: false,
		dtime: 0,
		ip: '',
		text: '',
		// user: null, 
	},
});

/**
 * User / Participant
 */
var Participant = Backbone.Model.extend({
	defaults: {
		cid: null,
		uid: null,
		dtime_join: 0,
		dtime_lsend: 0,
		// user: null, 
	},
});

