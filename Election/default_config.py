import logging.handlers
import os

script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.')

DEBUG = True
DEVELOPMENT = True

db_url = os.getenv("DB_URL", "127.0.0.1")
db_name = os.getenv("DB_NAME", "election")
db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD", "rootpassword")
SQLALCHEMY_DATABASE_URI = 'mysql://{0}:{1}@{2}/{3}'.format(db_user, db_password, db_url, db_name)
SQLALCHEMY_POOL_RECYCLE = 60 * 5
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY ='this is secret'

formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

file_handler = logging.handlers.TimedRotatingFileHandler(
    os.path.join(script_path, 'logs', 'election.log'),
        when='midnight', encoding='utf-8',
        )
file_handler.setFormatter(formatter)

LOGGERS = [file_handler]
BLOCKCHAINURL = os.getenv("BlockChainURL", "127.0.0.1")
BLOCKCHAINNUMBER = int(os.getenv("BlockChainNumber", 0))
BLOCKCHAINFORMAT = 'http://{0}{1}:5000/{2}'
#BLOCKCHAINFORMAT = 'http://{0}/{1}'
EC2BLOCKCHAINURL=[os.getenv("BlockChainURL1", None), os.getenv("BlockChainURL2", None), os.getenv("BlockChainURL3", None)]