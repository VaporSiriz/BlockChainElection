from flask import Blueprint, render_template, make_response, request
from models import *
from flask_login import login_required
from login_manager import permission_admin, permission_user

vote_page = Blueprint('vote_page', __name__, template_folder='templates', static_folder='static')

#election_id와 candidate_id는 parameter으로 받음

@vote_page.route('/')
@login_required
@permission_user.require(http_exception=403)
def index():
    election_id = request.args.get('election_id')
    if election_id is None:
        return u'', 404
    return render_template('views/vote/index.html')

@vote_page.route('/vote/<election_id>/<candidate_id>')
@permission_user.require(http_exception=403)
def vote():
    return render_template('views/vote/index.html')


@vote_page.route('status')
def status():
    return 'OK', 200
    