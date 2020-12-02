from flask import Blueprint, render_template, make_response, redirect, request
from flask.helpers import url_for
from models import *
from .forms import AddCandidateForm, AddElectionForm, ManageElectionForm, ModifyElectionForm, AddElectionVoterForm
from datetime import datetime, timedelta
from login_manager import *
from flask_login import login_user, login_required, current_user
import csv
from datetime import datetime
election_page = Blueprint('election_page', __name__, template_folder='templates', static_folder='static')

@election_page.route('/')
def index():
    now = datetime.now()
    active_elections1 = Election.query.filter(Election.startat <= now, now < Election.endat, Election.destroy_date==None).limit(3).offset(0).all()

    active_elections2 = Election.query.filter(Election.startat <= now, now < Election.endat, Election.destroy_date==None).limit(3).offset(3).all()
    
    dead_elections1 = Election.query.filter(Election.endat <= now, Election.destroy_date==None).limit(3).offset(0).all()
        
    dead_elections2 = Election.query.filter(Election.endat <= now, Election.destroy_date==None).limit(3).offset(3).all()
    
    active_votes = {}
    dead_votes = {}
    for election in active_elections1+active_elections2:
        vote = {}
        vote['whole_of_vote'] = Voters.query.filter_by(election_id=election.id).count()
        vote['num_of_vote'] = Vote.query.filter_by(election_id=election.id).count()
        active_votes[election.id] = vote
    
    for election in dead_elections1+dead_elections2:
        vote = {}
        vote['whole_of_vote'] = Voters.query.filter_by(election_id=election.id).count()
        vote['num_of_vote'] = Vote.query.filter_by(election_id=election.id).count()
        dead_votes[election.id] = vote

    return render_template('views/election/index.html', active_elections1=active_elections1,
                                                        active_elections2=active_elections2,
                                                        dead_elections1=dead_elections1,
                                                        dead_elections2=dead_elections2,
                                                        active_votes=active_votes,
                                                        dead_votes=dead_votes)

@election_page.route('/tlist')
def tlist():
    now = datetime.now()
    startElections = Election.query.filter(Election.destroy_date==None).filter(Election.startat <= now).filter(Election.endat > now).all()
    waitElections = Election.query.filter(Election.destroy_date==None).filter(Election.startat > now).filter(Election.endat > now).all()
    endElections = Election.query.filter(Election.destroy_date==None).filter(Election.endat <= now).all()

    # page = request.args.get('page', type=int, default=1)
    # elections = Election.query.filter(Election.destroy_date==None).order_by(Election.create_date.asc())
    # elections = elections.paginate(page, per_page=10)

    for election in startElections:
        print(election)

    return render_template('views/election/tlist.html', startElections=startElections, waitElections=waitElections, endElections=endElections)

@election_page.route('/<int:election_id>/voter_list')
def voter_list(election_id):
    
    election_id = int(election_id)

    election = Election.query.filter_by(id=election_id).first()
    if election is None:
        return '', 403

    candidates = Candidate.query.filter_by(election_id=election_id, ).all()
    

    return render_template('views/election/voterlist.html', election=election,
                                                            candidates=candidates)

@election_page.route('/<int:election_id>/candidate')
def apply_candidate(election_id):
    election_id = int(election_id)

    election = Election.query.filter_by(id=election_id).first()
    if election is None:
        return '', 403

    try:
        candidate = Candidate(election_id, current_user.id)
        db_add(candidate)
        db_flush()
    except Exception as ex:
        print('ex : ', ex)
        db_rollback()
        return '', 400

    return '', 200


@election_page.route('/detail')
def detail():
    
    return render_template('views/election/detail.html')

@permission_admin.require(http_exception=403)
@election_page.route('/add', methods=['GET', 'POST'])
def addElection():
    form = AddElectionForm(request.form)
    now = datetime.now()
    if form.validate():
        if form['startat'].data <= now:
            return u'start date is less than now.', 400
        if form['startat'].data >= form['endat'].data:
            return u'start date is greater than end date.', 400#csv_name = add_election_voter_form.csv_file.name
        election = Election(form['title'].data, form['desc'].data, form.img_file.data, form['startat'].data, form['endat'].data)
        db.session.add(election)
        db_flush()

        # 임시 예측 땜빵 코드
        predict_election_id = Election.query.order_by(Election.id.desc()).first().id + 1
        adminbox=AdminMessageBox(current_user.id, predict_election_id)
        db.session.add(adminbox)
        db_flush()

        return redirect(url_for('election_page.manageElection'))
    return render_template('views/election/add.html', form=form)

