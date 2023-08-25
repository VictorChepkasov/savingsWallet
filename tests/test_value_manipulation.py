import pytest
from brownie import accounts
from conftest import walletFactory
from scripts.scripts import (
    getSavingWallet,
    createWallet,
    setConsentToBreakLimit,
    pay,
    breakTheLimit,
    getWalletInfo,
    getWalletBalance,
)

# @pytest.mark.parametrize(
#     'value', [pytest.param(0, marks=pytest.mark.xfail),
#     pytest.param(50, marks=pytest.mark.xfail),
#     1000, 2000000]
# )
def test_pay(walletFactory, value=1000, walletId=1):
    owner, b, _ = walletFactory
    c = accounts[2]
    createWallet(owner, b, value)
    walletContract = getSavingWallet(walletId)
    validInfo = getWalletInfo(walletContract)
    validBalance = getWalletBalance(walletContract)
    print(f'Info about Owner wei: {validInfo[-2]}')
    value /= 100
    pay(owner, c, value, walletContract)
    assert getWalletInfo(walletContract)[-2] == validInfo[-2] - value
    assert getWalletBalance(walletContract) == validBalance - value

# @pytest.mark.parametrize(
#     'value, deposit', 
#     [pytest.param((0, 0), "You aren't breaking the limit!", marks=pytest.mark.xfail),
#     pytest.param((30000, 5000000), "You aren't breaking the limit!", marks=pytest.mark.xfail),
#     (200, 1000), (20000, 100000)]
# )
def test_breakingTheLimit(walletContract, value=200, deposit=1000):
    owner, b, _ = walletContract
    c = accounts[2]
    createWallet(owner, b, deposit)
    getWalletInfo()
    validBalance = getWalletBalance() - value
    setConsentToBreakLimit(owner)
    setConsentToBreakLimit(b)
    breakTheLimit(c, value)
    weiPerDay = getWalletInfo()[2]
    newBalance = getWalletBalance()
    assert value > weiPerDay
    assert validBalance == newBalance