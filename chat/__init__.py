"""
ISIS: A Server-Sent Events Chat App.
Copyright 2013 Brand Thomas <bt@brand.io>
"""

from flask import Blueprint

mod_chat = Blueprint('chat', __name__)

from chat import views
from chat import models

