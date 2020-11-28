from datetime import datetime
 
from flask import Flask, render_template
from views import login, vote, index, election, message, register
from models import db, db_commit, db_end
from login_manager import login_manager, principals
from flask_util_js import FlaskUtilJs
from flask_login import current_user
from login_manager import init_login_manager
from login_manager import AccountRoles
from flask_principal import Principal
from blockchain_manager import BlockChainManager
import debugpy
import default_config
app = Flask(__name__)

app.register_blueprint(index.index_page, url_prefix='/')
app.register_blueprint(login.login_page, url_prefix='/login')
app.register_blueprint(register.register_page, url_prefix='/register')
app.register_blueprint(vote.vote_page, url_prefix='/vote')
app.register_blueprint(message.message_page, url_prefix='/message')
app.register_blueprint(election.election_page, url_prefix='/election')

#debugpy.listen(("0.0.0.0", 5678))

def init_app():
    app.config.from_object(default_config)
    for logger in app.config.get('LOGGERS', ()):
        app.logger.addHandler(logger)

    app.jinja_env.globals.update(JINJA_GLOBAL_FUNCTIONS)

    FlaskUtilJs(app)
    db.init_app(app)
    init_login_manager(app, Principal(app, skip_static=True))

    # BlockChainManager is Singleton Object
    BlockChainManager.instance().init_app(app)
    BlockChainManager.instance().load_blockchain_server()
    return app



@app.after_request
def after_request(response):
    db_commit()
    db_end()
    return response

def get_user_role():
    if current_user.is_authenticated:
        return current_user.role
    return None

def is_user_account():    
    return get_user_role() == AccountRoles.User.value

def is_admin_account():
    return get_user_role() == AccountRoles.Admin.value

JINJA_GLOBAL_FUNCTIONS = {
    'is_user_account': is_user_account,
    'is_admin_account': is_admin_account
}
