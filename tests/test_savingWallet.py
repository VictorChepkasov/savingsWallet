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
    validInfo = [owner.address, b.address, deposit // 100,
        0, False, deposit // 100, deposit // 100]
    setWalletInfo(owner, b, deposit)
    testInfo = getWalletInfo()
    print(f'Valid: {validInfo}')
    assert testInfo == validInfo

@pytest.mark.parametrize('value', [
    pytest.param(0, marks=pytest.mark.xfail),
    pytest.param(50, marks=pytest.mark.xfail),
    1000, 2000000])
def test_pay(walletContract, value):
    owner, b, contract = walletContract
    c = accounts[2]
    setWalletInfo(owner, b, value)
    validInfo = getWalletInfo()[-2] - (value / 100)
    validBalance = getWalletBalance() - value / 100
    pay(c, value / 100)
    # print(f'C balance: {c.balance}')
    newInfo = getWalletInfo()
    print(f'Info about Owner wei: {newInfo}')
    newBalance = getWalletBalance()
    assert validInfo == newInfo[-2]
    assert validBalance == newBalance

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

@pytest.mark.parametrize(
    'value, deposit', 
    [pytest.param((0, 0), "You aren't breaking the limit!", marks=pytest.mark.xfail), (200, 1000), (20000, 100000), pytest.param((30000, 5000000), "You aren't breaking the limit!", marks=pytest.mark.xfail)])
def test_breakingTheLimit(walletContract, value, deposit):
    owner, b, _ = walletContract
    c = accounts[2]
    setWalletInfo(owner, b, deposit)
    getWalletInfo()
    validBalance = getWalletBalance() - value
    setConsentToBreakLimit(owner)
    setConsentToBreakLimit(b)
    breakTheLimit(c, value)
    weiPerDay = getWalletInfo()[2]
    newBalance = getWalletBalance()
    assert value > weiPerDay
    assert newBalance == validBalance