# Propose Masternode in Xinfin Network

# Prepare
```
pip3 install -r requirements.txt
```

# prepare your owner account
```
touch keys/OWNER_KEY.txt
vim OWNER_KEY.txt # private key
```

# prepare which account you want to nominate
```
vim masternodes.json
```

# Update network config
```
# NODE_RPC
vim config.py
```

# run
```
python3 add_masternode.py
```
