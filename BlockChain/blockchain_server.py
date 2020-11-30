from flask import Flask
from flask import jsonify
from flask import request

import blockchain
import wallet
import urllib
import threading
import requests
import asyncio
import json

BLOCKCHAIN_NEIGHBOURS_SYNC_TIME_SEC = 5

app = Flask(__name__)
cache = {}

def init_app():
    app.config.from_object('default_config')
    print('app.config : ', app.config)
    for logger in app.config.get('LOGGERS', ()):
        app.logger.addHandler(logger)

    #get_blockchain()
    #run_blockchain()

    return app

@app.route('/health_check_other_machine', methods=['GET'])
def health_check_other_machine():
    for url in app.config['BLOCKCHAINURLS']:
        url = app.config['BLOCKCHAINURLFORMAT'].format(url, 'status')
        print('url : ', url)
        try:
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                print('1 : 200')
            
        except Exception as ex:
            print('ex : ', ex)

def get_blockchain():
    cached_blockchain = cache.get('blockchain')
    if not cached_blockchain:
        cache['blockchain'] = blockchain.BlockChain(app.config['BLOCKCHAINURLS'])
        app.logger.warning({})
    return cache['blockchain']

def run_blockchain():
    cache['blockchain'].run()

@app.route('/status', methods=['GET'])
def status():

    return 'OK', 200

@app.route('/health_check', methods=['GET'])
def health_check():
    return 'OK', 200

@app.route('/chain', methods=['GET'])
def get_chain():
    block_chain = get_blockchain()
    response = {
        'chain': block_chain.chain
    }
    return jsonify(response), 200


@app.route('/transactions', methods=['GET', 'POST', 'PUT', 'DELETE'])
def transaction():
    block_chain = get_blockchain()
    if request.method == 'GET':
        transactions = block_chain.transaction_pool
        response = {
            'transactions': transactions,
            'length': len(transactions)
        }
        return jsonify(response), 200

    if request.method == 'POST':
        request_json = request.json
        print(request_json)

        required = (
            'account_address',
            'account_public_key',
            'candidate_id',
            'election_id',
            'signature')
        if not all(k in request_json for k in required):
            return jsonify({'message': 'missing values'}), 400

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

@app.route('/mine', methods=['GET'])
def mine():
    block_chain = get_blockchain()
    is_mined = block_chain.mining()
    if is_mined:
        return jsonify({'message': 'success'}), 200
    return jsonify({'message': 'fail'}), 400


@app.route('/mine/start', methods=['GET'])
def start_mine():
    get_blockchain().start_mining()
    return jsonify({'message': 'success'}), 200


@app.route('/consensus', methods=['PUT'])
def consensus():
    block_chain = get_blockchain()
    replaced = block_chain.resolve_conflicts()
    return jsonify({'replaced': replaced}), 200


@app.route('/amount', methods=['GET'])
def get_total_amount():
    blockchain_address = request.args['blockchain_address']
    return jsonify({
        'amount': get_blockchain().calculate_total_amount(blockchain_address)
    }), 200

@app.before_request
def before_request():
    pass

@app.after_request
def after_request(response):

    return response