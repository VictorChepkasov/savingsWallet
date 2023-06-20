from brownie import SavingWallet, accounts
from dotenv import load_dotenv

load_dotenv()

def main():
    deploySavingWallet(accounts[0])

def deploySavingWallet(_from):
    walletContract = SavingWallet.deploy({
        'from': _from,
        "priority_fee": '10 wei'
    })
    print(f'Contract deployed at {walletContract} by {_from}')
    return walletContract