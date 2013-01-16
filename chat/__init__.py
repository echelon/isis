from flask import Blueprint

mod_chat = Blueprint('chat', __name__)

import chat.views

