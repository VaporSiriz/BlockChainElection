from wtforms import Form, BooleanField, TextField, StringField, PasswordField, SelectField, TextAreaField, validators, DateTimeField, DateField
from wtforms.fields.html5 import DateTimeLocalField

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class UserLoginForm(Form):
    username = StringField('user_id', validators=[validators.InputRequired('')])
    password = PasswordField('password', validators=[validators.InputRequired('')])

class AddElectionForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    desc = StringField('desc', validators=[DataRequired()])
    startat = DateTimeLocalField('startat', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    endat = DateTimeLocalField('endat', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')