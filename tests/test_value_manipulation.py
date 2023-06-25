import pytest
from brownie import accounts
from scripts.deploySavingWallet import deploySavingWallet
from scripts.scripts import (
    setWalletInfo,
    setConsentToBreakLimit,
    pay,
    breakTheLimit,
    getWalletInfo,
    getWalletBalance,
)

@pytest.fixture(autouse=True)
def walletContract():
    owner = accounts[0]
    b = accounts[1]
    contract = deploySavingWallet(owner)
    return owner, b, contract

@pytest.mark.parametrize('value', [
    pytest.param(0, marks=pytest.mark.xfail),
    pytest.param(50, marks=pytest.mark.xfail),
    1000, 2000000])
def test_pay(walletContract, value):
    owner, b, _ = walletContract
    c = accounts[2]
    setWalletInfo(owner, b, value)
    validInfo = getWalletInfo()[-2] - (value / 100)
    validBalance = getWalletBalance() - value / 100
    pay(c, value / 100)
    newInfo = getWalletInfo()
    print(f'Info about Owner wei: {newInfo}')
    newBalance = getWalletBalance()
    assert validInfo == newInfo[-2]
    assert validBalance == newBalance

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