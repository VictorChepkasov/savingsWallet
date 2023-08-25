import pytest
from brownie import accounts, WrappedETH
from conftest import walletsFactory, WETHFactory
from scripts.scripts import (
    approve,
    pay,
    buyWETH,
    createWallet,
    setConsentToBreakLimit,
    breakTheLimit,
    getSavingWallet,
    getWalletInfo,
    getWalletBalance
)

def test_pay(WETHFactory, walletsFactory, amount=1000, walletId=1):
    owner, b, factory = walletsFactory
    c = accounts[2]

    buyWETH(owner, WETHFactory.address, amount*2)

    approve(owner, factory.address, amount)
    createWallet(WETHFactory.token(), owner, b, amount)
    
    walletContract = getSavingWallet(walletId)
    validInfo = getWalletInfo(owner, walletContract)
    validBalance = getWalletBalance(walletContract)

    # owner.transfer(walletContract.address, '1000 gwei', priority_fee='10 wei')
    approve(owner, walletContract.address, 200)
    print(f'Owner balance: {WrappedETH.at(WETHFactory.token()).balanceOf(owner)}')

    walletContract.pay(c, 5, {
        'from': owner,
        'priority_fee': '10 wei'
    })

    assert getWalletInfo(owner, walletContract)[-2] == validInfo[-2]-amount//100
    assert getWalletBalance(walletContract) == validBalance-amount//100

# @pytest.mark.parametrize(
#     'value', [pytest.param(0, marks=pytest.mark.xfail),
#     pytest.param(50, marks=pytest.mark.xfail),
#     1000, 2000000]
# )
# def test_pay_old(walletsFactory, value=1000, walletId=1):
#     owner, b, _ = walletsFactory
#     c = accounts[2]
#     createWallet(owner, b, value)
#     walletContract = getSavingWallet(walletId)
#     validInfo = getWalletInfo(walletContract)
#     validBalance = getWalletBalance(walletContract)
#     print(f'Info about Owner wei: {validInfo[-2]}')
#     value /= 100
#     pay(owner, c, value, walletContract)
#     assert getWalletInfo(walletContract)[-2] == validInfo[-2] - value
#     assert getWalletBalance(walletContract) == validBalance - value

# @pytest.mark.parametrize(
#     'value, deposit', 
#     [pytest.param((0, 0), "You aren't breaking the limit!", marks=pytest.mark.xfail),
#     pytest.param((30000, 5000000), "You aren't breaking the limit!", marks=pytest.mark.xfail),
#     (200, 1000), (20000, 100000)]
# )
# def test_breakingTheLimit(walletContract, value=200, deposit=1000):
#     owner, b, _ = walletContract
#     c = accounts[2]
#     createWallet(owner, b, deposit)
#     getWalletInfo()
#     validBalance = getWalletBalance() - value
#     setConsentToBreakLimit(owner)
#     setConsentToBreakLimit(b)
#     breakTheLimit(c, value)
#     weiPerDay = getWalletInfo()[2]
#     newBalance = getWalletBalance()
#     assert value > weiPerDay
#     assert validBalance == newBalance