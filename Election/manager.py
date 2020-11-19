from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from default_config import SQLALCHEMY_DATABASE_URI
from models import Account
from models import db, db_commit, db_add
import election


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
def addAccount(user, password):
    account = Account(user, password)
    db_add(account)
    db_commit()

if __name__ == '__main__':
    manager.run()