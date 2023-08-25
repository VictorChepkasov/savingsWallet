import pytest
from brownie import accounts
from scripts.deploySavingWallet import deployFactory
from scripts.deployWETH import deployWETH

@pytest.fixture(scope='session')
def walletsFactory():
    owner, b = accounts[0], accounts[1]
    contract = deployFactory(owner)
    return owner, b, contract

@pytest.fixture(scope='session')
def WETHFactory():
    return deployWETH(accounts[3])