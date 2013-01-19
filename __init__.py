"""
ISIS: A Server-Sent Events Chat App.
Copyright 2013 Brand Thomas <bt@brand.io>
"""

from flask import Blueprint

mod_user = Blueprint('users', __name__,
		template_folder='./templates')

import user.views
import user.models
