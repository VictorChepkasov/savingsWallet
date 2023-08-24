from brownie import SavingWallet, WalletsFactory, accounts
from dotenv import load_dotenv

load_dotenv()

def main():
    deployFactory(accounts[0])

def deployFactory(_from):
    masterContract = SavingWallet.deploy({
        'from': _from,
        'priority_fee': '10 wei'
    })
    print(f'Master-contract address: {masterContract.address} \n')
    cloneFactory = WalletsFactory.deploy(masterContract.address, {
        'from': _from,
        'priority_fee': '10 wei'
    })
    print(f'Wallets clone-factory deployed successful!')
    return cloneFactory
