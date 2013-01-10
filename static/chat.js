console.log('chat.js installed');

var main = function() {
	var source = new EventSource('/stream');

	source.onmessage = function(ev) {
		$('#chat').append('<div>' + ev.data + '</div>');
	}

	$('form').submit(function(ev) {
		console.log('form submit');

		var msg = $('#input').val();

		$.post('', {message: msg});
		$('#input').val('');

		ev.preventDefault();
		return false;
	});
}

// Go, go, go!
$(main());
