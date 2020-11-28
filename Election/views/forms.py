from wtforms import Form, StringField, PasswordField, SelectField, FileField, validators
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.fields.simple import SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from models import get_session, Election

class UserLoginForm(Form):
    username = StringField('username', validators=[validators.InputRequired('')])
    password = PasswordField('password', validators=[validators.InputRequired('')])

class UserRegisterForm(Form):
    username = StringField('username', validators=[validators.InputRequired('')])
    password = PasswordField('password', validators=[validators.InputRequired('')])

class ManageElectionForm(Form):
    startbtn = SubmitField(label='시작')
    endbtn = SubmitField(label='종료')

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

def get_elections():
    a = []
    d = get_session().query(Election.id, Election.title)
    print("d : ", d)
    for e in d.all():
        a.append((e[0], e[1]))
    #return Election.query(Election.id, Election.title).all()
    return a

class AddElectionVoterForm(Form):

    #election = QuerySelectField('election',  query_factory=get_elections,  allow_blank=True)
    # election은 알아서 추가
    election = SelectField('election', choices=list(), validators=[validators.InputRequired('')])
    csv_file = FileField('csv_file')
