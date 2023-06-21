import pytest
from brownie import accounts
from scripts.deploySavingWallet import deploySavingWallet
from scripts.scripts import (
    setWalletInfo,
    updateLimit,
    getWalletInfo,
    getWalletBalance,
    pay
)

@pytest.fixture(autouse=True)
def walletContract():
    owner = accounts[0]
    b = accounts[1]
    contract = deploySavingWallet(owner)
    return owner, b, contract

@pytest.fixture(autouse=True)
def walletInfo(walletContract):
    deposit = 500
    setWalletInfo(walletContract[0], walletContract[1], deposit)
    walletInfo = getWalletInfo()
    return walletInfo

def test_setWalletInfo(walletContract):
    owner, b, _ = walletContract
    deposit = 500
    validInfo = [owner.address, b.address, 5, 0, False, 0, 0]
    setWalletInfo(owner, b, deposit)
    testInfo = getWalletInfo()
    assert testInfo == validInfo

def test_pay(walletContract, walletInfo):
    _, _, contract = walletContract
    deposit = 5
    pay(contract, deposit)
    newInfo = getWalletInfo()
    print(f'New info about Owner balance: {newInfo}')
    assert walletInfo[-2] - deposit == newInfo[-2]
