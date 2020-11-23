from wtforms import Form, BooleanField, TextField, StringField, PasswordField, SelectField, TextAreaField, validators, DateTimeField, DateField
from wtforms.fields.html5 import DateTimeLocalField

class UserLoginForm(Form):
    username = StringField('user_id', validators=[validators.InputRequired('')])
    password = PasswordField('password', validators=[validators.InputRequired('')])

class AddElectionForm(Form):
    title = StringField('title', validators=[validators.InputRequired('선거 이름을 입력해주세요')])
    desc = StringField('desc', validators=[validators.InputRequired('선거 내용을 입력해주세요')])
    startat = DateTimeLocalField('startat', validators=[validators.InputRequired('시작 시간을 입력해주세요')], format='%Y-%m-%dT%H:%M')
    endat = DateTimeLocalField('endat', validators=[validators.InputRequired('종료 시간을 입력해주세요')], format='%Y-%m-%dT%H:%M')