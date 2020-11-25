from wtforms import Form, StringField, PasswordField, validators
from wtforms.fields.html5 import DateTimeLocalField

class UserLoginForm(Form):
    username = StringField('user_id', validators=[validators.InputRequired('')])
    password = PasswordField('password', validators=[validators.InputRequired('')])

class AddElectionForm(Form):
    title = StringField('title', validators=[validators.InputRequired()])
    desc = StringField('desc', validators=[validators.InputRequired()])
    startat = DateTimeLocalField('startat', validators=[validators.InputRequired()], format='%Y-%m-%dT%H:%M')
    endat = DateTimeLocalField('endat', validators=[validators.InputRequired()], format='%Y-%m-%dT%H:%M')

class ModifyElectionForm(Form):
    title = StringField('title', validators=[validators.InputRequired()])
    desc = StringField('desc', validators=[validators.InputRequired()])
    startat = DateTimeLocalField('startat', validators=[validators.InputRequired()], format='%Y-%m-%dT%H:%M')
    endat = DateTimeLocalField('endat', validators=[validators.InputRequired()], format='%Y-%m-%dT%H:%M')