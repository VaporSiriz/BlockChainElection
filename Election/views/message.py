from flask import Blueprint, render_template, make_response, flash, request, redirect, \
                  url_for, session
from flask_login import login_user, logout_user
from .forms import UserLoginForm
from models import Account
from models import Msg,UserMessageBox,Election


from models import db, db_add, db_flush
import datetime

message_page = Blueprint('message_page', __name__, template_folder='templates', static_folder='static')


@message_page.route('staris')
def staris():
    return 'starismessage'
@message_page.route('/msglist')
def msglist():
    data=Msg.query.all()
    l=len(data)
    return render_template('views/message/managerMsglist.html',data=data,l=l)



@message_page.route('/detailMsg/')
def detailMsg():

    eid=request.args.get('variable',234)

    return str(eid)



@message_page.route('/userMsgList')
def userMsgList():
    userid=1
    data=UserMessageBox.query.filter_by(userid=userid).all()
    result=[]
    l=0
    for i in data:
        msg=models.Msg.query.filter_by(state=1).filter_by(election_id=i.election_id).all()
        result.append(msg)
        l+=len(msg)




    return render_template('views/message/UserMsglist.html',l=l,result=result)


@message_page.route('/writeMsg')
def writeMsg():
    return render_template('views/message/writeMsg.html')

@message_page.route('/addMsg',methods=['POST'])
def addMsg():
    a=Msg()
    # date = urllib.request.urlopen('http://www.google.com').headers['Date']
    # a.wroteTime=date

    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    a.wroteTime=formatted_date

    a.state=0
    a.election_id=request.form['Eid']
    a.msgTitle=request.form['title']
    a.msgContent=request.form['content']
    #models.db_add(a)
    db_add(a)

    data=Msg.query.all()
    l=len(data)
    return render_template('views/message/managerMsglist.html',data=data,l=l)

@message_page.route('/sendMsg',methods=['POST'])
def sendMsg():

    msgid=request.form['msgId']
    # Eid=request.for['election_id']
    # msg=models.Msg.query.filter_by(id=msgid).first()
    msg =Msg.query.filter_by(id=msgid).first()
    #
    #
    #
    # print date

    userid=1
    usermsgbox = UserMessageBox.query.filter_by(userid=userid).filter_by(election_id=msg.election_id).first()
    if usermsgbox:
        pass
    else:
        a=UserMessageBox()
        a.userid=userid
        a.election_id=msg.election_id
        db_add(a)

    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    msg.sendedTime=formatted_date

    msg.state=1
    db.session.commit()
    db.session.remove()

    data=Msg.query.all()
    l=len(data)

    return render_template('views/message/managerMsglist.html',data=data,l=l)



@message_page.route('/staris1')
def staris1():
    return render_template('views/message/staris1.html')

@message_page.route('/createRoom',methods=['POST'])
def createRoom():
    value = request.form['roomName']
    return render_template('views/message/staris2.html',roomname=value)

@message_page.route('/createDball')
def crdbAll():
        db.create_all()
        return "2"

@message_page.route('/createDb')
def crdb():
    # create
    #models.db.create_all()

    a=Election("title?","description")
    a.id=1
    a.title="title"
    a.desc="description"
    db_add(a)
    return render_template('views/message/staris2.html')
@message_page.route('/readDb')
def readDb():

    #models.db.create_all()


    #read
    n=Election.query.filter_by(id=1).first()    #id 값만 받아오네..?


    #delete:
    # user = models.Election.query.filter_by(title="title").first()
    # models.db.session.delete(user)

    #update
    # user = models.Election.query.filter_by(title="title").first()
    # user.title="nontitle"
    # models.db.session.commit()
    # models.db.session.remove()


    return render_template('views/message/staris3.html',m=n.desc)