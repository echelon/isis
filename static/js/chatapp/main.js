// ISIS Chat System
// Copyright 2013 Brandon Thomas

var ChatApp = Backbone.View.extend({
	initialize: function() {

		// FIXME: BAD PLACE FOR THIS!
		window.cid = $('#chatinfo').data('id');

		// Chat model, fetch info
		var chat = new Chat({id: window.cid});
		chat.fetch({
			success: function(m) {
				console.log('Chat Info Fetched');
			}
		});

		// Setup ChatView ... does all work
		var chatView = new ChatView({model:chat});


		var chats = new Chats();
		var sidebarView = new SidebarView({collection:chats});

		// TODO: Belongs HERE
		chatView.$el.find('.chatSidebarContainer')
			.html(sidebarView.$el);
	},
});
