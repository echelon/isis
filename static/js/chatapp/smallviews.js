// Copyright 2013 Brandon Thomas
// XXX: uses chatapp.html template!

var ChatlineView = Backbone.View.extend({
	className: 'chatlineView',

	// Models,etc.
	chatlines: null,

	initialize: function() {
		console.log('INIT');
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

	initialize: function() {
		var that = this;

		// Models
		this.chatlines = new ChatChatlines({cid: window.cid});

		// Static rendering
		this.$el = $('.'+this.className)
		 			.clone()
					.removeClass('INVISIBLE_TEMPLATE');

		// Event bindings
		this.listenTo(this.chatlines, 'add', this.addChatline);

		// Ajax fetch
		this.chatlines.fetch({
			update: true,
			success: function(m) {
				console.log('Chatline history recvd');
			}
		});
	},

	addChatline: function(model, collection, options) {
		console.log('Add Chatline');
		var view = new ChatlineView({model: model});
		this.chatlineViews.push(view);
		console.log('Appending view.$el for chatline');
		console.log(view.$el);
		this.$el.append(view.$el);
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
		// Static rendering
		this.$el = $('.'+this.className)
		 			.clone()
					.removeClass('INVISIBLE_TEMPLATE');
	},

	show: function() {
		this.$el.show();
	},

	hide: function() {
		this.$el.hide();
	},
});


