console.log('chat.js installed');

var main = function() {
	var id = $('#chat').data('id');
	var source = new EventSource('/chat_api/stream/'+id);

	source.onmessage = function(ev) {
		console.log('stream.onmessage()')
		$('#chat').append('<div>' + ev.data + '</div>');
	}

	$('form').submit(function(ev) {
		console.log('form submit');

		var msg = $('#input').val();

		$.post('/chat_api/chat/'+id, {message: msg});
		$('#input').val('');

		ev.preventDefault();
		return false;
	});
}

// Go, go, go!
$(main());
