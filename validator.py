from web3 import Web3
from config import *
import json

# Connect with all nodes
w3 = Web3(Web3.HTTPProvider(NODE_RPC))
# Load contract abi
with open(CONTRACT_JSON, "r") as f:
  contract = json.load(f)
# Load contract abi into web3
val_addr = "0x0000000000000000000000000000000000000088"
val_abi = contract["abi"]
val_contract = w3.eth.contract(address=val_addr, abi=val_abi)

def transfer(value, from_account, to_addr):
  signed_transaction = w3.eth.account.sign_transaction({
    "from": from_account.address,
    "to": to_addr,
    "nonce": w3.eth.get_transaction_count(from_account.address),
    "gas": 21000,
    "gasPrice": 250000000,
    "value": value
  }, from_account.key)

  txn_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
  return txn_hash.hex()

def uploadKYC(kyhash, from_account):
  estimate_gas = val_contract.functions["uploadKYC"](kyhash).estimate_gas()
  encoded_data = val_contract.encodeABI(fn_name="uploadKYC", args=[kyhash])
  signed_transaction = w3.eth.account.sign_transaction({
    "from": from_account.address,
    "to": val_addr,
    "nonce": w3.eth.get_transaction_count(from_account.address),
    "gas": estimate_gas,
    "gasPrice": 250000000,
    "value": 0,
    "data": encoded_data
  }, from_account.key)

  txn_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
  return txn_hash.hex()

def propose(candidate_addr, owner_account, gas, nonce):
  encoded_data = val_contract.encodeABI(fn_name="propose", args=[candidate_addr])
  signed_transaction = w3.eth.account.sign_transaction({
    "from": owner_account.address,
    "to": val_addr,
    "nonce": nonce,
    "gas": gas,
    "gasPrice": 250000000,
    "value": 10000000000000000000000000,
    "data": encoded_data
  }, owner_account.key)

  txn_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
  return txn_hash.hex()
