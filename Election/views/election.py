from flask import Blueprint, render_template, make_response, redirect, request
from flask.helpers import url_for
from models import *
#from .forms import AddElectionForm, ManageElectionForm, ModifyElectionForm
from datetime import datetime, time, timedelta

election_page = Blueprint('election_page', __name__, template_folder='templates', static_folder='static')

@election_page.route('/')
def index():
    
    return render_template('views/election/list.html')

@election_page.route('/add', methods=['GET', 'POST'])
def addElection():
    form = AddElectionForm(request.form)
    if form.validate():
        election = Election()
        election.title = form['title'].data
        election.desc = form['desc'].data
        election.create_date = datetime.now()
        election.state = 0
        election.startat = form['startat'].data
        election.endat = form['endat'].data

        db.session.add(election)
        db.session.commit()

        return redirect('/')
    return render_template('views/election/add.html', form=form)


@election_page.route('/manage', methods=['GET', 'POST'])
def manageElection():
    form = ManageElectionForm()
    now = datetime.now() + timedelta(hours=9)
    elections = Election.query.all()

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

    for i in elections:
        if i.endat >= now:   # 종료시간이 지나지 않으면(진행(1) or 대기(0))
            if (i.startat < now) and (i.state == 0):
                i.state = 1
        else:   # 종료시간이 지나면(종료(-1))
            if i.state != -1:
                i.state = -1
    db.session.commit()
        
    page = request.args.get('page', type=int, default=1)
    res_list = Election.query.filter(Election.endat >= now).order_by(Election.create_date.asc())
    res_list = res_list.paginate(page, per_page=4)

    page2 = request.args.get('page2', type=int, default=1)
    end_list = Election.query.filter(Election.endat < now).order_by(Election.create_date.asc())
    end_list = end_list.paginate(page2, per_page=4)

    return render_template('views/election/manage.html', res_list=res_list, end_list=end_list, form=form)

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