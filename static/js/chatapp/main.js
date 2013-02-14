// ISIS Chat System
// Copyright 2013 Brandon Thomas

var ChatApp = Backbone.View.extend({
	models: {
		chat: null, // active chat
	},

	views: {
		chat: null, // active chat window
		input: null,
		sidebar: null,
	},

	// Model pointing to the current chat.
	curChatId: null,

	initialize: function()
	{
		// FIXME: BAD PLACE FOR THIS!
		window.app = this;
		window.cid = $('#chatinfo').data('id');

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

		this.models.chat = chat;

		// Make views
		var sidebarView = new SidebarView({collection:chats});
		var inputView = new InputView();
		
		// Attach views
		this.$el.find('#chatSidebarContainer')
			.html(sidebarView.$el);
		this.$el.find('#inputContainer')
			.html(inputView.$el);

		this.views.sidebar = sidebarView;
		this.views.input = inputView;

		this.setCurChat(chat);
	},

	// Install a chat window for the current chat.
	setCurChat: function(chat) {
		var chatView = null;

		if(this.views.chat) {
			this.views.chat.remove();

			this.$el.find('#chatWindowContainer')
					.children()
					.remove();
			this.$el.find('#chatWindowContainer')
					.empty();
		}
		
		// XXX: Don't create before destroying the last one!
		// The jquery clone will copy both className's !!!
		chatView = new ChatWindowView({model:chat});

		this.$el.find('#chatWindowContainer')
				.html(chatView.$el);

		this.views.chat = chatView;
		this.curChatId = chat.get('id');
	},
});
