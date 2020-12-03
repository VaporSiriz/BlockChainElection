from flask import Blueprint, render_template, make_response, flash, request, redirect, \
                  url_for, session
from flask_login import login_user, logout_user, current_user, login_required
from .forms import UserRegisterForm
from models import Account
from login_manager import AccountRoles

from models import db, db_add, db_flush
register_page = Blueprint('register_page', __name__, template_folder='templates', static_folder='static')

@register_page.route('status')
def status():
    return 'OK', 200

    
@register_page.route('/',  methods=['GET'])
def index():
    print(' current_user.is_authenticated : ',  current_user.is_authenticated)
    if current_user.is_authenticated:
        return redirect(url_for('index_page.index'))
    form = UserRegisterForm()

    return render_template('views/register/index.html', form=form)

@register_page.route('/',  methods=['POST'])
def register():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.

    form = UserRegisterForm(request.form)
    username = form['username'].data.encode('utf-8')
    password = form['password'].data
    print("username : ", username, "password : ", password)
    if form.validate():
        user = db.session.query(Account).filter(Account.username==username).first()#type: Account
        print(user)
        if user is not None:
            return u'username already exist.', 400
        else:
            user = Account(username, password, AccountRoles.User.value)
            db_add(user)
            db_flush()
            return '', 200
    return '', 400
