import pytest
from brownie import chain
from scripts.deploySavingWallet import deploySavingWallet
from scripts.scripts import (
    setWalletInfo,
    blockPartyB,
    updateWalletBalance,
    updateLimit,
    getWalletInfo,
    getWalletBalance,
)

pytestmark = pytest.mark.parametrize('amount', [0, 100, 200000])

def test_setWalletInfo(walletContract, amount):
    owner, b, _ = walletContract
    deploySavingWallet(owner)
    validInfo = [owner.address, b.address, amount // 100,
        chain.time() // 3600, False, amount // 100, amount // 100]
    setWalletInfo(owner, b, amount)
    testInfo = getWalletInfo()
    testInfo[3] //= 3600
    print(f'Valid: {validInfo}')
    assert validInfo == testInfo

def test_blockPartyB(walletContract, amount):
    owner, b, _ = walletContract
    setWalletInfo(owner, b, amount)
    validBalance = int(str(owner.balance())[:-9])
    blockPartyB()
    newInfo = getWalletInfo()[-3]
    ownerBalance = int(str(owner.balance())[:-9])
    assert validBalance == ownerBalance
    assert True == newInfo

def test_updateLimit(walletContract, amount):
    owner, b, _ = walletContract
    setWalletInfo(owner, b, amount)
    validInfo = getWalletInfo()
    validInfo = [validInfo[-1], validInfo[-2]]
    chain.sleep(86401)
    updateLimit()
    newInfo = getWalletInfo()
    newInfo = [newInfo[-1], newInfo[-2]]
    assert validInfo == newInfo

def test_updateWalletBalance(walletContract, amount):
    owner, b, _ = walletContract
    initialamount = 500
    setWalletInfo(owner, b, initialamount)
    validBalance = initialamount + amount
    chain.sleep(86401)
    updateWalletBalance(amount)
    newBalance = getWalletBalance()
    assert validBalance == newBalance

