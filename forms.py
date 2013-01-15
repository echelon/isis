from flask.ext.wtf import Form, BooleanField, TextField, \
		PasswordField, validators


class RegistrationForm(Form):
    username = TextField('Username',
			[validators.Length(min=2, max=25)])

    email = TextField('Email Address',
			[validators.Length(min=5, max=35)])

    password = PasswordField('New Password',
			[validators.Required(),
				validators.EqualTo('confirm',
					message='Passwords must match')
    ])

    confirm = PasswordField('Repeat Password')

    accept_tos = BooleanField('I accept the TOS',
			[validators.Required()])

class LoginForm(Form):
    username = TextField('Username',
			[validators.Length(min=2, max=25)])

    password = PasswordField('Password',
			[validators.Required()])

