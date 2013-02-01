// XXX: uses chatapp.html template!

var ChatlineView = Backbone.View.extend({
});

var ChatWindowView = Backbone.View.extend({
	className: 'chatWindowView',

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


