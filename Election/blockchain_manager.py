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

    def init_app(self, app):
        self._app = app
        self.loaded_blockchain_server = []
        self.blockchain_url = app.config['BLOCKCHAINURL']
        self.blockchain_number = app.config['BLOCKCHAINNUMBER']
        self.url_format = app.config['BLOCKCHAINFORMAT']
        #self.blockchain_urls = app.config['EC2BLOCKCHAINURL'] # 클라우드 instance로 올려서 사용할 때.
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

        """ 순서 : transactions -> mining -> sync -> delete extra transactions
            원래는 블록체인 서버끼리 이 작업을 해야하나 구현의 문제가 있어 클라쪽 서버에서 일련의 과정을
            모두 실행.
        """
        rand_num = self.get_blockchain_server_with_rand()
        # for i in range(1, self.blockchain_number+1):
        #     url = self.url_format.format(self.blockchain_url, rand_num, 'transactions')
        #     rsp = requests.delete(url)
        #     sleep(1)
        url = self.url_format.format(self.blockchain_url, rand_num, 'transactions')
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        rsp = requests.post(url, data, headers=headers, timeout=3)
        if rsp.status_code == 201:
            sleep(1)
            url = self.url_format.format(self.blockchain_url, rand_num, 'mine')
            rsp = requests.get(url)
            if rsp.status_code == 200:
                return True
        return False

    def get_my_vote(self, election_id, account_address):
        params = {'election_id': election_id, 'account_address': account_address}
        json = None
        for i in range(1, self.blockchain_number):
            url = self.url_format.format(self.blockchain_url, i, 'get_vote')
            rsp = requests.get(url, params={'election_id':election_id, 'account_address': account_address})
            if json is None:
                json = rsp.json()
            if json != rsp.json():
                return None
            print(rsp.json())
        return json

    def get_my_vote_block(self, election_id, account_address):
        params = {'election_id': election_id, 'account_address': account_address}
        json = None
        for i in range(1, self.blockchain_number):
            url = self.url_format.format(self.blockchain_url, i, 'get_vote_block')
            rsp = requests.get(url, params={'election_id':election_id, 'account_address': account_address})
            print(rsp.json())
            if json is None:
                json = rsp.json()
            if json != rsp.json():
                return None
            print(rsp.json())
        return json

    def get_vote_result(self, election_id):
        params = {'election_id': election_id}
        json = []
        for i in range(1, self.blockchain_number+1):
            url = self.url_format.format(self.blockchain_url, i, 'result')
            rsp = requests.get(url)
            json.append(rsp.json())
            print(rsp.json())
        return json

            
    
    