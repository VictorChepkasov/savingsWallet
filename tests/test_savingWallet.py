import pytest
from brownie import accounts
from scripts.deploySavingWallet import deploySavingWallet
from scripts.scripts import (
    setWalletInfo,
    setConsentToBreakLimit,
    pay,
    breakTheLimit,
    updateWalletBalance,
    updateLimit,
    getWalletInfo,
    getWalletBalance,
)

@pytest.fixture(autouse=True)
def walletContract():
    owner = accounts[0]
    b = accounts[1]
    contract = deploySavingWallet(owner)
    return owner, b, contract

@pytest.mark.parametrize('deposit', [0, 50, 100, 200000])
def test_setWalletInfo(walletContract, deposit):
    owner, b, _ = walletContract
    deploySavingWallet(owner)
    validInfo = [owner.address, b.address, deposit / 100,
        0, False, deposit / 100, deposit / 100]
    setWalletInfo(owner, b, deposit)
    testInfo = getWalletInfo()
    print(f'Valid: {validInfo}')
    getWalletBalance()
    assert testInfo == validInfo

@pytest.mark.parametrize('deposit', [
    pytest.param(0, marks=pytest.mark.xfail),
    pytest.param(50, marks=pytest.mark.xfail),
    100, 200000])
def test_pay(walletContract, deposit):
    owner, b, contract = walletContract
    setWalletInfo(owner, b, deposit)
    validInfo = getWalletInfo()[-2] - (deposit / 100)
    pay(contract, deposit / 100)
    newInfo = getWalletInfo()
    print(f'New info about Owner balance: {newInfo}')
    assert validInfo == newInfo[-2]

@pytest.mark.parametrize('deposit', [0, 50, 100, 200000])
def test_updateLimit(walletContract, deposit):
    owner, b, _ = walletContract
    setWalletInfo(owner, b, deposit)
    validInfo = getWalletInfo()
    validInfo = [validInfo[-1], validInfo[-2]]
    updateLimit()
    newInfo = getWalletInfo()
    newInfo = [newInfo[-1], newInfo[-2]]
    assert validInfo == newInfo

@pytest.mark.parametrize('deposit', [0, 50, 100, 200000])
def test_updateWalletBalance(walletContract, deposit):
    owner, b, _ = walletContract
    initialDeposit = 500
    setWalletInfo(owner, b, initialDeposit)
    validBalance = initialDeposit + deposit
    updateWalletBalance(deposit)
    updatedBalance = getWalletBalance()
    assert updatedBalance == validBalance

@pytest.mark.parametrize('value', [100])
@pytest.mark.parametrize('deposit', [1000])
def test_breakingTheLimit(walletContract, value, deposit):
    owner, b, _ = walletContract
    c = accounts[2]
    setWalletInfo(owner, b, deposit)
    validBalance = getWalletBalance() - value
    setConsentToBreakLimit(owner)
    setConsentToBreakLimit(b)
    breakTheLimit(c, value)
    print(f'C balance: {c.balance}')
    weiPerDay = getWalletInfo()[2]
    newBalance = getWalletBalance()
    assert value > weiPerDay
    assert newBalance == validBalance