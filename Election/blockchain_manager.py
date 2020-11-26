from urllib.parse import urlparse, urljoin
import asyncio
import requests
import random
from time import sleep
from singleton import SingletonInstane
from models import Account, Election

# BLockChainManager는 Singleton으로 생성
class BlockChainManager(SingletonInstane):
#    def __init__(self, app):

    def init_app(self, app):
        self._app = app.config
        self.loaded_blockchain_server = []
        self.blockchain_url = app.config['BLOCKCHAINURL']
        self.blockchain_number = app.config['BLOCKCHAINNUMBER']
        self.url_format = app.config['BLOCKCHAINFORMAT']
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.load_blockchain_server())
        self.loop.close()
    """
        get connenctable blockchain server with async
        
    """
    async def blockchain_healthcheck(self, number):
        # Demo용으로는 3개의 블록체인 서버만 이용하기로 하고, 모든 서버는 연결된다고 가정함.
        url = self.url_format.format(self.blockchain_url, number, 'health_check')
        while True:
            try:
                #response = requests.get(url, timeout=3) url, params=None, **kwargs
                response = await self.loop.run_in_executor(None, requests.get, url, {'timeout':3})
                if response.status_code == 200:
                    self.loaded_blockchain_server.append(''.join(url.split('/')[:-1]))
                    break
            except Exception as ex:
                # 연결이 안될시 연결 될때까지 5초에 한번씩 연결시도
                print('url : ', url)
                sleep(5.0)
        print('self.loaded_blockchain_server : ', self.loaded_blockchain_server)
        
        return True

    async def load_blockchain_server(self):
        loads = [asyncio.ensure_future(self.blockchain_healthcheck(number)) for number in range(1, self.blockchain_number+1)]

        result = await asyncio.gather(*loads)
        print(result)

    def get_blockchain_server_with_rand(self):
        return self.loaded_blockchain_server[random.randint(1, self.blockchain_number)]
    
    def voting_to_blockchain_server(self, election, account, candidate):
        #type: (Election, Account, Candidate) -> Boolean
        block = {
            'election_id': election.id,
            'account_public_key': account.public_key,
            'candidate_id': candidate.id
        }

    