@permission_admin.require(http_exception=403)
@election_page.route('/manage', methods=['GET'])
def manageElection():
    form = ManageElectionForm()
    add_election_voter_form = AddElectionVoterForm()
    now = datetime.now()
    elections = Election.query.filter_by(destroy_date=None).all()
    for election in elections:
        if now < election.startat:
            add_election_voter_form.election.choices.append((election.id, '{0}({1})'.format(election.title, election.id)))
        
    page = request.args.get('page', type=int, default=1)
    res_list = Election.query.filter(Election.endat >= now, Election.destroy_date==None).order_by(Election.create_date.desc())
    res_list = res_list.paginate(page, per_page=4)

    page2 = request.args.get('page2', type=int, default=1)
    end_list = Election.query.filter(Election.endat < now, Election.destroy_date==None).order_by(Election.create_date.desc())
    end_list = end_list.paginate(page2, per_page=4)

    return render_template('views/election/manage.html', res_list=res_list, end_list=end_list, form=form,
                            add_election_voter_form=add_election_voter_form, now=now)

@permission_admin.require(http_exception=403)
@election_page.route('/manage/start_election/<int:election_id>', methods=['POST'])
def start_election(election_id):
    election_id = int(election_id)
    election = Election.query.filter_by(id=election_id).first()
    now = datetime.now()
    if election is not None:
        if election.startat <= now:
            return u'이미 시작된 선거입니다.', 400
        election.startat = datetime.now()
        db_add(election)
        db_flush()
        return '', 200
    return '', 400

@permission_admin.require(http_exception=403)
@election_page.route('/manage/end_election/<int:election_id>', methods=['POST'])
def end_election(election_id):
    election_id = int(election_id)
    election = Election.query.filter_by(id=election_id).first()
    now = datetime.now()
    if election is not None:
        if election.endat <= now:
            return u'이미 종료된 선거입니다.', 400
        election.endat = datetime.now()
        db_add(election)
        db_flush()
        return '', 200
    return '', 400

@permission_admin.require(http_exception=403)
@election_page.route('/manage/destroy_election/<int:election_id>', methods=['POST'])
def destroy_election(election_id):
    election_id = int(election_id)
    election = Election.query.filter_by(id=election_id).first()
    if election is not None:
        now = datetime.now()
        election.destroy()
        return '', 200
    return '', 400

@permission_admin.require(http_exception=403)
@election_page.route('/modify/<int:id>', methods=['GET', 'POST'])
def modifyElection(id):
    form = ModifyElectionForm(request.form)
    data = Election.query.get(id)
    if form.validate():
        election = Election.query.get(id)
        election.title = form['title'].data
        election.desc = form['desc'].data
        election.startat = form['startat'].data
        election.endat = form['endat'].data
        db.session.commit()

        return redirect(url_for('election_page.manageElection'))
    return render_template('views/election/modify.html', form=form, data=data)

@permission_admin.require(http_exception=403)
@election_page.route('/add_voters', methods=['GET', 'POST'])
def add_voters():
    election_id = int(request.form['election'])
    add_election_voter_form = AddElectionVoterForm(request.form)
    csv_name = add_election_voter_form.csv_file.name
    csv_file = request.files[csv_name]
    csv_list = csv_file.read().decode('utf-8').replace('\n', '').split('\r')
    fail_account_idx = []
    """
        csv파일은
        | id |
        | 1  |
        | 2  |
        와 같은 형식을 따를 것.
        
    """
    for n, row in enumerate(csv_list):
        if n == 0:
            continue
        row = row.split(',')
        account_id = row[0]

##        
        if len(account_id)==0:
            return "success"
##

        try:
            if Account.check_account(account_id) is None:
                raise Exception("account_id '{0}' doesn't exist.".format(account_id))

            voter = Voters(election_id, account_id)
            db_add(voter)
            
            userbox=UserMessageBox()
            userbox.election_id=election_id
            userbox.userid=account_id
            userbox.msg_id=-1
            userbox.state=0
        
            db_add(userbox)
            db_flush()
        except Exception as ex:
            print(ex)
            db_rollback()
            fail_account_idx.append(account_id)
            continue

    return 'failed account idx : {0}'.format(str(fail_account_idx)), 200

@permission_admin.require(http_exception=403)
@election_page.route('/view_voters/<int:election_id>', methods=['GET', 'POST'])
def view_voters(election_id):
    page = request.args.get('page', type=int, default=1)
    voters = Voters.query.filter_by(election_id=election_id).paginate(page, per_page=5)
    
    return render_template('views/election/voters.html', voters=voters)

@permission_admin.require(http_exception=403)
@election_page.route('/mancandidate/<int:election_id>', methods=['GET', 'POST'])
def man_candidate(election_id):
    candidates = Candidate.query.filter(Candidate.election_id==election_id).order_by(Candidate.symbolnum.asc())
    
    return render_template('views/election/mancandidate.html', candidates=candidates, election_id=election_id)

@permission_admin.require(http_exception=403)
@election_page.route('/addcandidate/<int:election_id>', methods=['GET', 'POST'])
def add_candidate(election_id):
    form = AddCandidateForm()
    if form.validate(request.form):
        print('감지')
        candidate = Candidate(form['name'].data, form['symbolnum'].data, form.img_file.data, election_id)
        db.session.add(candidate)
        db.session.commit()
        return redirect(url_for('election_page.man_candidate', election_id=election_id))
    return render_template('views/election/addcandidate.html', form=form)