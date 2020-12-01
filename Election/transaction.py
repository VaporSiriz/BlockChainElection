import base58
import codecs
import hashlib

from ecdsa import NIST256p
from ecdsa import SigningKey

import utils

class Transaction(object):
    def __init__(self, election_id, account, candidate_id):
        self.election_id = election_id
        self.account_private_key = account.private_key
        self.account_public_key = account.public_key
        self.account_blockchain_address = account.blockchain_address
        self.candidate_id = candidate_id

    def generate_signature(self):
        sha256 = hashlib.sha256()
        transaction = utils.sorted_dict_by_key({
            'election_id': self.election_id,
            'account_address': self.account_blockchain_address,
            'candidate_id': self.candidate_id
        })
        sha256.update(str(transaction).encode('utf-8'))
        message = sha256.digest()
        private_key = SigningKey.from_string(bytes().fromhex(self.account_private_key), curve=NIST256p)
        private_key_sign = private_key.sign(message)
        signature = private_key_sign.hex()
        return signature