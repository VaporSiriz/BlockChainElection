from flask import Blueprint, render_template, make_response, request
from models import *
from flask_login import login_required, current_user
from login_manager import permission_admin, permission_user
from blockchain_manager import BlockChainManager

vote_page = Blueprint('vote_page', __name__, template_folder='templates', static_folder='static')

#election_id와 candidate_id는 parameter으로 받음

@vote_page.route('/status')
@login_required
@permission_user.require(http_exception=403)
def status():
    acc = Account.query.filter_by(id=current_user.id).first()#type: Account
    if acc is None:
        return u"account doesn't exist", 400
    print(acc.private_key)
    status = BlockChainManager.instance().voting_to_blockchain_server(1, acc, 1)
    print(status)

    return '',200

@vote_page.route('/')
@login_required
@permission_user.require(http_exception=403)
def index():
    election_id = request.args.get('election_id')
    if election_id is None:
        return u'election doesn', 404
    return render_template('views/vote/index.html')

@vote_page.route('/my_vote')
@login_required
@permission_user.require(http_exception=403)
def my_vote():
    election_id = request.args.get('election_id')
    if election_id is None:
        return u'election doesn\' exist.', 404
    election_id = int(election_id)
    election = Election.query.filter_by(election_id=election_id).scalar()
    if election is None:
        return u'election doesn\' exist.', 404

    vote = BlockChainManager.instance().get_my_vote(election_id, current_user.id)
    print(vote)
    
    return render_template('views/vote/my_vote.html')


@vote_page.route('/vote')
@permission_user.require(http_exception=403)
def vote():
    acc = Account.query.filter_by(id=current_user.id).first()#type: Account
    if acc is None:
        return u"account doesn't exist", 400

    election_id = int(request.form['election_id'])
    candidate_id = int(request.form['candidate_id'])
    
    if Election.query.filter_by(id=election_id).scalar() is None:
        return u"election doesn't exist", 400
    
    if Candidate.query.filter_by(election_id=election_id, candidate_id=candidate_id).scalar() is None:
        return u"candidate doesn't exist", 400
    
    status = BlockChainManager.instance().voting_to_blockchain_server(election_id, acc, candidate_id)
    print(status)
    return render_template('views/vote/index.html')

@vote_page.route('/vote/result')
@permission_user.require(http_exception=403)
def get_result():
    election_id = int(request.form['election_id'])
    result = BlockChainManager.instance().get_vote_result(election_id)
    print(result)

    return render_template('views/vote/result.html')