from web3 import Web3, Account
import json

rpc_eth = 'https://stylus-testnet.arbitrum.io/rpc'
w3 = Web3(Web3.HTTPProvider(rpc_eth))
#https://t.me/mallinmakin
#https://t.me/mallinmakin
#https://t.me/mallinmakin
ERC20_ABI = json.loads('''[{"type":"error","name":"InvalidBlockNumber","inputs":[{"type":"uint256","name":"requested","internalType":"uint256"},{"type":"uint256","name":"current","internalType":"uint256"}]},{"type":"event","name":"L2ToL1Transaction","inputs":[{"type":"address","name":"caller","internalType":"address","indexed":false},{"type":"address","name":"destination","internalType":"address","indexed":true},{"type":"uint256","name":"uniqueId","internalType":"uint256","indexed":true},{"type":"uint256","name":"batchNumber","internalType":"uint256","indexed":true},{"type":"uint256","name":"indexInBatch","internalType":"uint256","indexed":false},{"type":"uint256","name":"arbBlockNum","internalType":"uint256","indexed":false},{"type":"uint256","name":"ethBlockNum","internalType":"uint256","indexed":false},{"type":"uint256","name":"timestamp","internalType":"uint256","indexed":false},{"type":"uint256","name":"callvalue","internalType":"uint256","indexed":false},{"type":"bytes","name":"data","internalType":"bytes","indexed":false}],"anonymous":false},{"type":"event","name":"L2ToL1Tx","inputs":[{"type":"address","name":"caller","internalType":"address","indexed":false},{"type":"address","name":"destination","internalType":"address","indexed":true},{"type":"uint256","name":"hash","internalType":"uint256","indexed":true},{"type":"uint256","name":"position","internalType":"uint256","indexed":true},{"type":"uint256","name":"arbBlockNum","internalType":"uint256","indexed":false},{"type":"uint256","name":"ethBlockNum","internalType":"uint256","indexed":false},{"type":"uint256","name":"timestamp","internalType":"uint256","indexed":false},{"type":"uint256","name":"callvalue","internalType":"uint256","indexed":false},{"type":"bytes","name":"data","internalType":"bytes","indexed":false}],"anonymous":false},{"type":"event","name":"SendMerkleUpdate","inputs":[{"type":"uint256","name":"reserved","internalType":"uint256","indexed":true},{"type":"bytes32","name":"hash","internalType":"bytes32","indexed":true},{"type":"uint256","name":"position","internalType":"uint256","indexed":true}],"anonymous":false},{"type":"function","stateMutability":"view","outputs":[{"type":"bytes32","name":"","internalType":"bytes32"}],"name":"arbBlockHash","inputs":[{"type":"uint256","name":"arbBlockNum","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"arbBlockNumber","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"arbChainID","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"arbOSVersion","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"getStorageGasAvailable","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"isTopLevelCall","inputs":[]},{"type":"function","stateMutability":"pure","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"mapL1SenderContractAddressToL2Alias","inputs":[{"type":"address","name":"sender","internalType":"address"},{"type":"address","name":"unused","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"myCallersAddressWithoutAliasing","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"size","internalType":"uint256"},{"type":"bytes32","name":"root","internalType":"bytes32"},{"type":"bytes32[]","name":"partials","internalType":"bytes32[]"}],"name":"sendMerkleTreeState","inputs":[]},{"type":"function","stateMutability":"payable","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"sendTxToL1","inputs":[{"type":"address","name":"destination","internalType":"address"},{"type":"bytes","name":"data","internalType":"bytes"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"wasMyCallersAddressAliased","inputs":[]},{"type":"function","stateMutability":"payable","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"withdrawEth","inputs":[{"type":"address","name":"destination","internalType":"address"}]}]''')
eth_contract_address = Web3.to_checksum_address('0x0000000000000000000000000000000000000064')
eth_contract = w3.eth.contract(eth_contract_address, abi=ERC20_ABI)

def bridge(account):
    address = account.address
    nonce = w3.eth.get_transaction_count(address)
    
    transaction = eth_contract.functions.withdrawEth(address).build_transaction({
        'gas': 162204,
        'from': address,
        'nonce': nonce,
        'value': 2000000000000000


    })
    transaction.update({'maxFeePerGas': w3.eth.fee_history(w3.eth.get_block_number(), 'latest')['baseFeePerGas'][-1] + w3.eth.max_priority_fee})
    transaction.update({'maxPriorityFeePerGas': w3.eth.max_priority_fee})
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=account.key)
    txn = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return txn

txt = 'privates.txt'
with open(txt, 'r', encoding = 'utf-8') as keys_file:
    accounts = [Account.from_key(line.replace("\n", "")) for line in keys_file.readlines()]
    for account in accounts:
        txn = bridge(account)
        print(f'https://stylus-testnet-explorer.arbitrum.io/tx/{txn.hex()}')
