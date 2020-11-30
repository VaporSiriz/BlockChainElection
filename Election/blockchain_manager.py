from urllib.parse import urlparse, urljoin
import asyncio
import requests
import random
from time import sleep
from singleton import SingletonInstane
from models import Account, Election
import threading
import utils
import hashlib
from ecdsa import NIST256p
from ecdsa import SigningKey
from transaction import Transaction
import json

# BLockChainManager는 Singleton으로 생성
class BlockChainManager(SingletonInstane):
#    def __init__(self, app):

    def init_app(self, app):
        self._app = app
        self.loaded_blockchain_server = []
        # self.blockchain_url = app.config['BLOCKCHAINURL']
        self.blockchain_number = app.config['BLOCKCHAINNUMBER']
        self.url_format = app.config['BLOCKCHAINFORMAT']
        self.blockchain_urls = app.config['EC2BLOCKCHAINURL']
        self._semaphore = threading.Semaphore(1)

    def get_blockchain_server_with_rand(self):
        return random.randint(1, self.blockchain_number)

    def voting_to_blockchain_server(self, election_id, account, candidate_id):
        #type: (Election, Account, Candidate) -> Boolean
        transaction = Transaction(election_id, account, candidate_id)
        data = json.dumps(utils.sorted_dict_by_key({
                            'election_id': election_id,
                            'account_address': account.blockchain_address,
                            'account_public_key': account.public_key,
                            'candidate_id': candidate_id,
                            'signature': transaction.generate_signature()
                          }))
        print('data : ', data)
        #url = self.url_format.format(self.blockchain_url, self.get_blockchain_server_with_rand(), 'transactions')
        url = self.url_format.format(self.blockchain_urls[self.get_blockchain_server_with_rand()-1], 'transactions')
        print('url : ', url)
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        rsp = requests.post(url, data, headers=headers, timeout=3)
        
        if rsp.status_code == 200:
            return True
        else:
            return False

    