from flask import Blueprint, render_template, make_response, flash, request, redirect, \
                  url_for, session, current_app
from flask_login import login_user, logout_user, current_user, login_required
from .forms import UserLoginForm
from models import Account
from flask_principal import Identity, AnonymousIdentity, identity_changed, identity_loaded
from login_manager import AccountRoles
from models import db, db_add, db_flush
users_page = Blueprint('users_page', __name__, template_folder='templates', static_folder='static')

@users_page.route('/',  methods=['GET'])
@login_required
def index():
    accounts = Account.query.order_by(Account.id.desc()).filter_by(role=AccountRoles.User.value)
    page = request.args.get('page', type=int, default=1)
    accounts = accounts.paginate(page, per_page=10)
    return render_template('views/users/index.html', accounts=accounts)