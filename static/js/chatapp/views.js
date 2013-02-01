// Copyright 2013 Brandon Thomas
// XXX: uses chatapp.html template!

var ChatView = Backbone.View.extend({
	className: 'chatView',

	// Subviews 
	views: {
		chatWindow: null,
		input: null,
	},

	// Models, etc.
	model: null,
	
	initialize: function() {
		var that = this;

		// Static render
		this.$el = $('.'+this.className + '.INVISIBLE_TEMPLATE')
		 			.clone()
					.removeClass('INVISIBLE_TEMPLATE')
					.appendTo('#attach');

		this.show();

		// Subviews
		var chatwin = new ChatWindowView();
		var input = new InputView();

		this.$el.find('.chatWindowContainer')
			.html(chatwin.$el);

		this.$el.find('.inputContainer')
			.html(input.$el);

		this.views.chatWindow = chatwin;
		this.views.input = input;

		// Events
		this.listenTo(this.model, 'change', this.render);
	},

	render: function() {
		// TODO
		this.$el.find('.chatName').html(this.model.getName());
	},

	show: function() { 
		this.$el.show();
	},

	hide: function() {
		this.$el.hide();
	},
});

var ChatApp = Backbone.View.extend({
	initialize: function() {

		// FIXME: BAD PLACE FOR THIS!
		window.cid = $('#chatinfo').data('id');

		var chat = new Chat({id: window.cid});

		// Get Chat Info
		chat.fetch({
			success: function(m) {
				console.log('Chat Info Fetched');
			}
		});

		

		// Setup Views
		var chatView = new ChatView({model:chat});
	},
});

