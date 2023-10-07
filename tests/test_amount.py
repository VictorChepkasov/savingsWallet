import pytest
from brownie import chain
from conftest import *
from test_breakingTheLimit import setEnvironment
from scripts.savingsWalletFactoryScripts import approve
from scripts.savingsWalletClass import *
pytestmark = pytest.mark.parametrize(
    'amount',
    [pytest.param(0, marks=pytest.mark.xfail), 1000]
)

def test_createWallet(WETHFactory, walletsFactory, amount):
    owner, b, _, walletsFactory, weth, wallet, ownerBalance = setEnvironment(WETHFactory, walletsFactory, amount)
    walletBalance = weth.balanceOf(wallet.address)

    validInfo = [owner.address, b.address, walletsFactory.walletsCounter(), amount // 100, chain.time() // 3600, False, amount // 100, amount // 100]
    print(f'Valid: {validInfo}')

    testInfo = wallet.getWalletInfo()
    testInfo[4] //= 3600

    assert validInfo == testInfo
    assert walletBalance == amount
    assert ownerBalance == weth.balanceOf(owner)

def test_pay(WETHFactory, walletsFactory, amount):
    owner, _, c, walletsFactory, weth, wallet, ownerBalance = setEnvironment(WETHFactory, walletsFactory, amount*100)
    
    validInfo = wallet.getWalletInfo()
    validBalance = wallet.getWalletBalance()

    owner.transfer(wallet.address, '1000 gwei', priority_fee='10 wei')
    wallet.pay(c, amount)

    assert wallet.getWalletInfo()[-2] == validInfo[-2] - amount
    assert wallet.getWalletBalance() == validBalance - amount
    assert ownerBalance == weth.balanceOf(owner)

def test_blockPartyB(WETHFactory, walletsFactory, amount):
    owner, _, _, walletsFactory, weth, wallet, ownerBalance = setEnvironment(WETHFactory, walletsFactory, amount)
    walletBalance = weth.balanceOf(wallet.address)

    wallet.blockPartyB()
    newInfo = wallet.getWalletInfo()[-3]

    assert ownerBalance + walletBalance == weth.balanceOf(owner)
    assert True == newInfo
    assert weth.balanceOf(wallet.address) == 0

def test_updateLimit(WETHFactory, walletsFactory, amount):
    owner, _, _, walletsFactory, _, wallet, _ = setEnvironment(WETHFactory, walletsFactory, amount)
        
    validInfo = wallet.getWalletInfo()[-2:]
    print(f'Valid info: {validInfo}')
    
    chain.sleep(86401)
    wallet.updateLimit()

    assert validInfo == wallet.getWalletInfo()[-2:]

def test_updateWalletBalance(WETHFactory, walletsFactory, amount):
    owner, _, _, walletsFactory, weth, wallet, ownerBalance = setEnvironment(WETHFactory, walletsFactory, amount)

    initialAmount = 500
    validInfo = [i + initialAmount // 100 for i in wallet.getWalletInfo()[-2:]]

    approve(owner, wallet.address, initialAmount)
    wallet.updateWalletBalance(initialAmount)

    assert initialAmount + amount == wallet.getWalletBalance()
    assert ownerBalance - initialAmount == weth.balanceOf(owner) 
    assert validInfo == wallet.getWalletInfo()[-2:]