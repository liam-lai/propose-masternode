from multiprocessing.sharedctypes import Value
from time import sleep
from web3 import Web3
from eth_account import Account
from config import *
import validator
import json


# Connect with all nodes
w3 = Web3(Web3.HTTPProvider(NODE_RPC))

# Load all nodes account
# node_accounts = []
# for i in range(NUM_TEST_NODE):
#   with open(f"{TEST_NODE_KEY_FOLDER}/PRIVATE_KEY_{i+1}.txt", "r") as f:
#     privKey = f.readline().strip()
#     node_accounts.append(
#       Account.from_key(f"0x{privKey}")
#     )

# Load rich account
# with open(RICH_KEY, "r") as f:
#   privKey = f.readline().strip()
#   rich_account = Account.from_key(f"0x{privKey}")
#   print("rich_account:",rich_account.address)

# Load generated key 1 for testing
with open(OWNER_KEY, "r") as f:
  privKey = f.readline().strip()
  owner_account = Account.from_key(f"0x{privKey}")
  print("owner_account:",owner_account.address)

with open("masternodes.json", "r") as json_data:
  masternodes = json.load(json_data)
  addresses = [v['address'] for v in masternodes.values()]


if __name__ == "__main__":
  
  # 1. transfer entire amount of XDC from rich account to owner account
  # 1,120,000,000,000,000,000,000,000,000 wei == 12,000,000 coin
  # txn1 = validator.transfer(12000000000000000000000000 * len(addresses), rich_account, owner_account.address)
  #sleep(2)

  # 2. submit kyhash from owner account to add it into whitelist
  # txn2 = validator.uploadKYC("test", owner_account)
  # sleep(2)
  
  txns = []
  gas = 600000
  nonce = w3.eth.get_transaction_count(owner_account.address)

  for addr in addresses:
    gas = 600000
    while True:
      try:
        print("propose", addr, gas, nonce)
        validator.propose(addr, owner_account, int(gas), nonce)
      except Exception as e:
        if e.args[0]['message'] == 'nonce too low':
          nonce = nonce+1
        if e.args[0]['message'] == 'replacement transaction underpriced':
          gas *= 1.1
          gas = int(gas)
        print("continue", e.args[0]['message'])
        sleep(1)
        continue
      print("successfully proposed", addr)
      nonce = nonce+1
      sleep(5)
      break
