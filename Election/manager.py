from flask_script import Manager
#from flask_migrate import Migrate, MigrateCommand
from default_config import SQLALCHEMY_DATABASE_URI
from models import db, db_commit, db_add
from election import app

manager = Manager(app)

@manager.command
def initdb():
    print("initdb")
    db.create_all()
#    db_commit()

if __name__ == '__main__':
    manager.run()