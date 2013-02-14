// ISIS Chat System
// Copyright 2013 Brandon Thomas

var ChatApp = Backbone.View.extend({
	views: {
		chat: null,
		input: null,
		sidebar: null,
	},

	// Model pointing to the current chat.
	curChat: null,
	curChatId: null,

	initialize: function()
	{
		// FIXME: BAD PLACE FOR THIS!
		window.cid = $('#chatinfo').data('id');
		this.curChatId = window.cid;

		// Static rendering
		this.$el = $('#appView');

		// Configure markdown
		// TODO: Needs word wrap!!
		marked.setOptions({
			gfm: true,
			pedantic: false,
			tables: false,
			breaks: true,
			smartLists: true,
			sanitize: true,
		});

		// Chat model, fetch info
		var chat = new Chat({id: window.cid});
		chat.fetch({
			success: function(m) {
				console.log('Chat Info Fetched');
			}
		});

		var chats = new Chats();

		// Make views
		var chatView = new ChatWindowView();
		var inputView = new InputView();
		var sidebarView = new SidebarView({collection:chats});

		
		// Attach views
		this.$el.find('.chatWindowContainer')
			.html(chatView.$el);

		this.$el.find('.inputContainer')
			.html(inputView.$el);

		this.$el.find('.chatSidebarContainer')
			.html(sidebarView.$el);

		this.views.chat = chatView;
		this.views.input = inputView;
		this.views.sidebar = sidebarView;
	},

});
