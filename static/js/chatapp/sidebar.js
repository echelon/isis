// ISIS Chat System
// Copyright 2013 Brandon Thomas

var SidebarView = Backbone.View.extend({
	className: 'sidebarView',

	// TODO: Why both?
	collection: null,
	sidebarViews: [],

	events: {
	},

	initialize: function() {
		var that = this;

		// Static rendering
		this.$el = $('.'+this.className + '.INVISIBLE_TEMPLATE')
		 			.clone()
					.removeClass('INVISIBLE_TEMPLATE');

		//this.listenTo(this.collection, 'add', this.test);

		// XXX: Something is wrong with collection Ajax API
		this.collection.fetch({
			success: function() {
				that._addViews();
			}
		});
	},

	// Add views for each chat.
	_addViews: function() {
		var that = this;
		this.$el.html('');

		this.collection.each(function(chat) {
			var v = new SidebarChatView({model:chat});
			that.sidebarViews.push(v);

			that.$el.append(v.$el);
		});
	},

	render: function() {
	},

	show: function() { 
		this.$el.show();
	},

	hide: function() {
		this.$el.hide();
	},
});


var SidebarChatView = Backbone.View.extend({

	className: 'sidebarChatView',
	model: null,

	events: {
		'click': 'onClick',
	},

	initialize: function() {
		// Static rendering
		this.$el = $('.'+this.className + '.INVISIBLE_TEMPLATE')
		 			.clone()
					.removeClass('INVISIBLE_TEMPLATE');

		this.render();
	},

	onClick: function() {
		console.log(this.model.appUrl());
		return false;
	},

	render: function() {
		console.log('render XYZ');
		this.$el.find('.name')
			.html(
				'<a href="' +
					this.model.appUrl() +
				'">'+
					this.model.getName() +
				'</a>'
			);
	},

	show: function() { 
		this.$el.show();
	},

	hide: function() {
		this.$el.hide();
	},
});
