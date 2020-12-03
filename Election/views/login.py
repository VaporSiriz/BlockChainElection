from flask import Blueprint, render_template, make_response, flash, request, redirect, \
                  url_for, session, current_app
from flask_login import login_user, logout_user, current_user, login_required
from .forms import UserLoginForm
from models import Account
from flask_principal import Identity, AnonymousIdentity, identity_changed, identity_loaded
from login_manager import role_list
from models import db, db_add, db_flush
login_page = Blueprint('login_page', __name__, template_folder='templates', static_folder='static')

@identity_loaded.connect
def on_identity_loaded(sender, identity):
    if current_user.is_authenticated:
        identity.id = current_user.id
        identity.user = current_user
        for i in range(0, current_user.role + 1):
            identity.provides.add(role_list[i])

@login_page.route('status')
def status():
    return 'OK', 200


@login_page.route('/',  methods=['GET'])
def index():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    if current_user.is_authenticated:
        return redirect(url_for('index_page.index'))
    form = UserLoginForm()

    return render_template('views/login/index.html', form=form)

@login_page.route('/',  methods=['POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.

    form = UserLoginForm(request.form)
    username = form['username'].data.encode('utf-8')
    password = form['password'].data
    print("username : ", username, "password : ", password)
    if form.validate():
        user = db.session.query(Account).filter(Account.username==username).first()#type: Account
        print(user)
        if user is not None and user.check_password(password):
            print(u"login success")

            login_user(user)
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))


            return '', 200
            #return redirect(next or url_for('index_page.status'))
    return '', 400
#    return render_template('views/login/login.html', form=form)

@login_page.route('/logout',  methods=['GET'])
@login_required
def logout():
    logout_user()
    session.clear()
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    return redirect(url_for('index_page.index'))