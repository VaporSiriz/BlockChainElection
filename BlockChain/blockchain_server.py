from flask import Flask
from flask import jsonify
from flask import request

from blockchain import BlockChain
import wallet
import urllib
import threading
import requests
import asyncio
import json

BLOCKCHAIN_NEIGHBOURS_SYNC_TIME_SEC = 5

app = Flask(__name__)

def init_app():
    app.config.from_object('default_config')
    for logger in app.config.get('LOGGERS', ()):
        app.logger.addHandler(logger)

    BlockChain.instance().init_blockchain(app, app.config['BLOCKCHAINURLS'])

    return app

@app.route('/health_check_other_machine', methods=['GET'])
def health_check_other_machine():
    for url in app.config['BLOCKCHAINURLS']:
        url = app.config['BLOCKCHAINURLFORMAT'].format(url, 'status')
        print('url : ', url)
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                print('1 : 200')
            
        except Exception as ex:
            print('ex : ', ex)
    return '', 200

def get_blockchain():
    if not cached_blockchain:
        print('not cached')
        cached_blockchain['blockchain'] = BlockChain()
        cached_blockchain['blockchain'].init_blockchain(app, app.config['BLOCKCHAINURLS'])
        app.logger.warning({})
    return cached_blockchain['blockchain']

@app.route('/status', methods=['GET'])
def status():

    return 'OK', 200

@app.route('/health_check', methods=['GET'])
def health_check():
    return 'OK', 200

@app.route('/chain', methods=['GET'])
def get_chain():
    block_chain = BlockChain.instance()
    print('block_chain.chain : ', block_chain.chain)
    response = {
        'chain': block_chain.chain
    }
    return jsonify(response), 200


@app.route('/transactions', methods=['GET', 'POST', 'PUT', 'DELETE'])
def transaction():
    block_chain = BlockChain.instance()
    if request.method == 'GET':
        print('transaction get')
        transactions = block_chain.transaction_pool
        response = {
            'transactions': transactions,
            'length': len(transactions)
        }
        return jsonify(response), 200

    if request.method == 'POST':
        request_json = request.json
        required = (
            'account_address',
            'account_public_key',
            'candidate_id',
            'election_id',
            'signature')
        if not all(k in request_json for k in required):
            return jsonify({'message': 'missing values'}), 400

        vote_check = block_chain.is_there_vote(request_json['election_id'],
                                               request_json['account_address'])
        print('vote_check : ', vote_check)
        if vote_check is True:
            return jsonify({'message': 'there is already vote.'}), 400
        print('create_transaction1')
        is_created = block_chain.create_transaction(
            request_json['account_address'],
            request_json['account_public_key'],
            request_json['candidate_id'],
            request_json['election_id'],
            request_json['signature'],
        )
        if not is_created:
            return jsonify({'message': 'fail'}), 400
        return jsonify({'message': 'success'}), 201

    if request.method == 'PUT':
        request_json = request.json
        required = (
            'account_address',
            'account_public_key',
            'candidate_id',
            'election_id',
            'signature')
        if not all(k in request_json for k in required):
            return jsonify({'message': 'missing values'}), 400
        print('add_transaction')
        is_updated = block_chain.add_transaction(
            request_json['account_address'],
            request_json['account_public_key'],
            request_json['candidate_id'],
            request_json['election_id'],
            request_json['signature'],
        )
        if not is_updated:
            return jsonify({'message': 'fail'}), 400
        return jsonify({'message': 'success'}), 200

    if request.method == 'DELETE':
        block_chain.transaction_pool = []
        return jsonify({'message': 'success'}), 200

@app.route('/mine', methods=['GET'])
def mine():
    block_chain = BlockChain.instance()
    is_mined = block_chain.mining()
    print('mining : ', is_mined)
    if is_mined:
        block_chain.transaction_pool = []
        return jsonify({'message': 'success'}), 200
    return jsonify({'message': 'fail'}), 400

@app.route('/resolve_conflicts', methods=['GET'])
def resolve_conflicts():
    block_chain = BlockChain.instance()
    block_chain.resolve_conflicts()
    print('resolve_conflicts')
    return 'ok', 200

@app.route('/consensus', methods=['PUT'])
def consensus():
    block_chain = BlockChain.instance()
    replaced = block_chain.resolve_conflicts()
    print('consensus : ', replaced)
    return jsonify({'replaced': replaced}), 200

@app.route('/get_vote', methods=['GET'])
def get_vote():
    election_id = int(request.args['election_id'])
    account_address = request.args['account_address']
    
    return jsonify({
        'candidate_id': BlockChain.instance().get_vote(election_id, account_address)
    }), 200

@app.route('/get_vote_block', methods=['GET'])
def get_vote_block():
    election_id = int(request.args['election_id'])
    account_address = request.args['account_address']
    
    return jsonify({
        'block': BlockChain.instance().get_vote_block(election_id, account_address)
    }), 200

@app.route('/result', methods=['GET'])
def get_result():
    election_id = int(request.args['election_id'])
    return jsonify({
        'data': BlockChain.instance().calculate_result(election_id)
    }), 200

@app.route('/init', methods=['GET'])
def init():
    block_chain = get_blockchain()
    block_chain.chain = []
    return jsonify({
        'data': block_chain.chain
    }), 200
