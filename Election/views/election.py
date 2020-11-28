from flask import Blueprint, render_template, make_response, redirect, request
from flask.helpers import url_for
from models import *
from .forms import AddElectionForm, ManageElectionForm, ModifyElectionForm, AddElectionVoterForm
from datetime import datetime, timedelta
from login_manager import *
from flask_login import login_user, login_required, current_user
import csv
from datetime import datetime
election_page = Blueprint('election_page', __name__, template_folder='templates', static_folder='static')

@election_page.route('/')
def index():
    
    return render_template('views/election/list.html')

@permission_admin.require(http_exception=403)
@election_page.route('/add', methods=['GET', 'POST'])
def addElection():
    form = AddElectionForm(request.form)
    print("form['startat'].data : ", form['startat'].data)
    print("form['endat'].data : ", form['endat'].data)
    if form.validate():
        if form['startat'].data >= form['endat'].data:
            return '', 400
        election = Election(form['title'].data, form['desc'].data, form['startat'].data, form['endat'].data)
        db.session.add(election)
        db.session.flush()
        #adminbox=AdminMessageBox()

        #el = Election.query.filter_by(title=form['title'].data).filter_by(desc=form['desc'].data).filter_by().filter_by(startat=form['startat'].data).filter_by(endat=form['endat'].data).first()
        #.filter_by(create_date=datetime.now()).filter_by(state=0).filter_by(startat=form['startat'].data).filter_by(endat=form['endat'].data).first()

        #adminbox.election_id=el.id
        #adminbox.admin_id=current_user.id
        #db.session.add(adminbox)
        #db.session.commit()


        return redirect(url_for('election_page.manageElection'))
    return render_template('views/election/add.html', form=form)

@permission_admin.require(http_exception=403)
@election_page.route('/manage', methods=['GET'])
def manageElection():
    form = ManageElectionForm()
    add_election_voter_form = AddElectionVoterForm()
    now = datetime.now() + timedelta(hours=9)
    elections = Election.query.all()
    for election in elections:
        if election.endat < datetime.now():
            add_election_voter_form.election.choices.append((election.id, election.title))

    if form.validate():
        if request.args.get('startbtn') != None:
            election = Election.query.get(request.args.get('startbtn'))
            election.startat = now + timedelta(seconds=-1)
            db.session.commit()
            return redirect(url_for('election_page.manageElection'))
        elif request.args.get('endbtn') != None:
            election = Election.query.get(request.args.get('endbtn'))
            election.endat = now + timedelta(seconds=-1)
            db.session.commit()
        elif request.args.get('delbtn') != None:
            election = Election.query.get(request.args.get('delbtn'))
            db.session.delete(election)
            db.session.commit()
            return redirect(url_for('election_page.manageElection'))

    # for i in elections:
    #     if i.endat >= now:   # 종료시간이 지나지 않으면(진행(1) or 대기(0))
    #         if (i.startat < now) and (i.state == 0):
    #             i.state = 1
    #     else:   # 종료시간이 지나면(종료(-1))
    #         if i.state != -1:
    #             i.state = -1
    # db.session.commit()
        
    page = request.args.get('page', type=int, default=1)
    res_list = Election.query.filter(Election.endat >= now).order_by(Election.create_date.asc())
    res_list = res_list.paginate(page, per_page=4)

    page2 = request.args.get('page2', type=int, default=1)
    end_list = Election.query.filter(Election.endat < now).order_by(Election.create_date.asc())
    end_list = end_list.paginate(page2, per_page=4)

    return render_template('views/election/manage.html', res_list=res_list, end_list=end_list, form=form,
                            add_election_voter_form=add_election_voter_form)

@permission_admin.require(http_exception=403)
@election_page.route('/manage/start/<int:election_id>', methods=['POST'])
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
        try:
            voter = Voters(election_id, account_id)
            db_add(voter)
            db_flush()
        except Exception as ex:
            print('fail')
            db_rollback()
            fail_account_idx.append(account_id)
            continue

    return 'failed account idx : {0}'.format(str(fail_account_idx)), 200
    

@permission_admin.require(http_exception=403)
@election_page.route('/view_voters/<int:election_id>', methods=['GET', 'POST'])
def view_voters(election_id):
    voters = Voters.query.filter_by(election_id=election_id).all()
    

    return render_template('views/election/modify.html')

