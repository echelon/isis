from flask import Blueprint

mod_user = Blueprint('users', __name__,
		template_folder='templates')

import user.views

