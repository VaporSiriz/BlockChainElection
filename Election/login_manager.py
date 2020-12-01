from enum import Enum

from flask_login import LoginManager
from flask_principal import Permission, RoleNeed, ActionNeed

from models import Account
from models import db

login_manager = LoginManager()
principals = None

def init_login_manager(app, principals):
    login_manager.init_app(app)
    principals = principals
    login_manager.login_view = 'login_page.status'
    login_manager.login_message = u"Login 성공"

@login_manager.user_loader
def load_user(id):
    return db.session.query(Account).get(int(id))

# ldap module doesn't exist, so only code
class AdminType(Enum):
    NONE = 0
    LDAP = 1

# permissions
class AccountRoles(Enum):
    User = 0
    Admin = 1

# User Roles
role_user = RoleNeed(AccountRoles.User)
role_admin = RoleNeed(AccountRoles.Admin)

role_list = [role_user, role_admin]

#Permissions
permission_user = Permission(role_user)
permission_admin = Permission(role_admin)

permission_list = [permission_user, permission_admin]