from flask import Blueprint, render_template, make_response, flash, request, redirect, \
                  url_for, session
from flask_login import login_user, logout_user
from .forms import UserLoginForm
from models import Account
# 
from models import Msg,UserMessageBox,Election,AdminMessageBox
from login_manager import AccountRoles
from models import db, db_commit, db_add,db_flush
from flask_login import login_user, login_required, current_user
import datetime

message_page = Blueprint('message_page', __name__, template_folder='templates', static_folder='static')

#@permission_admin.require(http_exception=403)
@message_page.route('/msglist')
def msglist():
    admin_id=current_user.id#세션에서 얻어오기...가 아니네..?
    
    isadmin=AdminMessageBox.query.filter_by(admin_id=admin_id).all()
    electionid=[]
    for i in isadmin:
        electionid.append(i.election_id)
    data=[]
    for eid in electionid:
        data.append(Msg.query.filter_by(election_id=eid).all())
    l=len(data)
    result=[]
    for r in data:
        for a in r:
            result.append(a)
    l=len(result)
    return str(admin_id)
    return render_template('views/message/managerMsglist.html',data=result,l=l)
   


@message_page.route('/detailMsg')
def detailMsg():
    mid=request.args.get('variable',234)
    msg=Msg.query.filter_by(id=mid).first()
    return render_template('views/message/detailMsg.html',ml=msg)


#@permission_user.require(http_exception=403)
@message_page.route('/userMsgList',methods=['GET'])
def userMsgList():
    userid=request.args.get('eid',1)
  
    data=UserMessageBox.query.filter_by(userid=userid).all()
    result=[]
    l=0
    for i in data:
        msg=Msg.query.filter_by(state=1).filter_by(election_id=i.election_id).all()
        result.append(msg)
        l+=len(msg)
    return render_template('views/message/UserMsglist.html',l=l,result=result)

#@permission_admin.require(http_exception=403)
@message_page.route('/writeMsg')
def writeMsg():
    admin_id='admin1'#세션에서 얻어오기
    isadmin=AdminMessageBox.query.filter_by(admin_id=admin_id).all()
    data=[]
    for i in isadmin:
        data.append(i.election_id)
    return render_template('views/message/writeMsg.html',data=data)

#@permission_admin.require(http_exception=403)
@message_page.route('/addMsg',methods=['POST'])
def addMsg():
    a=Msg()
    # date = urllib.request.urlopen('http://www.google.com').headers['Date']
    # a.wroteTime=date

    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    a.wroteTime=formatted_date
    a.state=0
    a.election_id=request.form['selected']
    a.msgTitle=request.form['title']
    a.msgContent=request.form['content']
    a.election_title='title'+request.form['selected']
    #Election.query.filter_by(id=a.election_id).first().title
    #models.db_add(a)


    db_add(a)
    # data=Msg.query.all()
    # l=len(data)
    return msglist()
    #return render_template('views/message/managerMsglist.html',data=data,l=l)

#@permission_admin.require(http_exception=403)
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

    #userid=1
    usermsgbox = UserMessageBox.query.filter_by(election_id=msg.election_id).all()
    # if usermsgbox:
    #     pass
    # else:
    #     a=UserMessageBox()
    #     a.userid=userid
    #     a.election_id=msg.election_id
    #     a.state=0
    #     db_add(a)

    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    msg.sendedTime=formatted_date

    msg.state=1
    db.session.commit()
    db.session.remove()


    return msglist()
    #return render_template('views/message/managerMsglist.html',data=data,l=l)


#@permission_admin.require(http_exception=403)
@message_page.route('/delMsg' ,methods=['POST'])
def delMsg():
    msgid=request.form['msgId']
    msg = Msg.query.filter_by(id=msgid).first()
    db.session.delete(msg)
    data=Msg.query.all()
    l=len(data)
    return msglist()
   # return render_template('views/message/managerMsglist.html',data=data,l=l)


#permission_admin.require(http_exception=403)
@message_page.route('/receiverList' ,methods=['GET'])
def receiverList():
    
    eid=request.args.get('eid',234)
    rlist = UserMessageBox.query.filter_by(election_id=eid).all()

    userlist=[]
    l=len(userlist)
    for i in rlist:
        userlist.append(Account.query.filter_by(id=i.userid).first())
        
    return render_template('views/message/receiverList.html',data=userlist,l=l)



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
@message_page.route('/addadmin')
def addadmin():
        account = Account("admin1", "admin1", AccountRoles.Admin.value)
        db_add(account)
        db_commit()
        return "admin 추가"

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