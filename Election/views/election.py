from flask import Blueprint, render_template, make_response, redirect, request
from models import *
from .forms import AddElectionForm
from datetime import datetime, timedelta

election_page = Blueprint('election_page', __name__, template_folder='templates', static_folder='static')

@election_page.route('/')
def index():
    
    return render_template('views/election/list.html')

@election_page.route('/add', methods=['GET', 'POST'])
def addElection():
    form = AddElectionForm()
    if form.validate_on_submit():
        election = Election()
        election.title = form.data.get('title')
        election.desc = form.data.get('desc')
        election.create_date = datetime.now()
        election.state = 0
        election.startat = form.data.get('startat')
        election.endat = form.data.get('endat')

        db.session.add(election)
        db.session.commit()

        return redirect('/')
    return render_template('views/election/add.html', form=form)


@election_page.route('/manage', methods=['GET', 'POST'])
def manageElection():

    now = datetime.now() + timedelta(hours=9)
    elections = Election.query.all()
    
    for i in elections:
        print(i.startat >= now)
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

    return render_template('views/election/manage.html', res_list=res_list, end_list=end_list)