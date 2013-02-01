// Copyright 2013 Brandon Thomas
// XXX: uses chatapp.html template!

var ChatlineView = Backbone.View.extend({
	className: 'chatlineView',

	// Models,etc.
	chatlines: null,

	initialize: function() {
		// Static rendering
		this.$el = $('.'+this.className + '.INVISIBLE_TEMPLATE')
		 			.clone()
					.removeClass('INVISIBLE_TEMPLATE');

		this.render();
	},

	render: function() {
		this.$el.find('.name').html(this.model.get('username'));
		this.$el.find('.text').html(this.model.get('text'));
	},
});

var ChatWindowView = Backbone.View.extend({
	className: 'chatWindowView',

	// Models,etc.
	chatlines: null,

	// Views
	chatlineViews: [],

	eventSrc: null,

	initialize: function() {
		var that = this;

		// Models
		this.chatlines = new ChatChatlines({cid: window.cid});

		// Events 
		this.eventSrc = new EventSource('/chat/api/stream/' + 
											window.cid);

		// Static rendering
		this.$el = $('.'+this.className)
		 			.clone()
					.removeClass('INVISIBLE_TEMPLATE');

		// Event bindings
		this.listenTo(this.chatlines, 'add', this.addChatline);

		this.eventSrc.onmessage = function(ev) {
			var line = new Chatline($.parseJSON(ev.data));
			that.chatlines.push(line);
		}

		// Ajax fetch
		this.chatlines.fetch({
			update: true, // Trigger 'add' event
			success: function(m) {
			}
		});
	},

	addChatline: function(model, collection, options) {
		var view = new ChatlineView({model: model});
		this.chatlineViews.push(view);
		this.$el.append(view.$el);

		this.$el.scrollTop(this.$el[0].scrollHeight);
	},

	show: function() {
		this.$el.show();
	},

	hide: function() {
		this.$el.hide();
	},
});

var InputView = Backbone.View.extend({
	className: 'inputView',

	initialize: function() {
		var that = this;

		// Static rendering
		this.$el = $('.'+this.className + '.INVISIBLE_TEMPLATE')
		 			.clone()
					.removeClass('INVISIBLE_TEMPLATE');

		// Event binding
		this.$el.submit(function(ev) {
			ev.preventDefault();
			var input = $(this).find('input.text');
			that.sendMessage(input.val());
			input.val('');
			return false;
		});
	},

	// Send chat text to server
	sendMessage: function(msg) {
		console.log('Sending msg:', msg);
		$.post('/chat/api/chat/'+window.cid, {message: msg});
	},

	show: function() {
		this.$el.show();
	},

	hide: function() {
		this.$el.hide();
	},
});


