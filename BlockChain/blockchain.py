import contextlib
import hashlib
import json
import logging
import sys
import time
import threading

from ecdsa import NIST256p
from ecdsa import VerifyingKey
import requests

import utils

MINING_DIFFICULTY = 3
MINING_SENDER = 'THE BLOCKCHAIN'
MINING_REWARD = 1.0
MINING_TIMER_SEC = 20

BLOCKCHAIN_PORT_RANGE = (5000, 5003)
NEIGHBOURS_IP_RANGE_NUM = (0, 1)
BLOCKCHAIN_NEIGHBOURS_SYNC_TIME_SEC = 20

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


class BlockChain(object):

    def __init__(self, neighbours=[]):
        self.transaction_pool = []
        self.chain = []
        self.neighbours = neighbours
        print('self.neighbours : ', self.neighbours)
        self.create_block(0, self.hash({}))
        self.mining_semaphore = threading.Semaphore(1)
        self.sync_neighbours_semaphore = threading.Semaphore(1)

    def run(self):
        self.sync_neighbours()
        self.resolve_conflicts()
        self.start_mining()

    def sync_neighbours(self):
        print('1')
        is_acquire = self.sync_neighbours_semaphore.acquire(blocking=False)
        if is_acquire:
            with contextlib.ExitStack() as stack:
                stack.callback(self.sync_neighbours_semaphore.release)
                loop = threading.Timer(
                    BLOCKCHAIN_NEIGHBOURS_SYNC_TIME_SEC, self.sync_neighbours)
                loop.start()

    def create_block(self, nonce, previous_hash):
        block = utils.sorted_dict_by_key({
            'timestamp': time.time(),
            'transactions': self.transaction_pool,
            'nonce': nonce,
            'previous_hash': previous_hash
        })
        self.chain.append(block)
        self.transaction_pool = []

        for node in self.neighbours:
            try:
                #requests.delete(f'http://{node}/transactions')
                requests.delete(f'{node}/transactions')
            except Exception as ex:
                print('ex1 : ', ex)
                continue

        return block

    def hash(self, block):
        sorted_block = json.dumps(block, sort_keys=True)
        return hashlib.sha256(sorted_block.encode()).hexdigest()

    def add_transaction(self, account_address,
                        account_public_key, candidate_id,
                        election_id=None, signature=None):
        transaction = utils.sorted_dict_by_key({
            'election_id': election_id,
            'account_address': account_address,
            'candidate_id': candidate_id,
        })

        if self.verify_transaction_signature(
                account_public_key, signature, transaction):
            self.transaction_pool.append(transaction)
            return True
        return False

    def create_transaction(self, account_address,
                           account_public_key, candidate_id,
                           election_id, signature):

        is_transacted = self.add_transaction(
            account_address, account_public_key,
            candidate_id, election_id, signature)

        if is_transacted:
            for node in self.neighbours:
                try:
                    requests.put(
                        #f'http://{node}/transactions',
                        f'{node}/transactions',
                        json={
                            'account_address': account_address,
                            'account_public_key':
                                account_public_key,
                            'candidate_id': candidate_id,
                            'election_id': election_id,
                            'signature': signature,
                        }
                    )
                except Exception as ex:
                    print('ex2 : ', ex)
                    continue
        return is_transacted

    def verify_transaction_signature(
            self, account_public_key, signature, transaction):
        sha256 = hashlib.sha256()
        sha256.update(str(transaction).encode('utf-8'))
        message = sha256.digest()
        signature_bytes = bytes().fromhex(signature)
        verifying_key = VerifyingKey.from_string(
            bytes().fromhex(account_public_key), curve=NIST256p)
        verified_key = verifying_key.verify(signature_bytes, message)
        return verified_key

    def valid_proof(self, transactions, previous_hash, nonce,
                    difficulty=MINING_DIFFICULTY):
        guess_block = utils.sorted_dict_by_key({
            'transactions': transactions,
            'nonce': nonce,
            'previous_hash': previous_hash
        })
        guess_hash = self.hash(guess_block)
        return guess_hash[:difficulty] == '0'*difficulty

    def proof_of_work(self):
        transactions = self.transaction_pool.copy()
        previous_hash = self.hash(self.chain[-1])
        nonce = 0
        while self.valid_proof(transactions, previous_hash, nonce) is False:
            nonce += 1
        return nonce

    def mining(self):
        # if not self.transaction_pool:
        #     return False

        nonce = self.proof_of_work()
        previous_hash = self.hash(self.chain[-1])
        self.create_block(nonce, previous_hash)
        logger.info({'action': 'mining', 'status': 'success'})

        for node in self.neighbours:
            try:
                #requests.put(f'http://{node}/consensus')
                requests.put(f'{node}/consensus')
            except Exception as ex:
                print('ex3 : ', ex)
                continue

        return True

    def start_mining(self):
        print('3')
        is_acquire = self.mining_semaphore.acquire(blocking=False)
        if is_acquire:
            with contextlib.ExitStack() as stack:
                stack.callback(self.mining_semaphore.release)
                self.mining()
                loop = threading.Timer(MINING_TIMER_SEC, self.start_mining)
                loop.start()

    def calculate_total_amount(self, blockchain_address):
        total_amount = 0.0
        for block in self.chain:
            for transaction in block['transactions']:
                value = float(transaction['value'])
                if blockchain_address == \
                        transaction['recipient_blockchain_address']:
                    total_amount += value
                if blockchain_address == \
                        transaction['sender_blockchain_address']:
                    total_amount -= value
        return total_amount

    def valid_chain(self, chain):
        pre_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            if block['previous_hash'] != self.hash(pre_block):
                return False

            if not self.valid_proof(
                    block['transactions'], block['previous_hash'],
                    block['nonce'], MINING_DIFFICULTY):
                return False

            pre_block = block
            current_index += 1
        return True

    def resolve_conflicts(self):
        print('2')
        longest_chain = None
        max_length = len(self.chain)
        for node in self.neighbours:
            try:
                #response = requests.get(f'http://{node}/chain')
                response = requests.get(f'{node}/chain')
                if response.status_code == 200:
                    response_json = response.json()
                    chain = response_json['chain']
                    chain_length = len(chain)
                    if chain_length > max_length and self.valid_chain(chain):
                        max_length = chain_length
                        longest_chain = chain
            except Exception as ex:
                    print('ex4 : ', ex)
                    continue

        if longest_chain:
            self.chain = longest_chain
            logger.info({'action': 'resolve_conflicts', 'status': 'replaced'})
            return True

        logger.info({'action': 'resolve_conflicts', 'status': 'not_replaced'})
        return False
