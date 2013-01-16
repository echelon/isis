from flask import Blueprint

mod_chat = Blueprint('chat', __name__,
		template_folder='templates')

import chat.views

