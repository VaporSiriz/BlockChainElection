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

BlockChainUrlFormat = '{0}/{1}'
BlockChainUrls= [BlockChainUrlFormat.format(os.getenv("BlockChainURL1", "127.0.0.1"), 'health_check'),
                 BlockChainUrlFormat.format(os.getenv("BlockChainURL2", "127.0.0.1"), 'health_check')]

BlockChainPorts = range(5000, 5003)# 5000:5003 번포트 사용
