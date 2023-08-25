import pytest
from brownie import accounts
from scripts.deploySavingWallet import deployFactory

@pytest.fixture(scope='session', autouse=True)
def walletFactory():
    owner, b = accounts[0], accounts[1]
    contract = deployFactory(owner)
    return owner, b, contract