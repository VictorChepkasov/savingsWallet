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

def setEnvironment(_WETHFactory, _walletsFactory, _amount):
    owner, b, walletsFactory = _walletsFactory
    c = accounts[2]
    # получаю контаркт WETH
    weth = WrappedETH.at(_WETHFactory.token())

    # оборачиваю эфир
    buyWETH(owner, _WETHFactory.address, _amount)
    
    # разрешаю фабрике кошельков тратить n токенов владельца кошелька
    approve(owner, walletsFactory.address, _amount)
    createWallet(_WETHFactory.token(), owner, b, _amount)
    ownerBalance = weth.balanceOf(owner)
    walletContract = getSavingWallet(walletsFactory.walletsCounter())

    return owner, b, c, walletsFactory, weth, walletContract, ownerBalance

@pytest.mark.parametrize(
    'amount', [
        pytest.param(0, marks=pytest.mark.xfail),
        1000,
        2000000
    ]
)
def test_pay(WETHFactory, walletsFactory, amount):
    owner, _, c, walletsFactory, weth, walletContract, ownerBalance = setEnvironment(WETHFactory, walletsFactory, amount*100)
    
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
    owner, b, c, walletsFactory, weth, walletContract, ownerBalance = setEnvironment(WETHFactory, walletsFactory, amount)

    validBalance = getWalletBalance(walletContract) - value

    # стороны соглашаются потратить больше обозначенной суммы
    setConsentToBreakLimit(owner, walletContract)
    setConsentToBreakLimit(b, walletContract)
    
    breakTheLimit(owner, c, value, walletContract)
    weiPerDay = getWalletInfo(owner, walletContract)[2]

    assert value > weiPerDay
    assert validBalance == getWalletBalance(walletContract)
    assert ownerBalance == weth.balanceOf(owner)