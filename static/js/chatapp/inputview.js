// ISIS Chat System
// Copyright 2013 Brandon Thomas

/**
 * InputView
 * The input box allows for single or multiline entry.
 * With ctrl+enter, newlines are entered and the <input>
 * becomes a <textarea> !
 */
var InputView = Backbone.View.extend({
	className: 'inputView',

	events: {
		'keypress': 'onKeypress',
		'submit': 'onSubmit',
	},

	TEXTAREA_MAX_HEIGHT: 110,

	initialize: function() {
		var that = this;

		// Static rendering
		this.$el = $('.'+this.className + '.INVISIBLE_TEMPLATE')
		 			.clone()
					.removeClass('INVISIBLE_TEMPLATE');

		this.setInputState('input', '');
	},

	onSubmit: function(ev) {
		var val = '';
		ev.preventDefault();
		val = this.getVal()
				.replace(/^\s\s*/, '')
				.replace(/\s\s*$/, '');
		if(val) {
			this.sendMessage(val);
		}
		this.setInputState('input', '');
		return false;
	},

	// Enable long input
	onKeypress: function(ev) {
		// From Stack Overflow
		// http://stackoverflow.com/a/6014917
		// TODO: Turn into jQuery extension?
		var getCaret = function(el) {
			if(el.selectionStart) {
				return el.selectionStart;
			}
			else if(document.selection) {
				el.focus();
				var r = document.selection.createRange();
				if (r == null) {
					return 0;
				}
				var re = el.createTextRange(),
				rc = re.duplicate();
				re.moveToBookmark(r.getBookmark());
				rc.setEndPoint('EndToStart', re);
				return rc.text.length;
			}  
			return 0;
		};

		// From Stack Overflow
		// http://stackoverflow.com/a/3651232
		// TODO: Turn into jQuery extension, as in url.
		// TODO: Actually, make *ONE* jQuery extension:
		// $.caret() to get, and $.caret(pos) to set.
		var setCaret = function(el, pos) {
			el.each(function(index, elem) {
				if (elem.setSelectionRange) {
					elem.setSelectionRange(pos, pos);
				} else if (elem.createTextRange) {
					var range = elem.createTextRange();
					range.collapse(true);
					range.moveEnd('character', pos);
					range.moveStart('character', pos);
					range.select();
				}
			});
			return this;
		};

		var state = this.getInputState(),
			pos = 0,
			val = '',
			el = null;

		// Ctrl+Enter => Linebreak and switch mode!
		// Note: Shift and Alt are also mode keys accepted.
		if(( ev.ctrlKey || ev.shiftKey || ev.altKey ) && 
				(ev.which === 13)) {
			val = this.getVal();
			switch(state) {
				case 'textarea':
					el = this.$el.find('textarea');
					break;
				case 'input':
				default:
					el = this.$el.find('input.text');
					break;
			}

			pos = getCaret(el[0]);
			val = val.substring(0, pos) + 
				  '\n' + 
				  val.substring(pos, val.length);
			
			if(state === 'input') {
				this.setInputState('textarea', val);
				el = this.$el.find('textarea');
			}
			else {
				this.setVal(val);
			}
			
			setCaret(el, pos+1);

			if(state === 'textarea') {
				el.css('height', Math.min(el[0].scrollHeight, 
									this.TEXTAREA_MAX_HEIGHT));
			}

			ev.preventDefault(); // Don't submit form!
		}
		else if(ev.which === 13 && state === 'textarea') {
			// Submit textareas on <Enter>
			this.doSubmit();
		}
	}, 

	// Get the current value of the textbox, regardless of state
	getVal: function() {
		switch(this.getInputState()) {
			case 'textarea':
				return this.$el.find('textarea').val();
			case 'input':
			default:
				return this.$el.find('input.text').val();
		}
	},

	// Set the value of the textbox, regardless of state/type
	setVal: function(val) {
		switch(this.getInputState()) {
			case 'textarea':
				this.$el.find('textarea').val(val);
				return;
			case 'input':
			default:
				this.$el.find('input.text').val(val);
				return;
		}
	},

	// Get the current input type state
	getInputState: function() {
		if(this.$el.find('textarea').filter(':hidden').length) {
			return 'input';
		}
		return 'textarea';
	},

	// Set the current state, and optionally a value
	// val: string to input
	// focus: bool to gain focus
	setInputState: function(type, val, focus) {
		switch(type) {
			case 'textarea':
				this.$el.find('input.text').hide();
				this.$el.find('textarea')
					.show()
					.val(val)
					.focus()
					.css('height', ''); // Reset from resize
				return;
			case 'input':
			default:
				this.$el.find('textarea').hide();
				this.$el.find('input.text')
					.show()
					.val(val)
					.focus();
				return;
		}
		this.setVal(val);
	},

	// Send chat text to server
	sendMessage: function(msg) {
		var id = window.app.curChatId;
		// TODO: Needs word wrap!!
		console.log(id);
		$.post('/chat/api/chat/'+id, {message: msg});
	},

	// Force DOM to send form
	doSubmit: function() {
		this.$el.find('form').submit();
	},

	show: function() {
		this.$el.show();
	},

	hide: function() {
		this.$el.hide();
	},
});

