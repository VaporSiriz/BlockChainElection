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
    img_file = FileField('img_file')
    startat = DateTimeLocalField('startat', validators=[validators.InputRequired()], format='%Y-%m-%dT%H:%M')
    endat = DateTimeLocalField('endat', validators=[validators.InputRequired()], format='%Y-%m-%dT%H:%M')

class ModifyElectionForm(Form):
    title = StringField('title', validators=[validators.InputRequired()])
    desc = StringField('desc', validators=[validators.InputRequired()])
    startat = DateTimeLocalField('startat', validators=[validators.InputRequired()], format='%Y-%m-%dT%H:%M')
    endat = DateTimeLocalField('endat', validators=[validators.InputRequired()], format='%Y-%m-%dT%H:%M')

class AddElectionVoterForm(Form):
    election = SelectField('election', choices=list(), validators=[validators.InputRequired('')])
    csv_file = FileField('csv_file')

class AddCandidateForm(Form):
    name = StringField('name', validators=[validators.InputRequired()])
    candidate_id = StringField('candidate_id', validators=[validators.InputRequired()])
    candidate_img = FileField('candidate_img')
    pledge = FileField('pledge')
    career = FileField('career')
    profile_sub1 = FileField('candidate_img')
    profile_sub2 = FileField('candidate_img')
    profile_sub3 = FileField('candidate_img')
    extra_img = FileField('extra_img')
    extra = StringField('extra', validators=[validators.InputRequired()])

class ModifyCandidateForm(Form):
    name = StringField('name', validators=[validators.InputRequired()])
    candidate_id = StringField('candidate_id', validators=[validators.InputRequired()])
    candidate_img = FileField('candidate_img')
    pledge = FileField('pledge')
    career = FileField('career')
    profile_sub1 = FileField('candidate_img')
    profile_sub2 = FileField('candidate_img')
    profile_sub3 = FileField('candidate_img')
    extra_img = FileField('extra_img')
    extra = StringField('extra', validators=[validators.InputRequired()])

    def fill(self, candidate):
        self.name.data = candidate.name
        self.candidate_id.data = candidate.candidate_id
        self.candidate_img.data = candidate.candidate_img
        self.pledge.data = candidate.pledge
        self.career.data = candidate.career
        self.profile_sub1.data = candidate.profile_sub1
        self.profile_sub2.data = candidate.profile_sub2
        self.profile_sub3.data = candidate.profile_sub3
        self.extra_img.data = candidate.extra_img
        self.extra.data = candidate.extra