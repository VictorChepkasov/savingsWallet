import pytest
from brownie import chain
from conftest import *
from scripts.scripts import (
    getWalletInfo,
    getWalletBalance,
    updateLimit,
    updateWalletBalance,
    approve,
    pay,
    blockPartyB
)
from test_breakingTheLimit import setEnvironment

pytestmark = pytest.mark.parametrize(
    'amount',
    [pytest.param(0, marks=pytest.mark.xfail), 100, 200000]
)

def test_createWallet(WETHFactory, walletsFactory, amount):
    owner, b, _, walletsFactory, weth, walletContract, ownerBalance = setEnvironment(WETHFactory, walletsFactory, amount)
    walletBalance = weth.balanceOf(walletContract)

    validInfo = [owner.address, b.address, walletsFactory.walletsCounter(), amount // 100, chain.time() // 3600, False, amount // 100, amount // 100]
    print(f'Valid: {validInfo}')

    testInfo = getWalletInfo(owner, walletContract)
    testInfo[4] //= 3600

    assert validInfo == testInfo
    assert walletBalance == amount
    assert ownerBalance == weth.balanceOf(owner)

def test_pay(WETHFactory, walletsFactory, amount):
    owner, _, c, walletsFactory, weth, walletContract, ownerBalance = setEnvironment(WETHFactory, walletsFactory, amount*100)
    
    validInfo = getWalletInfo(owner, walletContract)
    validBalance = getWalletBalance(walletContract)

    owner.transfer(walletContract.address, '1000 gwei', priority_fee='10 wei')
    pay(owner, c, amount, walletContract)

    assert getWalletInfo(owner, walletContract)[-2] == validInfo[-2] - amount
    assert getWalletBalance(walletContract) == validBalance - amount
    assert ownerBalance == weth.balanceOf(owner)

def test_blockPartyB(WETHFactory, walletsFactory, amount):
    owner, _, _, walletsFactory, weth, walletContract, ownerBalance = setEnvironment(WETHFactory, walletsFactory, amount)
    walletBalance = weth.balanceOf(walletContract)

    blockPartyB(owner, walletContract)
    newInfo = getWalletInfo(owner, walletContract)[-3]

    assert ownerBalance + walletBalance == weth.balanceOf(owner)
    assert True == newInfo
    assert weth.balanceOf(walletContract) == 0

def test_updateLimit(WETHFactory, walletsFactory, amount):
    owner, _, _, walletsFactory, weth, walletContract, ownerBalance = setEnvironment(WETHFactory, walletsFactory, amount)
        
    validInfo = getWalletInfo(owner, walletContract)[-2:]
    print(f'Valid info: {validInfo}')
    
    chain.sleep(86401)
    updateLimit(owner, walletContract)

    assert validInfo == getWalletInfo(owner, walletContract)[-2:]

def test_updateWalletBalance(WETHFactory, walletsFactory, amount):
    owner, _, _, walletsFactory, weth, walletContract, ownerBalance = setEnvironment(WETHFactory, walletsFactory, amount)

    initialAmount = 500
    validInfo = [i + initialAmount // 100 for i in getWalletInfo(owner, walletContract)[-2:]]

    approve(owner, walletContract.address, initialAmount)
    updateWalletBalance(owner, initialAmount, walletContract)

    assert initialAmount + amount == getWalletBalance(walletContract)
    assert ownerBalance - initialAmount == weth.balanceOf(owner) 
    assert validInfo == getWalletInfo(owner, walletContract)[-2:]