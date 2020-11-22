from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from default_config import SQLALCHEMY_DATABASE_URI
from models import Account, Election
from models import db, db_commit, db_add
import election
from datetime import datetime, timedelta


def configure_app():
    app = election.init_app()
    return app

app = configure_app()

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def initdb():
    print("initdb")
    db.create_all()
#    db_commit()

@manager.command
def fillelectiontable():
    for i in range(33):
        election = Election()
        election.title = i
        election.desc = i
        election.state = 0
        election.create_date = datetime.now() + timedelta(hours=9)
        election.startat = datetime.now() + timedelta(hours=9)
        election.endat = datetime.now() + timedelta(hours=9, minutes=i)

        db.session.add(election)
        db.session.commit()

@manager.command
def addAccount(user, password):
    account = Account(user, password)
    db_add(account)
    db_commit()

if __name__ == '__main__':
    manager.run()