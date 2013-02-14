// ISIS Chat System
// Copyright 2013 Brandon Thomas

var ChatApp = Backbone.View.extend({
	models: {
		chat: null, // active chat
		chats: null, // collection
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
		var that = this;

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
		this.models.chats = chats;

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

		this.setChat(chat);

		$(window).on('hashchange', function() { 
			that.onHashChange(); 
		});
	},

	onHashChange: function() {
		var getHashNum = function() {
			var m = null;
			if(!location.hash) {
				return;
			}
			m = location.hash.match(/^#?(\d+)/);
			if(!m || m.length < 2) {
				return;
			}
			return parseInt(m[1]);
		}

		var id = getHashNum();
		if(id === undefined) {
			return;
		}

		this.setChat(this.models.chats.get(id));
	},

	// Install a chat window for the current chat.
	setChat: function(chat) {
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
