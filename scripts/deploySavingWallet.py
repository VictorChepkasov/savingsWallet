from brownie import WalletsFactory
from dotenv import load_dotenv

load_dotenv()

def deployFactory(_from):
    deployed = WalletsFactory.deploy({
        'from': _from,
        'priority_fee': '10 wei'
    })
    print(f'Wallets factory deployed successful!')
    return deployed
