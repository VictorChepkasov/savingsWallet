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

pytestmark = pytest.mark.parametrize('deposit', [0, 100, 200000])

def test_setWalletInfo(walletContract, deposit):
    owner, b, _ = walletContract
    deploySavingWallet(owner)
    validInfo = [owner.address, b.address, deposit // 100,
        chain.time() // 3600, False, deposit // 100, deposit // 100]
    setWalletInfo(owner, b, deposit)
    testInfo = getWalletInfo()
    testInfo[3] //= 3600
    print(f'Valid: {validInfo}')
    assert validInfo == testInfo

def test_blockPartyB(walletContract, deposit):
    owner, b, _ = walletContract
    setWalletInfo(owner, b, deposit)
    validBalance = int(str(owner.balance())[:-9])
    blockPartyB()
    newInfo = getWalletInfo()[-3]
    ownerBalance = int(str(owner.balance())[:-9])
    assert validBalance == ownerBalance
    assert True == newInfo

def test_updateLimit(walletContract, deposit):
    owner, b, _ = walletContract
    setWalletInfo(owner, b, deposit)
    validInfo = getWalletInfo()
    validInfo = [validInfo[-1], validInfo[-2]]
    chain.sleep(86401)
    updateLimit()
    newInfo = getWalletInfo()
    newInfo = [newInfo[-1], newInfo[-2]]
    assert validInfo == newInfo

def test_updateWalletBalance(walletContract, deposit):
    owner, b, _ = walletContract
    initialDeposit = 500
    setWalletInfo(owner, b, initialDeposit)
    validBalance = initialDeposit + deposit
    chain.sleep(86401)
    updateWalletBalance(deposit)
    newBalance = getWalletBalance()
    assert validBalance == newBalance

