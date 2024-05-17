from bitcoinlib.wallets import Wallet
from bitcoinlib.services.services import Service
from bitcoinlib.mnemonic import Mnemonic
from web3 import Web3

def check_balance_and_transfer(wallet_phrase, my_wallet_address, coin):
    if coin.lower() == 'bitcoin':
        # Generate Bitcoin wallet from recovery phrase
        wallet = Wallet.create('wallet_name', keys=wallet_phrase)

        # Get the total balance of the Bitcoin wallet
        total_balance = wallet.balance()

        # Check if the total balance is over $100
        if total_balance >= 100:
            # Get the list of unspent transaction outputs (UTXOs) for the Bitcoin wallet
            utxos = wallet.utxos()

            # Create a Bitcoin transaction
            tx = wallet.create_transaction(outputs=[(my_wallet_address, total_balance)], unspents=utxos)

            # Sign the Bitcoin transaction
            tx.sign()

            # Broadcast the Bitcoin transaction to the network
            Service.broadcast(tx)

            return f"Transferred {total_balance} BTC to {my_wallet_address}"
        else:
            return "Total balance is less than $100, no transfer needed."

    elif coin.lower() == 'ethereum':
        # Connect to Ethereum node
        w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/your_infura_project_id'))

        # Derive Ethereum private key from recovery phrase
        private_key = Mnemonic.to_private_key(wallet_phrase)

        # Get the Ethereum balance
        balance_wei = w3.eth.get_balance(my_wallet_address)

        # Convert balance from wei to ether
        total_balance = w3.fromWei(balance_wei, 'ether')

        # Check if the total balance is over $100
        if total_balance >= 100:
            # Create a raw Ethereum transaction
            tx = {
                'to': my_wallet_address,
                'value': balance_wei,
                'gas': 21000,
                'gasPrice': w3.toWei('50', 'gwei'),
                'nonce': w3.eth.getTransactionCount(w3.toChecksumAddress(my_wallet_address))
            }

            # Sign the Ethereum transaction
            signed_tx = w3.eth.account.sign_transaction(tx, private_key)

            # Send the signed transaction
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

            return f"Transferred {total_balance} ETH to {my_wallet_address} with tx hash {tx_hash.hex()}"
        else:
            return "Total balance is less than $100, no transfer needed."

    else:
        return "Unsupported coin. Supported coins are Bitcoin and Ethereum."

# Example usage
recovery_phrase = "your recovery phrase here"
my_wallet_address = "your wallet address here"
coin = "Bitcoin"  # or "Ethereum"

result = check_balance_and_transfer(recovery_phrase, my_wallet_address, coin)
print(result)
