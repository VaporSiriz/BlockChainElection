from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from ecdsa import NIST256p, SigningKey
import base58
import codecs
import hashlib

db = SQLAlchemy()

def get_session():
    return db.session

def db_commit():
    db.session.commit()

def db_flush():
    db.session.flush()

def db_add(o):
    db.session.add(o)

def db_end():
    db.session.close()

def db_rollback():
    db.session.rollback()

class Admin(db.Model):
    __table_name__ = 'admin'
    __table_args__ = (
        {'extend_existing': True,
            'mysql_charset': 'utf8mb4',
            'mysql_engine': 'InnoDB'})
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(str(password))

class Account(db.Model, UserMixin):
    __table_name__ = 'account'
    __table_args__ = (
        {'extend_existing': True,
            'mysql_charset': 'utf8mb4',
            'mysql_engine': 'InnoDB'})
 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    _private_key = db.Column(db.String(256), nullable=False, doc="블록체인 address를 생성하기 위한 private_key")
    _public_key = db.Column(db.String(256), nullable=False, doc="블록체인 address를 생성하기 위한 public_key")
    _blockchain_address = db.Column(db.String(256), nullable=False, doc="블록 체인을 이용하기 위한 address")

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(str(password))
        self._private_key = SigningKey.generate(curve=NIST256p)
        self._public_key = self._private_key.get_verifying_key()
        self._blockchain_address = self.generate_blockchain_address()

    @property
    def private_key(self):
        return self._private_key.to_string().hex()

    @property
    def public_key(self):
        return self._public_key.to_string().hex()

    @property
    def blockchain_address(self):
        return self._blockchain_address

    def generate_blockchain_address(self):
        public_key_bytes = self._public_key.to_string()
        sha256_bpk = hashlib.sha256(public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()

        ripemed160_bpk = hashlib.new('ripemd160')
        ripemed160_bpk.update(sha256_bpk_digest)
        ripemed160_bpk_digest = ripemed160_bpk.digest()
        ripemed160_bpk_hex = codecs.encode(ripemed160_bpk_digest, 'hex')

        network_byte = b'00'
        network_public_key = network_byte + ripemed160_bpk_hex
        network_public_key_bytes = codecs.decode(
            network_public_key, 'hex')

        sha256_bpk = hashlib.sha256(network_public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        sha256_2_nbpk = hashlib.sha256(sha256_bpk_digest)
        sha256_2_nbpk_digest = sha256_2_nbpk.digest()
        sha256_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')

        checksum = sha256_hex[:8]

        address_hex = (network_public_key + checksum).decode('utf-8')

        blockchain_address = base58.b58encode(address_hex).decode('utf-8')
        return blockchain_address

    def check_password(self, password):
        return check_password_hash(self.password, str(password))

class Election(db.Model):
    __table_name__ = 'election'
    __table_args__ = (
        {'extend_existing': True,
            'mysql_charset': 'utf8mb4',
            'mysql_engine': 'InnoDB'})
 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    desc = db.Column(db.String(4196), nullable=False)

    def __init__(self, title, desc):
        self.title = title
        self.desc = desc

class Candidate(db.Model):
    __table_name__ = 'election'
    __table_args__ = (
        {'extend_existing': True,
            'mysql_charset': 'utf8mb4',
            'mysql_engine': 'InnoDB'})
 
    id = db.Column(db.Integer, primary_key=True)
    


    def __init__(self, title, desc):
        self.title = title
        self.desc = desc

class Vote(db.Model):
    __table_name__ = 'vote'
    __table_args__ = (
        {'extend_existing': True,
            'mysql_charset': 'utf8mb4',
            'mysql_engine': 'InnoDB'})
    
    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, nullable=False)
    account_id = db.Column(db.Integer, nullable=False)

class AdminMessageBox(db.Model):
    __table_name__ = 'vote'
    __table_args__ = (
        {'extend_existing': True,
            'mysql_charset': 'utf8mb4',
            'mysql_engine': 'InnoDB'})
    
    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, nullable=True)
    admin_id=db.Column(db.String(64),nullable=True)
    

class Msg(db.Model):
    __table_name__ = 'msg'
    __table_args__ = (
        {'extend_existing': True,
            'mysql_charset': 'utf8mb4',
            'mysql_engine': 'InnoDB'})
    election_title=db.Column(db.String(64),nullable=True)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wroteTime=db.Column(db.DateTime,nullable=True)
    sendedTime=db.Column(db.DateTime,nullable=True)
    election_id = db.Column(db.String(64), nullable=False)
    msgTitle = db.Column(db.String(64), nullable=False)
    msgContent = db.Column(db.String(64), nullable=False)
    state=db.Column(db.Integer,nullable=True)

class UserMessageBox(db.Model):
    __table_name__ = 'user_message_box'
    __table_args__ = (
        {'extend_existing': True,
            'mysql_charset': 'utf8mb4',
            'mysql_engine': 'InnoDB'})
    id = db.Column(db.Integer, primary_key=True)
    userid=db.Column(db.Integer,nullable=False)
    election_id = db.Column(db.Integer, nullable=False)
    state=db.Column(db.Integer, nullable=False)

    