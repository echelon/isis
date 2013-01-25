from flask.ext.wtf import Form, BooleanField, TextField, \
		PasswordField, validators

class ChatInitForm(Form):
    issue = TextField('Issue',
			[validators.Length(min=0, max=2000)])

