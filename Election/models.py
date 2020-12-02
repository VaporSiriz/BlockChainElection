from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.util.langhelpers import symbol
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from ecdsa import NIST256p, SigningKey
import base58
import codecs
import hashlib
from datetime import datetime
from enums import CandidateStatus, VoteStatus

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

class Account(db.Model, UserMixin):
    __table_name__ = 'account'
    __table_args__ = (
        {'extend_existing': True,
        'mysql_charset': 'utf8mb4',
        'mysql_engine': 'InnoDB'})
 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Integer, nullable=False, default=1, server_default='0', doc='0:USER, 1:ADMIN')
    _private_key = db.Column(db.String(256), nullable=False, doc="블록체인 address를 생성하기 위한 private_key")
    _public_key = db.Column(db.String(256), nullable=False, doc="블록체인 address를 생성하기 위한 public_key")
    _blockchain_address = db.Column(db.String(256), nullable=False, doc="블록 체인을 이용하기 위한 address")

    def __init__(self, username, password, role):
        self.username = username
        self.password = generate_password_hash(str(password))
        self.role = role
        signing_key = SigningKey.generate(curve=NIST256p)
        self._private_key = signing_key.to_string().hex()
        self._public_key = signing_key.get_verifying_key().to_string().hex()
        self._blockchain_address = self.generate_blockchain_address(signing_key)

    @property
    def private_key(self):
        return self._private_key

    @property
    def public_key(self):
        return self._public_key

    @property
    def blockchain_address(self):
        return self._blockchain_address

    def generate_blockchain_address(self, signing_key):
        public_key_bytes = signing_key.to_string()
        sha256_bpk = hashlib.sha256(public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()

        ripemed160_bpk = hashlib.new('ripemd160')
        ripemed160_bpk.update(sha256_bpk_digest)
        ripemed160_bpk_digest = ripemed160_bpk.digest()
        ripemed160_bpk_hex = codecs.encode(ripemed160_bpk_digest, 'hex')

        network_byte = b'00'
        network_public_key = network_byte + ripemed160_bpk_hex
        network_public_key_bytes = codecs.decode(network_public_key, 'hex')

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
    
    @staticmethod
    def check_account(account_id):
        return Account.query.filter_by(id=account_id).scalar()

class Election(db.Model):
    __table_name__ = 'election'
    __table_args__ = (
        {'extend_existing': True,
        'mysql_charset': 'utf8mb4',
        'mysql_engine': 'InnoDB'})
 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    desc = db.Column(db.String(4196), nullable=False)
    main_img = db.Column(db.String(256), nullable=True)
    create_date = db.Column(db.DateTime(), nullable=False)
    startat = db.Column(db.DateTime(), nullable=False)
    endat = db.Column(db.DateTime(), nullable=False)
    destroy_date = db.Column(db.DateTime(), nullable=True)

    def __init__(self, title, desc, main_img, startat, endat):
        self.title = title
        self.desc = desc
        self.main_img = main_img
        self.create_date = datetime.now()
        self.startat = startat
        self.endat = endat

    def is_ended(self):
        return self.endat >= datetime.now()

    def in_works(self):
        return self.startat <= datetime.now()

    def is_destroy(self):
        return self.destroy_date is not None

    def destroy(self):
        self.destroy_date = datetime.now()
        db_add(self)
        db_flush()

class Voters(db.Model):
    __table_name__ = 'voters'
    __table_args__ = (
        {'extend_existing': True,
        'mysql_charset': 'utf8mb4',
        'mysql_engine': 'InnoDB'})
 
    election_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=False)
    account_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=False)
    is_candidate = db.Column(db.Boolean, nullable=False, default=False)
    create_date = db.Column(db.DateTime, nullable=True)
    update_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, election_id, account_id):
        self.election_id = election_id
        self.account_id = account_id
        self.create_date = datetime.now()
        self.update_date = datetime.now()

    def change_state_candidate(self):
        self.is_candidate = not self.is_candidate

    @property
    def username(self):
        acc = Account.query.filter_by(id=self.account_id).first()
        if acc is not None:
            return acc.username
        return None

    @staticmethod
    def get_number_of_voters(election_id):
        return Voters.query.filter_by(election_id=election_id).count()

class Candidate(db.Model):
    __table_name__ = 'candidate'
    __table_args__ = (
        {'extend_existing': True,
            'mysql_charset': 'utf8mb4',
            'mysql_engine': 'InnoDB'})

    name = db.Column(db.String(64), nullable=False)
    election_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=False)
    candidate_id = db.Column(db.Integer, nullable= False, primary_key=True, autoincrement=False)
    candidate_img = db.Column(db.String(256), nullable=True)
    create_date = db.Column(db.DateTime, nullable=True)
    update_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, name, symbolnum, candidate_img, election_id):
        self.name = name
        self.symbolnum = symbolnum
        self.election_id = election_id
        self.candidate_img = candidate_img
        self.create_date = datetime.now()
        self.update_date = datetime.now()

    def change_status(self, state):
        self.state = state
        if self.state < CandidateStatus.APPROVE:
            voter = Voters.query.filter(Voters.update_date)

class Vote(db.Model):
    __table_name__ = 'vote'
    __table_args__ = (
        db.Index('ix_vote_election_id_account_id', 'election_id', 'account_id'),
        {'extend_existing': True,
            'mysql_charset': 'utf8mb4',
            'mysql_engine': 'InnoDB'})
    
    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, nullable=False)
    account_id = db.Column(db.Integer, nullable=False)
    candidate_id = db.Column(db.Integer, nullable=False)
    state = db.Column(db.Boolean, nullable=False, default=False, doc='F:블록체인 서버 등록 대기, T: 등록 완료')
    create_date = db.Column(db.DateTime, nullable=False)
    destory_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, election_id, account_id, candidate_id):
        self.election_id = election_id
        self.account_id = account_id
        self.candidate_id = candidate_id
        self.state = VoteStatus.PENDING
        self.create_date = datetime.now()
        self.update_date = datetime.now()

    def approve_vote(self):
        self.state = VoteStatus.APPROVE

    def is_approved(self):
        return self.state == VoteStatus.APPROVE
    
    def is_destoryed(self):
        return self.destroy_date is not None

class AdminMessageBox(db.Model):
    __table_name__ = 'vote'
    __table_args__ = (
        {'extend_existing': True,
            'mysql_charset': 'utf8mb4',
            'mysql_engine': 'InnoDB'})
    
    admin_id=db.Column(db.String(64), primary_key=True, nullable=False, autoincrement=False)
    election_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=False)
    
    def __init__(self, admin_id, election_id):
        self.admin_id = admin_id
        self.election_id = election_id

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
    msg_id= db.Column(db.Integer, nullable=False)
    state=db.Column(db.Integer, nullable=False)

    