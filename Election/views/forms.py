from wtforms import Form, BooleanField, TextField, StringField, PasswordField, SelectField, TextAreaField, validators

class UserLoginForm(Form):
    username = StringField('user_id', validators=[validators.InputRequired('')])
    password = PasswordField('password', validators=[validators.InputRequired('')])

