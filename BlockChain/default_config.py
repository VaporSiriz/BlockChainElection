import logging.handlers
import os
import requests
import urllib

script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.')

DEBUG = True
DEVELOPMENT = True

SECRET_KEY ='this is secret'

formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

file_handler = logging.handlers.TimedRotatingFileHandler(
    os.path.join(script_path, 'logs', 'blockchain.log'),
        when='midnight', encoding='utf-8',
        )
file_handler.setFormatter(formatter)

LOGGERS = [file_handler]

BLOCKCHAINURLFORMAT = 'http://{0}/{1}'
#BLOCKCHAINURLS= [os.getenv("BlockChainURL1", "127.0.0.1"), os.getenv("BlockChainURL2", "127.0.0.1")] local
# 임시로 사용하는 URL
BLOCKCHAINURLS= [os.getenv("BlockChainURL1", "127.0.0.1"), 
                 os.getenv("BlockChainURL2", "127.0.0.1")]
