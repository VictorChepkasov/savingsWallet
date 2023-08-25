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

@pytest.mark.parametrize(
    'amount', [
        pytest.param(0, marks=pytest.mark.xfail),
        1000,
        2000000
    ]
)
def test_pay(WETHFactory, walletsFactory, amount):
    owner, b, walletsFactory = walletsFactory
    c = accounts[2]
    weth = WrappedETH.at(WETHFactory.token())

    buyWETH(owner, WETHFactory.address, amount*100)

    approve(owner, walletsFactory.address, amount*100)
    createWallet(WETHFactory.token(), owner, b, amount*100)
    ownerBalance = weth.balanceOf(owner)
    
    walletContract = getSavingWallet(walletsFactory.walletsCounter())
    validInfo = getWalletInfo(owner, walletContract)
    validBalance = getWalletBalance(walletContract)

    owner.transfer(walletContract.address, '1000 gwei', priority_fee='10 wei')
    pay(owner, c, amount, walletContract)

    assert getWalletInfo(owner, walletContract)[-2] == validInfo[-2] - amount
    assert getWalletBalance(walletContract) == validBalance - amount
    assert ownerBalance == weth.balanceOf(owner)

@pytest.mark.parametrize(
    'value, amount', 
    [pytest.param((0, 0), "You aren't breaking the limit!", marks=pytest.mark.xfail),
    pytest.param((30000, 5000000), "You aren't breaking the limit!", marks=pytest.mark.xfail),
    (200, 1000), (20000, 100000)]
)
def test_breakingTheLimit(WETHFactory, walletsFactory, value, amount):
    owner, b, walletsFactory = walletsFactory
    c = accounts[2]
    weth = WrappedETH.at(WETHFactory.token())

    buyWETH(owner, WETHFactory.address, amount)

    approve(owner, walletsFactory.address, amount)
    createWallet(WETHFactory.token(), owner, b, amount)

    walletContract = getSavingWallet(walletsFactory.walletsCounter())
    validBalance = getWalletBalance(walletContract) - value
    ownerBalance = weth.balanceOf(owner)

    setConsentToBreakLimit(owner, walletContract)
    setConsentToBreakLimit(b, walletContract)
    
    breakTheLimit(owner, c, value, walletContract)
    weiPerDay = getWalletInfo(owner, walletContract)[2]

    assert value > weiPerDay
    assert validBalance == getWalletBalance(walletContract)
    assert ownerBalance == weth.balanceOf(owner)