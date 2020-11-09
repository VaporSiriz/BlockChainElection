from flask import Blueprint, render_template, make_response
from models import *

index_page = Blueprint('index_page', __name__, template_folder='templates', static_folder='static')

@index_page.route('/')
def index():
    return render_template('views/index.html')

@index_page.route('status')
def status():
    return 'OK', 200