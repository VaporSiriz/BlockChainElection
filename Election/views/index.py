from flask import Blueprint, render_template, make_response, flash, request, redirect, url_for
from flask_login import login_user, login_required, current_user
from .forms import UserLoginForm

from models import db, db_add, db_flush
index_page = Blueprint('index_page', __name__, template_folder='templates', static_folder='static')

@index_page.route('status')
@login_required
def status():
    return 'OK', 200
    
@index_page.route('/',  methods=['GET'])
def index():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.

    print("current_user : ", current_user)

    return redirect(url_for('election_page.index'))#render_template('views/index/index.html')
