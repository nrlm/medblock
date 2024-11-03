# app.py
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from blockchain import MedBlock
from models import db, Participant, Hospital

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bpjs_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
CORS(app)
db.init_app(app)

medblock = MedBlock()

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'receiver', 'amount', 'type']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = medblock.new_transaction(
        sender=values['sender'],
        receiver=values['receiver'],
        amount=values['amount'],
        transaction_type=values['type'],
        details=values.get('details')
    )
    response = {'message': f'Transaksi akan ditambahkan ke Blok {index}'}
    return jsonify(response), 201

@app.route('/mine', methods=['GET'])
def mine():
    last_block = medblock.last_block
    last_proof = last_block['proof']
    proof = medblock.proof_of_work(last_proof)

    block = medblock.new_block(proof)

    response = {
        'message': "Blok Baru Dibentuk",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': medblock.chain,
        'length': len(medblock.chain),
        'pending_transactions': medblock.current_transactions  # Menyertakan transaksi yang belum dimasukkan ke blok
    }
    return jsonify(response), 200

@app.route('/last_transactions')
def last_transactions():
    return render_template('last_transactions.html')

@app.route('/transactions/history/<identifier>', methods=['GET'])
def transaction_history(identifier):
    transactions = [txn for block in medblock.chain for txn in block['transactions'] if txn['sender'] == identifier or txn['receiver'] == identifier]
    return jsonify(transactions), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Membuat tabel database
    app.run(host='0.0.0.0', port=5000)
