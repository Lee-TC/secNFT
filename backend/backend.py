from flask import Flask, request
from web3 import Web3, HTTPProvider
import json

app = Flask(__name__)

w3 = Web3(HTTPProvider('http://localhost:8545'))

with open("artifacts/contracts/MyNFT.sol/MyNFT.json", "r") as load_f:
    contract_abi = json.load(load_f)['abi']
contract_addr = '0x5fbdb2315678afecb367f032d93f642f64180aa3'
contract_addr = w3.toChecksumAddress(contract_addr)
owner_address = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
contract = w3.eth.contract(address=contract_addr, abi=contract_abi)

@app.route("/owner", methods = ['GET'])
def owner():
    return contract.functions.owner().call()

@app.route("/balanceof/<address>", methods = ['GET'])
def balanceof(address):
    result = contract.functions.balanceOf(w3.toChecksumAddress(address)).call()
    return str(result)

@app.route("/tokenURI/<token_id>", methods = ['GET'])
def tokenURI(token_id):
    result = contract.functions.tokenURI(int(token_id)).call()
    return str(result)

@app.route("/getApproved/<token_id>", methods = ['GET'])
def getApproved(token_id):
    result = contract.functions.getApproved(int(token_id)).call()
    return str(result)

@app.route("/isApprovedForAll/<owner_addr>/<operator_addr>", methods = ['GET'])
def isApprovedForAll(owner_addr, operator_addr):
    result = contract.functions.isApprovedForAll(w3.toChecksumAddress(owner_addr), w3.toChecksumAddress(operator_addr)).call()
    return str(result)

@app.route("/ownerOf/<token_id>", methods = ['GET'])
def ownerOf(token_id):
    result = contract.functions.ownerOf(int(token_id)).call()
    return str(result)

@app.route("/transfer", methods = ['POST'])
def transfer():
    from_addr = request.args.get('from')
    to_addr = request.args.get('to')
    token_id = request.args.get('token_id')
    private_key = request.args.get('private_key')
    from_addr = w3.toChecksumAddress(from_addr)
    to_addr = w3.toChecksumAddress(to_addr)
    nonce = w3.eth.getTransactionCount(from_addr)
    TransactionData = contract.functions['safeTransferFrom'](from_addr, to_addr, int(token_id)).buildTransaction({
        'chainId': w3.eth.chain_id,
        'from': from_addr,
        'gas': 3000000,
        'gasPrice': w3.toWei(1,'wei'),
        'nonce': nonce,
        'value': w3.toWei(0,'wei')
    })
    signed_txn = w3.eth.account.signTransaction(TransactionData, private_key)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    return txn_hash
    
@app.route("/mint", methods = ['POST'])
def mint():
    to = request.args.get('to')
    tokenURI = request.args.get('uri')
    private_key = request.args.get('private_key')
    sender = w3.eth.account.privateKeyToAccount(private_key).address
    TransactionData = contract.functions['mintNFT'](w3.toChecksumAddress(to), tokenURI).buildTransaction({
        'chainId': w3.eth.chain_id,
        'from': sender,
        'gas': 3000000,
        'gasPrice': w3.toWei(1,'wei'),
        'nonce': w3.eth.getTransactionCount(sender),
        'value': w3.toWei(0,'wei')
    })
    signed_txn = w3.eth.account.signTransaction(TransactionData, private_key)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    return txn_hash

@app.route("/approve", methods = ['POST'])
def approve():
    to = request.args.get('to')
    token_id = request.args.get('token_id')
    private_key = request.args.get('private_key')
    sender = w3.eth.account.privateKeyToAccount(private_key).address
    TransactionData = contract.functions['approve'](w3.toChecksumAddress(to), int(token_id)).buildTransaction({
        'chainId': w3.eth.chain_id,
        'from': sender,
        'gas': 3000000,
        'gasPrice': w3.toWei(1,'wei'),
        'nonce': w3.eth.getTransactionCount(sender),
        'value': w3.toWei(0,'wei')
    })
    signed_txn = w3.eth.account.signTransaction(TransactionData, private_key)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    return txn_hash

@app.route("/setApprovalForAll", methods = ['POST'])
def setApprovalForAll():
    to = request.args.get('to')
    approved = request.args.get('approved')
    private_key = request.args.get('private_key')
    sender = w3.eth.account.privateKeyToAccount(private_key).address
    TransactionData = contract.functions['setApprovalForAll'](w3.toChecksumAddress(to), w3.toChecksumAddress(approved)).buildTransaction({
        'chainId': w3.eth.chain_id,
        'from': sender,
        'gas': 3000000,
        'gasPrice': w3.toWei(1,'wei'),
        'nonce': w3.eth.getTransactionCount(sender),
        'value': w3.toWei(0,'wei')
    })
    signed_txn = w3.eth.account.signTransaction(TransactionData, private_key)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    return txn_hash

if __name__ == "__main__":
    app.run()

