
var ItemView = Backbone.View.extend({
	model: null,

	tagName: 'div',
	className: 'thingyView',

	events: {
		'click img': 'launchModal',
		'click button': 'toggleCart',
	},

	// XXX: model must be set
	initialize: function() {
		// Static render.
		this.$el.html('<div class="thingy">' +
				'<img src="' + 
					this.model.get('img') + 
				'">' +
				'<div class="btns">'+ 
					'<button class="btn btn-primary addCart ">' +
					'Add ' +
					this.model.get('title') +
					'</button>' +
				'</div></div>');

		this.model.on('change:added', this.render, this);
	},

	render: function() {
		var src = null,
			btn = null,
			text = '';

		if(this.model.get('added')) {
			src = this.model.get('imgAdded');
			text = 'Remove ' + this.model.get('title');
		}
		else {
			src = this.model.get('img');
			text = 'Add ' + this.model.get('title');
		}

		this.$el.find('img').attr('src', src);
		this.$el.find('button').html(text);

		// FIXME -- why do I have to do this!?
		this.delegateEvents();
	},

	toggleCart: function() {
		this.model.set('added', !this.model.get('added'));
	},

	launchModal: function() {
		this.model.modalView.show();
	},

	show: function() {
		// XXX: show()/hide() mess up re-rendering in this case.
		this.$el.css('display', 'inline-block');
	},

	hide: function() {
		// XXX: show()/hide() mess up re-rendering in this case.
		this.$el.css('display', 'none');
	},
});





