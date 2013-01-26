"""
ISIS: A Server-Sent Events Chat App.
Copyright 2013 Brand Thomas <bt@brand.io>
"""

from flask import Blueprint

mod_chat_api = Blueprint('chat_api', __name__)

from chat_api import views

