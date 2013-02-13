// ISIS Chat System
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
					//.appendTo('#attach');
					
		$('#attach').replaceWith(this.$el);

		this.show();

		// Subviews
		var chatwin = new ChatWindowView();
		var input = new InputView();

		this.$el.find('.chatWindowContainer')
			.replaceWith(chatwin.$el);

		this.$el.find('.inputContainer')
			.replaceWith(input.$el);

		this.views.chatWindow = chatwin;
		this.views.input = input;

		// Configure markdown (TODO: Move elsewhere?)
		// TODO: Needs word wrap!!
		marked.setOptions({
			gfm: true,
			pedantic: false,
			tables: false,
			breaks: true,
			smartLists: true,
			sanitize: true,
		});

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


