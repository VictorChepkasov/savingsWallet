from brownie import SavingWallet, WalletsFactory, accounts, network
from dotenv import load_dotenv

load_dotenv()

def main():
    account = accounts[0] if network.show_active() == 'development' else accounts.load('victor')
    deployFactory(account)

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
