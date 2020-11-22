from urllib.parse import urlparse, urljoin
import asyncio
import requests
import random

from models import Account, Election

class BlockChainManager(object):
    def __init__(self, app):
        self._app = app.config
        self.loaded_blockchain_server = []
        self.blockchain_url = app.config['BLOCKCHAINURL']
        self.blockchain_number = app.config['BLOCKCHAINNUMBER']
        self.url_format = app.config['BLOCKCHAINFORMAT']
        self.loop = asyncio.get_event_loop()

    """
        get connenctable blockchain server with async
        
    """
    async def blockchain_healthcheck(self, number):
        url = self.url_format.format(self.blockchain_url, number, 'health_check')
        while True:
            print("url : ", url)
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                self.loaded_blockchain_server.append(''.join(url.split('/')[:-1]))
                break
            asyncio.sleep(3.0)
        print('self.loaded_blockchain_server : ', self.loaded_blockchain_server)

    def load_blockchain_server(self):
        for number in range(1, self.blockchain_number+1):
            self.loop.run_until_complete(self.blockchain_healthcheck(number))

    def get_blockchain_server_with_rand(self):
        return self.loaded_blockchain_server[random.randint(1, self.blockchain_number)]
    
    def voting_to_blockchain_server(self, election, account, candidate):
        #type: (Election, Account) -> Boolean
        block = {
            'election_id': election.id,
            'account_public_key': account.public_key,
            'candidate_id': candidate.id
        }

    