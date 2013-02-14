// ISIS Chat System
// Copyright 2013 Brandon Thomas
// XXX: uses chatapp.html template!

var ChatWindowView = Backbone.View.extend({
	className: 'chatWindowView',

	// Models,etc.
	model: null, // current chat
	chatlines: null,

	// Views
	chatlineViews: [],

	eventSrc: null,

	initialize: function() {
		var that = this;
		var id = this.model.get('id');

		// Models
		// TODO: reference model.
		this.chatlines = new ChatChatlines({ cid: id });

		// Events 
		this.eventSrc = new EventSource('/chat/api/stream/' + id);

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

		// Ajax fetch chat history
		this.chatlines.fetch({
			update: true, // Trigger 'add' event
			success: function(m) {
				that.$el.find('h1.loading').hide();
			}
		});
	},

	remove: function() {
		this.eventSrc.close();
		this.stopListening();
		this.$el.remove();
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
		var t = this.model.getFormatted();
		this.$el.find('.name').html(this.model.get('username'));
		this.$el.find('.text').html(t);
	},
});
