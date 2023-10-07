import pytest
from brownie import accounts, WrappedETH
from conftest import *
from scripts.savingsWalletFactoryScripts import (
    getSavingWallet,
    approve,
    buyWETH,
    createWallet
)
from scripts.savingsWalletClass import *

def setEnvironment(_WETHFactory, _walletsFactory, _amount):
    owner, b, walletsFactory = _walletsFactory
    c = accounts[2]
    # получаю контаркт WETH
    weth = WrappedETH.at(_WETHFactory.token())

    # оборачиваю эфир
    buyWETH(owner, _WETHFactory.address, _amount)
    
    # разрешаю фабрике кошельков тратить n токенов владельца кошелька
    approve(owner, walletsFactory.address, _amount)
    walletId = createWallet(_WETHFactory.token(), owner, b, _amount)
    wallet = SavingsWallet(getSavingWallet(owner, walletId))
    ownerBalance = weth.balanceOf(owner)

    return owner, b, c, walletsFactory, weth, wallet, ownerBalance

@pytest.mark.parametrize(
    'value, amount', 
    [pytest.param((0, 0), "You aren't breaking the limit!", marks=pytest.mark.xfail),
    pytest.param((30000, 5000000), "You aren't breaking the limit!", marks=pytest.mark.xfail),
    (200, 1000)]
)
def test_breakingTheLimit(WETHFactory, walletsFactory, value, amount):
    owner, b, c, walletsFactory, weth, wallet, ownerBalance = setEnvironment(WETHFactory, walletsFactory, amount)

    validBalance = wallet.getWalletBalance() - value

    # стороны соглашаются потратить больше обозначенной суммы
    wallet.setConsentToBreakLimit(owner)
    wallet.setConsentToBreakLimit(b)
    
    wallet.breakTheLimit(c, value)
    weiPerDay = wallet.getWalletInfo()[2]

    assert value > weiPerDay
    assert validBalance == wallet.getWalletBalance()
    assert ownerBalance == weth.balanceOf(owner)