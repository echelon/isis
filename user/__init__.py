from flask import Blueprint

mod_user = Blueprint('users', __name__)

import user.views

